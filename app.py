from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/entry/*")
def get_entry(entry_name):
    return "<p> This is a placeholder for the logic </p>"