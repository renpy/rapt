# This sets up various variables and commands based on the platform we're on.

from __future__ import print_function

##############################################################################
# These are set based on the platform we're on.
windows = False
macintosh = False
linux = False

import os
import platform
import traceback
import shutil

if "ANT_HOME" in os.environ:
    del os.environ["ANT_HOME"]


def set_win32_java_home():

    if "JAVA_HOME" in os.environ:
        return

    import _winreg

    with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\JavaSoft\Java Development Kit") as jdk:  # @UndefinedVariable
        current_version, _type = _winreg.QueryValueEx(jdk, "CurrentVersion")  # @UndefinedVariable

        with _winreg.OpenKey(jdk, current_version) as cv:  # @UndefinedVariable
            java_home, _type = _winreg.QueryValueEx(cv, "JavaHome")  # @UndefinedVariable

        os.environ["JAVA_HOME"] = java_home


def maybe_java_home(s):
    """
    If JAVA_HOME is in the environ, return $JAVA_HOME/bin/s. Otherwise, return
    s.
    """

    if "JAVA_HOME" in os.environ:
        return os.path.join(os.environ["JAVA_HOME"], "bin", s)
    else:
        return s


if platform.win32_ver()[0]:
    windows = True

    try:
        set_win32_java_home()
    except:
        traceback.print_exc()

    adb = "platform-tools\\adb.exe"
    sdkmanager = "tools\\bin\\sdkmanager.bat"

    javac = maybe_java_home("javac.exe")
    keytool = maybe_java_home("keytool.exe")

    gradlew = "project/gradlew.bat"

elif platform.mac_ver()[0]:
    macintosh = True

    adb = "platform-tools/adb"
    sdkmanager = "tools/bin/sdkmanager"

    javac = maybe_java_home("javac")
    keytool = maybe_java_home("keytool")

    os.environ.setdefault("JAVA_HOME", "/usr")

    gradlew = "project/gradlew"

else:
    linux = True

    adb = "platform-tools/adb"
    sdkmanager = "tools/bin/sdkmanager"

    javac = maybe_java_home("javac")
    keytool = maybe_java_home("keytool")

    gradlew = "project/gradlew"


# The path to RAPT.
RAPT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def path(path, relative=False):
    """
    Turns a relative path into an absolute path relative to the RAPT
    directory.
    """

    if not path:
        return RAPT_PATH

    if not relative:
        path = os.path.join(RAPT_PATH, path)

    return path


sdk_version = "4333796"

try:
    with open(path("sdk.txt")) as f:
        sdk = f.read().strip()
except:
    sdk = path("Sdk")

adb = os.path.join(sdk, adb)
sdkmanager = os.path.join(sdk, sdkmanager)

gradlew = path(gradlew)

# This gets set in the Ren'Py launcher if we're a Ren'Py build.
renpy = False


def rename(src, dst):
    """
    Renames src to dst.
    """

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    elif os.path.exists(dst):
        os.unlink(dst)

    if os.path.isdir(src):
        shutil.copytree(src, dst)
        shutil.rmtree(src)
    else:
        shutil.copy(src, dst)
        os.unlink(src)
