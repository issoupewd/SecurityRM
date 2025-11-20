from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------
# LFSR UTILITIES
# -------------------------------------------------------

def xor_bits_from_indices(state, indices):
    """Compute XOR of selected tap positions."""
    v = 0
    for i in indices:
        if 0 <= i < len(state):
            v ^= (state[i] & 1)
    return v


def generate_lfsr_sequence(init_state, taps, max_steps=1 << 20):
    """
    Generate LFSR states until first repeated state.
    Returns: outputs, period, states
    """
    state = list(init_state)
    seen = {}
    outputs = []
    states = []

    step = 0
    while True:
        key = tuple(state)
        if key in seen:
            period = step - seen[key]
            return outputs, period, states

        seen[key] = step
        states.append(state.copy())
        outputs.append(state[-1])   # RIGHTMOST bit

        newbit = xor_bits_from_indices(state, taps)
        state = [newbit] + state[:-1]
        step += 1

        if step >= max_steps:
            return outputs, len(outputs), states


# -------------------------------------------------------
# FSM GENERATION
# -------------------------------------------------------

def generate_fsm(r1_seq, r2_seq, r3_seq, b_minus1=0, c_minus1=0, steps=None):
    """Generate FSM output and stats (real period = steps)."""

    # If no steps provided → real-length based execution
    if steps is None:
        steps = len(r1_seq) * len(r2_seq) * len(r3_seq)

    b_prev = b_minus1 & 1
    c_prev = c_minus1 & 1

    idx1 = 0
    idx2 = -1
    idx3 = -1

    fsm = []

    for _ in range(steps):
        a = r1_seq[idx1 % len(r1_seq)]

        if a == 1:
            idx2 += 1
            b_prev = r2_seq[idx2 % len(r2_seq)]
        else:
            idx3 += 1
            c_prev = r3_seq[idx3 % len(r3_seq)]

        fsm.append(b_prev ^ c_prev)
        idx1 += 1

    stats = {
        "steps": steps,
        "real_period": steps,          # <-- REAL PERIOD
        "theoretical_period": len(r1_seq) * len(r2_seq) * len(r3_seq),
        "r1_index": idx1,
        "r2_index": idx2,
        "r3_index": idx3,
        "ones": sum(fsm),
        "zeros": steps - sum(fsm)
    }

    return fsm, stats


# -------------------------------------------------------
# API ROUTES
# -------------------------------------------------------

@app.route("/generate_lfsr", methods=["POST"])
def api_generate_lfsr():
    data = request.get_json()
    outputs, period, states = generate_lfsr_sequence(
        data["init_state"],
        data["taps"]
    )
    return jsonify({
        "outputs": outputs,
        "period": period,
        "states": states,
        "theoretical_period": 2 ** len(data["init_state"]) - 1    # optional
    })


@app.route("/run_fsm", methods=["POST"])
def api_run_fsm():
    data = request.get_json()
    fsm, stats = generate_fsm(
        data["r1"],
        data["r2"],
        data["r3"],
        data.get("b_minus1", 0),
        data.get("c_minus1", 0),
        data.get("steps")
    )
    return jsonify({"fsm": fsm, "stats": stats})


# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)
