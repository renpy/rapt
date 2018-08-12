#!/bin/bash

set -e

unset RENPY_STEAM_PLATFORM
unset RENPY_STEAM_SDK

export ROOT=$(dirname $(readlink -f $0))
export DIST="$ROOT/dist"
export RENPY_ROOT="${2:-/home/tom/ab/renpy}"
export PYGAME_SDL2_ROOT="${3:-/home/tom/ab/pygame_sdl2}"

pushd "$ROOT/native"
./build.sh
popd

cd "$ROOT"

rm -Rf "$RENPY_ROOT/rapt"
mkdir -p "$RENPY_ROOT/rapt"
rm -Rf "$DIST"
ln -s "$RENPY_ROOT/rapt" "$DIST"

for i in android.py blacklist.txt buildlib project templates whitelist.txt; do
    cp -a "$ROOT/$i" "$DIST/$i"
done

for i in build \
    .gradle \
    local.properties \
    app/build \
    app/debug \
    app/src/main/AndroidManifest.xml \
    app/src/main/assets \
    app/src/main/res/values/strings.xml \
    app/src/main/res/mipmap-*dpi \
    app/release \
    renpyandroid/src/main/java/org/renpy/android/Constants.java \
    renpyandroid/src/main/AndroidManifest.xml \
    renpyandroid/src/main/res/values/strings.xml \
    buildlib/CheckJDK8.class \
        ; do

    rm -Rf "$DIST/project/$i"
done
