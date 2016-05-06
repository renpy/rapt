#!/bin/bash

export NATIVE="$(dirname $(readlink -f $0))"
export SOURCE="$NATIVE/source"
export NDK="$NATIVE/android-ndk"
export SDK="$NATIVE/../android-sdk"
export ANDROID_PLATFORM=android-15

. "$NATIVE/scripts/common.sh"

mkdir -p "$NATIVE/build/complete"


# Build for host.
export PLATFORM=host
export CC="ccache gcc"
export LD="ccache gcc"

run_once python unpack
run_once python hostbuild


build_platform () {
    export INSTALL_LIBS="$NATIVE/libs/$PLATFORM"

    mkdir -p $INSTALL_LIBS

    run_once toolchain create

    run_once python unpack
    run_once python apply_patches

    run python build

}

export PLATFORM=armeabi
export NDK_ARCH=arm
export GCC_ARCH=arm-linux-androideabi

build_platform
