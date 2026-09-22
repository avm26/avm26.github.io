# AVM'26 - Program

All accepted talks, grouped by session in programme order.

Short talks are schedules for 15 minutes, long talks for 30 minutes - this includes discussion as well, so please prepare accordingly (i.e., 10 and 20 minute talks).
Invited talks are scheduled for 90 minutes and tutorials for 60 minutes (including discussion).

---

# Tuesday - Industry and Application day

**08:30-09:00 · Registration**

**09:00-09:15 · Opening**

## Research session (morning) - AI and Networked Systems
**When:** Tuesday, 09:15-10:30  ·  **Chair:** Zoltán Micskei

### Soft voting robustness in neural network ensembles with empirical analysis and formal verification
*short*

Neural network ensembles with soft voting improve accuracy and stability by aggregating multiple models; however, their reliability under individual model failure remains a critical concern. This paper addresses the robustness of soft-voting ensembles in safety-critical settings by combining empirical analysis and formal verification. We evaluate the impact of single-model failures on ensemble performance and find that soft voting yields graceful degradation, with only minimal loss in accuracy when one component model is removed or corrupted. In parallel, we develop a formal verification framework to investigate whether the ensemble's final prediction remains unchanged under any single-model failure scenario. The results demonstrate that soft-voting ensembles can maintain reliable outputs despite individual model failures, providing both empirical evidence and provable guarantees of fault tolerance in neural network ensembles.

Roland Gunics
*Eszterházy Károly Catholic University*

Roland Gunics, Gergely Kovásznai, Ádám Kovács, Tibor Tajti

### Explainability and Verifiability of Artificial Intelligence in ICU Mortality Prediction
*long*

A high area under the receiver operating characteristic curve (AUROC) certifies only discrimination; it says nothing about whether an intensive care unit (ICU) mortality model is calibrated, whether its features behave in clinically plausible directions, whether its explanations are stable, or whether it generalizes across hospitals. We argue that such a model should not be trusted until it is verified along these independent axes, and we present an explainability-and-verifiability framework that operationalizes this principle. The framework couples an XGBoost-multilayer perceptron (MLP) soft-voting ensemble, trained on MIMIC-IV (50,920 adult ICU stays, 10.23% in-hospital mortality; 58 features spanning age, seven vital signs, and twelve laboratory measurements, each summarized by mean, minimum, and maximum), with five complementary verification experiments-monotonicity scanning, perturbation robustness, subgroup fairness, explanation stability, and cross-model explanation consistency-delivered at the bedside through a Streamlit-based clinical decision-support (CDSS) prototype. Verification exposes two problems that the model's AUROC of 0.888 conceals, and for each we contribute a diagnostic or repair rather than a single pass/fail verdict. First, only six of sixteen features with an established clinical monotonic prior behaved monotonically; because a binary monotonicity result is not actionable, we introduce a five-segment risk-decomposition A/B/C diagnosis that sorts each of the ten violations into a candidate treatment-confounded reversal (five features), a clinically genuine non-monotonic shape (mean SpO2, a U-shaped curve), a low-importance and low-sensitivity violation (one C-moderate feature), or an unresolved "investigate" case (three features). Second, because soft-voting averages rather than cancels systematic component bias, component-level Platt scaling on the XGBoost branch reduced the expected calibration error (ECE) from 0.090 to 0.006 internally and, under strict external validation on eICU-CRD (138,868 stays, 9.46% mortality), from 0.167 to 0.045, with Brier scores improving in parallel while AUROC held at 0.856. Across these experiments we find that AUROC and ECE degrade asynchronously under distribution shift and that explanations are only moderately stable (top-three SHAP stability 52.3%), reinforcing our central claim: discrimination, calibration, monotonicity, and explanation stability must be verified jointly, not inferred from any single headline metric.

Chen Yuqi
*Eszterházy Károly Catholic University*

Chen Yuqi and Kovásznai Gergely

### Safety Analysis in Broadcast Networks Defined by Graph Grammars
*long*

