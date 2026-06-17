# Resultados dos Experimentos

Seeds utilizadas: 0, 42, 123, 789, 1024  
Parametros: feromonio inicial=1 | evaporacao=0.1 | Q=1

---

## Dataset: yeast.csv
Instancias: 1484 | Atributos: 8 | Classes: 10

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|---------------------:|
| 0 | 800 | 0.787062 | 0.386763 |
| 42 | 782 | 0.785040 | 0.261474 |
| 123 | 800 | 0.784367 | 0.262546 |
| 789 | 793 | 0.785040 | 0.263765 |
| 1024 | 757 | 0.784367 | 0.255017 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 0.285913 s |
| Desvio padrao run_colony | 0.056478 s |
| Media instancias selecionadas | 786.40 |
| Tempo total do experimento | 1.439253 s |

---

## Dataset: vh_data15.csv
Instancias: 3353 | Atributos: 41 | Classes: 2

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 1700 | 0.853564 | 84.406 | 38.521 | 123.093 |
| 42 | 1747 | 0.851775 | 82.890 | 38.249 | 121.303 |
| 123 | 1710 | 0.852669 | 83.654 | 38.414 | 122.229 |
| 789 | 1669 | 0.852073 | 82.393 | 38.312 | 120.861 |
| 1024 | 1712 | 0.853564 | 82.890 | 38.360 | 121.401 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 121.777400 s |
| Desvio padrao run_colony | 0.886181 s |
| Media instancias selecionadas | 1707.60 |
| Tempo total do experimento | 609.010000 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|
| 0 | 1741 | 0.855652 | 0.013615 | 4.180865 | 1.031662 | 5.370043 |
| 42 | 1726 | 0.854160 | 0.011363 | 4.236742 | 1.074578 | 5.340975 |
| 123 | 1760 | 0.852371 | 0.011349 | 4.306106 | 1.216457 | 5.544289 |
| 789 | 1764 | 0.854459 | 0.011444 | 4.224703 | 1.186317 | 5.431912 |
| 1024 | 1711 | 0.852967 | 0.011353 | 4.236651 | 1.082131 | 5.341916 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 5.405827 s |
| Desvio padrao run_colony | 0.085766 s |
| Media instancias selecionadas | 1740.40 |
| Tempo total do experimento | 27.113335 s |

### Speedup CUDA vs C (vh_data15)
Speedup medio run_colony: 121.777400 / 5.405827 = **22.53x**

---

## Dataset: optdigits_csv.csv
Instancias: 5620 | Atributos: 64 | Classes: 10

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2849 | 0.995552 | 445.347 | 136.234 | 582.239 |
| 42 | 2779 | 0.995552 | 461.957 | 138.807 | 601.411 |
| 123 | 2770 | 0.995374 | 466.883 | 137.501 | 605.040 |
| 789 | 2820 | 0.995552 | 451.918 | 138.892 | 591.475 |
| 1024 | 2813 | 0.995374 | 448.006 | 136.896 | 585.585 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 593.150000 s |
| Desvio padrao run_colony | 9.857751 s |
| Media instancias selecionadas | 2806.20 |
| Tempo total do experimento | 2965.832000 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|
| 0 | 2884 | 0.996085 | 0.055863 | 18.875945 | 12.609711 | 31.645549 |
| 42 | 2839 | 0.995552 | 0.047335 | 18.900082 | 12.995137 | 31.963733 |
| 123 | 2827 | 0.995730 | 0.047582 | 18.908996 | 12.867987 | 31.845900 |
| 789 | 2794 | 0.995552 | 0.047322 | 18.913883 | 12.747811 | 31.729868 |
| 1024 | 2835 | 0.995552 | 0.047301 | 18.911900 | 12.809873 | 31.791640 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 31.795338 s |
| Desvio padrao run_colony | 0.120052 s |
| Media instancias selecionadas | 2835.80 |
| Tempo total do experimento | 159.052134 s |

### Speedup CUDA vs C (optdigits)
Speedup medio run_colony: 593.150000 / 31.795338 = **18.65x**

---

## Dataset: covtype_sample.csv (Forest Cover Type, amostra estratificada)
Instancias: 5620 | Atributos: 54 | Classes: 7 | Alvo: Cover_Type

