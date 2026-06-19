# Resultados dos Experimentos

Seeds utilizadas: 0, 42, 123, 789, 1024  
Parametros: feromonio inicial=1 | evaporacao=0.1 | Q=1

---

## Dataset: yeast.csv
Instancias: 1484 | Atributos: 8 | Classes: 10 | Alvo: name
Execucoes feitas em um RTX 4060 TI e processador Ryzen 5700X3D para Python, C e CUDA.

### Versao Python (NumPy vetorizado)
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 756 | 0.783019 | 68.544987 | 7.054984 | 75.624469 | 75.633594 |
| 42 | 781 | 0.783019 | 68.429288 | 6.447527 | 74.899222 | 74.903080 |
| 123 | 775 | 0.780997 | 67.686294 | 7.319547 | 75.030835 | 75.034568 |
| 789 | 805 | 0.782345 | 64.602495 | 6.659379 | 71.283990 | 71.287797 |
| 1024 | 810 | 0.781671 | 70.103430 | 6.734751 | 76.859399 | 76.863126 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 74.739583 s |
| Desvio padrao run_colony | 2.081350 s |
| Tempo medio total por seed | 74.744433 s |
| Desvio padrao total por seed | 2.081895 s |
| Media instancias selecionadas | 785.40 |
| Tempo total do experimento | 373.741689 s |

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 790 | 0.785714 | 5.388000 | 2.591000 | 7.997000 | 7.999000 |
| 42 | 775 | 0.787062 | 4.656000 | 2.556000 | 7.227000 | 7.229000 |
| 123 | 779 | 0.784367 | 4.631000 | 2.524000 | 7.171000 | 7.172000 |
| 789 | 783 | 0.783693 | 6.853000 | 3.079000 | 9.948000 | 9.949000 |
| 1024 | 785 | 0.788410 | 4.532000 | 2.565000 | 7.113000 | 7.114000 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 7.891200 s |
| Desvio padrao run_colony | 1.204893 s |
| Tempo medio total por seed | 7.892600 s |
| Desvio padrao total por seed | 1.204777 s |
| Media instancias selecionadas | 782.40 |
| Tempo total do experimento | 39.466000 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 800 | 0.787062 | 0.000800 | 0.226516 | 0.052886 | 0.407305 | 0.409222 |
| 42 | 782 | 0.785040 | 0.000335 | 0.237575 | 0.053883 | 0.295359 | 0.296008 |
| 123 | 800 | 0.784367 | 0.000338 | 0.225899 | 0.058617 | 0.288768 | 0.289518 |
| 789 | 793 | 0.785040 | 0.000332 | 0.224775 | 0.052904 | 0.281484 | 0.282168 |
| 1024 | 757 | 0.784367 | 0.000329 | 0.224671 | 0.057544 | 0.286075 | 0.286724 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 0.311798 s |
| Desvio padrao run_colony | 0.053626 s |
| Tempo medio total por seed | 0.312728 s |
| Desvio padrao total por seed | 0.054174 s |
| Media instancias selecionadas | 786.40 |
| Tempo total do experimento | 1.570741 s |

### Speedup no yeast.csv (mesma maquina)
| Comparacao | Calculo | Speedup medio run_colony |
|---|---:|---:|
| C vs Python | 74.739583 / 7.891200 | **9.47x** |
| CUDA vs Python | 74.739583 / 0.311798 | **239.71x** |
| CUDA vs C | 7.891200 / 0.311798 | **25.31x** |

---

## Dataset: vh_data15.csv
Instancias: 3353 | Atributos: 41 | Classes: 2

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 1700 | 0.853564 | 54.364164 | 43.797277 | 98.254161 | 98.254522 |
| 42 | 1747 | 0.851775 | 54.276685 | 44.037504 | 98.404764 | 98.405143 |
| 123 | 1710 | 0.852669 | 54.271744 | 43.857178 | 98.217623 | 98.217986 |
| 789 | 1669 | 0.852073 | 54.308828 | 43.780535 | 98.178402 | 98.178762 |
| 1024 | 1712 | 0.853564 | 54.203367 | 43.701929 | 97.993750 | 97.994109 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 98.209740 s |
| Desvio padrao run_colony | 0.148074 s |
| Tempo medio total por seed | 98.210104 s |
| Desvio padrao total por seed | 0.148081 s |
| Media instancias selecionadas | 1707.60 |
| Tempo total do experimento | 491.086415 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 1741 | 0.855652 | 0.002792 | 0.929815 | 0.222413 | 1.414063 | 1.414405 |
| 42 | 1726 | 0.854160 | 0.002259 | 0.922620 | 0.220740 | 1.150464 | 1.150806 |
| 123 | 1760 | 0.852371 | 0.002261 | 0.923316 | 0.222047 | 1.152455 | 1.152770 |
| 789 | 1764 | 0.854459 | 0.002256 | 0.929196 | 0.221511 | 1.157823 | 1.158162 |
| 1024 | 1711 | 0.852967 | 0.002258 | 0.935218 | 0.221746 | 1.164057 | 1.164396 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 1.207772 s |
| Desvio padrao run_colony | 0.115440 s |
| Tempo medio total por seed | 1.208108 s |
| Desvio padrao total por seed | 0.115444 s |
| Media instancias selecionadas | 1740.40 |
| Tempo total do experimento | 6.074633 s |

### Speedup CUDA vs C (vh_data15)
Speedup medio run_colony: 98.209740 / 1.207772 = **81.31x**

---

## Dataset: optdigits_csv.csv
Instancias: 5620 | Atributos: 64 | Classes: 10

