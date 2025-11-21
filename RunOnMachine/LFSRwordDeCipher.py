
# simple_lfsr_with_dictionary.py

from typing import List
import math

# ---------- ciphertext ----------
cipher_bits = [
 1,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,1,0,0,1,1,
 1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0
]

# ---------- your 5 explicit keys ----------
key1 = [1,0,1,0,1,1,1,1,0,0,0,1,0,0,1]
key2 = [0,1,0,1,1,1,1,0,0,0,1,0,0,1,1]
key3 = [1,0,1,1,1,1,0,0,0,1,0,0,1,1,0]
key4 = [0,1,1,1,1,0,0,0,1,0,0,1,1,0,1]
key5 = [1,1,1,1,0,0,0,1,0,0,1,1,0,1,0]

keys = [key1, key2, key3, key4, key5]

# ---------- small French dictionary ----------
dictionary = [
    # Articles
    "LE","LA","LES","UN","UNE","DES","DU","DE","AU","AUX",

    # Pronouns
    "JE","TU","IL","ELLE","NOUS","VOUS","ILS","ELLES","ON","CE","CELA","CELUI",
    "QUI","QUE","QUOI","DONT","OU",

    # Common verbs (present/basic forms only)
    "ETRE","AVOIR","FAIRE","DIRE","POUVOIR","ALLER","VOULOIR","VOIR","SAVOIR",
    "DEVOIR","PRENDRE","PARLER","METTRE","DONNER","TROUVER","COMPRENDRE",
    "VENIR","PASSER","POURSUIVRE","LIRE","ECRIRE","SORTIR",

    # Everyday words
    "BONJOUR","SALUT","MERCI","OUI","NON","EXCUSE","PARDON","BIEN","MAL",
    "MAISON","FILLE","GARCON","HOMME","FEMME","AMIS","AMIE","TRAVAIL",
    "TEMPS","JOUR","NUIT","MATIN","SOIR","HEURE","MINUTE",

    # Prepositions
    "SUR","SOUS","AVEC","SANS","DANS","ENTRE","PENDANT","APRES","AVANT","POUR",
    "PAR","VERS","CHEZ","CONTRE","PRES","DEPUIS","SELON",

    # Conjunctions
    "ET","MAIS","OU","DONC","CAR","COMME","SI","LORSQUE","PARCE","QUE",

    # Numbers
    "UN","DEUX","TROIS","QUATRE","CINQ","SIX","SEPT","HUIT","NEUF","DIX",

    # School / exercise context words
    "FIN","EXERCICE","EXERCICES","QUESTION","REPONSE","DEVOIR","PROFESSEUR",
    "ETUDIANT","COURS","LECON","SUJET",

    # Tech / general nouns
    "SYSTEME","CODE","MESSAGE","CLE","DONNEE","BIT","SEQUENCE","LOGIQUE",
    "ALGORITHME","ANALYSE","RESULTAT","ERREUR","VALEUR",

    # Useful long words (great for scoring)
    "IMPORTANT","DIFFICILE","INTERESSANT","POSSIBLE","COMPLETE",
    "EVIDEMMENT","ACTUELLEMENT","RAPIDEMENT",

    # Additional common vocab
    "ANNEE","MOIS","SEMAINE","MAIN","TETE","OEIL","PAYS","VILLE","MONDE",
    "VRAI","FAUX","PETIT","GRAND","NOUVEAU","VIEUX","BEAU","BON","MEILLEUR",
    "TOUJOURS","JAMAIS","PEUT","PEUTETRE","DEJA","MAINTENANT","ICI","LA",
    "LAHAUT","LAISSER","DEMANDER","REPONDRE"
]


# ---------------- simple helpers ----------------
def repeat_to_length_simple(seq: List[int], target_len: int) -> List[int]:
    repeats = math.ceil(target_len / len(seq))
    big = seq * repeats
    return big[:target_len]

def xor_simple(a: List[int], b: List[int]) -> List[int]:
    return [x ^ y for x, y in zip(a, b)]

def bits5_to_letter(bits5):
    # join bits into a string like "10110"
    bin_str = "".join(str(b) for b in bits5)

    # convert from binary to decimal
    v = int(bin_str, 2)

    return chr(ord('A') + v) if 0 <= v < 26 else '?'

def bits_to_text_simple(bitstream: List[int]) -> str:
    out = []
    for i in range(0, len(bitstream), 5):
        b = bitstream[i:i+5]

        out.append(bits5_to_letter(b))
    return "".join(out)

# ---------- NEW: scoring using dictionary ----------
def score_text_with_dictionary(text: str, dict_words: List[str]) -> int:
    """
    Count how many dictionary words appear inside the text.
    Very simple but effective.
    """
    T = text.upper()
    score = 0
    for w in dict_words:
        if w in T:
            score += len(w)      # longer words give more score
    return score

# ---------- MAIN: process all keys and pick best ----------
def find_best_key():
    best_score = -1
    best_text = ""
    best_index = None

    for i, key in enumerate(keys, start=1):
        # 1. expand key
        key70 = repeat_to_length_simple(key, len(cipher_bits))

        # 2. xor
        plain_bits = xor_simple(cipher_bits, key70)

        # 3. convert to text
        text = bits_to_text_simple(plain_bits)

        # 4. score with dictionary
        score = score_text_with_dictionary(text, dictionary)

        print(f"Key{i}: {text}    (score={score})")

        # 5. select the best
        if score > best_score:
            best_score = score
            best_text = text
            best_index = i

    print("\nBest key:", best_index)
    print("Decoded text:", best_text)
    print("Score:", best_score)

# Run
if __name__ == "__main__":
    find_best_key()
