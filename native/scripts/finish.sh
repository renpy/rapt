. "$NATIVE/scripts/common.sh"

DIST="$ANDROID/dist"
PYLIB="$DIST/private/lib/python2.7"

clean () {
    rm -Rf "$DIST" || true
}

dist () {

    # Copy the native libs.
    mkdir -p "$DIST"
    cp -a "$NATIVE/libs" "$DIST/libs"

    mkdir -p "$DIST/private/include/python2.7"
    cp -a "$NATIVE/install/armeabi/include/python2.7/pyconfig.h" "$DIST/private/include/python2.7"

    mkdir -p "$DIST/private/lib"
    cp -a "$NATIVE/install/armeabi/lib/python2.7" "$PYLIB"

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

    # unused binary python modules
    rm -Rf "$PYLIB/lib-dynload/_sqlite3.so"
    rm -Rf "$PYLIB/lib-dynload/_lsprof.so"
    rm -Rf "$PYLIB/lib-dynload/*audioop.so"
    rm -Rf "$PYLIB/lib-dynload/_hotshot.so"
    rm -Rf "$PYLIB/lib-dynload/_csv.so"
    rm -Rf "$PYLIB/lib-dynload/_lsprof.so"
    rm -Rf "$PYLIB/lib-dynload/_heapq.so"
    rm -Rf "$PYLIB/lib-dynload/grp.so"
    rm -Rf "$PYLIB/lib-dynload/resource.so"

    # odd files
    rm -Rf "$PYLIB/plat-linux"*/regen
    rm -Rf "$PYLIB/site-packages/pygame_sdl2/threads/Py25Queue.pyo"
    rm -Rf "$PYLIB/unittest/"*
    rm -Rf "$PYLIB/distutils/"*.exe

}

"$@"
