#!/bin/bash

try () {
    "$@" || exit 1
}

if [ "$1" != "" ]; then
    DISTRO="rapt-$1"    
else
    DISTRO=renpy
fi



export ROOT=$(dirname $(readlink -f $0))

export RENPYROOT="$ROOT/renpy"
export RENPY_ANDROID="$ROOT"
export RENPY_PYARGS="-OO"

export ANDROIDSDK="$ROOT/android-sdk"
export ANDROIDNDK="$ROOT/android-ndk-r8c"
export ANDROIDNDKVER=r8c
export ANDROIDAPI=9

try cd $RENPYROOT
try ./run.sh the_question compile

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

# Copy the common files over.
try mkdir -p "$DISTROROOT/renpy"
try cp -a "$RENPYROOT/renpy/common" "$DISTROROOT/renpy"

try rm -f "$DISTROROOT/renpy/common/"*.rpy
try rm -Rf "$DISTROROOT/renpy/common/_compat"

try cp "$RENPYROOT/renpy.py" "$DISTROROOT/private/main.py"

# Copy the build scripts.
try ./copy_scripts.sh "$DISTROROOT"

echo Done adding renpy.

if [ "$1" != "" ]; then
    cd "$ROOT/dist"
    tar cjf "rapt-$1.tar.bz2" "rapt-$1"
fi