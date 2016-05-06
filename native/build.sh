#!/bin/bash

export NATIVE="$(dirname $(readlink -f $0))"
export SOURCE="$NATIVE/source"
export NDK="$NATIVE/android-ndk"
export SDK="$NATIVE/../android-sdk"

. "$NATIVE/scripts/common.sh"

mkdir -p "$NATIVE/build/complete"


# Build for host.
export PLATFORM=host
export CC="ccache gcc"
export LD="ccache gcc"

run_once python unpack
run_once python hostbuild
