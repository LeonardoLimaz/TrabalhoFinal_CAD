# Projeto Final de Computacao de Alto Desempenho - Paralelizacao em CUDA do algoritmo ACO Guloso

Este projeto implementa e compara três versões de um algoritmo ACO guloso para redução de instâncias em datasets CSV:

- versão base em Python;
- versão sequencial em C;
- versão paralela em CUDA C/C++.

O objetivo principal foi partir do código utilizado como referência no artigo do trabalho, converter a implementação para C e, em seguida, paralelizar as etapas computacionalmente mais custosas usando GPU com CUDA.

## Datasets Disponiveis

Os datasets utilizados estao na pasta `dataset/`:

| Arquivo | Descricao no projeto |
| --- | --- |
| `dataset/yeast.csv` | Menor dataset, usado como primeiro caso de teste e validacao. |
| `dataset/vh_data15.csv` | Dataset intermediario disponivel para testes posteriores. |
| `dataset/optdigits_csv.csv` | Maior dataset disponivel na pasta do projeto. |

Durante o desenvolvimento, os primeiros testes foram feitos no `yeast.csv`, por ser o menor dataset e permitir validar mais rapidamente o comportamento das versões C e CUDA.

## Arquivo Base em Python

O arquivo base do projeto é:

```text
GulosoComplexity.py
```

Esse arquivo representa a implementação em Python do algoritmo ACO guloso utilizada como base a partir do artigo de referência do trabalho. Ele usa bibliotecas como:

- `pandas`, para leitura e manipulação do CSV;
- `numpy`, para estruturas matriciais;
- `sklearn.metrics.pairwise.euclidean_distances`, para calcular a matriz de distâncias;
- `KNeighborsClassifier`, para avaliar a solução final usando 1-NN;
- `random`, para o sorteio binario durante a construção dos caminhos das formigas.

A logica geral do algoritmo é:

1. Ler o dataset.
2. Separar atributos e classe.
3. Calcular a matriz de distâncias entre todas as instâncias.
4. Criar uma colônia com uma formiga por instancia.
5. Cada formiga seleciona ou rejeita instâncias de forma gulosa, considerando a matriz de feromônio.
6. Atualizar o feromônio com deposito e evaporação.
7. Ao final, avaliar as soluções usando 1-NN.
8. Salvar um CSV reduzido apenas com as instâncias selecionadas.

Para facilitar testes com o `yeast.csv`, tambem foi criado o runner:

```text
run_python_yeast.py
```

Esse script reaproveita as funções do arquivo Python original, ajusta a coluna alvo para `name`, executa múltiplas seeds e calcula média e desvio padrão dos tempos.

## Conversão para C

A versão sequencial em C está no arquivo:

```text
GulosoComplexity.c
```

A conversão para C manteve a semantica principal do algoritmo, mas removeu dependências de alto nivel como `pandas`, `numpy` e `scikit-learn`. Na versão C foram implementadas manualmente:

- leitura de CSV;
- parsing de valores numéricos;
- codificação de atributos categóricos;
- resolução da coluna alvo;
- calculo da matriz de distâncias;
- estrutura da colônia;
- matriz de feromônio;
- escolha gulosa dos caminhos;
- depósito e evaporação de feromônio;
- avaliação 1-NN;
- escrita do CSV reduzido;
- execução com múltiplas seeds;
- calculo de média e desvio padrão.

A interface da versao C permite executar:

```powershell
.\GulosoComplexity.exe dataset\yeast.csv dataset\yeast_reduzido_c.csv --seeds 0,42,123,789,1024
```

Também é possível informar parâmetros como:

```text
--target
--seed
--seeds
--initial-pheromone
--evaporation-rate
--q
```

Nos testes com `yeast.csv`, a versão C reduziu significativamente o tempo em relação ao Python porque elimina grande parte do overhead do interpretador e trabalha diretamente com arrays contíguos em memoria.

## Versão CUDA

A versão CUDA está no arquivo:

```text
GulosoComplexityCUDA.cu
```

Essa versão manteve na CPU as etapas de entrada e saida de dados:

- leitura do CSV;
- parsing;
- codificação de atributos categóricos;
- escolha da coluna alvo;
- controle das seeds;
- impressão dos resultados;
- escrita dos CSVs reduzidos.

As etapas computacionalmente mais caras foram migradas para a GPU.

### Partes Paralelizadas em CUDA

#### Calculo da matriz de distâncias

Kernel:

```text
calculate_pairwise_distances_kernel
```

