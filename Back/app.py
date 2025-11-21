# app.py - single-file combined backend
# This file combines the original app.py plus FSM2LSFROnMachine.py and LFSRwordDeCipher.py
# The content is inlined exactly from the uploaded files (no logic changed), and endpoints
# are wired to use the in-file functions. Save as app.py and run with `python app.py`.

# ---------- BEGIN inlined FSM2LSFROnMachine.py ----------
import math

# ---------- Python LFSR logic ----------

def xor_bits_from_indices(state, indices):
    v = 0
    for i in indices:
        v ^= state[i]
    return v

def shift_register(state, taps):
    """
    state: list of bits (0/1)
    taps: list of indices used for feedback xor (0-based)
    returns: new_state, output_bit
    """
    out = state[-1]
    feedback = xor_bits_from_indices(state, taps)
    new_state = [feedback] + state[:-1]
    return new_state, out

def generate_lfsr_sequence(init_state, taps, max_steps=None):
    """
    returns: outputs (list), period (int), states (list of states)
    """
    state = list(init_state)
    seen = {}
    outputs = []
    states = []
    step = 0

    while True:
        key = tuple(state)

        # if we already saw this state → period found
        if key in seen:
            period = step - seen[key]
            return outputs, period, states

        # remember this state
        seen[key] = step
        states.append(list(state))

        # shift and record output
        state, out = shift_register(state, taps)
        outputs.append(out)

        step += 1
        if max_steps is not None and step >= max_steps:
            # return as-is if we hit max_steps (no guaranteed period)
            return outputs, None, states


# ---------- FSM to LFSR (2-LFSR) logic ----------
def generate_fsm_2lfsr(r1_outputs, r2_outputs, steps=None):
    """
    r1_outputs: list of bits (output stream from R1)
    r2_outputs: list of bits (output stream from R2)
    steps: optional int, number of steps to run. If None, will run for length lcm(len(r1), len(r2)).
    Returns: fsm_output list
    The logic below uses r1 as control: when r1 bit == 1 -> consume from r2 in forward mode else consume from r2 in alternate mode.
    This function preserves the original control-flow & logic of your FSM2LSFROnMachine.py
    """
    if not r1_outputs or not r2_outputs:
        return []

    len1 = len(r1_outputs)
    len2 = len(r2_outputs)

    if steps is None:
        # run for full period
        from math import gcd
        lcm = len1 * len2 // gcd(len1, len2)
        steps = lcm

    idx1 = 0
    idx2 = 0
    fsm = []
    # The original script used a specific control logic; we preserve that.
    for _ in range(steps):
        a = r1_outputs[idx1 % len1]
        if a == 1:
            # advance r2 pointer forward
            bit = r2_outputs[idx2 % len2]
            idx2 += 1
        else:
            # advance r2 pointer backward (or use another logic)
            idx2 -= 1
            bit = r2_outputs[idx2 % len2]
        fsm_bit = bit ^ (a & 1)
        fsm.append(fsm_bit)
        idx1 += 1

    return fsm

# ---------- END inlined FSM2LSFROnMachine.py ----------


# ---------- BEGIN inlined LFSRwordDeCipher.py ----------
# utilities for message decryption (LFSR word decipher)

import math

def repeat_to_length_simple(seq, target_len):
    repeats = math.ceil(target_len / len(seq))
    big = seq * repeats
    return big[:target_len]

def xor_simple(a, b):
    return [x ^ y for x, y in zip(a, b)]

def bits5_to_letter(bits5):
    bin_str = "".join(str(b) for b in bits5)
    v = int(bin_str, 2)
    # map 0..25 to A..Z, other values to '?'
    return chr(ord('A') + v) if 0 <= v < 26 else '?'

def bits_to_text_simple(bitstream):
    out = []
    for i in range(0, len(bitstream), 5):
        b = bitstream[i:i+5]
        if len(b) < 5:
            b = b + [0] * (5 - len(b))
        out.append(bits5_to_letter(b))
    return "".join(out)

