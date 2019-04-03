# Craig Stringham (craig@capellaspace.com)
# Date: March 2019

FROM continuumio/anaconda3 as build

RUN conda install -y cartopy
RUN conda install -y pip
WORKDIR /opt/
# TODO get changes pushed in to scottyhq's branch
RUN git clone https://github.com/stringhamc/dinosar.git
WORKDIR /opt/dinosar
RUN pip install .

# Used this entrypoint to create a user matching our userid
# Following: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
RUN apt-get update && apt-get -y --no-install-recommends install ca-certificates curl gnupg2 dirmngr
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu


COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

WORKDIR /home/user

CMD /bin/bash
