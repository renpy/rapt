#!/bin/bash

set -e

export NATIVE="$(dirname $(readlink -f $0))"

rm -Rf "$NATIVE/build"
rm -Rf "$NATIVE/lib"
rm -Rf "$NATIVE/install"
