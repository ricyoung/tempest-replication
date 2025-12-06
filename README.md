# TEMPEST Replication Study

Replication and comparative analysis of multi-turn adversarial attacks on frontier LLMs.

## Paper

"Replication and Comparative Analysis of Multi-Turn Adversarial Attacks on Frontier Large Language Models"

Richard Young, University of Nevada Las Vegas (December 2025)

## Key Findings

- **10 frontier models tested** across 100 harmful behaviors from JailbreakBench
- **ASR range: 42-100%** - all models vulnerable to multi-turn attacks
- **No scale-safety correlation** (r=-0.12, n.s.) - larger models not safer
- **Thinking mode helps**: Kimi K2 Thinking achieved 42% ASR vs 97% standard mode

## Repository Structure

```
tempest-replication/
├── config.yaml              # Experiment hyperparameters
├── tempest/                  # Attack framework code
│   ├── tempest_pipeline.py   # Main pipeline
│   ├── conversation_attack.py # Multi-turn attack logic
│   ├── ollama_evaluator.py   # LLM-based evaluator
│   └── ...
├── paper/                    # Paper and figures
│   ├── paper_draft.tex       # LaTeX source
│   └── figures/              # All figures (PDF, PNG, SVG)
├── outputs/
│   └── paper_experiments/    # Raw JSON results (10 models × 100 behaviors)
├── run_paper_experiments.sh  # Reproduction script
├── analyze_results.py        # Analysis and figure generation
└── setup.sh                  # Environment setup
```

## Quick Start

```bash
# Setup
./setup.sh

# Configure Ollama endpoint
cp .env.example .env
# Edit .env with your Ollama URL

# Run experiments (requires Ollama with cloud routing)
./run_paper_experiments.sh

# Analyze results
python analyze_results.py
```

## Results Data

JSON files in `outputs/paper_experiments/` contain:
- Behavior index and description
- Attack success/failure (`is_harmful` field)
- Full conversation history
- Query counts (target, evaluator, optimization)

## Citation

```bibtex
@article{young2025tempest,
  title={Replication and Comparative Analysis of Multi-Turn Adversarial Attacks on Frontier Large Language Models},
  author={Young, Richard},
  year={2025},
  institution={University of Nevada Las Vegas}
}
```

## License

MIT License - See LICENSE file

## Related Projects

- **Zochi**: Full research framework - [github.com/IntologyAI/Zochi](https://github.com/IntologyAI/Zochi)

## Acknowledgments

Based on the TEMPEST framework by Zhou & Arel (2025).
