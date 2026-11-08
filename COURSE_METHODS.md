# COURSE_METHODS.md — lecture techniques used in the report

Page numbers are PDF page numbers of the files in `lecture_slides/`.

| Technique used in the report | Where in the lectures | How it is used |
|---|---|---|
| Analysis framework: input size → basic operation → count → closed form → asymptotic class | Slide01 pp. 3–9 | Structure of every one of the 12 analyses |
| Definitions B(n) = min τ(I), W(n) = max τ(I), A(n) = Σ τ(I)p(I) | Slide01 pp. 10–13 | Formal definition of the 12 quantities; exhaustive checks compute exactly these |
| A(n) needs a probability distribution | Slide01 pp. 16–17 | Variant distribution p_a = p_b = 2/5, p_c = 1/5, independent positions |
| "Realistic" basic operation: count bounded by constant multiples of real time | Slide01 pp. 5–6 | Choice of group (4) as the correct basic operation (§4 of the assignment) |
| Loop increments are "not typical/characteristic" basic operations | Slide02 p. 22 (linear search) | Discussion of why group (2) misses the dominant inner loop |
| Θ, O, Ω definitions with explicit constants c1, c2, n0 | Slide01 pp. 27–38 | Every asymptotic claim is proved with explicit constants |
| Limit analysis, properties of orders | Slide01 pp. 48–60 | Showing c^n (here (4/5)^n) terms vanish, ordering of classes |
| Logarithmic order, base irrelevant | Slide01 pp. 65–66 | ⌊log₂ n⌋ + 1 ∈ Θ(log n) |
| Summations Σ i = n(n+1)/2, Σ i^p ∈ Θ(n^{p+1}), geometric series | Slide02 pp. 2–4, 8–14 | Closed forms of the nested-loop sums |
| Linear search B/W/A, A(n) = Σ i·p_i | Slide02 pp. 21–27 | Template for writing best/worst inputs and expectations |
| Binary search: number of halvings ⌊log₂ n⌋ + 1, bounding with 2^{i−1} ≤ n < 2^i | Slide02 pp. 28–30 | Exact iteration count of the `while k > 0` loop |
| Insertion sort: B(n), W(n) argued per iteration; A(n) = E[τ] = Σ E[τ_i] (divide into consecutive steps, linearity of expectation) | Slide03 pp. 5–14 | Main template: τ = Σ_i τ_i over outer-loop iterations, per-iteration min/max for proofs, E[τ_i] for A(n) |
| Type-1 recurrence x(n) = a·x(n−1) + f(n), forward/backward substitution | Slide04 pp. 5–9, 21–23 | E[s_{i+1}] = (4/5)E[s_i] + 2/5 solved by backward substitution |
| MaxMin A(n): split τ = τ1 + τ2, conditional expectation E[X | Y], indicator-style counting | Slide05 pp. 12–21 | Conditioning on X_i (the current character) and independence of s_i from X_i |
| Limitations of asymptotic analysis (constants, low-order terms) | Slide05 pp. 54–55 | Interpreting small-n timing, interpreter overhead |

Not used: Slide06–Slide07 (parallel algorithms, PRAM) — not relevant to a sequential
operation-count analysis. Master theorem (Slide04 pp. 28–31) — no divide-and-conquer recurrence appears.

Advanced machinery deliberately avoided: generating functions, Markov-chain stationary
distributions, martingales. The only "probability" tools are expectation of a discrete random
variable, linearity of expectation, indicators, independence, and conditioning on the current
character — all of which appear in Slide01, Slide03 and Slide05.
