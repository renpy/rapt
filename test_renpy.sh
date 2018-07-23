#!/bin/bash

set -e


ROOT="$(dirname $(readlink -f $0))"

# "$ROOT/build_renpy.sh"

cd "$ROOT"

if [ "$1" != "" ]; then
    cd "$ROOT"
    /home/tom/ab/renpy/renpy.sh /home/tom/ab/renpy/launcher android_build "$1" build
fi
