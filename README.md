A script to determine the ex$\left(K_{n_1, \dots, n_m}, k K_r\right)$ for arbitrary $n_1, \dots, n_m$, $k$, and $r$. Recall that, for graphs $G$ and $H$, ex($G,H$) denotes the maximum number of edges in a subgraph of $G$ that contains no copy of $H$. De Silva et al. and Wagner considered ex($G,H$) were $H$ is $k$ disjoint $K_r$'s and $G$ is a complete multipartite graph (https://doi.org/10.48550/arxiv.1610.00777). The following is known regarding such extremal numbers.

1. For any integers $ k \leq n_1 \leq n_2 \leq \dots \leq n_r$ $\textnormal{ex}(K_{n_1, \dots, n_r}, k K_r) = \left( \sum_{1 \leq i < j \leq r} n_i n_j \right) -n_1n_2 + n_2(k-1)$ (https://doi.org/10.48550/arxiv.1610.00777)).
2. For all integers $k \leq n$, we have ex$\left(K_{n,n,n,n}, k K_3\right) \geq 4n^2 + (k-1)n$ (https://arxiv.org/abs/1903.05495).

This problem can be phrased with the following ILP. Fix some $n_1,\dots, n_m$, $k$, and $r$. We wish to find the subgraph $H$ of $K_{n_1,\dots,n_m}$ with the maximum number of edges such that $H$ contains no $kK_r$. For each edge $ e $ in $E(K_{n_1,\dots,n_m})$ let $x_e$ be an indicator variable giving the truth value of the statement $ e \in E(H)$. To ensure that $H$ contains no $kK_r$, for every collection of $k \binom{r}{2} $ edges $e_1, e_2, \dots, e_{k \binom{r}{2} } $ forming a $kK_r$, we add the constraint $\sum_{i =1}^{ k \binom{r}{2} } e_i &\leq k \binom{r}{2} -1.$ As we wish to maximize $ \left| E(G) \right|$, our objective function is simply $ \sum_{e \in E(K_{n_1,\dots, n_m})} x_e$.

See run.py for an implementation of this ILP. My code uses backtracking to determine all edges in a $K_{n_1, \dots, n_m}$ as well as all possible collections of $k K_r$'s to form the constraints. I used a Gurobi solver for the ILP portion of my code. Input $n_1, \dots, n_m$, $k$, and $r$ at the bottom of the script. I have tested the results against the bounds given in Theorem 1 and 2. 

This work was inspired by https://arxiv.org/abs/1903.05495.
