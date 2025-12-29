new_name = request.form.get("addNameInput", "").strip()
    if not new_name:
        return "student name cannot be empty", 400