#!/usr/bin/env python3
# Cisco-Konfig-Generator (IT-Admin I)
# Aufbau: Schritt für Schritt nach "Aufgabenbereich" (wie Klausur/Übung)
# Nur das, was ihr typischerweise hattet: VLAN/Access/Trunk/PortSec/DHCP/RIP/DefaultRoute/MAC-Listen

# ==================================================
# AUFGABENBEREICH 1: VLANs anlegen + Namen
# (Wenn die Aufgabe VLANs fordert)
# ==================================================
vlans = [
    (10, "VLAN10"),
    (20, "VLAN20"),
    (40, "VLAN40"),
]

print("enable")
print("conf t")

for vlan_id, vlan_name in vlans:
    print(f"vlan {vlan_id}")
    print(f" name {vlan_name}")
    print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 2: Access-Ports (Port ↔ VLAN)  (len + 2 Listen)
# (Typische Aufgabe: Ports zu VLANs zuordnen)
# ==================================================
access_ports = [1, 2, 4]
access_vlans = [10, 20, 40]

print("enable")
print("conf t")

for i in range(len(access_ports)):
    print(f"interface FastEthernet0/{access_ports[i]}")
    print(" switchport mode access")
    print(f" switchport access vlan {access_vlans[i]}")
    print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 3: Trunk-Ports + allowed VLANs
# (Typische Aufgabe: Trunk konfigurieren)
# ==================================================
trunk_ports = [3]
allowed_vlans_for_trunks = [10, 20, 40]   # wird als "10,20,40" ausgegeben
allowed_str = ",".join(str(v) for v in allowed_vlans_for_trunks)

print("enable")
print("conf t")

for port in trunk_ports:
    print(f"interface FastEthernet0/{port}")
    print(" switchport mode trunk")
    print(f" switchport trunk allowed vlan {allowed_str}")
    print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 4: Port-Security auf bestimmten Ports
# (Übung/Klausur: PortSec-Branch)
# ==================================================
portsec_ports = [1, 2]

print("enable")
print("conf t")

for port in portsec_ports:
    print(f"interface FastEthernet0/{port}")
    print(" switchport port-security")
    print(" switchport port-security maximum 2")
    print(" switchport port-security violation restrict")
    print(" switchport port-security mac-address sticky")
    print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 5: Router-Interfaces IP + no shutdown (len + 3 Listen)
# (Wenn Router-Interfaces gesetzt werden müssen)
# ==================================================
router_interfaces = ["GigabitEthernet0/0", "GigabitEthernet0/1"]
router_ips        = ["192.168.10.1",      "192.168.20.1"]
router_masks      = ["255.255.255.0",     "255.255.255.0"]

print("enable")
print("conf t")

for i in range(len(router_interfaces)):
    print(f"interface {router_interfaces[i]}")
    print(f" ip address {router_ips[i]} {router_masks[i]}")
    print(" no shutdown")
    print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 6: DHCP auf Router (Pool + Excluded)
# (Sehr typisch: „DHCP-Konfiguration ausgeben“)
# ==================================================
dhcp_excluded_start = "192.168.10.1"
dhcp_excluded_end   = "192.168.10.20"

dhcp_pool_name      = "VLAN10"
dhcp_network        = "192.168.10.0"
dhcp_mask           = "255.255.255.0"
dhcp_default_router = "192.168.10.1"
dhcp_dns            = "8.8.8.8"

print("enable")
print("conf t")

print(f"ip dhcp excluded-address {dhcp_excluded_start} {dhcp_excluded_end}")

print(f"ip dhcp pool {dhcp_pool_name}")
print(f" network {dhcp_network} {dhcp_mask}")
print(f" default-router {dhcp_default_router}")
print(f" dns-server {dhcp_dns}")
print(" exit")

print("end")


# ==================================================
# AUFGABENBEREICH 7: RIP v2 (dynamisches Routing) + Default Route
# (Typisch: RIP + Default Route 0.0.0.0/0)
# ==================================================
rip_networks = ["192.168.10.0", "192.168.20.0"]
default_route_next_hop = "192.168.20.254"

print("enable")
print("conf t")

print("router rip")
print(" version 2")
print(" no auto-summary")

for net in rip_networks:
    print(f" network {net}")

print(" exit")

print(f"ip route 0.0.0.0 0.0.0.0 {default_route_next_hop}")

print("end")


# ==================================================
# AUFGABENBEREICH 8: MAC-Adressen-Liste ausgeben (für „moremacs“ / Tippfehlerfix)
# (Übungsnah: manchmal sollten neue MACs verwendet werden)
# ==================================================
macs = [
    "aaaa.bbbb.ccc1",
    "aaaa.bbbb.ccc2",
    "aaaa.bbbb.ccc3",
]

# Beispiel: Ausgabe einer Tabelle/Übersicht (nur Text, keine Cisco-CLI)
# Wenn ihr MACs in Konfig einbauen musstet, kann man daraus gezielt Zeilen bauen.
print("enable")
print("conf t")

for i in range(len(macs)):
    # Beispiel-Pattern (anpassen, falls eure Aufgabe konkrete Zeilen vorgibt)
    print(f"! MAC[{i}] = {macs[i]}")

print("end")
