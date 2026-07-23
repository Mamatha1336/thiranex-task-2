from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("taskmanager.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home
@app.route("/")
def home():
    return redirect("/login")

# Register
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")

        except:
            return "Username already exists"

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template("dashboard.html", tasks=tasks)

# Add Task
@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]

    conn = get_db()

    conn.execute(
        "INSERT INTO tasks(title,status,user_id) VALUES(?,?,?)",
        (title,"Pending",session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# Complete Task
@app.route("/complete/<int:id>")
def complete_task(id):

    conn = get_db()

    conn.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# Delete Task
@app.route("/delete/<int:id>")
def delete_task(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
