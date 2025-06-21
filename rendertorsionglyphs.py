
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sklearn.decomposition import PCA

def rendertorsionglyphs(Phi_evo, loop_indices, curvature_magnitude, Lambda_fn):
    '''
    Visualizes Φ evolution as a 3D torsion glyph field.

    Parameters:
    - Phi_evo: [steps+1, X] array of Φ(x, t)
    - loop_indices: list of (t1, t2) recursion pairs
    - curvature_magnitude: [steps+1] array of ∥∂²Φ/∂τ²∥ values
    - Lambda_fn(t): function mapping τ to entropy suppression coefficient
    '''

    steps, X = Phi_evo.shape
    τ = np.arange(steps)

    # Compute coherence gradient dΦ/dτ (Z axis)
    dPhi_dt = np.gradient(Phi_evo, axis=0)

    # Use PCA for semantic drift axis (X axis)
    pca = PCA(n_components=1)
    phi_phase = pca.fit_transform(Phi_evo)[:, 0]

    # Create 3D plot
    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Normalize Lambda for colormap
    Lambda_vals = np.array([Lambda_fn(t) for t in τ])
    norm = plt.Normalize(vmin=np.min(Lambda_vals), vmax=np.max(Lambda_vals))
    color_map = cm.plasma(norm(Lambda_vals))

    # Plot agent trajectories
    for i in range(X):
        z = dPhi_dt[:, i]
        y = τ
        x = phi_phase  # same for all in proto; refine later per agent

        ax.plot(x, y, z, color='grey', alpha=0.3)

    # Highlight recursive loops
    for (t1, t2) in loop_indices:
        ax.plot([phi_phase[t1], phi_phase[t2]],
                [τ[t1], τ[t2]],
                [np.mean(dPhi_dt[t1]), np.mean(dPhi_dt[t2])],
                color='red', lw=2.5, linestyle='--', label='Loop' if (t1, t2)==loop_indices[0] else "")

    # Curvature flares
    spike_indices = np.where(curvature_magnitude > np.percentile(curvature_magnitude, 95))[0]
    for t in spike_indices:
        ax.scatter(phi_phase[t], τ[t], np.mean(dPhi_dt[t]), color='yellow', s=40, edgecolor='black')

    ax.set_xlabel("Φ Phase Offset")
    ax.set_ylabel("τ (Time)")
    ax.set_zlabel("∂Φ/∂τ (Gradient)")
    ax.set_title("🧠 Torsion Glyph Manifold: Recursive Simulation Field")

    plt.tight_layout()
    plt.show()
