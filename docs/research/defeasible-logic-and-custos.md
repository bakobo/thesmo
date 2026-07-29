# Custos vs. the defeasibility literature: a hostile-witness report

Research date: 2026-07-29. Prepared as a test of the hypothesis, not a confirmation of it.

## Verification legend

Every claim below carries a marker. Please hold me to them.

- **[V]** — I fetched the source and read its own text (or its verbatim abstract). Quotes are from the source.
- **[V\*]** — I fetched the source's HTML and a summarizing model extracted names/quotes from real page content. Element/attribute names are reliable; interpretive glosses should be spot-checked.
- **[S]** — Comes from a search-engine synthesis that quoted the source, but I did not read the source myself. Treat as "the literature says roughly this, citation is right, wording may drift."
- **[R]** — Recalled from training, unverified in this session. **Do not repeat these without checking.**
- **[A]** — My own analysis/mapping. Not a literature claim. This is where the value is, and also where the risk is.

A methodological note you should know: two PDF fetches (the Delgrande survey, the Catala paper) came back as unparsed binary, and the fetch tool's summarizer *hallucinated a clean comparison table* for the Delgrande survey rather than reporting failure. I discarded it and extracted the PDF text locally instead. If you ever see me produce a suspiciously tidy table from a PDF, distrust it.

---

## 0. Bottom line

Your hypothesis is **substantially correct, with one important correction.**

Correct: Custos has reinvented a defeasibility calculus. It has a name, a formal home, forty years of literature, decidability and complexity results, and at least four engineered artifacts (Catala, IBM CommonRules, LegalRuleML+SPINdle/Turnip, Blawx/s(CASP)) that solve overlapping problems.

The correction: **Custos is not a non-monotonic logic at all, and that is the most consequential fact in this report.** By asserting monotonicity over evidence growth and no backward transitions, Custos has left the non-monotonic-reasoning family and joined a different one: monotone, lattice-valued, fixpoint semantics — Belnap/Fitting bilattices on the logic side, CRDTs and the CALM theorem on the systems side. That is a *coherent and arguably brilliant* fit for a no-consensus KERI substrate. But it is purchased with an expressiveness price that Custos does not appear to have priced, and the unpaid bill has a name: **reinstatement**. See §5, which is the section to read if you read only one.

The single most uncomfortable finding: the three "open defects" you describe as reducing to "how do you impose a total order on competing defeats" do **not** reduce to that. The literature is nearly unanimous that you should *not* impose a total order, and that determinism is obtained by other means entirely (§1.4). Your defects more plausibly reduce to a different question — *is the object you require to be monotone the right object?* — and the literature has a clean answer (§5.4).

---

## 1. Defeat priority ordering (highest-value question)

### 1.1 The name and the formal home

What Custos calls "defeater classes, enumerated and ranked" is, in the literature, the **superiority relation** (defeasible logic), the **preference/priority relation on defaults** (default logic), the **argument ordering** (structured argumentation), or **prioritized conflict handling** (logic programming). The umbrella term is **preference handling in nonmonotonic reasoning**, and it has a canonical survey:

> James P. Delgrande, Torsten Schaub, Hans Tompits, Kewen Wang, "A Classification and Survey of Preference Handling Approaches in Nonmonotonic Reasoning," *Computational Intelligence* 20(2):308–334, 2004. PDF: https://www.cs.uni-potsdam.de/wv/publications/DBLP_journals/ci/DelgrandeSTW04.pdf **[V — I extracted and read the PDF text]**

Its opening paragraph is uncomfortably on-point for Custos:

> "In legal reasoning, laws may conflict. Conflicts may be resolved by principles such as ruling that newer laws will have priority over less recent ones, and laws of a higher authority will have priority over laws of a lower authority. For a conflict among these principles, one may further decide that the 'authority' preference takes priority over the 'recency' preference." **[V, verbatim modulo OCR]**

That is *lex posterior*, *lex superior*, and a meta-priority between them — i.e., exactly Custos's "defeater classes are enumerated and ranked," identified as a known problem in the first 200 words of a 22-year-old survey.

### 1.2 The classification axes you should be using

The survey's axes (all **[V]**, read from the text):

1. **Prescriptive vs. descriptive.** Prescriptive: `<` specifies *the order in which rules are to be considered for application*. Descriptive: `<` is a ranking on *desired outcomes* — the preferred situation is one where the most preferred rules are applied. These are genuinely different and give different answers. Custos, as described, is **prescriptive** (a fold applies clauses in an order to reach a verdict). Consequence: you inherit the prescriptive family's known behaviour, including that a lower-ranked defeat can never be used to enable a higher-ranked one.
2. **Static vs. dynamic.** Static = fixed when the theory is written; dynamic = determined during inference. "An approach with external preferences will, of necessity, have static preferences." **[V]** Custos's defeater-class rank is static and external. That is the tractable choice; see §1.6 for what you give up.
3. **Meta-level vs. object-level.** Is `<` imposed externally on rules, or is it a first-class term you can reason about (and therefore defeat)?
4. **Properties of the ordering.** This is the money quote, verbatim from the survey **[V]**:

> "The majority of approaches assume that the relation `<` is an (irreflexive) partial order; this seems to be the minimal notion that would justify the use of the term 'preference'. However, one might go on and impose further conditions, such as connectivity or (in the case of infinite orderings) well-foundedness. **Some approaches assume that `<` is a total order, since orderings of this kind are easier to deal with.** As an intermediate approach between these two possibilities... in some approaches `<` is assumed to be a partial order, but this is extended to a set of total orders before applying the preference relation."

And on how the total-order extension is actually used **[V]**:

> "One may define preferred extensions in terms of total orders extending the given partial order `<` (as, e.g., done in the approach of Brewka [1994]). **Each such total order then is used to generate a preferred extension.**"

Read that twice. In the mainstream construction, going from a partial order to total orders **multiplies** the answers — one extension per linearization. Totality per se does not buy you determinism; it buys you *a* determinate answer only if you also pick *which* total order, which is the original problem displaced by one level.

### 1.3 Adequacy tests your ranking scheme must pass

Brewka & Eiter's two principles, as stated in the survey **[V, close paraphrase of the verbatim text]**:

- **Principle I.** Let `B₁`, `B₂` be extensions of a prioritised theory `(T,<)` generated by rules `R ∪ {δ₁}` and `R ∪ {δ₂}` respectively, `δ₁,δ₂ ∉ R`. If `δ₁` is preferred over `δ₂`, then `B₂` is not a preferred extension of `T`. ("Generated" is crucial: for extension `B`, rule `δ` is *generating* iff its prerequisites are in `B` and it is not defeated by `B`.)
- **Principle II.** Let `B` be a preferred extension of `(T,<)` and `δ` a rule at least one of whose prerequisites is not in `B`. Then `B` is a preferred extension of `(T ∪ {δ}, <′)` whenever `<′` agrees with `<` on priorities among rules in `T`. I.e., **adding an inapplicable rule must not change the verdict.**

The survey notes "While Principle I is widely accepted, descriptive approaches do not satisfy Principle II in general" **[V]**.

**[A] These are precisely the two conformance tests Custos should be running against its fold, and Principle II is a monotonicity property in disguise** — it says adding irrelevant evidence must not perturb the judgment. For a standard whose whole selling point is byte-identical reproducibility across strangers holding different-sized bundles, Principle II is not academic hygiene; it is a security property. Its violation is an attack: an adversary commits an inapplicable-but-priority-bearing clause and flips your verdict. I would write Principle I and II into the Custos test suite verbatim.

### 1.4 How the literature actually gets determinism (the important part)

Five distinct mechanisms. **None of them is "impose a total order on defeats."**

**(a) Skeptical semantics that returns "undecided."** Defeasible logic (Nute; Antoniou, Billington, Governatori, Maher) keeps the superiority relation a *partial* order and simply fails to conclude when a conflict is unresolved. From the primary source **[V — I downloaded arXiv cs/0003082 and read the extracted text]**:

> "In Defeasible Logic, priorities are **local** in the following sense: Two rules are considered to be competing with one another only if they have complementary heads. Thus, since the superiority relation is used to resolve conflicts among competing rules, it is only used to compare rules with complementary heads; the information `r > r′` for rules `r, r′` without complementary heads may be part of the superiority relation, but has no effect on the proof theory." **[V]**

> "...it makes no sense to have both `r > r′` and `r′ > r`. Consequently, we will focus on cases where the superiority relation is **acyclic**." **[V]**

So the two requirements are **locality** (only compare genuinely competing rules) and **acyclicity** — not totality. Unresolved conflict yields `-∂q` and `-∂¬q`: undecided, deterministically. Determinism comes from the *proof theory*, not the order.

Citation: G. Antoniou, D. Billington, G. Governatori, M. J. Maher, "Representation Results for Defeasible Logic," *ACM Transactions on Computational Logic* 2(2):255–287, 2001. Preprint: https://arxiv.org/abs/cs/0003082

**(b) Acyclicity / well-foundedness collapses all semantics to one.** Dung's theorem (reported as Thm 30 of Dung 1995): if the argumentation framework is well-founded — for finite frameworks, iff the attack graph is **acyclic** — then the grounded extension is the *unique* stable, complete, and preferred extension. The grounded extension is always unique for any framework; the other semantics are what multiply. **[S]**

**[A] This is the theorem Custos should be quoting.** Your determinism requirement is satisfied by *acyclicity of the defeat graph plus grounded (skeptical) semantics*. Ranking is not needed for determinism; it is needed only to convert an "undecided" into a verdict — a strictly separate and optional design goal.

**(c) Acyclicity/stratification in prioritized logic programming: Grosof's courteous logic programs.** From the Delgrande survey's own catalog entry, verbatim structure **[V]**:

> "[Grosof, 1997]: Host system: **acyclic** extended logic programs. Strategy: prescriptive. Preference: preference on rules; dynamic preference; strict partial order only on stratified logic programs. Approach: meta-level; apply the preference ordering 'directly'. Complexity: same level as host system. Distinguished properties: (1) **each ordered logic program without recursion has a unique model**; (2) Brewka and Eiter's Principle I and II are satisfied. Related work: IBM CommonRules project."

