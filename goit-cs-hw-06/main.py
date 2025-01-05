from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
from flask_sock import Sock
import socket
import threading
import json
from datetime import datetime
from pymongo import MongoClient, errors

# setup MongoDB
try:
    client = MongoClient("mongodb://mongodb:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # check connection
    db = client["messages_db"]
    collection = db["messages"]
except errors.ServerSelectionTimeoutError:
    print("ERROR: Can't connect to MongoDB.")
except Exception as e:
    print(f"OOPss! Something goes wrong: {e}")

# Flask HTTP-server
app = Flask(__name__)
sock = Sock(app)

# routing
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        # get data grom form
        username = request.form["username"]
        message = request.form["message"]

        # send to Socket-server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            data = {"username": username, "message": message}
            s.sendto(json.dumps(data).encode(), ("127.0.0.1", 5000))

        return redirect(url_for("index"))
    return render_template("message.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

# Socket-server
def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 5000))
        print("Socket-server run on port 5000...")
        while True:
            data, _ = s.recvfrom(1024)
            message = json.loads(data.decode())
            message["date"] = datetime.now().isoformat()
            collection.insert_one(message)
            print("Message saved to db:", message)

# run servers
if __name__ == "__main__":
    # run Socket-server in separate thread
    threading.Thread(target=socket_server, daemon=True).start()

    # run Flask HTTP-server
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)