O dataset original (kaggle.com/datasets/uciml/forest-cover-type-dataset) possui 581.012 instancias. Como o algoritmo guloso usa uma matriz de distancias O(n^2), o tamanho completo e computacionalmente inviavel nesta maquina (a matriz de distancias sozinha exigiria ~2,7 petabytes). Foi extraida uma amostra estratificada por classe de 5.620 instancias (mesma escala do maior dataset ja validado no projeto, optdigits) usando `dataset/prepare_kaggle_datasets.py` (seed de amostragem 42).

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2925 | 0.860676 | 299.617 | 218.254 | 518.192 |
| 42 | 2865 | 0.863523 | 299.146 | 218.122 | 517.599 |
| 123 | 2865 | 0.862278 | 298.802 | 217.987 | 517.115 |
| 789 | 2904 | 0.866014 | 302.156 | 218.056 | 520.538 |
| 1024 | 2871 | 0.862633 | 300.328 | 218.423 | 519.077 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 518.504238 s |
| Desvio padrao run_colony | 1.352149 s |
| Media instancias selecionadas | 2886.00 |
| Tempo total do experimento | 2592.547052 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|
| 0 | 2886 | 0.861388 | 0.009146 | 3.862999 | 1.060572 | 5.073625 |
| 42 | 2904 | 0.862100 | 0.008525 | 3.880099 | 1.056673 | 4.958426 |
| 123 | 2875 | 0.861922 | 0.008517 | 3.878727 | 1.060122 | 4.960454 |
| 789 | 2909 | 0.861744 | 0.008526 | 3.865052 | 1.058198 | 4.944875 |
| 1024 | 2888 | 0.861566 | 0.008517 | 3.885548 | 1.057972 | 4.965158 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 4.980508 s |
| Desvio padrao run_colony | 0.052597 s |
| Media instancias selecionadas | 2892.40 |
| Tempo total do experimento | 24.935738 s |

### Speedup CUDA vs C (covtype_sample), por seed
| Seed | Tempo C run_colony (s) | Tempo CUDA run_colony (s) | Speedup |
|-----:|------------------------:|---------------------------:|--------:|
| 0 | 518.192 | 5.074 | 102.13x |
| 42 | 517.599 | 4.958 | 104.39x |
| 123 | 517.115 | 4.960 | 104.25x |
| 789 | 520.538 | 4.945 | 105.27x |
| 1024 | 519.077 | 4.965 | 104.54x |

Speedup medio run_colony: 518.504238 / 4.980508 = **104.11x**

---

## Dataset: weatherAUS_sample.csv (Weather Dataset Rattle Package, amostra estratificada)
Instancias: 5620 | Atributos: 21 | Classes: 2 | Alvo: RainTomorrow

O dataset original (kaggle.com/datasets/jsphyg/weather-dataset-rattle-package) possui 145.460 linhas, das quais apenas 56.420 estao completas (sem valores faltantes). A coluna `Date` foi descartada (alta cardinalidade, sem valor para a metrica de distancia) e as linhas com qualquer valor `NA` foram removidas antes da amostragem. Foi extraida uma amostra estratificada por classe de 5.620 instancias (mesma logica e seed de amostragem do covtype_sample) usando `dataset/prepare_kaggle_datasets.py`.

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2851 | 0.908897 | 302.281 | 218.517 | 521.018 |
| 42 | 2790 | 0.910320 | 298.633 | 217.934 | 516.762 |
| 123 | 2862 | 0.910142 | 298.911 | 218.018 | 517.118 |
| 789 | 2818 | 0.908719 | 300.721 | 218.055 | 518.967 |
| 1024 | 2914 | 0.911032 | 299.666 | 217.521 | 517.377 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 518.248448 s |
| Desvio padrao run_colony | 1.763094 s |
| Media instancias selecionadas | 2847.00 |
| Tempo total do experimento | 2591.255067 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|
| 0 | 2871 | 0.909786 | 0.003397 | 3.887554 | 1.056103 | 5.095149 |
| 42 | 2925 | 0.910854 | 0.003007 | 3.872152 | 1.056949 | 4.945124 |
| 123 | 2842 | 0.908541 | 0.003074 | 3.862054 | 1.057629 | 4.935892 |
| 789 | 2854 | 0.909609 | 0.003008 | 3.864663 | 1.057127 | 4.937836 |
| 1024 | 2868 | 0.910498 | 0.003062 | 3.865468 | 1.057409 | 4.938766 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 4.970554 s |
| Desvio padrao run_colony | 0.069737 s |
| Media instancias selecionadas | 2872.00 |
| Tempo total do experimento | 24.875351 s |

