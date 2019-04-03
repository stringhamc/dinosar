# Scott Henderson (scottyh@uw.edu)
# Date: July 2018
FROM nvidia/cuda:9.2-devel-ubuntu18.04 as build

WORKDIR /tmp

COPY v2.3.1.tar.gz SConfigISCE /tmp/

# Update Base Ubuntu installation
ENV DEBIAN_FRONTEND noninteractive


RUN apt update && \
    apt install -y gfortran libmotif-dev libhdf5-dev libfftw3-dev libgdal-dev scons python3 cython3 python3-scipy python3-matplotlib python3-h5py python3-gdal python3-pip gnupg2 dirmngr curl&& \
    rm -rf /var/lib/apt/lists/*

# build gosu for user switching
RUN gpg2 --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg2 --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

# Install ISCE and remove files from /tmp folder
RUN tar -zxf v2.3.1.tar.gz && \
    cd isce2-2.3.1 && \
    export PYTHONPATH=/tmp/isce2-2.3.1/configuration && \
    export SCONS_CONFIG_DIR=/tmp && \
    scons install --skipcheck && \
    rm -rf /tmp/*

# Multistage build reduces size (no need for all development libraries)
FROM nvidia/cuda:9.2-runtime-ubuntu18.04 as run 

# Install run-time libraries
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt install -y zip curl libmotif-common libfftw3-3 python3 cython3 python3-scipy python3-matplotlib python3-h5py python3-gdal python3-pip aria2 python3-ipython libxm4 && \
    rm -rf /var/lib/apt/lists/*

# Setup ISCE environment
ENV ISCE_ROOT /opt/isce2-2.3.1
ENV ISCE_HOME $ISCE_ROOT/isce
ENV PATH $ISCE_HOME/bin:$ISCE_HOME/applications:$PATH
ENV PYTHONPATH $ISCE_ROOT:$ISCE_HOME/applications:$ISCE_HOME/component

# Copy ISCE installation files
COPY --from=build /opt /opt
COPY --from=build /usr/local/bin/gosu /usr/local/bin/gosu

# Don't run container as root user
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

WORKDIR /home/user

CMD /bin/bash
