#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import subprocess

libs = [ ]
objects = [ ]
output = None

i = 1
while i < len(sys.argv):
    opt = sys.argv[i]
    i += 1

    if opt == "-o":
        output = sys.argv[i]
        i += 1
        continue

    if opt.startswith("-l") or opt.startswith("-L"):
        libs.append(opt)
        continue

    if opt in ("-r", "-pipe", "-no-cpp-precomp"):
        continue

    if opt in ("--sysroot", "-isysroot", "-framework", "-undefined",
            "-macosx_version_min"):
        i += 1
        continue

    if opt.startswith("-I"):
        continue

    if opt.startswith("-m"):
        continue

    if opt.startswith("-f"):
        continue

    if opt.startswith("-O"):
        continue

    if opt.startswith("-g"):
        continue

    if opt.startswith("-D"):
        continue

    if opt.startswith("-"):
        print(sys.argv)
        print("Unknown option: %s" % opt)
        sys.exit(1)

    if not opt.endswith('.o'):
        continue

    objects.append(opt)


module = os.path.join(os.environ["BUILD"], "pymodules", os.path.basename(output))

with open(module + ".libs", "w") as f:
    f.write(" ".join(libs))

ld = os.environ["GCC_ARCH"] + "-ld"

args = [ "ccache", ld, '-r', '-o', module + '.o'] + objects

if subprocess.call(args):
    sys.exit(1)

with open(output, "w") as f:
    pass

