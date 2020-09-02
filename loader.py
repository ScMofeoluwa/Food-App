import json
def load_db():
    with open("foods.json",'rb') as f:
        return json.load(f)

foods = load_db()

