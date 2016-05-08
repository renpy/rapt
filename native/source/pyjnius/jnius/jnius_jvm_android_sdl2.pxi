# on android, rely on SDL to get the JNI env
cdef extern void *SDL_AndroidGetJNIEnv()

cdef JNIEnv *get_platform_jnienv():
    return <JNIEnv *> SDL_AndroidGetJNIEnv()
