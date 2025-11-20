import math


# ---------- Python LFSR & FSM logic ----------

def xor_bits_from_indices(state, indices):
    v = 0
    for i in indices:
        v ^= state[i]
    return v


def generate_lfsr_sequence(init_state, taps, max_steps=1 << 20):
    """Return (outputs_list, period, states_list) until first repeated state."""
    state = list(init_state)
    seen = {}
    outputs = []
    states = []
    step = 0

    while True:
        key = tuple(state)

        if key in seen:  # a previous state repeated → period found
            period = step - seen[key]
            return outputs, period, states

        seen[key] = step
        states.append(tuple(state))
        outputs.append(state[-1])  # output is RIGHTMOST bit

        newbit = xor_bits_from_indices(state, taps)
        state = [newbit] + state[:-1]
        step += 1

        if step >= max_steps:
            return outputs, len(outputs), states


def generate_fsm(r1_seq, r2_seq, r3_seq, b_minus1=0, c_minus1=0, steps=None):
    """Generate FSM alternating-step sequence."""

    if steps is None:
        steps = len(r1_seq) * len(r2_seq) * len(r3_seq)

    b_prev = int(b_minus1) & 1
    c_prev = int(c_minus1) & 1

    idx1 = 0
    idx2 = -1
    idx3 = -1

    fsm = []

    for j in range(int(steps)):

        # R1 controls FSM
        a = r1_seq[idx1]

        if a == 1:
            idx2 += 1
            if idx2 >= len(r2_seq):
                idx2 = 0
            b_prev = r2_seq[idx2]
        else:
            idx3 += 1
            if idx3 >= len(r3_seq):
                idx3 = 0
            c_prev = r3_seq[idx3]

        fsm_bit = b_prev ^ c_prev
        fsm.append(fsm_bit)

        idx1 += 1
        if idx1 >= len(r1_seq):
            idx1 = 0  # wrap around

    stats = {
        "steps": int(steps),
        "ones": sum(fsm),
        "zeros": int(steps) - sum(fsm)
    }

    return fsm, stats


# ============================================================
#               DEFAULT VALUES (no frontend)
# ============================================================

# Initial states:
R1_INIT = [0, 0, 1]
R2_INIT = [1, 0, 1, 1]
R3_INIT = [0, 1, 0, 0, 1]

# Taps:
R1_TAPS = [0, 2]
R2_TAPS = [0, 1]
R3_TAPS = [0, 1, 2, 4]

# ============================================================
#               RUN LFSRs
# ============================================================

print("\n=== RUNNING LFSRs ===\n")

r1_out, r1_period, r1_states = generate_lfsr_sequence(R1_INIT, R1_TAPS)
r2_out, r2_period, r2_states = generate_lfsr_sequence(R2_INIT, R2_TAPS)
r3_out, r3_period, r3_states = generate_lfsr_sequence(R3_INIT, R3_TAPS)

print("R1 period:", r1_period)
print("R1 outputs:", r1_out)
print("R1 states:")
for i, s in enumerate(r1_states):
    print(" ", i, ":", s)

print("\nR2 period:", r2_period)
print("R2 outputs:", r2_out)
print("R2 states:")
for i, s in enumerate(r2_states):
    print(" ", i, ":", s)

print("\nR3 period:", r3_period)
print("R3 outputs:", r3_out)
print("R3 states:")
for i, s in enumerate(r3_states):
    print(" ", i, ":", s)

# ============================================================
#               RUN FSM
# ============================================================

print("\n=== RUNNING FSM ===\n")

fsm_out, fsm_stats = generate_fsm(r1_out, r2_out, r3_out)

print("FSM stats:")
for k, v in fsm_stats.items():
    print(" ", k, ":", v)

print("\nFSM output:")
print(fsm_out)

print("\nFSM output length:", len(fsm_out))


# Save FSM output to a text file
with open("FSMexo4.txt", "w") as f:
    f.write(str(fsm_out))

