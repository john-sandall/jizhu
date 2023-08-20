"""Make Anki deck.

Usage:

    python -m jizhu.create Inputs.xlsx
"""
from datetime import datetime
from pathlib import Path

import genanki
import pandas as pd
import typer
from google.cloud import translate_v2 as translate
from joblib import Memory
from pypinyin import pinyin

ROOT = Path(".")
cachedir = ROOT / ".cache"
memory = Memory(cachedir, verbose=0)


def get_model():
    return genanki.Model(
        1775386933,
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )


@memory.cache
def translate_to_english(text: str):
    """Make Anki deck."""
    translate_client = translate.Client()
    # Target must be an ISO 639-1 language code.
    # See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    # English is 'en'
    # Chinese Simplified is 'zh-CN'

    # Text can also be a sequence of strings, in which case this method will return a sequence of
    # results for each text.
    english = translate_client.translate(text, target_language="en")["translatedText"]
    pinyin_characters = " ".join([x[0].strip() for x in pinyin(text)])

    return {"hanzi": text, "english": english, "pinyin": pinyin_characters}


def make_notes(hanzi, model):
    output = translate_to_english(hanzi)
    # Card 1: Hanzi on front, pinyin + English on back
    back = f"{output['pinyin']}<br/>{output['english']}"
    note1 = genanki.Note(model=model, fields=[hanzi, back])
    # Card 2: pinyin on front, English + hanzi on back
    note2 = genanki.Note(model=model, fields=[output["pinyin"], f"{output['english']}<br/>{hanzi}"])
    # Card 3: English on front, pinyin + hanzi on back
    note3 = genanki.Note(model=model, fields=[output["english"], f"{output['pinyin']}<br/>{hanzi}"])

    return note1, note2, note3


def make_anki_deck(filename: str, deck: str = "Mandarin World - Level 2 - A"):
    """
    Generate unique IDs:
        import random; random.randrange(1 << 30, 1 << 31)
    """
    deck_id_lookup = {
        "Mandarin World - Level 2 - A": 1963098631,
        "Mando John": 1101970412,
    }
    if deck not in deck_id_lookup:
        raise RuntimeError(
            f"Deck `{deck}` not found in deck_id_lookup. "
            "Please run the following to generate an ID:"
            "\n`import random; random.randrange(1 << 30, 1 << 31)`",
        )
    deck_id = deck_id_lookup[deck]
    deck = genanki.Deck(deck_id, deck)
    # deck = genanki.Deck(1876232028, "Test1")  # noqa: E800
    model = get_model()

    df = pd.read_excel(ROOT / "data" / "raw" / filename, sheet_name="Sheet1").dropna(subset="Hanzi")
    for i, row in df.iterrows():
        hanzi = row["Hanzi"]
        if pd.isna(row["Pinyin"]):
            df.loc[i, "Pinyin"] = translate_to_english(hanzi)["pinyin"]
        if pd.isna(row["English"]):
            df.loc[i, "English"] = translate_to_english(hanzi)["english"]
        if pd.isna(row["Added"]):
            notes = make_notes(hanzi, model)
            for note in notes:
                deck.add_note(note)
            df.loc[i, "Added"] = True

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    df.to_excel(ROOT / "data" / "raw" / f"{filename.split('__')[0]}__{timestamp}.xlsx", index=False)
    genanki.Package(deck).write_to_file(ROOT / "data" / "decks" / f"deck__{timestamp}.apkg")


if __name__ == "__main__":
    typer.run(make_anki_deck)
