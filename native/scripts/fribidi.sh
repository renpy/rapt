. "$NATIVE/scripts/common.sh"

version="0.19.2"

unpack () {
    tar xzf "$SOURCE/fribidi-$version.tar.gz"
}


build () {
    activate_toolchain

    pushd "fribidi-$version"

    ./configure --host=$NDK_ARCH-unknown-linux-gnu --enable-static --disable-shared --prefix="$INSTALLDIR"

    make
    make install

    popd
}


"$1"
