#!/bin/bash

try () {
    "$@" || exit 1
}

DISTRO=pgs4a

ROOT=$(dirname $(readlink -f $0))

export ANDROIDSDK="$ROOT/android-sdk"
export ANDROIDNDK="$ROOT/android-ndk-r8c"
export ANDROIDNDKVER=r8c
export ANDROIDAPI=9

# Build the python-for-android distro.
try cd "$ROOT/python-for-android"
try ./distribute.sh -d "$DISTRO" -m "android pygame pyjnius"

# Move the built distro to $DISTROROOT.
DISTROROOT="$ROOT/dist/$DISTRO"

try cd "$ROOT"
try mkdir "$ROOT/dist"

if [ -e "$DISTROROOT" ]; then
    try rm -Rf "$DISTROROOT"
fi

try mv "$ROOT/python-for-android/dist/$DISTRO" "$DISTROROOT"
try cd "$DISTROROOT"

