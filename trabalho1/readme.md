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
        |   |
        |   |-- maze.py
        |   |-- search.py
        |   |-- heuristics.py
        |
        |-- data/
        |   |-- labirinto.txt
        |
        |-- tests/
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
