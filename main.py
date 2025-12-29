import json, os

file = "student.json"

def load_data():
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return []
    with open(file, "r") as f:
        return json.load(f)

data = load_data()

def view_data():
    for x in data:
        print("id : ", x["id"], " - ", x["name"], " - ", x["dept"])
        print("total : ", sum(x["subjects"].values()))

new_name = input("enter the name: ")
new_id = int(input("enter the id: "))
new_dept = input("enter the dept: ")
new_year = int(input("enter the year: "))

sub_no = int(input("enter the no. of subjects: "))

subjects = {}
for _ in range(sub_no):
    sub = input("enter subject name: ")
    mark = int(input("enter the marks: "))
    subjects[sub] = int(mark)

if any(s["id"] == new_id for s in data):
    print("ID already exists. Not adding student.")
else:
    data.append({
        "id": new_id,
        "name": new_name,
        "dept": new_dept,
        "year": new_year,
        "totalSubs": sub_no,
        "subjects": subjects
    })

# view_data()

def write_data():
    with open(file, "w") as f:
        json.dump(data, f, indent = 4)

write_data()
view_data()