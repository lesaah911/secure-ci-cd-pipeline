import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Pipeline sécurisé opérationnel"

@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    return os.popen(f"ping -c 1 {host}").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)