#!/usr/bin/env python

import traceback
import os
import zipfile
import tarfile
import shutil
import subprocess

import rapt.plat as plat


##############################################################################
def run(interface, *args, **kwargs):
    """
    Runs the supplied arguments.
    """

    try:
        interface.call(args, **kwargs)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def run_slow(interface, *args, **kwargs):
    """
    Runs the supplied arguments in a manner that lets the program
    be cancelled.
    """

    interface.call(args, cancel=True, **kwargs)
    return True


##############################################################################
def check_java(interface):
    """
    Checks for the presence of a minimally useful java on the user's system.
    """

    interface.info("""\
I'm compiling a short test program, to see if you have a working JDK on your
system.
""")

    SOURCE = """\
class test {
    public static void main(String args[]) {
    }
}
"""

    f = file(plat.path("test.java"), "w")
    f.write(SOURCE)
    f.close()

    if not run_slow(interface, plat.javac, "test.java", use_path=True):
        interface.fail("""\
I was unable to use javac to compile a test file. If you haven't installed
the Java Development Kit yet, please download it from:

http://www.oracle.com/technetwork/java/javase/downloads/index.html

The JDK is different from the JRE, so it's possible you have Java
without having the JDK. Without a working JDK, I can't continue.
""")

    interface.success("The JDK is present and working. Good!")

    os.unlink(plat.path("test.java"))
    os.unlink(plat.path("test.class"))


class FixedZipFile(zipfile.ZipFile):
    """
    Patches zipfile.zipfile so it sets the executable bit when necessary.
    """

    def extract(self, member, path=None, pwd=None):

        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)
        attr = member.external_attr >> 16

        if attr:
            os.chmod(ret_val, attr)

        return ret_val


def unpack_sdk(interface):

    if os.path.exists(plat.sdkmanager):
        interface.success("The Android SDK has already been unpacked.")
        return

    if "RAPT_NO_TERMS" not in os.environ:
        interface.terms("https://developer.android.com/studio/terms", "Do you accept the Android SDK Terms and Conditions?")

    if plat.windows:
        archive = "sdk-tools-windows-{}.zip".format(plat.sdk_version)
    elif plat.macintosh:
        archive = "sdk-tools-darwin-{}.zip".format(plat.sdk_version)
    elif plat.linux:
        archive = "sdk-tools-linux-{}.zip".format(plat.sdk_version)

    url = "https://dl.google.com/android/repository/" + archive

    interface.info("I'm downloading the Android SDK. This might take a while.")

    interface.download(url, plat.path(archive))

    interface.info("I'm extracting the Android SDK.")

    def extract():

        zf = FixedZipFile(plat.path(archive))

        # We have to do this because Python has a small (260?) path length
        # limit on windows, and the Android SDK has very long filenames.
        old_cwd = os.getcwd()
        os.chdir(plat.path("."))

        zf.extractall("Sdk")

        os.chdir(old_cwd)

        zf.close()

    interface.background(extract)

    interface.success("I've finished unpacking the Android SDK.")


def get_packages(interface):

    packages = [ ]

    wanted_packages = [
        ( "build-tools;28.0.1", "build-tools/28.0.1" ),
        ( "platform-tools", "platform-tools"),
        ( "platforms;android-28", "platforms/android-28"),
        ]

    for i, j in wanted_packages:
        if not os.path.exists(os.path.join(plat.sdk, j)):
            packages.append(i)

    if packages:

        interface.info("I'm about to download and install the required Android packages. This might take a while.")

        if not run_slow(interface, plat.sdkmanager, "--licenses", yes=True):
            interface.fail("I was unable to accept the Android licenses.")

        if not run_slow(interface, plat.sdkmanager, *packages):
            interface.fail("I was unable to install the required Android packages.")

    interface.success("I've finished installing the required Android packages.")


local_properties = plat.path("project/local.properties")


def set_property(key, value, replace=False):
    """
    Sets the property `key` in local.properties to `value`. If replace is True,
    replaces the value.
    """

    lines = [ ]

    try:
        with open(local_properties, "r") as f:
            for l in f:
                k = l.partition("=")[0].strip()

                if k == key:
                    if not replace:
                        return
                    else:
                        continue

                lines.append(l)

    except:
        pass

    with open(local_properties, "w") as f:
        for l in lines:
            f.write(l)

        f.write("{}={}\n".format(key, value))


def get_property(key):

    with open(local_properties, "r") as f:
        for l in f:
            k, _, v = l.partition("=")

            if k.strip() == key:
                return v.strip()

    return None


def generate_keys(interface):

    set_property("key.alias", "android")
    set_property("key.store.password", "android")
    set_property("key.alias.password", "android")
    set_property("key.store", plat.path("android.keystore").replace("\\", "/"))

    if get_property("key.store") != plat.path("android.keystore"):
        interface.info("You set the keystore yourself, so I'll assume it's how you want it.")
        return

    if os.path.exists(plat.path("android.keystore")):
        interface.info("You've already created an Android keystore, so I won't create a new one for you.")
        return

    if not interface.yesno("""\
I can create an application signing key for you. Signing an application with
this key allows it to be placed in the Android Market and other app stores.

Do you want to create a key?"""):
        return

    if not interface.yesno("""\
I will create the key in the android.keystore file.

You need to back this file up. If you lose it, you will not be able to upgrade
your application.

You also need to keep the key safe. If evil people get this file, they could
make fake versions of your application, and potentially steal your users'
data.

Will you make a backup of android.keystore, and keep it in a safe place?"""):
        return

    org = interface.input("Please enter your name or the name of your organization.")

    dname = "CN=" + org

    if not run(interface, plat.keytool, "-genkey", "-keystore", "android.keystore", "-alias", "android", "-keyalg", "RSA", "-keysize", "2048", "-keypass", "android", "-storepass", "android", "-dname", dname, "-validity", "20000", use_path=True):
        interface.fail("Could not create android.keystore. Is keytool in your path?")

    interface.success("""I've finished creating android.keystore. Please back it up, and keep it in a safe place.""")


def install_sdk(interface):
    check_java(interface)

    unpack_sdk(interface)

    get_packages(interface)

    generate_keys(interface)

    set_property("sdk.dir", plat.sdk.replace("\\", "/"), replace=True)

    interface.final_success("It looks like you're ready to start packaging games.")