We consider families of networks where processes communicate by synchronous broadcast (i.e., a sent message is received by all the neighbours of the emitter) and we study the following safety problem: is there a network in the given family, such that some process can reach an error location? Specifically, we focus on families of network topologies defined by graph grammars, where each node of the produced graph can be either a clique or a cloud (anti-clique) of processes of unbounded sizes. We show that, in general, the considered safety problem is undecidable, when the communication is reliable, and becomes decidable with unreliable communication (i.e., broadcast messages can be lost) or whenever the protocols executed by the different processes cannot send and receive messages from the same control state (also known as the wait-only syntactic restriction).

Christoffer Lind Andersen
*Verimag, CNRS*

Christoffer Lind Andersen; Radu Iosif; Arnaud Sangnier

**10:30-11:00 · Coffee break**

## Invited talk 1
**When:** Tuesday, 11:00-12:30  ·  **Chair:** Zoltán Micskei

### Formal methods for critical control systems at CERN

The CERN BE-ICS group is integrating formal methods into the engineering and validation of safety-relevant control systems for particle accelerators and their industrial installations. In this talk we cover our recent activities and ongoing real-world applications of formal verification for programmable logic controller (PLC) programs, neural network controllers, and industrial C++ code. For PLC program verification our group has invested substantial resources over the last decade to develop the PLCverif platform for model checking based PLC verification. We give an overview over the framework and share recent experience reports of applying it to CERN projects. On neural networks we present recent works and challenges: how to evaluate and verify robustness against perturbations under real-world conditions, and the challenge of verifying stability of neural-network based approximate MPC for closed-loop controls of industrial installations. Finally, we present early-stage work on applying model checking to C++ code for the validation of a critical control system.

Xaver Fink
*CERN*

Xaver Fink, Borja Fernandez Adiego

**12:30-14:00 · Lunch**

## Tutorial
**When:** Tuesday, 14:00-15:00  ·  **Chair:** Zsófia Ádám

### Soundness Is Not Security: Layered Verification of BPMN Collaborations with the Tamarin Prover

A BPMN collaboration is a model of a business process performed by several organizations. Traditional verification of such models tends to focus on traces in which every participant plays by the rules laid out by the standard BPMN semantics. Our goal is to extend the analysis to scenarios where adversaries also participate. A dishonest procurement coordinator, for instance, may decide to award a contract to two different suppliers simultaneously instead of one, to hedge its own supply chain risk. Standard semantics rule out this trace, so existing verification tooling does not even look for it. On a platform that merely authenticates messages this scheme is executable. This gap is not specific to BPMN. Whatever a checker proves about a multi-party model holds only for runs in which every party keeps to the model.

In this tutorial, we reason about those traces with Tamarin, a prover used to verify security protocols. The BPMN process is encoded as a Tamarin theory through the correspondence between place/transition nets, the usual semantics of BPMN, and multiset rewriting, the language of Tamarin. In that encoding, a dishonest participant is a rewriting rule set that may emit any message the platform accepts, not just the ones allowed by the process. The model has two layers: the process, and the platform that carries the messages between participants. Swapping either layer lets us test one process over a range of orchestration platforms, and one platform against many processes. The takeaways are the prover, its Petri-net reading, and a question worth asking of any multi-party model: what does its verification results quantify over, and where could it be broken? A 20-minute take-home exercise with a Docker image has attendees write one platform layer themselves, predict which of the collaboration's security properties survive, then run the prover. No prior exposure to Tamarin or BPMN is assumed.

Martin Farkas
*BME, Budapest*

Martin Farkas, Dr. Imre Kocsis

**15:00-15:30 · Coffee break**

## Research session (afternoon) - Embedded- and Real-Time Systems
**When:** Tuesday, 15:30-16:30  ·  **Chair:** Levente Bajczi

### Bridging testing and formal methods: equivalence detection and test generation for mutation testing in PLC software
*short*

