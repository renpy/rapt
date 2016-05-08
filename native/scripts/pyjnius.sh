. "$NATIVE/scripts/common.sh"

build () {

    pushd "$SOURCE/pyjnius/"

    export NDKPLATFORM=$PLATFORM
    export PYJNIUS_SDL_VERSION=2
    export LIBLINK=1
    export ARCH=$PLATFORM

    cython "jnius/jnius.pyx"

    setup_py "pyjnius"

    popd

}


"$1"
