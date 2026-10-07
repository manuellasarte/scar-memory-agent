# Scar Memory Agent: Adaptive-Pressure Scar Formation for Emergent Capabilities

## Subtitle
A mechanism for transforming recurring failures into persistent capabilities in autonomous software agents.

---

## Abstract
We present a mechanism by which an autonomous agent transforms recurring failures into persistent capabilities through the formation of "scars". Unlike repetition-based approaches that count identical errors, our mechanism models scar formation as a function of cumulative *adaptive pressure*, combining failure frequency, severity, and impact. We evaluate against a repetition-based baseline across two experiments: a probabilistic stream of 500 events and a curated stream of rare severe failures. The adaptive-pressure agent achieved 29.8% higher average capability utility and 50.0% higher survival rate in Experiment 001, and detected 100% of rare severe failures that the baseline missed entirely in Experiment 002. A multi-seed study across 10 independent seeds confirms these results are not artifacts of a single seed. All results are reproducible from a fixed seed and a shared error stream.

---

## 1. Introduction
Autonomous agents that operate over long horizons accumulate failures. Most systems treat failures as transient events: they log, retry, and move on. The failure leaves no persistent trace, and the agent repeats the same mistake indefinitely. This is a learning problem, not a memory problem.

We propose a mechanism that transforms recurring failures into persistent *scars*, and scars into *capabilities*. A scar is a structural modification of agent behavior, formed only when the cumulative *adaptive pressure* of a failure class exceeds a threshold. Adaptive pressure combines three dimensions: **frequency** (how often), **severity** (how damaging), and **impact** (how far consequences propagate).

This departs from repetition-based approaches. Repetition is a poor proxy for relevance. A thousand trivial warnings are not equivalent to a single data corruption event. Our core claim is that *adaptive pressure*, not frequency, is the correct signal for structural adaptation.

### Contributions
1. **A mechanism**: scar formation based on cumulative adaptive pressure.
2. **A lifecycle**: capabilities emerge from scars and must justify their existence through measurable utility (NACIENTE → ACTIVA → CONSOLIDADA).
3. **An empirical evaluation**: two complementary experiments against a repetition baseline, with a 10-seed robustness study.

---

## 2. Related Work
Our work sits at the intersection of four lines. **Memory in cognitive architectures** (Soar, ACT-R) modifies behavior through rule learning, but assumes a symbolic rule base and frequency-based triggers. **Evolutionary agents** (NEAT, POET) adapt at population level, not within a single lifetime. **Failure-tolerant systems** (circuit breakers, retry policies) react to failures but do not create persistent capabilities. **Biological scarring** is a metaphor: scars are structural modifications produced by system history, not errors or logs.

The gap: none combines (P1) multi-dimensional pressure triggering, (P2) an evolutionary lifecycle for capabilities, and (P3) full reproducible persistence. Our mechanism satisfies all three.

---

## 3. Methodology

### 3.1 Wound Model
A *wound* records a failure event: `error_type` (string), `severity` (0–1), `impact` (0–1), `created_at`. Wounds are never deleted; they form the immutable evidence base.

### 3.2 Adaptive Pressure
For an error type `e` observed `n` times:

freq_norm(e) = min(n / 10, 1)
sev_avg(e) = mean(severity of wounds of type e)
imp_avg(e) = mean(impact of wounds of type e)
pressure(e) = freq_norm(e) * 0.4 + sev_avg(e) * 0.3 + imp_avg(e) * 0.3


The weights (0.4, 0.3, 0.3) are a priori. All components are in [0, 1].

**Design intuition**: A single event with severity=0.95, impact=0.99 yields pressure=0.622 (above threshold). Ten trivial events (severity=0.1, impact=0.1) yield pressure=0.46 (below threshold). Pressure rewards severity-weighted histories, not merely frequent ones.

### 3.3 Scar Formation
A scar is created when `pressure(e) >= tau`, where `tau = 0.55`. The scar record stores the computed pressure, threshold, formula version, and links every contributing wound.

