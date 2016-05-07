. "$NATIVE/scripts/common.sh"

build () {
    export PYGAME_SDL2_ANDROID="$NATIVE"

    pushd "$PYGAME_SDL2_ROOT"

    setup_py "pygame_sdl2"

    popd
}


"$1"
