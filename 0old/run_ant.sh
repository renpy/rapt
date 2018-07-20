#!/bin/bash

root="$(cd $(dirname $0); pwd)"
dist="$root/dist/${ANDROID_DIST:-renpy}"

set -e

cd $dist
ant "$@"
