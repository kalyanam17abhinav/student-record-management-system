from flask import Flask, render_template, url_for, request, redirect
import os, json

file = "student.json"

app = Flask(__name__)

def load_data():
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        return []
    with open(file, "r") as f:
        return json.load(f)


def write_data(new_id, new_name, new_dept, new_year, new_semester, sub_no, subjects):
    data = load_data()

    if any(str(s["id"]).upper() == str(new_id).upper() for s in data):
        print("ID already exists. Not adding student.")
        return "ID already exists", 400
    else:
        data.append({
            "id": new_id,
            "name": new_name,
            "dept": new_dept,
            "year": new_year,
            "semester": new_semester,
            "totalSubs": sub_no,
            "subjects": subjects
        })

    with open(file, "w") as f:
        json.dump(data, f, indent = 4)

def first_cap(s):
    return ' '.join(word[0].upper() + word[1:] for word in s.split())

def caps(s):
    return s.upper()

def get_grade(percentage):
    if percentage >= 90:
        return "O"
    elif percentage >= 80:
        return "A+"
    elif percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B+"
    elif percentage >= 50:
        return "B"
    elif percentage >= 40:
        return "C"
    else:
        return "F"

def get_result(grade):
    if grade == 'F':
        return "FAIL"
    else:
        return "PASS"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students")
def students():
    data = load_data()
    students = []

    for x in data:
        total = sum(x["subjects"].values())
        totalSubs = int(x["totalSubs"])
        # percentage = round((total / (totalSubs * 100)) * 100, 2)
        percentage = round(total / totalSubs, 2)
        grade = get_grade(percentage)
        result = get_result(grade)

        students.append({
            "id": caps(x["id"]),
            "name": first_cap(x["name"]),
            "dept": x["dept"],
            "year": x["year"],
            "semester": x["semester"],
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "result": result
        })
    return render_template("students.html", students = students)
    # return render_template("students.html")

@app.route("/add", methods=["GET"])
def add():
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def add_student():

    new_id = request.form["addIdInput"]
    new_name = request.form["addNameInput"]
    new_dept = request.form["dept"]
    new_year = request.form["year"]
    new_semester = request.form["semester"]
    sub_no = int(request.form["addSubNoInput"])

    new_id = new_id.strip()
    if not new_id:
        return "id cannot be empty", 400
    
    new_name = new_name.strip()
    if not new_name:
        return "name cannot be empty", 400
    
    subjects = {}
    seen = set()

    for i in range(1, sub_no + 1):
        sub = request.form.get(f"subject_{i}")
        mark = request.form.get(f"marks_{i}")
        # subs[sub] = int(mark)

        if not sub or not mark:
            return "please click + and enter all subject details", 400
        
        sub = sub.strip().lower()
        
        if sub in seen:
            return "duplicate subject names are not allowed", 400
        
        seen.add(sub)
        subjects[sub] = int(mark)

    result = write_data(new_id, new_name, new_dept, new_year, new_semester, sub_no, subjects)
    if result:
        return result
    return redirect(url_for("home"))

@app.route("/edit", methods=["GET"])
def edit_search():
    return render_template("edit_search.html")

@app.route("/edit/<sid>", methods=["GET"])
def edit_get(sid):

    data = load_data()
    sid = sid.replace(" ", "").upper()

    for s in data:
        if s["id"].upper() == sid:
            return render_template("edit.html", student = s)

    return "student not found", 404

@app.route("/edit/<sid>", methods=["POST"])
def edit_save(sid):
    data = load_data()

    for i, s in enumerate(data):
        if s["id"].upper() == sid.upper():

            name = request.form["name"].strip()
            dept = request.form["dept"]
            year = request.form["year"]
            semester = request.form["semester"]

            subjects = {}
            seen = set()

            idx = 1
            while True:
                sub = request.form.get(f"subject_{idx}")
                mark = request.form.get(f"marks_{idx}")
                if not sub or not mark:
                    break

                sub = sub.strip().lower()
                if sub in seen:
                    return "duplicate subject names", 400
                seen.add(sub)
                subjects[sub] = int(mark)
                idx += 1
            
            if not subjects:
                return "at least one subject required", 400
                # flash("at least one subject is required")
            
            s["name"] = name
            s["dept"] = dept
            s["year"] = year
            s["semester"] = semester
            s['subjects'] = subjects
            s["totalSubs"] = len(subjects)

            data[i] = s
            break
    else:
        return "student not found", 404
    with open(file, "w") as f:
        json.dump(data, f, indent = 4)

    return redirect(url_for("home"))

@app.route("/edit/<sid>/delete", methods=["POST"])
def delete_student(sid):
    data = load_data()

    new_data = [s for s in data if s["id"].upper() != sid.upper()]
    if len(new_data) == len(data):
        return "student not found", 404
    
    with open(file, "w") as f:
        json.dump(new_data, f, indent=4)
    
    return redirect(url_for("home", deleted=1))

@app.route("/edit", methods=["POST"])
def edit_post():
    data = load_data()
    ids = [s["id"].replace(" ","").upper() for s in data]
    
    new_id = request.form["id"].strip().replace(" ","").upper()
    
    if new_id in ids:
        return redirect(url_for("edit_get", sid = new_id))
    
    return render_template("edit_search.html", error="id not found")


@app.route("/search", methods=["GET"])
def search_get():
    return render_template("search_id.html")

@app.route("/search", methods=["POST"])
def search_post():
    data = load_data()
    ids = [s["id"].replace(" ","").upper() for s in data]

    new_id = request.form["id"].strip().replace(" ","").upper()

    # new_id = request.form.get("id", "").strip()
    if not new_id:
        return render_template("search_id.html", error="id cannot be empty")
    
    if new_id in ids:
        return redirect(url_for("search_show", sid = new_id))

    return render_template("search_id.html", error="id not found")

@app.route("/search/<sid>", methods=["GET"])
def search_show(sid):
    data = load_data()
    sid = sid.replace(" ", "").upper()

    for s in data:
        if s["id"].replace(" ","").upper() == sid:
            return render_template("search.html", student = s)

    return render_template("search_id.html", error="id not found")

if __name__ == "__main__":
    app.run(debug=True)