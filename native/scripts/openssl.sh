. "$NATIVE/scripts/common.sh"

version="1.0.2m"

unpack () {
    tar xzf "$SOURCE/openssl-$version.tar.gz"
}


build () {
    activate_toolchain

    pushd "openssl-$version"

    export CROSS_SYSROOT="$INSTALLDIR/toolchain/sysroot"

    ./Configure --prefix="$INSTALLDIR" \
        no-asm no-shared no-comp no-hw no-engine \
        $OPENSSL_ARCH -fPIC \
        -D__ANDROID_API__=${ANDROID_PLATFORM#android-}

    make depend CFLAGS="$CFLAGS"
    make
    make install

    popd
}


"$1"
