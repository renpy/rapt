. "$NATIVE/scripts/common.sh"

PROJECT="$ANDROID/project"
JNILIBS="$PROJECT/renpyandroid/src/main/jniLibs"
PRIVATE="$PROJECT/renpyandroid/src/main/private"
PYLIB="$PRIVATE/lib/python2.7"

clean () {
    rm -Rf "$JNILIBS" || true
    rm -Rf "$PRIVATE" || true
}

dist () {

    # Copy the native libs.
    mkdir -p "JNILIBS"
    cp -a "$NATIVE/libs"* "$JNILIBS"

    mkdir -p "$PRIVATE/include/python2.7"
    cp -a "$NATIVE/install/armeabi-v7a/include/python2.7/pyconfig.h" "$PRIVATE/include/python2.7"

    mkdir -p "$PRIVATE/lib"
    cp -a "$NATIVE/install/armeabi-v7a/lib/python2.7" "$PYLIB"

    # unused encodings
    rm -Rf "$PYLIB/lib-dynload/"*codec*
    rm -Rf "$PYLIB/encodings/cp"*.pyo
    rm -Rf "$PYLIB/encodings/tis"*
    rm -Rf "$PYLIB/encodings/shift"*
    rm -Rf "$PYLIB/encodings/iso"*
    rm -Rf "$PYLIB/encodings/undefined"*
    rm -Rf "$PYLIB/encodings/johab"*
    rm -Rf "$PYLIB/encodings/p"*
    rm -Rf "$PYLIB/encodings/m"*
    rm -Rf "$PYLIB/encodings/euc"*
    rm -Rf "$PYLIB/encodings/k"*
    rm -Rf "$PYLIB/encodings/gb"*
    rm -Rf "$PYLIB/encodings/big5"*
    rm -Rf "$PYLIB/encodings/hp"*
    rm -Rf "$PYLIB/encodings/hz"*

    # unused python modules
    rm -Rf "$PYLIB/bsddb/"*
    rm -Rf "$PYLIB/wsgiref/"*
    rm -Rf "$PYLIB/sqlite3/"*
    rm -Rf "$PYLIB/hotshot/"*
    rm -Rf "$PYLIB/pydoc_data/"*
    rm -Rf "$PYLIB/tty.pyo"
    rm -Rf "$PYLIB/anydbm.pyo"
    rm -Rf "$PYLIB/nturl2path.pyo"
    rm -Rf "$PYLIB/LICENCE.txt"
    rm -Rf "$PYLIB/macurl2path.pyo"
    rm -Rf "$PYLIB/dummy_threading.pyo"
    rm -Rf "$PYLIB/audiodev.pyo"
    rm -Rf "$PYLIB/antigravity.pyo"
    rm -Rf "$PYLIB/dumbdbm.pyo"
    rm -Rf "$PYLIB/sndhdr.pyo"
    rm -Rf "$PYLIB/__phello__.foo.pyo"
    rm -Rf "$PYLIB/sunaudio.pyo"
    rm -Rf "$PYLIB/os2emxpath.pyo"
    rm -Rf "$PYLIB/multiprocessing/dummy"*
    rm -Rf "$PYLIB/lib2to3"
    rm -Rf "$PYLIB/idlelib"
    rm -Rf "$PYLIB/ctypes/test"
    rm -Rf "$PYLIB/distutils"


    # unused binary python modules
    rm -Rf "$PYLIB/lib-dynload/"*.so

    # odd files
    rm -Rf "$PYLIB/plat-linux"*/regen
    rm -Rf "$PYLIB/site-packages/pygame_sdl2/threads/Py25Queue.pyo"
    rm -Rf "$PYLIB/unittest/"*
    rm -Rf "$PYLIB/distutils/"*.exe
    rm -Rf "$PYLIB/distutils/command/"*.exe
    rm -Rf "$PYLIB/config/"*.a

    find "$PYLIB" -name \*.pyc -delete
    find "$PYLIB" -name \*.egg-info -delete


}

"$@"
