#!/usr/bin/env python2.7

import sys

import re
import tarfile
import os
import shutil
import time
import zipfile
import subprocess

import rapt.plat as plat

sys.path.append(os.path.join(plat.RAPT_PATH, "buildlib", "jinja2.egg"))

import jinja2
import rapt.configure as configure

# If we have python 2.7, record the path to it.
if sys.version_info.major == 2 and sys.version_info.minor == 7:
    PYTHON = sys.executable
else:
    PYTHON = None

class PatternList(object):
    """
    Used to load in the blacklist and whitelist patterns.
    """

    def __init__(self, *args):
        self.patterns = [ ]

        for i in args:
            self.load(plat.path(i))

    def match(self, s):
        """
        Matches the patterns against s. Returns true if they match, False
        otherwise.
        """

        slash_s = "/" + s

        for p in self.patterns:
            if p.match(s):
                return True
            if p.match(slash_s):
                return  True

        return False


    def load(self, fn):

        with open(fn, "r") as f:
            for l in f:
                l = l.strip()
                if not l:
                    continue

                if l.startswith("#"):
                    continue

                self.patterns.append(self.compile(l))

    def compile(self, pattern):
        """
        Compiles a pattern into a regex object.
        """

        regexp = ""

        while pattern:
            if pattern.startswith("**"):
                regexp += r'.*'
                pattern = pattern[2:]
            elif pattern[0] == "*":
                regexp += r'[^/]*'
                pattern = pattern[1:]
            elif pattern[0] == '[':
                regexp += r'['
                pattern = pattern[1:]

                while pattern and pattern[0] != ']':
                    regexp += pattern[0]
                    pattern = pattern[1:]

                pattern = pattern[1:]
                regexp += ']'

            else:
                regexp += re.escape(pattern[0])
                pattern = pattern[1:]

        regexp += "$"

        return re.compile(regexp, re.I)



# Used by render.
environment = jinja2.Environment(loader=jinja2.FileSystemLoader(plat.path('templates')))

def render(template, dest, **kwargs):
    """
    Using jinja2, render `template` to the filename `dest`, supplying the keyword
    arguments as template parameters.
    """

    dest = plat.path(dest)

    template = environment.get_template(template)
    text = template.render(**kwargs)

    f = file(dest, "wb")
    f.write(text.encode("utf-8"))
    f.close()

def compile_dir(iface, dfn):
    """
    Compile *.py in directory `dfn` to *.pyo
    """

    # -OO = strip docstrings
    iface.call([PYTHON,'-OO','-m','compileall','-f',dfn])

def make_tar(fn, source_dirs):
    """
    Make a zip file `fn` from the contents of source_dis.
    """

    source_dirs = [ plat.path(i) for i in source_dirs ]

    def include(fn):
        rv = True

        if blacklist.match(fn):
            rv = False

        if whitelist.match(fn):
            rv = True

        return rv

    # zf = zipfile.ZipFile(fn, "w")
    tf = tarfile.open(fn, "w:gz")

    added = set()

    def add(fn, relfn):

        adds = [ ]

        while relfn:
            adds.append((fn, relfn))
            fn = os.path.dirname(fn)
            relfn = os.path.dirname(relfn)

        adds.reverse()

        for fn, relfn in adds:

            if relfn not in added:
                added.add(relfn)
                tf.add(fn, relfn, recursive=False)


    for sd in source_dirs:

        if PYTHON and not RENPY:
            compile_dir(iface, sd)

        sd = os.path.abspath(sd)

        for dir, dirs, files in os.walk(sd): #@ReservedAssignment

            for _fn in dirs:
                fn = os.path.join(dir, _fn)
                relfn = os.path.relpath(fn, sd)

                if include(relfn):
                    add(fn, relfn)

            for fn in files:
                fn = os.path.join(dir, fn)
                relfn = os.path.relpath(fn, sd)

                if include(relfn):
                    add(fn, relfn)

    tf.close()

def make_tree(src, dest):

    src = plat.path(src)
    dest = plat.path(dest)

    def ignore(dir, files):

        rv = [ ]

        for basename in files:
            fn = os.path.join(dir, basename)
            relfn = os.path.relpath(fn, src)

            ignore = False

            if blacklist.match(relfn):
                ignore = True
            if whitelist.match(relfn):
                ignore = False

            if ignore:
                rv.append(basename)

        return rv

    shutil.copytree(src, dest, ignore=ignore)

def join_and_check(base, sub):
    """
    If base/sub is a directory, returns the joined path. Otherwise, return None.
    """

    rv = os.path.join(base, sub)
    if os.path.exists(rv):
        return rv

    return None


