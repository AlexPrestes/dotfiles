---
name: graph-topological-features
description: >-
  Use ao extrair features topológicas de pares de nós para link prediction
  (predição de arestas) — interactomas/PPI, redes biológicas/sociais. Cobre
  o cálculo VETORIZADO por álgebra matricial esparsa (NUNCA loop por aresta),
  o anti-leakage "safe edge" e o protocolo de avaliação. Gatilhos:
  "features de grafo para ML", "common neighbors / Adamic-Adar / Jaccard /
  resource allocation", "link prediction", "predizer arestas".
---

# Features topológicas para link prediction

Coração do pipeline. Acompanha [[graph-ml-dataset]] (formato dos dados) e
[[graph-kfold-link-prediction]] (split). API estilo sklearn: `fit(train)`
constrói o grafo-base e pré-computa as matrizes; `transform(pares)` colhe o
vetor de features por par.

## Convenções não-negociáveis

- **Álgebra matricial esparsa, NUNCA loop por aresta.** Loop por aresta
  (estilo networkx) é proibido — explode o tempo em grafos reais.
- **Nada de matriz densa N×N.** Mantenha no `fit` só esparsas/vetores; calcule
  PA, Jaccard, clustering e triângulos **por par no `transform`**, só nos pares
  pedidos (O(M)). Materializar `deg_matrix`/`PA_mat`/`clus_mat` N×N é
  desperdício — o `transform` lê uns poucos pares, não N².
- **Triângulos via Hadamard, nunca `A@A@A`**: `tri = (CN.multiply(A)).sum(1)/2`
  dá `diag(A³)` sem materializar A³ — que era o maior vilão de RAM do `fit`.
- **CN/AA/RA em lote, não por elemento**: para um lote de pares,
  `C = A[u].multiply(A[v])`, depois `cn=C.sum(1)`, `aa=C@w_aa`, `ra=C@w_ra` —
  evita indexar matriz pré-materializada (o "slice" caro a milhões de pares).
- **Grafo não-direcionado** → adjacência simétrica (insira as duas direções).
- **Esparso de ponta a ponta**: `scipy.sparse` (`coo_array` → `csr_array`),
  `setdiag(0)` + `eliminate_zeros()` após cada produto.
- **Dtypes**: features de saída em `float32`; adjacência em `float64`.

## Safe edge — anti-leakage (a regra que mais importa)

Ao calcular as features de um par `(u, v)`, **o grafo-base não pode conter a
aresta-alvo**. Construa o grafo-base apenas com o treino do fold atual (ver
[[graph-kfold-link-prediction]]) e desconte a contribuição da própria aresta
quando ela existir no grafo. Vazamento aqui infla todas as métricas e invalida
o experimento.

## Protocolo de avaliação (a régua)

- Reporte **AUROC + AUPRC + P@k + NDCG** sempre juntos — AUROC sozinho engana
  sob desbalanceamento extremo (típico de link prediction). Sintoma clássico:
  AUROC alto mas **AUPRC ≈ 0** ao avaliar contra todas as não-arestas.
- Desbalanceamento: `class_weight='balanced'` (lineares) ou `scale_pos_weight`
  (boosting).
- Mantenha um conjunto de **validação independente** dos folds (ex.: validação
  experimental), reportado por fold.

## Escala: chunke o caminho de teste inteiro

Avaliar contra todas as não-arestas faz o teste ser O(N²) — o gargalo de tempo
**e** de RAM, não o `fit`. **Processe o teste em lotes** (features → poly →
`predict_proba`), nunca segurando o conjunto inteiro × nada.
`PolynomialFeatures` é o pior infrator (a expansão grau-2 é densa e cresce
quadraticamente no nº de features). Detalhes em `reference.md`.

## O que NÃO fixar

Modelo e hiperparâmetros (`num_leaves`, `C`, `n_estimators`, o valor de
`scale_pos_weight`…) variam por dataset — não pertencem a esta skill.

## Referência

As 9 features (fórmulas), os snippets esparsos de cada uma, os gotchas
numéricos e o exemplo real completo (interactoma HuRI) estão em
`reference.md` — leia ao implementar ou depurar uma feature específica.
