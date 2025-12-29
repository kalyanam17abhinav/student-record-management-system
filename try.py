# print("hello world")

import json, os

def read_data():
    if os.path.getsize("try.json") == 0:
        return {}
    with open("try.json", "r") as f:
        return json.load(f)

dataR = read_data()

print(dataR["student"]["subjects"]["python"])
print(dataR["age"])

dataR["name"] = "kalyanam"

with open("try.json", "w") as f:
    json.dump(dataR, f, indent=4)

print(read_data())