from flask import Flask, render_template, request

from .handle import handle_message, handle_callback

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        update = request.json
        if update is None:
            return "ok"
        if "message" in update:
            handle_message(update)
        elif "callback_query" in update:
            handle_callback(update)
        return "ok"
    return render_template("status.html")


handler = app