def edit_file(fn, pattern, line):
    """
    Replaces lines in `fn` that begin with `pattern` with `line`. `line`
    should not end with a newline - we add it.
    """

    fn = plat.path(fn)

    lines = [ ]

    with open(fn, "r") as f:
        for l in f:

            if re.match(pattern, l):
                l = line + "\n"

            lines.append(l)

    with open(fn, "w") as f:
        f.write(''.join(lines))

def zip_directory(zf, dirname):
    """
    Zips up the directory with `dirname`. `zf` is the file to place the
    contents of the directory into.
    """

    dirname = plat.path(dirname)

    for dirname, dirs, files in os.walk(dirname):
        for fn in files:
            fn = os.path.join(dirname, fn)
            zf.write(fn)

def copy_icon(directory, name, default):
    """
    Copys icon or presplash files ending with `name` found in `directory` to
    the appropriate res/drawables directory. If the file doesn't exist,
    copies in default instead.
    """

    def copy(src, dst):
        try:
            os.makedirs(os.path.dirname(dst))
        except:
            pass

        shutil.copy(src, dst)

    res = plat.path("res")

    # Clean out old files.
    for i in os.listdir(res):
        if not i.startswith("drawable"):
            continue

        fn = os.path.join(res, i, name)

        if os.path.exists(fn):
            os.unlink(fn)

    found = False

    # Copy files, if any are found.
    for i in os.listdir(directory):

        fullfn = os.path.join(directory, i)
        fn = i.lower()

        if not fn.startswith("android-"):
            continue

        if not fn.endswith("-" + name):
            continue

        prefix, rest = fn.split("-", 1)

        if "-" in rest:
            selector, _name = rest.rsplit("-", 1)

            if selector not in [ "ldpi", "mdpi", "hdpi", "xhdpi", "xxhdpi", "tvdpi" ]:
                continue

            dest = os.path.join(res, "drawable-" + selector, name)
        else:
            dest = os.path.join(res, "drawable", rest)

        copy(fullfn, dest)

        found = True


    if found:
        return

    # If no files are found, copy over the default.
    copy(default, os.path.join(res, "drawable", name))




