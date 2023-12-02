import subprocess
import re
import json

USED_NODE_FILE = 'used_node.json'

try:
    with open(USED_NODE_FILE, 'r') as file:
        used_node = json.load(file)
except FileNotFoundError:
    used_node = {'192.168.21.240': 0, '192.168.21.129': 0, '192.168.21.20': 0}

def save_used_node():
    with open(USED_NODE_FILE, 'w') as file:
        json.dump(used_node, file)

def calculate_rtt(source_ip, target_ips):
    rtt_results = {}

    for target_ip in target_ips:
        try:
            if used_node[target_ip] == 0:
                result = subprocess.run(['ping', '-c', '4', '-i', '0.2', target_ip],
                                        capture_output=True, text=True, check=True)
                rtt_match = re.search(r"min/avg/max/mdev = (.+?)\/", result.stdout)
                if rtt_match:
                    rtt = float(rtt_match.group(1))
                    rtt_results[target_ip] = rtt
                else:
                    rtt_results[target_ip] = float('inf')
        except subprocess.CalledProcessError:
            print(f"Error pinging {target_ip}")

    return rtt_results

if __name__ == "__main__":
    source_ip = '192.168.21.81'
    target_ips = ['192.168.21.240', '192.168.21.129', '192.168.21.20']

    rtt_results = calculate_rtt(source_ip, target_ips)

    if rtt_results:
        min_rtt_ip = min(rtt_results, key=rtt_results.get)
        used_node[min_rtt_ip] = 1
        if min_rtt_ip == '192.168.21.240':
            name = 'sujitha-virtual-machine'
        elif min_rtt_ip == '192.168.21.129':
            name = 'ubuntulinux'
        elif min_rtt_ip == '192.168.21.20':
            name = 'cantcode-virtualbox'
        
        try:
            subprocess.run(['kubectl', 'taint', 'node', name, 'key1-']) #untaints the node with minimal latency
            subprocess.run(['kubectl', 'create', '-f', 'health_app.yaml']) #creates an instance of the application of untainted node

            save_used_node()

        except Exception as e:
            print(f"Error during kubectl taint command: {e}")
    else:
        print("No valid RTT results.")
