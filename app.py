from flask import Flask, render_template
import json
from jinja2 import Template
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import ast

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():

    with open('users_id.json', 'w') as k:
        pass

    save_data_drive = drive.CreateFile({'id': '13zDkqN5uhG0_jaoqCC_csZKjTnX6EX15'})
    save_data = save_data_drive.GetContentString()
    save_dict = ast.literal_eval(save_data)

    with open('users_id.json', 'w') as k:
        json.dump(save_dict, k)

    with open('users_id.json', 'r') as p:
        users = json.load(p)

    s = "{% for user, level in dict_item.items() %}{{user}} {{level}} \n{% endfor %}"

    template = Template(s)
    content = template.render(dict_item = users)
    print(content)
    return render_template("leaderboard.html", user_data = content)

if __name__ == "__main__":
    app.run()
