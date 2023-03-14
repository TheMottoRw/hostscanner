import datetime
import os
import re
import subprocess
import sys
import ipaddress

# IP_PATTERN = "[1-9][0-9]{1,2}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}"
import time

import requests as requests

IP_PATTERN = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
LINUX_IPINFO_REGEX = "inet 192.*.255"
WINDOWS_IP = f"IPv4 Address[. :]+ {IP_PATTERN}"
WINDOWS_SUBNET = f"Subnet Mask[. :]+ {IP_PATTERN}"
WINDOWS_GATEWAY = f"Default Gateway[. :]+ {IP_PATTERN}"
HOSTNAME_PATTERN = f"for [a-zA-Z0-9 -_@]+ \({IP_PATTERN}\)"
GATEWAY = {}


def scan_host():
    """ We use HOSTNAME_PATTERN to retrieve all device with hostname,Mobile phone can be detected with
     IP PATTERN But is not reliable because we can't track when ip changes without having their hostname"""
    found_host = []
    network_address, broadcast = get_network_address()
    # network address
    print(f"Network address {network_address}")
    if sys.platform == 'win32':  # windows does not display gateway hostname
        found_host.append(GATEWAY)
    out = subprocess.run(["nmap", network_address, "-sn"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).stdout.decode("UTF-8")
    # print(out)
    pattern_host_ip = re.compile(IP_PATTERN)
    patter_hostname = re.compile(HOSTNAME_PATTERN)
    if out is not None:
        found_ip = pattern_host_ip.findall(out)
        found_hostnames_ip = patter_hostname.findall(out)
        for host in found_hostnames_ip:
            hostname_ip = extract_hostname_and_ip(host)
            if hostname_ip is not None:
                found_host.append(hostname_ip)
        # get hostname of each ip addr
        # >>> socket.gethostbyaddr("192.168.1.11")
        print("Found hostname and ip")
        print(found_host)
        print("Found IP regardless of hostname")
        print(found_ip)
    else:
        print("Did not detect any host")
    return found_host


def get_network_address():
    os_name = sys.platform
    if os_name == 'linux':
        print("Linux operating system")
        out = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("UTF-8")
        # extract ip,broadcast and gateway
        pattern_ip = re.compile(LINUX_IPINFO_REGEX)
        ip_info = pattern_ip.findall(out)
        ip_arr = ip_info[0].split(" ")
        ip = ip_arr[1]
        netmask = ip_arr[4]
        broadcast = ip_arr[7]
        print(f"Broadcast ip {broadcast}")
        network_address = str(ipaddress.ip_network(f"{ip}/{netmask}", strict=False))
        return str(network_address), broadcast
    else:
        print("Other operating system like Windows")
        out = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("UTF-8")
        pattern_ip = re.compile(WINDOWS_IP)
        ip_patt = re.compile(IP_PATTERN)
        pattern_subnet = re.compile(WINDOWS_SUBNET)
        pattern_gateway = re.compile(WINDOWS_GATEWAY)
        ip_arr = pattern_ip.findall(out)
        ip = ip_patt.findall(ip_arr[len(ip_arr) - 1])[0]
        print(f"ip is {ip}")
        subnet_arr = pattern_subnet.findall(out)
        subnet = ip_patt.findall(subnet_arr[len(subnet_arr) - 1])[0]
        print(f"Subnet  mask is {subnet}")
        gateway_arr = pattern_gateway.findall(out)
        print(f"Gateway array {gateway_arr}")
        gateway = ip_patt.findall(gateway_arr[len(gateway_arr) - 1])[0]
        GATEWAY['_gateway'] = gateway
        print(f"Gateway is {gateway}")
        network_obj = ipaddress.ip_network(f"{ip}/{subnet}", False)
        network_address = str(ipaddress.ip_network(f"{ip}/{subnet}", False))
        broadcast = str(network_obj.broadcast_address)
        return network_address, broadcast


def extract_hostname_and_ip(hostname_and_ip):
    hostnames_ip = dict()
    host_array = hostname_and_ip.split(" ")
    if len(host_array) > 2:
        hostname = host_array[1]
        ip_regex = re.compile(IP_PATTERN)
        ip = ip_regex.findall(host_array[2])
        hostnames_ip[hostname] = ip[0]
    else:
        print("Data not matching the pattern")
        print(hostname_and_ip)
    return hostnames_ip


def save_scanned_hosts(host_list):
    for host_obj in host_list:
        for key in host_obj:
            # ScannedHosts.save(key, host_obj[key])
            r = requests.post("http://localhost:5000/api/hosts", data={"hostname": key, "ip": host_obj[key]})
            print("Response from api")
            print(r.text)


def save_scanned_hosts_array(host_list):
    r = requests.post("http://localhost:5000/api/hosts_array", json={"data": host_list})
    print("Response from api")
    print(r.text)


def angry_scan_host():
    """ We use HOSTNAME_PATTERN to retrieve all device with hostname,Mobile phone can be detected with
     IP PATTERN But is not reliable because we can't track when ip changes without having their hostname"""
    filename = os.getcwd() + "/ip.txt"
    found_host = []
    network_address, broadcast = get_network_address()
    start_ip = network_address.split("/")[0]
    # network address
    try:

        subprocess.run(["ipscan", "-sq", "-f:range", start_ip, broadcast, "-o", filename],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT).stdout.decode("UTF-8")
        found_host = read_ip_file(filename)
    except Exception as e:
        print(repr(e))

    return found_host


def read_ip_file(file="/home/asua/ip.txt"):
    data = []
    with open(file) as f:
        lines = f.readlines()
        lines = lines[7:]
        temp = []
        print(lines[174])
        for line in lines:
            if not line.__contains__("ms"):
                temp.append("ms")
                # print("Not contains ms")
                continue
            lin = list(filter(None, line.split("  ")))
            if not lin[2].__contains__("[n/a]"):
                # li = [i for i in lin if i != ""]
                data.append({lin[2].strip(): lin[0].strip()})

    return data


if __name__ == '__main__':
    # scan every 15 minutes
    print(f"Started scan every 15 minutes from {datetime.datetime.now()}")
    # print(angry_scan_host())
    # quit()
    while True:
        data = {}
        print(f"Rescan at {datetime.datetime.now()}")
        # hosts = scan_host()
        hosts = angry_scan_host()
        print("Scan complete,saving data...")
        print(hosts)


        # save scanned hosts
        # hosts = ['ASUA-TECRA-Z50-A']
        # save_scanned_hosts(hosts)
        save_scanned_hosts_array(hosts)
        time.sleep(15)
    print(f"Scan stopped at {datetime.datetime.now()}")
