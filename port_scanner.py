import socket
import sys
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-alt",
}


def check_port(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except Exception:
        return port, False


def scan(host):
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(lambda p: check_port(host, p), COMMON_PORTS))
    return [p for p, ok in results if ok]


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    print("Scanning", host, "(only scan devices you own or have permission to test)")
    open_ports = scan(host)
    if not open_ports:
        print("No common ports are open.")
    for p in open_ports:
        print("OPEN:", p, COMMON_PORTS[p])
