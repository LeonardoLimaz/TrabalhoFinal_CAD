import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score

import warnings
warnings.filterwarnings("ignore")

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
            "python":   "dataset/optdigits_reduzido_python_seed42.csv",
            "c":        "dataset/optdigits_reduzido_c_seed42.csv",
            "cuda":     "dataset/optdigits_reduzido_cuda_seed42.csv",
        },
    },
    "vh_data15": {
        "multiclass": False,
        "versions": {
            "original": "dataset/vh_data15.csv",
            "python":   "dataset/vh_data15_reduzido_python_seed42.csv",
            "c":        "dataset/vh_data15_reduzido_c_seed42.csv",
            "cuda":     "dataset/vh_data15_reduzido_cuda_seed42.csv",
        },
    },
    "covtype": {
        "multiclass": True,
        "versions": {
            "original": "dataset/covtype_sample.csv",
            "python":   "dataset/covtype_reduzido_python_seed42.csv",
            "c":        "dataset/covtype_reduzido_c_seed42.csv",
            "cuda":     "dataset/covtype_reduzido_cuda_seed42.csv",
        },
    },
    "weatherAUS": {
        "multiclass": False,
        "versions": {
            "original": "dataset/weatherAUS_sample.csv",
            "python":   "dataset/weatherAUS_reduzido_python_seed42.csv",
            "c":        "dataset/weatherAUS_reduzido_c_seed42.csv",
            "cuda":     "dataset/weatherAUS_reduzido_cuda_seed42.csv",
        },
    },
}

VERSION_ORDER  = ["original", "python", "c", "cuda"]
VERSION_COLORS = {
    "original": "#888888",
    "python":   "#55A868",
    "c":        "#DD8452",
    "cuda":     "#4C72B0",
}



def build_model(X_train: pd.DataFrame) -> Pipeline:
    """
    Pipeline: pré-processamento → RandomForest.

    Colunas categóricas : OrdinalEncoder (desconhecidos → -1)
    Colunas numéricas   : SimpleImputer(mediana) + passthrough
                          → necessário para vh_data15, que tem NaN em 36 colunas
    max_depth=5         : conservador; análise de gap treino/validação mostrou
                          overfitting severo em yeast (gap +0.23) com depth=10
    """
    cat_cols = X_train.select_dtypes(exclude="number").columns.tolist()
    num_cols = X_train.select_dtypes(include="number").columns.tolist()

    transformers = []
    if cat_cols:
        transformers.append((
            "cat",
            OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1,
                encoded_missing_value=-1,
            ),
            cat_cols,
        ))
    if num_cols:
        transformers.append((
            "num",
            Pipeline([("imputer", SimpleImputer(strategy="median"))]),
            num_cols,
        ))

    return Pipeline([
        ("preprocessor", ColumnTransformer(transformers=transformers)),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=0,
        )),
    ])



all_results = []
binary_roc  = {}  

for dataset_name, config in DATASETS.items():
    is_multiclass = config["multiclass"]
    output_dir    = os.path.join("resultados", dataset_name)
    os.makedirs(output_dir, exist_ok=True)

    dataset_results = []
    n_original   = None   
    acc_original = None   

    for version_name, path in config["versions"].items():
        if not os.path.exists(path):
            print(f"[AVISO] Arquivo não encontrado, pulando: {path}")
            continue

        data = pd.read_csv(path)
        X    = data.iloc[:, :-1]
        y    = data.iloc[:, -1]

        
        if not pd.api.types.is_numeric_dtype(y):
            y = LabelEncoder().fit_transform(y)
        else:
            y = y.to_numpy()

        # stratify preserva proporção das classes no split
        # crítico para yeast (classe mínima 0.34%) e covtype (0.48%)
        X_train, X_valid, y_train, y_valid = train_test_split(
            X, y, test_size=0.25, random_state=0, stratify=y
        )

        model = build_model(X_train)
        model.fit(X_train, y_train)

        y_pred       = model.predict(X_valid)
        y_pred_proba = model.predict_proba(X_valid)
        accuracy     = accuracy_score(y_valid, y_pred)

        auc = None
        if not is_multiclass:
            auc = roc_auc_score(y_valid, y_pred_proba[:, 1])
            fpr, tpr, _ = roc_curve(y_valid, y_pred_proba[:, 1])
            binary_roc.setdefault(dataset_name, {})[version_name] = (fpr, tpr, auc)

        
        if version_name == "original":
            n_original   = len(data)
            acc_original = accuracy

       
        row = {
            "dataset":      dataset_name,
            "version":      version_name,
            "n_samples":    len(data),
            "n_treino":     len(X_train),
            "n_teste":      len(X_valid),
            "accuracy":     round(accuracy, 4),
            "auc":          round(auc, 4) if auc is not None else None,
            "delta":        round(accuracy - acc_original, 4) if acc_original is not None else None,
            "taxa_retencao": round(len(data) / n_original, 4) if n_original else None,
        }
        dataset_results.append(row)
        all_results.append(row)

        auc_str = f"auc={auc:.3f}" if auc is not None else "auc=N/A"
        print(f"{dataset_name:12} | {version_name:8} | n={len(data):6} | "
              f"acc={accuracy:.4f} | {auc_str}")

    
    pd.DataFrame(dataset_results).to_csv(
        os.path.join(output_dir, "metricas.csv"), index=False
    )


results_df = pd.DataFrame(all_results)
results_df.to_csv("resultados/metricas_geral.csv", index=False)
print("\nSalvo: resultados/metricas_geral.csv")


for ds_name, roc_data in binary_roc.items():
    fig, ax = plt.subplots(figsize=(7, 5))

    for version in VERSION_ORDER:
        if version not in roc_data:
            continue
        fpr, tpr, auc = roc_data[version]
        ax.plot(
            fpr, tpr,
            color=VERSION_COLORS[version],
            linestyle="--" if version == "original" else "-",
            linewidth=1.8,
            label=f"{version}  (AUC = {auc:.3f})",
        )

    ax.plot([0, 1], [0, 1], color="black", linestyle=":", linewidth=0.8,
            label="Aleatório (AUC = 0.500)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_title(f"Curva ROC — {ds_name}", fontsize=12)
    ax.set_xlabel("Taxa de Falsos Positivos")
    ax.set_ylabel("Taxa de Verdadeiros Positivos")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join("resultados", ds_name, "roc_comparison.png"), dpi=150)
    plt.close()
    print(f"Salvo: resultados/{ds_name}/roc_comparison.png")

print("\nTreino concluído. Execute PlotResultados.py para gerar os gráficos de comparação.")
