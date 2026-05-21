from flask import Flask, render_template, request
import os

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
