from python_hosts import Hosts, HostsEntry

hosts_url = "https://theforcer.de/wii_hosts_mkw.txt"

print("Füge DNS-Einträge zu Hosts-Liste hinzu...")
hosts = Hosts()
hosts.import_url(url=hosts_url)
hosts.write()
print("Fertig")