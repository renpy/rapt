#!/bin/bash

try () {
    "$@" || exit 1
}

try ./build_pgs4a.sh

ROOT=$(dirname $(readlink -f $0))
D=dist/pgs4a

try ln -s "$ROOT/android-sdk-"* "$D"
try ln -s "$ROOT/apache-ant-"* "$D"

try cd "$D"

export PGS4A_NO_TERMS=1
(echo no) | try ./android.py installsdk

try cp "$ROOT/local.properties" .
try touch "android.keystore"

./android.py build /home/tom/ab/android/tests/color_touch debug install
adb shell am start -n org.renpy.ct/org.renpy.android.PythonSDLActivity
