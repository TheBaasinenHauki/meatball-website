from flask import Flask, render_template
import json
from jinja2 import Template

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    with open('users_id.json', 'r') as p:
        users = json.load(p)

    s = "{% for user, level in dict_item.items() %}{{user}} {{level}} \n{% endfor %}"

    template = Template(s)
    content = template.render(dict_item = users)
    print(content)
    return render_template("leaderboard.html", user_data = content)

if __name__ == "__main__":
    app.run()
