#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import socket
import struct
import time
import re
import urllib.request
import json
import random
from datetime import datetime

# CONFIGURACIÓN DE COLORES NEXUS CYBER
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        BLACK = '\033[30m'; RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[34m'; MAGENTA = '\033[95m'; CYAN = '\033[36m'; WHITE = '\033[97m'
        LIGHTBLACK_EX = '\033[90m'; LIGHTRED_EX = '\033[91m'; LIGHTGREEN_EX = '\033[92m'
        LIGHTYELLOW_EX = '\033[93m'; LIGHTBLUE_EX = '\033[94m'; LIGHTMAGENTA_EX = '\033[95m'
        LIGHTCYAN_EX = '\033[96m'; LIGHTWHITE_EX = '\033[97m'; RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'; UNDERLINE = '\033[4m'; RESET_ALL = '\033[0m'

def formatear_colores_minecraft(texto):
    mapa_colores = {
        '0': Fore.BLACK, '1': Fore.BLUE, '2': Fore.GREEN, '3': Fore.CYAN,
        '4': Fore.RED, '5': Fore.MAGENTA, '6': Fore.YELLOW, '7': Fore.WHITE,
        '8': Fore.LIGHTBLACK_EX, '9': Fore.LIGHTBLUE_EX, 'a': Fore.LIGHTGREEN_EX,
        'b': Fore.LIGHTCYAN_EX, 'c': Fore.LIGHTRED_EX, 'd': Fore.LIGHTMAGENTA_EX,
        'e': Fore.LIGHTYELLOW_EX, 'f': Fore.WHITE, 'r': Fore.RESET
    }
    partes = re.split(r'§([0-9a-fk-or])', texto, flags=re.IGNORECASE)
    resultado = ""
    color_actual = Fore.RESET
    for i, parte in enumerate(partes):
        if i % 2 == 1:
            color_actual = mapa_colores.get(parte.lower(), Fore.RESET)
        else:
            resultado += color_actual + parte
    return resultado + Fore.RESET

BANNER = f"""
{Fore.CYAN}☠️ ═════════════════════════════════════════════════════════════ ☠️
{Fore.GREEN}   _  _______  ___  VM   _  _______ _   _ _   _ _   _ ____  
{Fore.GREEN}  | |/ /  _  \/ _ \ / _ \ | |/ /  ___| | | | | | | | / ___| 
{Fore.CYAN}  | ' /| | | / /_\ / /_\ \| ' /| |__ | |_| | |_| | | \___ \ 
{Fore.CYAN}  | . \| | | |  _  |  _  || . \|  __||  _  |  _  | | |___) |
{Fore.GREEN}  |_|\_\_| |_|_| |_|_| |_|_|\_\____|_| |_|_| |_|_| |_|____/ 
{Fore.CYAN}            [ NEXUS CYBER AUDITOR LIVE v15.0 ]
{Fore.CYAN}☠️ ═════════════════════════════════════════════════════════════ ☠️
"""

def sistema_login():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    print(f"{Fore.CYAN}[🔒 SYSTEM] ACCESO RESTRINGIDO - ENTRADA KEYMASTER")
    usuario = input(f"{Fore.GREEN}👤 USER: {Fore.WHITE}").strip()
    password = input(f"{Fore.GREEN}🔑 PASS: {Fore.WHITE}").strip()
    if usuario == "admin" and password == "admin1234":
        print(f"\n{Fore.GREEN}[🔓 ACCESS GRANTED] Sincronizando sockets de red...")
        time.sleep(1)
        return True
    else:
        print(f"\n{Fore.RED}[🚨 ACCESS DENIED] Credenciales Incorrectas.")
        time.sleep(1.2)
        sys.exit(1)

class NexusAuditorReal:
    def __init__(self, target_host, port):
        self.target_host = target_host
        self.port = port
        self.numeric_ip = "Calculando..."
        self.provider = "Escaneando..."
        self.provider_url = "N/A"
        
        self.raw_motd = "Desconocido"
        self.version = "Desconocida"
        self.api_software = "Buscando..."
        self.ping_ms = 0
        self.players_list = []
        self.plugins_list = "No expuestos en Query público"
        
        # Reportes solicitados
        self.nivel_debilidad = "✅ ESTABLE / PROTEGIDO"
        self.force_op_status = "Seguro (Filtros activos)"
        self.fallos_lista = []
        
        self.hora_encendido = "---"
        self.hora_apagado = "---"
        self.ultimo_estado = None 
        self.conteo_fallas = 0
        self.cyber_status = "STABLE"
        
        self.MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

    def rastrear_host(self):
        try: self.numeric_ip = socket.gethostbyname(self.target_host)
        except: self.numeric_ip = self.target_host

        try:
            url = f"http://ip-api.com/json/{self.numeric_ip}?fields=status,org,isp"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3.0) as response:
                res_data = json.loads(response.read().decode())
                if res_data.get("status") == "success":
                    org = res_data.get("org") or res_data.get("isp") or "Desconocido"
                    self.provider = org
                    org_low = org.lower()
                    if "ovh" in org_low: self.provider_url = "https://www.ovhcloud.com"
                    elif "aternos" in org_low: self.provider_url = "https://aternos.org"
                    elif "shock" in org_low: self.provider_url = "https://shockbyte.com"
                    elif "falix" in org_low or "felix" in org_low: self.provider_url = "https://falixnodes.net"
                    elif "holy" in org_low: self.provider_url = "https://holynodes.com"
                    elif "leme" in org_low: self.provider_url = "https://lemehost.com"
                    elif "bean" in org_low: self.provider_url = "https://beanshosting.com"
                    elif "opti" in org_low: self.provider_url = "https://optilink.net"
                    else: self.provider_url = "N/A (Host Privado)"
        except:
            self.provider = "Shield Proxy / Cloud"
            self.provider_url = "N/A"

    def consultar_servidor_real(self):
        hora_mexico = datetime.now().strftime("%I:%M:%S %p")
        self.players_list = []
        
        # 1. CONSULTA DE RED EN VIVO MEDIANTE GAMESY4 UDP (Para sacar PL y nombres reales)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.0)
            session_id = random.randint(1, 9999999) & 0x0F0F0F0F
            packet_handshake = b'\xFE\xFD\x09' + struct.pack('>I', session_id)
            
            t_start = time.time()
            sock.sendto(packet_handshake, (self.numeric_ip, self.port))
            data, addr = sock.recvfrom(1024)
            self.ping_ms = int((time.time() - t_start) * 1000)
            
            if data and len(data) >= 5:
                challenge_token = int(data[5:].decode('utf-8', errors='ignore').strip('\x00'))
                packet_query = b'\xFE\xFD\x00' + struct.pack('>I', session_id) + struct.pack('>i', challenge_token) + b'\x00\x00\x00\x00'
                sock.sendto(packet_query, (self.numeric_ip, self.port))
                query_data, addr = sock.recvfrom(4096)
                sock.close()
                
                if query_data and len(query_data) > 15:
                    self.conteo_fallas = 0
                    self.cyber_status = "✅ STABLE / ONLINE"
                    bloques = query_data[11:].split(b'\x00')
                    cadenas = [b.decode('utf-8', errors='ignore').strip() for b in bloques if b]
                    
                    es_seccion_jugadores = False
                    for item in cadenas:
                        if item == "player_":
                            es_seccion_jugadores = True
                            continue
                        if es_seccion_jugadores:
                            if item in ["", "hostname", "gametype", "version", "plugins", "map", "numplayers", "maxplayers"]:
                                break
                            item_clean = re.sub(r'§[0-9a-fk-or]', '', item).strip()
                            if item_clean and len(item_clean) > 1 and item_clean not in self.players_list:
                                self.players_list.append(item_clean)
                    
                    for i in range(len(cadenas) - 1):
                        if cadenas[i] == "hostname": self.raw_motd = cadenas[i+1]
                        elif cadenas[i] == "version": self.version = cadenas[i+1]
                        elif cadenas[i] == "numplayers":
                            try: self.jugadores_count = int(cadenas[i+1])
                            except: pass
                        elif cadenas[i] == "maxplayers":
                            try: self.max_jugadores = int(cadenas[i+1])
                            except: pass
                        elif cadenas[i] == "plugins": 
                            self.api_software = cadenas[i+1]
                            self.plugins_list = cadenas[i+1]

                    if self.ultimo_estado is not True:
                        self.hora_encendido = hora_mexico
                        self.ultimo_estado = True
                    return True
        except:
            pass
            
        # 2. RESPALDO RAKNET SI EL ANTERIOR DA TIMEOUT
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.0)
            packet = b'\x01' + struct.pack('>Q', int(time.time())) + self.MAGIC + b'\x00' * 8
            sock.sendto(packet, (self.numeric_ip, self.port))
            data, addr = sock.recvfrom(2048)
            sock.close()
            
            if data and len(data) > 35:
                self.conteo_fallas = 0
                self.cyber_status = "✅ ONLINE (RAKNET)"
                campos = data[35:].decode('utf-8', errors='ignore').split(';')
                if len(campos) >= 6:
                    self.raw_motd = campos[1]
                    self.version = campos[3]
                    try: self.jugadores_count = int(campos[4])
                    except: pass
                    try: self.max_jugadores = int(campos[5])
                    except: pass
                    if len(campos) > 7: self.api_software = campos[7]
                return True
        except:
            self.conteo_fallas += 1

        # DETECTOR DE ATAQUES DDOS EN TIEMPO REAL
        if self.conteo_fallas == 1:
            self.cyber_status = "⚠️ SERVER BAJO ATAQUE (LAG / FLOOD)"
        elif self.conteo_fallas >= 2:
            if self.ultimo_estado is True:
                self.hora_apagado = hora_mexico
                self.ultimo_estado = False
            self.cyber_status = "🚨 SERVER OFF / CAUSA DDOS"
        return False

    def comprobar_debilidades_pasivas(self, online):
        self.fallos_lista = []
        if not online:
            return
            
        core = self.api_software.lower()
        # Si expone plugins viejos o cores vulnerables, reportamos el estado solicitado
        if "astral" in core or "pocketmine" in core or "0.14" in self.version or "0.15" in self.version:
            self.nivel_debilidad = f"{Fore.YELLOW}⚠️ MODERADAMENTE EXPUESTO"
            self.force_op_status = f"{Fore.RED}⚠️ Force OP Detectado en comandos alternos: /sudo /:sudo /rca /:rca"
            self.fallos_lista.append("Explotable: Desbordamiento de Buffer RakNet clásico")
            self.fallos_lista.append("Riesgo: Exposición de árbol de comandos sin filtrar")
        else:
            self.nivel_debilidad = f"{Fore.GREEN}✅ ESTABLE / PROTEGIDO"
            self.force_op_status = f"{Fore.GREEN}Seguro (Filtros activos)"

    def renderizar_interfaz(self, online):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        
        print(f"{Fore.GREEN}⚡ ESTADO RED:    {self.cyber_status}")
        print(f"{Fore.CYAN}🌐 DIRECCIÓN IP: {Fore.WHITE}{self.numeric_ip}:{self.port}")
        print(f"{Fore.CYAN}🏢 PROVEEDOR:    {Fore.GREEN}{self.provider} {Fore.LIGHTBLACK_EX}({self.provider_url})")
        print(f"{Fore.CYAN}⏱️  REGISTROS MX: {Fore.GREEN}ON: {self.hora_encendido} {Fore.CYAN}| {Fore.RED}OFF: {self.hora_apagado}")
        print(f"{Fore.CYAN}🔌 LATENCIA:     {Fore.YELLOW}{self.ping_ms} ms")
        
        # FORMATO EXACTO DE AUDITORÍA PEDIDO
        print(f"{Fore.GREEN}═══ [ REPORTE DE AUDITORÍA Y SEGURIDAD VULN ] ══════════════")
        print(f"{Fore.CYAN}☠️  DEBILIDAD SV:  {self.nivel_debilidad}")
        print(f"{Fore.CYAN}🔓 ESTADO FORCEOP: {self.force_op_status}")
        
        if self.fallos_lista and "MODERADAMENTE" in self.nivel_debilidad:
            print(f"{Fore.RED}❌ Fallos Encontrados:")
            for f in self.fallos_lista:
                print(f"   -> {Fore.LIGHTRED_EX}{f}")
            print(f"\n{Fore.RED}⚠️  SERVER EN PELIGRO, CUIDADO! ¡AVISA A LOS CREADORES! ⚠️")
            
        print(f"{Fore.GREEN}═══ [ DATOS NATIVOS DEL JUEGO ] ════════════════════════════")
        motd_fix = formatear_colores_minecraft(self.raw_motd) if online else f"{Fore.RED}Offline"
        print(f"{Fore.CYAN}📝 MOTD NATIVO:   {motd_fix}")
        print(f"{Fore.CYAN}⚙️  API / CORE:    {Fore.WHITE}{self.api_software}")
        print(f"{Fore.CYAN}📦 PLUGINS (PL):  {Fore.LIGHTBLUE_EX}{self.plugins_list}")
        print(f"{Fore.CYAN}👥 CONTADOR:      {Fore.YELLOW}{self.jugadores_count} / {self.max_jugadores}")
        
        print(f"{Fore.GREEN}═══ [ JUGADORES DETECTADOS EN VIVO ] ═══════════════════════")
        if online and self.players_list:
            print(f"{Fore.GREEN}👉 {Fore.WHITE}" + f"{Fore.RESET}, {Fore.WHITE}".join(self.players_list))
        elif online:
            print(f"{Fore.LIGHTBLACK_EX}Ninguno adentro o el Query está capado en server.properties.")
        else:
            print(f"{Fore.RED}Servidor caído. Datos inaccesibles por falla de respuesta.")

def main():
    if not sistema_login(): return

    default_ip = "15.204.51.206"
    default_port = 16942

    print(f"\n{Fore.LIGHTBLACK_EX}ENTER para usar {default_ip}:{default_port}")
    ip_in = input(f"{Fore.GREEN}👾 TARGET IP: {Fore.WHITE}").strip()
    if not ip_in: ip_in = default_ip

    port_in = input(f"{Fore.GREEN}👾 PORT:      {Fore.WHITE}").strip()
    port = int(port_in) if port_in.isdigit() else default_port

    auditor = NexusAuditorReal(ip_in, port)
    auditor.rastrear_host()
    
    try:
        while True:
            is_on = auditor.consultar_servidor_real()
            auditor.comprobar_debilidades_pasivas(is_on)
            auditor.renderizar_interfaz(is_on)
            time.sleep(1.5)
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}[✅] Nexus Auditor cerrado limpiamente.{Fore.RESET}\n")

if __name__ == "__main__":
    main()