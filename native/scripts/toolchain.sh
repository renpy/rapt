. "$NATIVE/scripts/common.sh"

create () {

    "$NDK/build/tools/make-standalone-toolchain.sh" \
        --arch=$NDK_ARCH --platform=$ANDROID_PLATFORM \
        --install-dir="$INSTALLDIR/toolchain"

}


"$1"