def build(iface, directory, commands):

    # Are we doing a Ren'Py build?

    global RENPY
    RENPY = os.path.exists(plat.path("renpy"))

    if not os.path.isdir(directory):
        iface.fail("{} is not a directory.".format(directory))

    if RENPY and not os.path.isdir(os.path.join(directory, "game")):
        iface.fail("{} does not contain a Ren'Py game.".format(directory))


    config = configure.Configuration(directory)
    if config.package is None:
        iface.fail("Run configure before attempting to build the app.")


    global blacklist
    global whitelist

    blacklist = PatternList("blacklist.txt")
    whitelist = PatternList("whitelist.txt")

    if RENPY:
        manifest_extra = None
        default_icon = plat.path("templates/renpy-icon.png")
        default_presplash = plat.path("templates/renpy-presplash.jpg")

        public_dir = None
        private_dir = None
        assets_dir = directory

    else:
        manifest_extra = ""
        default_icon = plat.path("templates/pygame-icon.png")
        default_presplash = plat.path("templates/pygame-presplash.jpg")

        if config.layout == "internal":
            private_dir = directory
            public_dir = None
            assets_dir = None
        elif config.layout == "external":
            private_dir = None
            public_dir = directory
            assets_dir = None
        elif config.layout == "split":
            private_dir = join_and_check(directory, "internal")
            public_dir = join_and_check(directory, "external")
            assets_dir = join_and_check(directory, "assets")

    versioned_name = config.name.replace(" ", "").replace("'", "") + "-" + config.version

    # Annoying fixups.
    config.name = config.name.replace("'", "\\'")
    config.icon_name = config.icon_name.replace("'", "\\'")

    # Figure out versions of the private and public data.
    private_version = str(time.time())

    if public_dir:
        public_version = private_version
    else:
        public_version = None

    # Render the various templates into control files.
    render(
        "AndroidManifest.tmpl.xml",
        "AndroidManifest.xml",
        config = config,
        manifest_extra = manifest_extra,
        )

    render(
        "strings.xml",
        "res/values/strings.xml",
        public_version = public_version,
        private_version = private_version,
        config = config)

    try:
        os.unlink(plat.path("build.xml"))
    except:
        pass

    iface.info("Updating source code.")

    edit_file("src/org/renpy/android/DownloaderActivity.java", r'import .*\.R;', 'import {}.R;'.format(config.package))

    iface.info("Updating build files.")

    # Update the project to a recent version.
    iface.call([plat.android, "update", "project", "-p", '.', '-t', 'android-8', '-n', versioned_name,
        # "--library", "android-sdk/extras/google/play_licensing/library",
        "--library", "android-sdk/extras/google/play_apk_expansion/downloader_library",
        ])


    iface.info("Creating assets directory.")

    if os.path.isdir(plat.path("assets")):
        shutil.rmtree(plat.path("assets"))

    def make_assets():

        if assets_dir is not None:
            make_tree(assets_dir, plat.path("assets"))
        else:
            os.mkdir(plat.path("assets"))

        # Copy in the Ren'Py common assets.
        if os.path.exists(plat.path("renpy/common")):

            if os.path.isdir(plat.path("assets/common")):
                shutil.rmtree(plat.path("assets/common"))

            make_tree("renpy/common", "assets/common")

            # Ren'Py uses a lot of names that don't work as assets. Auto-rename
            # them.
            for dirpath, dirnames, filenames in os.walk(plat.path("assets"), topdown=False):

                for fn in filenames + dirnames:
                    if fn[0] == ".":
                        continue

                    old = os.path.join(dirpath, fn)
                    new = os.path.join(dirpath, "x-" + fn)

                    plat.rename(old, new)

    iface.background(make_assets)

    if config.expansion:
        iface.info("Creating expansion file.")
        expansion_file = "main.{}.{}.obb".format(config.numeric_version, config.package)

        def make_expansion():

            zf = zipfile.ZipFile(plat.path(expansion_file), "w", zipfile.ZIP_STORED)
            zip_directory(zf, "assets")
            zf.close()

            # Delete and re-make the assets directory.
            shutil.rmtree(plat.path("assets"))
            os.mkdir(plat.path("assets"))

        iface.background(make_expansion)

        # Write the file size into DownloaderActivity.
        file_size = os.path.getsize(plat.path(expansion_file))

        edit_file("src/org/renpy/android/DownloaderActivity.java",
            r'    private int fileVersion =',
            '    private int fileVersion = {};'.format(config.numeric_version))

        edit_file("src/org/renpy/android/DownloaderActivity.java",
            r'    private int fileSize =',
            '    private int fileSize = {};'.format(file_size))

    else:
        expansion_file = None

    # Update the GP key and salt.
    if config.google_play_key:
        edit_file("src/org/renpy/android/DownloaderService.java",
            r'    private static final String BASE64_PUBLIC_KEY',
            '    private static final String BASE64_PUBLIC_KEY = "%s";' % config.google_play_key)

    if config.google_play_salt:
        edit_file("src/org/renpy/android/DownloaderService.java",
            r'    private static final byte\[\] SALT',
            '    private static final byte[] SALT = new byte[] { %s };' % config.google_play_salt)


    iface.info("Packaging internal data.")

    private_dirs = [ 'private' ]

    if private_dir is not None:
        private_dirs.append(private_dir)

    if os.path.exists(plat.path("engine-private")):
        private_dirs.append(plat.path("engine-private"))

    def pack():
        make_tar(plat.path("assets/private.mp3"), private_dirs)

    iface.background(pack)

    if public_dir is not None:
        iface.info("Packaging external data.")
        make_tar(plat.path("assets/public.mp3"), [ public_dir ])

    # Copy over the icon and presplash files.
    copy_icon(directory, "icon.png", default_icon)
    copy_icon(directory, "presplash.jpg", default_presplash)

    # Copy over the OUYA icon.
    ouya_icon = join_and_check(directory, "ouya-icon.png") or join_and_check(directory, "ouya_icon.png")

    if ouya_icon:
        if not os.path.exists(plat.path("res/drawable-xhdpi")):
            os.mkdir(plat.path("res/drawable-xhdpi"))

        shutil.copy(ouya_icon, plat.path("res/drawable-xhdpi/ouya_icon.png"))

    # Build.
    iface.info("I'm using Ant to build the package.")

    try:

        # Clean is required, so we don't use old code.
        iface.call([plat.ant, "clean"] +  commands, cancel=True)

        if (expansion_file is not None) and ("install" in commands):
            iface.info("Uploading expansion file.")

            dest = "/mnt/sdcard/{}".format(expansion_file)

            iface.call([ plat.adb, "push", plat.path(expansion_file), dest ], cancel=True)

        if expansion_file is not None:
            plat.rename(plat.path(expansion_file), plat.path("bin/" + expansion_file))

    except subprocess.CalledProcessError:
        iface.fail("The build seems to have failed.")

    iface.final_success("The build seems to have succeeded.")
