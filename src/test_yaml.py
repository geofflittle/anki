import os
import genanki
import yaml
import re
from datetime import datetime
import shutil

alpha = re.compile("[^A-Za-z0-9_ ]+")


def get_dash_case(val):
    return alpha.sub('', val).lower().replace(" ", "-")


def get_notes(text):
    title = get_dash_case(text["title"])
    notes = [(title + "-" + str(i), note) for (i, note) in enumerate(text["notes"])] if "notes" in text else []
    section_notes = [(title + "-" + t, note) for section in text["sections"] for (t, note) in get_notes(section)] \
        if "sections" in text else []
    return notes + section_notes


def run(path):
    basename = os.path.basename(path)
    name = os.path.splitext(basename)[0]
    deck_name = name.replace("_", " ").title()
    deck = genanki.Deck(
        hash(deck_name),
        deck_name
    )
    with open(path) as f:
        text = yaml.load(f, Loader=yaml.FullLoader)
        notes = get_notes(text)
        generated = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
        for (id,note) in notes:
            print(note)
            genaki_note = genanki.Note(
                guid=genanki.guid_for(id),
                sort_field=id,
                tags=["generated_" + generated],
                fields=[note],
                model=genanki.CLOZE_MODEL
            )
            deck.add_note(genaki_note)
    genanki.Package(deck).write_to_file("./dist/{}.apkg".format(name))


if __name__ == "__main__":
    shutil.rmtree("./dist")
    os.makedirs("./dist")
    run("./assets/test_collection.yml")
