"""Recherche, compatibilités et préparation des commandes BureauBlasters."""

import re


# Étape 2 : nettoyer une recherche et combiner des critères.
def rechercher_produits(catalogue, recherche):
    """Retourne les fiches dont le nom ou la description contient la recherche nettoyée."""
    query = recherche.strip().lower()
    return [
        item
        for item in catalogue
        if query in item["nom"].lower() or query in item["description"].lower()
    ]


def selectionner_equipements(catalogue, prix_max, poids_max_g, longueur_max_cm):
    """Retourne les lanceurs et accessoires respectant les trois maxima inclusifs."""
    result = [
        item
        for item in catalogue
        if item["prix_euros"] <= prix_max
        and item["poids_g"] <= poids_max_g
        and item["dimensions_cm"]["longueur"] <= longueur_max_cm
        and item["categorie"] in ["lanceur", "accessoire"]
    ]
    return result


# Étape 3 : réunir les codes, filtrer les fiches et repérer une offre manquante.
def consommables_disponibles(catalogue):
    """Retourne les codes utilisés ou fournis, sans doublons ni mutation."""
    return {
        item
        for p in catalogue
        for k in ("consommables_utilises", "consommables_fournis")
        for item in p.get(k, [])
    }


def filtrer_par_consommable(catalogue, code):
    """Retourne une nouvelle liste des utilisateurs et fournisseurs du code, dans l'ordre."""
    return [
        produit
        for produit in catalogue
        if code in produit["consommables_utilises"]
        or code in produit["consommables_fournis"]
    ]


def consommables_sans_offre(catalogue):
    """Retourne les codes utilisés par un produit mais fournis par aucune référence."""
    consommables_utilises = {
        consommable
        for produit in catalogue
        for consommable in produit["consommables_utilises"]
    }
    consommables_fournis = {
        consommable
        for produit in catalogue
        for consommable in produit["consommables_fournis"]
    }
    return consommables_utilises - consommables_fournis


# Étape 4 : transformer chaque demande en une ligne de commande indépendante.
def trouver_produit(catalogue, identifiant):
    """Retourne la fiche d'identifiant exact, ou None si elle est absente."""
    resultat = [produit for produit in catalogue if produit["id"] == identifiant]
    return resultat[0] if len(resultat) > 0 else None


def lire_demande(texte):
    """Retourne un dictionnaire id/quantite depuis une ligne « identifiant ; entier »."""
    parties = re.findall(r"(\w+-?\d*)\s*;\s*(\d+)\s*", texte.strip())
    if len(parties) == 1 and len(parties[0]) == 2:
        return {"id": parties[0][0].upper(), "quantite": int(parties[0][1])}
    else:
        return {}


def calculer_budget(produit, quantite):
    """Retourne le prix de quantite conditionnements, entière positive ou nulle, arrondi à deux décimales."""
    return round(produit["prix_euros"] * quantite, 2)


def preparer_ligne(produit, quantite):
    """Retourne une copie superficielle de la fiche avec quantite et sous_total_euros."""
    return produit.copy() | {
        "quantite": quantite,
        "sous_total_euros": calculer_budget(produit, quantite),
    }


def preparer_commande(catalogue, demandes):
    """Retourne un dictionnaire lignes/inconnues en ignorant les demandes blanches."""
    commande = {"lignes": [], "inconnues": []}
    for demande in demandes:
        demande_lue = lire_demande(demande)
        if demande_lue:
            if produit := trouver_produit(catalogue, demande_lue["id"]):
                ligne = preparer_ligne(produit, demande_lue["quantite"])
                if {"quantite", "sous_total_euros"} < ligne.keys():
                    commande["lignes"].append(ligne)
                else:
                    raise ValueError(
                        f"Attributs manquants dans ligne de devis: {ligne}"
                    )
            else:
                if _id := demande_lue["id"].strip():
                    commande["inconnues"].append(_id)
        elif type(demande) is str and (d := demande.strip()):
            commande["inconnues"].append(d)

    return commande


# Étape 5 : réutiliser les résultats et choisir les effets sur les données.
def calculer_total(lignes):
    """Retourne la somme des sous-totaux arrondie à deux décimales, ou zéro."""
    return round(sum([ligne["sous_total_euros"] for ligne in lignes]), 2)


def total_avec_livraison(lignes, frais_euros=6):
    """Ajoute les frais une seule fois si les lignes ne sont pas vides, sinon retourne zéro."""
    if not lignes:
        return calculer_total(lignes)
    else:
        return calculer_total(lignes) + frais_euros


def formater_devis(lignes, frais_euros=6):
    """Retourne le récapitulatif textuel avec deux décimales et un total livré."""
    return "\n".join(
        [
            f"{ligne["id"]} | {ligne["quantite"]} x {ligne["nom"]} : {ligne["sous_total_euros"]:.2f} €"
            for ligne in lignes
        ]
        + [f"Total livré : {total_avec_livraison(lignes, frais_euros):.2f} €"]
    )


def definir_favori(produit, favori):
    """Modifie uniquement favori dans le dictionnaire reçu et retourne None."""
    produit["favori"] = favori


# Bonus audio : retrouver les chemins associés à une référence.
def sons_pour_produit(identifiant, associations):
    """Retourne les chemins associés à l'identifiant, ou une liste vide."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("sons_pour_produit est à compléter.")
