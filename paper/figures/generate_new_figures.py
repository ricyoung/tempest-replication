#!/usr/bin/env python3
"""
Generate new figures for the TEMPEST replication paper.
Following Nature/Springer guidelines with colorblind-safe palette.

New figures:
- Fig 2: Scale vs Safety (Two Panels) - Total vs Active parameters
- Fig 3: Thinking Mode Comparison - Kimi K2 Standard vs Thinking
- Fig 4: Vulnerability Spectrum - Bar chart sorted by parameter count
- Fig 5: Literature Context Matrix - Position our findings in existing research
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import os

# ============================================================================
# NATURE/SPRINGER STYLE CONFIGURATION (same as existing script)
# ============================================================================

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 8
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

# Figure dimensions (inches) - Nature standard widths
SINGLE_COL_WIDTH = 3.54  # ~90mm
DOUBLE_COL_WIDTH = 7.09  # ~180mm
MAX_HEIGHT = 6.69  # ~170mm

# Colorblind-friendly palette (Wong, 2011 - Nature Methods)
COLORS = {
    'blue': '#0072B2',
    'orange': '#E69F00',
    'green': '#009E73',
    'yellow': '#F0E442',
    'sky_blue': '#56B4E9',
    'vermillion': '#D55E00',
    'purple': '#CC79A7',
    'black': '#000000',
    'gray': '#999999',
    'dark_gray': '#333333',
    'light_gray': '#E5E5E5',
    'white': '#FFFFFF',
}

OUTPUT_DIR = '/Volumes/i7_data/_github/Zochi/paper/figures'

# ============================================================================
# MODEL DATA (from experiments)
# ============================================================================

MODELS = {
    'Gemma3 12B': {
        'total': 12e9,
        'active': 12e9,
        'asr': 100,
        'turns': 1.1,
        'type': 'dense',
        'short_name': 'Gemma3'
    },
    'GPT-OSS 20B': {
        'total': 21e9,
        'active': 3.6e9,
        'asr': 78,
        'turns': 9.8,
        'type': 'moe',
        'short_name': 'GPT-OSS 20B'
    },
    'GPT-OSS 120B': {
        'total': 117e9,
        'active': 5.1e9,
        'asr': 73,
        'turns': 11.4,
        'type': 'moe',
        'short_name': 'GPT-OSS 120B'
    },
    'MiniMax M2': {
        'total': 230e9,
        'active': 10e9,
        'asr': 55,
        'turns': 22.7,
        'type': 'moe',
        'short_name': 'MiniMax'
    },
    'GLM-4.6': {
        'total': 357e9,
        'active': 32e9,
        'asr': 99,
        'turns': 2.0,
        'type': 'moe',
        'short_name': 'GLM-4.6'
    },
    'Cogito 2.1': {
        'total': 671e9,
        'active': 671e9,
        'asr': 96,
        'turns': 3.6,
        'type': 'dense',
        'short_name': 'Cogito'
    },
    'DeepSeek V3.1': {
        'total': 671e9,
        'active': 37e9,
        'asr': 99,
        'turns': 1.6,
        'type': 'moe',
        'short_name': 'DeepSeek'
    },
    'Mistral Large 3': {
        'total': 675e9,
        'active': 675e9,
        'asr': 100,
        'turns': 1.0,
        'type': 'dense',
        'short_name': 'Mistral L3'
    },
    'Kimi K2': {
        'total': 1e12,
        'active': 32e9,
        'asr': 97,
        'turns': 1.6,
        'type': 'moe',
        'short_name': 'Kimi K2'
    },
    'Kimi K2 Thinking': {
        'total': 1e12,
        'active': 32e9,
        'asr': 42,
        'turns': 17.2,
        'type': 'moe_thinking',
        'short_name': 'Kimi K2\n(Thinking)'
    },
}


def add_panel_label(ax, label, x=-0.12, y=1.05):
    """Add lowercase bold panel label (Nature style)."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top', ha='left',
            fontfamily='Arial')


def save_figure(fig, basename, dpi=300):
    """Save figure in multiple formats (PNG, PDF, SVG)."""
    for fmt in ['png', 'pdf', 'svg']:
        filepath = os.path.join(OUTPUT_DIR, f'{basename}.{fmt}')
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight',
                    facecolor='white', edgecolor='none', format=fmt)
    print(f"Saved: {basename} (PNG, PDF, SVG)")


# ============================================================================
# FIGURE 2: SCALE VS SAFETY (TWO PANELS)
# ============================================================================

