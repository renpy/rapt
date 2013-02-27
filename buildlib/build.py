#!/usr/bin/env python2.7

import sys
sys.path.insert(0, 'buildlib/jinja2.egg')
sys.path.insert(0, 'buildlib')

# import zlib
# zlib.Z_DEFAULT_COMPRESSION = 9

import tarfile
import os
import shutil
import subprocess
import time

import jinja2
import configure

import plat

# Are we doing a Ren'Py build?
RENPY = os.path.exists("private/renpy")

# If we have python 2.7, record the path to it.
if not RENPY and sys.version_info.major == 2 and sys.version_info.minor == 7:
    PYTHON = sys.executable
else:
    PYTHON = None

# Files and extensions we should not package.
BLACKLIST_FILES = [
    "icon.ico",
    "icon.icns",
    "android-icon.png",
    "android-presplash.png",
    "launcherinfo.py",
    ".nomedia",
    ".android.json",
    ]

BLACKLIST_EXTENSIONS = [
    "~",
    ".bak",
    ".rpy",
    ".swp",
    ".pyc",
    ]

BLACKLIST_DIRS = [
    ".hg",
    ".git",
    ".bzr",
    ".svn",
    ]

# Used by render.
environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

def render(template, dest, **kwargs):
    """
    Using jinja2, render `template` to the filename `dest`, supplying the keyword
    arguments as template parameters.
    """

    template = environment.get_template(template)
    text = template.render(**kwargs)

    f = file(dest, "wb")
    f.write(text.encode("utf-8"))
    f.close()
    
def compile_dir(dfn):
    """
    Compile *.py in directory `dfn` to *.pyo
    """

    # -OO = strip docstrings
    subprocess.call([PYTHON,'-OO','-m','compileall','-f',dfn])

def make_tar(fn, source_dirs):
    """
    Make a zip file `fn` from the contents of source_dis.
    """

    # zf = zipfile.ZipFile(fn, "w")
    tf = tarfile.open(fn, "w:gz")
    
    for sd in source_dirs:

        if PYTHON and not RENPY:
            compile_dir(sd)
    
        sd = os.path.abspath(sd)    
    
        for dir, dirs, files in os.walk(sd): #@ReservedAssignment
            for bd in BLACKLIST_DIRS:
                if bd in dirs:
                    dirs.remove(bd)

            for fn in dirs:
                fn = os.path.join(dir, fn)
                relfn = os.path.relpath(fn, sd)
                tf.add(fn, relfn, recursive=False)

            for fn in files:        
                fn = os.path.join(dir, fn)
                relfn = os.path.relpath(fn, sd)

                bl = False
                for e in BLACKLIST_EXTENSIONS:
                    if relfn.endswith(e):
                        bl = True

                if bl:
                    continue

                if relfn in BLACKLIST_FILES:
                    continue

                tf.add(fn, relfn)

    # TODO: Fix me.
    # tf.writestr(".nomedia", "")
    tf.close()

def join_and_check(base, sub):
    """
    If base/sub is a directory, returns the joined path. Otherwise, return None.
    """
    
    rv = os.path.join(base, sub)
    if os.path.exists(rv):
        return rv
    
    return None
    
def build_core(iface, directory, commands):

    global BLACKLIST_DIRS
    global BLACKLIST_FILES

    if not os.path.isdir(directory):
        iface.fail("{} is not a directory.".format(directory))

    if RENPY and not os.path.isdir(os.path.join(directory, "game")):
        iface.fail("{} does not contain a Ren'Py game.".format(directory))

    config = configure.Configuration(directory)
    if config.package is None:
        iface.fail("Run configure before attempting to build the app.")

    if not config.include_sqlite:
        BLACKLIST_DIRS += ['sqlite3']
        BLACKLIST_FILES += ['_sqlite3.so']
        shelve_lib('libsqlite3.so')

    if not config.include_pil:
        BLACKLIST_DIRS += ['PIL']
        BLACKLIST_FILES += ['_imaging.so','_imagingft.so','_imagingmath.so']
    
    if not RENPY and not config.source:
        if not PYTHON:
            iface.fail("Can't compile Python source, and not including python source. Giving up.")
            
        BLACKLIST_EXTENSIONS.append(".py")
    
    if RENPY:
        manifest_extra = '<uses-feature android:glEsVersion="0x00020000" />'        
        default_icon = "templates/renpy-icon.png"
        default_presplash = "templates/renpy-presplash.jpg"

        public_dir = None
        private_dir = None
        assets_dir = directory
    
    else:
        manifest_extra = ""
        default_icon = "templates/pygame-icon.png"
        default_presplash = "templates/pygame-presplash.jpg"
        
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
        os.unlink("build.xml")
    except:
        pass
        
    iface.info("Updating build files.")
        
    # Update the project to a recent version.
    subprocess.call([plat.android, "update", "project", "-p", '.', '-t', 'android-8', '-n', versioned_name])

    iface.info("Creating assets directory.")

    if os.path.isdir("assets"):
        shutil.rmtree("assets")
    
    if assets_dir is not None:
        shutil.copytree(assets_dir, "assets")
    else:
        os.mkdir("assets")

    # Copy in the Ren'Py common assets.
    if os.path.exists("engine-assets/common"):
        shutil.copytree("engine-assets/common", "assets/common")

        # Ren'Py uses a lot of names that don't work as assets. Auto-rename
        # them.
        for dirpath, dirnames, filenames in os.walk("assets", topdown=False):
            
            for fn in filenames + dirnames:
                if fn[0] == ".":
                    continue
                
                old = os.path.join(dirpath, fn)
                new = os.path.join(dirpath, "x-" + fn)
                
                os.rename(old, new)

    iface.info("Packaging internal data.")

    private_dirs = [ 'private' ]

    if private_dir is not None:
        private_dirs.append(private_dir)
        
    if os.path.exists("engine-private"):
        private_dirs.append("engine-private")

    make_tar("assets/private.mp3", private_dirs)
    
    if public_dir is not None:
        iface.info("Packaging external data.")
        make_tar("assets/public.mp3", [ public_dir ])

    # Copy over the icon and presplash files.
    shutil.copy(join_and_check(directory, "android-icon.png") or default_icon, "res/drawable/icon.png")
    shutil.copy(join_and_check(directory, "android-presplash.jpg") or default_presplash, "res/drawable/presplash.jpg")

    # Build.
    iface.info("I'm using Ant to build the package.")

    # Clean is required 
    try:   
        subprocess.check_call([plat.ant, "clean"] +  commands)
        iface.success("It looks like the build succeeded.")
    except:
        iface.fail("The build seems to have failed.")


def shelve_lib(lfn):
    for root, _dirs, files in os.walk('libs'):
        for fn in files:
            if fn == lfn:
                shelf_dir = os.path.join('.shelf', root)
                if not os.path.exists(shelf_dir):
                    os.makedirs(shelf_dir)
                shutil.move(os.path.join(root,fn), shelf_dir)


def unshelve_libs():
    if os.path.exists('.shelf'):
        for root, _dirs, files in os.walk('.shelf'):
            for fn in files:
                lib_dir = root[len('.shelf/'):]
                shutil.move(os.path.join(root,fn), lib_dir)
        shutil.rmtree('.shelf')


def build(iface, directory, commands):
    try:
        build_core(iface, directory, commands)
    finally:
        unshelve_libs()

