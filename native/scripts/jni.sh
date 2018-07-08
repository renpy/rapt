. "$NATIVE/scripts/common.sh"

platform () {
    export NDK_CCACHE=$(which ccache)
    "$NDK/ndk-build" V=1 ARCH="$PLATFORM"
}

all () {
    export NDK_CCACHE=$(which ccache)
    "$NDK/ndk-build" V=1 ARCH="armeabi-v7a x86"
}



"$1"
