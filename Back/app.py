from flask import Flask, request, jsonify
from flask_cors import CORS

# Create Flask backend application
app = Flask(__name__)

# Enable CORS so that a frontend (React/Next.js) can call this backend
CORS(app)

# -------------------------------------------------------
# LFSR UTILITIES
# -------------------------------------------------------

def xor_bits_from_indices(state, indices):
    """Compute XOR of selected tap positions."""
    v = 0                     # accumulator for XOR result
    for i in indices:         # iterate through each tap index        
            v ^= (state[i] )   # XOR with bit at that index
    return v                   # return XOR result


def generate_lfsr_sequence(init_state, taps, max_steps=1 << 20):
    """
    Generate LFSR states until first repeated state.
    Returns: outputs, period, states
    """
    state = list(init_state)   # make a working copy of the initial LFSR state
    seen = {}                  # dictionary to detect when a state repeats
    outputs = []               # list of output bits
    states = []                # list of all visited states

    step = 0                   # iteration counter
    while True:
        key = tuple(state)     # convert state list → tuple so it's hashable
        if key in seen:        # if we have seen this exact state before
            period = step - seen[key]   # period = distance between repeats
            return outputs, period, states

        seen[key] = step       # mark this state as visited at this step
        states.append(state.copy())  # store a copy of current state
        outputs.append(state[-1])    # output = RIGHTMOST bit

        newbit = xor_bits_from_indices(state, taps)  # compute feedback bit
        state = [newbit] + state[:-1]                # shift right with feedback
        step += 1                                     # increment step counter

        if step >= max_steps:      # failsafe to avoid infinite loop
            return outputs, len(outputs), states


# -------------------------------------------------------
# FSM GENERATION
# -------------------------------------------------------

def generate_fsm(r1_seq, r2_seq, r3_seq, b_minus1=0, c_minus1=0, steps=None):
    """Generate FSM output and stats (real period = steps)."""

    # If no "steps" provided → run for full theoretical length
    if steps is None:
        steps = len(r1_seq) * len(r2_seq) * len(r3_seq)

    b_prev = b_minus1 & 1   # previous R2 output (initial b(-1))
    c_prev = c_minus1 & 1   # previous R3 output (initial c(-1))

    idx1 = 0                # index pointer for R1 sequence
    idx2 = -1               # index pointer for R2 sequence
    idx3 = -1               # index pointer for R3 sequence

    fsm = []                # stores resulting keystream bits

    for _ in range(steps):  # for each FSM step
        a = r1_seq[idx1 ]   # get R1 output (controls R2/R3)

        if a == 1:                        # If R1 outputs 1 → clock R2
            idx2 += 1
            if idx2 >= len(r2_seq):
             idx2 = 0  # wrap around
            b_prev = r2_seq[idx2 ]
        else:                             # If R1 outputs 0 → clock R3
            idx3 += 1
            if idx3 >= len(r3_seq):
             idx3 = 0  # wrap around
            c_prev = r3_seq[idx3 ]

        fsm.append(b_prev ^ c_prev)       # FSM output = b XOR c
        idx1 += 1
        if idx1 >= len(r1_seq):
            idx1 = 0  # wrap around

    # build statistics dictionary
    stats = {
        "steps": steps,                                      # real executed steps
        "real_period": steps,                                # real period = steps
        "theoretical_period": len(r1_seq) * len(r2_seq) * len(r3_seq),
        "r1_index": idx1,
        "r2_index": idx2,
        "r3_index": idx3,
        "ones": sum(fsm),                                     # count of 1-bits
        "zeros": steps - sum(fsm)                             # count of 0-bits
    }

    return fsm, stats


# -------------------------------------------------------
# API ROUTES
# -------------------------------------------------------

@app.route("/generate_lfsr", methods=["POST"])
def api_generate_lfsr():
    # parse JSON sent from frontend
    data = request.get_json()

    # run LFSR generator
    outputs, period, states = generate_lfsr_sequence(
        data["init_state"],
        data["taps"]
    )

    # return results as JSON
    return jsonify({
        "outputs": outputs,
        "period": period,
        "states": states,
        "theoretical_period": 2 ** len(data["init_state"]) - 1    # optional
    })


@app.route("/run_fsm", methods=["POST"])
def api_run_fsm():
    # parse request
    data = request.get_json()

    # run FSM
    fsm, stats = generate_fsm(
        data["r1"],
        data["r2"],
        data["r3"],
        data.get("b_minus1", 0),
        data.get("c_minus1", 0),
        data.get("steps")
    )
    return jsonify({"fsm": fsm, "stats": stats})  # return output + stats


# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------

if __name__ == "__main__":
    # start Flask backend on port 5000
    app.run(port=5000, debug=True)
