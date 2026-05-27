# Referência — features topológicas (implementação esparsa)

> Exemplo real de origem: pipeline HuRI (PPI link prediction), reproduzindo
> *Assessment of community efforts to advance network-based prediction of
> protein–protein interactions* (Nature Communications, 2023).

## Vetor de 9 features por par (u, v)

| idx | feature | fórmula |
|-----|---------|---------|
| 0 | Common Neighbors | `|N(u) ∩ N(v)|` = `(A @ A)[u, v]` |
| 1 | Jaccard | `CN / (deg_u + deg_v − CN)` |
| 2 | Adamic-Adar | `Σ_{z ∈ CN} 1/log(deg_z)` |
| 3 | Preferential Attachment | `deg_u · deg_v` |
| 4 | Resource Allocation | `Σ_{z ∈ CN} 1/deg_z` |
| 5 | clustering (diferença) | `|clus_u − clus_v|` |
| 6 | clustering (média) | `(clus_u + clus_v) / 2` |
| 7 | triângulos (diferença) | `|tri_u − tri_v|` |
| 8 | triângulos (média) | `(tri_u + tri_v) / 2` |

## Snippets esparsos

### Adjacência (não-direcionada, sem auto-loop)
```python
row = np.concatenate([u, v])
col = np.concatenate([v, u])
A = coo_array((np.ones(len(row)), (row, col)), shape=(N, N)).tocsr()
A.setdiag(0)
A.eliminate_zeros()
deg = A.sum(axis=0).astype(np.float64)
```

### Common Neighbors / triângulos
```python
CN  = csr_array(A @ A)
# diag(A³) SEM materializar A³ — o A@A@A é o maior custo de RAM/tempo do fit.
tri = np.asarray(CN.multiply(A).sum(axis=1)).ravel() / 2.0   # diag(A³)_i = Σ_j (A²)_ij·A_ij
```

### Adamic-Adar / Resource Allocation
```python
w_aa = np.where(deg > 1, 1.0 / np.log(deg), 0.0)
AA = A @ (w_aa[:, None] * A)
AA.setdiag(0); AA.eliminate_zeros()

w_ra = np.where(deg > 0, 1.0 / deg, 0.0)
RA = csr_array(A @ (w_ra[:, None] * A))
```

### Jaccard (com proteção numérica)
```python
union = deg_matrix + deg_matrix.T - CN
union = np.maximum(union, 1e-10)            # evita divisão por zero
J = np.nan_to_num(CN / union, nan=0.0, posinf=0.0, neginf=0.0)
```

### clustering
```python
mask = deg_matrix > 1                        # clustering só para deg > 1
clus = np.zeros((N, N))
clus[mask] = 2 * tri_mat[mask] / (deg_matrix[mask] * (deg_matrix[mask] - 1))
```

## Gotchas aprendidos no HuRI

- **clustering** só é definido para `deg > 1` — proteja a divisão.
- **Nenhuma feature precisa de matriz densa N×N.** PA, Jaccard, clustering e
  triângulos saem da indexação dos vetores `deg`/`tri` e do `cn` por par —
  calcule no `transform`, só nos pares pedidos (O(M)). Materializar
  `deg_matrix`/`PA_mat`/`J_mat`/`clus_mat` N×N é desnecessário e domina a RAM
  do `fit`. Valide os valores contra um oráculo (networkx com `remove_edge`).
- **IDs/datas inválidos**: filtre antes de mapear `nó → idx`, senão o
  mapeamento contíguo quebra (ver [[graph-ml-dataset]]).
- **Shuffle do teste** custa caro sem ganho de métrica → não embaralhe o teste
  (ver [[graph-kfold-link-prediction]]).
- A feature de clustering/triângulos entra como **par** (diferença e média)
  porque é assimétrica entre `u` e `v` no grafo direcionado de cálculo.

## Escala e RAM — o conjunto de teste é O(N²)

O gargalo do pipeline não é o `fit`, é o `transform` do **teste**: avaliar
contra todas as não-arestas dá um teste de tamanho O(N²) — domina tempo **e**
RAM. Lições:

- **CN/AA/RA por elemento são o custo do "slice".** Indexar
  `CN_mat[u_idx, v_idx]` (busca binária em CSR por elemento) sobre milhões de
  pares domina o tempo. Em vez disso, compute em **lote** sobre os pares, sem
  indexar matriz pré-materializada:
  ```python
  C  = A[u].multiply(A[v])          # (m, N) esparsa: vizinhos comuns por par
  cn = np.asarray(C.sum(1)).ravel()
  aa = C @ w_aa                     # Σ_z (comum) · 1/log(deg_z)
  ra = C @ w_ra                     # Σ_z (comum) · 1/deg_z
  ```
  Isso também dispensa materializar `CN_mat`/`AA_mat`/`RA_mat` no `fit`.
- **Chunke o caminho de teste INTEIRO** — features → (poly) → `predict_proba`
  em lotes. Limita o pico de RAM independente de N; é o que faz caber em
  cliente com pouca RAM. Nunca segure o conjunto de teste inteiro × nada.
- **`PolynomialFeatures` é o pior infrator de RAM** sob esse regime: a expansão
  grau-2 é **densa** e cresce quadraticamente no nº de features — materializá-la
  sobre o teste inteiro estoura a RAM. Só sobrevive chunkando o `predict`;
  avalie se o ganho de métrica justifica o modelo.
- **Safe-edge é estruturalmente 0 no teste**: pares de teste (positivos
  held-out + não-arestas) não estão no grafo de treino, então `A_train[u,v]=0`
  — a correção só importa nos pares de **treino** (ver
  [[graph-kfold-link-prediction]]).
- **AUPRC ≈ 0 no teste** com AUROC alto é o sintoma de avaliar contra todas as
  não-arestas. Não é bug do extractor; é a régua funcionando. Se incomodar,
  amostre negativas no teste (decisão de método, não otimização).
