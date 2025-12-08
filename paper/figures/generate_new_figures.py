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
        'active': 37e9,  # MoE based on DeepSeek architecture
        'asr': 96,
        'turns': 3.6,
        'type': 'moe',
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
        'active': 41e9,  # Sparse MoE with 41B active parameters
        'asr': 100,
        'turns': 1.0,
        'type': 'moe',
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
    # Custom label positioning with arrows for clustered high-ASR region
    # Total params: Gemma3=12B, GPT-OSS 20B=21B, GPT-OSS 120B=117B, MiniMax=230B,
    #               GLM-4.6=357B, Cogito=671B, DeepSeek=671B, Mistral=675B, Kimi=1000B
    label_config_a = {
        'Gemma3': (0, 6, 'center', 'bottom', False),           # 12B, 100% - alone
        'GPT-OSS 20B': (0, 6, 'center', 'bottom', False),      # 21B, 78% - alone
        'GPT-OSS 120B': (0, 6, 'center', 'bottom', False),     # 117B, 73% - alone
        'MiniMax': (0, 6, 'center', 'bottom', False),          # 230B, 55% - alone
        'GLM-4.6': (15, 8, 'left', 'bottom', True),            # 357B, 99% - right
        'Cogito': (40, -15, 'left', 'top', True),              # 671B, 96% - right, down
        'DeepSeek': (-45, 8, 'right', 'bottom', True),         # 671B, 99% - left, up
        'Mistral L3': (-55, -8, 'right', 'top', True),         # 675B, 100% - far left
        'Kimi K2': (15, 6, 'left', 'bottom', True),            # 1000B, 97% - right
    }

    for name, data in models_no_thinking.items():
        marker = 'o' if data['type'] == 'dense' else '^'
        color = COLORS['blue'] if data['type'] == 'dense' else COLORS['orange']
        ax1.scatter(data['total'] / 1e9, data['asr'],
                   marker=marker, s=80, c=color, edgecolors=COLORS['dark_gray'],
                   linewidth=0.5, zorder=5, label=data['type'] if name == list(models_no_thinking.keys())[0] else '')

        # Get custom config for this model
        short_name = data['short_name'].replace('\n', ' ')
        offset_x, offset_y, ha, va, use_arrow = label_config_a.get(short_name, (0, 6, 'center', 'bottom', False))

        if use_arrow:
            ax1.annotate(data['short_name'], (data['total']/1e9, data['asr']),
                        xytext=(offset_x, offset_y), textcoords='offset points',
                        fontsize=6, ha=ha, va=va,
                        arrowprops=dict(arrowstyle='-', color=COLORS['gray'], lw=0.5))
        else:
            ax1.annotate(data['short_name'], (data['total']/1e9, data['asr']),
                        xytext=(offset_x, offset_y), textcoords='offset points',
                        fontsize=6, ha=ha, va=va)

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
    # Custom label positioning with arrows for the clustered high-ASR region
    # Active params: Gemma3=12B, GPT-OSS 20B=3.6B, GPT-OSS 120B=5.1B, MiniMax=10B,
    #                GLM-4.6=32B, Kimi K2=32B, Cogito=37B, DeepSeek=37B, Mistral=41B
    label_config = {
        'Gemma3': (0, 6, 'center', 'bottom', False),           # 12B, 100% - alone
        'GPT-OSS 20B': (-15, 6, 'center', 'bottom', False),    # 3.6B, 78% - alone
        'GPT-OSS 120B': (-15, -10, 'center', 'top', False),    # 5.1B, 73% - below
        'MiniMax': (0, 6, 'center', 'bottom', False),          # 10B, 55% - alone
        'GLM-4.6': (55, 15, 'left', 'center', True),           # 32B, 99% - far right, HIGH
        'Kimi K2': (-50, 8, 'right', 'center', True),          # 32B, 97% - far left, up
        'Cogito': (-55, -12, 'right', 'center', True),         # 37B, 96% - far left, down
        'DeepSeek': (60, -3, 'left', 'center', True),          # 37B, 99% - far right
        'Mistral L3': (25, 22, 'left', 'bottom', True),        # 41B, 100% - up HIGH, right
    }

    for name, data in models_no_thinking.items():
        marker = 'o' if data['type'] == 'dense' else '^'
        color = COLORS['blue'] if data['type'] == 'dense' else COLORS['orange']
        ax2.scatter(data['active'] / 1e9, data['asr'],
                   marker=marker, s=80, c=color, edgecolors=COLORS['dark_gray'],
                   linewidth=0.5, zorder=5)

        # Get custom config for this model
        short_name = data['short_name'].replace('\n', ' ')
        offset_x, offset_y, ha, va, use_arrow = label_config.get(short_name, (0, 6, 'center', 'bottom', False))

        if use_arrow:
            ax2.annotate(data['short_name'], (data['active']/1e9, data['asr']),
                        xytext=(offset_x, offset_y), textcoords='offset points',
                        fontsize=6, ha=ha, va=va,
                        arrowprops=dict(arrowstyle='-', color=COLORS['gray'], lw=0.5))
        else:
            ax2.annotate(data['short_name'], (data['active']/1e9, data['asr']),
                        xytext=(offset_x, offset_y), textcoords='offset points',
                        fontsize=6, ha=ha, va=va)

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
    ax.text(len(model_names) - 0.5, 108, 'Zhou & Arel (2025) baseline: 97%',
            fontsize=7, fontweight='bold', ha='right', va='bottom', color=COLORS['dark_gray'])

    # Add "Sorted by parameter count" annotation
    ax.text(0.02, 0.98, 'Sorted by parameter count →', transform=ax.transAxes,
            fontsize=7, ha='left', va='top', color=COLORS['gray'], style='italic')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend for colors - positioned at bottom right to avoid overlapping bars
    high_patch = mpatches.Patch(color=COLORS['vermillion'], label='ASR ≥ 90%')
    mid_patch = mpatches.Patch(color=COLORS['orange'], label='ASR 50-89%')
    low_patch = mpatches.Patch(color=COLORS['green'], label='ASR < 50%')
    ax.legend(handles=[high_patch, mid_patch, low_patch], loc='lower right',
              fontsize=7, frameon=True, fancybox=True, ncol=3)

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
    Redesigned for clarity - clean, professional, no internal borders
    """
    # 18% wider to fill the page
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH * 1.18, 4.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.8, 8)
    ax.axis('off')
    ax.set_facecolor('white')

    # Title
    ax.text(5, 7.5, 'Literature Context: When Does Thinking Mode Help?',
            fontsize=12, fontweight='bold', ha='center', color=COLORS['dark_gray'])

    # Column headers
    ax.text(5, 6.85, 'THINKING MODE', fontsize=10, fontweight='bold', ha='center',
            color=COLORS['dark_gray'])
    ax.text(3.5, 6.4, 'Disabled', fontsize=9, fontweight='bold', ha='center',
            color='#555555')
    ax.text(6.5, 6.4, 'Enabled', fontsize=9, fontweight='bold', ha='center',
            color='#555555')

    # Row headers (darker, more readable)
    ax.text(1.2, 5.2, 'Reasoning-\nTargeted\nAttacks', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.3, color='#333333')
    ax.text(1.2, 3.2, 'General\nMulti-Turn\nAttacks', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.3, color='#333333')
    ax.text(1.2, 1.2, 'Structured\nReasoning\nDefenses', fontsize=8, fontweight='bold',
            ha='center', va='center', linespacing=1.3, color='#333333')

    # No grid lines - cleaner professional look

    # === ROW 1: Reasoning-Targeted Attacks ===
    # Disabled - N/A (no border)
    ax.add_patch(FancyBboxPatch((2.55, 4.25), 2.3, 1.7,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#F0F0F0', edgecolor='none'))
    ax.text(3.7, 5.1, 'N/A', fontsize=10, ha='center', va='center',
            color='#888888', fontweight='bold')

    # Enabled - VULNERABLE (H-CoT) - subtle shadow effect via background
    ax.add_patch(FancyBboxPatch((5.15, 4.25), 2.3, 1.7,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#FECACA', edgecolor='none'))
    ax.text(6.3, 5.6, 'VULNERABLE', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#DC2626')
    ax.text(6.3, 5.15, 'H-CoT', fontsize=8, ha='center', va='center', color='#333333')
    ax.text(6.3, 4.75, '(98%→2% refusal)', fontsize=7, ha='center', va='center',
            color='#666666', style='italic')

    # === ROW 2: General Multi-Turn Attacks ===
    # Disabled - VULNERABLE (Baseline)
    ax.add_patch(FancyBboxPatch((2.55, 2.35), 2.3, 1.6,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#FED7AA', edgecolor='none'))
    ax.text(3.7, 3.65, 'VULNERABLE', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#EA580C')
    ax.text(3.7, 3.2, 'Baseline', fontsize=8, ha='center', va='center', color='#333333')
    ax.text(3.7, 2.8, '(97% ASR)', fontsize=7, ha='center', va='center',
            color='#666666', style='italic')

    # Enabled - PROTECTED (This work) - HIGHLIGHTED
    ax.add_patch(FancyBboxPatch((5.15, 2.35), 2.3, 1.6,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#BBF7D0', edgecolor='none'))
    ax.text(6.3, 3.65, 'PROTECTED', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#16A34A')
    ax.text(6.3, 3.2, 'This Work', fontsize=8, fontweight='bold',
            ha='center', va='center', color='#333333')
    ax.text(6.3, 2.8, '(42% ASR)', fontsize=7, ha='center', va='center',
            color='#666666', style='italic')

    # === ROW 3: Structured Reasoning Defenses ===
    # Disabled - N/A
    ax.add_patch(FancyBboxPatch((2.55, 0.35), 2.3, 1.7,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#F0F0F0', edgecolor='none'))
    ax.text(3.7, 1.2, 'N/A', fontsize=10, ha='center', va='center',
            color='#888888', fontweight='bold')

    # Enabled - PROTECTED (ARMOR)
    ax.add_patch(FancyBboxPatch((5.15, 0.35), 2.3, 1.7,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#BBF7D0', edgecolor='none'))
    ax.text(6.3, 1.65, 'PROTECTED', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#16A34A')
    ax.text(6.3, 1.2, 'ARMOR', fontsize=8, ha='center', va='center', color='#333333')
    ax.text(6.3, 0.8, '(0.06% ASR)', fontsize=7, ha='center', va='center',
            color='#666666', style='italic')

    # Key insight box (clean minimal design)
    ax.add_patch(FancyBboxPatch((0.5, -0.55), 9.0, 0.6,
                                 boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#F5F5F5', edgecolor='none'))
    ax.text(5, -0.25, 'Key Insight: Thinking mode helps against general attacks but not reasoning-targeted attacks',
            fontsize=8, ha='center', va='center', color='#333333', fontweight='bold')

    # Citation column (darker, more readable)
    ax.text(8.7, 5.2, 'Li et al.\n2025', fontsize=7, ha='center', va='center',
            color='#666666', linespacing=1.2)
    ax.text(8.7, 3.2, 'This study\n2025', fontsize=7, ha='center', va='center',
            color='#333333', fontweight='bold', linespacing=1.2)
    ax.text(8.7, 1.2, 'Zhao et al.\n2025', fontsize=7, ha='center', va='center',
            color='#666666', linespacing=1.2)

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
