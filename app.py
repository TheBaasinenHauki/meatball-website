from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/a")
def a():
    return render_template("a.html")

if __name__ == "__main__":
    app.run()