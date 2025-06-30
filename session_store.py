sessions = {}

def get_session(user_id):
    return sessions.setdefault(user_id, {"fase": "esperando_datos", "datos": {}})

def reset_session(user_id):
    sessions[user_id] = {"fase": "esperando_datos", "datos": {}}