def create_figure2_scale_panels():
    """
    Figure 2: Scale vs Safety - Two-panel scatter plot
    Panel A: Total Parameters vs ASR
    Panel B: Active Parameters vs ASR
    Shows no correlation in either view (critical for H2)
    """
    # Stacked vertically for better readability
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(SINGLE_COL_WIDTH * 1.5, 5.5))

    # Prepare data
    models_no_thinking = {k: v for k, v in MODELS.items() if v['type'] != 'moe_thinking'}

    # Panel A: Total Parameters
    for name, data in models_no_thinking.items():
        marker = 'o' if data['type'] == 'dense' else '^'
        color = COLORS['blue'] if data['type'] == 'dense' else COLORS['orange']
        ax1.scatter(data['total'] / 1e9, data['asr'],
                   marker=marker, s=80, c=color, edgecolors=COLORS['dark_gray'],
                   linewidth=0.5, zorder=5, label=data['type'] if name == list(models_no_thinking.keys())[0] else '')

        # Label points
        offset_y = 3 if data['asr'] < 95 else -5
        offset_x = 0
        if 'Mistral' in name:
            offset_x = -50
        ax1.annotate(data['short_name'], (data['total']/1e9, data['asr']),
                    xytext=(offset_x, offset_y), textcoords='offset points',
                    fontsize=6, ha='center', va='bottom' if offset_y > 0 else 'top')

    ax1.set_xscale('log')
    ax1.set_xlabel('Total Parameters (B)', fontsize=9)
    ax1.set_ylabel('Attack Success Rate (%)', fontsize=9)
    ax1.set_ylim(40, 105)
    ax1.set_xlim(8, 1500)

    # Add correlation annotation
    total_params = [v['total']/1e9 for v in models_no_thinking.values()]
    asrs = [v['asr'] for v in models_no_thinking.values()]
    corr = np.corrcoef(np.log10(total_params), asrs)[0, 1]
    ax1.text(0.95, 0.05, f'r = {corr:.2f} (n.s.)', transform=ax1.transAxes,
            fontsize=7, ha='right', va='bottom', color=COLORS['gray'])

    # Add horizontal line at Zhou & Arel baseline
    ax1.axhline(y=97, color=COLORS['vermillion'], linestyle=':', linewidth=1, alpha=0.7)
    ax1.text(12, 98, 'Zhou & Arel baseline', fontsize=6, color=COLORS['vermillion'])

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    add_panel_label(ax1, 'a')
    ax1.set_title('Total Parameters', fontsize=9, fontweight='bold')

    # Panel B: Active Parameters
    for name, data in models_no_thinking.items():
        marker = 'o' if data['type'] == 'dense' else '^'
        color = COLORS['blue'] if data['type'] == 'dense' else COLORS['orange']
        ax2.scatter(data['active'] / 1e9, data['asr'],
                   marker=marker, s=80, c=color, edgecolors=COLORS['dark_gray'],
                   linewidth=0.5, zorder=5)

        # Label points
        offset_y = 3 if data['asr'] < 95 else -5
        offset_x = 0
        if 'Cogito' in name or 'Mistral' in name:
            offset_x = -30
        ax2.annotate(data['short_name'], (data['active']/1e9, data['asr']),
                    xytext=(offset_x, offset_y), textcoords='offset points',
                    fontsize=6, ha='center', va='bottom' if offset_y > 0 else 'top')

    ax2.set_xscale('log')
    ax2.set_xlabel('Active Parameters (B)', fontsize=9)
    ax2.set_ylabel('Attack Success Rate (%)', fontsize=9)
    ax2.set_ylim(40, 105)
    ax2.set_xlim(2, 1000)

    # Add correlation annotation
    active_params = [v['active']/1e9 for v in models_no_thinking.values()]
    corr_active = np.corrcoef(np.log10(active_params), asrs)[0, 1]
    ax2.text(0.95, 0.05, f'r = {corr_active:.2f} (n.s.)', transform=ax2.transAxes,
            fontsize=7, ha='right', va='bottom', color=COLORS['gray'])

    ax2.axhline(y=97, color=COLORS['vermillion'], linestyle=':', linewidth=1, alpha=0.7)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    add_panel_label(ax2, 'b')
    ax2.set_title('Active Parameters (MoE)', fontsize=9, fontweight='bold')

    # Legend - place on first panel for vertical layout
    dense_marker = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['blue'],
                              markeredgecolor=COLORS['dark_gray'], markersize=8, label='Dense')
    moe_marker = plt.Line2D([0], [0], marker='^', color='w', markerfacecolor=COLORS['orange'],
                            markeredgecolor=COLORS['dark_gray'], markersize=8, label='MoE')
    ax1.legend(handles=[dense_marker, moe_marker], loc='lower left',
               ncol=2, fontsize=8, frameon=True, fancybox=True)

    plt.tight_layout()
    save_figure(fig, 'fig2_scale_panels')
    plt.close()


