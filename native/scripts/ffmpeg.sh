. "$NATIVE/scripts/common.sh"

version="3.0"

unpack () {
    tar xjf "$SOURCE/ffmpeg-$version.tar.bz2"
}


build () {
    activate_toolchain

    pushd "ffmpeg-$version"

    ./configure --prefix="$INSTALLDIR" \
       --cc="$CC" \
       --ld="$CC" \
       --target-os=android \
       --arch=$FFMPEG_ARCH \
       --extra-cflags="$CFLAGS" \
       --extra-ldflags="$LDFLAGS" \
       --extra-ldexeflags=-pie \
       --enable-cross-compile \
       --disable-shared \
       --enable-static \
       --enable-runtime-cpudetect \
       --enable-avresample \
       --disable-encoders \
       --disable-muxers \
       --disable-bzlib \
       --disable-demuxers \
       --enable-demuxer=au \
       --enable-demuxer=avi \
       --enable-demuxer=flac \
       --enable-demuxer=m4v \
       --enable-demuxer=matroska \
       --enable-demuxer=mov \
       --enable-demuxer=mp3 \
       --enable-demuxer=mpegps \
       --enable-demuxer=mpegts \
       --enable-demuxer=mpegtsraw \
       --enable-demuxer=mpegvideo \
       --enable-demuxer=ogg \
       --enable-demuxer=wav \
       --disable-decoders \
       --enable-decoder=flac \
       --enable-decoder=mp2 \
       --enable-decoder=mp3 \
       --enable-decoder=mp3on4 \
       --enable-decoder=mpeg1video \
       --enable-decoder=mpeg2video \
       --enable-decoder=mpegvideo \
       --enable-decoder=msmpeg4v1 \
       --enable-decoder=msmpeg4v2 \
       --enable-decoder=msmpeg4v3 \
       --enable-decoder=mpeg4 \
       --enable-decoder=pcm_dvd \
       --enable-decoder=pcm_s16be \
       --enable-decoder=pcm_s16le \
       --enable-decoder=pcm_s8 \
       --enable-decoder=pcm_u16be \
       --enable-decoder=pcm_u16le \
       --enable-decoder=pcm_u8 \
       --enable-decoder=theora \
       --enable-decoder=vorbis \
       --enable-decoder=opus \
       --enable-decoder=vp3 \
       --enable-decoder=vp8 \
       --enable-decoder=vp9 \
       --disable-parsers \
       --enable-parser=mpegaudio \
       --enable-parser=mpegvideo \
       --enable-parser=mpeg4video \
       --enable-parser=vp3 \
       --enable-parser=vp8 \
       --disable-protocols \
       --disable-devices \
       --disable-vdpau \
       --disable-vda \
       --disable-filters \
       --disable-bsfs \
       --disable-stripping \
       --disable-iconv

    make
    make install

    popd
}


"$1"

