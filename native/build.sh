#!/bin/bash

export NATIVE="$(dirname $(readlink -f $0))"
export ANDROID="$(dirname $NATIVE)"
export SOURCE="$NATIVE/source"
export SDK="${ANDROID_HOME:-/home/tom/Android/Sdk}"
export NDK="${ANDROID_NDK:-$SDK/ndk-bundle}"

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

    # Build openssl.
    run_once openssl unpack
    run_once openssl build

    # ffmpeg takes forever.
    run_once ffmpeg unpack
    run_once ffmpeg build

    run_once fribidi unpack
    run_once fribidi build

    # Use the toolchain to build python.
    run_once python unpack
    run_once python apply_patches
    run_once python build

    # Build and biglink the android module alone, so we have a libpymodules
    # that will let us build the full jni.
    run android build
    run biglink link
    run jni platform

    run_once pyjnius build

    run pygame_sdl2 build
    run renpy build

    # Do a final biglink that includes the full libpymodules.
    run biglink link
}

build_arm () {

    # The version of Android use.
    export ANDROID_PLATFORM=android-15

    # The binary platform.
    export PLATFORM=armeabi-v7a

    # The arch, as given to the toolchain.
    export NDK_ARCH=arm

    # The arch, as  given to ffmpeg.
    export FFMPEG_ARCH=arm

    # The prefix used for GCC.
    export GCC_ARCH=arm-linux-androideabi

    # The arch arguments provided to openssl.
    export OPENSSL_ARCH="android -march=armv7-a"

    # The -fPIC flag, if needed.
    export PICFLAG=""

    build_platform
}

# ARM64 uses OPENSSL_ARCH="linux-generic64 -DB_ENDIAN"


# x86 FFMPEG doesn't work on modern android, and neither side wants to
# do the work to fix it. So we'll drop support.

# build_x86 () {
#
#     export ANDROID_PLATFORM=android-15
#     export PLATFORM=x86
#     export NDK_ARCH=x86
#     export FFMPEG_ARCH=x86
#     export GCC_ARCH=i686-linux-android
#     export OPENSSL_ARCH="android-x86"
#     export PICFLAG="-fPIC"
#
#     build_platform
# }

build_x86_64 () {

    export ANDROID_PLATFORM=android-21
    export PLATFORM=x86_64
    export NDK_ARCH=x86_64
    export FFMPEG_ARCH=x86_64
    export GCC_ARCH=x86_64-linux-android
    export OPENSSL_ARCH="linux-generic64"
    export PICFLAG="-fPIC"

    build_platform
}


build_ () {
    run finish clean

    build_host

    build_arm
    build_x86_64

    export ANDROID_PLATFORM=android-15
    export ALL_PLATFORMS="armeabi-v7a x86_64"

    run jni all
    run finish dist
}

build_$1