# ============================================================================
# FIGURE 3: THINKING MODE COMPARISON
# ============================================================================

def create_figure3_thinking():
    """
    Figure 3: Thinking Mode Comparison
    Paired bar chart showing ASR and average turns for Kimi K2 Standard vs Thinking
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL_WIDTH, 3.0))

    # Data
    modes = ['Standard', 'Thinking']
    asr_values = [97, 42]
    turn_values = [1.6, 17.2]

    bar_width = 0.6
    x = np.arange(len(modes))

    # Panel A: ASR Comparison
    bars1 = ax1.bar(x, asr_values, bar_width,
                    color=[COLORS['vermillion'], COLORS['green']],
                    edgecolor=COLORS['dark_gray'], linewidth=1)

    # Add value labels
    for bar, val in zip(bars1, asr_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add improvement arrow
    ax1.annotate('', xy=(1, 47), xytext=(0, 92),
                arrowprops=dict(arrowstyle='->', color=COLORS['dark_gray'], lw=2))
    ax1.text(0.5, 70, '−55 pp', ha='center', va='center', fontsize=9, fontweight='bold',
            color=COLORS['dark_gray'], bbox=dict(boxstyle='round', facecolor='white', edgecolor='none'))

    ax1.set_xticks(x)
    ax1.set_xticklabels(modes, fontsize=9)
    ax1.set_ylabel('Attack Success Rate (%)', fontsize=9)
    ax1.set_ylim(0, 110)
    ax1.set_title('Kimi K2: ASR Reduction', fontsize=10, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    add_panel_label(ax1, 'a')

    # Panel B: Turns Comparison
    bars2 = ax2.bar(x, turn_values, bar_width,
                    color=[COLORS['sky_blue'], COLORS['purple']],
                    edgecolor=COLORS['dark_gray'], linewidth=1)

    for bar, val in zip(bars2, turn_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add multiplier annotation
    ax2.annotate('', xy=(1, 15.5), xytext=(0, 3.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['dark_gray'], lw=2))
    ax2.text(0.5, 9, '10.8×', ha='center', va='center', fontsize=9, fontweight='bold',
            color=COLORS['dark_gray'], bbox=dict(boxstyle='round', facecolor='white', edgecolor='none'))

    ax2.set_xticks(x)
    ax2.set_xticklabels(modes, fontsize=9)
    ax2.set_ylabel('Average Turns to Jailbreak', fontsize=9)
    ax2.set_ylim(0, 22)
    ax2.set_title('Kimi K2: Computational Cost', fontsize=10, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    add_panel_label(ax2, 'b')

    # Overall caption area - key insight
    fig.text(0.5, -0.02,
             'Thinking mode reduces ASR by 55 percentage points but 42% of attacks still succeed',
             ha='center', va='top', fontsize=8, style='italic', color=COLORS['dark_gray'])

    plt.tight_layout()
    save_figure(fig, 'fig3_thinking_comparison')
    plt.close()


# ============================================================================
# FIGURE 4: VULNERABILITY SPECTRUM BY SIZE
# ============================================================================

def create_figure4_spectrum():
    """
    Figure 4: Vulnerability Spectrum
    Bar chart sorted by parameter count (NOT by ASR)
    Shows lack of correlation between size and safety
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 3.5))

    # Sort models by total parameters
    sorted_models = sorted(MODELS.items(), key=lambda x: x[1]['total'])

    # Prepare data
    model_names = [m[1]['short_name'].replace('\n', ' ') for m in sorted_models]
    asr_values = [m[1]['asr'] for m in sorted_models]
    param_labels = []
    for m in sorted_models:
        total = m[1]['total']
        if total >= 1e12:
            param_labels.append(f'{total/1e12:.0f}T')
        else:
            param_labels.append(f'{total/1e9:.0f}B')

    # Colors based on ASR thresholds
    bar_colors = []
    for asr in asr_values:
        if asr >= 90:
            bar_colors.append(COLORS['vermillion'])
        elif asr >= 50:
            bar_colors.append(COLORS['orange'])
        else:
            bar_colors.append(COLORS['green'])

    x = np.arange(len(model_names))
    bars = ax.bar(x, asr_values, color=bar_colors, edgecolor=COLORS['dark_gray'], linewidth=0.5)

    # Add value labels
    for bar, val in zip(bars, asr_values):
        y_pos = bar.get_height() + 1.5
        ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                f'{val}%', ha='center', va='bottom', fontsize=7, fontweight='bold')

    # X-axis with both model name and param count
    ax.set_xticks(x)
    labels = [f'{name}\n({param})' for name, param in zip(model_names, param_labels)]
    ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')

    ax.set_ylabel('Attack Success Rate (%)', fontsize=9)
    ax.set_ylim(0, 115)
    ax.set_xlim(-0.6, len(model_names) - 0.4)

    # Add Zhou & Arel baseline
    ax.axhline(y=97, color=COLORS['dark_gray'], linestyle='--', linewidth=1, alpha=0.7)
    ax.text(len(model_names) - 0.5, 98, 'Zhou & Arel (2025) baseline: 97%',
            fontsize=6, ha='right', va='bottom', color=COLORS['dark_gray'])

    # Add "Sorted by parameter count" annotation
    ax.text(0.02, 0.98, 'Sorted by parameter count →', transform=ax.transAxes,
            fontsize=7, ha='left', va='top', color=COLORS['gray'], style='italic')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend for colors
    high_patch = mpatches.Patch(color=COLORS['vermillion'], label='ASR ≥ 90%')
    mid_patch = mpatches.Patch(color=COLORS['orange'], label='ASR 50-89%')
    low_patch = mpatches.Patch(color=COLORS['green'], label='ASR < 50%')
    ax.legend(handles=[high_patch, mid_patch, low_patch], loc='upper left',
              fontsize=7, frameon=True, fancybox=True)

    add_panel_label(ax, '')

    plt.tight_layout()
    save_figure(fig, 'fig4_vulnerability_spectrum')
    plt.close()


