. "$NATIVE/scripts/common.sh"

link () {
    activate_toolchain

    "$NATIVE/scripts/biglink.py" "$INSTALLDIR/lib/libpymodules.so" "$BUILD/pymodules"
}


"$@"
