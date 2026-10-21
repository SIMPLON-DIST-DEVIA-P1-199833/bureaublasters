"""Tes tests obligatoires : python tests_catalogue.py perso."""

from typing import assert_type, Set
from copy import deepcopy

from fonctions import (
    calculer_total,
    consommables_disponibles,
    filtrer_par_consommable,
    consommables_sans_offre,
    definir_favori,
    formater_devis,
    lire_demande,
    preparer_commande,
    preparer_ligne,
    rechercher_produits,
    selectionner_equipements,
    total_avec_livraison,
)

from catalogue import CATALOGUE


def catalogue_essai():
    return [
        {
            "id": "L1",
            "nom": "Lanceur",
            "description": "Propulse une bille.",
            "categorie": "lanceur",
            "prix_euros": 20,
            "poids_g": 800,
            "dimensions_cm": {"longueur": 50},
            "favori": False,
            "consommables_utilises": ["bille"],
            "consommables_fournis": [],
        },
        {
            "id": "A1",
            "nom": "Brume",
            "description": "Un accessoire de poche.",
            "categorie": "accessoire",
            "prix_euros": 15,
            "poids_g": 801,
            "dimensions_cm": {"longueur": 10},
            "favori": False,
            "consommables_utilises": ["liquide"],
            "consommables_fournis": [],
        },
        {
            "id": "M1",
            "nom": "Billes",
            "description": "Pour le lanceur.",
            "categorie": "munition",
            "prix_euros": 5,
            "poids_g": 100,
            "dimensions_cm": {"longueur": 10},
            "favori": False,
            "consommables_utilises": [],
            "consommables_fournis": ["bille"],
        },
    ]


def catalogue_normal():
    return CATALOGUE


# Étape 2 : comparer les références et vérifier une frontière.
def test_recherche_normalisee():
    """Avec catalogue_essai(), «  LANCEUR  » et « lanceur » doivent retrouver L1 et M1."""
    catalogue = catalogue_essai()
    resultat = rechercher_produits(catalogue, "  LANCEUR  ")
    assert {produit["id"] for produit in resultat} == {"L1", "M1"}


def test_selection_seuil_inclus():
    """Avec les maxima 20 €, 800 g et 50 cm, seule L1 convient ; A1 dépasse le poids."""
    catalogue = catalogue_normal()
    resultat = selectionner_equipements(catalogue, 60, 800, 50)
    resultat_BB = {
        produit["id"] for produit in resultat if produit["id"].startswith("BB")
    }
    assert resultat_BB == {"BB-01", "BB-04", "BB-06", "BB-08"}


def test_consommables_disponibles():
    consommables = consommables_disponibles(catalogue_normal())
    assert_type(consommables, Set[str])
    assert "croissant-mousse" in consommables
    assert len(consommables) > 0


def test_filtrer_par_consommable():
    assert [
        produit["id"]
        for produit in filtrer_par_consommable(catalogue_normal(), "croissant-mousse")
    ] == [
        "BB-07",
        "RE-05",
    ]


# Étape 3 : comparer les besoins aux références fournies.
def test_consommable_sans_fournisseur():
    """catalogue_essai() utilise « liquide » sans fournisseur ; seul ce code est attendu."""
    assert consommables_sans_offre(catalogue_essai()) == {"liquide"}


# Étape 4 : contrôler la conversion et la copie d'une fiche.
def test_lecture_demande():
    """« l1 ; 2 » doit donner {"id": "L1", "quantite": 2}, avec une quantité entière."""
    assert lire_demande("BB-01 ; 75") == {"id": "BB-01", "quantite": 75}
    assert lire_demande("RE-13    ;    11") == {"id": "RE-13", "quantite": 11}
    assert lire_demande(" l1 ; 2 ") == {"id": "L1", "quantite": 2}
    assert lire_demande("corn flakes") == {}


def test_ligne_independante():
    """Deux L1 coûtent 40 € ; la ligne est un autre dictionnaire et la fiche reste inchangée."""
    produit_l1 = catalogue_essai()[0]
    ligne = preparer_ligne(produit_l1, 2)
    assert ligne["sous_total_euros"] == 40
    assert ligne["quantite"] == 2
    assert ligne["nom"] == produit_l1["nom"]


# Étape 5 : vérifier les cumuls, le paramètre par défaut et la mutation choisie.
def test_total_cumule():
    """Deux lignes de sous-totaux 40 € et 15 € donnent 55 €, sans modifier les lignes."""
    lignes = [{"sous_total_euros": 40}, {"sous_total_euros": 15}]
    assert calculer_total(lignes) == 55


def test_commande_vide_sans_frais():
    """Une commande vide donne zéro, même avec 10 € de frais demandés."""
    assert total_avec_livraison([], 3) == 0
    assert total_avec_livraison([], 3) == 0


def test_favori_autres_champs():
    """Active puis désactive le favori de L1 ; les autres champs restent inchangés, retour None."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    produit = catalogue_essai()[0].copy()
    produit["favori"] = "anything"
    definir_favori(produit, True)
    assert produit["favori"] == True


def test_frais_parametres():
    """Deux lignes totalisant 55 € donnent 61 € par défaut, 55 € avec zéro et 65 € avec dix."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    lignes = [{"sous_total_euros": 40}, {"sous_total_euros": 15}]
    assert total_avec_livraison(lignes) == 61
    assert total_avec_livraison(lignes, 0) == 55
    assert total_avec_livraison(lignes, 10) == 65


# Étape 6 : vérifier plusieurs fonctions dans un même parcours.
def test_parcours_complet():
    """Deux L1, une référence absente et trois M1 donnent 55 € avant frais et 61 € livrés."""
    orig_catalogue_essai = deepcopy(catalogue_essai())
    demandes = [" l1 ; 2 ", " absent ; 1 ", "m1;3", "   "]
    orig_demandes = demandes.copy()
    commande = preparer_commande(catalogue_essai(), demandes)
    assert {"lignes", "inconnues"} <= commande.keys()
    assert len(commande["lignes"]) == 2
    assert len(commande["inconnues"]) == 1
    assert commande["lignes"][0]["id"] == "L1"
    assert commande["lignes"][1]["id"] == "M1"
    assert (
        commande["lignes"][1]["sous_total_euros"]
        + commande["lignes"][0]["sous_total_euros"]
        == 55
    )
    devis = formater_devis(commande["lignes"])
    devis_lines = devis.split("\n")
    assert len(devis_lines) == 3
    assert devis_lines[-1].endswith("61.00 €")
    assert (
        devis
        == "L1 | 2 x Lanceur : 40.00 €\nM1 | 3 x Billes : 15.00 €\nTotal livré : 61.00 €"
    )
    assert orig_catalogue_essai == catalogue_essai()
    assert demandes == orig_demandes
