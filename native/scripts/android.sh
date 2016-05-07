. "$NATIVE/scripts/common.sh"

CYTHON=$(which cython)


gen() {
    if [ "$1.pyx" -nt  "$1.c" ]; then
        cython "$1.pyx"
    fi
}

build () {
    pushd "$SOURCE/android"

    gen android/_android
    setup_py "android"

    popd

}

"$1"
