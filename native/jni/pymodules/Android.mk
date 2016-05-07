LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := $(wildcard "$(INSTALLDIR)/lib/libpymodules.so", "")
LOCAL_MODULE := pymodules

ifneq ("$(LOCAL_SRC_FILES)", "") 
	include $(PREBUILT_SHARED_LIBRARY)
endif

