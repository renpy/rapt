#!/bin/bash

./build_pgs4a.sh 

D=dist/pgs4a

ln -s /tmp/android-sdk "$D"
ln -s /tmp/apache-ant "$D"

cd "$D"

(echo no) | ./android.py installsdk 
./android.py build /home/tom/ab/android/tests/color_touch debug install
