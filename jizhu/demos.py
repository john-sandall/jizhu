"""Make Anki deck."""

import genanki
from google.cloud import translate_v2 as translate
from pypinyin import pinyin


def main(text: str):
    """Make Anki deck."""
    translate_client = translate.Client()
    # Target must be an ISO 639-1 language code.
    # See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    # English is 'en'
    # Chinese Simplified is 'zh-CN'

    # Text can also be a sequence of strings, in which case this method will return a sequence of
    # results for each text.
    english = translate_client.translate(text, target_language="en")["translatedText"]
    py = " ".join([x[0].strip() for x in pinyin(text)])

    print(f"{english=}")
    print(f"{py=}")


def make_anki_deck():
    my_model = genanki.Model(
        # import random; random.randrange(1 << 30, 1 << 31)  # noqa: E800
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

    my_note = genanki.Note(model=my_model, fields=["Capital of Argentina", "Buenos Aires"])

    # import random; random.randrange(1 << 30, 1 << 31)  # noqa: E800
    my_deck = genanki.Deck(1698022074, "Country Capitals")
    my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file("output.apkg")


if __name__ == "__main__":
    main(text="用 Anki 记住中文单词")
    make_anki_deck()
