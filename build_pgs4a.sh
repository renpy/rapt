#!/bin/bash

try () {
    "$@" || exit 1
}


if [ "$1" != "" ]; then
    DISTRO="pgs4a-$1"    
else
    DISTRO=pgs4a
fi

ROOT=$(dirname $(readlink -f $0))

export ANDROIDSDK="$ROOT/android-sdk"
export ANDROIDNDK="$ROOT/android-ndk-r8c"
export ANDROIDNDKVER=r8c
export ANDROIDAPI=9

# Build the python-for-android distro.
try cd "$ROOT/python-for-android"
echo | try ./distribute.sh -d "$DISTRO" -m "android pygame pyjnius"

# Move the built distro to $DISTROROOT.
DISTROROOT="$ROOT/dist/$DISTRO"

try cd "$ROOT"
try mkdir -p "$ROOT/dist"

if [ -e "$DISTROROOT" ]; then
    try rm -Rf "$DISTROROOT"
fi

try mv "$ROOT/python-for-android/dist/$DISTRO" "$DISTROROOT"

try ./copy_scripts.sh "$DISTROROOT"

if [ "$1" != "" ]; then
    cd "$ROOT/dist"
    tar cjf "pgs4a-$1.tar.bz2" "pgs4a-$1"
fi