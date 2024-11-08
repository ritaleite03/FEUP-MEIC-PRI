import json
import re

def load_json(file_name):
    f = open(file_name, "r", encoding="UTF-8")
    return json.load(f)

if __name__ == "__main__":
    data = load_json("../../wikidata/New/wikipedia_complete.json")
    print(len(data))

