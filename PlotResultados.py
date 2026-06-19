"""
Lê resultados/metricas_geral.csv (gerado por train_rf.py) e produz:
  acuracia_absoluta.png  — barras de acurácia absoluta por versão
  acuracia_relativa.png  — linhas de acurácia relativa ao original
  amostras_por_versao.png — barras de nº de amostras por versão

Narrativa central: redução de ~50% das amostras com perda mínima de acurácia.
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─── Constantes ───────────────────────────────────────────────────────────────
VERSION_ORDER  = ["original", "python", "c", "cuda"]
VERSION_COLORS = {
    "original": "#888888",
    "python":   "#55A868",
    "c":        "#DD8452",
    "cuda":     "#4C72B0",
}
DS_PALETTE = {
    "yeast":      "#C94040",
    "optdigits":  "#17A589",
    "vh_data15":  "#7A5C99",
    "covtype":    "#D4A017",
    "weatherAUS": "#2196A6",
}
DATASETS_ORDER = ["yeast", "optdigits", "vh_data15", "covtype", "weatherAUS"]

# ─── Leitura e validação ──────────────────────────────────────────────────────
CSV_PATH = "resultados/metricas_geral.csv"
if not os.path.exists(CSV_PATH):
    sys.exit(f"[ERRO] '{CSV_PATH}' não encontrado. Execute train_rf.py primeiro.")

results_df    = pd.read_csv(CSV_PATH)
datasets_list = [d for d in DATASETS_ORDER if d in results_df["dataset"].values]

if not datasets_list:
    sys.exit("[ERRO] Nenhum dataset reconhecido no CSV.")

originals    = results_df[results_df["version"] == "original"].set_index("dataset")["accuracy"]
all_versions = [v for v in VERSION_ORDER if v in results_df["version"].values]
has_std = "accuracy_std" in results_df.columns
has_f1  = "f1" in results_df.columns

os.makedirs("resultados", exist_ok=True)

x     = np.arange(len(datasets_list))
n_ver = len(all_versions)
width = 0.18

# ═══════════════════════════════════════════════════════════════════════════════
# Figura 1 — Acurácia absoluta (barras)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))

for i, version in enumerate(all_versions):
    grp = (results_df[results_df["version"] == version]
           .set_index("dataset").reindex(datasets_list))
    acc_vals = grp["accuracy"].values.astype(float)

    std_vals = (grp["accuracy_std"].values.astype(float)
                if has_std else np.zeros(len(datasets_list)))

    bars = ax.bar(
        x + (i - n_ver / 2 + 0.5) * width,
        acc_vals, width,
        color=VERSION_COLORS.get(version, "gray"),
        label=version, zorder=3,
        edgecolor="white", linewidth=0.4,
        yerr=std_vals if has_std else None,
        capsize=3, error_kw={"elinewidth": 1.1, "ecolor": "black", "alpha": 0.7},
    )
    for rect, val, std in zip(bars, acc_vals, std_vals):
        if np.isnan(val):
            continue
        offset = (std if has_std else 0) + 0.008
        label  = f"{val:.3f}±{std:.3f}" if has_std else f"{val:.3f}"
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            val + offset,
            label,
            ha="center", va="bottom",
            fontsize=5, color="black", rotation=90,
        )

ax.set_ylim(0, 1.12)
ax.set_title("Acurácia Absoluta por Versão — Random Forest (seed 42)", fontsize=12)
ax.set_ylabel("Acurácia")
ax.set_xlabel("Dataset")
ax.set_xticks(x)
ax.set_xticklabels(datasets_list, rotation=20, ha="right")
ax.legend(title="Versão", fontsize=8.5)
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
plt.tight_layout()
plt.savefig("resultados/acuracia_absoluta.png", dpi=150, bbox_inches="tight")
plt.close()
print("Salvo: resultados/acuracia_absoluta.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Figura 2 — Acurácia relativa ao original (linhas)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))

for ds_name in datasets_list:
    orig_acc = originals.get(ds_name, np.nan)
    if np.isnan(orig_acc):
        continue
    ds_rows   = results_df[results_df["dataset"] == ds_name]
    color     = DS_PALETTE.get(ds_name, "gray")
    vers_pres = [v for v in all_versions if v in ds_rows["version"].values]
    x_coords  = [all_versions.index(v) for v in vers_pres]
    rel_accs  = [float(ds_rows[ds_rows["version"] == v]["accuracy"].iloc[0]) / orig_acc
                 for v in vers_pres]

    ax.plot(x_coords, rel_accs, color=color, marker="o",
            linewidth=2, markersize=7, label=ds_name, zorder=3)

ax.axhline(1.0, color="black", linewidth=0.9, linestyle="--", alpha=0.5)
ax.set_xlim(-0.5, len(all_versions) - 0.5)
ax.set_ylim(0.85, 1.05)
ax.set_xticks(range(len(all_versions)))
ax.set_xticklabels(all_versions)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
ax.set_title("Acurácia Relativa ao Original por Versão — Random Forest (seed 42)", fontsize=12)
ax.set_xlabel("Versão")
ax.set_ylabel("Acurácia / Acurácia Original")
ax.legend(title="Dataset", fontsize=8.5, loc="lower left", framealpha=0.9)
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("resultados/acuracia_relativa.png", dpi=150, bbox_inches="tight")
plt.close()
print("Salvo: resultados/acuracia_relativa.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Figura 3 — Número de amostras por versão (barras)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))

for i, version in enumerate(all_versions):
    grp = (results_df[results_df["version"] == version]
           .set_index("dataset").reindex(datasets_list))
    n_vals = grp["n_samples"].values.astype(float)

    bars = ax.bar(
        x + (i - n_ver / 2 + 0.5) * width,
        n_vals, width,
        color=VERSION_COLORS.get(version, "gray"),
        label=version, zorder=3,
        edgecolor="white", linewidth=0.4,
    )
    for rect, val in zip(bars, n_vals):
        if np.isnan(val):
            continue
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            val + ax.get_ylim()[1] * 0.01,
            f"{int(val)}",
            ha="center", va="bottom",
            fontsize=5.5, color="black", rotation=90,
        )

ax.set_title("Número de Amostras por Versão (seed 42)", fontsize=12)
ax.set_ylabel("Número de amostras")
ax.set_xlabel("Dataset")
ax.set_xticks(x)
ax.set_xticklabels(datasets_list, rotation=20, ha="right")
ax.legend(title="Versão", fontsize=8.5)
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
plt.tight_layout()
plt.savefig("resultados/amostras_por_versao.png", dpi=150, bbox_inches="tight")
plt.close()
print("Salvo: resultados/amostras_por_versao.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Figura 4 — F1-Score ponderado por versão (apenas se disponível no CSV)
# ═══════════════════════════════════════════════════════════════════════════════
if has_f1:
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, version in enumerate(all_versions):
        grp = (results_df[results_df["version"] == version]
               .set_index("dataset").reindex(datasets_list))
        f1_vals = grp["f1"].values.astype(float)

        bars = ax.bar(
            x + (i - n_ver / 2 + 0.5) * width,
            f1_vals, width,
            color=VERSION_COLORS.get(version, "gray"),
            label=version, zorder=3,
            edgecolor="white", linewidth=0.4,
        )
        for rect, val in zip(bars, f1_vals):
            if np.isnan(val):
                continue
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                val + 0.005,
                f"{val:.3f}",
                ha="center", va="bottom",
                fontsize=5.5, color="black", rotation=90,
            )

    ax.set_ylim(0, 1.12)
    ax.set_title("F1-Score Ponderado por Versão — Random Forest (seed 42)", fontsize=12)
    ax.set_ylabel("F1-Score (weighted)")
    ax.set_xlabel("Dataset")
    ax.set_xticks(x)
    ax.set_xticklabels(datasets_list, rotation=20, ha="right")
    ax.legend(title="Versão", fontsize=8.5)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    plt.tight_layout()
    plt.savefig("resultados/f1_por_versao.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Salvo: resultados/f1_por_versao.png")
else:
    print("[INFO] Coluna 'f1' não encontrada no CSV — execute RandomForest.py para gerar.")

print("\nPlots concluídos. Arquivos salvos em 'resultados/'.")
