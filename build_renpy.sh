#!/bin/bash

try () {
    "$@" || exit 1
}

export ROOT=$(dirname $(readlink -f $0))

export DISTRO="${1:-renpy}"
export RENPYROOT="${2:-/home/tom/ab/renpy}"
export PYGAME_SDL2_ROOT="${3:-/home/tom/ab/pygame_sdl2}"

try cd $RENPYROOT

if [ -n "$VIRTUAL_ENV" ] ; then
    try ./run.sh the_question compile
fi

rm -Rf "$RENPYROOT/module/build/lib.android"

export RENPY_ANDROID="$ROOT"
export PYGAME_SDL2_ANDROID="$ROOT"

export RENPY_PYARGS="-O"

export ANDROIDSDK="$ROOT/android-sdk"
export ANDROIDNDK="$ROOT/android-ndk-r11b"
export ANDROIDNDKVER=r11b
export ANDROIDAPI=9

# Build the python-for-android distro.
try cd "$ROOT/python-for-android"
# rm -Rf build/android
# rm -Rf build/pygame_sdl2
# rm -Rf build/renpy
# rm -Rf build/pyjnius
try ./distribute.sh -d "$DISTRO" -m "android pygame_sdl2 renpy pyjnius"

# Move the built distro to $DISTROROOT.
DISTROROOT="$ROOT/dist/$DISTRO"

try cd "$ROOT"
try mkdir -p "$ROOT/dist"

if [ -e "$DISTROROOT" ]; then
    try rm -Rf "$DISTROROOT"
fi

try mv "$ROOT/python-for-android/dist/$DISTRO" "$DISTROROOT"

# Delete unneeded librarys and the python install.

tryrm () {
  echo rm "$@"
  try rm -Rf "$@"
}

tryrm "$DISTROROOT/local.properties"

tryrm "$DISTROROOT/lib/armeabi/"*.a

tryrm "$DISTROROOT/python-install"
# tryrm "$DISTROROOT/libs/armeabi/libSDL2_ttf.so"

python="$DISTROROOT/private/lib/python2.7"
pygame="$python/site-packages/pygame"

tryrm "$pygame/threads/Py25Queue.pyo"

# unused encodings
tryrm "$python/unittest/"*
tryrm "$python/distutils/"*.exe
tryrm "$python/lib-dynload/"*codec*

tryrm "$python/encodings/cp"*.pyo
tryrm "$python/encodings/tis"*
tryrm "$python/encodings/shift"*
tryrm "$python/encodings/iso"*
tryrm "$python/encodings/undefined"*
tryrm "$python/encodings/johab"*
tryrm "$python/encodings/p"*
tryrm "$python/encodings/m"*
tryrm "$python/encodings/euc"*
tryrm "$python/encodings/k"*
tryrm "$python/encodings/gb"*
tryrm "$python/encodings/big5"*
tryrm "$python/encodings/hp"*
tryrm "$python/encodings/hz"*

# unused python modules
tryrm "$python/bsddb/"*
tryrm "$python/wsgiref/"*
tryrm "$python/sqlite3/"*
tryrm "$python/hotshot/"*
tryrm "$python/pydoc_data/"*
tryrm "$python/tty.pyo"
tryrm "$python/anydbm.pyo"
tryrm "$python/nturl2path.pyo"
tryrm "$python/LICENCE.txt"
tryrm "$python/macurl2path.pyo"
tryrm "$python/dummy_threading.pyo"
tryrm "$python/audiodev.pyo"
tryrm "$python/antigravity.pyo"
tryrm "$python/dumbdbm.pyo"
tryrm "$python/sndhdr.pyo"
tryrm "$python/__phello__.foo.pyo"
tryrm "$python/sunaudio.pyo"
tryrm "$python/os2emxpath.pyo"
tryrm "$python/multiprocessing/dummy"*

# unused binaries python modules
tryrm "$python/lib-dynload/_sqlite3.so"
tryrm "$python/lib-dynload/_lsprof.so"
tryrm "$python/lib-dynload/*audioop.so"
tryrm "$python/lib-dynload/_hotshot.so"
tryrm "$python/lib-dynload/_csv.so"
tryrm "$python/lib-dynload/_lsprof.so"
tryrm "$python/lib-dynload/_heapq.so"
tryrm "$python/lib-dynload/grp.so"
tryrm "$python/lib-dynload/resource.so"

# odd files
tryrm "$python/plat-linux3/regen"


# Copy the common files over.
try mkdir -p "$DISTROROOT/renpy"

# try cp -a "$RENPYROOT/renpy/common" "$DISTROROOT/renpy"
# try rm -f "$DISTROROOT/renpy/common/"*.rpy
# try rm -Rf "$DISTROROOT/renpy/common/_compat"
# try cp "$RENPYROOT/renpy.py" "$DISTROROOT/private/main.py"

# Copy the build scripts.
try ./copy_scripts.sh "$DISTROROOT"
try cp "whitelist-renpy.txt" "$DISTROROOT/whitelist.txt"
try cp "blacklist-renpy.txt" "$DISTROROOT/blacklist.txt"

# Copy the SDKs over.
try cp "$ROOT/amazon-iap-2.0.1.jar" "$DISTROROOT/libs/"
try cp -a "$ROOT/extras" "$DISTROROOT/extras"

# echo Done adding renpy.

# if [ "$1" != "" ]; then
    #    try cd "$ROOT/dist"
    # try tar cjf "rapt-$1.tar.bz2" "rapt-$1"
    # try zip -9r "rapt-$1.zip" "rapt-$1"
# fi