Cada thread calcula uma posição `(i, j)` da matriz de distâncias `n x n`. A matriz inteira é calculada na GPU, mesmo sendo simétrica, para manter a implementação simples e direta.

#### Inicializacao da matriz de feromonio

Kernel:

```text
init_pheromone_kernel
```

A diagonal recebe `0.0` e as demais posições recebem o valor de feromônio inicial.

#### Inicializacao da colônia

Kernel:

```text
init_colony_kernel
```

Inicializa a matriz da colônia com `-1`, colocando `1` na diagonal para indicar que cada formiga inicialmente seleciona sua propria instancia.

#### Escolha gulosa dos caminhos

Kernel:

```text
choose_paths_greedy_block_kernel
```

A primeira versão CUDA usava uma thread por formiga. Depois, a implementação foi otimizada para usar um bloco por formiga.

Na versao atual:

- cada bloco CUDA representa uma formiga;
- as threads do bloco varrem candidatos em paralelo;
- uma redução em memória compartilhada encontra o candidato com maior feromônio;
- a thread `0` do bloco aplica o sorteio binário;
- se o sorteio for `1`, o candidato é marcado como escolhido;
- se o sorteio for `0`, o candidato é marcado como rejeitado;
- o contador global de posicoes indefinidas é atualizado com operacao atômica.

Essa estratégia preserva a lógica gulosa, mas explora melhor o paralelismo da GPU do que a abordagem inicial de uma única thread por formiga.

#### Depósito de feromônio

Kernels:

```text
calculate_deposits_kernel
apply_deposits_edges_kernel
```

O primeiro kernel calcula o depósito de cada formiga com base no comprimento do caminho.

O segundo aplica os depósitos nas arestas visitadas. Como diferentes formigas podem depositar feromônio na mesma aresta simultaneamente, a atualizacao usa `atomicAdd`.

#### Evaporação de feromônio

Kernel:

```text
evaporate_pheromone_kernel
```

Cada thread atualiza uma posição da matriz de feromônio:

```text
pheromone[idx] *= (1.0 - evaporation_rate)
```

#### Avaliação final com 1-NN

Kernel:

```text
evaluate_solutions_1nn_kernel
```

Cada bloco avalia uma formiga. As threads do bloco dividem as instâncias do dataset e contam quantas classificações foram corretas usando 1-NN. Depois, os acertos por formiga são copiados para a CPU, onde a melhor solução é selecionada.

### Compilação da Versão CUDA

No Windows, usando CUDA Toolkit e Visual Studio Build Tools:

```powershell
cmd /c 'call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" && "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.3\bin\nvcc.exe" -O3 -arch=sm_89 GulosoComplexityCUDA.cu -o aco_cuda.exe'
```

O parâmetro `-arch=sm_89` foi usado porque a GPU de teste é uma RTX 4060 Ti.

Em um ambiente Linux com `nvcc` no `PATH`, a compilação pode ser feita com:

```bash
nvcc -O3 GulosoComplexityCUDA.cu -o aco_cuda -lm
```

### Execução da Versão CUDA

Para executar no `yeast.csv` com as cinco seeds padrão:

```powershell
.\aco_cuda.exe dataset\yeast.csv dataset\yeast_reduzido_cuda.csv --seeds 0,42,123,789,1024
```

As saidas são geradas com sufixo por seed, por exemplo:

```text
dataset/yeast_reduzido_cuda_seed0.csv
dataset/yeast_reduzido_cuda_seed42.csv
dataset/yeast_reduzido_cuda_seed123.csv
dataset/yeast_reduzido_cuda_seed789.csv
dataset/yeast_reduzido_cuda_seed1024.csv
```

## Resultados Iniciais no Dataset `yeast.csv`

Na execução com as seeds `0, 42, 123, 789, 1024`, a versão CUDA apresentou:

| Seed | Instancias selecionadas | Acuracia 1-NN | Tempo `run_colony` |
| ---: | ---: | ---: | ---: |
| 0 | 800 | 0.787062 | 0.386763 s |
| 42 | 782 | 0.785040 | 0.261474 s |
| 123 | 800 | 0.784367 | 0.262546 s |
| 789 | 793 | 0.785040 | 0.263765 s |
| 1024 | 757 | 0.784367 | 0.255017 s |

Resumo:

| Metrica | Valor |
| --- | ---: |
| Tempo medio `run_colony` | 0.285913 s |
| Desvio padrao `run_colony` | 0.056478 s |
| Tempo medio total por seed | 0.287074 s |
| Desvio padrao total por seed | 0.057224 s |
| Media de instancias selecionadas | 786.40 |
| Tempo total do experimento | 1.439253 s |

