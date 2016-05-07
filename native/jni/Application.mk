APP_PROJECT_PATH := $(call my-dir)/..

APP_MODULES := python SDL2 png16 jpeg SDL2_image SDL2_gfx SDL2_ttf SDL2_mixer freetype main pymodules

APP_ABI := $(ARCH)
APP_STL := gnustl_static
APP_CFLAGS += $(OFLAG)

APP_PLATFORM := android-9
