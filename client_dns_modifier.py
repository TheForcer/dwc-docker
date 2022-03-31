from python_hosts import Hosts, HostsEntry, is_ipv4
from time import sleep
import ctypes, os


def is_admin():
    try:
        admin = (os.getuid() == 0)
    except AttributeError:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return admin

# Hostnames we need to spoof
wfc_hostnames = [
    "gamestats.gs.nintendowifi.net",
    "gamestats2.gs.nintendowifi.net",
    "gpcm.gs.nintendowifi.net",
    "gpsp.gs.nintendowifi.net",
    "mariokartwii.available.gs.nintendowifi.net",
    "mariokartwii.gamestats.gs.nintendowifi.net",
    "mariokartwii.gamestats2.gs.nintendowifi.net",
    "mariokartwii.master.gs.nintendowifi.net",
    "mariokartwii.ms19.gs.nintendowifi.net",
    "mariokartwii.natneg1.gs.nintendowifi.net",
    "mariokartwii.natneg2.gs.nintendowifi.net",
    "mariokartwii.natneg3.gs.nintendowifi.net",
    "mariokartwii.sake.gs.nintendowifi.net",
    "naswii.nintendowifi.net",
    "nas.nintendowifi.net",
    "nintendowifi.net",
]

# Admin check
if not is_admin():
    print("No administrative privileges. Please restart as administrator!")
    sleep(5)
    exit()

# Get IP and check if it is a valid IPv4 address
ip_input = input("Please enter the IP address for the fake Nintendo WFC server: ")
try:
    if not is_ipv4(ip_input):
        raise ValueError
except ValueError:
    print("Not a valid IP address! Please try again.")
    sleep(5)
    exit()

# Add DNS records to the system
print("Adding DNS records to system...")
sleep(2)
hosts = Hosts()
for wfc_hostname in wfc_hostnames:
    hosts.add(
        [HostsEntry(entry_type="ipv4", address=ip_input, names=[wfc_hostname])],
        force=True,  # Force overwrite
        allow_address_duplication=True,  # Allow duplicate entries
    )
try:
    hosts.write()
    print("Added records successfully!")
except:
    print("Failed to add records! Did you run as administrator?")
    sleep(5)
    exit()

print("Done!")
sleep(10)