Supporting detail **[S]**: the mechanism is *mutual-exclusion (mutex) constraints* that scope conflict locally plus `overrides(rule1, rule2)` as an ordinary predicate over rule labels; the "courteous compiler" translates a courteous LP into an ordinary LP with tractable overhead, and the result is a consistent, tractably computable, unique answer set. Citations: B. N. Grosof, "Prioritized conflict handling for logic programs," *ILPS 1997*, 197–211; "Courteous logic programs: prioritized conflict handling for rules," IBM Research Report RC 20836, 1997; compiler: IBM RR RC21472, 1999; shipped in **IBM CommonRules** with a BRML XML interchange syntax.

**[A] Grosof is the closest prior art to Custos's engineering brief that I found**: partial order (not total), local conflict scope, guaranteed unique model, tractable, compiles to a simpler substrate, and an XML wire format for interchange. It even satisfies Principles I and II. If Custos's ranking apparatus does not do at least this much, it is behind 1997.

**(d) Derive a total preorder from the rule set instead of authoring one: System Z / rational closure.** Pearl's System Z computes a *unique* ranking of defaults **from the knowledge base itself**, by iterated "tolerance" partitioning, respecting specificity. **[S]** The reported abstract language: inferences "are supported by a **unique priority ordering on rules which is syntactically derived from the knowledge base**, an ordering that accounts for rule interactions, respects specificity considerations, and facilitates the construction of coherent belief states," with practical algorithms for consistency-checking, computing the rule ordering, and query answering. The z-partition is "the unique ordered partition `(D₀,…,D_k)` of `D` such that each `D_i` is the set of all defaults in `D − ⋃{D_j | j<i}` that are tolerated by `D − ⋃{D_j | j<i}`." Citations: J. Pearl, "System Z: a natural ordering of defaults with tractable applications to nonmonotonic reasoning," TARK 1990; Goldszmidt & Pearl, "On the relation between rational closure and System Z" (NMR 1990) and "Qualitative probabilities for default reasoning, belief revision, and causal modeling," *AI* 84:57–112, 1996; equivalent to Lehmann & Magidor's **rational closure** (1992). **[S]** Known limitation **[S]**: System Z and its relatives "fail to allow full inheritance of properties and allow unwanted specificity relations."

**[A] For Custos this is a live option and possibly the best one:** rather than a human-authored, politically contestable rank order over defeater classes, *compute* the canonical rank from the clause set by specificity, and publish the algorithm. It is unique, syntactically derived, and therefore byte-reproducible by a stranger who holds the same clause set — which is precisely your reproducibility criterion. It also removes "who decided the ranking?" from governance disputes.

**(e) Numeric/stratified total preorder → several distinct deterministic entailments.** If you *do* have a total preorder on strata, the canonical treatment is Benferhat, Cayrol, Dubois, Lang, Prade, "Inconsistency management and prioritized syntax-based entailment," *IJCAI'93*, 640–645, https://www.ijcai.org/Proceedings/93-1/Papers/090.pdf **[S]**. They study several priority-based inference relations over inconsistent sets, including one "based on a **lexicographic ordering of maximal consistent subsets**" which "refines Brewka's preferred sub-theories," with comparisons to System Z and possibilistic logic. The named family (possibilistic/linear-order entailment, **best-out**, **lexicographic**) matters: *the same total order yields several different deterministic answers depending on which aggregation you choose.* **[S/A]** So even total order + determinism does not pin down a unique semantics; Custos must name its aggregation rule explicitly, and "we impose a total order" does not name it.

**(f) Refuse to answer: Catala's runtime conflict error.** See §3. When two same-priority exceptions both apply, Catala **aborts** with a conflict error `⊛`. That is a legitimate, honest, and engineerable fourth answer to your problem, and it is the one taken by the most mature artifact in the field.

### 1.5 Which approaches give a unique answer vs. multiple extensions

Synthesized; individual markers as shown.

| Approach | Order required | Answer |
|---|---|---|
| Defeasible logic, `+∂`/`-∂` tags (Nute; Antoniou et al.) | acyclic, **local**, partial | **Unique** (skeptical; unresolved ⇒ undecided) **[V]** |
| Dung grounded semantics | none (order optional) | **Unique**, always **[S]** |
| Dung preferred / stable | none | **Multiple** (even cycles ⇒ many; odd cycles ⇒ stable may not exist) **[S]** |
| Well-founded / acyclic framework | acyclic | **Unique**, all semantics coincide (Dung Thm 30) **[S]** |
| Brewka preferred subtheories (1989/94) | partial, extended to total orders | **Multiple** — one per linearization **[V]** |
| Grosof courteous LP | strict partial order, acyclic/stratified host | **Unique** model; satisfies Principles I & II **[V]** |
| System Z / rational closure | order *computed*, total preorder | **Unique** **[S]** |
| Lexicographic / best-out (Benferhat et al.) | total preorder on strata | Unique **per chosen aggregation**; family of them **[S]** |
| ASPIC+ with last-link / weakest-link ordering | preorder on rules/premises | Inherits Dung: unique under grounded, multiple otherwise **[S]** |
| Catala prioritized default logic | static per-scope tree (acyclic by construction) | Unique or **hard error** **[V]** |
| Horty fixed-priority default theories | partial order over defaults | **Multiple** extensions; skeptical/credulous choice left to user **[S]** |

