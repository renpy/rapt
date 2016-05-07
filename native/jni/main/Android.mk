LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := main

SDL_PATH := ../sdl2

LOCAL_C_INCLUDES := $(LOCAL_PATH)/$(SDL_PATH)/include  $(LOCAL_PATH)/../sdl2_image $(LOCAL_PATH)/../../install/$(TARGET_ARCH_ABI)/include/python2.7

# Add your application source files here...
LOCAL_SRC_FILES := $(SDL_PATH)/src/main/android/SDL_android_main.c \
        main.c

LOCAL_SHARED_LIBRARIES := SDL2 SDL2_image

LOCAL_LDFLAGS += -L$(LOCAL_PATH)/../../install/$(TARGET_ARCH_ABI)/lib
LOCAL_LDLIBS := -lGLESv1_CM -lGLESv2 -lpython2.7 -llog

include $(BUILD_SHARED_LIBRARY)
