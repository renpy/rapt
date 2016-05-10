#!/bin/bash

export NATIVE="$(dirname $(readlink -f $0))"
export ANDROID="$(dirname $NATIVE)"
export SOURCE="$NATIVE/source"
export NDK="$NATIVE/android-ndk"
export SDK="$NATIVE/../android-sdk"
export ANDROID_PLATFORM=android-9

export PYGAME_SDL2_ROOT="${PYGAME_SDL2_ROOT:-/home/tom/ab/pygame_sdl2}"
export RENPY_ROOT="${RENPY_ROOT:-/home/tom/ab/renpy}"

cd "$NATIVE"

. "$NATIVE/scripts/common.sh"

mkdir -p "$NATIVE/build/complete"

build_host() {

    # Build for host.
    export PLATFORM=host
    export CC="ccache gcc"
    export LD="ccache gcc"

    run_once python unpack
    run_once python hostbuild
}

build_platform () {
    mkdir -p "$NATIVE/build/$PLATFORM/pymodules"

    # Set up the toolchain.
    run_once toolchain create

    # Use the toolchain to build python.
    run_once python unpack
    run_once python apply_patches
    run_once python build

    # Build and biglink the android module alone, so we have a libpymodules
    # that will let us build the full jni.
    run android build
    run biglink link
    run jni platform

    # ffmpeg takes forever.
    run_once ffmpeg unpack
    run_once ffmpeg build

    run_once fribidi unpack
    run_once fribidi build

    run_once pyjnius build

    run pygame_sdl2 build
    run renpy build

    # Do a final biglink that includes the full libpymodules.
    run biglink link
}

build_arm () {

    export PLATFORM=armeabi
    export NDK_ARCH=arm
    export FFMPEG_ARCH=arm
    export GCC_ARCH=arm-linux-androideabi

    build_platform
}


build_x86 () {

    export PLATFORM=x86
    export NDK_ARCH=x86
    export FFMPEG_ARCH=x86
    export GCC_ARCH=i686-linux-android

    build_platform
}

build_ () {
    run finish clean

    build_host
    build_x86
    build_arm

    run jni all
    run finish dist
}

build_$1