ASPIC+ detail worth having **[S]**: Modgil & Prakken, "The ASPIC+ framework for structured argumentation: a tutorial," *Argument & Computation* 5(1):31–62, 2014; Prakken, "An abstract framework for argumentation with structured arguments," *A&C* 1(2):93–124, 2010. Two "reasonable" orderings are standard: **last-link** (compare the last defeasible rules used — Prakken & Sartor's "relevant set") and **weakest-link** (compare all fallible elements on their weakest). Crucially: "preference-based argumentation frameworks don't recognise that **undercutting attacks succeed regardless of preferences**," and bolting preferences on abstractly "leads to violations of subargument closure and consistency." **[S]**

**[A] That last point is a direct hit on Custos.** If defeater classes are ranked and *all* defeat is adjudicated by rank, then Custos has no analogue of an **undercutter** — a defeat that succeeds irrespective of priority because it attacks the *applicability of the inference itself* rather than its conclusion. Real governance is full of these ("the signer lacked authority", "the evidence is out of time"). Custos's `self-convicted` is a special case of an undercutter that has been promoted to its own value; the general case seems to be missing. ASPIC+ says the rank-immune category must exist. That is a concrete gap, and it is orthogonal to your ordering problem.

### 1.6 The result that should make you most uncomfortable

From the same primary source, verbatim from the extracted text **[V]**:

> "As a consequence, we show that **for every defeasible theory T there is an equivalent theory T′ which has an empty superiority relation, and neither defeaters nor facts.**"

The rest of that paper builds *modular* and *incremental* transformations achieving it (modularity = "a transformation may be applied to a part of a program or theory without the need to notify or modify the rest"; incrementality = "an update in the original theory should have cost proportional to the change") **[V]**. The technique: introduce fresh intermediate literals between rule bodies and heads, and simulate the priority effect with new defeasible rules attacking those literals **[V]**.

**[A] What this means for Custos.** The ranked-defeater-class apparatus is **eliminable**: it carries no expressive power that structured clauses do not already have, and the elimination is modular and incremental (i.e., compatible with append-only evidence and with amending one clause without republishing the corpus). Two consequences:

1. You should stop treating "defeater classes are enumerated and ranked" as a *semantic primitive of the calculus*. It is a *presentation* convenience over a normal form. The standard would be stronger if it defined the normal form (empty superiority relation) as the semantic ground truth and the ranked presentation as sugar with a specified compilation — because then reproducibility only has to be defended for the normal form, and the ranking becomes a governance artifact rather than a logic artifact.
2. It does **not** mean the ranking decision is unnecessary. Elimination *relocates* the decision into rule structure; it cannot manufacture it. Any claim that a formalism will tell you whether *lex superior* beats *lex specialis* is false — that is a substantive legal-political choice. **[A]** Custos's real open defect is therefore not formal; it is that a political choice is currently sitting where a formal invariant is claimed to be. The literature's honest options are: publish the choice (Grosof/LegalRuleML style), compute it (System Z), or refuse to make it (defeasible logic's `undecided`, Catala's `⊛`).

### 1.7 Priorities about priorities

Legal reality is that the priority relation is itself contested. The literature has this too, and it costs you determinism:

- Horty's **fixed-priority** vs. variable-priority default theories; in the latter "the priority relation among defaults... is itself established through default reasoning — since a default supplying priority information is itself a default, the information it provides concerning priority between two other defaults is defeasible as well," with the ordering "lifted" to the metalevel; lineage to Brewka (1994, 1996). J. F. Horty, *Reasons as Defaults*, OUP 2012; manuscript at http://www.horty.umiacs.io/courses/readings/rd-root.pdf **[S]**
- Prakken, "Reasoning about priority relations," in *Logical Tools for Modelling Legal Argument* — the standard reference for arguing about *lex superior / posterior / specialis* interactions. **[S]**
- Prakken & Sartor's position that "the evaluation criteria are themselves debatable, so argumentation systems should allow defeasible arguments about those criteria." **[S]**
- Governatori et al., "Computing Defeasible Meta-logic," JELIA, LNCS 12678, 69–84 — defeasible reasoning *about* rules. **[S]**

**[A] Custos's static, externally-fixed class rank is the tractable choice, and I would keep it** — but say so explicitly as a limitation, because governance disputes will be *precisely* about the rank order, and a standard that makes its most contested element unamendable-by-argument will be amended by fork instead.

### 1.8 Complexity and decidability

- **Propositional defeasible logic: linear time.** M. J. Maher, "Propositional defeasible logic has linear complexity," *TPLP* 1(6):691–711, 2001, doi:10.1017/S1471068401001168 — "inference in the propositional form of the logic can be performed in linear time, which contrasts markedly with most other propositional nonmonotonic logics, where inference is intractable"; implemented as **Delores**. **[S]**
- Later parallel-friendly variants also linear (Rethinking Defeasible Reasoning, *TPLP*; arXiv:2001.00406) **[S]**; the 2001 algorithm "does not easily support parallelism, nor does it easily extend to first-order defeasible logics" **[S]**.
- Argumentation and ASP semantics are by contrast intractable in general (NP/coNP-complete and up for preferred/stable acceptance). **[R — I did not verify the specific completeness results in this session.]**

**[A] This is a strong argument for Custos to consciously locate itself in the defeasible-logic family rather than the argumentation/ASP family.** A standard whose core promise is "any stranger can recompute the judgment byte-identically" needs the *verifier* to be cheap and total. Linear-time propositional DL is exactly that. If Custos's fold is Turing-complete or its evaluation is search-based, the reproducibility promise is only as good as the weakest re-implementation. Bounding the fold to a linear-time fragment would be a defensible headline property — and it is a published theorem you can cite rather than a claim you must defend.

---

## 2. Is the four-valued codomain a known structure?

Short answer: **yes, and it is a *better* known structure than you probably realise — but not the one you'd guess.** It is not defeasible logic's proof tags. It is Belnap's four values with the *information* ordering, and the "two currents that must never merge" is the defining feature of a **bilattice**.

### 2.1 Not defeasible logic's proof tags

Verified from the primary source **[V]** (arXiv cs/0003082, extracted text; `Δ` and `∂` reconstructed from the glyph mapping):

> A conclusion "can have one of the following four forms: `+Δq` which is intended to mean that `q` is definitely provable in `D`. `-Δq` which is intended to mean that we have proved that `q` is not definitely provable in `D`. `+∂q` which is intended to mean that `q` is defeasibly provable in `D`. `-∂q` which is intended to mean that we have proved that `q` is not defeasibly provable in `D`." Also: "If we are able to prove `q` definitely, then `q` is also defeasibly provable."

And the five components **[V]**: "There are five kinds of features in Defeasible Logic: facts, strict rules, defeasible rules, **defeaters**, and a superiority relation among rules."

**[A] These four tags are *not* a four-valued codomain.** They are two polarities (`+`/`-`) crossed with two strengths (`Δ`/`∂`), applied *per literal*, so the tag space per proposition `p` is `{±Δ, ±∂} × {p, ¬p}` — eight cells, of which the coherent combinations give you roughly: definitely-provable / defeasibly-provable / provably-not-provable / (unresolved). Custos's codomain maps onto DL only loosely:

| Custos | Defeasible logic | Fit |
|---|---|---|
| `affirmed` | `+∂p` (or `+Δp` for strict) | good; DL even gives you the affirmed-strictly/affirmed-defeasibly distinction Custos lacks **[A]** |
| `defeated(citation)` | `+∂¬p` — the *opposite* is defeasibly proved | good, but DL carries no citation **[A]** |
| `pending(req)` | `-∂p ∧ -∂¬p` — both refuted, nothing concluded | structurally right, but DL's is a *negative* fact ("we proved you can't prove it"), not a *typed requirement* **[A]** |
| `self-convicted` | **no counterpart.** DL is a skeptical logic that by design "does not support contradictory conclusions" **[S]** | **bad fit** |

So DL gives you three of four values and explicitly refuses the fourth. Also note DL's `-∂` is not "we don't know yet" — it is a *proved* negative, computed against a closed theory. **[A] That difference matters enormously for §5:** DL's `-∂p` is not monotone under adding facts, whereas Custos's `pending` is meant to be.

### 2.2 The actual home: Belnap's FOUR under the knowledge ordering

Belnap's four values: `t`, `f`, `n` (none — no information), `b` (both — contradictory information). Two lattice orders on the same carrier **[S, from a synthesis quoting the sources]**:

- **truth order** `≤_t`: `f ≤ n ≤ t` and `f ≤ b ≤ t`; meet/join written `∧`, `∨`.
- **knowledge/information order** `≤_k`: `n ≤ t ≤ b` and `n ≤ f ≤ b`; meet/join written `⊗` (consensus), `⊕` (gullibility). "Inspired by domain theory, initiated by Scott... this is precisely why monotonicity/continuity in `≤_k` underwrites fixed-point constructions."

Both orders together form an **interlaced bilattice**. Ginsberg introduced bilattices as an algebra for Belnap's connectives; Fitting used them for logic-programming semantics. Fitting's own motivation for the fourth value is *your* use case: "an application to a logic programming language supporting spatially distributed programs, where a fourth value `⊤` naturally denotes **conflicting information received from different nodes in a computing network**." **[S]** And Belnap's original 1977 framing is about "integrating data from various data sources" where `b` represents "the inconsistency of claiming both 'True' and 'False'." **[S]**

Key citations: N. D. Belnap, "A useful four-valued logic" (1977); M. Ginsberg, "Multivalued logics: a uniform approach to reasoning in AI," *Computational Intelligence* 4:265–316, 1988 **[R for the exact volume/pages]**; **M. Fitting, "Bilattices and the semantics of logic programming," *Journal of Logic Programming* 11:91–116, 1991** **[S]**; A. Avron, "The structure of interlaced bilattices" / "The logical role of the four-valued bilattice" **[S]**; recent survey: Tomáš Jakl, "Four Imprints of Belnap's Useful Four-Valued Logic in Computer Science," *Studia Logica*, 2026, arXiv:2503.20679 — abstract verified verbatim **[V]**: reviews d-frames, linear logic, Blame Calculus and **LVars**, with "the key to three of these connections... via the **twist-product representation of bilattices**."

### 2.3 The mapping — and why "two currents that never merge" is exactly right

**[A] My analysis, not a literature claim. This is the central structural finding of the report.**

```
Custos                    Belnap FOUR         knowledge order ≤_k
pending                   n  (none)           ⊥ — least
affirmed                  t                   incomparable middle
defeated                  f                   incomparable middle
self-convicted            b  (both)           ⊤ — greatest, absorbing
```

Under this reading, every one of Custos's structural axioms becomes a known algebraic fact rather than a design assertion:

- **"No backward transitions"** = the fold is **monotone in `≤_k`**. Standard, and it is the condition Scott/Kleene/Fitting fixpoint semantics is built on.
- **"Monotonicity over evidence growth"** = the fold is a monotone (ideally Scott-continuous) map from the evidence lattice to FOUR.
- **"Defeat annihilates upward"** = propagation along the **truth order** — `∧` over conjunctive requirements: one `f` conjunct forces `f`.
- **"Duplicity taints upward"** = propagation along the **knowledge order** — `⊕` (gullibility join): one `b` input forces `b`, because `b` is `≤_k`-top and absorbing for `⊕`.
- **"The two currents must never merge"** = the two lattice structures of a bilattice are *distinct orders on the same carrier*. The **interlacing conditions** state precisely how they coexist: each order's operations are monotone with respect to the other order. That is the formal content of "coexist coherently without merging."

If that mapping holds, Custos's judgment codomain is `FOUR`, its two propagation currents are the two lattices of the four-valued bilattice, and it has an off-the-shelf 45-year-old algebra with representation theorems (every bilattice is a twist product **[S]**), a fixpoint theory, and a logic-programming semantics. **I would be surprised if this mapping is wrong, but I have not proved it against the Custos spec — I have only read your prose description.** It should be checked clause by clause, and if it holds, cited.

### 2.4 The other near-miss: Caminada labellings

Argumentation's standard three-valued labelling is `{in, out, undec}` — "an argument is labelled **in** if all its attackers are labelled **out**, and **out** if it has at least one attacker labelled **in**; otherwise **undec**" **[S]**, introduced as **reinstatement labelling** (Caminada 2006) and proved equivalent to Dung's complete extensions; `undec(Lab) = ∅` characterises stable, maximal `in` gives preferred, etc. (Caminada & Gabbay 2009). **[S]**

`in / out / undec` = `affirmed / defeated / pending`. Exactly. And **[S]**: "there is no label for 'both in and out', which is precisely what **paraconsistent four-valued labellings** add" — a four-valued labelling induced by a subset of arguments "is called a *paraconsistent labelling* (or p-labelling), used for **conflict-tolerant** semantics where in/out labels may overlap," grounded in Belnap 1977. See Arieli & Caminada on conflict-tolerant/paraconsistent argumentation semantics **[S]**.

**[A] So: Custos's four values are a paraconsistent (four-valued) labelling of a defeat graph.** That phrase is the literature-standard name for the object. It also tells you where to look for existing algorithms and complexity results, and — see §5 — where to look for the bad news, because the labelling is named for *reinstatement*.

### 2.5 On `pending(typed-requirement)` specifically

Custos's `pending` carries *what is missing*, with a "cure species." That is more than `undec`. The literature names for "what would have to be added so that this conclusion holds":

- **Abduction** — abductive explanation / abductive argumentation (e.g. "Abduction and Dialogical Proof in Argumentation and Logic Programming," arXiv:1407.3896) **[S]**.
- **Enforcement** in argumentation dynamics — Baumann & Brewka, "Expanding Argumentation Frameworks: Enforcing and Monotonicity Results," COMMA 2010, FAIA 216:75–86, which "shows both **possibility and impossibility results** related to the problem of enforcing a desired set of arguments." **[S]**

**[A] Take the impossibility results seriously.** Custos requires that `pending` *always* names a typed requirement. Enforcement is known to be sometimes impossible, and abduction is in general more expensive than deduction. A standard that mandates a total, always-computable cure function is making a stronger claim than the enforcement literature supports. At minimum, Custos needs a `pending` sub-case for "no finite cure exists" or "cure not computable from the current bundle," or the mandate should be softened to "names a *sufficient* requirement if one is derivable in the fragment."

---

## 3. Catala

**What it is.** A domain-specific language for statutory law, in which each paragraph of legal text is immediately followed by its executable transcription (literate programming), compiled to OCaml/Python/JS/etc.

**Who.** Denis Merigoux, Nicolas Chataing, Jonathan Protzenko (Inria PROSECCO + Microsoft Research), with legal co-authors **Liane Huttner** and **Sarah Lawsky**, and later Raphaël Monat. **[V]**

**Semantic basis — your belief is correct.** From the paper (ar5iv HTML, read) **[V]**:

> "the one closest to the purposes of the law is known as **prioritized default logic**... **Lawsky** argues that this flavor of default logic is the best suited to expressing the law. We concur."

Attribution is to **Brewka & Eiter (2000)** for prioritized default logic **[V]**, and to Sarah Lawsky for the legal argument (see §3.1).

**How priority actually works — and this is the part Custos should study.** Catala does *not* implement full prioritized default logic. Verified **[V]**:

- Each variable definition is "its own world" — an isolated **static priority tree** with mutually-exclusive exceptions; "priorities are baked directly in the syntax tree of each definition"; "the pre-order is derived directly from the syntax tree of rules and definitions."
- Therefore: **priority is local (per definition/scope), static, and acyclic by construction** — no global ordering, ever.
- Scopes provide modular abstraction following the law's implicit structure; no general recursion, no fixpoints, deliberately non-Turing-complete.
- Rationale, verbatim: this made the semantics "tractable, both in the paper formalization and in the formal proof."

**The default calculus and its conflict handling** **[V]**. Core term: `⟨e₁,…,eₙ | e_just :- e_cons⟩` — exceptions, justification, consequence. Reduction:

- exactly one exception non-empty ⇒ return it;
- **two or more exceptions non-empty ⇒ raise `⊛`, a conflict error, fatal under any context.** The paper's own words: "if two or more exceptions are non-empty, **we cannot determine the priority order between them, and abort program execution**";
- no exception applies and justification true ⇒ consequence;
- no exception applies and justification false ⇒ `∅`, an *empty error*, which "propagates only through regular contexts."

**[A] This is the single most directly transferable design lesson in the report.** The most mature legal-computation artifact in existence, having chosen prioritized default logic on the advice of a tax-law professor, concluded that (i) priority must be **local and syntactic**, never a global rank, and (ii) when priority is indeterminate the correct behaviour is **to fail loudly, not to invent a tiebreak**. Custos's requirement that "one canonical defeat must be selected deterministically" is the opposite choice. It may still be right — a distributed verifier cannot "abort" as usefully as a benefits calculator can — but you should be able to say why you diverged from Catala, and you probably need a fifth value or a distinguished `defeated(⊛)` for "irresolvably multiply defeated," so that the *fact of indeterminacy* is itself reproducible rather than papered over by an arbitrary total order.

Note also the two distinct error values `⊛` (conflict, fatal) and `∅` (empty, propagates through regular contexts). **[A] Catala independently arrived at two propagation currents that must not be merged** — one absorbing/fatal, one context-sensitive. That is suspiciously parallel to Custos's "defeat annihilates" vs. "duplicity taints" and to the bilattice picture in §2.3. Three independent arrivals at the same structure is evidence the structure is real.

**Statute/code pairing** **[V]**: literate programming — "each paragraph of law is immediately followed by its Catala transcription"; surface syntax co-designed with lawyers (`definition`, `consequence`, `under condition`); a metadata section declaring structures, scopes and context variables must precede the rules, "materializing implicit legal concepts."

**Maturity and real-law exercise.** Verified from the arXiv abstract **[V]**: correctness of "core compilation steps" proven in **F\***; evaluated on "**section 121 of the US federal income tax**" and "the byzantine **French family benefits**"; "in doing so, we uncover a bug in the official implementation." Peer-reviewed at *PACMPL* (ICFP 2021), doi:10.1145/3473582.

Follow-on maturity **[S]**:
- L. Huttner & D. Merigoux, "Catala: Moving towards the future of legal expert systems," *Artificial Intelligence and Law*, 2022, doi:10.1007/s10506-022-09328-5 — language **plus a pair-programming development process** between lawyer and programmer.
- "Rules, Computation and Politics: Scrutinizing Unnoticed Programming Choices in French Housing Benefits," *J. Cross-disciplinary Research in Computational Law*, 2023.
- Merigoux, Huttner, Monat et al., "**Coding computational laws: 20 recommendations for public administrations**," *Information & Communications Technology Law*, 2026 — https://rmonat.fr/data/pubs/2026/2026-02-16_legal_code_recos.pdf
- CUTECat: concolic execution for Catala programs, arXiv:2410.18212, exercised on French housing benefits and IRC §132.
- The Catala book (https://book.catala-lang.org/) has a chapter on real-world projects: version control, monitoring legal changes, testing, CI, automated deployment.

**Honest read on production status [S/A]:** heavily exercised on real statutes (French housing/family benefits, US IRC §121 and §132), engaged with the French administration, formally verified in part, actively developed 2021→2026, and now publishing governance recommendations for public administrations. I found **no** confirmation of a production rollout inside DGFiP. Call it "the most mature research artifact in computational law, with real administrative engagement, not yet demonstrably load-bearing in production."

### 3.1 Sarah Lawsky — the legal grounding you can cite

- S. B. Lawsky, "**A Logic for Statutes**," 21 *Florida Tax Review* 60 (2017); SSRN 3088206; PDF mirror https://gwern.net/doc/law/2017-lawsky.pdf. Argues the correct logical model of statutory reasoning (as distinct from statutory *interpretation*) is **default logic**, because statutory provisions characteristically have the form "rule subject to exceptions," which classical deductive logic handles poorly. Worked example: IRC §163(h), home mortgage interest deduction. **[S]**
- S. B. Lawsky, "Coding the Code: Catala and Computationally Accessible Tax Law," 75 *SMU L. Rev.* 535 (2022). **[S]**
- Pertierra, Lawsky, Hemberg, O'Reilly, "Toward Formalizing Statute Law as Default Logic Through Automatic Semantic Parsing," ASAIL 2017 — notable negative result: off-the-shelf semantic parsers (C&C/Boxer, CAMR) "failed to correctly parse even one of the shortest sentences in the section." **[S]**

**[A] What Custos lacks that Lawsky supplies:** an argued reason, from inside legal scholarship, why the general/exception structure (not the ranking structure) is the right primitive. If Custos wants uptake beyond the KERI community, "we chose this shape because Lawsky/Catala argue statutes have this shape" is a far stronger warrant than "we designed it this way."

---

## 4. Defeasible deontic logic and LegalRuleML

### 4.1 Governatori's line

Guido Governatori (formerly NICTA/Data61) with Antonino Rotolo, Giovanni Sartor, Régis Riveret, Francesco Olivieri, Matteo Cristani and others has spent ~25 years building **Defeasible Deontic Logic (DDL)**: defeasible logic extended with deontic modalities, temporal parameters, violations and reparation chains, norm change, and metalevel reasoning. Representative works **[S]**:

- Governatori, Rotolo, Sartor, "Logic and the Law: Philosophical Foundations, Deontics, and Defeasible Reasoning," in *Handbook of Deontic Logic and Normative Reasoning*, Vol. 2, College Publications, 2021, 655–760. **[S — this is the survey to read]**
- Governatori & Rotolo, "Logic of violations: A Gentzen system for reasoning with contrary-to-duty obligations," *Australasian J. Logic*, 2006.
- Governatori, Rotolo, Sartor, "Temporalised normative positions in defeasible logic," ICAIL 2005.
- Governatori & Rotolo, "Changing legal systems: legal abrogations and annulments in defeasible logic," *Logic J. IGPL*, 2010.
- Governatori, "On the relationship between Carneades and defeasible logic," ICAIL 2011 — maps Gordon & Walton's weighted-argument model onto DL.
- Antoniou, "Defeasible logic with **dynamic** priorities," *Int. J. Intelligent Systems*, 2004 — priorities derived from the deductive process itself rather than externally given.
- Cristani, Governatori, Olivieri, Pasetto et al., "The architecture of a reasoning system for Defeasible Deontic Logic," *Procedia CS*, 2023; "Unravel legal references in defeasible deontic logic," ICAIL 2021; "**Extraction of Defeasible Proofs as Explanations**," 2023; "Legal Explanation in Defeasible Deontic Logic via LegalRuleML," ICAIL 2025.
- Governatori's own bibliography: http://www.governatori.net/research/pubs/defeasible.html

**[A] What DDL supplies that Custos lacks:** (a) **deontic structure** — Custos's judgment is epistemic (`affirmed`/`defeated`) but governance clauses are *normative* (obligation/permission/prohibition), and the two are not the same; "this clause is affirmed" does not tell you whether a duty was violated or discharged. (b) **Violation/reparation chains** — a defeated obligation typically *triggers a secondary obligation*, and Custos's `defeated` appears to be terminal. (c) A published, tested treatment of **norm change** (abrogation, annulment, derogation) which any long-lived governed domain will need, and which is where the temporal axes bite. (d) An **explanation** apparatus built for exactly Custos's requirement — proofs extracted from the DL derivation as explanations.

On the *lex specialis / posterior / superior* trio specifically **[S]**: I found no single Governatori paper devoted to formalizing the trio; the relevant treatment is Prakken's "Reasoning about priority relations" and the temporalised-DL line. Also worth knowing **[S]**: doctrinal scholarship warns that *lex specialis* has a **wider scope** than *lex posterior* and is often used to resolve **redundancy** rather than antinomy — i.e., to *prevent* simultaneous application of a general and special rule, not to break a tie. **[A] If Custos's defeater classes were modelled on the trio, that asymmetry means the trio is not a rank order at all and modelling it as one is a category error.**

### 4.2 LegalRuleML

**Status.** OASIS **Standard** as of September 2021 (LegalRuleML Core Specification v1.0). Authors: Monica Palmirani, Guido Governatori, Tara Athan, Harold Boley, Adrian Paschke, Adam Wyner. Statements of Use from Swansea University (Livio Robaldo), CSIRO Data61, CIRSFID-AlmaAI. Spec: https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html Design paper: Athan et al., "OASIS LegalRuleML," ICAIL 2013 — http://www.governatori.net/papers/2013/icail2013legalruleml.pdf **[S for provenance, V\* for spec contents]**

**How it represents what Custos needs** (element names from the spec HTML) **[V\*]**:

| Custos concern | LegalRuleML |
|---|---|
| defeater ranking | `<lrml:OverrideStatement><lrml:Override over="#cs2" under="#cs1"/>` — `@over` = higher priority, `@under` = lower. A **binary relation over rules**, selectively defined; **no total order mandated**. |
| defeater class / rule strength | `<lrml:hasStrength>` with `<lrml:StrictStrength>`, `<lrml:DefeasibleStrength>`, `<lrml:Defeater>`; or contextually via `<lrml:appliesStrength>` in `<lrml:Context>` |
| deontic operators | `<lrml:Obligation>`, `<lrml:Permission>`, `<lrml:Prohibition>`, `<lrml:Right>` |
| consequence of defeat | `<lrml:Violation>`, `<lrml:ReparationStatement>` / `<lrml:Reparation>` with `<lrml:appliesPenalty>`, `<lrml:toPrescriptiveStatement>`; plus **`SuborderList`**: "a Deontic Specification in the SuborderList holds if all Deontic Specifications that precede it have been violated" |
| temporal parameters | `<ruleml:Time>`, `<lrml:TemporalCharacteristic>` with `<lrml:forStatus>` (e.g. `InForce`), `<lrml:hasStatusDevelopment>` (e.g. `Starts`), `<lrml:atTime>`; **three legal axes: entry into force, efficacy, applicability** |

**Canonical serialization / determinate order — the answer is no.** **[V\*]** The spec defines both a "Normalized Serialization" and a "Compact Serialization" as alternatives and does not privilege one as normative for semantics; and critically: "**LegalRuleML is independent from any legal ontology and logic framework**." Defeasible-logic concepts (`->`, `=>`, `~>`) are described, but **no specific logic is mandated**; `@iri` hooks point to external semantics.

**[A] Assessment for Custos.**
- **What it supplies:** a ratified, citable vocabulary for exactly the things Custos is inventing names for; a *checklist* of things Custos is probably missing — the three temporal axes (in-force vs. efficacy vs. applicability, which are routinely conflated and which a "committed log bytes" model is well placed to distinguish), jurisdiction of norms, authorial tracking, norm classification (constitutive vs. prescriptive), and **isomorphism** between rules and the natural-language provisions they encode; and an interchange path so a Custos domain could be exported/audited by existing legal-tech tooling.
- **What it does not supply, and what Custos genuinely has that it lacks:** determinism. LegalRuleML is deliberately semantics-agnostic and has no canonical serialization, therefore **no byte-identical reproducibility**. That is a real Custos contribution and you should claim it in exactly those terms: *Custos is to LegalRuleML what a canonical form is to an interchange format.* Note the corollary: two conforming LegalRuleML consumers can disagree; Custos's whole point is that they cannot. Pitch it that way and the standards community will understand instantly what you built.
- **Nomenclature advice [A]:** adopt `Override(over, under)` semantics and `Strict/Defeasible/Defeater` strengths rather than inventing parallel vocabulary. Gratuitous divergence from an OASIS standard is the cheapest thing to fix and the most expensive to leave.

---

## 5. Monotonicity — the crux (read this section)

You suspected this is the crux. It is, and it is worse and more interesting than you framed it.

### 5.1 Custos's claim is not "non-monotonic reasoning." It is the opposite.

Non-monotonicity *is* the property that adding information can retract a conclusion. KLM open their founding paper by observing that nonmonotonic reasoning "had almost always been described only negatively, by the property it does not enjoy — monotonicity" **[S]** (Kraus, Lehmann, Magidor, "Nonmonotonic reasoning, preferential models and cumulative logics," *AI* 44:167–207, 1990; arXiv:cs/0202021).

So a calculus asserting that a larger evidence bundle "refines and never contradicts" a smaller one, with **no backward transitions**, is asserting **monotonicity**. Custos is a *monotone* calculus with an explicit "unknown" value. It is in the family of Kleene/Belnap/Fitting fixpoint semantics, not the family of Reiter/Nute/Dung.

The weakened monotonicity principles you might reach for do **not** rescue the "non-monotonic" label:

- **Cautious Monotony** (KLM System P): if `φ ⤳ ψ` and `φ ⤳ τ` then `φ∧ψ ⤳ τ` — you may add a conclusion you already drew without losing others. **[S]**
- **Rational Monotony** (Lehmann & Magidor 1992, = System Z / rational closure): stronger, "substantially more controversial." **[S]**

**[A] Neither is what Custos claims.** Both are conditional monotonicity under adding *derived* or *non-refuting* information. Custos claims monotonicity under adding **arbitrary committed evidence**, including evidence that defeats. That is full monotonicity in the information order. It is a *strictly stronger* claim than System P, and strictly stronger than anything the nonmonotonic-reasoning literature offers, because that literature exists precisely to *not* have it.

### 5.2 The good news: full monotonicity has a name, and it is the right name for KERI

Two literatures, one theorem.

**Logic side [S/A]:** monotone in the knowledge order `≤_k` over a bilattice, with least-fixpoint semantics à la Kripke/Fitting. The knowledge order is "inspired by domain theory, initiated by Scott... which is precisely why monotonicity/continuity in `≤_k` underwrites fixed-point constructions" **[S]**. Cite Fitting, "Bilattices and the semantics of logic programming," *JLP* 11:91–116, 1991.

**Systems side [S]:** the **CALM theorem** — *Consistency As Logical Monotonicity*. Hellerstein & Alvaro, "Keeping CALM: When Distributed Consistency is Easy," arXiv:1901.01930, *CACM* 63(9):72–81, 2020; https://cacm.acm.org/research/keeping-calm/. Verified content of the result **[S]**: "the programs that have consistent, coordination-free distributed implementations are **exactly** the programs that can be expressed in monotonic logic. Monotonic problems have consistent, coordination-free implementations; non-monotonic problems **require coordination** for consistency." Monotonicity defined as: `S ⊆ T ⇒ P(S) ⊆ P(T)`. Consistency recast as **confluence** — same output for any order/batching of inputs. Also: monotone problems are exactly those that "do not require knowledge of network membership." And the CRDT link: "a CRDT's merge (`⊔`) forms a join-semilattice — commutative, associative, idempotent — and CAI suffices for **strong eventual consistency**: replicas receiving the same updates converge regardless of delivery order or duplication, **with no agreement protocol**. This is the algebraic manifestation of the CALM principle." Related: Bloom/Bloom^L, Lasp, LVars.

**[A] This is the most valuable single connection in the report, and Custos should lead with it.** The KERI thesis is "no blockchain, no global consensus." CALM is the theorem that says *when* you are entitled to that: exactly when your computation is monotone. So Custos's monotonicity axiom is not an incidental design taste — **it is the necessary and sufficient condition for the fold to be verifiable without coordination.** Every stranger converges on the same judgment, in any delivery order, without agreement, *because* the fold is monotone. That is a one-sentence justification for the entire architecture, backed by a *CACM* theorem, and it reframes monotonicity from "a constraint we chose" into "the thing that makes the no-consensus claim true." It also gives you a precise statement of the price: **any non-monotone element in the fold reintroduces the need for coordination**, i.e. destroys the core value proposition. That's a much sharper design rule than "we prefer monotonicity."

Note also from the CALM literature a distinction you will need **[S]**: **lattice monotonicity** (state only moves up the semilattice) vs. **observable monotonicity** (a fact, once visible, stays visible) — "some designs deliberately break" the latter. Custos's "no backward transitions" is a claim about *observable* monotonicity of the verdict, which is the harder one.

### 5.3 The bad news: reinstatement

**[A] This is the defect I would most want to be wrong about.**

The central phenomenon of the entire defeasible-reasoning literature is **reinstatement**: `A` is defeated by `D`; then `D` is itself defeated by `D′`; therefore `A` is **reinstated**. It is so central that argumentation's standard labelling is *named after it* — Caminada's "**reinstatement labelling**" **[S]** — and Dung's whole apparatus is built on "defends": a set is complete iff it contains every argument it defends **[S]**. Operationally the grounded extension is computed by "accepting unattacked arguments, deleting arguments attacked by accepted ones, and iterating until a fixpoint" **[S]** — a *global* recomputation, not an incremental accumulation.

Now: in Custos, a reinstatement is a transition `defeated → affirmed`. That is:

1. A **backward transition**, which Custos forbids by axiom; and
2. **Not** an upward move in the knowledge order `≤_k` (`f` and `t` are `≤_k`-incomparable), so it is not monotone under *any* reading of the four-valued lattice.

Therefore, exactly one of the following is true of Custos:

- **(i) Defeats are indefeasible.** A committed defeat can never itself be defeated. Then the calculus really is monotone and CALM applies — but Custos cannot express "the defeating evidence was forged / out of time / issued by someone without authority," which is a first-order requirement in any real governance system, and is precisely ASPIC+'s rank-immune **undercutter** (§1.5). This is a large expressiveness price and it is not currently disclosed.
- **(ii) Defeats are defeasible.** Then judgments can flip `defeated → affirmed`, the no-backward-transition axiom is **false**, monotonicity is **false**, and — by CALM — coordination-freeness is **not** guaranteed by the calculus's structure.

**There is no third option available inside a 4-element codomain**, because the only monotone destination from `defeated` is `self-convicted`, and routing reinstatement there would be semantically absurd (the subject would be convicted for having been *wrongly* accused).

I cannot tell from your description which branch Custos is on. If the spec has not confronted this, it is the highest-priority thing to confront. If it *has* chosen (i), say so loudly and in those words — "defeat is terminal; defeat-of-defeat is not expressible; use `pending` and off-chain adjudication instead" — because reviewers from this field will look for reinstatement in the first ten minutes and will assume the worst if they don't find it addressed.

Supporting literature for "which shapes of growth preserve extensions": Baumann & Brewka, COMMA 2010, created the expansion taxonomy for exactly this question — **normal** expansion (no new attacks purely among old arguments), **strong** (normal + new arguments not attacked by old), **weak** (new arguments do not attack old), **local** (only new attacks) **[S]**. Follow-ups: Baumann, "Normal and strong expansion equivalence for argumentation frameworks," *AI* 193:18–44, 2012; Baumann & Brewka, "The equivalence zoo for Dung-style semantics," *JLC* 28(3):477–498, 2018. **[S]** **[A] Custos's evidence growth is at best a *normal* expansion — new commitments do attack old conclusions — which is the class where flipping is possible. I did not verify which expansion class Baumann & Brewka prove monotonicity for; check that before citing a direction.**

### 5.4 What monotonicity costs you in expressiveness — precisely

**[A] All of this is analysis.** A monotone fold into a four-valued lattice cannot express:

1. **Negation as failure / closed-world reasoning.** No clause of the form "if no evidence of X, conclude Y." Such a clause is non-monotone by construction. It must be rewritten as `pending`, which is exactly what Custos's `pending` is *for* — so this cost is already paid, deliberately and well. Note that defeasible logic's `-∂p` ("proved not defeasibly provable") **is** a closed-world judgment and therefore is **not** available to Custos. Anywhere Custos borrows DL machinery it must check for this.
2. **Reinstatement / defeat-of-defeat.** §5.3.
3. **Undercutting defeat that ignores rank.** §1.5.
4. **Ambiguity blocking.** Maher's distinction **[S]**: with ambiguity *blocking*, an unresolved conflict simply blocks downstream inference; with ambiguity *propagating*, "the fact that there are claims for `q` that are not overcome by claims for `¬q`" influences later inferences. His expressiveness results: **team defeat is not an expressiveness distinction** (logics with and without it are equally expressive), but **ambiguity handling is** — "logics that handle ambiguity differently... have distinct expressiveness, with neither able to simulate the other." (M. Maher, "Relative Expressiveness of Defeasible Logics," arXiv:1210.1785, *TPLP* 12(4–5):793–810, 2012.) **[A] Two implications: (a) Custos must state whether it blocks or propagates ambiguity — it is a real, non-cosmetic choice with a proof that the alternatives are inter-untranslatable; (b) Maher's result is independent formal support for your intuition that the two upward currents "must never merge": the literature has a theorem that these two propagation disciplines are not reducible to each other.**
5. **Non-monotone aggregation** — counting, thresholds over open sets, "the majority of committed attestations," "no more than N." Any such clause is non-monotone unless the denominator is itself committed and closed. This is the classic CRDT trap and I'd bet a real Custos domain wants at least one of these.
6. **Accrual of reasons** — several weak reasons jointly outweighing a strong one. Horty flags accrual as an open problem even in the non-monotone setting **[S]**; in a monotone four-valued setting it is simply unavailable.

### 5.5 The concrete fix — separate the monotone object from the verdict

**[A] Recommendation, my analysis.** The literature's actual architecture is:

> the **framework grows monotonically**; the **labelling is recomputed**, and is not monotone.

That is Dung + Caminada exactly: add arguments and attacks (monotone, append-only, CRDT-shaped, coordination-free to *replicate*), then compute the grounded labelling as a global fixpoint (deterministic and unique, but *not* an incremental refinement of the previous labelling). Custos has conflated the two objects and asserted monotonicity of the wrong one.

Two coherent designs, pick one and say which:

- **Design A — keep verdict monotonicity, pay for it.** Axiomatize *indefeasible defeat*. State the exclusion of reinstatement, undercutters, and non-monotone aggregation as explicit non-goals. You keep CALM, byte-identical incremental verification, and no-backward-transitions. This is a defensible, publishable position — it is essentially "Datalog without negation, for governance" — but it must be stated as a *restriction*, with the excluded phenomena named, or the first serious reviewer will read the omission as naivety rather than as a choice.
- **Design B — move monotonicity down a level.** The monotone object is the evidence/defeat graph (a join-semilattice under union — a genuine CRDT). The verdict is a deterministic *function* of that graph (grounded/skeptical labelling), unique by Dung's uniqueness of the grounded extension, byte-reproducible because the graph is canonically serialized and the labelling algorithm is fixed. You then **drop** the no-backward-transition claim for verdicts, and replace it with the accurate and still-strong claim: *the evidence lattice is monotone, and the verdict is a deterministic, coordination-free function of it.* Reinstatement becomes expressible. You lose incremental verdict stability (a verdict can flip when the bundle grows), which you must then handle at the protocol level — e.g. verdicts are always stated relative to a named bundle digest, which a KERI-based system can do trivially and which is arguably what byte-identical reproducibility *already* requires.

### 5.6 A concrete monotonicity bug in "canonical defeat selection"

**[A] My analysis; check it against the spec.** Custos requires that where several defeats stand, one canonical defeat be selected deterministically, and that the judgment carry that defeat's citation and class.

Consider a selector "pick the **most specific / earliest / first-in-log** defeat." Under evidence growth, a stranger with a larger bundle may discover a defeat that is *more* specific or *earlier in some other KEL* than the previously canonical one. The verdict value stays `defeated` — fine — but the **citation changes**. If the citation is part of the judgment, the judgment is **not** monotone, and two honest verifiers with different bundles produce different bytes. Your "byte-identically reproducible by any stranger" promise fails on the citation component even though it holds on the value component. Note that append-only-ness of a *single* KEL does not save you: bundles are unions across subjects, so "earliest" is not stable under bundle growth.

Now consider the selector "pick the **maximum** under a fixed total order." A maximum over a growing set is **monotone non-decreasing**. So:

> **canonical_defeat := max over standing defeats, ordered by (defeater-class rank, then the defeat's SAID as a byte string)**

This is (a) **total** — SAIDs are distinct, so ties never survive the second key; (b) **deterministic**; (c) **monotone** — as evidence grows the selected defeat can only move *up* the order, so a citation change is an upward refinement rather than a contradiction, and the judgment can be typed as living in a lattice of `(value, rank, said)` triples; (d) **legally intelligible** — "highest-ranked defeat wins" is *lex superior*, and the SAID tiebreak only ever discriminates *within* a class, where by construction the law is indifferent.

If instead you tiebreak by *minimum* (first/earliest/most-specific), you get determinism but **lose** monotonicity. **[A] I suspect this is the actual mechanism behind at least one of your three open defects: they may not all be "we need a total order," but rather "our selector is a `min` where monotonicity requires a `max`."** That is a much smaller and more tractable defect than the one you thought you had.

And the residual case Catala teaches you to keep: if two defeats are in the top class and you are *unwilling* to break the tie arbitrarily (because the citation is legally load-bearing, not merely a display artifact), then you need `⊛` — an explicit "irresolvably multiply defeated" outcome — rather than an arbitrary winner. Making indeterminacy *itself* reproducible is strictly better than hiding it behind an arbitrary but reproducible choice, because the latter creates a false record of *why* the subject lost.

---

## 6. s(CASP), ASP for legal reasoning, Blawx

### 6.1 s(CASP) — the justification object

**What.** `s(CASP)` is a goal-directed, top-down, non-monotonic reasoner for **Constraint Answer Set Programs** with **no grounding phase** — it "retains logical variables and constraints both during execution and in the answer sets" and "returns **partial** stable models containing only the literals necessary to support the query." Because "its operational semantics relies on **backward chaining**, which is intuitive to follow," it "lends itself to generating explanations translatable into natural language." **[S]** Authors: Joaquín Arias, Manuel Carro, Zhuo Chen, Gopal Gupta (IMDEA/UPM/UT Dallas).

**The key paper for your purposes.** Arias, Carro, Chen, Gupta, "**Justifications for Goal-Directed Constraint Answer Set Programming**," ICLP 2020 Technical Communications, *EPTCS* 325:59–72, doi:10.4204/EPTCS.325.12, arXiv:2009.10238. **[S]** Verified-by-snippet claims:

- Motivation: "ethical and legal concerns make it necessary for programs that may directly influence people's lives (e.g., legal or health counseling) to **justify the advice given in human-understandable terms**."
- It produces a **justification tree** = the trace of the successful derivation, or of the *negated* query when it fails.
- Claims to be "the only approach providing full natural-language justifications for ASP programs **including constraints and negated literals**," with control over which literals appear in the tree for readability, and navigable HTML output.
- Because justification operates on the **non-ground** program, explanations are more compact.

Also: Arias et al., "A Short Tutorial on s(CASP)," https://ceur-ws.org/Vol-2970/gdepaper1.pdf **[S]**; and a recent survey, "An XAI View on Explainable ASP: Methods, Systems, and Perspectives," arXiv:2601.14764 **[S]**.

Legal application in the same line: Arias et al., "**Automated legal reasoning with discretion to act using s(LAW)**," *Artificial Intelligence and Law*, doi:10.1007/s10506-023-09376-5, arXiv:2401.14511 — models **vague/discretionary** concepts via patterns and justifies applicable legislation; validated on Comunidad de Madrid student-admission criteria. Their diagnosis is worth quoting **[S]**: "discretionality and vagueness cannot be expressed in Prolog-based top-down models, while in bottom-up ASP models justifications are **incomplete or not scalable**."

**[A] What s(CASP) supplies that Custos lacks:**
1. **Justification of negative answers.** This is the direct analogue of Custos's `defeated` and `pending` needing to carry their ground. "Why *not*" is much harder than "why," and s(CASP) is the reference implementation. Custos's `pending(typed-requirement)` is essentially *a justification for a negative answer, projected into a cure*. Look at how s(CASP) constructs the failure trace before designing that from scratch.
2. **A worked notion of justification-tree pruning.** Custos's grounds must be verifiable *and* human-legible; s(CASP) has explicit machinery for choosing which literals appear.
3. **Partial models.** Only the literals needed to support the query — the natural shape for a fold whose evidence bundle is partial by design.
4. **A warning.** s(CASP) is *non-monotone* (it has negation as failure, and ASP semantics is non-monotone). So you can borrow its **justification architecture** but not its **inference relation**. Given §5, be careful: importing ASP-style reasoning would break CALM.

### 6.2 Blawx and "Rules as Code"

**Blawx** — Jason Morris (Lexpedite Legal Technologies, Canada): a web-based Blockly (visual, drag-and-drop) front end that compiles to s(CASP); originally ErgoAI-backed, re-implemented on s(CASP), and as a consequence "provides justifications in natural language for both positive and negative queries" **[S]**. Morris holds an interdisciplinary LLM in Computational Law (Alberta), was an ABA Innovation Fellow 2018/19, and published "Blawx: Rules as Code Demonstration," *MIT Computational Law Report*, 2020, and "Modeling Administrative Discretion Using Goal-Directed Answer Set Programming" **[S]**.

**Maturity — be clear-eyed.** From the COHUBICOL typology entry (read) **[V]**: Blawx "remains a proof-of-concept and **'alpha software' unsuitable for production environments**," maintained primarily by Morris via Lexpedite, with an emerging API. Critical limitations flagged there **[V]**: legal unsoundness from translation quality, **lack of judicial authority for encoded interpretations**, maintenance burden as interpretations evolve, and possible inappropriateness for areas of law too complex or ambiguous for deductive systems. https://publications.cohubicol.com/typology/blawx/

**[A] What this supplies Custos:** (a) an existence proof that a justification-carrying legal reasoner can be made usable by non-programmers — worth studying for how Custos surfaces `pending` cures to humans; (b) a maturity calibration — the "Rules as Code" ecosystem is at alpha, so Custos is not late to a crowded market, it is early to an empty one; and (c) the COHUBICOL critique list, which is the set of objections Custos will face and should pre-empt in its own spec (especially: an encoded interpretation has no judicial authority — Custos's `defeated(citation)` looks like an adjudication and will be read as one).

### 6.3 The CS-theory framing for "every judgment carries its ground"

**[A]+[S]** The general name is **certifying algorithms**: "an algorithm that produces, with each output, a certificate or witness (easy-to-verify proof) that the particular output has not been compromised by a bug. The user inputs `x`, receives the output `y` and the certificate `w`, and then checks... that `w` proves `y` is a correct output for `x`. **This way the correctness of the output can be established without having to trust the algorithm.**" — R. M. McConnell, K. Mehlhorn, S. Näher, P. Schweitzer, "Certifying algorithms," *Computer Science Review* 5(2):119–161, 2011, doi:10.1016/j.cosrev.2010.09.009; see also Mehlhorn & Schweitzer, "Progress on Certifying Algorithms," 2010, https://users.cecs.anu.edu.au/~pascal/docs/progress_on_certifying_algorithms.pdf **[S]**. Adjacent: Necula & Lee, "The Design and Implementation of a Certifying Compiler," PLDI 1998 (proof-carrying code) **[S]**.

**[A] Why this matters to Custos more than the legal-AI citations do.** "Without having to trust the algorithm" is Custos's exact promise, stated in the vocabulary of a different and more rigorous field. The certifying-algorithms literature also supplies the design discipline Custos most needs: **the checker must be radically simpler than the producer.** If verifying a Custos judgment requires re-running the whole fold, you have a *reproducible* algorithm, not a *certifying* one, and the trust argument is much weaker (every verifier must implement the entire calculus correctly, and any two implementations must agree bit-for-bit). If instead a judgment carries a witness checkable by a small, obviously-correct program, the trust surface collapses. Custos's talk of judgments "carrying their ground" suggests it wants this; the four-value + citation payload as described is not obviously a *witness* in the technical sense, especially for `pending` (proving a negative usually needs a much larger certificate). This is worth a hard look.

---

## 7. Where the literature would say Custos has erred — the uncomfortable version

Ordered by how much I would want to be wrong.

1. **"Monotonic non-monotonic reasoning" is not a thing, and the reinstatement hole is real.** §5.3. Either defeat is indefeasible (large undisclosed expressiveness cost) or the no-backward-transition axiom is false. Nothing in a 4-element codomain lets you have both. This is the one to fix first.

2. **The framing "three defects all reduce to imposing a total order on defeats" is probably wrong, and pursuing it will waste effort.** The literature's consensus is that a total order is neither necessary nor sufficient: not necessary (determinism comes from skeptical semantics, acyclicity + locality, or a computed ranking — §1.4a–d); not sufficient (a total order over strata still admits several distinct deterministic entailments — best-out vs. lexicographic vs. possibilistic — §1.4e; and linearizing a partial order classically *multiplies* extensions, one per linearization — §1.2 **[V]**). The requirements you actually need are **acyclicity** and **locality** (compare only rules with complementary heads **[V]**), plus a named aggregation. Your real defect is more likely §5.6: a selector that is a `min` where monotonicity demands a `max`.

3. **The ranked-defeater-class apparatus is formally eliminable.** For every defeasible theory there is an equivalent one with an **empty superiority relation** and no defeaters or facts, via modular and incremental transformations **[V]**. So ranking is not a semantic primitive; it is sugar. Custos elevating it to a core axiom, and treating "the ranking is contested" as a *logic* problem, misplaces a governance decision inside the calculus. Define the normal form as ground truth; make the ranking a compiled, published, amendable artifact.

4. **There is no undercutter.** ASPIC+ is explicit that "undercutting attacks succeed **regardless of preferences**," and that bolting preferences onto attack abstractly "leads to violations of subargument closure and consistency" **[S]**. If all defeat in Custos is rank-adjudicated, then attacks on the *applicability* of an inference (authority, timeliness, jurisdiction, competence) are mismodelled as merely high-ranked rebuttals. `self-convicted` looks like one special case of an undercutter that got promoted to a value; the general category is missing.

5. **Ambiguity blocking vs. propagating is unstated, and it is a proven, non-cosmetic choice.** Maher: team defeat makes no expressiveness difference; **ambiguity handling does**, with neither variant able to simulate the other **[S]**. Custos must declare. (The good news: this is *also* independent formal support for "the two currents must never merge.")

6. **The four values are Belnap's, and the "two currents" are a bilattice.** Not an error — but presenting them as novel is. Belnap 1977, Ginsberg 1988, Fitting 1991. `self-convicted` is Belnap's `⊤`, whose *original motivating use case* is contradictory reports from multiple sources, and whose Fitting-era use case is **conflicting information from different nodes of a distributed network** **[S]**. Custos is 49 years downstream. Cite it and inherit the theorems (interlacing, twist-product representation, monotone-fixpoint semantics) instead of re-deriving them.

7. **`affirmed` conflates two strengths the literature keeps apart.** DL distinguishes `+Δ` (definitely provable, strict) from `+∂` (defeasibly provable) **[V]**. A judgment that is affirmed *and immune to any possible future defeat* is a materially different object from one that is affirmed *so far*. Custos's `affirmed` appears to be the latter but will be *read* as the former by every user. Given monotonicity, the strict/defeasible distinction is cheap to add and high-value: `+Δ` is the only value on which downstream parties can safely take irreversible action.

8. **Epistemic values are being used to do deontic work.** `affirmed`/`defeated` are truth/warrant judgments; governance clauses impose obligations, permissions and prohibitions, whose failure produces *violations* that trigger *reparation chains* (LegalRuleML's `SuborderList`: a deontic specification holds "if all Deontic Specifications that precede it have been violated" **[V\*]**). Custos's `defeated` is terminal; real norms cascade. 25 years of defeasible deontic logic exists here.

9. **The temporal dimension is absent from your description.** LegalRuleML distinguishes **three** legal time axes — entry into force, efficacy, applicability **[V\*]** — plus norm change (abrogation, annulment). A committed-log substrate is unusually well suited to getting this right, and unusually likely to get it wrong by conflating "when the bytes were committed" with "when the norm applied."

10. **`pending` promises a cure that may not exist.** Enforcement has known **impossibility** results **[S]**; abduction is not free. A mandate that every `pending` names a typed requirement is stronger than the literature supports.

11. **Reproducible ≠ certifying.** §6.3. If checking requires re-running the fold, the trust argument rests on every implementation being bit-identical — which is exactly the fragile assumption a certificate is supposed to remove.

**What Custos genuinely has that the field does not.** Being fair: (a) **byte-identical canonicity** — LegalRuleML explicitly declines to mandate a logic or a canonical serialization **[V\*]**, and no legal-reasoning system I found treats *reproducibility by a stranger* as the primary design constraint; (b) **evidence as committed log bytes with cryptographic provenance**, which converts "the priority relation is contested" from an unbounded argument into a bounded one about a fixed corpus; (c) `self-convicted` as a *first-class outcome with a propagation discipline* — paraconsistent labellings exist **[S]** but the "duplicity taints upward, and must never merge with defeat" discipline appears to be genuinely yours (and is exactly what bilattice interlacing formalises); (d) the CALM-shaped insight — even if arrived at accidentally — that a governance calculus can be **coordination-free iff monotone**. That last one is a real contribution and it is currently unlabelled.

---

## 8. If you only read three things

1. **Delgrande, Schaub, Tompits & Wang (2004), "A Classification and Survey of Preference Handling Approaches in Nonmonotonic Reasoning,"** *Computational Intelligence* 20(2):308–334 — https://www.cs.uni-potsdam.de/wv/publications/DBLP_journals/ci/DelgrandeSTW04.pdf
   The map of your highest-priority question. Read the classification axes (prescriptive/descriptive, static/dynamic, meta/object-level, properties of `<`), then **Brewka & Eiter's Principles I and II** and make them Custos conformance tests, then the catalog entry for Grosof — the closest prior art to your engineering brief.

2. **Antoniou, Billington, Governatori & Maher (2001), "Representation Results for Defeasible Logic,"** *ACM TOCL* 2(2):255–287 — https://arxiv.org/abs/cs/0003082
   Where your codomain's nearest rule-based relative lives, in its own words: the four proof tags, the five theory components, **locality + acyclicity instead of totality**, and the theorem that the superiority relation is **eliminable** by modular, incremental transformation. Pair with Maher (2001), *TPLP* 1(6):691–711, for propositional DL in **linear time** — the complexity result a reproducibility-first standard should be designing toward.

3. **Merigoux, Chataing & Protzenko (2021), "Catala: A Programming Language for the Law,"** *PACMPL* / ICFP — https://arxiv.org/abs/2103.03198 (readable HTML: https://ar5iv.labs.arxiv.org/html/2103.03198)
   The most mature engineered artifact solving your problem, and the one that made the opposite choice at your exact decision point: priorities **local, static, syntax-derived, acyclic by construction**, and on indeterminacy it **aborts with a conflict error `⊛`** rather than inventing a tiebreak. Read §§2–4 and ask why Custos diverges.

**Runners-up, and honestly you should read these too:** Hellerstein & Alvaro, "Keeping CALM: When Distributed Consistency Is Easy," *CACM* 63(9), 2020 (https://cacm.acm.org/research/keeping-calm/) — the theorem that turns your monotonicity axiom into the justification for the whole no-consensus architecture; and Fitting, "Bilattices and the semantics of logic programming," *JLP* 11:91–116, 1991, for the algebra of your four values and your two never-merging currents.

---

## 9. Citation index

**Priority ordering / preference handling**
- Delgrande, Schaub, Tompits, Wang, *Computational Intelligence* 20(2):308–334, 2004. https://www.cs.uni-potsdam.de/wv/publications/DBLP_journals/ci/DelgrandeSTW04.pdf **[V]**
- Antoniou, Billington, Governatori, Maher, *ACM TOCL* 2(2):255–287, 2001. https://arxiv.org/abs/cs/0003082 **[V]**
- Maher, "Propositional defeasible logic has linear complexity," *TPLP* 1(6):691–711, 2001. doi:10.1017/S1471068401001168 **[S]**
- Maher, "Relative Expressiveness of Defeasible Logics," *TPLP* 12(4–5):793–810, 2012. https://arxiv.org/abs/1210.1785 **[S]**
- Grosof, "Prioritized conflict handling for logic programs," ILPS 1997, 197–211; IBM RR RC 20836 (1997); courteous compiler IBM RR RC21472 (1999); IBM CommonRules. **[S; survey entry V]**
- Brewka, "Preferred subtheories," IJCAI 1989, 1043–1048. **[S]**
- Brewka & Eiter, "Preferred answer sets for extended logic programs," *AI* 109, 1999 / 2000 principles. **[S; principles as stated in survey V]**
- Pearl, "System Z," TARK 1990; Goldszmidt & Pearl, *AI* 84:57–112, 1996; Lehmann & Magidor, *AI* 55(1):1–60, 1992 (rational closure). **[S]**
- Benferhat, Cayrol, Dubois, Lang, Prade, IJCAI'93:640–645. https://www.ijcai.org/Proceedings/93-1/Papers/090.pdf **[S]**
- Modgil & Prakken, "The ASPIC+ framework... a tutorial," *Argument & Computation* 5(1):31–62, 2014; Prakken, *A&C* 1(2):93–124, 2010. **[S]**
- Prakken & Vreeswijk, "Logics for Defeasible Argumentation," *Handbook of Philosophical Logic* vol. 4, 2001/2002, 219–318. http://www.horty.umiacs.io/courses/readings/prakken-vreeswijk-2002.pdf **[S]** — source of the *unique vs. multiple status assignment* framing and the *justified / overruled / defensible* trichotomy.
- Horty, *Reasons as Defaults*, OUP 2012. http://www.horty.umiacs.io/courses/readings/rd-root.pdf **[S]**
- Prakken, "Reasoning about priority relations," in *Logical Tools for Modelling Legal Argument*. **[S]**
- Dung, "On the acceptability of arguments...," *AI* 77:321–357, 1995 — uniqueness of grounded extension; Thm 30 (well-founded ⇒ all semantics coincide). **[S]**
- Baumann & Brewka, "Expanding Argumentation Frameworks: Enforcing and Monotonicity Results," COMMA 2010, FAIA 216:75–86. **[S]**

**Four-valued / bilattice**
- Belnap, "A useful four-valued logic," 1977. **[S]**
- Ginsberg, "Multivalued logics: a uniform approach to reasoning in AI," *Computational Intelligence* 4, 1988. **[R for exact cite]**
- Fitting, "Bilattices and the semantics of logic programming," *JLP* 11:91–116, 1991. **[S]**
- Jakl, "Four Imprints of Belnap's Useful Four-Valued Logic in Computer Science," *Studia Logica*, 2026. https://arxiv.org/abs/2503.20679 **[V — abstract verbatim]**
- Caminada, reinstatement labelling (2006); Caminada & Gabbay (2009); Baroni, Caminada, Giacomin, "An introduction to argumentation semantics," *KER*. https://bista.sites.dmi.unipg.it/didattica/CSP/argumentation/KER-BaroniCaminadaGiacomin.pdf **[S]**
- Arieli & Caminada, conflict-tolerant / paraconsistent labellings. **[S]**

**Monotonicity / systems**
- Kraus, Lehmann, Magidor, *AI* 44:167–207, 1990. https://arxiv.org/abs/cs/0202021 **[S]**
- SEP, "Non-monotonic Logic." https://plato.stanford.edu/entries/logic-nonmonotonic/ **[S]**
- Hellerstein & Alvaro, "Keeping CALM," arXiv:1901.01930; *CACM* 63(9):72–81, 2020. https://cacm.acm.org/research/keeping-calm/ **[S]**

**Catala / legal formalization**
- Merigoux, Chataing, Protzenko, *PACMPL* 2021, doi:10.1145/3473582; arXiv:2103.03198; HTML https://ar5iv.labs.arxiv.org/html/2103.03198 **[V]**
- Huttner & Merigoux, *Artificial Intelligence and Law*, 2022, doi:10.1007/s10506-022-09328-5 **[S]**
- Merigoux, Huttner, Monat et al., "Coding computational laws: 20 recommendations for public administrations," *ICT Law*, 2026. https://rmonat.fr/data/pubs/2026/2026-02-16_legal_code_recos.pdf **[S]**
- CUTECat, arXiv:2410.18212 **[S]**; Catala book https://book.catala-lang.org/ **[S]**
- Lawsky, "A Logic for Statutes," 21 Fla. Tax Rev. 60 (2017). https://gwern.net/doc/law/2017-lawsky.pdf **[S]**
- Lawsky, "Coding the Code: Catala and Computationally Accessible Tax Law," 75 SMU L. Rev. 535 (2022). **[S]**
- Brewka & Eiter, prioritized default logic (2000) — Catala's cited basis. **[S]**

**Deontic / LegalRuleML**
- OASIS LegalRuleML Core Specification v1.0 (OASIS Standard, Sept 2021). https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html **[V\*]**
- Athan, Boley, Governatori, Palmirani, Paschke, Wyner, "OASIS LegalRuleML," ICAIL 2013. http://www.governatori.net/papers/2013/icail2013legalruleml.pdf **[S]**
- Athan et al., "LegalRuleML: Design Principles and Foundations," Reasoning Web 2015, Springer, 151–188. **[S]**
- Governatori, Rotolo, Sartor, "Logic and the Law...," *Handbook of Deontic Logic and Normative Reasoning* vol. 2, 2021, 655–760. **[S]**
- Governatori's bibliography: http://www.governatori.net/research/pubs/defeasible.html **[S]**
- "Unravel legal references in defeasible deontic logic," ICAIL 2021; "Legal Explanation in Defeasible Deontic Logic via LegalRuleML," ICAIL 2025; "Extraction of Defeasible Proofs as Explanations," 2023. **[S]**

**Explanation / justification**
- Arias, Carro, Chen, Gupta, "Justifications for Goal-Directed Constraint Answer Set Programming," ICLP 2020 TC, *EPTCS* 325:59–72. https://arxiv.org/abs/2009.10238 **[S]**
- Arias et al., "Automated legal reasoning with discretion to act using s(LAW)," *AI & Law*, 2023. https://arxiv.org/abs/2401.14511 **[S]**
- "A Short Tutorial on s(CASP)." https://ceur-ws.org/Vol-2970/gdepaper1.pdf **[S]**
- Blawx: https://www.blawx.com/ ; COHUBICOL typology https://publications.cohubicol.com/typology/blawx/ **[V]** ; Morris, "Blawx: Rules as Code Demonstration," *MIT Computational Law Report*, 2020 **[S]**
- McConnell, Mehlhorn, Näher, Schweitzer, "Certifying algorithms," *Computer Science Review* 5(2):119–161, 2011. **[S]**
- Necula & Lee, "The Design and Implementation of a Certifying Compiler," PLDI 1998. **[S]**

---

## 10. Unresolved / would-check-next

Honest list of what I did not nail down.

1. **Which Baumann–Brewka expansion class preserves which semantics.** I have the taxonomy verbatim **[S]** but not the direction of the monotonicity theorems. Get COMMA 2010 pp. 75–86 before citing a direction. This bears directly on §5.
2. **Exact complexity classes for argumentation semantics.** Marked **[R]**. Verify against Dunne & Wooldridge or the *Handbook of Formal Argumentation* before putting numbers in a Custos document.
3. **Whether the bilattice mapping in §2.3 survives contact with the actual Custos spec.** I worked from your prose. The interlacing conditions are the specific thing to check: are Custos's two propagation rules each monotone with respect to the other order?
4. **Ginsberg 1988 exact citation** — recalled, unverified.
5. **Whether any Custos clause requires non-monotone aggregation** (counting/thresholds/majority). If yes, §5.4 item 5 is not hypothetical and CALM does not apply to that clause.
6. **A defeasible-logic-vs-Custos formal correspondence.** The obvious next piece of work: exhibit a translation from the Custos fold into DL(∂) or DL(δ) and check it is modular in Maher's sense. If it exists, Custos inherits linear-time verification and a large body of theorems; if it provably does not, that is itself a publishable novelty claim and you'd want to know exactly which axiom blocks it (my bet: `self-convicted`, since DL is skeptical and refuses contradictory conclusions **[S]**).
