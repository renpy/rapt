# Common functions used by native building scripts.

set -e

if test -z "$NATIVE"; then
    echo "This should be run in a native environment."
    exit 1
fi

green () {
    echo -e "\e[1;32m$@\e[0m"
}

run () {
    export BUILD="$NATIVE/build/$PLATFORM"
    export INSTALLDIR="$NATIVE/install/$PLATFORM"

    mkdir -p "$BUILD"
    mkdir -p "$INSTALLDIR"

    echo
    green "$PLATFORM $1 $2: starting."

    pushd "$BUILD"
    bash "$NATIVE/scripts/$1.sh" $2
    popd

    green "$PLATFORM $1 $2: finished."
}

run_once () {

    finished="$NATIVE/build/complete/$PLATFORM-$1-$2"

    if test -e "$finished"; then
        echo
        green "$PLATFORM $1 $2: already complete."
    else
        run "$1" "$2"
        touch "$finished"
    fi
}


includedir () {
    CFLAGS="$CFLAGS -I$1"
}

libdir () {
    LDFLAGS="$LDFLAGS -L$1"
}

activate_toolchain () {
    export PATH="$INSTALLDIR/toolchain/bin:$PATH"

    export CC="ccache $GCC_ARCH-gcc -isysroot $INSTALLDIR/toolchain/sysroot"
    export CXX="ccache $GCC_ARCH-g++ -isysroot $INSTALLDIR/toolchain/sysroot"
    export LD="ccache $GCC_ARCH-gcc -isysroot $INSTALLDIR/toolchain/sysroot"
    export LDXX="ccache $GCC_ARCH-g++ -isysroot $INSTALLDIR/toolchain/sysroot"
    export RANLIB="$GCC_ARCH-ranlib"

    export CFLAGS="-DANDROID -D__ANDROID_API__=${ANDROID_PLATFORM#android-}"
    export LDFLAGS=""

    libdir "$INSTALLDIR/lib"
    libdir "$NATIVE/obj/local/$PLATFORM"

    includedir "$INSTALLDIR/include"
    includedir "$INSTALLDIR/include/openssl"
    includedir "$INSTALLDIR/python2.7"

    includedir "$NATIVE/jni/png"
    includedir "$NATIVE/jni/jpeg"
    includedir "$NATIVE/jni/freetype/include"
    includedir "$NATIVE/jni/sdl2/include"
    includedir "$NATIVE/jni/sdl2_image"
    includedir "$NATIVE/jni/sdl2_ttf"
    includedir "$NATIVE/jni/sdl2_mixer"
}

setup_py () {
    activate_toolchain

    export LDSHARED="$NATIVE/scripts/liblink.py"
    export HOSTPYTHON="$INSTALLDIR/bin/hostpython"

    $HOSTPYTHON setup.py build -b "$BUILD/$1/lib" -t "$BUILD/$1/tmp" install -O2
}
