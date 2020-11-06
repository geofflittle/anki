import os
import re
import sys

import genanki
import yaml

# TODO: Breakdown this regex
words = r"[\w %]+"
cloze = r"{{c\d+::" + words + "}}"
cloze_regex = re.compile(r"^(?:\w+|{{c\d+::[\w' %]+}})(?:(?: |, |'s | \(|-| \")(?:\w+|{{c\d+::[\w' %]+}}))+(?:\)|\")?\.?$")


def write_deck_to_file(path):
    basename = os.path.basename(path)
    name = os.path.splitext(basename)[0]
    deck_name = name.replace("_", " ").title()
    deck = genanki.Deck(
        hash(deck_name),
        deck_name
    )
    with open(path) as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        seen = set()
        for note_data in notes:
            note_id = note_data["id"]
            note_cloze = note_data["cloze"]
            note_tags = note_data["tags"]
            if note_id in seen:
                sys.exit("duplicate id {} found".format(note_id))
            if not cloze_regex.match(note_cloze):
                sys.exit("note id {} with cloze '{}' doesn't match expected format".format(note_id, note_cloze))
            print(note_data)
            note = genanki.Note(
                guid=genanki.guid_for(note_id),
                fields=[note_cloze],
                tags=note_tags,
                model=genanki.CLOZE_MODEL
            )
            deck.add_note(note)
            seen.add(note_id)
    genanki.Package(deck).write_to_file("{}.apkg".format(name))


if __name__ == "__main__":
    deck_yamls = ["private_pilot_license.yml"]
    for deck_yaml in deck_yamls:
        write_deck_to_file(os.path.abspath(deck_yaml))

