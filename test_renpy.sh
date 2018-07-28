#!/bin/bash

set -e


ROOT="$(dirname $(readlink -f $0))"

cd "$ROOT"
"$ROOT/build_renpy.sh"

# ln -s "$ROOT/Sdk" "$ROOT/dist/Sdk"

cd "$ROOT/dist"
export PGS4A_NO_TERMS=1
python android.py installsdk

# if [ "$1" != "" ]; then
#     /home/tom/ab/renpy/renpy.sh /home/tom/ab/renpy/launcher android_build "$1" installDebug --launch
# fi
