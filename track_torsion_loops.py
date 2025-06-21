
import numpy as np

def track_torsion_loops(Phi_evolution, tau_window=5, threshold=1e-3):
    '''
    Tracks torsion loops — recursive return to prior epistemic states.

    Parameters:
    - Phi_evolution: [steps+1, X] array of Φ(x, t)
    - tau_window: int, minimum τ separation between states to compare
    - threshold: float, L2 distance below which states are considered recursively similar

    Returns:
    - loop_indices: list of (t1, t2) tuples where recursion detected
    '''
    steps, X = Phi_evolution.shape
    loop_indices = []

    for t1 in range(steps - tau_window):
        for t2 in range(t1 + tau_window, steps):
            dist = np.linalg.norm(Phi_evolution[t1] - Phi_evolution[t2])
            if dist < threshold:
                loop_indices.append((t1, t2))

    return loop_indices
