from anki.lang import _
from aqt import mw
from aqt.dbcheck import check_db
from aqt.importing import onImport
from aqt.qt import qconnect
# from aqt.utils import showInfo
from PyQt5 import QtWidgets


# This function expects existing cards in the collection and the cards in the file to be imported each to contain a
# "generated_*" tag.  Existing cards with this tag that are *not* updated by the import are deleted.
def put_import():
    generated_tags = set()
    for cid in mw.col.find_cards(""):
        card = mw.col.getCard(cid)
        card_generated_tags = [tag for tag in card.note().tags if tag.startswith("generated_")]
        generated_tags.update(card_generated_tags)
    # showInfo(_("found tags: " + ",".join(generated_tags)))
    onImport(mw)
    query = " or ".join(["tag:" + tag for tag in generated_tags])
    # showInfo(_("query: " + query))
    cards_to_remove = [cid for cid in mw.col.find_cards(query)]
    # showInfo(_("to rem: " + ",".join([str(card) for card in cards_to_remove])))
    mw.col.remove_notes_by_card(cards_to_remove)
    check_db(mw)


actionPutImport = QtWidgets.QAction(mw)
actionPutImport.setText(_("&Put Import"))
actionPutImport.setObjectName("actionPutImport")
qconnect(actionPutImport.triggered, put_import)
mw.form.menuCol.addAction(actionPutImport)
