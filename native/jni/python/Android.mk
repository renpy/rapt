LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := python

LOCAL_SRC_FILES := $(INSTALLDIR)/lib/libpython2.7.so
LOCAL_EXPORT_C_INCLUDES := $(INSTALLDIR)/include/python2.7

include $(PREBUILT_SHARED_LIBRARY)

