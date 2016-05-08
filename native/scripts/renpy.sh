. "$NATIVE/scripts/common.sh"

build () {
    export RENPY_ANDROID="$NATIVE"

    pushd "$RENPY_ROOT/module"

    setup_py "renpy"

    popd
}

"$@"
