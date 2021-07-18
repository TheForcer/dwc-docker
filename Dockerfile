FROM python:2.7-slim

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends git && \
    pip install twisted

# Replacments to enable listening on all interfaces, also to put DBs in extra directory
RUN git clone https://github.com/barronwaffles/dwc_network_server_emulator.git /dwc && \
    sed -i "s/127.0.0.1/0.0.0.0/g" /dwc/altwfc.cfg && \
    sed -i "s?gpcm.db?./data/gpcm.db?g" /dwc/gamespy/gs_database.py && \
    sed -i "s?storage.db?./data/storage.db?g" /dwc/storage_server.py && \
    mkdir /dwc/data
COPY adminpageconf.json /dwc/adminpageconf.json

EXPOSE 8000 9000 9001 27500 28910 29900 29901 29920 27900/udp 27901/udp

WORKDIR /dwc/
CMD python master_server.py
