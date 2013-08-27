# This sets up various variables and commands based on the platform we're on.

##############################################################################
# These are set based on the platform we're on.
windows = False
macintosh = False
linux = False

import os
import platform
import traceback

def set_win32_java_home():

    if "JAVA_HOME" in os.environ:
        return

    import _winreg

    with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\JavaSoft\Java Development Kit") as jdk: #@UndefinedVariable
        current_version, _type = _winreg.QueryValueEx(jdk, "CurrentVersion") #@UndefinedVariable

        with _winreg.OpenKey(jdk, current_version) as cv: #@UndefinedVariable
            java_home, _type = _winreg.QueryValueEx(cv, "JavaHome") #@UndefinedVariable

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

    android = "android-sdk\\tools\\android.bat"
    ant = "apache-ant\\bin\\ant.bat"
    adb = "android-sdk\\platform-tools\\adb.exe"
    javac = maybe_java_home("javac.exe")
    keytool = maybe_java_home("keytool.exe")

elif platform.mac_ver()[0]:
    macintosh = True
    android = "android-sdk/tools/android"
    ant = "apache-ant/bin/ant"
    adb = "android-sdk/platform-tools/adb"
    javac = maybe_java_home("javac")
    keytool = maybe_java_home("keytool")

else:
    linux = True
    android = "android-sdk/tools/android"
    ant = "apache-ant/bin/ant"
    adb = "android-sdk/platform-tools/adb"
    javac = maybe_java_home("javac")
    keytool = maybe_java_home("keytool")

RAPT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def path(path):
    """
    Turns a relative path into an absolute path relative to the RAPT
    directory.
    """

    rv = os.path.join(RAPT_PATH, path)
    return rv

def rename(src, dst):
    """
    Renames src to dst.
    """

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    elif os.path.exists(dst):
        os.unlink(dst)

    os.rename(src, dst)

