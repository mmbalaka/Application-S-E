"""Compile les fichiers de traduction .po en .mo (remplace `manage.py compilemessages`,
qui exige GNU gettext, non disponible sous Windows).

Usage : python scripts/compile_translations.py
"""
from pathlib import Path

import polib

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / "locale"


def main() -> None:
    po_files = sorted(LOCALE_DIR.glob("*/LC_MESSAGES/*.po"))
    if not po_files:
        print(f"Aucun fichier .po trouvé dans {LOCALE_DIR}")
        return
    for po_path in po_files:
        mo_path = po_path.with_suffix(".mo")
        po = polib.pofile(str(po_path))
        po.save_as_mofile(str(mo_path))
        print(f"Compilé : {po_path.relative_to(BASE_DIR)} -> {mo_path.name} ({len(po)} messages)")


if __name__ == "__main__":
    main()
