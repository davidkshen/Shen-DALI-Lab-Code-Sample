"""Render clearly labeled synthetic previews; does not read or train on lab data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(20261020)
sns.set_theme(style="whitegrid", font_scale=1.0)

# Illustration of the per-molecule, per-feature matrix layout, not real chemistry.
fingerprints = rng.integers(0, 2, size=(16, 14))
fig, ax = plt.subplots(figsize=(10, 6.5), constrained_layout=True)
sns.heatmap(
    fingerprints, ax=ax, cmap=sns.color_palette(["#eef4f5", "#156b78"]),
    vmin=0, vmax=1, linewidths=.6, linecolor="white",
    xticklabels=[f"F{i:02d}" for i in range(1, 15)],
    yticklabels=[f"Example {i:02d}" for i in range(1, 17)],
    cbar_kws={"ticks": [0, 1], "label": "Synthetic structural-feature flag"},
)
ax.set_xlabel("Illustrative fingerprint feature")
ax.set_ylabel("Dummy molecule label")
ax.set_title("SYNTHETIC EXAMPLE | Fingerprint heatmap\nRandom binary flags; no lab compounds or measurements", pad=15)
ax.tick_params(axis="y", rotation=0)
fig.savefig(OUT / "synthetic_fingerprint_heatmap.png", dpi=170)
plt.close(fig)

# All groups share the same generating distribution: no implied true ranking.
rows = []
for method in ["Random forest", "SVR", "MLP"]:
    for feature_set in ["Fingerprints", "Docking terms", "Combined"]:
        for value in rng.normal(.5, .16, 60):
            rows.append({"Method": method, "Inputs": feature_set, "Score": float(value)})
frame = pd.DataFrame(rows)
fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
sns.violinplot(
    data=frame, x="Method", y="Score", hue="Inputs", ax=ax,
    palette=["#16798a", "#dfa34b", "#86689f"], cut=0, inner="quartile",
)
ax.set_title("SYNTHETIC EXAMPLE | Model-comparison violin plots\nRandomly generated scores; no models trained", pad=15)
ax.set_xlabel("Illustrative model family")
ax.set_ylabel("Illustrative score (random values)")
ax.legend(title="Illustrative feature set", loc="upper center", bbox_to_anchor=(.5, -.18), ncol=3, frameon=False)
fig.savefig(OUT / "synthetic_model_violin.png", dpi=170)
plt.close(fig)
print("Created two synthetic previews; no research inputs were read.")