### 3.4 Capability Registry and Lifecycle
Each scar gives rise to a *capability*. States: `NACIENTE → ACTIVA → CONSOLIDADA → OBSOLETA → RETIRADA`. Transitions:
- `usage_count >= 20 and utility_score >= 0.8` → CONSOLIDADA
- `usage_count >= 5 and utility_score >= 0.5` → ACTIVA

Capabilities must earn persistence through measurable utility.

### 3.5 Persistence and Reproducibility
Every wound, scar, capability, usage, and state transition is stored in SQLite. The entire pipeline runs with one command (`bash reproduce.sh`).

---

## 4. Experimental Setup

### 4.1 Error Streams
- **Stream A (probabilistic)**: 500 events (50% TRIVIAL, 30% MODERATE, 20% SEVERE), seed=42.
- **Stream B (curated)**: 34 events (25 TRIVIAL, 6 MODERATE, 1 SEVERE_DATA_CORRUPTION, 2 SEVERE_AUTH_BYPASS), seed=42.

### 4.2 Agents
- **A — Adaptive Pressure**: forms scar when pressure ≥ 0.55.
- **B — Repetition Rule**: forms scar when same error type occurs ≥ 3 times.

### 4.3 Utility Model
Utility is modeled by error class: TRIVIAL→0.2, MODERATE→0.6, SEVERE→0.9. This is a declared assumption.

---

## 5. Results

### 5.1 Experiment 001 — General Performance
| Metric | A | B |
|---|---|---|
| Scars formed | 2 | 3 |
| Capabilities born | 2 | 3 |
| Avg utility | 0.7500 | 0.5778 |
| Survival rate | 1.0000 | 0.6667 |
| False scar rate | 0.0000 | 0.3333 |

A produced fewer, higher-quality scars, with zero false positives.

### 5.2 Experiment 002 — Safety Property
| Metric | A | B |
|---|---|---|
| Missed severe rate | 0.0000 | 1.0000 |
| Detected severe | 2/2 | 0/2 |
| False scar rate | 0.0000 | 0.5000 |

A detected 100% of rare severe failures; B missed 100% of them.

### 5.3 Multi-Seed Robustness (10 seeds)
| Metric | A (mean±std) | B (mean±std) | A wins |
|---|---|---|---|
| Avg utility | 0.7500±0.0638 | 0.5667±0.0419 | 10/10 |
| Survival rate | 1.0000±0.0000 | 0.7334±0.1405 | 8/10 |
| False scar rate | 0.0000±0.0000 | 0.3333±0.0000 | 10/10 |

The advantage holds across all ten seeds for utility and false-positive rate.

---

## 6. Discussion
Two claims are supported. **First**, pressure separates signal from noise: the repetition rule cannot distinguish 25 trivial events from 25 corruption events. **Second**, scarcity is not irrelevance: a single corruption may outweigh hundreds of warnings. The lifecycle reinforces this: capabilities earn persistence through utility.

---

## 7. Limitations
- Synthetic streams, not real-world telemetry.
- Declared utility model, not empirically measured.
- Single-agent evaluation.
- Fixed threshold (0.55).

---

## 8. Conclusion
We presented a mechanism that transforms recurring failures into persistent capabilities through adaptive pressure. It consistently produces fewer, higher-utility capabilities, never produces false-positive scars, and never misses severe failures. All results are reproducible from a fixed seed and a shared error stream.

---

## Reproducibility Statement
The full pipeline can be re-executed with:

python3 -m src.run_experiment
python3 -m src.run_experiment_002
python3 -m src.multiseed_experiment

All configurations, seeds, and result files are available in the repository.

---

## References
- Laird, J. E. (2012). *The Soar Cognitive Architecture*. MIT Press.
- Anderson, J. R. (2007). *How Can the Human Mind Occur in the Physical Universe?* Oxford University Press.
- Stanley, K. O., & Miikkulainen, R. (2002). Evolving neural networks through augmenting topologies. *Evolutionary Computation*, 10(2), 99–127.
- Wang, R., et al. (2019). POET: Paired Open-Ended Trailblazer. *arXiv:1901.01753*.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software*. Pragmatic Bookshelf.