Programmable logic controllers (PLCs) are often used in safety-critical industrial automation, and thus require rigorous software verification. While formal verification provides strong mathematical guarantees, dynamic testing remains the primary approach in industrial practice, despite the challenges of evaluating cyclically executed PLC code. Mutation testing can effectively assess and improve these test suites, but engineers still find designing tests for surviving mutants and identifying equivalent mutants challenging. In this talk, I will demonstrate how formal model checking, specifically utilizing the PLCverif framework, can be used for both equivalence detection and test case generation for live mutants. Finally, I'll show how this formal methodology integrates into a broader, AI-driven test improvement and generation framework currently in development.

Andrada Alexia Serban
*BME, Budapest*

Andrada Alexia Serban

### A Symbolic Execution Framework for Symbolic Timing Analysis of Digital Integrated Circuits
*short*

Simulation-based dynamic timing analysis of digital integrated circuits (DDTA) offers a faster alternative to traditional analog SPICE simulations. To achieve timing predictions that are reasonably competitive in terms of accuracy, however, DDTA mandates gate delay models that go beyond the standard pure or inertial delay models used in state-of-the-art tools. Recent advances in analytic gate delay models, which now also capture effects like drafting and multi-input switching, unlock new possibilities for timing analysis, which go way beyond simulation-based approaches towards an exhaustive exploration. In this paper, we present the cornerstones of a novel symbolic execution framework, which utilizes such analytic delay models for automatically computing symbolic delay expressions for all paths in a digital circuit, for some given ordering of the input transitions. To reduce combinatorial explosion, we introduce symbolic pruning methods that also enable path-sensitive, goal-driven reasoning about timing properties and analytic optimization of specific circuit paths.
The reported prototype evaluation is restricted to finite, acyclic NOR
circuits with a single positive symbolic constant delay shared by all gates. It measures the effects of constraint propagation, exact symbolic-configuration quotienting, and certified closed-frontier POR.

Dennis Eigner
*TU Wien*

Dennis Eigner, Arman Ferdowsi, Ulrich Schmid

### Unified Timing-Aware Program Verification
*long*

Three complementary verification approaches exist for real-time concurrent programs: (i) Timed Automata (TA) model checkers reason rigorously about timing but cannot express C’s memory model and synchronization primitives. (ii) Program verifiers handle advanced language features but ignore timing, producing spurious errors when timing makes races impossible. (iii) Worst-Case Execution Time (WCET) analyzers bound execution time but cannot verify safety properties.
We present a vision for timing-aware program verification and propose a workflow that integrates: (i) TA semantics, (ii) existing C program verifier capabilities, and (iii) WCET timing estimates. We identify three key research challenges and demonstrate feasibility through a prototype implementation in the Theta software model checker. Our prototype demonstrates the potential to eliminate false positives from timing-infeasible scenarios and verify real-time properties previously impossible to express in C program verifiers.
This talk is an extended version of the one previously presented at FASE 2026.

Dóra Cziborová
*BME, Budapest*

Dóra Cziborová, Mihály Dobos-Kovács, Kristóf Marussy, András Vörös

---

# Wednesday - Model checking, Exchange Formats and SMT

## Research session (morning) - Model Checking and Exchange Formats
**When:** Wednesday, 09:00-10:30  ·  **Chair:** Dirk Beyer

### Combining formal verification algorithms
*short*

Model checking is a formal verification technique that exhaustively explores all possible behaviors of a system to prove correctness or detect errors. Two prominent approaches are Complementary Approximate Reachability (CAR), which simultaneously tightens over- and under-approximations of reachable states, and Counterexample-Guided Abstraction Refinement (CEGAR), which iteratively refines a coarse abstraction until the property can be decided.

Implicit abstraction allows wrapping any reachability algorithm in a CEGAR loop, but discards all intermediate results upon each refinement.

