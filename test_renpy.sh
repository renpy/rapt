#!/bin/bash

set -e


ROOT="$(dirname $(readlink -f $0))"
D=dist

"$ROOT/build_renpy.sh"

ln -s "$ROOT/android-sdk"* "$D"
ln -s "$ROOT/apache-ant"* "$D"

cd "$D"

export PGS4A_NO_TERMS=1
(echo no) | ./android.py installsdk

cp "$ROOT/local.properties" .
touch "android.keystore"

if [ "$1" != "" ]; then
    cd "$ROOT"
    ./renpy/renpy.sh ./renpy/launcher android_build --launch "$1" release install
fi
