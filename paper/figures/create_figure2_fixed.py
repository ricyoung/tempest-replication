#!/usr/bin/env python3
"""
Figure 2: Multi-Branch Conversation Tree - Fixed arrows
Professional design with clear flow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Arrow
import matplotlib.patheffects as path_effects
import numpy as np

# Professional color palette
COLORS = {
    'root': '#2C3E50',
    'active': '#3498DB',
    'active_light': '#E3F2FD',
    'promising': '#27AE60',
    'promising_light': '#E8F5E9',
    'pruned': '#E74C3C',
    'pruned_light': '#FFEBEE',
    'success': '#27AE60',
    'text': '#1D3557',
    'arrow': '#7F8C8D',
    'turn_bg': '#34495E',
}

def create_fixed_figure2():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Title
    ax.text(7, 8.7, 'Multi-Branch Conversation Tree',
            fontsize=16, fontweight='bold', ha='center', color=COLORS['text'])
    ax.text(7, 8.35, 'Breadth-First Search with Adaptive Pruning',
            fontsize=10, ha='center', color='#666666', style='italic')

    # =========================================
    # ROOT NODE - Target Behavior
    # =========================================
    root_box = FancyBboxPatch((4.5, 7.4), 5, 0.7,
                               boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor=COLORS['root'], edgecolor='#1A252F', linewidth=2)
    ax.add_patch(root_box)
    ax.text(7, 7.85, 'TARGET BEHAVIOR', fontsize=10, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(7, 7.55, '"Generate harmful content about X"', fontsize=8,
            ha='center', va='center', color='#BDC3C7', style='italic')

    # =========================================
    # TURN LABELS (Left side)
    # =========================================
    turn_labels = ['TURN 1', 'TURN 2', 'TURN 3']
    turn_y = [6.0, 4.0, 2.0]

    for label, y in zip(turn_labels, turn_y):
        turn_box = FancyBboxPatch((0.3, y - 0.25), 1.2, 0.5,
                                   boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=COLORS['turn_bg'], edgecolor='none')
        ax.add_patch(turn_box)
        ax.text(0.9, y, label, fontsize=8, fontweight='bold',
                ha='center', va='center', color='white')

    # =========================================
    # TURN 1 - Initial Strategies (6 branches)
    # =========================================
    turn1_data = [
        ('Academic\nFraming', 4, COLORS['active'], COLORS['active_light']),
        ('Security\nAudit', 6, COLORS['active'], COLORS['active_light']),
        ('Fiction\nWriting', 3, COLORS['pruned'], COLORS['pruned_light']),
        ('Bundled\nRequest', 7, COLORS['promising'], COLORS['promising_light']),
        ('Roleplay', 5, COLORS['active'], COLORS['active_light']),
        ('Filter\nCalibration', 4, COLORS['active'], COLORS['active_light']),
    ]

    turn1_x = [2.0, 3.8, 5.6, 7.4, 9.2, 11.0]
    turn1_centers = []

    for i, ((label, score, color, bg_color), x) in enumerate(zip(turn1_data, turn1_x)):
        # Node box
        node = FancyBboxPatch((x - 0.65, 5.5), 1.3, 1.0,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=bg_color, edgecolor=color, linewidth=2)
        ax.add_patch(node)

        # Label
        ax.text(x, 6.2, label, fontsize=7, ha='center', va='center',
                color=color, fontweight='bold')

        # Score
        ax.text(x, 5.7, f'Score: {score}', fontsize=7, ha='center', va='center',
                color='#666666')

        turn1_centers.append((x, 5.5))

        # Arrow from root to node - USING SIMPLE LINES
        ax.plot([7, x], [7.4, 6.55], color=COLORS['arrow'], lw=1.5, alpha=0.6)
        # Arrowhead
        ax.plot([x], [6.55], marker='v', markersize=6, color=COLORS['arrow'], alpha=0.6)

    # Pruned label for Fiction Writing
    ax.text(5.6, 5.2, 'PRUNED', fontsize=7, ha='center', color=COLORS['pruned'],
            fontweight='bold')

    # =========================================
    # TURN 2 - Adapted (4 branches, 2 pruned)
    # =========================================
    turn2_data = [
        ('Escalate\nDetail', 5, COLORS['active'], COLORS['active_light'], 2.0),
        ('Add\nUrgency', 7, COLORS['promising'], COLORS['promising_light'], 3.8),
        ('Split\nTopics', 9, COLORS['promising'], COLORS['promising_light'], 7.4),
        ('Persona\nShift', 6, COLORS['active'], COLORS['active_light'], 10.1),
    ]

    turn2_x = [2.9, 5.0, 7.4, 10.1]
    turn2_centers = []

    for (label, score, color, bg_color, parent_x), x in zip(turn2_data, turn2_x):
        node = FancyBboxPatch((x - 0.6, 3.5), 1.2, 1.0,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=bg_color, edgecolor=color, linewidth=2)
        ax.add_patch(node)

        ax.text(x, 4.2, label, fontsize=7, ha='center', va='center',
                color=color, fontweight='bold')
        ax.text(x, 3.7, f'Score: {score}', fontsize=7, ha='center', va='center',
                color='#666666')

        turn2_centers.append((x, 3.5))

        # Arrow from parent - SIMPLE LINES
        ax.plot([parent_x, x], [5.5, 4.55], color=COLORS['arrow'], lw=1.5, alpha=0.6)
        ax.plot([x], [4.55], marker='v', markersize=6, color=COLORS['arrow'], alpha=0.6)

    # Highlight promising branch (Score 9)
    highlight = plt.Circle((7.4, 4.0), 0.85, fill=False, color='#F1C40F',
                           lw=3, linestyle='--')
    ax.add_patch(highlight)
    ax.text(8.5, 4.3, 'Promising!', fontsize=8, color='#F39C12', fontweight='bold')

    # =========================================
    # TURN 3 - Final (3 active + 1 success)
    # =========================================
    turn3_data = [
        ('Deeper\nFraming', 6, COLORS['active'], COLORS['active_light'], 2.9),
        ('Context\nOverload', 7, COLORS['active'], COLORS['active_light'], 5.0),
        ('Authority\nAppeal', 5, COLORS['pruned'], COLORS['pruned_light'], 10.1),
    ]

    turn3_x = [3.2, 5.5, 10.1]

    for (label, score, color, bg_color, parent_x), x in zip(turn3_data, turn3_x):
        node = FancyBboxPatch((x - 0.55, 1.5), 1.1, 0.9,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=bg_color, edgecolor=color, linewidth=2)
        ax.add_patch(node)

        ax.text(x, 2.15, label, fontsize=7, ha='center', va='center',
                color=color, fontweight='bold')
        ax.text(x, 1.7, f'Score: {score}', fontsize=7, ha='center', va='center',
                color='#666666')

        # Arrow from parent
        ax.plot([parent_x, x], [3.5, 2.45], color=COLORS['arrow'], lw=1.5, alpha=0.6)
        ax.plot([x], [2.45], marker='v', markersize=6, color=COLORS['arrow'], alpha=0.6)

    # Pruned label
    ax.text(10.1, 1.2, 'PRUNED', fontsize=7, ha='center', color=COLORS['pruned'],
            fontweight='bold')

    # =========================================
    # SUCCESS NODE
    # =========================================
    success_box = FancyBboxPatch((6.85, 1.5), 1.3, 0.9,
                                  boxstyle="round,pad=0.05,rounding_size=0.1",
                                  facecolor=COLORS['success'], edgecolor='#1E8449', linewidth=3)
    ax.add_patch(success_box)
    ax.text(7.5, 2.1, 'SUCCESS', fontsize=9, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(7.5, 1.7, 'Score: 10', fontsize=8, ha='center', va='center',
            color='white')

    # Arrow from Split Topics to Success
    ax.plot([7.4, 7.5], [3.5, 2.45], color=COLORS['success'], lw=2.5)
    ax.plot([7.5], [2.45], marker='v', markersize=8, color=COLORS['success'])

    # =========================================
    # SUCCESS CALLOUT
    # =========================================
    callout = FancyBboxPatch((9.2, 0.6), 3.5, 1.5,
                              boxstyle="round,pad=0.1,rounding_size=0.15",
                              facecolor='#E8F5E9', edgecolor=COLORS['success'], linewidth=2)
    ax.add_patch(callout)
    ax.text(10.95, 1.85, 'JAILBREAK DETECTED', fontsize=9, ha='center',
            fontweight='bold', color='#1E8449')
    ax.text(10.95, 1.5, '• Harmful content generated', fontsize=7, ha='center', color=COLORS['success'])
    ax.text(10.95, 1.2, '• Attack terminates early', fontsize=7, ha='center', color=COLORS['success'])
    ax.text(10.95, 0.9, '• ASR counter incremented', fontsize=7, ha='center', color=COLORS['success'])

    # Arrow to callout
    ax.plot([8.2, 9.15], [1.95, 1.5], color=COLORS['success'], lw=2)
    ax.plot([9.15], [1.5], marker='>', markersize=8, color=COLORS['success'])

    # =========================================
    # LEGEND
    # =========================================
    legend_y = 0.15

    # Active
    leg1 = FancyBboxPatch((0.5, legend_y), 0.4, 0.35,
                           boxstyle="round,pad=0.02,rounding_size=0.08",
                           facecolor=COLORS['active_light'], edgecolor=COLORS['active'], linewidth=1.5)
    ax.add_patch(leg1)
    ax.text(1.1, legend_y + 0.17, 'Active Branch', fontsize=8, va='center', color=COLORS['text'])

    # Promising
    leg2 = FancyBboxPatch((2.8, legend_y), 0.4, 0.35,
                           boxstyle="round,pad=0.02,rounding_size=0.08",
                           facecolor=COLORS['promising_light'], edgecolor=COLORS['promising'], linewidth=1.5)
    ax.add_patch(leg2)
    ax.text(3.4, legend_y + 0.17, 'High Score (≥7)', fontsize=8, va='center', color=COLORS['text'])

    # Pruned
    leg3 = FancyBboxPatch((5.3, legend_y), 0.4, 0.35,
                           boxstyle="round,pad=0.02,rounding_size=0.08",
                           facecolor=COLORS['pruned_light'], edgecolor=COLORS['pruned'], linewidth=1.5)
    ax.add_patch(leg3)
    ax.text(5.9, legend_y + 0.17, 'Pruned (score <4)', fontsize=8, va='center', color=COLORS['text'])

    # Success
    leg4 = FancyBboxPatch((7.5, legend_y), 0.4, 0.35,
                           boxstyle="round,pad=0.02,rounding_size=0.08",
                           facecolor=COLORS['success'], edgecolor='#1E8449', linewidth=1.5)
    ax.add_patch(leg4)
    ax.text(8.1, legend_y + 0.17, 'Success (ASR+1)', fontsize=8, va='center', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig2_tree.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig2_tree.svg',
                format='svg', bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("Created fixed Figure 2: Multi-Branch Tree (with proper arrows)")

if __name__ == '__main__':
    create_fixed_figure2()