In this paper, we propose CARCEGAR, an algorithm that wraps CAR in an implicit CEGAR loop while preserving partial results across refinement iterations. We unify the underapproximation tree of CAR with the abstract reachability graph of CEGAR into a single structure, enabling lazy pruning to retain useful state-space information between iterations. We implemented the algorithm in the open-source Theta model checker and evaluated it on industrial hardware models from the Hardware Model Checking Competition, where it showed promising results.

Dániel Kovács
*BME, Budapest*

Dániel Kovács, Milán Mondok

### Bringing Saturation to Concurrent Software
*long*

Saturation is a symbolic reachability algorithm for asynchronous systems. It works well because transitions in such systems are mostly local: each event reads and writes only a few variables, and saturation iterates along that structure instead of applying the whole transition relation at every step. Until now, this has been limited to models with explicit or limited next-state relations, mainly Petri nets. Software models, where transitions are given as logical formulas, are usually checked with SMT-based methods (BMC, CEGAR, ...) that do not use locality.

This talk is about bringing saturation to a much wider set of domains: any transition system that can be described using SMT formulas. Substitution diagrams (presented in an earlier AVM talk) let saturation take SMT predicates as its next-state relation. Substitution diagrams lazily enumerate a decision-diagram-like structure using SMT queries during exploration. One problem comes up that does not exist for Petri nets: successor values at one level can depend on variables at lower levels, and the recursion may not terminate. We handle this with look-ahead, which uses the state set explored so far to bound the iteration.

The approach is implemented in Theta. We evaluated it on Petri nets, DVE models, and concurrent C programs. For concurrent C, we are competitive with partial-order CEGAR. On Petri nets and DVE, a constant-factor overhead separates us from dedicated saturation engines.

Milán Mondok
*BME, Budapest*

Milán Mondok, Vince Molnár

### Precision Reuse for Exchange between Verifiers
*short*

Program changes made during the evolution of software may invalidate verification results, therefore, every program version needs to be (re)verified. Performing a complete reverification, however, is too costly to keep up with today’s frequent program changes. In 2013, precision reuse was introduced as a means to speed up the iterative computation of an abstraction level that is appropriate for verification. In an external reproduction and replication study, we examine the major claims and observations of the original study and find that they mostly remain valid and carry over, but the benefits of precision reuse are less significant. We further observe that the format used in the original study has limited use for exchange, as it contains verifier-specific elements. Thus, we additionally propose a verifier-independent exchange format for precisions, and evaluate its utility in 3 abstraction-based verification tools. Our evaluation shows that cooperation between verifiers by exchanging precisions can improve verification performance, solving tasks that could not be solved by any of the verifiers alone.

Márk Somorjai
*LMU Munich*

Paulína Ayaziová, Dirk Beyer, Marie-Christine Jakobs, Martin Jonáš, Marian Lingsch-Rosenfeld, Jindřich Sedláček, Márk Somorjai, Jan Strejček

### Transition Invariants Revisited: Termination Witnesses and Their Validation
*long*

Whenever automated provers such as automatic software verifiers deliver a verdict (true or false), they are expected to produce also a witness that justifies the verdict. This allows independent validation of the verdict using the witness by a third party, increasing trust in the results. The current standard exchange formats for witnesses in software verification do not support program termination. To fill this gap, we propose an extension of the witness format that is based on transition invariants as a general and effective formalism. We justify this by (a) proving that transition invariants can encode other popular termination arguments like ranking functions and (b) providing three different validation approaches for transition invariants, which together can validate most of the exported witnesses. Our approach based on transition invariants was integrated into version 2.1 of the recently released witness format, and the software-verification community has adopted the format for SV-COMP.

Marek Jankola
*LMU Munich*

Dirk Beyer, Marek Jankola, and Marian Lingsch-Rosenfeld

**10:30-11:00 · Coffee break**

## Invited talk 2
**When:** Wednesday, 11:00-12:30  ·  **Chair:** András Vörös

### Industrial experiences in the use of static analysis

