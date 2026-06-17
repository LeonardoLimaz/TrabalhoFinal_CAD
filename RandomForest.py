import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score

import warnings
warnings.filterwarnings("ignore")

# ─── Dataset configuration ────────────────────────────────────────────────────
DATASETS = {
    "yeast": {
        "multiclass": True,
        "versions": {
            "original": "dataset/yeast.csv",
            "python":   "dataset/yeast_reduzido_python_seed42.csv",
            "c":        "dataset/yeast_reduzido_c_seed42.csv",
            "cuda":     "dataset/yeast_reduzido_cuda_seed42.csv",
        },
    },
    "optdigits": {
        "multiclass": True,
        "versions": {
            "original": "dataset/optdigits_csv.csv",
            "c":        "dataset/optdigits_reduzido_c_seed42.csv",
            "cuda":     "dataset/optdigits_reduzido_cuda_seed42.csv",
        },
    },
    "vh_data15": {
        "multiclass": False,
        "versions": {
            "original": "dataset/vh_data15.csv",
            "c":        "dataset/vh_data15_reduzido_c_seed42.csv",
            "cuda":     "dataset/vh_data15_reduzido_cuda_seed42.csv",
        },
    },
}

# ─── Main loop ────────────────────────────────────────────────────────────────
all_results = []

for dataset_name, config in DATASETS.items():
    is_multiclass = config["multiclass"]
    output_dir = os.path.join("resultados", dataset_name)
    os.makedirs(output_dir, exist_ok=True)

    dataset_results = []

    if not is_multiclass:
        plt.figure()

    for version_name, path in config["versions"].items():
        data = pd.read_csv(path)
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        # encode string targets
        if y.dtype == object or str(y.dtype) == "str":
            y = LabelEncoder().fit_transform(y)

        X_train, X_valid, y_train, y_valid = train_test_split(
            X, y, test_size=0.25, random_state=0
        )

        # auto-detect column types
        categorical_cols = X_train.select_dtypes(exclude="number").columns.tolist()
        numerical_cols   = X_train.select_dtypes(include="number").columns.tolist()

        transformers = []
        if categorical_cols:
            transformers.append(("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-1), categorical_cols))
        if numerical_cols:
            transformers.append(("num", "passthrough", numerical_cols))

        model = make_pipeline(
            ColumnTransformer(transformers=transformers),
            RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0),
        )

        model.fit(X_train, y_train)
        y_pred       = model.predict(X_valid)
        y_pred_proba = model.predict_proba(X_valid)

        accuracy = accuracy_score(y_valid, y_pred)

        if is_multiclass:
            auc = None
        else:
            auc = roc_auc_score(y_valid, y_pred_proba[:, 1])
            fpr, tpr, _ = roc_curve(y_valid, y_pred_proba[:, 1])
            plt.plot(fpr, tpr, label=f"{version_name} (AUC={auc:.3f})")

        row = {
            "dataset":   dataset_name,
            "version":   version_name,
            "n_samples": len(data),
            "accuracy":  round(accuracy, 4),
            "auc":       round(auc, 4) if auc is not None else None,
        }
        dataset_results.append(row)
        all_results.append(row)

        auc_str = f"auc={auc:.3f}" if auc is not None else "auc=N/A"
        print(f"{dataset_name:12} | {version_name:8} | n={len(data):5} | acc={accuracy:.3f} | {auc_str}")

    # ROC curve — only for binary datasets
    if not is_multiclass:
        plt.title(f"Curva ROC — {dataset_name}")
        plt.xlabel("Taxa de Falsos Positivos")
        plt.ylabel("Taxa de Verdadeiros Positivos")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "roc_comparison.png"))
        plt.close()

    pd.DataFrame(dataset_results).to_csv(
        os.path.join(output_dir, "metricas.csv"), index=False
    )

# ─── Consolidated comparison ──────────────────────────────────────────────────
results_df = pd.DataFrame(all_results)

# compute accuracy delta relative to original
originals = results_df[results_df["version"] == "original"].set_index("dataset")["accuracy"]
results_df["delta"] = results_df.apply(
    lambda r: r["accuracy"] - originals[r["dataset"]], axis=1
)
reduced_df = results_df[~results_df["version"].isin(["original", "python"])]

colors = {"c": "#DD8452", "cuda": "#4C72B0"}

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# ── Delta chart ───────────────────────────────────────────────────────────────
for version, group in reduced_df.groupby("version"):
    axes[0].bar(
        [d + f"\n({version})" for d in group["dataset"]],
        group["delta"],
        color=colors.get(version, "gray"),
        label=version,
    )
axes[0].axhline(0, color="black", linewidth=0.8, linestyle="--")
axes[0].set_title("Delta de Acurácia vs Original")
axes[0].set_ylabel("Δ acurácia (reduzido − original)")
axes[0].set_xlabel("Dataset / Versão")
axes[0].legend(title="Versão")
axes[0].tick_params(axis="x", rotation=30)

# ── Line chart: accuracy per version ─────────────────────────────────────────
version_order = ["original", "c", "cuda"]
palette = {"yeast": "#C94040", "optdigits": "#55A868", "vh_data15": "#7A5C99"}
offsets = {"optdigits": 8, "vh_data15": -14, "yeast": 8}

for ds_name, group in results_df.groupby("dataset"):
    group = group.set_index("version").reindex([v for v in version_order if v in group["version"].values])
    axes[1].plot(
        group.index, group["accuracy"],
        marker="o", label=ds_name,
        color=palette.get(ds_name, "gray"), linewidth=2, markersize=7,
    )
    for version, row in group.iterrows():
        axes[1].annotate(
            f"n={int(row['n_samples'])}",
            (version, row["accuracy"]),
            textcoords="offset points",
            xytext=(0, offsets.get(ds_name, 8)),
            fontsize=7, ha="center",
            color=palette.get(ds_name, "gray"),
            annotation_clip=False,
        )

axes[1].set_title("Acurácia por Versão")
axes[1].set_xlabel("Versão")
axes[1].set_ylabel("Acurácia")
axes[1].legend(title="Dataset")
axes[1].grid(True, linestyle="--", alpha=0.4)
axes[1].margins(x=0.15)

plt.suptitle("Original vs Reduzido — Comparação Random Forest")
plt.tight_layout()
plt.savefig("resultados/comparacao_geral.png", bbox_inches="tight")
plt.close()

results_df.to_csv("resultados/metricas_geral.csv", index=False)
print("\nDone. Results saved in 'resultados/'.")
