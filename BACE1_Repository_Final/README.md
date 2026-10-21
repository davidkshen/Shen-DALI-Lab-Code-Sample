# BACE1 activity prediction

An exploratory research notebook comparing molecular fingerprints, docking-derived energy/interaction features, and their combination for predicting BACE1-associated activity. The analysis includes data alignment, feature selection, regression comparisons, and interpretation through heatmaps, violin plots, prediction plots, and SHAP analyses.

[View the notebook](notebooks/BACE1_PDB_pIC50.ipynb).

## Process

Existing SMILES strings and molecule identifiers are exported to `.smi` files for PaDEL fingerprint generation. Each molecule becomes a row in a feature matrix; fingerprint columns encode structural patterns. Generated features are matched to activity records by identifier because descriptor generation can reorder or omit records.

The notebook explores low-variance filtering, standardized Ridge-based feature ranking, and selection frequency across repeated 80/20 splits to reduce the input feature set. It then compares docking-only, selected-fingerprint-only, and combined inputs using regressors including NuSVR, random forests, ExtraTrees, and gradient boosting. Performance is summarized using mean R² and standard deviation across repeated evaluations. Docking features were supplied by my mentor; their simulation is not implemented here.

## Results from my research poster

![Regression model comparison presented in my research poster](assets/poster_results.png)

The table reports mean R² (standard deviation) from the original poster experiments. NuSVR with combined features achieved the highest reported mean R² of **0.60 (SD 0.09)**. These are previously presented results; the private analysis was not rerun when preparing this public copy.

## Dependencies

Python/Jupyter; NumPy, pandas, SciPy, scikit-learn, matplotlib, seaborn, and NetworkX. Optional branches use LazyPredict, XGBoost, LightGBM, SHAP, and mlxtend. Fingerprint generation requires Java and PaDEL-Descriptor. See [requirements.txt](requirements.txt) and [requirements-optional.txt](requirements-optional.txt); historical APIs may require compatible versions.

## Data and attribution

The lab datasets and original saved notebook outputs are withheld; private feature selections are redacted. Reproduction requires authorized inputs. The notebook retains alternative exploratory branches.

The fingerprint workflow draws on the [Data Professor tutorial](https://github.com/dataprofessor/bioinformatics). Public-copy preparation and the synthetic previews below were AI-assisted.

## Synthetic visualization previews

These illustrate the plotting styles using randomly generated values. They are **not research results**.

![Synthetic fingerprint heatmap](assets/synthetic_fingerprint_heatmap.png)

![Synthetic model-comparison violin plots](assets/synthetic_model_violin.png)
