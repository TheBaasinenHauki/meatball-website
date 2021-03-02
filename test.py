import json

user_id_file = {}

with open('users_id.json', 'w') as f:
    pass
    
with open('users.json', 'r') as p:
    users = json.load(p)

for user in users:
    user_id_file[f"{user}"] = {}
    user_id_file[f"{user}"]['experience'] = users[f"{user}"]['experience']
    user_id_file[f"{user}"]['level'] = users[f"{user}"]['level']
    user_id_file[f"{user}"]['messages'] = users[f"{user}"]['messages']

with open('users_id.json', 'w') as f:
    json.dump(user_id_file, f)

print(user_id_file)
