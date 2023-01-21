# DWC Docker Deployment

This repo provides a Docker setup that allows you to run your own multiplayer server for a number of Nintendo Wii games (most notably Mario Kart Wii).

## Requirements

As this setup builds the server container manually, any system running Docker should work fine.

 - git - `sudo apt install git`
 - Docker - `sudo apt install docker.io`
 - Docker Compose - `sudo apt install docker-compose`

## Installation

```
git clone https://github.com/theforcer/dwc-docker/
cd dwc-docker
```

If you want to use a custom domain for your server, replace the nintendowifi.net appearances in the haproxy.cfg file with your domain name (e.g. `sed -i 's/nintendowifi.net/example.com/g' haproxy.cfg`) to your domain name. You will also need to patch the domain name into the game later (see network setup method 1).

If you want to connect using spoofed nintendowifi.net records (network setup method 2), leave them as they are and start the server with

```
docker-compose up -d
```

Persistent data (account information, etc.) is stored in a Docker-managed volume. In a typical Docker installation, you should find the databases in `/var/lib/docker/volumes/dwc_data/_data`.

## Network Setup - Server

Make sure your server is accessible on the following ports:

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
| TCP      | 9998  | RegisterPage               |^

If you are using a custom domain, the correct DNS records for the subdomains must also point to your server's IP; see Method 2 for a list of required subdomains for Mario Kart Wii.

## Network Setup - Clients

There are three ways to allow Dolphin clients to connect to your "fake" server.

The first is to patch the server domain in the game ISO that you use, the second is to manually change the DNS records for nintendowifi.net on each PC. Finally, you could create a custom DNS server for the PCs to use, but that would open a can of worms of its own.

The following sections explain how to patch a Mario Kart ROM or make the local DNS changes using the hosts file.

### Method 1: Creating a patched MKW ISO

#### Preparation

- Download the Wii ISO Toolset from https://wit.wiimm.de/wit/
	- This can be used to pack and unpack Wii ISOs, file structures, WBFS etc.
- Download the Wii SZS Toolset from https://szs.wiimm.de/
	- This can be used to manipulate the game files directly.
- Unzip all the tools in the appropriate folders.

#### Patching

- Move the game ISO to the bin directory inside the wit folder. Now extract the ISO with `\wit.exe extract 'MarioKartWii.iso' mkw`. This will create a folder called `mkw` containing the game files.
- Locate the files `sys/main.dol` and `files/rel/StaticR.rel` and add them to the bin directory of the szs folder.
- Now we patch the domain name with the command `.\wstrt.exe PATCH --https DOMAIN --domain example.com main.dol StaticR.rel`, using example.com as an example. This will also convert all HTTPS requests to plain HTTP.
- The tool should indicate that both files have been successfully patched.
- Now the two patched files can be copied back to their original location in the ROM folder (mkw).
- The folder containing the game files can then be packed into an ISO with `.\wit.exe COPY mkw MarioKartWii_patched.iso`.
- The ISO can now be used to play on your alternative server in Dolphin.

### Method 2: Spoofing nintendowifi.net DNS records

The code snippet below shows which name records need to be spoofed. You can add these manually to your DNS server, `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts` file. You can also automate this by using the "client_dns_modifier" script, which can be run as is within a Python environment or by using the supplied executable.

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

Also, the games you want to play must connect to the server via plain HTTP, as we cannot spoof the SSL certificates for Nintendo's domains. For Mario Kart Wii, we can use a Gecko cheat code to patch HTTPS calls to HTTP:

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

- Some of the HTTP requests from Dolphin contain a duplicate "Host" header for some reason. A recent NGINX complains, logs this as an INFO error (not shown in error_log by default) and does not proxy the request to the server (similar behaviour for other proxies like Caddy as well). This is why HAProxy is used.
- Services running in containers on the localhost interface will not be able to communicate with other container services. So these services are now running on all interfaces so that the HAProxy <--> server communication can take place.
- This also works for Custom Track Mario Kart Wii distributions. The setup has been successfully tested with 7 players and [Mario Kart Fun 2013-10](https://wiki.tockdom.com/wiki/Wiimms_Mario_Kart_Fun_2013-10)
