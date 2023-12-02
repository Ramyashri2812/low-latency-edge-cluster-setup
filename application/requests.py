#A python script which creates specified number of requests (1000 in this case) to the health monitoring application running on the cluster
import requests
import time
import random
import math
import matplotlib.pyplot as plt

def poisson_distribution(lmbda):
    return -math.log(1.0 - random.random()) / lmbda

base_url = "http://192.168.21.81:30123/Wendy_Schwartz"

lambda_param = 1

num_requests = 1000

timestamps = []
request_counts = []

for i in range(num_requests):
    timestamp = time.time()
    timestamps.append(timestamp)

    delay = poisson_distribution(lambda_param)
    time.sleep(delay)

    try:
        response = requests.get(base_url)
        print(f"Request {i + 1}: {response.status_code}")
    except Exception as e:
        print(f"Request {i + 1}: Error - {e}")

    request_counts.append(i + 1)

print("Testing complete.")

plt.plot(timestamps, request_counts, marker='o')
plt.title('Number of Requests Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of Requests')
plt.show()
