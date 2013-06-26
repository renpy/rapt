#!/bin/bash

try () {
    "$@" || exit 1
}

try ./build_pgs4a.sh 

ROOT=$(dirname $(readlink -f $0))
D=dist/pgs4a

try ln -s "$ROOT/android-sdk" "$D"
try ln -s "$ROOT/apache-ant" "$D"

cd "$D"

(echo no) | ./android.py installsdk 
./android.py build /home/tom/ab/android/tests/color_touch debug install
