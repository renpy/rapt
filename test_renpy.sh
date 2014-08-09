#!/bin/bash

try () {
    "$@" || exit 1
}


try ./build_renpy.sh

ROOT=$(dirname $(readlink -f $0))
D=dist/renpy

try ln -s "$ROOT/android-sdk-"* "$D"
try ln -s "$ROOT/apache-ant-"* "$D"

try cd "$D"

export PGS4A_NO_TERMS=1
(echo no) | try ./android.py installsdk

try cp "$ROOT/local.properties" .
try touch "android.keystore"

if [ "$1" != "" ]; then
    cd "$ROOT"

    # try ./android.py build $1 debug install
    try ./renpy/renpy.sh ./renpy/launcher android_build $1 release install
fi
