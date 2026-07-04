"""Import d'indicateurs depuis un fichier CSV ou Excel (.xlsx).

Les entêtes de colonnes sont reconnues de façon souple (accents, majuscules,
espaces ignorés). Colonnes reconnues :

    code, intitule, definition, type (intrant/processus/produit/effet/impact),
    unite, baseline, cible_finale, frequence, mode_calcul, methode_collecte,
    source_donnees, moyen_verification, numerateur, denominateur

Seul « intitule » est obligatoire. Si un indicateur du même projet porte déjà
le même code (ou le même intitulé), il est mis à jour au lieu d'être dupliqué.
"""
import csv
import io
import unicodedata

from django.utils.translation import gettext as _

from .models import Indicateur


def _normaliser(texte):
    """minuscules, sans accents, espaces/tirets -> underscore."""
    if texte is None:
        return ""
    texte = str(texte).strip().lower()
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    for ch in (" ", "-", "/", "'", "’", "(", ")"):
        texte = texte.replace(ch, "_")
    while "__" in texte:
        texte = texte.replace("__", "_")
    return texte.strip("_")


# Synonymes d'entêtes -> nom de champ
ALIAS = {
    "code": "code",
    "code_indicateur": "code",
    "reference": "code",
    "intitule": "intitule",
    "indicateur": "intitule",
    "nom": "intitule",
    "intitule_de_l_indicateur": "intitule",
    "definition": "definition",
    "type": "niveau",
    "niveau": "niveau",
    "type_d_indicateur": "niveau",
    "unite": "unite",
    "unite_de_mesure": "unite",
    "baseline": "baseline",
    "valeur_de_reference": "baseline",
    "reference_baseline": "baseline",
    "cible": "cible_finale",
    "cible_finale": "cible_finale",
    "valeur_cible": "cible_finale",
    "frequence": "frequence",
    "frequence_de_collecte": "frequence",
    "mode_calcul": "mode_calcul",
    "formule": "mode_calcul",
    "formule_de_calcul": "mode_calcul",
    "methode_collecte": "methode_collecte",
    "methode_de_collecte": "methode_collecte",
    "source": "source_donnees",
    "source_donnees": "source_donnees",
    "source_de_donnees": "source_donnees",
    "moyen_verification": "moyen_verification",
    "moyen_de_verification": "moyen_verification",
    "moyens_de_verification": "moyen_verification",
    "numerateur": "numerateur_libelle",
    "libelle_numerateur": "numerateur_libelle",
    "denominateur": "denominateur_libelle",
    "libelle_denominateur": "denominateur_libelle",
}

NIVEAUX = {
    "intrant": Indicateur.Niveau.INTRANT,
    "input": Indicateur.Niveau.INTRANT,
    "processus": Indicateur.Niveau.PROCESSUS,
    "process": Indicateur.Niveau.PROCESSUS,
    "produit": Indicateur.Niveau.PRODUIT,
    "extrant": Indicateur.Niveau.PRODUIT,
    "output": Indicateur.Niveau.PRODUIT,
    "produit_extrant": Indicateur.Niveau.PRODUIT,
    "effet": Indicateur.Niveau.EFFET,
    "resultat": Indicateur.Niveau.EFFET,
    "resultat_effet": Indicateur.Niveau.EFFET,
    "outcome": Indicateur.Niveau.EFFET,
    "impact": Indicateur.Niveau.IMPACT,
}

FREQUENCES = {
    "mensuelle": Indicateur.Frequence.MENSUELLE,
    "mensuel": Indicateur.Frequence.MENSUELLE,
    "mois": Indicateur.Frequence.MENSUELLE,
    "monthly": Indicateur.Frequence.MENSUELLE,
    "trimestrielle": Indicateur.Frequence.TRIMESTRIELLE,
    "trimestriel": Indicateur.Frequence.TRIMESTRIELLE,
    "trimestre": Indicateur.Frequence.TRIMESTRIELLE,
    "quarterly": Indicateur.Frequence.TRIMESTRIELLE,
    "semestrielle": Indicateur.Frequence.SEMESTRIELLE,
    "semestriel": Indicateur.Frequence.SEMESTRIELLE,
    "semestre": Indicateur.Frequence.SEMESTRIELLE,
    "annuelle": Indicateur.Frequence.ANNUELLE,
    "annuel": Indicateur.Frequence.ANNUELLE,
    "annee": Indicateur.Frequence.ANNUELLE,
    "yearly": Indicateur.Frequence.ANNUELLE,
    "annual": Indicateur.Frequence.ANNUELLE,
}


