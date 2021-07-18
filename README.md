# DWC Docker Deployment

This provides a Docker setup, which enables you to run your own Multiplayer Server for several Nintendo Wii Games (Mario Kart Wii, SSBB, etc.).

## Requirements

This has only been tested on Ubuntu 20.04.

 - Docker - ```sudo apt install docker.io```
 - Docker Compose - ```sudo apt install docker-compose```

## Network Setup - Server

Make sure that your server is reachable via the following ports:

| Protocol | Port  | Service                    |
|----------|-------|----------------------------|
| TCP      | 80    | WebServer                  |
| TCP      | 8000  | StorageServer              |
| TCP      | 9000  | NasServer                  |
| TCP      | 9001  | InternalStatsServer        |
| TCP      | 27500 | GameSpyManager             |
| TCP      | 28910 | GameSpyServerBrowserServer |
| TCP      | 29900 | GameSpyProfileServer       |
| TCP      | 29901 | GameSpyPlayerSearchServer  |
| TCP      | 29920 | GameSpyGamestatsServer     |
| UDP      | 27900 | GameSpyQRServer            |
| UDP      | 27901 | GameSpyNatNegServer        |

The following ports are optional:

| Protocol | Port  | Service                    |
|----------|-------|----------------------------|
| TCP      | 9003  | Dls1Server                 |
| TCP      | 9009  | AdminPage                  |
| TCP      | 9000  | RegisterPage               |

## Network Setup - Clients

Remember that you need a Dolphin Client with the correct modifications to be able to join a spoofed server.
Every client systems also needs the correct DNS records to be able to connect to your server. These can be provided by adding them to the Hosts file of each client:

```
PUBLIC_IP		gamestats.gs.nintendowifi.net
PUBLIC_IP		gamestats2.gs.nintendowifi.net
PUBLIC_IP		gpcm.gs.nintendowifi.net
PUBLIC_IP		gpsp.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.available.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.gamestats.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.gamestats2.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.master.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.ms19.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.natneg1.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.natneg2.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.natneg3.gs.nintendowifi.net
PUBLIC_IP		mariokartwii.sake.gs.nintendowifi.net
PUBLIC_IP		naswii.nintendowifi.net
PUBLIC_IP		nas.nintendowifi.net
PUBLIC_IP		nintendowifi.net
PUBLIC_IP		wiimmfi.de
```

## Installation

```
git clone https://github.com/theforcer/dwc-docker/
cd dwc-docker
sudo docker-compose up -d
```

Persistent data is stored in a Docker-managed volume. With a usual Docker installation, you should find the databases in ```/var/lib/docker/volumes/dwc_data/_data```.

## Other tidbits

- Some of the HTTP requests from Dolphin contain a duplicate "Host" Header for whatever reason. An up-to-date NGINX complains, logs this as an INFO error (does not show up by default in error_log) and does not proxy the request to the server. This could be solved via some rewrite magic, for now we are using an older version of NGINX.

- Services running in containers on the localhost interface will not be able to communicate with other container services. Therefore these services now run on all interfaces, so the NGINX <--> server communication can take place.