Static analysis is a method that allows us to examine source code without running it. Its scope of application is wide: it ranges from code understanding to software vulnerability discovery. Its great advantage is that it provides early feedback in modern CI pipelines, and we know that the sooner we fix a bug, the lower its cost.

Static analysis is a popular topic in the academic world. But how does it perform in practice, in a real industrial environment?

In my talk, I will report on the experiences we have gained from the CodeChecker infrastructure, jointly developed by Ericsson and Eötvös Loránd University, over the past nearly 10 years. CodeChecker is a framework that controls the execution of several static analyzers and provides their results to developers in a unified way. It is used by Apple, Google, Sony, BMW, and many others. The paid version of GitLab provides this as a built-in static analysis service.

Zoltán Porkoláb
*Eötvös Loránd University, Faculty of Informatics*

Zoltán Porkoláb

**12:30-14:00 · Lunch**

## Tutorial
**When:** Wednesday, 14:00-15:00  ·  **Chair:** András Vörös

### SV-LIB 1.0: A Standard Exchange Format for Software-Verification Tasks

In the past two decades, significant research and development effort went into the development of verification tools for individual languages, such as C, C++, and Java. Many of the used verification approaches are in fact language-agnostic and it would be beneficial for the technology transfer to allow for using the implementations also for other programming and modeling languages. To address the problem, we propose SV-LIB, an exchange format and intermediate language for software-verification tasks, including programs, specifications, and verification witnesses. SV-LIB is based on well-known concepts from imperative programming languages and uses SMT-LIB to represent expressions and sorts used in the program. This makes it easy to parse and to build into existing infrastructure, since many verification tools are based on SMT solvers already. Furthermore, SV-LIB defines a witness format for both correct and incorrect SV-LIB programs, together with means for specifying witness-validation tasks. This makes it possible both to implement independent witness validators and to reuse some verifiers also as validators for witnesses. This talk will present version 1.0 of the SV-LIB format, including its design goals, the syntax, and informal semantics. Formal semantics and further extensions to concurrency are planned for future versions.

Marian Lingsch-Rosenfeld
*LMU Munich*

Dirk Beyer, Gidon Ernst, Martin Jonáš, Marian Lingsch-Rosenfeld

**15:00-15:30 · Coffee break**

## Research session (afternoon) - SAT/SMT
**When:** Wednesday, 15:30-17:00  ·  **Chair:** Dirk Beyer

### Inductive Satisfiability Certification for Universal Quantifiers and Uninterpreted Function Symbols
*long*

The combination of uninterpreted function symbols and universal quantification occurs in many applications of automated reasoning, for example, as it enables reasoning about arrays. Yet the satisfiability of such formulas is, in general, undecidable. In practice, SMT solvers are often successful in the unsatisfiable case, using heuristics. However, in the satisfiable case, they rely on explicit model construction, which fails for formulas whose smallest model is not small enough. We introduce an alternative approach that certifies satisfiability using induction arguments, and apply it to the case of linear integer arithmetic. The resulting algorithm is able to prove satisfiability of formulas that are out of reach for current SMT solvers.

Anggha Stefan Nugraha
*Institute of Computer Science Czech Academy of Sciences*

Marek Dančo, Mikoláš Janota, Anggha Nugraha, and Stefan Ratschan

### Model Enumeration using IPASIR-UP without Blocking Clauses
*short*

The Boolean satisfiability problem (SAT) is a fundamental NP-complete problem with numerous applications in verification and reasoning. While modern Conflict-Driven Clause Learning (CDCL) based SAT solvers efficiently compute single satisfying assignments, many applications require enumerating all solutions (AllSAT). This is challenging due to their potentially exponential number and the inefficiency of standard techniques such as blocking clauses. Implementing a model enumerator through the IPASIR-UP interface allows to leverage highly optimized SAT solvers such as CaDiCaL while maintaining a clear separation between the solver and the enumeration logic. This modular approach ensures that the enumerator remains independent of a specific solver implementation, requiring only compliance with the interface. As a result, improvements in underlying solvers can be directly utilized without modifying the enumerator, enabling both flexibility and long-term maintainability. This thesis presents CaDiCAll: a model enumerator without blocking clauses using the IPASIR-UP interface.