# ============================================================================
# FIGURE 5: LITERATURE CONTEXT MATRIX
# ============================================================================

def create_figure5_literature():
    """
    Figure 5: Literature Context Matrix
    Positions our finding within conflicting literature on thinking mode
    Shows when thinking helps vs hurts based on attack type
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 8)  # Extended to include Key Insight box
    ax.axis('off')

    # Title
    ax.text(5, 7.6, 'Literature Context: When Does Thinking Mode Help?',
            fontsize=11, fontweight='bold', ha='center')

    # Matrix headers
    ax.text(5, 6.9, 'THINKING MODE', fontsize=9, fontweight='bold', ha='center')
    ax.text(3.5, 6.5, 'Disabled', fontsize=8, fontweight='bold', ha='center')
    ax.text(6.5, 6.5, 'Enabled', fontsize=8, fontweight='bold', ha='center')

    # Row headers
    ax.text(1.3, 5.3, 'Reasoning-\nTargeted\nAttacks', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.2)
    ax.text(1.3, 3.3, 'General\nMulti-Turn\nAttacks', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.2)
    ax.text(1.3, 1.3, 'Structured\nReasoning\nDefenses', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.2)

    # Draw grid
    # Vertical lines
    ax.plot([2.5, 2.5], [0.3, 6.2], color=COLORS['dark_gray'], lw=1)
    ax.plot([5, 5], [0.3, 6.2], color=COLORS['dark_gray'], lw=1)
    ax.plot([7.5, 7.5], [0.3, 6.2], color=COLORS['dark_gray'], lw=1)

    # Horizontal lines
    ax.plot([2.5, 7.5], [6.2, 6.2], color=COLORS['dark_gray'], lw=1)
    ax.plot([2.5, 7.5], [4.3, 4.3], color=COLORS['dark_gray'], lw=1)
    ax.plot([2.5, 7.5], [2.3, 2.3], color=COLORS['dark_gray'], lw=1)
    ax.plot([2.5, 7.5], [0.3, 0.3], color=COLORS['dark_gray'], lw=1)

    # Cell contents
    # Row 1: Reasoning-Targeted Attacks
    # Disabled cell - N/A
    na_box = FancyBboxPatch((2.6, 4.4), 2.3, 1.7,
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor=COLORS['light_gray'], edgecolor='none')
    ax.add_patch(na_box)
    ax.text(3.75, 5.3, 'N/A', fontsize=9, ha='center', va='center', color=COLORS['gray'])

    # Enabled cell - VULNERABLE (H-CoT)
    vuln_box1 = FancyBboxPatch((5.1, 4.4), 2.3, 1.7,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#FEE2E2', edgecolor=COLORS['vermillion'], lw=1.5)
    ax.add_patch(vuln_box1)
    ax.text(6.25, 5.7, 'VULNERABLE', fontsize=8, fontweight='bold',
            ha='center', va='center', color=COLORS['vermillion'])
    ax.text(6.25, 5.3, 'H-CoT', fontsize=7, ha='center', va='center', color=COLORS['dark_gray'])
    ax.text(6.25, 4.9, '(98%→2% refusal)', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], style='italic')

    # Row 2: General Multi-Turn Attacks
    # Disabled cell - VULNERABLE (Baseline)
    vuln_box2 = FancyBboxPatch((2.6, 2.4), 2.3, 1.7,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#FEE2E2', edgecolor=COLORS['vermillion'], lw=1.5)
    ax.add_patch(vuln_box2)
    ax.text(3.75, 3.7, 'VULNERABLE', fontsize=8, fontweight='bold',
            ha='center', va='center', color=COLORS['vermillion'])
    ax.text(3.75, 3.3, 'Baseline', fontsize=7, ha='center', va='center', color=COLORS['dark_gray'])
    ax.text(3.75, 2.9, '(97% ASR)', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], style='italic')

    # Enabled cell - PROTECTED (This work) - HIGHLIGHTED
    prot_box1 = FancyBboxPatch((5.1, 2.4), 2.3, 1.7,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#D1FAE5', edgecolor=COLORS['green'], lw=2.5)
    ax.add_patch(prot_box1)
    ax.text(6.25, 3.7, 'PROTECTED', fontsize=8, fontweight='bold',
            ha='center', va='center', color=COLORS['green'])
    ax.text(6.25, 3.3, 'This Work', fontsize=7, fontweight='bold',
            ha='center', va='center', color=COLORS['dark_gray'])
    ax.text(6.25, 2.9, '(42% ASR)', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], style='italic')

    # Row 3: Structured Reasoning Defenses
    # Disabled cell - N/A
    na_box2 = FancyBboxPatch((2.6, 0.4), 2.3, 1.7,
                              boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor=COLORS['light_gray'], edgecolor='none')
    ax.add_patch(na_box2)
    ax.text(3.75, 1.3, 'N/A', fontsize=9, ha='center', va='center', color=COLORS['gray'])

    # Enabled cell - PROTECTED (ARMOR)
    prot_box2 = FancyBboxPatch((5.1, 0.4), 2.3, 1.7,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#D1FAE5', edgecolor=COLORS['green'], lw=1.5)
    ax.add_patch(prot_box2)
    ax.text(6.25, 1.7, 'PROTECTED', fontsize=8, fontweight='bold',
            ha='center', va='center', color=COLORS['green'])
    ax.text(6.25, 1.3, 'ARMOR', fontsize=7, ha='center', va='center', color=COLORS['dark_gray'])
    ax.text(6.25, 0.9, '(0.06% ASR)', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], style='italic')

    # Key insight box
    insight_box = FancyBboxPatch((0.3, -0.6), 9.4, 0.7,
                                  boxstyle="round,pad=0.1,rounding_size=0.1",
                                  facecolor=COLORS['light_gray'],
                                  edgecolor=COLORS['dark_gray'], lw=1)
    ax.add_patch(insight_box)
    ax.text(5, -0.25, 'Key Insight: Thinking mode helps against general attacks but not reasoning-targeted attacks',
            fontsize=8, ha='center', va='center', color=COLORS['dark_gray'], fontweight='bold')

    # Citation column on the right
    ax.text(8.5, 5.3, 'Li et al.\n2025', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], linespacing=1.2)
    ax.text(8.5, 3.3, 'This study\n2025', fontsize=6, ha='center', va='center',
            color=COLORS['dark_gray'], fontweight='bold', linespacing=1.2)
    ax.text(8.5, 1.3, 'Zhao et al.\n2025', fontsize=6, ha='center', va='center',
            color=COLORS['gray'], linespacing=1.2)

    add_panel_label(ax, '', x=0.01, y=0.99)

    plt.tight_layout()
    save_figure(fig, 'fig5_literature_context')
    plt.close()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Generating new figures for TEMPEST replication paper...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    create_figure2_scale_panels()
    create_figure3_thinking()
    create_figure4_spectrum()
    create_figure5_literature()

    print("-" * 50)
    print("All new figures generated successfully!")
    print("\nGenerated figures:")
    print("  - fig2_scale_panels: Two-panel scatter (Total vs Active params)")
    print("  - fig3_thinking_comparison: Kimi K2 Standard vs Thinking")
    print("  - fig4_vulnerability_spectrum: Bar chart sorted by size")
    print("  - fig5_literature_context: Literature positioning matrix")
