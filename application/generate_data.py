import json
import random
from faker import Faker

fake = Faker()
def generate_random_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "date": fake.date_this_decade(),
            "time": fake.time(),
            "heart_rate": random.randint(60, 100)
        }
        data.append(record)
    return data

random_data = generate_random_data(10)

json_data = json.dumps(random_data, default=str)

print(json_data)
