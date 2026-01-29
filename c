## 1. Grundkonfiguration von Routern

**Was gemacht wurde:**
Router initialisiert, Hostname gesetzt, Passwörter vergeben, CLI abgesichert.

```
enable
configure terminal
hostname R1
enable secret cisco
line console 0
password cisco
login
exit
line vty 0 4
password cisco
login
exit
service password-encryption
end
write memory
```

---

## 2. IP‑Adressen auf Router‑Interfaces konfigurieren

**Was gemacht wurde:**
Interfaces mit IP‑Adressen versehen und aktiviert.

```
configure terminal
interface gigabitEthernet0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit
interface gigabitEthernet0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
exit
end
```

---

## 3. Switch‑Grundkonfiguration

**Was gemacht wurde:**
Switch benannt, Management‑IP vergeben, Default‑Gateway gesetzt.

```
enable
configure terminal
hostname S1
interface vlan 1
ip address 192.168.1.2 255.255.255.0
no shutdown
exit
ip default-gateway 192.168.1.1
end
write memory
```

---

## 4. PCs / Clients konfigurieren

**Was gemacht wurde:**
Endgeräte manuell mit IP, Subnetzmaske und Gateway versehen.

```
IP Address: 192.168.1.10
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.1.1
DNS Server: 8.8.8.8
```

---

## 5. Statisches Routing

**Was gemacht wurde:**
Manuelle Routen zwischen mehreren Netzwerken eingerichtet.

```
configure terminal
ip route 192.168.3.0 255.255.255.0 192.168.2.2
ip route 192.168.4.0 255.255.255.0 192.168.2.2
end
```

---

## 6. Default Route konfigurieren

**Was gemacht wurde:**
Standardroute für unbekannte Netze gesetzt.

```
configure terminal
ip route 0.0.0.0 0.0.0.0 192.168.1.254
end
```

---

## 7. RIP (Routing Information Protocol)

**Was gemacht wurde:**
Dynamisches Routing mit RIP v2 eingerichtet.

```
configure terminal
router rip
version 2
no auto-summary
network 192.168.1.0
network 192.168.2.0
end
```

---

## 8. DHCP‑Server auf Router konfigurieren

**Was gemacht wurde:**
Router als DHCP‑Server verwendet.

```
configure terminal
ip dhcp excluded-address 192.168.1.1 192.168.1.20
ip dhcp pool LAN1
network 192.168.1.0 255.255.255.0
default-router 192.168.1.1
dns-server 8.8.8.8
end
```

---

## 9. VLANs erstellen

**Was gemacht wurde:**
Virtuelle Netze auf Switches angelegt.

```
configure terminal
vlan 10
name Verwaltung
vlan 20
name Technik
exit
```

---

## 10. VLAN‑Ports zuweisen

**Was gemacht wurde:**
Switch‑Ports festen VLANs zugeordnet.

```
configure terminal
interface fastEthernet0/1
switchport mode access
switchport access vlan 10
exit
interface fastEthernet0/2
switchport mode access
switchport access vlan 20
exit
```

---

## 11. Trunk konfigurieren

**Was gemacht wurde:**
Verbindung zwischen Switches oder Router‑on‑a‑Stick.

```
configure terminal
interface gigabitEthernet0/1
switchport mode trunk
exit
```

---

## 12. Inter‑VLAN‑Routing (Router‑on‑a‑Stick)

**Was gemacht wurde:**
Routing zwischen VLANs über Subinterfaces.

```
configure terminal
interface gigabitEthernet0/0.10
encapsulation dot1Q 10
ip address 192.168.10.1 255.255.255.0
exit
interface gigabitEthernet0/0.20
encapsulation dot1Q 20
ip address 192.168.20.1 255.255.255.0
exit
```

---

## 13. ACL – Standard Access Control List

**Was gemacht wurde:**
Zugriff anhand der Quell‑IP eingeschränkt.

```
configure terminal
access-list 1 deny 192.168.1.0 0.0.0.255
access-list 1 permit any
interface gigabitEthernet0/0
ip access-group 1 in
end
```

---

## 14. ACL – Extended Access Control List

**Was gemacht wurde:**
Zugriff nach Quelle, Ziel und Protokoll gesteuert.

```
configure terminal
access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 80
access-list 100 deny ip any any
interface gigabitEthernet0/0
ip access-group 100 out
end
```

## 16. Tests & Fehlersuche

**Was gemacht wurde:**
Konnektivität geprüft und Konfiguration kontrolliert.

```
ping 192.168.1.1
tracert 192.168.2.10
show ip route
show running-config
show ip interface brief
```
