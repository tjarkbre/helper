#!/usr/bin/env python3
# Python + Cisco (IT-Admin I) – Komplett-Guide als EIN .py
# Zweck: Beim Ausführen wird eine gut lesbare Anleitung ausgegeben (mit Überschriften + Leerzeilen),
# die du direkt kopieren kannst. Inhalt: nur f-Strings, step-by-step, Cisco-Kombi.

def out(line=""):
    print(line)

def h(title: str):
    out("=" * len(title))
    out(title)
    out("=" * len(title))
    out()

def sh(title: str):
    out(title)
    out("-" * len(title))
    out()

def code(lines):
    out("```")
    for ln in lines:
        out(ln)
    out("```")
    out()

def main():
    h("Python + Cisco (IT-Admin I) – Komplett-Guide (nur f-Strings, step-by-step)")

    out("Ziel: Du musst nicht 'programmieren können'. Du nutzt Python als Text-Generator,")
    out("um Cisco-Konfigurationszeilen automatisch zu erzeugen.")
    out("Regel: Alles, was rauskommen soll, passiert über print(...).")
    out()

    h("0) Python ist ein Drucker")

    sh("0.1 Nur Text ausgeben (minimales Skript)")
    code([
        'print("enable")',
        'print("conf t")',
        'print("end")',
    ])
    out("Merke: Python läuft von oben nach unten. Jede print-Zeile ist 1:1 Output.")
    out()

    sh("0.2 Sinnvolles Grundgerüst für Cisco (Start/Ende)")
    code([
        'print("enable")',
        'print("conf t")',
        '# ... hier kommen deine automatisch erzeugten Zeilen ...',
        'print("end")',
    ])

    h("1) f-Strings (Lückentext) – das Wichtigste")

    sh("1.1 Ein Wert in Text einsetzen")
    code([
        "port = 5",
        'print(f"interface FastEthernet0/{port}")',
    ])
    out("Ausgabe: interface FastEthernet0/5")
    out("Merke: f\"...\" + {port} -> Wert wird eingesetzt.")
    out()

    sh("1.2 Mehrere Werte einsetzen")
    code([
        'ip = "192.168.10.1"',
        'mask = "255.255.255.0"',
        'print(f"ip address {ip} {mask}")',
    ])

    h("2) Listen (Sammlung von Werten)")

    sh("2.1 Liste definieren")
    code([
        "ports = [1, 4, 6]",
    ])
    out("Merke: Liste = mehrere Werte, die du nacheinander abarbeiten willst.")
    out()

    sh("2.2 Listen können auch Text enthalten (Interface-Namen)")
    code([
        'ifaces = ["GigabitEthernet0/0", "GigabitEthernet0/1"]',
    ])

    h("3) Einfache Schleife: für jedes Element (Copy-Paste-Automat)")

    sh("3.1 Für jeden Port eine Zeile")
    code([
        "ports = [1, 4, 6]",
        "for port in ports:",
        '    print(f"interface FastEthernet0/{port}")',
    ])

    sh("3.2 Für jeden Port mehrere Zeilen (Cisco-Block)")
    code([
        "ports = [1, 4, 6]",
        "for port in ports:",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode access")',
        '    print(" exit")',
    ])
    out("Merke: Alles, was eingerückt ist, wird pro Element wiederholt.")
    out()

    h("4) range(): Zahlenbereiche (Ports 10 bis 20)")

    sh("4.1 Ports 10..20")
    code([
        "for port in range(10, 21):",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" exit")',
    ])
    out("Merke: range(10, 21) -> 10..20 (die letzte Zahl zählt nicht mit).")
    out()

    h("5) Zwei Listen parallel (Port ↔ VLAN) – Klausurklassiker")

    out("Situation: Port 1->VLAN10, Port 4->VLAN10, Port 6->VLAN20")
    out()

    sh("5.1 Zwei Listen")
    code([
        "ports = [1, 4, 6]",
        "vlans = [10, 10, 20]",
    ])

    sh("5.2 Parallel abarbeiten (gleiche Position gehört zusammen)")
    code([
        "ports = [1, 4, 6]",
        "vlans = [10, 10, 20]",
        "",
        "for i in range(len(ports)):",
        "    port = ports[i]",
        "    vlan = vlans[i]",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode access")',
        '    print(f" switchport access vlan {vlan}")',
        '    print(" exit")',
    ])
    out("Merke: i ist nur die Position (0,1,2,...). ports[i] passt zu vlans[i].")
    out()

    h("6) Access + Trunk getrennt (typisches Cisco-Muster)")

    sh("6.1 Access-Ports mit VLANs + Trunk-Ports")
    code([
        "access_ports = [1, 4, 6, 10, 11, 13]",
        "access_vlans = [10,10,20,20,10,10]",
        "trunk_ports  = [2, 3]",
        "",
        'print("enable")',
        'print("conf t")',
        "",
        "# Access Ports",
        "for i in range(len(access_ports)):",
        "    port = access_ports[i]",
        "    vlan = access_vlans[i]",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode access")',
        '    print(f" switchport access vlan {vlan}")',
        '    print(" exit")',
        "",
        "# Trunk Ports",
        "for port in trunk_ports:",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode trunk")',
        '    print(" exit")',
        "",
        'print("end")',
    ])

    h("7) Bedingungen (if/else) – optionales Werkzeug")

    sh("7.1 Einfaches if")
    code([
        "vlan = 10",
        "if vlan == 10:",
        '    print("name USERS")',
        "else:",
        '    print("name OTHER")',
    ])

    sh("7.2 Wenn Port in trunk_ports, sonst access (Alternative)")
    code([
        "ports = [1,2,3,4]",
        "trunk_ports = [2,3]",
        "for port in ports:",
        '    print(f"interface FastEthernet0/{port}")',
        "    if port in trunk_ports:",
        '        print(" switchport mode trunk")',
        "    else:",
        '        print(" switchport mode access")',
        '        print(" switchport access vlan 10")',
        '    print(" exit")',
    ])
    out("Merke: `if port in trunk_ports` prüft, ob der Port in der Liste steht.")
    out()

    h("8) Schleifen ineinander (verschachtelt) – VLAN gruppieren")

    sh("8.1 VLAN-Gruppen: VLAN + Portliste")
    code([
        "vlan_groups = [",
        "    (10, [1,4,11]),",
        "    (20, [6,10]),",
        "]",
    ])

    sh("8.2 Ausgabe: VLAN anlegen + Ports zuweisen")
    code([
        "vlan_groups = [",
        "    (10, [1,4,11]),",
        "    (20, [6,10]),",
        "]",
        "",
        'print("enable")',
        'print("conf t")',
        "",
        "for vlan, ports in vlan_groups:",
        '    print(f"vlan {vlan}")',
        '    print(f" name VLAN{vlan}")',
        '    print(" exit")',
        "",
        "    for port in ports:",
        '        print(f"interface FastEthernet0/{port}")',
        '        print(" switchport mode access")',
        '        print(f" switchport access vlan {vlan}")',
        '        print(" exit")',
        "",
        'print("end")',
    ])
    out("Merke: außen VLAN, innen Ports. So gruppierst du sauber.")
    out()

    h("9) VLAN-Namen aus Portliste bauen (String zusammenbauen)")

    sh("9.1 Name: vlan10_ports_1_4_11")
    code([
        "vlan = 10",
        "ports = [1,4,11]",
        'tail = "_".join(str(p) for p in ports)',
        'name = f"vlan{vlan}_ports_{tail}"',
        "print(name)",
    ])

    sh("9.2 Cisco: VLAN + Name ausgeben")
    code([
        "vlan = 10",
        "ports = [1,4,11]",
        'tail = "_".join(str(p) for p in ports)',
        'name = f"vlan{vlan}_ports_{tail}"',
        "",
        'print(f"vlan {vlan}")',
        'print(f" name {name}")',
        'print(" exit")',
    ])

    h("10) Router-Interfaces: Interface ↔ IP ↔ Maske (Listen parallel)")

    sh("10.1 Router-Konfig aus Listen")
    code([
        'interfaces = ["GigabitEthernet0/0", "GigabitEthernet0/1"]',
        'ips        = ["192.168.10.1",      "192.168.11.1"]',
        'masks      = ["255.255.255.0",     "255.255.255.0"]',
        "",
        'print("enable")',
        'print("conf t")',
        "",
        "for i in range(len(interfaces)):",
        "    iface = interfaces[i]",
        "    ip    = ips[i]",
        "    mask  = masks[i]",
        '    print(f"interface {iface}")',
        '    print(f" ip address {ip} {mask}")',
        '    print(" no shutdown")',
        '    print(" exit")',
        "",
        'print("end")',
    ])

    sh("10.2 Optional: speed/duplex (nur wenn gefordert)")
    code([
        'speed_values  = ["100", "auto"]',
        'duplex_values = ["full","auto"]',
        "",
        "for i in range(len(interfaces)):",
        '    print(f"interface {interfaces[i]}")',
        '    print(f" ip address {ips[i]} {masks[i]}")',
        '    print(f" speed {speed_values[i]}")',
        '    print(f" duplex {duplex_values[i]}")',
        '    print(" no shutdown")',
        '    print(" exit")',
    ])

    h("11) Validierung: wenn ungültig -> auto (kleine Absicherung)")

    sh("11.1 speed validieren")
    code([
        'allowed_speed = ["10","100","1000","auto"]',
        's = "999"',
        "if s not in allowed_speed:",
        '    s = "auto"',
        'print(f"speed {s}")',
    ])

    sh("11.2 duplex validieren")
    code([
        'allowed_duplex = ["auto","full","half"]',
        'd = "fast"',
        "if d not in allowed_duplex:",
        '    d = "auto"',
        'print(f"duplex {d}")',
    ])

    h("12) Port-Security (typisches Muster)")

    sh("12.1 Port-Security für mehrere Ports")
    code([
        "ports = [1,4,6]",
        "",
        'print("enable")',
        'print("conf t")',
        "",
        "for port in ports:",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport port-security")',
        '    print(" switchport port-security maximum 2")',
        '    print(" switchport port-security violation restrict")',
        '    print(" switchport port-security mac-address sticky")',
        '    print(" exit")',
        "",
        'print("end")',
    ])

    h("13) All-in-One Template (realistisch, nur Werte oben ändern)")

    sh("13.1 Komplett-Gerüst")
    code([
        "# --- DATEN (nur hier anpassen) ---",
        "access_ports = [1, 4, 6, 10, 11, 13]",
        "access_vlans = [10,10,20,20,10,10]",
        "trunk_ports  = [2, 3]",
        "",
        'router_ifaces = ["GigabitEthernet0/0", "GigabitEthernet0/1"]',
        'router_ips    = ["192.168.10.1",      "192.168.11.1"]',
        'router_masks  = ["255.255.255.0",     "255.255.255.0"]',
        "",
        "portsec_ports = [1, 4]",
        "",
        "# --- OUTPUT ---",
        'print("enable")',
        'print("conf t")',
        "",
        "# Access",
        "for i in range(len(access_ports)):",
        "    port = access_ports[i]",
        "    vlan = access_vlans[i]",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode access")',
        '    print(f" switchport access vlan {vlan}")',
        '    print(" exit")',
        "",
        "# Trunk",
        "for port in trunk_ports:",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport mode trunk")',
        '    print(" exit")',
        "",
        "# Router Interfaces (wenn gefordert)",
        "for i in range(len(router_ifaces)):",
        "    iface = router_ifaces[i]",
        "    ip    = router_ips[i]",
        "    mask  = router_masks[i]",
        '    print(f"interface {iface}")',
        '    print(f" ip address {ip} {mask}")',
        '    print(" no shutdown")',
        '    print(" exit")',
        "",
        "# Port-Security (wenn gefordert)",
        "for port in portsec_ports:",
        '    print(f"interface FastEthernet0/{port}")',
        '    print(" switchport port-security")',
        '    print(" switchport port-security maximum 2")',
        '    print(" switchport port-security violation restrict")',
        '    print(" switchport port-security mac-address sticky")',
        '    print(" exit")',
        "",
        'print("end")',
    ])

    h("14) Debug / Rettung (wenn Output komisch ist)")

    out("- Wenn Variablen nicht eingesetzt werden: fehlt das `f` vor dem String.")
    out('  Beispiel: falsch: "interface ... {port}"  | richtig: f"interface ... {port}"')
    out()
    out("- Wenn Einrückungen falsch sind: Python ist bei Einrückungen streng.")
    out("  Alles in der Schleife muss gleich eingerückt sein.")
    out()
    out("- Wenn Ports/VLANs falsch zugeordnet sind: Listenlängen prüfen.")
    out("  ports und vlans müssen gleich lang sein (bei Parallel-Listen).")
    out()

    h("15) Mini-Spickteil (wenn du nur 10 Zeilen behalten willst)")

    out("1) f-string:     f\"text {x}\"")
    out("2) Schleife:     for x in liste: print(f\"...{x}\")")
    out("3) Zwei Listen:  for i in range(len(A)): print(f\"{A[i]} {B[i]}\")")
    out("4) range:        for x in range(a,b+1): ...")
    out()
    out("ENDE.")

if __name__ == "__main__":
    main()