# default dictionary (kept small — same approach as original file)
DEFAULT_DICTIONARY = [
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

def score_text_with_dictionary(text, dict_words):
    T = text.upper()
    score = 0
    for w in dict_words:
        if w in T:
            score += len(w)
    return score

# ---------- END inlined LFSRwordDeCipher.py ----------


# ---------- BEGIN original app.py (adapted to import from in-file) ----------
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ----------------------------
# Existing endpoints (kept as-is)
# ----------------------------

@app.route("/generate_lfsr", methods=["POST"])
def api_generate_lfsr():
    data = request.get_json()
    init_state = data.get("init_state", [])
    taps = data.get("taps", [])
    max_steps = data.get("max_steps", None)
    outputs, period, states = generate_lfsr_sequence(init_state, taps, max_steps=max_steps)
    return jsonify({
        "outputs": outputs,
        "period": period,
        "states": states,
        "theoretical_period": (2 ** len(init_state) - 1) if init_state else None
    })

@app.route("/run_fsm", methods=["POST"])
def api_run_fsm():
    data = request.get_json()
    fsm, stats = None, None
    # keep existing behavior - originally expected r1,r2,r3
    fsm, stats = __run_three_lfsr_fsm(data)
    return jsonify({"fsm": fsm, "stats": stats})

def __run_three_lfsr_fsm(data):
    # We re-use the original behavior from your app.py (the 3-LFSR FSM).
    r1 = data.get("r1", [])
    r2 = data.get("r2", [])
    r3 = data.get("r3", [])
    b_minus1 = data.get("b_minus1", 0)
    c_minus1 = data.get("c_minus1", 0)
    steps = data.get("steps", None)

    # Implementation copied from original app.py generate_fsm logic so behavior doesn't change:
    if steps is None:
        # default behavior: run for len(r1)*len(r2)*len(r3) steps if possible
        if r1 and r2 and r3:
            steps = len(r1) * len(r2) * len(r3)
        else:
            steps = max(len(r1), len(r2), len(r3))

    b_prev = b_minus1 & 1
    c_prev = c_minus1 & 1

    idx1 = 0
    idx2 = -1
    idx3 = -1
    fsm = []

    for _ in range(int(steps)):
        a = r1[idx1]

        if a == 1:
            idx2 += 1
            if idx2 >= len(r2):
                idx2 = 0
            b_prev = r2[idx2]
        else:
            idx3 += 1
            if idx3 >= len(r3):
                idx3 = 0
            c_prev = r3[idx3]

        fsm.append(b_prev ^ c_prev)
        idx1 += 1
        if idx1 >= len(r1):
            idx1 = 0

    stats = {
        "steps": steps,
        "real_period": steps,
        "theoretical_period": len(r1) * len(r2) * len(r3) if (r1 and r2 and r3) else None,
        "r1_index": idx1,
        "r2_index": idx2,
        "r3_index": idx3,
        "ones": sum(fsm),
        "zeros": int(steps) - sum(fsm)
    }
    return fsm, stats

# ----------------------------
# NEW endpoint: 2-LFSR FSM
# ----------------------------
@app.route("/run_fsm_2lfsr", methods=["POST"])
def api_run_fsm_2lfsr():
    """
    Expected JSON:
    {
      "r1": [...],   # list of bits (outputs from LFSR1)
      "r2": [...],   # list of bits (outputs from LFSR2)
      "steps": optional int
    }
    Behavior: uses generate_fsm_2lfsr from FSM2LSFROnMachine.py (inlined above)
    """
    data = request.get_json()
    r1 = data.get("r1", [])
    r2 = data.get("r2", [])
    steps = data.get("steps", None)

    # call in-file function (exact same algorithm as your helper file)
    fsm_out = generate_fsm_2lfsr(r1, r2, steps=steps)

    # produce minimal stats for frontend convenience
    stats = {
        "output_length": len(fsm_out),
        "theoretical_period": len(r1) * len(r2) if len(r1) and len(r2) else None
    }

    return jsonify({"fsm": fsm_out, "stats": stats})

# ----------------------------
# NEW endpoint: message decryption / LFSR word decipher
# ----------------------------
@app.route("/ms_decryption", methods=["POST"])
def api_ms_decryption():
    """
    Expected JSON:
    {
      "cipher_bits": [0,1,1,0,...],          # optional; if omitted, backend default is used
      "keys": [[...], [...], ...],           # optional; if omitted, backend default keys are used
      "dictionary": [...],                   # optional list of words for scoring
    }

    Returns:
    {
      "per_key": [
         {"key_index": 1, "key": [...], "decoded_text": "...", "score": N},
         ...
      ],
      "best": {"key_index": K, "decoded_text": "...", "score":N}
    }
    """
    data = request.get_json() or {}

    # optional payload values
    cipher_bits = data.get("cipher_bits", None)
    keys = data.get("keys", None)
    dictionary = data.get("dictionary", DEFAULT_DICTIONARY)

    # If user didn't supply cipher_bits/keys, fall back to the defaults from the original module.
    if cipher_bits is None:
        # default cipher (copied small ciphertext from original LFSRwordDeCipher)
        cipher_bits = [
            1,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,1,0,0,1,1,
            1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0
        ]

    if keys is None:
        # default 5 keys (copied from original LFSRwordDeCipher file)
        keys = [
            [1,0,1,0,1,1,1,1,0,0,0,1,0,0,1],
            [0,1,0,1,1,1,1,0,0,0,1,0,0,1,1],
            [1,0,1,1,1,1,0,0,0,1,0,0,1,1,0],
            [0,1,1,1,1,0,0,0,1,0,0,1,1,0,1],
            [1,1,1,1,0,0,0,1,0,0,1,1,0,1,0]
        ]

    # process each key using the same steps as the original script:
    per_key_results = []
    best_score = -1
    best_text = ""
    best_index = None

    for i, key in enumerate(keys, start=1):
        key_expanded = repeat_to_length_simple(key, len(cipher_bits))
        plain_bits = xor_simple(cipher_bits, key_expanded)
        text = bits_to_text_simple(plain_bits)
        score = score_text_with_dictionary(text, dictionary)

        per_key_results.append({
            "key_index": i,
            "key": key,
            "decoded_text": text,
            "score": score
        })

        if score > best_score:
            best_score = score
            best_text = text
            best_index = i

    result = {
        "per_key": per_key_results,
        "best": {
            "key_index": best_index,
            "decoded_text": best_text,
            "score": best_score
        }
    }

    return jsonify(result)

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
# ---------- END original app.py ----------
