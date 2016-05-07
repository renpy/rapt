from distutils.core import setup, Extension
import os

setup(name='android',
      version='1.0',
      packages=['android'],
      package_dir={'android': 'android'},
      ext_modules=[

        Extension(
            'android._android', ['android/_android.c', 'android/_android_jni.c'],
            libraries=[ 'log' ],
            ),
        ]
      )
