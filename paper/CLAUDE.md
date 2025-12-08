# TEMPEST Paper - Claude Code Instructions

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
- `paper_draft.tex` - Main LaTeX source
- `figures/` - All figure PDFs, PNGs, SVGs
- `supplementary_results.csv` - Full 100 behaviors x 10 models results matrix