### Versao C Sequencial
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 2849 | 0.995552 | 279.037570 | 207.020425 | 486.404315 | 486.404843 |
| 42 | 2779 | 0.995552 | 278.310031 | 208.547967 | 487.193062 | 487.193615 |
| 123 | 2770 | 0.995374 | 280.006735 | 209.401949 | 489.740625 | 489.741127 |
| 789 | 2820 | 0.995552 | 281.794049 | 209.129923 | 491.255005 | 491.255502 |
| 1024 | 2813 | 0.995374 | 279.805393 | 208.703549 | 488.848450 | 488.848968 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 488.688291 s |
| Desvio padrao run_colony | 1.947648 s |
| Tempo medio total por seed | 488.688811 s |
| Desvio padrao total por seed | 1.947630 s |
| Media instancias selecionadas | 2806.20 |
| Tempo total do experimento | 2443.483253 s |

### Versao CUDA
| Seed | Instancias Selecionadas | Acuracia 1-NN | Tempo distancias (s) | Tempo ACO (s) | Tempo 1-NN (s) | Tempo run_colony (s) | Tempo total seed (s) |
|-----:|------------------------:|:-------------:|---------------------:|--------------:|---------------:|---------------------:|---------------------:|
| 0 | 2884 | 0.996085 | 0.009102 | 3.892801 | 1.059400 | 5.109765 | 5.110255 |
| 42 | 2839 | 0.995552 | 0.008509 | 3.898532 | 1.057934 | 4.978318 | 4.978879 |
| 123 | 2827 | 0.995730 | 0.008425 | 3.883610 | 1.058088 | 4.963389 | 4.963969 |
| 789 | 2794 | 0.995552 | 0.008497 | 3.895960 | 1.057660 | 4.975340 | 4.975826 |
| 1024 | 2835 | 0.995552 | 0.008411 | 3.877239 | 1.057708 | 4.956686 | 4.957206 |

| Metrica | Valor |
|---|---:|
| Tempo medio run_colony | 4.996700 s |
| Desvio padrao run_colony | 0.063813 s |
| Tempo medio total por seed | 4.997227 s |
| Desvio padrao total por seed | 0.063792 s |
| Media instancias selecionadas | 2835.80 |
| Tempo total do experimento | 25.012993 s |

### Speedup CUDA vs C (optdigits)
Speedup medio run_colony: 488.688291 / 4.996700 = **97.80x**

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
| yeast | 1484 | 8 | 25.31x |
| vh_data15 | 3353 | 41 | 81.31x |
| optdigits | 5620 | 64 | 97.80x |
| covtype_sample | 5620 | 54 | 104.11x |
| weatherAUS_sample | 5620 | 21 | 104.26x |
**Importante:** yeast, covtype_sample e weatherAUS_sample foram medidos nesta maquina local. vh_data15 e optdigits tiveram os resultados C/CUDA atualizados a partir dos logs executados no SSH; as comparacoes com Python para esses dois datasets permanecem aproximadas porque o Python foi medido em outra maquina.

---

## Resultados Python (NumPy vetorizado)

Implementacao Python reescrita com numpy vetorizado (sem lacos Python aninhados O(n^2)): escolha de caminho por argsort/flatnonzero, evaporacao por multiplicacao in-place, deposito por fancy-index, avaliacao 1-NN por argmin matricial. Executada nesta maquina (RTX 4090, mesma maquina dos experimentos C/CUDA de covtype e weatherAUS).

### Dataset: yeast.csv - Resultado consolidado nesta maquina
Os resultados atualizados do `yeast.csv` para Python, C e CUDA foram consolidados na primeira secao deste arquivo, permitindo comparar as tres versoes executadas no mesmo PC.

---

### Dataset: vh_data15.csv - Versao Python
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
> Atencao: Python foi medido em outra maquina; os resultados C e CUDA abaixo foram atualizados a partir dos logs executados no SSH. Comparacao aproximada.

| Comparacao | Calculo | Speedup medio run_colony |
|---|---:|---:|
| C vs Python | 433.057004 / 98.209740 | **4.41x** |
| CUDA vs Python | 433.057004 / 1.207772 | **358.56x** |
| CUDA vs C | 98.209740 / 1.207772 | **81.31x** |

---

### Dataset: optdigits_csv.csv - Versao Python
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
> Atencao: Python foi medido em outra maquina; os resultados C e CUDA abaixo foram atualizados a partir dos logs executados no SSH. Comparacao aproximada.

| Comparacao | Calculo | Speedup medio run_colony |
|---|---:|---:|
| C vs Python | 2202.496101 / 488.688291 | **4.51x** |
| CUDA vs Python | 2202.496101 / 4.996700 | **440.79x** |
| CUDA vs C | 488.688291 / 4.996700 | **97.80x** |

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
| yeast | 1484 | 8 | 74.74 | 7.89 | **9.47x** | 0.312 | **239.71x** | **25.31x** |
| vh_data15 | 3353 | 41 | 433.06 | 98.21 | **4.41x** | 1.208 | **358.56x** | **81.31x** |
| optdigits | 5620 | 64 | 2202.50 | 488.69 | **4.51x** | 4.997 | **440.79x** | **97.80x** |
| covtype_sample | 5620 | 54 | 2155.19 | 518.50 | **4.16x** | 4.981 | **432.73x** | **104.11x** |
| weatherAUS_sample | 5620 | 21 | 2157.26 | 518.25 | **4.16x** | 4.971 | **434.02x** | **104.26x** |

