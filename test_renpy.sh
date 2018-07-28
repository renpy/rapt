#!/bin/bash

set -e


ROOT="$(dirname $(readlink -f $0))"

cd "$ROOT"
"$ROOT/build_renpy.sh"

ln -s "$ROOT/Sdk" "$ROOT/dist/Sdk"

if [ "$1" != "" ]; then
    /home/tom/ab/renpy/renpy.sh /home/tom/ab/renpy/launcher android_build "$1" installDebug
fi
