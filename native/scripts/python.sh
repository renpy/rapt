. "$NATIVE/scripts/common.sh"

version="2.7.2"

unpack () {
    pushd "$BUILD"

    tar xaf "$SOURCE/Python-$version.tgz"

    popd
}


hostbuild () {
    pushd "$BUILD/Python-$version"

    ./configure --prefix="$INSTALLDIR/python"
    make
    make install
    cp -a Parser/pgen "$INSTALLDIR/python/bin/pgen"

    popd
}


"$1"
