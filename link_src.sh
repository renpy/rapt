#!/bin/bash

root="$(cd $(dirname $0); pwd)"
dist="$root/dist/${1:-renpy}"


set -e

rm -Rf "$dist/src"
ln -s "$root/python-for-android/src/src" "$dist/src"

