. "$NATIVE/scripts/common.sh"

build () {
    export NDK_CCACHE=$(which ccache)
    "$NDK/ndk-build" V=1 ARCH="$PLATFORM"
}

pymodules () {
    export NDK_CCACHE=$(which ccache)
    "$NDK/ndk-build" V=1 ARCH="$PLATFORM" APP_MODULES=pymodules
}


"$1"
