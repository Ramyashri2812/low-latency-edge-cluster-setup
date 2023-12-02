import subprocess
import json
import random

USED_NODE_FILE = 'used_node.json'

try:
    with open(USED_NODE_FILE, 'r') as file:
        used_node = json.load(file)
except FileNotFoundError:
    used_node = {'192.168.21.240': 0, '192.168.21.129': 0, '192.168.21.20': 0}

def save_used_node():
    with open(USED_NODE_FILE, 'w') as file:
        json.dump(used_node, file)

def choose_random_node(target_ips):
    available_nodes = [ip for ip in target_ips if used_node[ip] == 0]
    
    if not available_nodes:
        print("All nodes have been untainted.")
        return None

    return random.choice(available_nodes)

if __name__ == "__main__":
    target_ips = ['192.168.21.240', '192.168.21.129', '192.168.21.20']

    chosen_node = choose_random_node(target_ips)

    if chosen_node:
        used_node[chosen_node] = 1

        if chosen_node == '192.168.21.240':
            name = 'sujitha-virtual-machine'
        elif chosen_node == '192.168.21.129':
            name = 'ubuntulinux'
        elif chosen_node == '192.168.21.20':
            name = 'cantcode-virtualbox'
        
        try:
            print(f"A random node, {name}, has been chosen!")
            subprocess.run(['kubectl', 'taint', 'node', name, 'key1-']) //untaints the chosen node

            save_used_node()

        except Exception as e:
            print(f"Error during kubectl taint command: {e}")
    else:
        print("No valid nodes.")
