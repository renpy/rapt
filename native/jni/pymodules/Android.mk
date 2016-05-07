LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := $(INSTALLDIR)/lib/libpymodules.so
LOCAL_MODULE := pymodules

include $(PREBUILT_SHARED_LIBRARY)

