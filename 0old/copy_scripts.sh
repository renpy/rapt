#!/bin/bash

try () {
    "$@" || exit 1
}

ROOT=$(dirname $(readlink -f $0))

if [ -z "$1" ]; then
    echo "usage: $0 <doroot>"  
    exit 1
fi

DISTROROOT="$1"

try cd "$DISTROROOT"

rm -Rf buildlib
rm -Rf build.py
rm -Rf templates

try cp -a "$ROOT/buildlib" . 
try cp -a "$ROOT/android.py" . 
try cp -a "$ROOT/templates" . 
try cp -a "$ROOT/whitelist.txt" . 
try cp -a "$ROOT/blacklist.txt" .
