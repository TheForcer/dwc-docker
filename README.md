# DWC Docker Deployment

This repo provides a Docker setup, which enables you to run your own Multiplayer Server for several Nintendo Wii Games (Mario Kart Wii, SSBB, etc.).

## Requirements

This has been successfully tested on x64 Ubuntu 20.04 and Debian 11.

ARM architecture (for Raspberry Pi, M1 Macs etc.) is also supported, but hasn't been tested yet.

 - git - ```sudo apt install git```
 - Docker - ```sudo apt install docker.io```
 - Docker Compose - ```sudo apt install docker-compose```

## Installation

```
git clone https://github.com/theforcer/dwc-docker/
cd dwc-docker
sudo docker-compose up -d
``` 

Persistent data (account data etc.) is stored in a Docker-managed volume. With a typical Docker installation, you should find the databases in ```/var/lib/docker/volumes/dwc_data/_data```.

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
| TCP      | 9998  | RegisterPage               |

## Network Setup - Clients

Every participating Dolphin client has to complete the following steps to be able to join a spoofed server.

First up, every client systems needs the correct DNS records to be able to connect to your "fake" Nintendo WFC server. These can be provided by adding them to the hosts file of each client. You can also use the "client_dns_modifier" script, which can be run as is within a Python environment or by using the provided executable.

If you'd like, you can use PyInstaller to create your own executable: `pyinstaller --uac-admin --onefile --console client_dns_modifier.py`

```
SERVER_IP		gamestats.gs.nintendowifi.net
SERVER_IP		gamestats2.gs.nintendowifi.net
SERVER_IP		gpcm.gs.nintendowifi.net
SERVER_IP		gpsp.gs.nintendowifi.net
SERVER_IP		mariokartwii.available.gs.nintendowifi.net
SERVER_IP		mariokartwii.gamestats.gs.nintendowifi.net
SERVER_IP		mariokartwii.gamestats2.gs.nintendowifi.net
SERVER_IP		mariokartwii.master.gs.nintendowifi.net
SERVER_IP		mariokartwii.ms19.gs.nintendowifi.net
SERVER_IP		mariokartwii.natneg1.gs.nintendowifi.net
SERVER_IP		mariokartwii.natneg2.gs.nintendowifi.net
SERVER_IP		mariokartwii.natneg3.gs.nintendowifi.net
SERVER_IP		mariokartwii.sake.gs.nintendowifi.net
SERVER_IP		naswii.nintendowifi.net
SERVER_IP		nas.nintendowifi.net
SERVER_IP		nintendowifi.net
SERVER_IP		wiimmfi.de
```

Also, the games you want to play need to connect via plain HTTP to the server, since we cannot spoof the SSL certificates for Nintendo domains. For Mario Kart Wii, this can be achieved by using a Gecko Cheat Code:

~~~
c0000000 0000001d
3c004e80 60000020
900f0000 3d208000
3d00817f 61292fff
6108ffef 480000bc
89690001 2f8b0068
40be00ac 89690002
2f8b0074 40be00a0
89690003 2f8b0074
40be0094 89690004
2f8b0070 40be0088
89690005 2f8b0073
40be007c 89690006
2f8b003a 40be0070
89690007 2f8b002f
40be0064 89690008
2f8b002f 40be0058
89690009 2f8b0000
419e004c 7d2a4b78
39600000 48000008
396b0001 8cea0001
2f870000 409efff4
38cbfffd 38e90005
39400000 39290006
7cc903a6 48000010
7cc950ae 7cc751ae
394a0001 4200fff4
7c005a14 7c090378
38090001 7f804040
409dff40 4e800020
f0000000 00000000
~~~

## Other tidbits

- Some of the HTTP requests from Dolphin contain a duplicate "Host" Header for whatever reason. An up-to-date NGINX complains, logs this as an INFO error (does not show up by default in error_log) and does not proxy the request to the server (Similar behaviour for other proxies such as Caddy as well). This is why HAProxy is being used.

- Services running in containers on the localhost interface will not be able to communicate with other container services. Therefore these services now run on all interfaces, so the HAProxy <--> server communication can take place.

- This also works for Custom Track Mario Kart Wii Distributions. The setup has been successfully tested with 7 players and [Mario Kart Fun 2013-10](https://wiki.tockdom.com/wiki/Wiimms_Mario_Kart_Fun_2013-10)