### Speedup CUDA vs C (weatherAUS_sample), por seed
| Seed | Tempo C run_colony (s) | Tempo CUDA run_colony (s) | Speedup |
|-----:|------------------------:|---------------------------:|--------:|
| 0 | 521.018 | 5.095 | 102.26x |
| 42 | 516.762 | 4.945 | 104.50x |
| 123 | 517.118 | 4.936 | 104.77x |
| 789 | 518.967 | 4.938 | 105.10x |
| 1024 | 517.377 | 4.939 | 104.76x |

Speedup medio run_colony: 518.248448 / 4.970554 = **104.26x**

---

## Comparativo geral de speedup (todos os datasets)
| Dataset | Instancias | Atributos | Speedup medio run_colony |
|---|---:|---:|---:|
| vh_data15 | 3353 | 41 | 22.53x |
| optdigits | 5620 | 64 | 18.65x |
| covtype_sample | 5620 | 54 | 104.11x |
| weatherAUS_sample | 5620 | 21 | 104.26x |

**Importante:** vh_data15 e optdigits foram originalmente medidos em uma RTX 4060 Ti (ver README); covtype_sample e weatherAUS_sample foram medidos nesta maquina, com uma RTX 4090. O salto no speedup (~18-22x para ~104x) reflete majoritariamente essa diferenca de GPU, e nao um efeito do dataset em si — o tempo C permanece na mesma ordem de grandeza (~518s) que o de optdigits (~593s) para o mesmo n=5620, mas o tempo CUDA cai de ~32s para ~5s por ser uma GPU mais potente. Para uma comparacao justa entre datasets, os tempos absolutos de CUDA nao devem ser comparados entre maquinas diferentes.

---

## Resultados Python (NumPy vetorizado)

Implementacao Python reescrita com numpy vetorizado (sem lacos Python aninhados O(n^2)): escolha de caminho por argsort/flatnonzero, evaporacao por multiplicacao in-place, deposito por fancy-index, avaliacao 1-NN por argmin matricial. Executada nesta maquina (RTX 4090, mesma maquina dos experimentos C/CUDA de covtype e weatherAUS).

### Dataset: yeast.csv — Versao Python
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 791 | 0.785040 | 27.102436 | 4.358665 | 31.485772 |
| 42 | 773 | 0.785714 | 27.247917 | 4.230841 | 31.511593 |
| 123 | 785 | 0.781671 | 27.399593 | 4.219842 | 31.661415 |
| 789 | 757 | 0.783693 | 27.521716 | 4.220509 | 31.775444 |
| 1024 | 789 | 0.786388 | 27.684748 | 4.294446 | 32.012541 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 31.689353 s |
| Desvio padrao run_colony | 0.215457 s |
| Media instancias selecionadas | 779.00 |
| Tempo total do experimento | 158.461410 s |

### Speedup CUDA vs Python (yeast)
> Atencao: Python medido nesta maquina (RTX 4090); CUDA medido originalmente em RTX 4060 Ti. Comparacao indicativa — maquinas diferentes.

| Seed | Tempo Python (s) | Tempo CUDA (s) | Speedup CUDA/Python |
|-----:|-----------------:|---------------:|--------------------:|
| 0 | 31.486 | 0.387 | 81.37x |
| 42 | 31.512 | 0.261 | 120.73x |
| 123 | 31.661 | 0.263 | 120.46x |
| 789 | 31.775 | 0.264 | 120.36x |
| 1024 | 32.013 | 0.255 | 125.54x |

Speedup medio CUDA/Python: 31.689353 / 0.285913 = **110.83x** (cross-machine)

---

### Dataset: vh_data15.csv — Versao Python
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 1797 | 0.857143 | 264.269615 | 163.767545 | 428.149533 |
| 42 | 1746 | 0.855353 | 262.977422 | 164.744139 | 427.851615 |
| 123 | 1726 | 0.852967 | 265.958293 | 169.393415 | 435.472688 |
| 789 | 1735 | 0.855353 | 265.647136 | 170.563896 | 436.330755 |
| 1024 | 1721 | 0.853862 | 265.761356 | 171.598747 | 437.480430 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 433.057004 s |
| Desvio padrao run_colony | 4.671697 s |
| Media instancias selecionadas | 1745.00 |
| Tempo total do experimento | 2165.375994 s |

