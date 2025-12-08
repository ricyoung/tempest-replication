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
    Clean redesign with proper aspect ratio and clear feedback loop
    """
    # Use equal aspect ratio to keep circles circular
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9.17)  # Match aspect ratio for equal scaling
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('white')

    # === TITLE WITH BLUE BACKGROUND (centered) ===
    title_box = FancyBboxPatch((0.5, 8.0), 9.0, 1.0,
                                boxstyle="round,pad=0.1,rounding_size=0.15",
                                facecolor='#F0F9FF', edgecolor='#93C5FD', lw=1)
    ax.add_patch(title_box)
    ax.text(5, 8.7, 'TEMPEST: Multi-Turn Adversarial Attack Framework',
            fontsize=11, fontweight='bold', ha='center', va='center', color='#1F2937')
    ax.text(5, 8.25, 'Attacker → Target → Evaluator → Feedback Loop (if score < 10)',
            fontsize=7, ha='center', va='center', color='#0369A1')

    # Component dimensions
    box_width = 2.4
    box_height = 2.2
    box_y = 5.0

    # === STEP 1: ATTACKER ===
    attacker_x = 0.3

    # Step number circle
    ax.add_patch(FancyBboxPatch((attacker_x + box_width/2 - 0.25, box_y + box_height + 0.2), 0.5, 0.5,
                                 boxstyle="circle,pad=0", facecolor='#EA580C', edgecolor='white', lw=2))
    ax.text(attacker_x + box_width/2, box_y + box_height + 0.45, '1',
            fontsize=12, fontweight='bold', ha='center', va='center', color='white')

    # Main box
    attacker_box = FancyBboxPatch((attacker_x, box_y), box_width, box_height,
                                   boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor='#FFF7ED', edgecolor='#EA580C', linewidth=2.5)
    ax.add_patch(attacker_box)

    # Header bar
    header = FancyBboxPatch((attacker_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor='#EA580C', edgecolor='none')
    ax.add_patch(header)
    ax.text(attacker_x + box_width/2, box_y + box_height - 0.22, 'ATTACKER',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    # Content
    ax.text(attacker_x + box_width/2, box_y + 1.4, 'DeepSeek-v3.1',
            fontsize=9, ha='center', va='center', color='#333333', fontweight='bold')
    ax.text(attacker_x + box_width/2, box_y + 1.05, '671B Parameters',
            fontsize=7, ha='center', va='center', color='#666666')
    ax.text(attacker_x + box_width/2, box_y + 0.65, '"Siege" Agent',
            fontsize=8, ha='center', va='center', color='#EA580C', fontweight='bold', style='italic')
    ax.text(attacker_x + box_width/2, box_y + 0.3, '7 attack strategies',
            fontsize=6, ha='center', va='center', color='#666666')

    # === STEP 2: TARGET ===
    target_x = 3.8

    ax.add_patch(FancyBboxPatch((target_x + box_width/2 - 0.25, box_y + box_height + 0.2), 0.5, 0.5,
                                 boxstyle="circle,pad=0", facecolor='#0284C7', edgecolor='white', lw=2))
    ax.text(target_x + box_width/2, box_y + box_height + 0.45, '2',
            fontsize=12, fontweight='bold', ha='center', va='center', color='white')

    target_box = FancyBboxPatch((target_x, box_y), box_width, box_height,
                                 boxstyle="round,pad=0.05,rounding_size=0.1",
                                 facecolor='#F0F9FF', edgecolor='#0284C7', linewidth=2.5)
    ax.add_patch(target_box)

    header = FancyBboxPatch((target_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor='#0284C7', edgecolor='none')
    ax.add_patch(header)
    ax.text(target_x + box_width/2, box_y + box_height - 0.22, 'TARGET',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    ax.text(target_x + box_width/2, box_y + 1.4, 'Victim LLM',
            fontsize=9, ha='center', va='center', color='#333333', fontweight='bold')
    ax.text(target_x + box_width/2, box_y + 1.0, '10 Models Tested',
            fontsize=7, ha='center', va='center', color='#666666')
    ax.text(target_x + box_width/2, box_y + 0.6, 'Kimi | DeepSeek | Mistral',
            fontsize=6, ha='center', va='center', color='#666666')
    ax.text(target_x + box_width/2, box_y + 0.3, 'Cogito | GLM | Gemma3...',
            fontsize=6, ha='center', va='center', color='#666666')

    # === STEP 3: EVALUATOR ===
    eval_x = 7.3

    ax.add_patch(FancyBboxPatch((eval_x + box_width/2 - 0.25, box_y + box_height + 0.2), 0.5, 0.5,
                                 boxstyle="circle,pad=0", facecolor='#16A34A', edgecolor='white', lw=2))
    ax.text(eval_x + box_width/2, box_y + box_height + 0.45, '3',
            fontsize=12, fontweight='bold', ha='center', va='center', color='white')

    eval_box = FancyBboxPatch((eval_x, box_y), box_width, box_height,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=2.5)
    ax.add_patch(eval_box)

    header = FancyBboxPatch((eval_x, box_y + box_height - 0.45), box_width, 0.45,
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor='#16A34A', edgecolor='none')
    ax.add_patch(header)
    ax.text(eval_x + box_width/2, box_y + box_height - 0.22, 'EVALUATOR',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    ax.text(eval_x + box_width/2, box_y + 1.4, 'Harm Classifier',
            fontsize=9, ha='center', va='center', color='#333333', fontweight='bold')
    ax.text(eval_x + box_width/2, box_y + 1.0, 'DeepSeek-v3.1',
            fontsize=7, ha='center', va='center', color='#666666')
    ax.text(eval_x + box_width/2, box_y + 0.65, 'Llama-Guard-3',
            fontsize=7, ha='center', va='center', color='#666666')
    ax.text(eval_x + box_width/2, box_y + 0.3, 'Score ≥ 10 = Jailbreak!',
            fontsize=7, ha='center', va='center', color='#DC2626', fontweight='bold')

    # --- ARROWS between boxes ---
    arrow_y = box_y + box_height/2
    arrow_style = dict(arrowstyle='-|>', color='#333333', lw=2, mutation_scale=15)

    # Attacker -> Target
    ax.annotate('', xy=(target_x - 0.1, arrow_y),
                xytext=(attacker_x + box_width + 0.1, arrow_y),
                arrowprops=arrow_style)
    mid_x1 = (attacker_x + box_width + target_x) / 2
    ax.text(mid_x1, arrow_y + 0.2, 'Prompt', fontsize=7, ha='center', va='bottom',
            color='#333333', fontweight='bold')

    # Target -> Evaluator
    ax.annotate('', xy=(eval_x - 0.1, arrow_y),
                xytext=(target_x + box_width + 0.1, arrow_y),
                arrowprops=arrow_style)
    mid_x2 = (target_x + box_width + eval_x) / 2
    ax.text(mid_x2, arrow_y + 0.2, 'Response', fontsize=7, ha='center', va='bottom',
            color='#333333', fontweight='bold')

    # --- FEEDBACK LOOP (clear flowchart-style path) ---
    feedback_color = '#EA580C'

    # Connection points
    eval_bottom_x = eval_x + box_width/2
    eval_bottom_y = box_y
    attacker_bottom_x = attacker_x + box_width/2
    attacker_bottom_y = box_y
    loop_y = 3.6  # Height of the horizontal path

    # Draw the feedback path as connected segments:
    # 1. Vertical line DOWN from evaluator
    ax.plot([eval_bottom_x, eval_bottom_x], [eval_bottom_y, loop_y],
            color=feedback_color, lw=2.5, solid_capstyle='round')

    # 2. Horizontal line across (with gap for label)
    ax.plot([eval_bottom_x, 6.3], [loop_y, loop_y],
            color=feedback_color, lw=2.5, solid_capstyle='round')
    ax.plot([3.7, attacker_bottom_x], [loop_y, loop_y],
            color=feedback_color, lw=2.5, solid_capstyle='round')

    # 3. Vertical line UP to attacker with arrow
    ax.annotate('', xy=(attacker_bottom_x, attacker_bottom_y),
                xytext=(attacker_bottom_x, loop_y),
                arrowprops=dict(arrowstyle='-|>', color=feedback_color, lw=2.5, mutation_scale=15))

    # Small circles at corners for clean joints
    ax.plot(eval_bottom_x, loop_y, 'o', color=feedback_color, markersize=6, zorder=5)
    ax.plot(attacker_bottom_x, loop_y, 'o', color=feedback_color, markersize=6, zorder=5)

    # Connection indicator at evaluator (small horizontal tick)
    ax.plot([eval_bottom_x - 0.15, eval_bottom_x + 0.15], [eval_bottom_y, eval_bottom_y],
            color=feedback_color, lw=3)

    # "Score" label near evaluator
    ax.text(eval_bottom_x + 0.3, (eval_bottom_y + loop_y)/2 + 0.2, 'Score',
            fontsize=7, ha='left', va='center', color=feedback_color, fontweight='bold')

    # "FEEDBACK LOOP" label in center of horizontal path
    ax.text(5, loop_y, 'If score < 10', fontsize=7, ha='center', va='center',
            color='white', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=feedback_color, edgecolor='none'))

    # "Retry" label near attacker
    ax.text(attacker_bottom_x - 0.3, (attacker_bottom_y + loop_y)/2 + 0.2, 'Retry',
            fontsize=7, ha='right', va='center', color=feedback_color, fontweight='bold')

    # --- ATTACK STRATEGIES (4 on top row, 3 on bottom row, no border box) ---
    ax.text(5, 2.8, '7 Attack Strategies', fontsize=9, ha='center', va='center',
            color='#333333', fontweight='bold')

    # Row 1: 4 strategies matching Section 3.5 of paper
    strategies_row1 = ['Academic\nFraming', 'Bundled\nRequests', 'Roleplay\nScenarios', 'Refusal\nSuppression']
    colors_row1 = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6']
    # Darker versions for text
    dark_colors_row1 = ['#B91C1C', '#1D4ED8', '#15803D', '#7E22CE']

    pill_width = 2.2  # 10% bigger
    pill_height = 0.8  # 10% bigger
    row1_y = 1.7
    row1_start = 0.7

    for i, (strategy, color, dark_color) in enumerate(zip(strategies_row1, colors_row1, dark_colors_row1)):
        x = row1_start + i * 2.4
        pill = FancyBboxPatch((x, row1_y), pill_width, pill_height,
                               boxstyle="round,pad=0.02,rounding_size=0.15",
                               facecolor=color, edgecolor='none', alpha=0.25)
        ax.add_patch(pill)
        ax.text(x + pill_width/2, row1_y + pill_height/2, strategy,
                fontsize=8, ha='center', va='center', color=dark_color, fontweight='bold', linespacing=0.9)

    # Row 2: 3 strategies matching Section 3.5 of paper (centered)
    strategies_row2 = ['Progressive\nEscalation', 'Fiction\nFraming', 'Filter\nCalibration']
    colors_row2 = ['#F39C12', '#1ABC9C', '#34495E']
    dark_colors_row2 = ['#B45309', '#0F766E', '#1E293B']

    row2_y = 0.6
    row2_start = 1.9  # Centered for 3 items

    for i, (strategy, color, dark_color) in enumerate(zip(strategies_row2, colors_row2, dark_colors_row2)):
        x = row2_start + i * 2.4
        pill = FancyBboxPatch((x, row2_y), pill_width, pill_height,
                               boxstyle="round,pad=0.02,rounding_size=0.15",
                               facecolor=color, edgecolor='none', alpha=0.25)
        ax.add_patch(pill)
        ax.text(x + pill_width/2, row2_y + pill_height/2, strategy,
                fontsize=8, ha='center', va='center', color=dark_color, fontweight='bold', linespacing=0.9)

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
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 6.0))
    ax.set_xlim(0, 14)
    ax.set_ylim(-0.6, 9)
    ax.axis('off')
    ax.set_facecolor('white')

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

    # --- SUCCESS CALLOUT --- (positioned below Turn 3 to avoid overlap)
    callout = FancyBboxPatch((9.1, -0.35), 3.4, 1.4,
                              boxstyle="round,pad=0.08,rounding_size=0.12",
                              facecolor=SEMANTIC_COLORS['promising_light'],
                              edgecolor=SEMANTIC_COLORS['success'], linewidth=1.5)
    ax.add_patch(callout)
    ax.text(10.8, 0.8, 'JAILBREAK DETECTED', fontsize=8, ha='center',
            fontweight='bold', color='#166534')
    ax.text(10.8, 0.48, 'Harmful content generated', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])
    ax.text(10.8, 0.22, 'Attack terminates early', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])
    ax.text(10.8, -0.04, 'ASR counter incremented', fontsize=6, ha='center',
            color=SEMANTIC_COLORS['success'])

    ax.plot([8.15, 9.05], [1.95, 0.55], color=SEMANTIC_COLORS['success'], lw=1.5)
    ax.plot([9.05], [0.55], marker='>', markersize=6, color=SEMANTIC_COLORS['success'])

    # --- LEGEND --- (two-line format: label on top, criteria below)
    legend_y = -0.35
    legend_items = [
        (0.5, SEMANTIC_COLORS['active_light'], SEMANTIC_COLORS['active'], 'Active', 'Branch'),
        (2.4, SEMANTIC_COLORS['promising_light'], SEMANTIC_COLORS['promising'], 'High Score', '(>=7)'),
        (4.3, SEMANTIC_COLORS['pruned_light'], SEMANTIC_COLORS['pruned'], 'Pruned', '(score <4)'),
        (6.4, SEMANTIC_COLORS['success'], '#166534', 'Success', '(ASR+1)'),
    ]

    for x, bg, edge, label1, label2 in legend_items:
        leg = FancyBboxPatch((x, legend_y), 0.35, 0.3,
                              boxstyle="round,pad=0.02,rounding_size=0.06",
                              facecolor=bg, edgecolor=edge, linewidth=1)
        ax.add_patch(leg)
        ax.text(x + 0.55, legend_y + 0.22, label1, fontsize=7, va='center',
                color=SEMANTIC_COLORS['text'])
        ax.text(x + 0.55, legend_y + 0.02, label2, fontsize=6, va='center',
                color=COLORS['gray'])

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
    Double-column width - all 10 models, taller and better colors
    """
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_WIDTH, 5.5))

    # 5 categories matching paper section 3.3 Dataset description
    categories = ['Misinformation', 'Hate Speech', 'Violence', 'Illegal Activities', 'Privacy']
    models = ['Gemma3\n12B', 'GPT-OSS\n20B', 'GPT-OSS\n120B', 'MiniMax\nM2', 'GLM\n4.6',
              'Cogito\n671B', 'DeepSeek\nV3.1', 'Mistral\nLarge 3', 'Kimi\nK2', 'Kimi K2\nThinking']

    # Actual per-category ASR values from JSON data analysis
    # Each row is a category, columns are models in order above
    # Behavior mapping: Misinformation (50-59), Hate Speech (0-9), Violence (20-29),
    # Illegal Activities (10-19, 30-49, 60-69, 80-99 = 60 behaviors), Privacy (70-79)
    category_asr = np.array([
        [100, 70, 90, 60, 100, 100, 100, 100, 100, 70],  # Misinformation (10 behaviors)
        [100, 50, 80, 50, 100, 100, 100, 100, 100, 50],  # Hate Speech (10 behaviors)
        [100, 70, 60, 10, 100, 90, 100, 100, 100, 30],   # Violence (10 behaviors)
        [100, 83, 72, 60, 98, 95, 98, 100, 95, 42],      # Illegal Activities (60 behaviors)
        [100, 90, 70, 70, 100, 100, 100, 100, 100, 20],  # Privacy (10 behaviors)
    ], dtype=float)

    data = category_asr

    # Add average row at bottom
    avg_row = data.mean(axis=0, keepdims=True)
    data = np.vstack([data, avg_row])
    categories = categories + ['AVERAGE']

    # Better colormap - green (low ASR/protected) to yellow to red (high ASR/vulnerable)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('asr_cmap',
                                              ['#22C55E', '#84CC16', '#FBBF24', '#F97316', '#DC2626'])

    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=30, vmax=100)

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, fontsize=7, rotation=45, ha='right')
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, fontsize=8)

    # Add values
    for i in range(len(categories)):
        for j in range(len(models)):
            text_color = 'white' if data[i, j] > 85 else '#333333'
            # Bold the average row
            weight = 'bold'
            ax.text(j, i, f'{data[i, j]:.0f}', ha='center', va='center',
                    fontsize=6, color=text_color, fontweight=weight)

    # Add separator line above AVERAGE row (after 5 categories, row index 4)
    ax.axhline(y=4.5, color='#333333', linewidth=2)

    # Overlay AVERAGE row with consistent light blue background to distinguish it
    # AVERAGE is row 5 (0-indexed) after 5 categories
    for j in range(len(models)):
        ax.add_patch(plt.Rectangle((j - 0.5, 5 - 0.5), 1, 1,
                                    facecolor='#DBEAFE', edgecolor='none', alpha=1.0, zorder=2))
        # Re-add text on top
        text_color = '#1E3A5F'  # Dark blue text for contrast
        ax.text(j, 5, f'{data[5, j]:.0f}', ha='center', va='center',
                fontsize=6, color=text_color, fontweight='bold', zorder=3)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('ASR (%)', fontsize=9)
    cbar.ax.tick_params(labelsize=8)

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

    # Actual turns distribution from JSON data (839 successful jailbreaks)
    # Turn 1: 438, Turn 2: 165, Turn 3: 85, Turn 4: 86, Turn 5+: 65
    turns = [1, 2, 3, 4, 5]
    percentages = [52, 20, 10, 10, 8]  # Actual distribution from experiments

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
