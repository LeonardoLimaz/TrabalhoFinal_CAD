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
