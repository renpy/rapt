#!/bin/bash

set -e

unset RENPY_STEAM_PLATFORM
unset RENPY_STEAM_SDK

export ROOT=$(dirname $(readlink -f $0))
export DIST="$ROOT/dist"
export RENPY_ROOT="${2:-/home/tom/ab/renpy}"
export PYGAME_SDL2_ROOT="${3:-/home/tom/ab/pygame_sdl2}"

pushd "$RENPY_ROOT"
./run.sh the_question compile
popd

pushd "$ROOT/native"
./build.sh
popd

cd "$ROOT"

cp -a "$ROOT/src" "$DIST"
cp -a "$ROOT/res" "$DIST"
cp -a "$ROOT/buildlib" "$DIST"
cp -a "$ROOT/android.py" "$DIST"
cp -a "$ROOT/templates" "$DIST"
cp -a "$ROOT/whitelist.txt" "$DIST"
cp -a "$ROOT/blacklist.txt" "$DIST"

cp "$ROOT/amazon-iap-2.0.1.jar" "$DIST/libs/"
cp -a "$ROOT/extras" "$DIST"

