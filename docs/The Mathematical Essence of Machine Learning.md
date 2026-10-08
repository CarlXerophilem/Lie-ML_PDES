# **The Mathematical Essence of Machine Learning**

[https\://gemini.google.com/app/e46560de931c3524](https://gemini.google.com/app/e46560de931c3524)

*User prompt: what is the pure-mathematical essence of machine learning?*

Response: At its formal foundation, machine learning is the study of **ill-posed inverse problems over probability spaces, resolved through empirical process theory, functional approximation, and optimization dynamics on high-dimensional manifolds.**

Stripped of algorithmic heuristics and engineering terminology, the framework decomposes into four mathematical domains.

### **1\. Empirical Process Theory and Measure-Theoretic Generalization**

Let (Z,Σ) be a measurable space, where Z\=X×Y. Let P(Z) be the set of probability measures on (Z,Σ), and let *P*∈P(Z) be an unknown data-generating distribution.

Given a hypothesis space F⊆{*f*:X→Y} and a measurable loss functional ℓ:Y×Y→R≥0​, the target is the minimizer of the risk functional:

*R*(*f*)=E(*X*,*Y*)∼*P*​\[ℓ(*f*(*X*),*Y*)\]=∫Z​ℓ(*f*(*x*),*y*)*dP*(*x*,*y*)

Because *P* is inaccessible, one observes only an independent and identically distributed sample *Sn*​\={*zi*​}*i*\=1*n*​∼*P*⊗*n*. This sample defines the empirical measure *Pn*​\=*n*1​∑*i*\=1*n*​*δzi*​​, yielding the empirical risk:

*Rn*​(*f*)=∫Z​ℓ(*f*(*x*),*y*)*dPn*​(*x*,*y*)=*n*1​*i*\=1∑*n*​ℓ(*f*(*xi*​),*yi*​)

The primary mathematical question of statistical learning theory is whether the empirical minimizer *f*^​*n*​\=argmin*f*∈F​*Rn*​(*f*) satisfies *R*(*f*^​*n*​)→inf*f*∈F​*R*(*f*) as *n*→∞. This reduces to establishing uniform laws of large numbers over the empirical process G*n*​\=*n*​(*Pn*​−*P*):

*f*∈Fsup​∣*Rn*​(*f*)−*R*(*f*)∣*P*​0

This convergence is governed not by the ambient dimension of X, but by the geometric and metric entropy of the class F—quantified via Dudley chaining, Vapnik–Chervonenkis (VC) dimension, and Rademacher complexity:

R*n*​(F)=E*σ*,*Sn*​​\[*f*∈Fsup​*n*1​*i*\=1∑*n*​*σi*​*f*(*xi*​)\],*σi*​∼iidRademacher(±1)

### **2\. Functional Analysis and Approximation Theory**

The estimation of an unknown conditional expectation operator *f*∗(*x*)=E\[*Y*∣*X*\=*x*\] is constrained by the choice of hypothesis space F. Total error decomposes orthogonal to the data:

*R*(*f*^​*n*​)−*R*(*f*∗)=Estimation Error (Stochastic)(*R*(*f*^​*n*​)−*f*∈Finf​*R*(*f*))​​\+Approximation Error (Deterministic)(*f*∈Finf​*R*(*f*)−*R*(*f*∗))​​

Approximation theory examines the density and approximation rate of F within standard function spaces (such as *L*2(*PX*​), Sobolev spaces *Ws*,*p*(Ω), or Reproducing Kernel Hilbert Spaces H*K*​):

> * **Classical Approximation:** For smooth functions *f*∗∈*Ws*,∞(\[0,1\]*d*), achieving an approximation error *ϵ* with standard linear approximation schemes requires a basis size of O(*ϵ*−*d*/*s*), exhibiting the curse of dimensionality.  
> * **Nonlinear/Compositional Classes:** Modern deep parametric models *fθ*​(*x*)=(*σ*∘*WL*​∘⋯∘*σ*∘*W*1​)(*x*) circumvent this lower bound for specific target classes (e.g., Barron spaces or compositional functions *f*∗\=*gk*​∘⋯∘*g*1​) by exploiting low-dimensional intrinsic structures, such as Riemannian submanifolds M⊂R*d*.

### **3\. Ill-Posed Inverse Problems and Regularization**

Formulated functionally, learning is the inversion of an observation operator *A*:F→R*n*, where *A*(*f*)=(*f*(*x*1​),…,*f*(*xn*​))+*ξ*, with noise vector *ξ*.

Because the domain of *A* is infinite-dimensional and its range is finite-dimensional, the inverse problem *A*(*f*)≈*y* is severely ill-posed in the sense of Hadamard:

> 1. Solutions are non-unique (the null space ker(*A*) is infinite-dimensional).  
> 2. Solutions do not depend continuously on the observations (instability under perturbations).

To render the problem well-posed, variational regularization introduces an energy functional or prior Ω:F→R≥0​:

*f*∈Fmin​{*Rn*​(*f*)+*λ*Ω(*f*)}

In reproducing kernel Hilbert spaces, when Ω(*f*)=∥*f*∥H*K*​2​, the Riesz representation theorem and the classical Representer Theorem reduce this infinite-dimensional variational problem to a finite-dimensional linear system. In overparameterized neural architectures where *λ*\=0, the regularization is often **implicit**, determined by the inductive bias of the optimization geometry itself.

### **4\. Non-Convex Optimization and Measure Dynamics**

Parametric learning maps a parameter manifold Θ⊆R*p* to a hypothesis space via *θ*↦*fθ*​. The optimization problem:

*θ*∈Θmin​*Ln*​(*θ*):=*Rn*​(*fθ*​)

is typically non-convex, possessing degenerate saddle points and non-isolated manifolds of global minima.

The mathematical study of learning dynamics addresses this through:

> * **Riemannian and Metric Geometry:** Analyzing the loss landscape through the spectrum of the Hessian *H*(*θ*)=∇2*Ln*​(*θ*) and the empirical Fisher Information Matrix:  
>   *I*(*θ*)=*n*1​*i*\=1∑*n*​∇*θ*​log*p*(*yi*​∣*xi*​,*θ*)∇*θ*​log*p*(*yi*​∣*xi*​,*θ*)⊤  
> * **Infinite-Width Limits (Mean-Field vs. Kernel Regimes):**  
  * In the *Neural Tangent Kernel (NTK)* regime, as width *m*→∞ under specific parameter scaling, the dynamics linearize: Θ evolves under a static metric, and the gradient flow reduces to linear ordinary differential equations in function space.  
  * In the *Mean-Field* regime, parameters are treated as an empirical measure *μt*​\=*m*1​∑*j*\=1*m*​*δθj*​(*t*)​∈P(R*k*). The parameter trajectory under continuous-time gradient descent converges to a **Wasserstein gradient flow** governed by the non-linear continuity (Vlasov-Fokker-Planck) equation:  
    ∂*t*​*μt*​\=∇⋅(*μt*​∇*δμδ*E​(*μt*​))  
    where *δμδ*E​ denotes the first variation of the risk functional on the 2-Wasserstein space W2​(R*k*).

The mathematical essence of machine learning is therefore the interplay between **metric geometry on probability measures** (controlling concentration and generalization), **approximation in Sobolev/Banach spaces** (controlling representation), and **optimal transport/gradient flows** (governing convergence in overparameterized parameter spaces).

---

*User prompt: What are the components of ML? Is neural network neccessary?*

Response: From a formal mathematical standpoint, any machine learning formulation is characterized by a five-tuple:

(Z,H,ℓ,Ω,A)

Neural networks are **not** necessary. They represent only one specific parametric choice for the hypothesis space H.

### **The Fundamental Components of Machine Learning**

#### **1\. The Observation Space and Measure-Theoretic Environment (Z)**

Let Z\=X×Y be a measurable space equipped with an unknown data-generating Borel probability measure *P*∈P(Z). The learner has access only to an *n*\-element independent sample *Sn*​\={(*xi*​,*yi*​)}*i*\=1*n*​∼*P*⊗*n*, defining the discrete empirical measure:

*Pn*​\=*n*1​*i*\=1∑*n*​*δ*(*xi*​,*yi*​)​

#### **2\. The Hypothesis Space (H)**

A collection of candidate mappings from the input space to the action or label space:

H⊆{*f*:X→Y′}

The choice of H defines the representational capacity of the model and dictates the metric entropy, Vapnik–Chervonenkis (VC) dimension, or Rademacher complexity of the problem.

#### **3\. The Loss Functional (ℓ)**

A measurable mapping ℓ:Y′×Y→R≥0​ quantifying discrepancy between the prediction *f*(*x*) and true target *y*. This defines both:

> * The **True Risk**: *R*(*f*)=∫Z​ℓ(*f*(*x*),*y*)*dP*(*x*,*y*)  
> * The **Empirical Risk**: *Rn*​(*f*)=∫Z​ℓ(*f*(*x*),*y*)*dPn*​(*x*,*y*)=*n*1​∑*i*\=1*n*​ℓ(*f*(*xi*​),*yi*​)

#### **4\. The Inductive Bias or Regularizer (Ω)**

A functional Ω:H→R≥0​ that imposes a prior over candidate functions to resolve the ill-posed nature of minimizing empirical risk over rich spaces. Regularization restricts the effective capacity of H, stabilizing solutions against perturbations in *Sn*​.

#### **5\. The Search/Optimization Algorithm (A)**

A mapping A:Z*n*→H that extracts a specific hypothesis from the sample:

*f*^​*n*​\=A(*Sn*​)

In empirical risk minimization (ERM), A typically solves or approximates:

*f*^​*n*​∈arg*f*∈Hmin​{*Rn*​(*f*)+*λ*Ω(*f*)}

### **Is a Neural Network Necessary?**

No. A neural network is merely a **compositional parametric hypothesis space**:

HNN​\={*fθ*​(*x*)=*WL*​*σ*(*WL*−1​…*σ*(*W*1​*x*\+*b*1​)⋯+*bL*−1​)+*bL*​​*θ*\={*Wl*​,*bl*​}*l*\=1*L*​}

where *Wl*​ are linear operators, *bl*​ are translation vectors, and *σ* is an element-wise non-linear activation.

A significant portion of machine learning theory and application relies on entirely different hypothesis spaces and optimization principles:

| Paradigm | Hypothesis Space H | Regularization / Inductive Bias | Optimization Operator A |
| :---- | :---- | :---- | :---- |
| **Reproducing Kernel Hilbert Spaces (RKHS)** | Unit/bounded balls in Hilbert space H*K*​: *f*(*x*)=∑*i*\=1∞​*αi*​*K*(*x*,*xi*​) | RKHS norm ∥*f*∥H*K*​2​ (smoothness under Mercer kernels) | Convex quadratic programming, closed-form linear systems (Representer Theorem) |
| **Tree Ensembles (e.g., Random Forests, GBDTs)** | Dyadic axis-aligned step functions: *f*(*x*)=∑*m*\=1*M*​*cm*​1{*x*∈*Rm*​}​ | Tree depth, minimum leaf cardinality, shrinkage parameters | Greedy recursive partitioning, functional gradient boosting |
| **Non-Parametric Local Estimators** | Continuous functions under Lipschitz or Hölder conditions | Bandwidth *h* in smoothing kernels (e.g., Nadaraya–Watson) | Closed-form local averaging / nearest-neighbor queries |
| **Linear Models / GLMs** | Affine hyperplanes: *f*(*x*)=⟨*w*,*x*⟩+*b* | ℓ1​ (sparsity) or ℓ2​ (Euclidean shrinkage) parameter norms | Convex optimization (IRLS, coordinate descent, convex duality) |

### **When Compositional Architectures (Neural Networks) Are Chosen**

The mathematical necessity for choosing HNN​ over linear or kernel hypothesis spaces arises strictly under specific structural conditions of the target function *f*∗(*x*)=E\[*Y*∣*X*\=*x*\]:

> 1. **Circumventing the Curse of Dimensionality via Compositionality:** Linear approximation schemes in Sobolev spaces *Ws*,*p*(R*d*) require a basis dimension of order O(*ϵ*−*d*/*s*) to achieve error *ϵ*. If *f*∗ is known to be a composition of low-dimensional functions *f*∗\=*gk*​∘⋯∘*g*1​, neural networks achieve rates O(*ϵ*−*d*∗/*s*) where *d*∗\=max*j*​dim(*gj*​)≪*d*.  
> 2. **Manifold and Group Symmetries:** When the measure *P* is supported on a low-dimensional sub-manifold M⊂R*d*, or when *f*∗ exhibits equivariance under a Lie group action *G* (e.g., translations, permutations), specialized neural network architectures (CNNs, Transformers, Graph Neural Networks) directly encode these symmetries into H, reducing the sample complexity by the volume of the symmetry group.

When data is tabular, strictly low-dimensional, or when the optimal hypothesis belongs to a known RKHS, classical non-neural methods frequently match or exceed the performance of neural networks while retaining strict convex guarantees.

---

*User prompt: Which components/parameters can be tuned/adjusted/optimized/replaced ? e.g. replace observation space by diffeomorphic Lie group orbits.*

Response: Every constituent of the mathematical learning formulation (Z,*P*,H,ℓ,Ω,A) can be abstracted, lifted, or replaced by higher-order geometric, algebraic, or measure-theoretic structures.

The systematic generalizations for each component are structured as follows:

### **1\. The Observation Space Z\=X×Y**

Rather than restricting inputs and outputs to Euclidean domains R*d*, the observation space can be generalized to arbitrary topological and geometric structures:

> * **Homogeneous Spaces and Orbit Manifolds:** If a Lie group *G* acts smoothly on a manifold M, the input space can be replaced by the quotient space (orbit space) X\=M/*G*. In this formulation, the data consists of equivalence classes \[*x*\]={*g*⋅*x*∣*g*∈*G*}, eliminating nuisance degrees of freedom prior to hypothesis evaluation.  
> * **Vector Bundles and Gauge Fields:** Observations can be modeled not as point vectors, but as smooth sections Γ(*E*) of a vector bundle *π*:*E*→M over a base manifold M. This occurs in gauge-equivariant learning, where local reference frames possess gauge symmetries described by a structure group *G*.  
> * **Infinite-Dimensional Function Spaces:** In operator learning, X and Y are infinite-dimensional Banach spaces B1​,B2​ (e.g., Sobolev spaces *Hs*(Ω) or Lebesgue spaces *Lp*(Ω)). The data points themselves are functions (e.g., initial/boundary conditions of partial differential equations).  
> * **Metric Measure Spaces:** X can be generalized to a triple (*M*,*dM*​,*μM*​) equipped only with a metric and a reference Borel measure, admitting tools from persistent homology and non-Euclidean optimal transport.

### **2\. The Sampling Process and Underlying Measure *P***

The canonical independent and identically distributed (i.i.d.) assumption *Sn*​∼*P*⊗*n* can be modified:

> * **Ergodic Dynamical Systems:** Replacing i.i.d. sampling with trajectories of a measure-preserving dynamical system (*T*,X,Σ,*μ*) where *xt*\+1​\=*T*(*xt*​), requiring Birkhoff’s ergodic theorem instead of classical concentration inequalities.  
> * **Distributionally Robust Sets (Wasserstein Balls):** Instead of evaluating empirical risk over a static measure *Pn*​, the data distribution is treated as an adversarial variable within a Wasserstein uncertainty set B*ϵ*​(*Pn*​)={*Q*∈P(Z)∣*Wp*​(*Pn*​,*Q*)≤*ϵ*}.  
> * **Pushforward / Transport Spaces:** In generative modeling, the unknown measure *P* is represented via the pushforward *P*\=*T*\#​*μ*0​ of a canonical reference measure *μ*0​ (e.g., standard Gaussian) under a transport map *T*:X0​→X.

### **3\. The Hypothesis Space H**

The space of candidate solutions can be constrained to respect specific algebraic, geometric, or physical symmetries:

> * ***G*****\-Equivariant Morphisms:** For spaces endowed with representations *ρ*X​:*G*→GL(*V*X​) and *ρ*Y​:*G*→GL(*V*Y​), the hypothesis space is restricted to equivariant maps:  
>   H*G*​\={*f*∈H∣*f*(*ρ*X​(*g*)*x*)=*ρ*Y​(*g*)*f*(*x*),∀*g*∈*G*}  
>   By the Peter–Weyl theorem and Schur’s lemma, this decomposes the operator into irreducible representation blocks (e.g., spherical harmonics for SO(3)).  
> * **Symplectic and Contact Mappings:** In Hamiltonian mechanics, H is restricted to vector fields *XH*​ that preserve the canonical symplectic 2-form *ω*\=∑*dqi*​∧*dpi*​ (i.e., L*XH*​​*ω*\=0), enforcing conservation of energy via Noether's theorem.  
> * **Integral and Differential Operators:** In neural operator theory, H is lifted from point mappings to non-linear operators G:B1​→B2​, structured as iterations of kernel integral operators:  
>   G(*u*)(*x*)=*σ*(*Wu*(*x*)+∫Ω​*κθ*​(*x*,*y*)*u*(*y*)*dy*)  
> * **Unitary Ensembles:** In quantum machine learning, H consists of parameterized unitary transformations *U*(*θ*)∈U(HHilbert​).

### **4\. The Loss Functional ℓ (Metric Discrepancy)**

The loss function determines the topology under which predictions are evaluated:

> * **Optimal Transport (Wasserstein Distances):** Replacing pointwise loss with Kantorovich-Rubinstein metrics between distributions:  
>   *W*1​(*P*pred​,*P*target​)=∥*ϕ*∥Lip​≤1sup​∫*ϕd*(*P*pred​−*P*target​)  
>   This provides non-vanishing gradients even when support sets are mutually singular.  
> * **Information-Geometric Metrics:** Replacing Euclidean distances with the Fisher–Rao Riemannian metric or *f*\-divergences on statistical manifolds, yielding coordinate-invariant distance measures over parametric families.  
> * **Sobolev and Dual Graph Laplacians:** Measuring loss over derivatives using Sobolev norms ∥*f*−*y*∥*Hs*(Ω)2​\=∑∣*α*∣≤*s*​∥*Dα*(*f*−*y*)∥*L*22​, forcing the hypothesis to match differential structure and gradient fields.

### **5\. The Regularizer / Inductive Bias Ω**

The prior Ω(*f*) can encode geometric stability rather than simple ℓ*p*​ parameter norms:

> * **Dirichlet Energy on Manifolds:** Constraining functional smoothness across an underlying Riemannian metric *g*:  
>   Ω(*f*)=21​∫M​∥∇*g*​*f*∥*g*2​*d*vol*g*​\=21​⟨*f*,Δ*g*​*f*⟩*L*2(M)​  
>   where Δ*g*​ is the Laplace–Beltrami operator.  
> * **Total Variation (Bounded Variation Spaces):**  
>   Ω(*f*)=∫Ω​∣*Df*∣=sup{∫Ω​*f*div*ϕdx*​*ϕ*∈*Cc*1​(Ω,R*d*),∥*ϕ*∥∞​≤1}  
>   preserving jump discontinuities while suppressing oscillations.  
> * **Spectral / Lipschitz Constraints:** Restricting the operator norm of layer Jacobians ∥*Jf*​(*x*)∥op​≤*γ* to guarantee contractivity via Banach's fixed-point theorem.

### **6\. The Optimization Dynamics A**

The method of traversing the parameter or function space can be replaced to match intrinsic geometries:

> * **Riemannian Optimization:** When parameters lie on constrained manifolds (e.g., Stiefel manifold St(*p*,*n*)={*X*∈R*n*×*p*∣*X*⊤*X*\=*I*} or the cone of Symmetric Positive Definite matrices SPD(*n*)), Euclidean updates are replaced with geodesics via the exponential map:  
>   *θt*\+1​\=Exp*θt*​​(−*η*grad*L*(*θt*​))  
> * **Mirror Descent (Bregman Geometries):** Replacing Euclidean projections with non-Euclidean geometries defined by a strictly convex potential Φ:  
>   *θt*\+1​\=arg*θ*min​{⟨∇*L*(*θt*​),*θ*⟩+*η*1​*D*Φ​(*θ*,*θt*​)}  
>   where *D*Φ​ is the associated Bregman divergence.  
> * **Wasserstein Gradient Flows:** In the infinite-width limit, empirical parameters *θi*​ are treated as particles in a probability measure *ρ*∈P2​(R*d*). The optimization algorithm becomes continuous-time advection along the steepest descent of the functional E(*ρ*) under the 2-Wasserstein metric:  
>   ∂*t*​*ρ*\=∇⋅(*ρ*∇*δρδ*E​)

---

*User prompt: Derive the formal conditions for group-equivariant hypothesis spaces using the representation theory of compact Lie groups and the Peter-Weyl theorem.*

### **Response: 1\. Equivariance and Representation-Theoretic Formulation**

Let *G* be a compact Lie group, and let X and Y be topological vector spaces carrying continuous linear representations (*ρ*in​,X) and (*ρ*out​,Y), where each representation is a Lie group homomorphism *ρ*:*G*→GL(*V*).

A hypothesis space H⊆{*f*:X→Y} is ***G*****\-equivariant** if every candidate map Φ∈H intertwines the group actions:

Φ(*ρ*in​(*g*)*x*)=*ρ*out​(*g*)Φ(*x*),∀*g*∈*G*,∀*x*∈X\[cite: 1, 3\]

If *G* is connected with Lie algebra g\=*Te*​*G*, the global condition is infinitesimally equivalent to the Lie algebra intertwining condition:

*dρ*out​(*X*)∘*d*Φ(*x*)=*d*Φ(*x*)∘*dρ*in​(*X*),∀*X*∈g

which for a linear layer *W* reduces to *Wdρ*in​(*X*)=*dρ*out​(*X*)*W*.

### **2\. Spectral Decomposition via the Peter–Weyl Theorem**

Because *G* is compact, it admits a unique bi-invariant normalized Haar measure *dg* satisfying ∫*G*​*dg*\=1. Let *G* denote the set of equivalence classes of finite-dimensional, irreducible, unitary representations (irreps) of *G*. For each equivalence class *λ*∈*G*, let:

> * *Vλ*​ be the corresponding carrier Hilbert space of finite dimension *dλ*​\=dim(*Vλ*​).  
> * *ρλ*​:*G*→U(*Vλ*​) be a unitary representative.  
> * {*ei*(*λ*)​}*i*\=1*dλ*​​ be an orthonormal basis of *Vλ*​.  
> * *Dijλ*​(*g*)=⟨*ei*(*λ*)​,*ρλ*​(*g*)*ej*(*λ*)​⟩*Vλ*​​ be the matrix coefficient functions.

#### **The Peter–Weyl Theorem**

The collection of normalized matrix coefficients forms a complete orthonormal basis of the Hilbert space *L*2(*G*,*dg*):

B\={*dλ*​​*Dijλ*​​*λ*∈*G*,1≤*i*,*j*≤*dλ*​}

Consequently, under the two-sided regular representation (*Lg*​*Rh*​*ϕ*)(*u*)=*ϕ*(*g*−1*uh*), *L*2(*G*) decomposes into a Hilbert direct sum:

*L*2(*G*)≅⨁​*λ*∈*G*​(*Vλ*​⊗*Vλ*∗​)

with the Schur orthogonality relations:

∫*G*​*Dijλ*​(*g*)*Dklμ*​(*g*)​*dg*\=*dλ*​1​*δλμ*​*δik*​*δjl*​

### **3\. Constraints on Linear Equivariant Layers**

By the complete reducibility of representations of compact groups, any unitary or finite-dimensional representation space *V* decomposes into an isotypic direct sum of irreps:

*V*in​≅*λ*∈*G*⨁​C*m*in​(*λ*)⊗*Vλ*​,*V*out​≅*μ*∈*G*⨁​C*m*out​(*μ*)⊗*Vμ*​

where *m*in​(*λ*) and *m*out​(*μ*) denote the multiplicities of the irreps in the respective spaces.

#### **Application of Schur's Lemma**

Let L:*V*in​→*V*out​ be a bounded linear operator commuting with the *G*\-action: L∘*ρ*in​(*g*)=*ρ*out​(*g*)∘L for all *g*∈*G*.

By Schur's lemma:

> 1. If *λ*≅*μ*, then Hom*G*​(*Vλ*​,*Vμ*​)={0}.  
> 2. If *λ*≅*μ*, then Hom*G*​(*Vλ*​,*Vμ*​)=C⋅Id*Vλ*​​.

Applying this to the isotypic components yields the block-diagonal parameterization of the linear layer:

L\=*λ*∈*G*⨁​(*Wλ*​⊗Id*Vλ*​​)

where *Wλ*​∈C*m*out​(*λ*)×*m*in​(*λ*) are unconstrained trainable weight matrices acting purely on the channel/multiplicity indices, while the geometric transformation across coordinates in *Vλ*​ is fixed as the identity Id*Vλ*​​.

#### **Group Convolutions in Function Space**

When the domain is the group itself (X\=*L*2(*G*)) and the action is the regular representation (*ρ*(*g*)*f*)(*u*)=*f*(*g*−1*u*), every continuous linear equivariant operator L:*L*2(*G*)→*L*2(*G*) must take the form of a group convolution against a filter *ψ*∈*L*2(*G*):

(L*f*)(*g*)=(*f*∗*ψ*)(*g*)=∫*G*​*f*(*h*)*ψ*(*h*−1*g*)*dh*\[cite: 2\]

Using the non-commutative Fourier transform defined via Peter–Weyl:

*f*​(*λ*)=∫*G*​*f*(*g*)*ρλ*​(*g*)†*dg*∈C*dλ*​×*dλ*​

the convolution theorem transforms the operator into independent matrix multiplications across each irreducible frequency:

(L*f*)​(*λ*)=*ψ*​(*λ*)*f*​(*λ*),∀*λ*∈*G*

### **4\. Non-Linearity and the Clebsch–Gordan Decomposition**

A complete hypothesis space H requires non-linear operations *σ*:X→Y. Standard point-wise non-linearities (e.g., ReLU) generally do not preserve the transformation behavior of non-trivial irreps because they do not commute with spatial rotations or group actions.

Equivariant non-linear mappings between irreducible subspaces are constructed through tensor product representations:

*Vλ*1​​⊗*Vλ*2​​≅*ν*∈*G*⨁​*Cλ*1​*λ*2​*ν*​*Vν*​

where the decomposition is realized explicitly by the unitary Clebsch–Gordan transformation:

*vk*(*ν*)​\=*i*\=1∑*dλ*1​​​*j*\=1∑*dλ*2​​​C(*λ*1​,*i*),(*λ*2​,*j*)(*ν*,*k*)​(*vi*(*λ*1​)​⊗*vj*(*λ*2​)​)

The coefficients C(*λ*1​,*i*),(*λ*2​,*j*)(*ν*,*k*)​ are determined by integrating triple products of matrix elements via the Peter–Weyl basis:

C(*λ*1​,*i*),(*λ*2​,*j*)(*ν*,*k*)​∝∫*G*​*Dii*′*λ*1​​(*g*)*Djj*′*λ*2​​(*g*)*Dkk*′*ν*​(*g*)​*dg*

Any continuous, polynomial, or analytic equivariant hypothesis Φ∈H can be factored as a sequence of:

> 1. **Linear intertwining channel mixings:** *Wλ*​⊗Id*Vλ*​​ determined by Schur's Lemma.  
> 2. **Bilinear Clebsch–Gordan tensor contractions:** Mapping pairs (*Vλ*1​​,*Vλ*2​​) into target representations *Vν*​.  
> 3. **Scalar-gated modulations:** *σ*(∥*v*∥)⋅*v*, where ∥*v*∥ is an invariant scalar under unitary action (*λ*\=0, the trivial irrep).

---

