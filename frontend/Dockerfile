FROM nginx:1.27

# set environment variables
ENV BASE_DIRECTORY=/data
ENV SSL_DIRECTORY=/data/ssl
ENV CONFD_VERSION=0.16.0
ENV S6_OVERLAY_VERSION=3.2.0.0

# install additional packages
RUN \
 apt-get update && \
 apt-get install -y procps wget xz-utils && \
 apt-get autoremove && \
 apt-get clean && \
 rm -rf \
	/tmp/* \
	/var/lib/apt/lists/* \
	/var/tmp/*

# s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# copy root overlay
COPY docker /

# copy web assets
COPY dist/mixmatch/browser /data/www/

# create mixmatch user
RUN useradd -u 911 -U -d ${BASE_DIRECTORY} mixmatch && \
    usermod -G users mixmatch

# install confd
RUN \
  wget https://github.com/kelseyhightower/confd/releases/download/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64 \
  -q -O /usr/bin/confd && \
  chmod 0755 /usr/bin/confd

ENTRYPOINT ["/init"]
CMD []
