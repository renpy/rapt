#!/bin/bash

try () {
    "$@" || exit 1
}


try ./build_renpy.sh 

ROOT=$(dirname $(readlink -f $0))
D=dist/renpy

try ln -s "$ROOT/android-sdk" "$D"
try ln -s "$ROOT/apache-ant" "$D"

try cd "$D"

(echo no) | try ./android.py installsdk 

try cp "$ROOT/local.properties" .

# ./android.py configure /home/tom/ab/renpy/the_question
try ./android.py build /home/tom/ab/renpy/tutorial debug install
