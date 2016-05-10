LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := $(NATIVE)/install/$(TARGET_ARCH_ABI)/lib/libpymodules.so
LOCAL_MODULE := pymodules

include $(PREBUILT_SHARED_LIBRARY)

