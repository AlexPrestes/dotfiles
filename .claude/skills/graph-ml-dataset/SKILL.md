---
name: graph-ml-dataset
description: >-
  Use ao montar a classe de dataset para ML em grafos / link prediction —
  envelopar arestas de um grafo para treino de modelos. Define a convenção
  de mapeamento nó↔índice contíguo, fatias de índice por classe
  (positivos/negativos/validação) e indexação estilo sklearn. Gatilhos:
  "dataset de grafo", "link prediction", "preparar arestas para treino",
  "mapear nós para índices".
---

# Convenção de dataset para ML em grafos

Envelope para arestas de um grafo que vão alimentar um classificador. É uma
**convenção de organização**, não um algoritmo — siga-a para que o resto do
pipeline ([[graph-kfold-link-prediction]], [[graph-topological-features]])
funcione sem surpresas.

## Regras da convenção

- **Mapeamento `nó ↔ índice contíguo`**: ordene os nós únicos e crie
  `node_to_idx` e `idx_to_node`. Todo o pipeline opera sobre índices
  inteiros `[0, N)`, nunca sobre os rótulos originais. Matrizes esparsas e
  vetorização dependem disso.
- **Dtypes fixos**:
  - arestas → `np.uint16` (ou `uint32` se `N > 65535`)
  - labels → `np.bool_`, em coluna `(-1, 1)`
  - índices → `np.uint32`
  Em grafos grandes isso é a diferença entre rodar e estourar a RAM.
- **Fatias de índice por classe**: mantenha `positive_idx`, `negative_idx`,
  `experimental_idx` (validação) como arrays de índices apontando para uma
  **única** pilha `self.edges` / `self.labels`. Não duplique arestas em
  estruturas separadas — fatie a mesma pilha.
- **Indexação estilo sklearn**: `__getitem__(idx)` devolve
  `np.hstack([edges[idx], labels[idx]])` → linhas `[u, v, label]`, que é o
  formato que os outros estágios consomem.
- **Higiene de entrada**: filtre IDs/datas inválidos **antes** de mapear
  `nó → idx`; um nó órfão quebra o mapeamento contíguo.

## Esqueleto

```python
class GraphDataset:
    def __init__(self, ...):
        self.node_to_idx, self.idx_to_node = self._build_node_map()
        # empilha tudo numa pilha só; guarda apenas as fatias de índice
        self.edges, self.labels = ..., ...
        self.positive_idx, self.negative_idx, self.experimental_idx = ...

    def __len__(self):
        return len(self.edges)

    def __getitem__(self, idx):
        return np.hstack([self.edges[idx], self.labels[idx]])  # [u, v, label]
```

Uso: `dataset[dataset.positive_idx]` devolve as positivas no formato
`[u, v, label]` pronto para [[graph-kfold-link-prediction]].
