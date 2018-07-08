. "$NATIVE/scripts/common.sh"

build () {
    export RENPY_ANDROID="$NATIVE"
    unset RENPY_STEAM_PLATFORM
    unset RENPY_STEAM_SDK

    pushd "$RENPY_ROOT/module"

    setup_py "renpy"

    popd
}

"$@"
