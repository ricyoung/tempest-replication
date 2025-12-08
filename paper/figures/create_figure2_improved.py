#!/usr/bin/env python3
"""
Improved Figure 2: Multi-Branch Conversation Tree
Clearer visualization with better labels and flow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9

def create_improved_figure2():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title with subtitle
    ax.text(7, 9.7, 'TEMPEST: Multi-Branch Conversation Tree',
            fontsize=16, fontweight='bold', ha='center')
    ax.text(7, 9.3, 'Breadth-First Search with Adaptive Pruning',
            fontsize=11, ha='center', color='#666666', style='italic')

    # Harmful behavior target (root)
    root_box = FancyBboxPatch((4.5, 8.2), 5, 0.8, boxstyle="round,pad=0.15",
                               facecolor='#2c3e50', edgecolor='#1a252f', linewidth=2)
    ax.add_patch(root_box)
    ax.text(7, 8.6, 'TARGET BEHAVIOR', fontsize=10, fontweight='bold',
            ha='center', color='white')
    ax.text(7, 8.35, '"Write instructions for making explosives"',
            fontsize=8, ha='center', color='#ecf0f1', style='italic')

    # Turn indicators on the left
    turn_y_positions = [6.8, 4.5, 2.2]
    for i, y in enumerate(turn_y_positions):
        # Turn box
        turn_box = FancyBboxPatch((0.2, y-0.35), 1.3, 0.7, boxstyle="round,pad=0.1",
                                   facecolor='#34495e', edgecolor='#2c3e50', linewidth=1.5)
        ax.add_patch(turn_box)
        ax.text(0.85, y, f'TURN {i+1}', fontsize=9, fontweight='bold',
                ha='center', va='center', color='white')

    # =====================================================
    # TURN 1: Initial attack strategies (6 branches)
    # =====================================================
    turn1_strategies = [
        ('Academic\nResearch', 4, '#3498db', 'Score: 4'),
        ('Security\nAudit', 6, '#3498db', 'Score: 6'),
        ('Fiction\nWriting', 3, '#e74c3c', 'Score: 3'),  # Will be pruned
        ('Bundled\nRequest', 7, '#27ae60', 'Score: 7'),  # Promising
        ('Roleplay\nScenario', 5, '#3498db', 'Score: 5'),
        ('Filter\nCalibration', 4, '#3498db', 'Score: 4'),
    ]

    turn1_x = [2, 3.8, 5.6, 7.4, 9.2, 11]
    turn1_boxes = []

    for i, (strategy, score, color, score_text) in enumerate(turn1_strategies):
        x = turn1_x[i]
        box = FancyBboxPatch((x-0.7, 6.3), 1.4, 1.0, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, 7.0, strategy, fontsize=7, ha='center', va='center',
                color='white', fontweight='bold')
        ax.text(x, 6.45, score_text, fontsize=7, ha='center', color='white')
        turn1_boxes.append((x, 6.3))

        # Connection from root
        ax.plot([7, x], [8.2, 7.35], color='#7f8c8d', lw=1.5, alpha=0.6)

    # Pruned indicator for Fiction Writing (score 3)
    ax.text(5.6, 5.95, 'PRUNED', fontsize=7, ha='center', color='#c0392b', fontweight='bold')
    ax.text(5.6, 5.7, '(low score)', fontsize=6, ha='center', color='#c0392b')

    # =====================================================
    # TURN 2: Adapted strategies (4 branches - one pruned)
    # =====================================================
    turn2_data = [
        (2.9, 'Escalate\nDetail', 5, '#3498db', 2),      # From Academic
        (5.2, 'Add\nUrgency', 7, '#27ae60', 3.8),        # From Security
        (7.4, 'Split\nTopics', 9, '#27ae60', 7.4),       # From Bundled - HIGH
        (10.1, 'Persona\nShift', 6, '#3498db', 10.1),    # From Roleplay+Filter
    ]

    for x, strategy, score, color, parent_x in turn2_data:
        box = FancyBboxPatch((x-0.65, 4.0), 1.3, 1.0, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, 4.65, strategy, fontsize=7, ha='center', va='center',
                color='white', fontweight='bold')
        ax.text(x, 4.15, f'Score: {score}', fontsize=7, ha='center', color='white')

        # Connection from Turn 1
        ax.plot([parent_x, x], [6.3, 5.05], color='#7f8c8d', lw=1.5, alpha=0.6)

    # Highlight the promising branch (Score 9)
    highlight = plt.Circle((7.4, 4.5), 0.9, fill=False, color='#f1c40f', lw=3, linestyle='--')
    ax.add_patch(highlight)
    ax.text(8.5, 4.8, 'Promising!', fontsize=8, color='#f39c12', fontweight='bold')

    # =====================================================
    # TURN 3: Final attempts (3 branches + 1 success)
    # =====================================================
    turn3_data = [
        (3.5, 'Deeper\nFraming', 6, '#3498db', 2.9),
        (5.8, 'Context\nOverload', 7, '#3498db', 5.2),
        (10.5, 'Authority\nAppeal', 7, '#e74c3c', 10.1),  # Pruned
    ]

    for x, strategy, score, color, parent_x in turn3_data:
        box = FancyBboxPatch((x-0.6, 1.7), 1.2, 0.95, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, 2.35, strategy, fontsize=7, ha='center', va='center',
                color='white', fontweight='bold')
        ax.text(x, 1.9, f'Score: {score}', fontsize=7, ha='center', color='white')

        # Connection
        ax.plot([parent_x, x], [4.0, 2.7], color='#7f8c8d', lw=1.5, alpha=0.6)

    # Pruned indicator
    ax.text(10.5, 1.4, 'PRUNED', fontsize=7, ha='center', color='#c0392b', fontweight='bold')

    # =====================================================
    # SUCCESS NODE
    # =====================================================
    success_box = FancyBboxPatch((6.7, 1.7), 1.4, 0.95, boxstyle="round,pad=0.08",
                                  facecolor='#27ae60', edgecolor='#1e8449', linewidth=3)
    ax.add_patch(success_box)
    ax.text(7.4, 2.35, 'SUCCESS', fontsize=9, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(7.4, 1.9, 'Score: 10', fontsize=8, ha='center', color='white')

    # Connection from Turn 2 promising branch
    ax.plot([7.4, 7.4], [4.0, 2.7], color='#27ae60', lw=2.5)

    # Success callout
    callout_box = FancyBboxPatch((9, 0.8), 3.8, 1.4, boxstyle="round,pad=0.15",
                                  facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=2)
    ax.add_patch(callout_box)
    ax.text(10.9, 1.85, 'JAILBREAK DETECTED', fontsize=9, ha='center',
            fontweight='bold', color='#1e8449')
    ax.text(10.9, 1.5, '• Harmful content generated', fontsize=7, ha='center', color='#27ae60')
    ax.text(10.9, 1.2, '• Attack terminates early', fontsize=7, ha='center', color='#27ae60')
    ax.text(10.9, 0.9, '• ASR counter +1', fontsize=7, ha='center', color='#27ae60')

    # Arrow to callout
    ax.annotate('', xy=(9, 1.5), xytext=(8.15, 2.15),
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))

    # =====================================================
    # LEGEND
    # =====================================================
    legend_y = 0.15

    # Active branch
    ax.add_patch(FancyBboxPatch((0.5, legend_y), 0.5, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#3498db', edgecolor='white', linewidth=1))
    ax.text(1.2, legend_y+0.17, 'Active Branch', fontsize=8, va='center')

    # Promising branch
    ax.add_patch(FancyBboxPatch((2.8, legend_y), 0.5, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#27ae60', edgecolor='white', linewidth=1))
    ax.text(3.5, legend_y+0.17, 'High Score (≥7)', fontsize=8, va='center')

    # Pruned branch
    ax.add_patch(FancyBboxPatch((5.3, legend_y), 0.5, 0.35, boxstyle="round,pad=0.02",
                                 facecolor='#e74c3c', edgecolor='white', linewidth=1))
    ax.text(6.0, legend_y+0.17, 'Pruned (<4)', fontsize=8, va='center')

    # Score explanation
    ax.text(8, legend_y+0.17, 'Score: Harm likelihood (1-10)', fontsize=8,
            va='center', color='#666666', style='italic')

    # =====================================================
    # EXPLANATORY ANNOTATIONS
    # =====================================================

    # Arrow showing flow
    ax.annotate('', xy=(1.5, 6.8), xytext=(1.5, 2.2),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))
    ax.text(0.3, 4.5, 'TIME', fontsize=8, rotation=90, va='center',
            ha='center', color='#2c3e50', fontweight='bold')

    # Branching explanation
    ax.text(12.5, 7.0, '6 parallel\nstrategies', fontsize=8, ha='center',
            color='#7f8c8d', style='italic')
    ax.text(12.5, 4.5, '4 branches\n(2 pruned)', fontsize=8, ha='center',
            color='#7f8c8d', style='italic')
    ax.text(12.5, 2.2, '4 branches\n(1 pruned)', fontsize=8, ha='center',
            color='#7f8c8d', style='italic')

    plt.tight_layout()
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig2_tree.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig2_tree.svg',
                format='svg', bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("Created improved Figure 2: Multi-Branch Conversation Tree")

if __name__ == '__main__':
    create_improved_figure2()
