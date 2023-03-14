import psutil
import time

NETWORK_INTERFACE = 'wlp2s0'
NETWORK_LIMIT = 5000000  # 5GB in SI standard

while True:
    netio = psutil.net_io_counters(pernic=True)
    sent = netio[NETWORK_INTERFACE].bytes_sent
    recv = netio[NETWORK_INTERFACE].bytes_recv
    net_usage = sent + recv

    if net_usage > NETWORK_LIMIT:
        print("Meets network limit!")

    print("Sent bytes ",sent/(1024*1024), "MB Received ",recv/(1024*1024)," MB")
    time.sleep(15)
