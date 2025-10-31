# 🤖 Trabalho de Inteligência Artificial: Resolução de Labirintos

## 🧭 Parte 1: Problema do Labirinto (Buscas Informadas e Não-Informadas)

Este projeto implementa e compara diversos algoritmos de busca (incluindo buscas cegas e buscas heurísticas/informadas) para encontrar o caminho mais eficiente em um labirinto, como parte do trabalho da disciplina de Inteligência Artificial.

---

### 🚀 Funcionalidades Principais

* **Implementação de Buscas:** Inclui a implementação de algoritmos de busca (e.g., BFS, DFS, A*, Greedy Search - a depender da sua implementação em `search.py`).
* **Heurísticas Customizadas:** Utiliza diferentes funções heurísticas (em `heuristics.py`) para otimizar as buscas informadas (como A* e Busca Gulosa).
* **Visualização:** Gera arquivos na pasta `data/` para visualizar o caminho percorrido por cada algoritmo no labirinto.
* **Análise de Desempenho:** Exibe no terminal a comparação de métricas importantes (custo, nós expandidos) para cada tipo de busca.

### 📁 Estrutura do Projeto

A seguir, a estrutura de diretórios principal para o `trabalho1`:

```
 ia-trabalhos/
    |-- trabalho1/
        |
        |-- src/
        |   |-- main.py
        |   |-- maze_representation.py
        |   |-- search.py
        |   |-- heuristics.py
        |   |-- data_structures.py
        |   |-- labirinto.txt
        |-- data/
        |   |-- caminhos.png
        |
        |-- README.md
        |
        `-- relatorio.pdf

```
### ⚙️ Pré-requisitos e Bibliotecas

Para executar o projeto, você precisará ter o Python instalado e as seguintes bibliotecas:

| Biblioteca | Uso Principal |
| :--- | :--- |
| `matplotlib` | Geração de gráficos e visualização do caminho |
| `numpy` | Manipulação eficiente de estruturas de dados (matrizes/labirinto) |

Você pode instalá-las usando `pip`:

```
pip install matplotlib numpy
```

🛠️ Executando o Projeto

Siga os passos abaixo para rodar a simulação de busca no labirinto:

  1. Defina o Labirinto:
  2. Edite o arquivo data/labirinto.txt com a sua configuração de labirinto (tamanho, paredes, início e fim).
  3. Certifique-se de que o labirinto está formatado corretamente, conforme as especificações do projeto.
  4. Navegue até a pasta de código:
  5. Abra o terminal e acesse o diretório onde o arquivo principal (main.py) está localizado:
      ```
        cd trabalho1/src
      ```
  6. Execute o programa:

      Rode o script principal utilizando o Python 3:
     
      ```
       python3 main.py
      ```
  8. Analise os Resultados:

      Terminal: A saída no terminal exibirá a comparação de desempenho (custo do caminho, número de nós expandidos e tempo de execução) de cada algoritmo de busca implementado.
     
      Visualização: Verifique a pasta data/ para encontrar os arquivos de imagem gerados, que mostram visualmente o caminho percorrido por cada tipo de busca.
     
-----

## 👸 Parte 2: 8 Rainhas com Hill Climbing

Implementação do algoritmo Hill Climbing para o problema das 8 Rainhas, comparando quatro estratégias diferentes de otimização local.

### 📁 Estrutura do Projeto (Novos Arquivos Detalhados)

Os novos arquivos adicionados (`eight_queens_representation.py`, `hill_climbing.py`, `main_t2.py`) são detalhados abaixo:

```
ia-trabalhos/
    |-- trabalho1/
        |
        |-- src/
        |   |...
        |   |-- eight_queens_representation.py 
        |   |-- hill_climbing.py             
        |   |-- main_t2.py                   
        |...
```

### 📊 Estratégias de Hill Climbing Analisadas

O `main_t2.py` simula 100 execuções para cada uma das quatro configurações de Hill Climbing:

1.  **HC Simples** (Pure Hill Climbing)
2.  **HC Lateral** (Com limite de 10 movimentos laterais para escapar de platôs)
3.  **HC Random-Restart** (Reinicia ao atingir um máximo local)
4.  **HC Random-Restart com Lateral** (Combinação mais robusta)

### 🚀 Execução (Trabalho 2)

Para executar a simulação completa do Hill Climbing e gerar as métricas de sucesso, média de reinícios e média de passos, use:

```bash
python src/main_t2.py
```

### 📁 Diretório de Resultados (`data/`)

O diretório `data/` armazena os artefatos visuais e de análise gerados pelos scripts `main.py` e `main_t2.py`.

```
ia-trabalhos/
    |-- trabalho1/
        |...
        |-- data/
        |   |-- caminhos.png                  
        |   |-- taxa_sucesso_8rainhas.png    
        |
        |-- README.md
        |
        `-- relatorio.pdf                    
```
