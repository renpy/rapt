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
export ANDROIDNDK="$ROOT/android-ndk-r10c"
export ANDROIDNDKVER=r10c
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

# Copy the SDKs over.
try cp "$ROOT/ouya-sdk.jar" "$DISTROROOT/libs/"
try cp "$ROOT/Amazon-InAppSDK-Purchasing.jar" "$DISTROROOT/libs/"

# Build the documentation.
try cd "$ROOT/doc"
try make html
try cp -a "_build/html" "$DISTROROOT/doc"

if [ "$1" != "" ]; then

    try cd "$ROOT/dist"
    try tar cjf "pgs4a-$1.tar.bz2" "pgs4a-$1"
    try zip -9r "pgs4a-$1.zip" "pgs4a-$1"
fi
