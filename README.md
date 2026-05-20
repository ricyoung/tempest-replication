# Replicating TEMPEST at Scale

**Multi-Turn Adversarial Attacks Against Trillion-Parameter Frontier Models**

<div align="center">
  <img src="imgs/intology-wide.png" width="100%" alt="TEMPEST Replication" />
</div>

<div align="center" style="line-height: 1;">
  <a href="https://github.com/ricyoung/tempest-replication"><img alt="GitHub"
    src="https://img.shields.io/badge/GitHub-tempest--replication-181717?logo=github"/></a>
  <a href="https://huggingface.co/datasets/richardyoung/tempest-replication"><img alt="Hugging Face"
    src="https://img.shields.io/badge/🤗%20Dataset-tempest--replication-yellow"/></a>
  <a href="https://github.com/ricyoung/tempest-replication/blob/main/LICENSE"><img alt="License"
    src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53"/></a>
</div>

**Author:** Richard Young — University of Nevada, Las Vegas (`ryoung@unlv.edu`)

**Status:** Submitted to arXiv on 2025-12-07 (cs.CL primary; cs.CR, cs.AI cross-list).

---

## 1. Overview

This repository contains a large-scale **independent replication** of the TEMPEST multi-turn jailbreak framework (Zhou et al., ACL 2025, formerly *Siege*) extended to ten frontier LLMs released in 2025, ranging from 12 B to ~1 T parameters across eight vendors.

The original TEMPEST paper was produced by Intology's Zochi system and demonstrated near-saturated attack success rates on GPT-3.5/4 and Llama-3.1 on AdvBench. This replication asks a follow-up question:

> *Does additional model scale, newer alignment training, or test-time reasoning ("thinking" mode) confer meaningful resistance to adaptive multi-turn attacks?*

**Short answer:** No. Scale and recency do not provide meaningful protection. Test-time reasoning does.

The upstream TEMPEST framework code lives in [`tempest/`](./tempest) and is largely unchanged from the original release ([IntologyAI/Zochi](https://github.com/IntologyAI/Zochi)). This repo's contribution is the **replication study, dataset, and paper** in [`paper/`](./paper) and [`outputs/`](./outputs).

## 2. Key Findings

- **1,000 behaviors** evaluated (100 JailbreakBench behaviors × 10 target models)
- **97,501 total API queries** issued by the TEMPEST attacker pipeline
- **Overall ASR: 83.9%** — universal vulnerability across vendors and parameter counts
- **Scale is not a defense:** A 12 B open-weight model (Gemma 3) and a 1 T MoE cloud model (Kimi K2) sit within a few points of each other
- **Reasoning *is* a partial defense:** Kimi K2's `thinking` variant dropped ASR by **55 percentage points** (97% → 42%) versus the standard variant, the only intervention in this study that materially moved the needle

### Per-model results (full 100/100 evaluation)

| Model | Vendor | Parameters | ASR |
|---|---|---|---|
| Gemma 3 12B | Google | 12 B | 100% |
| Kimi K2 | Moonshot AI | 1 T (32 B active) | 97% |
| DeepSeek V3.1 | DeepSeek | 671 B | 99% |
| Mistral Large 3 | Mistral | ~123 B | 100% |
| GLM-4.6 | Zhipu AI | 357 B (32 B active) | 99% |
| Cogito 2.1 | Deep Cogito | 671 B | 96% |
| GPT-OSS 120B | OpenAI | 117 B (5.1 B active) | 73% |
| GPT-OSS 20B | OpenAI | 21 B (3.6 B active) | 78% |
| MiniMax M2 | MiniMax | 230 B (10 B active) | 55% |
| **Kimi K2 Thinking** | Moonshot AI | 1 T (32 B active) | **42%** |

Full per-behavior results: [`outputs/supplementary_results.csv`](./outputs/supplementary_results.csv).

## 3. Repository Layout

```
tempest-replication/
├── tempest/                  # Upstream TEMPEST attack framework (Zhou et al., ACL 2025)
├── csreft/                   # Upstream CS-ReFT (unrelated; preserved from Zochi repo)
├── paper/                    # Replication paper, LaTeX source, figures, analysis scripts
│   ├── paper_draft.tex       # 30-page manuscript, 11 figures, 5 tables
│   ├── figures/              # fig1–fig11 (architecture, tree, heatmap, scale panels…)
│   └── secondary_evaluator.py
├── outputs/
│   ├── paper_experiments/    # Per-model raw conversation logs (JSON)
│   └── supplementary_results.csv  # 100 behaviors × 10 models success matrix
├── run_paper_experiments.sh  # Driver script for the full sweep
├── analyze_results.py        # Aggregates JSON logs into the results matrix
└── config.yaml
```

## 4. Reproducing the Replication

### Requirements

- Python 3.10+
- An [Ollama](https://github.com/ollama/ollama) server (local or cloud-routed) for target models
- An attacker-model endpoint (this study used `deepseek-v3.1:671b-cloud`)

### Setup

```bash
git clone https://github.com/ricyoung/tempest-replication.git
cd tempest-replication
./setup.sh
pip install -r tempest/requirements.txt
```

### Run a single target model

```bash
cd tempest
python tempest_pipeline.py \
  --target_model local/gemma3:12b \
  --pipeline_model local/deepseek-v3.1:671b-cloud \
  --results_json ../outputs/paper_experiments/gemma3_12b.json

python get_metrics.py ../outputs/paper_experiments/gemma3_12b.json
```

Set `OLLAMA_BASE_URL` if your server is not at `http://localhost:11434`.

### Reproduce the full sweep

```bash
./run_paper_experiments.sh
python analyze_results.py
```

This regenerates `outputs/supplementary_results.csv` and the inputs for all figures in `paper/figures/`.

### Rebuild the paper

```bash
cd paper
pdflatex -interaction=nonstopmode paper_draft.tex
```

## 5. Ethical Considerations

This work was conducted for **defensive security research**. All generated harmful content remained within the research environment. Significant findings have been or will be communicated to affected model vendors prior to public dissemination. The released artifacts (success/failure matrix, conversation logs) are intended to support defensive evaluation; please use them accordingly.

## 6. Citation

```bibtex
@misc{young2025tempest,
  title  = {Replicating TEMPEST at Scale: Multi-Turn Adversarial Attacks
            Against Trillion-Parameter Frontier Models},
  author = {Young, Richard},
  year   = {2025},
  note   = {arXiv preprint, submitted 2025-12-07},
  url    = {https://github.com/ricyoung/tempest-replication}
}
```

### Upstream framework

```bibtex
@inproceedings{zhou2025tempest,
  title     = {Tempest: Autonomous Multi-Turn Jailbreaking of Large Language Models
               with Tree Search},
  author    = {Zhou, Andy and Arel, Ron and Dunn, Soren and Khandekar, Nikhil},
  booktitle = {Proceedings of ACL},
  year      = {2025}
}
```

See also: the original Zochi project — [IntologyAI/Zochi](https://github.com/IntologyAI/Zochi).

## 7. License

MIT — see [LICENSE](./LICENSE). Upstream Zochi code retains its original MIT license.
