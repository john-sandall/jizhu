# 记住 (Jì zhù)

[![CI](https://github.com/john-sandall/jizhu/actions/workflows/main.yaml/badge.svg)](https://github.com/john-sandall/jizhu/actions/workflows/main.yaml)

> 用 Anki 记住中文单词
> Yòng Anki jì zhù zhōngwén dāncí
> Memorize Chinese words with Anki

## Usage

1. Open most recent file in ./data/raw (e.g `PM-2A-2.xlsx__2023-03-18_0125.xlsx`)
2. Add new entries. Column A (`Hanzi`) must be non-empty.
3. Run `python -m jizhu.create FILENAME --deck "DECK NAME"`, this will:
   - Iterate over rows in Sheet1 where `Hanzi` column is non-empty.
   - If `Pinyin` row is empty, add it.
   - If `English` row is empty, add it.
   - For all row where `Added` is empty, we create a set of Anki notes and mark `Added` column with TRUE.
   - Timestamp and export new XLSX. No need to rename, it will remove last timetamp and replace.
   - Creates new Anki file to import with new cards only.


## Contributors cheatsheet

  - **pre-commit:** `pre-commit run --all-files`
  - **pytest:** `pytest` or `pytest -s`
  - **coverage:** `coverage run -m pytest` or `coverage html`
  - **poetry sync:** `poetry install --no-root --sync`
  - **updating requirements:** see [docs/updating_requirements.md](docs/updating_requirements.md)
  - **create towncrier entry:** `towncrier create 123.added --edit`


## Initial project setup

1. See [docs/getting_started.md](docs/getting_started.md) or [docs/quickstart.md](docs/quickstart.md)
   for how to get up & running.
2. Check [docs/project_specific_setup.md](docs/project_specific_setup.md) for project specific setup.
3. See [docs/using_poetry.md](docs/using_poetry.md) for how to update Python requirements using
   [Poetry](https://python-poetry.org/).
4. See [docs/detect_secrets.md](docs/detect_secrets.md) for more on creating a `.secrets.baseline`
   file using [detect-secrets](https://github.com/Yelp/detect-secrets).
5. See [docs/using_towncrier.md](docs/using_towncrier.md) for how to update the `CHANGELOG.md`
   using [towncrier](https://github.com/twisted/towncrier).


## Useful links

- [How to Type Pinyin with Tone Marks on Windows and Mac OS](https://yoyochinese.com/blog/how-to-type-pinyin-mandarin-chinese-tone-marks-windows-mac-os)
- [Google Translate](https://translate.google.com/?sl=zh-CN&tl=en)
