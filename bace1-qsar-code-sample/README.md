# BACE1 activity prediction

An exploratory notebook using molecular fingerprints and docking-derived energy/interaction features to predict BACE1-associated activity. It exports existing **SMILES** strings to `.smi` files for PaDEL, aligns the resulting descriptors with activity records by molecule identifier, prepares activity targets, selects features, and compares regression methods, including random forests, support-vector models and a LazyPredict benchmark with a neural network. Heatmaps, violin plots, prediction plots and SHAP analyses support interpretation.

**Dependencies:** Python/Jupyter; NumPy, pandas, SciPy, scikit-learn, matplotlib, seaborn and NetworkX. Optional branches use LazyPredict, XGBoost, LightGBM, SHAP and mlxtend. Fingerprint generation requires Java and PaDEL-Descriptor. See `requirements.txt` and `requirements-optional.txt`; historical APIs may require compatible versions.

**Data:** Lab datasets and saved research outputs are withheld. Private feature selections are redacted. Reproduction requires authorized inputs; the notebook contains alternative exploratory branches.

The fingerprint workflow draws on the [Data Professor tutorial](https://github.com/dataprofessor/bioinformatics). Previews below are only dummy so as to contain any proprietary information that belongs to me old lab. However, appearance-wise, it is still a demonstration of what was on my publications and demonstrates what the outputs appear as. 

## Visualization examples

Synthetic illustrations of the plotting styles, generated from random values. These are **not research results**.

![Synthetic fingerprint heatmap](assets/synthetic_fingerprint_heatmap.png)

![Synthetic model-comparison violin plots](assets/synthetic_model_violin.png)
