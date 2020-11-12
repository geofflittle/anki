import yaml
import re

alpha = re.compile('[^A-Za-z ]+')


def get_dash_case(val):
    return alpha.sub('', val).lower().replace(" ", "-")


def get_notes(text):
    title = get_dash_case(text["title"])
    notes = [(title + "-" + str(i), note) for (i, note) in enumerate(text["notes"])] if "notes" in text else []
    section_notes = [(title + "-" + t, note) for section in text["sections"] for (t, note) in get_notes(section)] \
        if "sections" in text else []
    return notes + section_notes


def run(path):
    with open(path) as f:
        text = yaml.load(f, Loader=yaml.FullLoader)
        notes = get_notes(text)
        for note in notes:
            print(note)


if __name__ == "__main__":
    run("van_sickles_modern_airmanship.yml")
