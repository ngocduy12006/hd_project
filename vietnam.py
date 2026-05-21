from flask import Flask, render_template, request, session, redirect, url_for
import os
from functools import wraps
from hmac import compare_digest

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

destinations = [
    {
        "id": "ha-long-bay",
        "name": "Ha Long Bay",
        "description": "Explore stunning limestone karsts and emerald waters on a traditional junk boat cruise.",
        "image": "https://images.unsplash.com/photo-1668000018482-a02acf02b22a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYWxvbmclMjBiYXklMjB2aWV0bmFtfGVufDF8fHx8MTc3OTI1NDgyOXww&ixlib=rb-4.1.0&q=80&w=1080",
        "duration": "2-3 Days"
    },
    {
        "id": "hoi-an",
        "name": "Hoi An",
        "description": "Wander through colorful lantern-lit streets in this charming ancient trading port.",
        "image": "https://images.unsplash.com/photo-1569271532956-3fb81a207115?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwyfHxob2klMjBhbiUyMHZpZXRuYW18ZW58MXx8fHwxNzc5MjU0ODI5fDA&ixlib=rb-4.1.0&q=80&w=1080",
        "duration": "2-4 Days"
    },
    {
        "id": "hanoi",
        "name": "Hanoi",
        "description": "Experience Vietnam's vibrant capital with its rich history, street food, and culture.",
        "image": "https://images.unsplash.com/photo-1533497394934-b33cd9695ba9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwyfHxoYW5vaSUyMHZpZXRuYW18ZW58MXx8fHwxNzc5MjU0ODMwfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "duration": "3-5 Days"
    },
    {
        "id": "ho-chi-minh-city",
        "name": "Ho Chi Minh City",
        "description": "Discover the bustling metropolis blending modern life with historical landmarks.",
        "image": "https://images.unsplash.com/photo-1583417319070-4a69db38a482?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxobyUyMGNoaSUyMG1pbmglMjBjaXR5JTIwdmlldG5hbXxlbnwxfHx8fDE3NzkyNTQ4MzB8MA&ixlib=rb-4.1.0&q=80&w=1080",
        "duration": "2-4 Days"
    }
]


def check_login(username, password):
    expected_username = os.getenv("ADMIN_USERNAME")
    expected_password = os.getenv("ADMIN_PASSWORD")

    if not expected_username or not expected_password:
        return False

    return (
        compare_digest(username, expected_username)
        and compare_digest(password, expected_password)
    )


def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    search = request.args.get("search", "").lower()
    duration = request.args.get("duration", "")

    filtered_destinations = destinations

    if search:
        filtered_destinations = [
            destination for destination in filtered_destinations
            if search in destination["name"].lower()
            or search in destination["description"].lower()
        ]

    if duration:
        filtered_destinations = [
            destination for destination in filtered_destinations
            if destination["duration"] == duration
        ]

    durations = sorted(set(destination["duration"] for destination in destinations))

    return render_template(
        "home.html",
        destinations=filtered_destinations,
        durations=durations,
        search=search,
        selected_duration=duration
    )


@app.route("/destination/<destination_id>")
def destination_detail(destination_id):
    selected_destination = None
    for destination in destinations:
        if destination["id"] == destination_id:
            selected_destination = destination
            break
    return render_template("destination.html", destination=selected_destination)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if check_login(username, password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("admin"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html", destinations=destinations)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG") == "1"
    )


