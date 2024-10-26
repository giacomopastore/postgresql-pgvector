FROM postgres:17

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y postgresql-server-dev-all && \
    apt-get install -y git && \
    apt-get install -y gcc make && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && make install && \
    cd .. && rm -rf pgvector && \
    apt-get remove -y gcc make && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 5432