def _nombre(valeur):
    """Convertit '1 234,5' -> 1234.5 ; renvoie None si vide/invalide."""
    if valeur in (None, ""):
        return None
    try:
        return float(str(valeur).replace(" ", "").replace(" ", "").replace(",", "."))
    except ValueError:
        return None


def _lignes_csv(fichier):
    """Itère les lignes d'un fichier CSV (détection , ou ;)."""
    brut = fichier.read()
    for encodage in ("utf-8-sig", "cp1252"):
        try:
            texte = brut.decode(encodage)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(_("Encodage du fichier non reconnu (utiliser UTF-8)."))
    premiere = texte.splitlines()[0] if texte.splitlines() else ""
    delimiteur = ";" if premiere.count(";") >= premiere.count(",") else ","
    return list(csv.reader(io.StringIO(texte), delimiter=delimiteur))


def _lignes_xlsx(fichier):
    """Itère les lignes de la première feuille d'un classeur Excel."""
    import openpyxl

    classeur = openpyxl.load_workbook(fichier, read_only=True, data_only=True)
    feuille = classeur.worksheets[0]
    return [[cellule for cellule in ligne] for ligne in feuille.iter_rows(values_only=True)]


def importer_indicateurs(projet, fichier, nom_fichier):
    """Importe les indicateurs du fichier dans le projet.

    Retourne (nb_crees, nb_mis_a_jour, erreurs).
    """
    if nom_fichier.lower().endswith((".xlsx", ".xlsm")):
        lignes = _lignes_xlsx(fichier)
    else:
        lignes = _lignes_csv(fichier)

    if not lignes:
        return 0, 0, [_("Le fichier est vide.")]

    entetes = [_normaliser(c) for c in lignes[0]]
    colonnes = {}
    for position, entete in enumerate(entetes):
        champ = ALIAS.get(entete)
        if champ and champ not in colonnes:
            colonnes[champ] = position

    if "intitule" not in colonnes:
        return 0, 0, [
            _("Colonne « intitulé » introuvable. Entêtes lues : %(entetes)s")
            % {"entetes": ", ".join(str(c) for c in lignes[0])}
        ]

    crees, mis_a_jour, erreurs = 0, 0, []
    for numero, ligne in enumerate(lignes[1:], start=2):
        if not ligne or all(c in (None, "") for c in ligne):
            continue

        def valeur_de(champ):
            position = colonnes.get(champ)
            if position is None or position >= len(ligne):
                return ""
            return str(ligne[position]).strip() if ligne[position] is not None else ""

        intitule = valeur_de("intitule")
        if not intitule:
            erreurs.append(_("Ligne %(n)s : intitulé manquant — ignorée.") % {"n": numero})
            continue

        champs = {
            "definition": valeur_de("definition"),
            "unite": valeur_de("unite") or "—",
            "mode_calcul": valeur_de("mode_calcul"),
            "methode_collecte": valeur_de("methode_collecte"),
            "source_donnees": valeur_de("source_donnees"),
            "moyen_verification": valeur_de("moyen_verification"),
            "numerateur_libelle": valeur_de("numerateur_libelle"),
            "denominateur_libelle": valeur_de("denominateur_libelle"),
        }
        niveau = NIVEAUX.get(_normaliser(valeur_de("niveau")))
        if niveau:
            champs["niveau"] = niveau
        frequence = FREQUENCES.get(_normaliser(valeur_de("frequence")))
        if frequence:
            champs["frequence"] = frequence
        baseline = _nombre(valeur_de("baseline"))
        if baseline is not None:
            champs["baseline"] = baseline
        cible_finale = _nombre(valeur_de("cible_finale"))
        if cible_finale is not None:
            champs["cible_finale"] = cible_finale
        # Numérateur/dénominateur renseignés => pourcentage par défaut
        if champs["numerateur_libelle"] and champs["denominateur_libelle"]:
            champs.setdefault("type_valeur", Indicateur.TypeValeur.POURCENTAGE)

        code = valeur_de("code")
        champs = {cle: v for cle, v in champs.items() if v not in ("", None)}

        # Mise à jour si le code (ou l'intitulé) existe déjà dans ce projet
        existant = None
        if code:
            existant = Indicateur.objects.filter(projet=projet, code=code).first()
        if existant is None:
            existant = Indicateur.objects.filter(projet=projet, intitule=intitule).first()

        if existant:
            for cle, v in champs.items():
                setattr(existant, cle, v)
            existant.intitule = intitule
            if code:
                existant.code = code
            existant.save()
            mis_a_jour += 1
        else:
            Indicateur.objects.create(
                projet=projet, code=code, intitule=intitule, **champs
            )
            crees += 1

    return crees, mis_a_jour, erreurs
