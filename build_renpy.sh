#!/bin/bash

try () {
    "$@" || exit 1
}

if [ "$1" != "" ]; then
    DISTRO="$1"
else
    DISTRO=renpy
fi

if [ "$2" != "" ]; then
    RENPYROOT="$2"
else
    RENPYROOT="/home/tom/ab/renpy"
fi

export ROOT=$(dirname $(readlink -f $0))

export RENPYROOT
export RENPY_ANDROID="$ROOT"
export RENPY_PYARGS="-O"

export ANDROIDSDK="$ROOT/android-sdk"
export ANDROIDNDK="$ROOT/android-ndk-r8c"
export ANDROIDNDKVER=r8c
export ANDROIDAPI=8

try cd $RENPYROOT
try ./run.sh the_question compile

rm -Rf "$RENPYROOT/module/build/lib.android"

# Build the python-for-android distro.
try cd "$ROOT/python-for-android"
try ./distribute.sh -d "$DISTRO" -m "android pygame renpy pyjnius"

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

tryrm "$DISTROROOT/python-install"
tryrm "$DISTROROOT/libs/armeabi/libsdl_mixer.so"
tryrm "$DISTROROOT/libs/armeabi/libsqlite3.so"

python="$DISTROROOT/private/lib/python2.7"
pygame="$python/site-packages/pygame"

tryrm "$pygame/_camera_"*
tryrm "$pygame/camera.pyo"
tryrm "$pygame/"*.html
tryrm "$pygame/"*.bmp
tryrm "$pygame/"*.svg
tryrm "$pygame/cdrom.so"
tryrm "$pygame/pygame_icon.icns"
tryrm "$pygame/threads/Py25Queue.pyo"
tryrm "$pygame/"*.ttf
tryrm "$pygame/mac"*
tryrm "$pygame/_numpy"*
tryrm "$pygame/sndarray.pyo"
tryrm "$pygame/surfarray.pyo"
tryrm "$pygame/_arraysurfarray.pyo"


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
try cp -a "$RENPYROOT/renpy/common" "$DISTROROOT/renpy"

try rm -f "$DISTROROOT/renpy/common/"*.rpy
try rm -Rf "$DISTROROOT/renpy/common/_compat"

try cp "$RENPYROOT/renpy.py" "$DISTROROOT/private/main.py"

# Copy the build scripts.
try ./copy_scripts.sh "$DISTROROOT"
try cp "whitelist-renpy.txt" "$DISTROROOT/whitelist.txt"
try cp "blacklist-renpy.txt" "$DISTROROOT/blacklist.txt"

# Copy the OUYA SDK over.
try cp "$ROOT/ouya-sdk.jar" "$DISTROROOT/libs/ouya-sdk.jar"

# echo Done adding renpy.

# if [ "$1" != "" ]; then
    #    try cd "$ROOT/dist"
    # try tar cjf "rapt-$1.tar.bz2" "rapt-$1"
    # try zip -9r "rapt-$1.zip" "rapt-$1"
# fi