Timpe Hörig
*University Freiburg*

Timpe Hörig

### Solving Sums over Arrays with LIA-star
*long*

In formal software verification, SMT solvers play an important role. They act as the backend of verification queries. The availability of decidable theories and efficient decision procedures is therefore crucial. One such theory is the theory of arrays defined by read and write. Several extensions have been studied in the past, including combinatory array logic, array folds logic or cartesian array logic. However, theories that support summation over arrays have received little attention so far. Only recently has this extension been investigated. The talk presents the theory extension by sum constraints. Particular focus is placed on the connection to LIA*, a theory extension of linear integer arithmetic by a star operator that allows constraints about the possible result of an iterated summation process over a set. It is shown how both arrays with bounded sums and arrays with unbounded sums can be reduced to LIA* and, consequently, decided in nondeterministic polynomial time.

Roland Graf
*University of Regensburg*

Philipp Rümmer, Roland Graf

### Z3-Nooder and Mata: String Solving with Stabilization and Transducers
*short*

We generalize an efficient automata-based approach to string solving, the stabilization-based method behind the solver Z3-Noodler, to support relational constraints represented by finite-state transducers (useful for modeling replaceAll constraints, etc.). We focus on efficient handling of length constraints by reducing the need for expensive concatenation elimination, a major bottleneck in automata-based string solving. We also propose heuristics that significantly improve performance in practice. Implemented on top of Z3-Noodler, our method clearly outperforms other solvers on benchmarks with relational constraints: it solves more instances and runs orders of magnitude faster.

David Chocholatý
*Brno University of Technology*

David Chocholatý, Vojtěch Havlena, Lukáš Holík, Michal Šedý, Juraj Síč

