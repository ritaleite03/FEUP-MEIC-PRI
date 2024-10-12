from utils import *

def merge(f1_content, f2_content):
    for disease,information in f2_content.items():

        if disease not in f1_content:
            f1_content[disease] = information
            continue

        f1_content[disease].update(information)

    return f1_content


if __name__ == "__main__":
    f1_content = get_json("./data/first_query.json")
    f2_content = get_json("./data/second_query.json")

    content = merge(f1_content, f2_content)

    write_to_file("wikidata.json", content)