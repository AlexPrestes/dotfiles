---
name: graph-kfold-link-prediction
description: >-
  Use ao montar a validação cruzada (K-fold) para link prediction em grafos.
  Cobre o split dos exemplos POSITIVOS em folds, amostragem de exemplos
  negativos a uma taxa configurável, e a iteração que produz (treino, teste).
  Gatilhos: "K-fold link prediction", "amostrar arestas negativas",
  "dividir folds de grafo", "negative sampling".
---

# K-fold para link prediction

Validação cruzada específica de link prediction: o desbalanceamento é
extremo (pouquíssimas arestas reais contra O(N²) não-arestas), então o split
e a amostragem de negativas exigem tratamento próprio.

## Regras

- **Divida só os POSITIVOS em folds.** Os negativos são amostrados, não
  particionados — há ordens de magnitude mais negativos que positivos.
- **Amostragem de negativas por taxa**: `negative_rate_sample × n_pos_treino`
  negativas vão para o treino; o **excedente de negativas vai para o teste**
  (espelha o desbalanceamento real na avaliação). Limite ao total disponível.
  ⚠️ Isso torna o teste O(N²) — o gargalo de tempo e RAM do pipeline. Chunke o
  caminho de teste inteiro (ver [[graph-topological-features]]). Alternativa de
  método: **amostrar** negativas no teste também (mais rápido, conserta
  AUPRC≈0), ao custo de avaliação menos dura.
- **Embaralhe só o treino, nunca o teste.** Embaralhar o teste custa caro e
  não muda métrica alguma — é desperdício por fold.
- **Saída por fold**: `yield (train_edges, test_edges)`, cada um no formato
  `[u, v, label]` (compatível com [[graph-ml-dataset]]).

## Contrato anti-leakage (crítico)

As features **devem** ser calculadas apenas sobre o grafo do **treino deste
fold** — a aresta-alvo (e qualquer aresta de teste) não pode existir no
grafo-base na hora de extrair suas features. Esse contrato é cumprido em
[[graph-topological-features]] (o "safe edge"); aqui basta garantir que
`train_edges` e `test_edges` são disjuntos e que o consumidor reconstrói o
grafo-base a cada fold.

## Amostragem das negativas

Enumere os pares do triângulo superior (`np.triu_indices(N)`), exclua os que
já são arestas (nas **duas** direções, grafo não-direcionado) e amostre. Para
N grande, gere as negativas sob demanda em vez de materializar todos os pares.

## Esqueleto

```python
class GraphKFold:
    def __init__(self, positive_edges, negative_edges,
                 negative_rate_sample=1, n_splits=5, shuffle=True, seed=42):
        ...  # embaralha índices de positivos/negativos; cria masks dos folds

    def __next__(self):
        pos_test  = positives[fold]            # 1/k dos positivos
        pos_train = positives[~fold]
        n_neg_tr  = min(len(pos_train) * self.negative_rate_sample, n_neg)
        neg_train, neg_test = negatives[:n_neg_tr], negatives[n_neg_tr:]
        train = concat(pos_train, neg_train); rng.shuffle(train)
        test  = concat(pos_test,  neg_test)   # NÃO embaralha
        return train, test
```