**18:00-22:00 · Wine dinner (at the venue's wine cellar)**

---

# Thursday - Software, Automata and Graphs

## Research session (morning) - Software Verification and Formalisation
**When:** Thursday, 09:00-10:30  ·  **Chair:** Oszkár Semeráth

### Universality of 1-Variable Automata is Decidable
*short*

Variable Automata (VA) are an extension of finite-state automata to infinite alphabets, where transition labels represent non-reassignable variables, allowing for the comparison of input letters. VA are applied in the modelling of systems that require unbounded data domains, such as sequence solving or XML documents with data values. The increased expressiveness comes at a price, as the universality problem (i.e., deciding whether a VA accepts all possible words over a fixed alphabet) is undecidable for VA. Our research is motivated by the close relationship between the universality problem and the complementation of languages, an operation that is often required in verification. We have shown that the universality problem is decidable when restricted to VA over a single variable, and will present the key ideas behind the construction in this talk.

Franziska Alber
*University of Regensburg*

Franziska Alber, Philipp Rümmer

### Proof assistant-based formalisation of Core Erlang
*long*

Refactoring tools are essential for software maintenance, yet they are rarely formally verified-causing developers to rely on manual transformations due to a lack of trust. This issue served as the motivation for our research over recent years: a machine-checked formalisation of Core Erlang, the sublanguage of Erlang, which is an impure functional programming language featuring strict evaluation, uncurried function abstractions, lightweight processes, and asynchronous communication. By using a formal semantics of Core Erlang and suitable program equivalence definitions, we can prove that a refactoring is correct if the programs before and after transformation are equivalent (i.e. they behave the same way).

This talk presents key results from our work: a reduction-style formal semantics for both the sequential features and a representative concurrent subset of Core Erlang, along with multiple semantics-based program equivalence concepts. We discuss how these equivalence definitions-including barbed bisimulation for concurrent setups-were successfully applied to verify the correctness of program refactorings and optimisations. Finally, we highlight our experiences and insights from machine-checking these formal definitions, equivalences, and proofs in the Rocq proof assistant. Beyond proving behaviour preservation, this formal framework also serves as the foundation for our current research: building a formally verified Erlang compiler.

Péter Bereczky
*Eötvös Loránd University, Faculty of Informatics*

Péter Bereczky

### A Unified Evaluation of Translation and Algorithmic Impacts in Hardware Verification
*short*

Formal verification is essential for ensuring system correctness, with BTOR2 serving as the standard word-level format for bit-precise hardware model checking. Recent approaches bridge hardware and software verification by translating BTOR2 designs into C programs to exploit mature software analyzers. Notably, tools like CPAchecker have demonstrated that software verifiers can detect bugs that state-of-the-art hardware checkers miss. However, routing designs through an intermediate C representation adds syntactic overhead, distorts native bit-vector semantics, and risks translation defects. Furthermore, evaluating across entirely separate tools makes fair comparisons difficult, as it is hard to separate fundamental algorithmic strengths from tool-specific engineering tricks. To isolate these effects, we implement a direct BTOR2 frontend within the generic Theta model checking framework, converting hardware models directly into Control Flow Automata (CFAs). This native mapping preserves bit-precise SMT semantics and hardware loop structures without extra layers. Leveraging Theta’s unified infrastructure for both hardware and C models, we evaluate HWMCC benchmarks under identical algorithmic conditions, revealing how direct versus indirect transformations truly impact verification performance.

Éva Mária Szabó
*BME, Budapest*

Éva Mária Szabó

### Combining Partial Order Reduction and Abstraction
*long*

Formal verification of concurrent software faces two major challenges: the state space explosion problem from data complexity, and the combinatorial explosion of thread interleavings. Abstraction and partial order reduction (POR) are well-established techniques for addressing these challenges individually. However, even their orthogonal application - when applying a traditional partial order reduction algorithm on an abstract state space - is not trivially sound. The talk presents a motivating example demonstrating the non-triviality of the combination of these techniques and outlines why this combination is still sound. Furthermore, partial order reduction can be extended to take abstraction into account to achieve further state space reduction. Specifically, the dependency relation used to decide the commutativity of actions for partial order reduction can be relaxed to ignore dependencies when the source of dependency (e.g., a shared variable) is invisible in the abstraction. Experiments reveal that this abstraction-aware extension is as powerful as the applied abstraction: the more details ignored by the abstraction, the better reduction is achieved.

Csanád Telbisz
*BME, Budapest*

Csanád Telbisz

**10:30-11:00 · Coffee break**

## Invited talk 3
**When:** Thursday, 11:00-12:30  ·  **Chair:** Levente Bajczi

### Refinery: A graph solver for generating models

TBA

Oszkár Semeráth
*BME, Budapest*

TBA

**12:30-14:00 · Lunch**

## Tutorial
**When:** Thursday, 14:00-15:00  ·  **Chair:** Oszkár Semeráth

### Modeling with Uncertainty: Using Refinery for Automated Graph Generation

In the realm of software and hardware verification, rigorously testing systems often requires generating complex, structurally valid input models, configurations, or network topologies. Refinery is an open-source graph solver designed to automate this exact process. By combining the mathematical precision of formal logic with the expressiveness of partial graph models, Refinery enables engineers to define structural constraints and automatically generate diverse, well-formed graphs. This capability is highly valuable for verification workflows, whether for synthesizing test scenarios, analyzing distributed architectures, or systematically exploring design alternatives under uncertainty.

This short tutorial provides a practical, fast-paced introduction to the Refinery framework. Participants will learn how to define a metamodel, write formal constraints using Refinery’s logical predicate language, and utilize the solver to complete partial models. By the end of the session, attendees will understand how to leverage Refinery’s web-based IDE and underlying graph algorithms to enhance their own verification and testing pipelines with automated, constraint-driven model generation.

Attila Ficsor
*BME, Budapest*

Attila Ficsor

**15:00-15:15 · Closing remarks (a few minutes)**

**15:15-15:45 · Coffee break**
