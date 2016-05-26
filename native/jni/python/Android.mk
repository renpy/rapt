LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := python

LOCAL_EXPORT_C_INCLUDES := $(NATIVE)/install/$(TARGET_ARCH_ABI)/include/python2.7
LOCAL_SRC_FILES := $(NATIVE)/install/$(TARGET_ARCH_ABI)/lib/libpython2.7.so

include $(PREBUILT_SHARED_LIBRARY)

