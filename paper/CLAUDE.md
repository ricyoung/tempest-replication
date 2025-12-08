# TEMPEST Replication Paper - Claude Code Instructions

## Project Status: COMPLETED

**Submitted to arXiv:** December 7, 2025
- Category: cs.CL (primary), cs.CR, cs.AI (cross-list)
- Title: "Replicating TEMPEST at Scale: Multi-Turn Adversarial Attacks Against Trillion-Parameter Frontier Models"
- Author: Richard Young (UNLV)

**Resources:**
- GitHub: https://github.com/ricyoung/tempest-replication
- Hugging Face: https://huggingface.co/datasets/richardyoung/tempest-replication
- arXiv archive: `/Volumes/i7_data/_github/Zochi/tempest_arxiv_submission.zip`

---

## Figure Generation - IMPORTANT

When regenerating figures for the paper, **DO NOT run `create_figures.py`**. This old script will overwrite the updated figures with outdated versions.

### Correct workflow:
```bash
cd /Volumes/i7_data/_github/Zochi/paper/figures

# Run ONLY these two scripts:
python3 create_all_figures_nature.py   # Main figures (Fig 1, 2, 3, 4, 5)
python3 generate_new_figures.py        # Additional figures (scale panels, thinking comparison, etc.)

# DO NOT RUN: create_figures.py (overwrites fig1 and fig2 with old designs)
```

### Script purposes:
- `create_all_figures_nature.py` - Nature/Springer style figures with updated designs (Fig 1 architecture, Fig 2 tree, heatmap, etc.)
- `generate_new_figures.py` - Additional analysis figures (scale panels, thinking comparison, vulnerability spectrum, literature context)
- `create_figures.py` - **DEPRECATED** - Old script that conflicts with above. Do not use.

### After generating figures:
```bash
cd /Volumes/i7_data/_github/Zochi/paper
pdflatex -interaction=nonstopmode paper_draft.tex
```

## File Structure
- `paper_draft.tex` - Main LaTeX source (30 pages, 11 figures, 5 tables)
- `figures/` - All figure PDFs (renamed to fig1-fig11 for paper numbering)
- `supplementary_results.csv` - Full 100 behaviors x 10 models results matrix

## Figure Naming (Final)
| Paper Fig | Filename | Description |
|-----------|----------|-------------|
| Fig 1 | fig1_architecture.pdf | TEMPEST system architecture |
| Fig 2 | fig2_tree.pdf | Multi-branch conversation tree |
| Fig 3 | fig3_vulnerability_spectrum.pdf | ASR by model (sorted by params) |
| Fig 4 | fig4_scale_panels.pdf | Scale vs safety (2 panels) |
| Fig 5 | fig5_heatmap.pdf | ASR by harm category |
| Fig 6 | fig6_cost_of_resistance.pdf | Query cost scatter plot |
| Fig 7 | fig7_thinking_comparison.pdf | Kimi K2 thinking vs standard |
| Fig 8 | fig8_attack_progression.pdf | Cumulative jailbreaks by turn |
| Fig 9 | fig9_behavior_funnel.pdf | Behavior difficulty distribution |
| Fig 10 | fig10_literature_context.pdf | Literature context matrix |
| Fig 11 | fig11_turns_dist.pdf | Turns distribution violin plot |

## Key Results Summary
- 10 models evaluated from 8 vendors
- 1,000 behaviors tested (100 per model)
- 97,501 total API queries
- Overall ASR: 83.9%
- Thinking mode reduced ASR by 55 percentage points (97% → 42%)
