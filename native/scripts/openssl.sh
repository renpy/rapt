. "$NATIVE/scripts/common.sh"

version="1.0.2m"

unpack () {
    tar xzf "$SOURCE/openssl-$version.tar.gz"
}


build () {
    activate_toolchain

    pushd "openssl-$version"

    ./Configure --prefix="$INSTALLDIR" -fPIC no-asm no-shared no-comp no-hw no-engine android

    make depend
    make
    make install

    popd
}


"$1"
