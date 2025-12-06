#!/usr/bin/env python3
"""
Generate all figures following Nature/Springer journal guidelines:
- Sans-serif font (Arial/Helvetica)
- Accessible colorblind-friendly palette (avoid red/green)
- Lowercase bold panel labels (a, b, c...)
- Single-column (~90mm/3.54in) or double-column (~180mm/7.09in) width
- Max height ~170mm (~6.7in)
- 300 DPI minimum resolution
- Vector formats (PDF, SVG) + high-res PNG
- Font sizes legible after reduction (8pt minimum)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np
import os

# ============================================================================
# NATURE/SPRINGER STYLE CONFIGURATION
# ============================================================================

# Set global font to Arial (Helvetica fallback)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 8  # Base font size
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
# Avoids red/green confusion
COLORS = {
    'blue': '#0072B2',       # Strong blue
    'orange': '#E69F00',     # Orange
    'green': '#009E73',      # Bluish green (safe)
    'yellow': '#F0E442',     # Yellow
    'sky_blue': '#56B4E9',   # Sky blue
    'vermillion': '#D55E00', # Vermillion (orange-red, not pure red)
    'purple': '#CC79A7',     # Reddish purple
    'black': '#000000',
    'gray': '#999999',
    'dark_gray': '#333333',
    'light_gray': '#E5E5E5',
    'white': '#FFFFFF',
}

# Semantic color mapping for figures
SEMANTIC_COLORS = {
    'attacker': COLORS['vermillion'],
    'attacker_light': '#FFEDD5',
    'target': COLORS['blue'],
    'target_light': '#DBEAFE',
    'evaluator': COLORS['green'],
    'evaluator_light': '#D1FAE5',
    'success': COLORS['green'],
    'warning': COLORS['orange'],
    'pruned': COLORS['gray'],
    'pruned_light': '#F3F4F6',
    'active': COLORS['blue'],
    'active_light': '#DBEAFE',
    'promising': COLORS['green'],
    'promising_light': '#D1FAE5',
    'arrow': COLORS['dark_gray'],
    'text': COLORS['black'],
    'accent': COLORS['orange'],
}

OUTPUT_DIR = '/Volumes/i7_data/_github/Zochi/paper/figures'


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
# FIGURE 1: SYSTEM ARCHITECTURE
# ============================================================================

def create_figure1_architecture():
    """
    Figure 1: TEMPEST System Architecture
    Double-column width, shows attacker-target-evaluator flow
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_facecolor('white')

    # Add panel label
    add_panel_label(ax, 'a', x=0.01, y=0.99)

    # Title (will be in figure caption in paper)
    ax.text(6, 6.6, 'TEMPEST System Architecture',
            fontsize=11, fontweight='bold', ha='center', va='top',
            color=SEMANTIC_COLORS['text'])
    ax.text(6, 6.25, 'Multi-Turn Adversarial Attack Framework',
            fontsize=9, ha='center', va='top', color=COLORS['gray'],
            style='italic')

    # Component dimensions
    box_width = 2.6
    box_height = 1.9
    box_y = 3.2

    # --- ATTACKER MODEL ---
    attacker_x = 1.0

    # Shadow
    shadow = FancyBboxPatch((attacker_x + 0.04, box_y - 0.04), box_width, box_height,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor='#00000010', edgecolor='none')
    ax.add_patch(shadow)

    # Main box
    attacker_box = FancyBboxPatch((attacker_x, box_y), box_width, box_height,
                                   boxstyle="round,pad=0.06,rounding_size=0.12",
                                   facecolor=SEMANTIC_COLORS['attacker_light'],
                                   edgecolor=SEMANTIC_COLORS['attacker'], linewidth=2)
    ax.add_patch(attacker_box)

    # Header
    header = FancyBboxPatch((attacker_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor=SEMANTIC_COLORS['attacker'], edgecolor='none')
    ax.add_patch(header)
    ax.text(attacker_x + box_width/2, box_y + box_height - 0.22, 'ATTACKER',
            fontsize=9, fontweight='bold', ha='center', va='center', color='white')

    # Content
    ax.text(attacker_x + box_width/2, box_y + 1.1, 'DeepSeek-v3.1',
            fontsize=8, ha='center', va='center', color=SEMANTIC_COLORS['text'], fontweight='bold')
    ax.text(attacker_x + box_width/2, box_y + 0.8, '671B Parameters',
            fontsize=7, ha='center', va='center', color=COLORS['gray'])
    ax.text(attacker_x + box_width/2, box_y + 0.4, '"Siege" Agent',
            fontsize=7, ha='center', va='center', color=SEMANTIC_COLORS['attacker'],
            fontweight='bold', style='italic')

    # --- TARGET MODEL ---
    target_x = 4.7

    shadow = FancyBboxPatch((target_x + 0.04, box_y - 0.04), box_width, box_height,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor='#00000010', edgecolor='none')
    ax.add_patch(shadow)

    target_box = FancyBboxPatch((target_x, box_y), box_width, box_height,
                                 boxstyle="round,pad=0.06,rounding_size=0.12",
                                 facecolor=SEMANTIC_COLORS['target_light'],
                                 edgecolor=SEMANTIC_COLORS['target'], linewidth=2)
    ax.add_patch(target_box)

    header = FancyBboxPatch((target_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor=SEMANTIC_COLORS['target'], edgecolor='none')
    ax.add_patch(header)
    ax.text(target_x + box_width/2, box_y + box_height - 0.22, 'TARGET',
            fontsize=9, fontweight='bold', ha='center', va='center', color='white')

    ax.text(target_x + box_width/2, box_y + 1.1, 'Victim LLM',
            fontsize=8, ha='center', va='center', color=SEMANTIC_COLORS['text'], fontweight='bold')
    models_text = 'Kimi-k2 (1T) | GLM-4.6\nCogito-2.1 | Gemma3'
    ax.text(target_x + box_width/2, box_y + 0.55, models_text,
            fontsize=7, ha='center', va='center', color=COLORS['gray'],
            linespacing=1.2)

    # --- EVALUATOR ---
    eval_x = 8.4

    shadow = FancyBboxPatch((eval_x + 0.04, box_y - 0.04), box_width, box_height,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor='#00000010', edgecolor='none')
    ax.add_patch(shadow)

    eval_box = FancyBboxPatch((eval_x, box_y), box_width, box_height,
                               boxstyle="round,pad=0.06,rounding_size=0.12",
                               facecolor=SEMANTIC_COLORS['evaluator_light'],
                               edgecolor=SEMANTIC_COLORS['evaluator'], linewidth=2)
    ax.add_patch(eval_box)

    header = FancyBboxPatch((eval_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor=SEMANTIC_COLORS['evaluator'], edgecolor='none')
    ax.add_patch(header)
    ax.text(eval_x + box_width/2, box_y + box_height - 0.22, 'EVALUATOR',
            fontsize=9, fontweight='bold', ha='center', va='center', color='white')

    ax.text(eval_x + box_width/2, box_y + 1.1, 'Harm Classifier',
            fontsize=8, ha='center', va='center', color=SEMANTIC_COLORS['text'], fontweight='bold')
    ax.text(eval_x + box_width/2, box_y + 0.75, 'Primary: DeepSeek-v3.1',
            fontsize=7, ha='center', va='center', color=COLORS['gray'])
    ax.text(eval_x + box_width/2, box_y + 0.5, 'Secondary: Llama-Guard-3',
            fontsize=7, ha='center', va='center', color=COLORS['gray'])

    # --- ARROWS ---
    arrow_style = dict(arrowstyle='->', color=SEMANTIC_COLORS['arrow'],
                       lw=1.5, mutation_scale=12)

    # Attacker -> Target
    ax.annotate('', xy=(target_x - 0.08, box_y + box_height/2),
                xytext=(attacker_x + box_width + 0.08, box_y + box_height/2),
                arrowprops=arrow_style)

    # Label
    label_box = FancyBboxPatch((3.45, 4.45), 1.15, 0.35,
                                boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor='white', edgecolor=SEMANTIC_COLORS['arrow'], linewidth=1)
    ax.add_patch(label_box)
    ax.text(4.025, 4.625, 'Attack\nPrompt', fontsize=6, ha='center', va='center',
            color=SEMANTIC_COLORS['text'], fontweight='bold', linespacing=0.9)

    # Target -> Evaluator
    ax.annotate('', xy=(eval_x - 0.08, box_y + box_height/2),
                xytext=(target_x + box_width + 0.08, box_y + box_height/2),
                arrowprops=arrow_style)

    label_box = FancyBboxPatch((7.15, 4.45), 1.15, 0.35,
                                boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor='white', edgecolor=SEMANTIC_COLORS['arrow'], linewidth=1)
    ax.add_patch(label_box)
    ax.text(7.725, 4.625, 'Response', fontsize=6, ha='center', va='center',
            color=SEMANTIC_COLORS['text'], fontweight='bold')

    # Feedback loop
    feedback_style = dict(arrowstyle='->', color=COLORS['gray'],
                          lw=1.5, linestyle='--', mutation_scale=12,
                          connectionstyle='arc3,rad=0.35')

    ax.annotate('', xy=(attacker_x + box_width/2, box_y - 0.25),
                xytext=(eval_x + box_width/2, box_y - 0.25),
                arrowprops=feedback_style)

    # Feedback label
    feedback_box = FancyBboxPatch((4.9, 2.2), 2.2, 0.5,
                                   boxstyle="round,pad=0.06,rounding_size=0.08",
                                   facecolor=COLORS['light_gray'], edgecolor=COLORS['gray'], linewidth=1)
    ax.add_patch(feedback_box)
    ax.text(6, 2.55, 'Feedback Loop', fontsize=7, ha='center', va='center',
            color=COLORS['dark_gray'], fontweight='bold')
    ax.text(6, 2.32, 'Adapt strategy based on score', fontsize=6, ha='center', va='center',
            color=COLORS['gray'])

    # --- STEP NUMBERS ---
    step_style = dict(fontsize=8, fontweight='bold', color='white', ha='center', va='center')

    for i, (x_pos, color) in enumerate([
        (attacker_x + box_width/2, SEMANTIC_COLORS['attacker']),
        (target_x + box_width/2, SEMANTIC_COLORS['target']),
        (eval_x + box_width/2, SEMANTIC_COLORS['evaluator'])
    ], 1):
        circle = Circle((x_pos, box_y + box_height + 0.25), 0.18,
                        facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x_pos, box_y + box_height + 0.25, str(i), **step_style)

    # --- ATTACK STRATEGIES BAR ---
    info_box = FancyBboxPatch((0.6, 0.35), 10.8, 1.4,
                               boxstyle="round,pad=0.08,rounding_size=0.12",
                               facecolor=COLORS['light_gray'], edgecolor=COLORS['gray'], linewidth=1)
    ax.add_patch(info_box)

    ax.text(6, 1.5, '7 Attack Strategies', fontsize=8, ha='center', va='center',
            color=SEMANTIC_COLORS['text'], fontweight='bold')

    strategies = [
        'Refusal\nSuppression', 'Dual\nResponse', 'Response\nPriming',
        'Persona\nModification', 'Hypothetical\nFraming', 'Topic\nSplitting', 'Opposite\nIntent'
    ]

    pill_colors = [SEMANTIC_COLORS['attacker'], SEMANTIC_COLORS['target'],
                   SEMANTIC_COLORS['evaluator'], SEMANTIC_COLORS['accent'],
                   SEMANTIC_COLORS['attacker'], SEMANTIC_COLORS['target'],
                   SEMANTIC_COLORS['evaluator']]

    start_x = 0.95
    for i, (strategy, color) in enumerate(zip(strategies, pill_colors)):
        pill_width = 1.35
        x = start_x + i * 1.52
        pill = FancyBboxPatch((x, 0.55), pill_width, 0.55,
                               boxstyle="round,pad=0.02,rounding_size=0.15",
                               facecolor=color, edgecolor='none', alpha=0.15)
        ax.add_patch(pill)
        ax.text(x + pill_width/2, 0.82, strategy, fontsize=5.5, ha='center', va='center',
                color=color, fontweight='bold', linespacing=0.85)

    plt.tight_layout()
    save_figure(fig, 'fig1_architecture')
    plt.close()


# ============================================================================
# FIGURE 2: MULTI-BRANCH CONVERSATION TREE
# ============================================================================

def create_figure2_tree():
    """
    Figure 2: Multi-Branch Conversation Tree
    Double-column width, shows BFS exploration with pruning
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 5.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('white')

    # Panel label
    add_panel_label(ax, 'b', x=0.01, y=0.99)

    # Title
    ax.text(7, 8.7, 'Multi-Branch Conversation Tree',
            fontsize=11, fontweight='bold', ha='center', color=SEMANTIC_COLORS['text'])
    ax.text(7, 8.35, 'Breadth-First Search with Adaptive Pruning',
            fontsize=9, ha='center', color=COLORS['gray'], style='italic')

    # --- ROOT NODE ---
    root_box = FancyBboxPatch((4.5, 7.4), 5, 0.65,
                               boxstyle="round,pad=0.08,rounding_size=0.12",
                               facecolor=COLORS['dark_gray'], edgecolor=COLORS['black'], linewidth=1.5)
    ax.add_patch(root_box)
    ax.text(7, 7.82, 'TARGET BEHAVIOR', fontsize=9, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(7, 7.55, '"Generate harmful content about X"', fontsize=7,
            ha='center', va='center', color=COLORS['light_gray'], style='italic')

    # --- TURN LABELS ---
    turn_labels = ['TURN 1', 'TURN 2', 'TURN 3']
    turn_y = [6.0, 4.0, 2.0]

    for label, y in zip(turn_labels, turn_y):
        turn_box = FancyBboxPatch((0.3, y - 0.22), 1.1, 0.44,
                                   boxstyle="round,pad=0.04,rounding_size=0.08",
                                   facecolor=COLORS['dark_gray'], edgecolor='none')
        ax.add_patch(turn_box)
        ax.text(0.85, y, label, fontsize=7, fontweight='bold',
                ha='center', va='center', color='white')

    # --- TURN 1 NODES ---
    turn1_data = [
        ('Academic\nFraming', 4, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light']),
        ('Security\nAudit', 6, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light']),
        ('Fiction\nWriting', 3, SEMANTIC_COLORS['pruned'], SEMANTIC_COLORS['pruned_light']),
        ('Bundled\nRequest', 7, SEMANTIC_COLORS['promising'], SEMANTIC_COLORS['promising_light']),
        ('Roleplay', 5, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light']),
        ('Filter\nCalibration', 4, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light']),
    ]

    turn1_x = [2.0, 3.8, 5.6, 7.4, 9.2, 11.0]

    for i, ((label, score, color, bg_color), x) in enumerate(zip(turn1_data, turn1_x)):
        node = FancyBboxPatch((x - 0.62, 5.52), 1.24, 0.96,
                               boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor=bg_color, edgecolor=color, linewidth=1.5)
        ax.add_patch(node)

        ax.text(x, 6.18, label, fontsize=6, ha='center', va='center',
                color=color, fontweight='bold', linespacing=0.9)
        ax.text(x, 5.72, f'Score: {score}', fontsize=6, ha='center', va='center',
                color=COLORS['gray'])

        # Arrow from root
        ax.plot([7, x], [7.4, 6.52], color=SEMANTIC_COLORS['arrow'], lw=1.2, alpha=0.6)
        ax.plot([x], [6.52], marker='v', markersize=5, color=SEMANTIC_COLORS['arrow'], alpha=0.6)

    # Pruned label
    ax.text(5.6, 5.22, 'PRUNED', fontsize=6, ha='center', color=SEMANTIC_COLORS['pruned'],
            fontweight='bold')

    # --- TURN 2 NODES ---
    turn2_data = [
        ('Escalate\nDetail', 5, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light'], 2.0),
        ('Add\nUrgency', 7, SEMANTIC_COLORS['promising'], SEMANTIC_COLORS['promising_light'], 3.8),
        ('Split\nTopics', 9, SEMANTIC_COLORS['promising'], SEMANTIC_COLORS['promising_light'], 7.4),
        ('Persona\nShift', 6, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light'], 10.1),
    ]

    turn2_x = [2.9, 5.0, 7.4, 10.1]

    for (label, score, color, bg_color, parent_x), x in zip(turn2_data, turn2_x):
        node = FancyBboxPatch((x - 0.58, 3.52), 1.16, 0.96,
                               boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor=bg_color, edgecolor=color, linewidth=1.5)
        ax.add_patch(node)

        ax.text(x, 4.18, label, fontsize=6, ha='center', va='center',
                color=color, fontweight='bold', linespacing=0.9)
        ax.text(x, 3.72, f'Score: {score}', fontsize=6, ha='center', va='center',
                color=COLORS['gray'])

        ax.plot([parent_x, x], [5.52, 4.52], color=SEMANTIC_COLORS['arrow'], lw=1.2, alpha=0.6)
        ax.plot([x], [4.52], marker='v', markersize=5, color=SEMANTIC_COLORS['arrow'], alpha=0.6)

    # Highlight promising (Score 9)
    highlight = plt.Circle((7.4, 4.0), 0.82, fill=False, color=SEMANTIC_COLORS['warning'],
                           lw=2, linestyle='--')
    ax.add_patch(highlight)
    ax.text(8.45, 4.25, 'Promising!', fontsize=7, color=SEMANTIC_COLORS['warning'], fontweight='bold')

    # --- TURN 3 NODES ---
    turn3_data = [
        ('Deeper\nFraming', 6, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light'], 2.9),
        ('Context\nOverload', 7, SEMANTIC_COLORS['active'], SEMANTIC_COLORS['active_light'], 5.0),
        ('Authority\nAppeal', 5, SEMANTIC_COLORS['pruned'], SEMANTIC_COLORS['pruned_light'], 10.1),
    ]

    turn3_x = [3.2, 5.5, 10.1]

    for (label, score, color, bg_color, parent_x), x in zip(turn3_data, turn3_x):
        node = FancyBboxPatch((x - 0.52, 1.52), 1.04, 0.86,
                               boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor=bg_color, edgecolor=color, linewidth=1.5)
        ax.add_patch(node)

        ax.text(x, 2.12, label, fontsize=6, ha='center', va='center',
                color=color, fontweight='bold', linespacing=0.9)
        ax.text(x, 1.72, f'Score: {score}', fontsize=6, ha='center', va='center',
                color=COLORS['gray'])

        ax.plot([parent_x, x], [3.52, 2.42], color=SEMANTIC_COLORS['arrow'], lw=1.2, alpha=0.6)
        ax.plot([x], [2.42], marker='v', markersize=5, color=SEMANTIC_COLORS['arrow'], alpha=0.6)

    ax.text(10.1, 1.22, 'PRUNED', fontsize=6, ha='center', color=SEMANTIC_COLORS['pruned'],
            fontweight='bold')

    # --- SUCCESS NODE ---
    success_box = FancyBboxPatch((6.88, 1.52), 1.24, 0.86,
                                  boxstyle="round,pad=0.04,rounding_size=0.08",
                                  facecolor=SEMANTIC_COLORS['success'], edgecolor='#166534', linewidth=2)
    ax.add_patch(success_box)
    ax.text(7.5, 2.08, 'SUCCESS', fontsize=8, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(7.5, 1.72, 'Score: 10', fontsize=7, ha='center', va='center',
            color='white')

    ax.plot([7.4, 7.5], [3.52, 2.42], color=SEMANTIC_COLORS['success'], lw=2)
    ax.plot([7.5], [2.42], marker='v', markersize=6, color=SEMANTIC_COLORS['success'])

    # --- SUCCESS CALLOUT ---
    callout = FancyBboxPatch((9.1, 0.65), 3.4, 1.4,
                              boxstyle="round,pad=0.08,rounding_size=0.12",
                              facecolor=SEMANTIC_COLORS['promising_light'],
                              edgecolor=SEMANTIC_COLORS['success'], linewidth=1.5)
    ax.add_patch(callout)
    ax.text(10.8, 1.8, 'JAILBREAK DETECTED', fontsize=8, ha='center',
            fontweight='bold', color='#166534')
    ax.text(10.8, 1.48, 'Harmful content generated', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])
    ax.text(10.8, 1.22, 'Attack terminates early', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])
    ax.text(10.8, 0.96, 'ASR counter incremented', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])

    ax.plot([8.15, 9.05], [1.95, 1.5], color=SEMANTIC_COLORS['success'], lw=1.5)
    ax.plot([9.05], [1.5], marker='>', markersize=6, color=SEMANTIC_COLORS['success'])

    # --- LEGEND ---
    legend_y = 0.18
    legend_items = [
        (0.5, SEMANTIC_COLORS['active_light'], SEMANTIC_COLORS['active'], 'Active Branch'),
        (2.8, SEMANTIC_COLORS['promising_light'], SEMANTIC_COLORS['promising'], 'High Score (>=7)'),
        (5.3, SEMANTIC_COLORS['pruned_light'], SEMANTIC_COLORS['pruned'], 'Pruned (score <4)'),
        (7.8, SEMANTIC_COLORS['success'], '#166534', 'Success (ASR+1)'),
    ]

    for x, bg, edge, text in legend_items:
        leg = FancyBboxPatch((x, legend_y), 0.35, 0.3,
                              boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=bg, edgecolor=edge, linewidth=1)
        ax.add_patch(leg)
        ax.text(x + 0.55, legend_y + 0.15, text, fontsize=7, va='center',
                color=SEMANTIC_COLORS['text'])

    plt.tight_layout()
    save_figure(fig, 'fig2_tree')
    plt.close()


# ============================================================================
# FIGURE 3: ATTACK SUCCESS RATES BAR CHART
# ============================================================================

def create_figure3_asr():
    """
    Figure 3: Attack Success Rates by Model
    Single-column width bar chart
    """
    fig, ax = plt.subplots(figsize=(SINGLE_COL_WIDTH, 3.5))

    # Data (from experiments)
    models = ['Gemma3\n12B', 'Kimi-k2\n1T', 'GLM-4.6\n357B', 'Cogito-2.1\n671B',
              'GPT-OSS\n120B', 'Calme-3.2\n78B']
    asr_values = [100.0, 99.0, 98.8, 98.3, 97.5, 96.2]

    # Colors based on ASR threshold
    bar_colors = [SEMANTIC_COLORS['success'] if v >= 99 else
                  SEMANTIC_COLORS['warning'] if v >= 97 else
                  SEMANTIC_COLORS['active'] for v in asr_values]

    bars = ax.bar(range(len(models)), asr_values, color=bar_colors,
                  edgecolor=COLORS['dark_gray'], linewidth=0.5)

    # Add value labels
    for bar, val in zip(bars, asr_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=7, fontweight='bold')

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, fontsize=7)
    ax.set_ylabel('Attack Success Rate (%)', fontsize=8)
    ax.set_ylim(90, 102)
    ax.set_xlim(-0.6, len(models) - 0.4)

    # Add 100% reference line
    ax.axhline(y=100, color=COLORS['gray'], linestyle='--', linewidth=0.8, alpha=0.5)

    # Add Zhou & Arel baseline
    ax.axhline(y=97, color=SEMANTIC_COLORS['attacker'], linestyle=':', linewidth=1, alpha=0.7)
    ax.text(len(models) - 0.5, 97.2, 'Zhou & Arel (2025)\nbaseline: 97%',
            fontsize=6, ha='right', va='bottom', color=SEMANTIC_COLORS['attacker'])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Panel label
    add_panel_label(ax, 'c')

    plt.tight_layout()
    save_figure(fig, 'fig3_asr_bar')
    plt.close()


# ============================================================================
# FIGURE 4: CATEGORY-LEVEL ANALYSIS HEATMAP
# ============================================================================

def create_figure4_heatmap():
    """
    Figure 4: ASR by Harm Category Heatmap
    Double-column width
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 3.0))

    # Categories and models
    categories = ['Violence', 'Fraud', 'Privacy', 'Hate Speech',
                  'Malware', 'Illegal Acts', 'Misinformation']
    models = ['Gemma3', 'Kimi-k2', 'GLM-4.6', 'Cogito-2.1', 'GPT-OSS', 'Calme-3.2']

    # Simulated data (replace with actual)
    np.random.seed(42)
    data = np.random.uniform(94, 100, (len(categories), len(models)))
    data = np.clip(data, 94, 100)

    # Custom colormap (sequential, colorblind-safe)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('asr_cmap',
                                              [COLORS['sky_blue'], SEMANTIC_COLORS['success']])

    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=90, vmax=100)

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, fontsize=7, rotation=45, ha='right')
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, fontsize=7)

    # Add values
    for i in range(len(categories)):
        for j in range(len(models)):
            text_color = 'white' if data[i, j] > 97 else COLORS['dark_gray']
            ax.text(j, i, f'{data[i, j]:.0f}', ha='center', va='center',
                    fontsize=6, color=text_color, fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('ASR (%)', fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # Panel label
    add_panel_label(ax, 'd')

    plt.tight_layout()
    save_figure(fig, 'fig4_heatmap')
    plt.close()


# ============================================================================
# FIGURE 5: TURNS TO JAILBREAK DISTRIBUTION
# ============================================================================

def create_figure5_turns():
    """
    Figure 5: Distribution of Turns to Jailbreak
    Single-column width
    """
    fig, ax = plt.subplots(figsize=(SINGLE_COL_WIDTH, 2.8))

    # Data
    turns = [1, 2, 3, 4, 5]
    percentages = [45, 32, 15, 6, 2]  # Example distribution

    bars = ax.bar(turns, percentages, color=SEMANTIC_COLORS['active'],
                  edgecolor=COLORS['dark_gray'], linewidth=0.5, width=0.7)

    # Highlight first turn
    bars[0].set_color(SEMANTIC_COLORS['success'])

    # Add value labels
    for bar, val in zip(bars, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}%', ha='center', va='bottom', fontsize=7, fontweight='bold')

    ax.set_xlabel('Number of Turns', fontsize=8)
    ax.set_ylabel('Successful Jailbreaks (%)', fontsize=8)
    ax.set_xticks(turns)
    ax.set_ylim(0, 55)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Annotation
    ax.annotate('45% succeed\nin 1 turn', xy=(1, 45), xytext=(2.5, 48),
                fontsize=7, ha='left',
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=0.8))

    # Panel label
    add_panel_label(ax, 'e')

    plt.tight_layout()
    save_figure(fig, 'fig5_turns_dist')
    plt.close()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Generating figures following Nature/Springer guidelines...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    create_figure1_architecture()
    create_figure2_tree()
    create_figure3_asr()
    create_figure4_heatmap()
    create_figure5_turns()

    print("-" * 50)
    print("All figures generated successfully!")
    print("\nKey compliance features:")
    print("  - Font: Arial/Helvetica (sans-serif)")
    print("  - Colors: Colorblind-friendly palette (Wong 2011)")
    print("  - Panel labels: Lowercase bold (a, b, c...)")
    print("  - Resolution: 300 DPI")
    print("  - Formats: PNG, PDF, SVG")
    print("  - Sizes: Single-column (3.54in) / Double-column (7.09in)")
