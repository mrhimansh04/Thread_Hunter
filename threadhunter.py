import socket
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from tqdm import tqdm

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(Fore.RED + r"""
████████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ 
╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗
   ██║   ███████║██████╔╝█████╗  ███████║██║  ██║
   ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══██║██║  ██║
   ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝
""")
    print(Fore.GREEN + "        ⚡ THREAD HUNTER ⚡")
    print(Fore.CYAN + "        Multi-Threaded Port Scanner\n")

def loading():
    print(Fore.MAGENTA + "[+] Initializing Thread Engine", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print("\n")

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None

def start_scan(target, start_port, end_port, threads=100):
    open_ports = []
    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, target, port) for port in ports]

        for future in tqdm(as_completed(futures),
                           total=len(futures),
                           desc="Scanning",
                           colour="green"):
            result = future.result()
            if result:
                open_ports.append(result)

    return open_ports

def main():
    clear()
    banner()
    time.sleep(2)
    loading()

    target = input(Fore.YELLOW + "[+] Enter Target IP: ")
    start_port = int(input(Fore.YELLOW + "[+] Start Port: "))
    end_port = int(input(Fore.YELLOW + "[+] End Port: "))

    print(Fore.MAGENTA + "\n[+] Starting Scan...\n")

    results = start_scan(target, start_port, end_port)

    print(Fore.GREEN + "\n[+] Scan Completed!\n")

    if results:
        for port in results:
            print(Fore.CYAN + f"[OPEN] Port {port}")
    else:
        print(Fore.RED + "No open ports found.")

if __name__ == "__main__":
    main()