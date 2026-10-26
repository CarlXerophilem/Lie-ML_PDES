# Bounded methods comparison

The search boundary is the two named methodological sources below, the official REDUCE manuals and the local 2022/2026 SVE papers. It is not an exhaustive novelty survey. Free PDFs were retrieved and text-extracted on 27 October 2026 (Japan time); hashes and UTC retrieval times are in [method-literature.json](sources/method-literature.json). The PDFs are not redistributed here.

| Method / source | Verified source statement | Application and limit |
|---|---|---|
| T. Wolf, *Size reduction and partial decoupling of systems of equations*, JSC 33(3), 367–383 (2002), arXiv:cs/0301029, §2 | Pairwise combinations reduce the term count; shorter systems can partially decouple and become easier to integrate | Apply before expensive differential elimination. Log an invertible row operation or its nonzero multiplier; reopen the zero-factor branch. This is an optimization, not a completeness theorem |
| T. Bächler, V. Gerdt, M. Lange-Hegermann, D. Robertz, *Thomas Decomposition of Algebraic and Differential Systems*, arXiv:1008.3767, §§3.3–3.4 | Simple systems combine algebraic simplicity, involutivity, minimal equations and reduced inequations; decomposition is disjoint | Use a branch ledger with equations, inequations, initials, separants and compatibility checks. The published implementation is Maple; Maple was not executed here |
| Official LIEPDE manual, Syntax / Flags | Point symmetries can be requested with general coefficient functions; parameters to be solved are distinguished from fixed coefficients | Keep arbitrary generator dependencies. Positive physical coefficients may remain fixed symbolic coefficients, but exceptional divisions still need analysis |
| Official CRACK manual, input/output | Each returned branch has four lists, including inequations | Retain raw final and terminal output. LIEPDE's reduced public result alone is insufficient to recover every condition |

An unrestricted generator has unknown functions such as xi_t(t,x,h,u,B), not a preselected polynomial. A genuine speed improvement must preserve that problem. The direct-CRACK variant receives the same thirty independently derived determining equations, with no known basis. The fixed-coefficient variant changes which parameters the CAS classifies; that difference is recorded and forbids a claim that it automatically completes exceptional-parameter coverage.

For continuous exponents, u>0 allows writing u^a=exp(a log u). Distinct exponents can only be split once the remaining coefficients are known not to conceal u-dependence. First derive those dependency conditions; then solve exponent-collision conditions; then check every zero pivot. A numerical sample of m cannot discharge these steps.

Proposed acceptance for a future optimizer: retain both systems and a reversible transformation certificate on each chart; compare original-PDE residuals of returned families; account for every divisor-zero stratum; run the same pinned solver with identical budgets; report unresolved branches as well as times. No such full optimizer benchmark or new complexity theorem is claimed in this release.
