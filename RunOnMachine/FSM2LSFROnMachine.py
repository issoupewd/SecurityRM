import math

# ---------- Python LFSR logic ----------

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

        # if we already saw this state → period found
        if key in seen:
            period = step - seen[key]
            return outputs, period, states

        # remember this state
        seen[key] = step
        states.append(tuple(state))

        # output = rightmost bit
        outputs.append(state[-1])

        # LFSR feedback + shift
        newbit = xor_bits_from_indices(state, taps)
        state = [newbit] + state[:-1]
        step += 1

        # safety (should not happen with small LFSRs)
        if step >= max_steps:
            return outputs, len(outputs), states


# ---------- FSM (2 LFSRs: R1, R2) ----------

def generate_fsm_2lfsr(r1_seq, r2_seq, steps=None):
    """
    FSM rule:
      - Both LFSRs are clocked in parallel.
      - If R1 output bit = 1 → FSM outputs R2 bit.
      - If R1 output bit = 0 → FSM outputs nothing (bit is ignored).
    """
    if steps is None:
        steps = len(r1_seq) * len(r2_seq)

    idx1 = 0  # pointer in r1_seq
    idx2 = 0  # pointer in r2_seq

    fsm = []

    for _ in range(int(steps)):
        a = r1_seq[idx1]
        b = r2_seq[idx2]

        if a == 1:
            fsm.append(b)   # only output when R1 = 1

        # advance R1 pointer with wrap
        idx1 += 1
        if idx1 >= len(r1_seq):
            idx1 = 0

        # advance R2 pointer with wrap
        idx2 += 1
        if idx2 >= len(r2_seq):
            idx2 = 0

    return fsm


# ============================================================
#               DEFAULT VALUES FOR EXO 1
# ============================================================

# Initial states from the statement:
# R1 has 3 cells: (s2, s1, s0) = (1, 0, 0)
R1_INIT = [0, 0, 1]

# R2 has 5 cells: (s4, s3, s2, s1, s0) = (0, 0, 1, 0, 1)
R2_INIT = [0, 0, 1, 0, 1]

# Taps (you can adjust if needed according to the PDF):
# (s0 + s2) mod 2 for R1 → indices [0, 2] if we index [s0, s1, s2]
R1_TAPS = [0, 2]

# (s0 + s2) or (s0 + s3) depending on the statement;
# here we put something, you can change it to match exactly:
R2_TAPS = [2, 4]   # change to [0, 3] if the correction says s0 + s3


# ============================================================
#               RUN LFSRs
# ============================================================

print("\n=== RUNNING LFSRs ===\n")

r1_out, r1_period, r1_states = generate_lfsr_sequence(R1_INIT, R1_TAPS)
r2_out, r2_period, r2_states = generate_lfsr_sequence(R2_INIT, R2_TAPS)

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

# ============================================================
#               RUN FSM (2 LFSRs)
# ============================================================

print("\n=== RUNNING FSM (2 LFSRs) ===\n")

fsm_out = generate_fsm_2lfsr(r1_out, r2_out)

print("FSM output length:", len(fsm_out))
print("FSM output (all bits):", fsm_out)
print("First 25 FSM bits:", fsm_out[:25])

# Save FSM output to a text file
with open("FSMex01.txt", "w") as f:
    f.write(str(fsm_out))

print("\nFSM keystream saved to FSM_ex1.txt")
