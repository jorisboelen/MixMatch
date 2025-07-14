FROM python:3.11

# set environment variables
ENV BASE_DIRECTORY=/data
ENV IMAGE_DIRECTORY=/data/image
ENV MUSIC_DIRECTORY=/data/music
ENV MIXMATCH_ENABLE_API=true
ENV MIXMATCH_ENABLE_MIGRATE=true
ENV MIXMATCH_ENABLE_SCHEDULER=true
ENV MIXMATCH_ENABLE_WORKER=true
ENV S6_OVERLAY_VERSION=3.2.0.2

# s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# set work directory
WORKDIR /data

# install pip package
COPY dist/mixmatch-*.tar.gz .
RUN pip install --no-cache-dir mixmatch-*.tar.gz && rm -f mixmatch-*.tar.gz

# copy root overlay
COPY docker /

# create mixmatch user
RUN useradd -u 1000 -U -d ${BASE_DIRECTORY} mixmatch && \
    usermod -G users mixmatch

HEALTHCHECK CMD ["bash", "/etc/health_check.sh"]
EXPOSE 8000/tcp
ENTRYPOINT ["/init"]
