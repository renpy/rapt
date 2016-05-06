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

    bash "$NATIVE/scripts/$1.sh" $2

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
