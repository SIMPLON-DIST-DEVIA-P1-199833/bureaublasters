"""Recherche, compatibilités et préparation des commandes BureauBlasters."""


# Étape 2 : nettoyer une recherche et combiner des critères.
def rechercher_produits(catalogue, recherche):
    """Retourne les fiches dont le nom ou la description contient la recherche nettoyée."""
    stripped_search = recherche.strip().lower()
    search_result = []
    for product in catalogue:
        if (
            stripped_search in product["nom"].lower()
            or stripped_search in product["description"].lower()
        ):
            search_result.append(product)
    return search_result


def selectionner_equipements(catalogue, prix_max, poids_max_g, longueur_max_cm):
    """Retourne les lanceurs et accessoires respectant les trois maxima inclusifs."""
    selected_equipment_list = []
    for product in catalogue:
        if (
            product["categorie"] == "lanceur" or product["categorie"] == "accessoire"
        ) and (
            product["prix_euros"] <= prix_max
            and product["poids_g"] <= poids_max_g
            and product["dimensions_cm"]["longueur"] <= longueur_max_cm
        ):
            selected_equipment_list.append(product)
    return selected_equipment_list


# Étape 3 : réunir les codes, filtrer les fiches et repérer une offre manquante.
def consommables_disponibles(catalogue):
    """Retourne les codes utilisés ou fournis, sans doublons ni mutation."""
    consumables = set()
    for product in catalogue:
        for consum in product["consommables_utilises"]:
            if consum not in consumables:
                consumables.add(consum)
        for consum in product["consommables_fournis"]:
            if consum not in consumables:
                consumables.add(consum)
    return consumables


def filtrer_par_consommable(catalogue, code):
    """Retourne une nouvelle liste des utilisateurs et fournisseurs du code, dans l'ordre."""
    filtrered_catalogue = []
    for product in catalogue:
        if (
            code in product["consommables_utilises"]
            or code in product["consommables_fournis"]
        ):
            filtrered_catalogue.append(product)
    return filtrered_catalogue


def consommables_sans_offre(catalogue):
    """Retourne les codes utilisés par un produit mais fournis par aucune référence."""
    besoin = set()
    offre = set()
    for product in catalogue:
        for cons_used in product["consommables_utilises"]:
            if cons_used not in besoin:
                besoin.add(cons_used)
        for cons_offered in product["consommables_fournis"]:
            if cons_offered not in offre:
                offre.add(cons_offered)
    return set(besoin - offre)
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    # raise NotImplementedError("consommables_sans_offre est à compléter.")


# Étape 4 : transformer chaque demande en une ligne de commande indépendante.
def trouver_produit(catalogue, identifiant):
    """Retourne la fiche d'identifiant exact, ou None si elle est absente."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("trouver_produit est à compléter.")


def lire_demande(texte):
    """Retourne un dictionnaire id/quantite depuis une ligne « identifiant ; entier »."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("lire_demande est à compléter.")


def calculer_budget(produit, quantite):
    """Retourne le prix de quantite conditionnements, entière positive ou nulle, arrondi à deux décimales."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("calculer_budget est à compléter.")


def preparer_ligne(produit, quantite):
    """Retourne une copie superficielle de la fiche avec quantite et sous_total_euros."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("preparer_ligne est à compléter.")


def preparer_commande(catalogue, demandes):
    """Retourne un dictionnaire lignes/inconnues en ignorant les demandes blanches."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("preparer_commande est à compléter.")


# Étape 5 : réutiliser les résultats et choisir les effets sur les données.
def calculer_total(lignes):
    """Retourne la somme des sous-totaux arrondie à deux décimales, ou zéro."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("calculer_total est à compléter.")


def total_avec_livraison(lignes, frais_euros=6):
    """Ajoute les frais une seule fois si les lignes ne sont pas vides, sinon retourne zéro."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("total_avec_livraison est à compléter.")


def formater_devis(lignes, frais_euros=6):
    """Retourne le récapitulatif textuel avec deux décimales et un total livré."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("formater_devis est à compléter.")


def definir_favori(produit, favori):
    """Modifie uniquement favori dans le dictionnaire reçu et retourne None."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("definir_favori est à compléter.")


# Bonus audio : retrouver les chemins associés à une référence.
def sons_pour_produit(identifiant, associations):
    """Retourne les chemins associés à l'identifiant, ou une liste vide."""
    # À compléter : suis le contrat et les vérifications de cette étape dans le README.
    raise NotImplementedError("sons_pour_produit est à compléter.")
