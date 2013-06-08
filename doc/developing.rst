=================
Developer's Guide
=================

This explains how to build and change PGS4A, if that's what you want
to do. You don't need this if all you're doing is developing *with*
PGS4A.

Compiling
=========

.. note::

    This has only been tried on Linux, and probably won't work on
    Windows without a lot of work.

PGS4A is built using a series of scripts. The :program:`build_all.sh`
script will build all of PGS4A, by calling the scriptsi in the
appropriate order. Beyond that:

:program:`environment.sh`

    Is called by the other scripts, and sets up the build
    environment. It expects android-ndk-r4b and android-sdk-linux_86
    to be in the current directory.

:program:`build_python.sh`

    Cross-compiles python. For this to work, a host-compiled python
    and pgen must be in the Python-2.6.4 directory. If they aren't
    there, linux-x64 binaries will be copied in - which probably won't
    help if you use a different system.

:program:`build_sdl.sh`

    Builds the SDL libraries.

:program:`build_pygame.sh`

    Builds pygame. Build_modules.sh must be called after this is run.

:program:`fill_python.sh`

    Cleans the private directory, and fills it with the Python and Pygame
    modules that will be used by the program. This script contains a
    list of modules to include.

:program:`build_modules.sh`

    Builds the android-specific modules, and the shared library that
    contains all of the binary modules in it.
    
:program:`liblink` and `biglink`

    Shared-library python modules should be compiled using
    :program:`liblink` instead of :program:`ld`.
    :program:`build_modules.sh` uses :program:`biglink` to merge them into a
    single file, libpymodules.so.

    This is necessary because Android has a limitation of 64 shared
    libraries per process.

    Due to limitations of Python and :program:`biglink`, there can
    only be one shared-library module with a given name in pygame and
    the user's code. Since ``pygame.time`` exists, the module ``mycode.time``
    will conflict with it. This doesn't apply to modules that are part
    of Python itself, so ``pygame.time`` can exist alongside the python
    ``time`` module.


Directories
===========

A PGS4A source build includes or creates the following interesting
directories:

assets/

    Contains the private.mp3 and public mp3 files, containing the game
    data. These are tar.gz files, renamed to mp3 to prevent them from
    being compressed by the Android build tooks.

bin/

    Apk files are created here.

buildlib/

    This directory contains the code used by android.py, and the libraries
    that code depends on.

doc/

    Contains the sphinx source for this documentation.

jni/

    Contains the source and build scripts for an NDK build of the
    SDL libraries. jni/application/src/start.pyx is the Cython
    file that's used to bootstrap Python.

private/

    This is where the files installed to the private areas of the
    android device live.

pygame-1.9.1release/

    The pygame source code.

Python-2.7.1/

    The python source code.

python-install/

    Where the cross-compiled Python is installed to after it is built.

res/

    Android resources.

runtimelib/

    Source code for Python modules that are installed to the device.

sdl/

    Source code for SDL. (We use SDL-1.2).

src/

    Java source code.

templates/

    This directory contains templates that are used to generate
    control files, and the default icons and presplash screens.