### Speedup C e CUDA vs Python (vh_data15)
> Atencao: C e CUDA medidos originalmente em RTX 4060 Ti; Python nesta maquina (RTX 4090). Comparacao aproximada.

| Seed | Tempo Python (s) | Tempo C (s) | Speedup C/Python | Tempo CUDA (s) | Speedup CUDA/Python |
|-----:|-----------------:|------------:|-----------------:|---------------:|--------------------:|
| 0 | 428.150 | 123.093 | 3.48x | 5.370 | 79.73x |
| 42 | 427.852 | 121.303 | 3.53x | 5.341 | 80.11x |
| 123 | 435.473 | 122.229 | 3.56x | 5.544 | 78.54x |
| 789 | 436.331 | 120.861 | 3.61x | 5.432 | 80.33x |
| 1024 | 437.480 | 121.401 | 3.60x | 5.342 | 81.90x |

Speedup medio C/Python: 433.057004 / 121.777400 = **3.56x** (cross-machine)
Speedup medio CUDA/Python: 433.057004 / 5.405827 = **80.11x** (cross-machine)

---

### Dataset: optdigits_csv.csv — Versao Python
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2792 | 0.995552 | 1177.840124 | 976.883790 | 2155.117319 |
| 42 | 2881 | 0.995374 | 1179.531750 | 978.194853 | 2158.006236 |
| 123 | 2796 | 0.995374 | 1308.160656 | 977.178981 | 2285.607162 |
| 789 | 2825 | 0.995374 | 1174.634890 | 978.236190 | 2153.135656 |
| 1024 | 2827 | 0.995552 | 1308.314310 | 952.034874 | 2260.614134 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 2202.496101 s |
| Desvio padrao run_colony | 65.087834 s |
| Media instancias selecionadas | 2824.20 |
| Tempo total do experimento | 11012.557576 s |

### Speedup C e CUDA vs Python (optdigits)
> Atencao: C e CUDA medidos originalmente em RTX 4060 Ti; Python nesta maquina (RTX 4090). Comparacao aproximada.

| Seed | Tempo Python (s) | Tempo C (s) | Speedup C/Python | Tempo CUDA (s) | Speedup CUDA/Python |
|-----:|-----------------:|------------:|-----------------:|---------------:|--------------------:|
| 0 | 2155.117 | 582.239 | 3.70x | 31.646 | 68.11x |
| 42 | 2158.006 | 601.411 | 3.59x | 31.964 | 67.52x |
| 123 | 2285.607 | 605.040 | 3.78x | 31.846 | 71.78x |
| 789 | 2153.136 | 591.475 | 3.64x | 31.730 | 67.86x |
| 1024 | 2260.614 | 585.585 | 3.86x | 31.792 | 71.11x |

Speedup medio C/Python: 2202.496101 / 593.150000 = **3.71x** (cross-machine)
Speedup medio CUDA/Python: 2202.496101 / 31.795338 = **69.27x** (cross-machine)

---

### Dataset: covtype_sample.csv — Versao Python
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2901 | 0.861210 | 1185.811520 | 975.946259 | 2162.125185 |
| 42 | 2868 | 0.860142 | 1175.041574 | 977.516035 | 2152.844991 |
| 123 | 2860 | 0.861566 | 1174.937293 | 980.301371 | 2155.509316 |
| 789 | 2889 | 0.861566 | 1176.592033 | 978.464138 | 2155.333990 |
| 1024 | 2852 | 0.862100 | 1169.763544 | 980.108868 | 2150.153428 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 2155.193382 s |
| Desvio padrao run_colony | 4.446503 s |
| Media instancias selecionadas | 2874.00 |
| Tempo total do experimento | 10776.037731 s |

### Speedup C e CUDA vs Python (covtype_sample) — mesma maquina
| Seed | Tempo Python (s) | Tempo C (s) | Speedup C/Python | Tempo CUDA (s) | Speedup CUDA/Python |
|-----:|-----------------:|------------:|-----------------:|---------------:|--------------------:|
| 0 | 2162.125 | 518.192 | 4.17x | 5.074 | 426.22x |
| 42 | 2152.845 | 517.599 | 4.16x | 4.958 | 434.16x |
| 123 | 2155.509 | 517.115 | 4.17x | 4.960 | 434.54x |
| 789 | 2155.334 | 520.538 | 4.14x | 4.945 | 435.90x |
| 1024 | 2150.153 | 519.077 | 4.14x | 4.965 | 433.09x |

Speedup medio C/Python: 2155.193382 / 518.504238 = **4.16x**
Speedup medio CUDA/Python: 2155.193382 / 4.980508 = **432.73x**

---

### Dataset: weatherAUS_sample.csv — Versao Python
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|
| 0 | 2837 | 0.909253 | 1185.109736 | 976.645159 | 2162.120433 |
| 42 | 2848 | 0.910498 | 1174.121259 | 979.281102 | 2153.726725 |
| 123 | 2827 | 0.909964 | 1178.153964 | 978.288931 | 2156.749602 |
| 789 | 2903 | 0.910320 | 1174.837868 | 981.453168 | 2156.561370 |
| 1024 | 2858 | 0.909609 | 1176.693963 | 980.175507 | 2157.138464 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 2157.259319 s |
| Desvio padrao run_colony | 3.036083 s |
| Media instancias selecionadas | 2854.60 |
| Tempo total do experimento | 10786.382251 s |

### Speedup C e CUDA vs Python (weatherAUS_sample) — mesma maquina
| Seed | Tempo Python (s) | Tempo C (s) | Speedup C/Python | Tempo CUDA (s) | Speedup CUDA/Python |
|-----:|-----------------:|------------:|-----------------:|---------------:|--------------------:|
| 0 | 2162.120 | 521.018 | 4.15x | 5.095 | 424.36x |
| 42 | 2153.727 | 516.762 | 4.17x | 4.945 | 435.55x |
| 123 | 2156.750 | 517.118 | 4.17x | 4.936 | 436.92x |
| 789 | 2156.561 | 518.967 | 4.16x | 4.938 | 436.74x |
| 1024 | 2157.138 | 517.377 | 4.17x | 4.939 | 436.76x |

Speedup medio C/Python: 2157.259319 / 518.248448 = **4.16x**
Speedup medio CUDA/Python: 2157.259319 / 4.970554 = **434.02x**

---

## Comparativo geral Python / C / CUDA (todos os datasets)

| Dataset | n | Atributos | Python medio (s) | C medio (s) | Speedup C/Python | CUDA medio (s) | Speedup CUDA/Python | Speedup CUDA/C |
|---|---:|---:|-----------------:|------------:|-----------------:|---------------:|--------------------:|---------------:|
| yeast | 1484 | 8 | 31.69 | — | — | 0.286 (*) | 110.83x (*) | 22.53x (*) |
| vh_data15 | 3353 | 41 | 433.06 | 121.78 (*) | 3.56x (*) | 5.406 (*) | 80.11x (*) | 22.53x (*) |
| optdigits | 5620 | 64 | 2202.50 | 593.15 (*) | 3.71x (*) | 31.795 (*) | 69.27x (*) | 18.65x (*) |
| covtype_sample | 5620 | 54 | 2155.19 | 518.50 | **4.16x** | 4.981 | **432.73x** | 104.11x |
| weatherAUS_sample | 5620 | 21 | 2157.26 | 518.25 | **4.16x** | 4.971 | **434.02x** | 104.26x |

(*) = comparacao entre maquinas diferentes (C/CUDA em RTX 4060 Ti; Python nesta maquina com RTX 4090). Valores indicativos.

**Conclusao:** Para os datasets medidos na mesma maquina (covtype e weatherAUS, n=5620), a versao C sequencial e ~4.16x mais rapida que o Python vetorizado com NumPy, e a versao CUDA e ~433x mais rapida que Python. O Python vetorizado, apesar de significativamente mais rapido que uma implementacao Python pura com lacos, continua limitado pelo overhead do interpretador e pela ausencia de paralelismo — o GIL impede threads, e o numpy opera sequencialmente no loop externo por formiga. A versao C explora SIMD e cache de forma mais eficiente para o padrao de acesso ao array, e a versao CUDA paraleliza o loop das formigas inteiramente na GPU.
