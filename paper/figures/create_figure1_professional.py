#!/usr/bin/env python3
"""
Professional Figure 1: TEMPEST System Architecture
Clean, modern design suitable for academic publication
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as path_effects
import numpy as np

# Professional color palette (based on academic paper standards)
COLORS = {
    'attacker': '#E63946',      # Red - danger/attack
    'attacker_light': '#FFCDD2',
    'target': '#457B9D',        # Blue - neutral/victim
    'target_light': '#E3F2FD',
    'evaluator': '#2A9D8F',     # Teal - judgment
    'evaluator_light': '#E0F2F1',
    'arrow': '#264653',         # Dark blue-gray
    'text': '#1D3557',          # Dark blue
    'bg': '#FAFAFA',            # Light gray background
    'accent': '#F4A261',        # Orange accent
    'success': '#4CAF50',       # Green
    'feedback': '#9E9E9E',      # Gray for feedback
}

def create_professional_figure1():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Title
    title = ax.text(6, 6.6, 'TEMPEST System Architecture',
                    fontsize=16, fontweight='bold', ha='center', va='top',
                    color=COLORS['text'], fontfamily='sans-serif')

    # Subtitle
    ax.text(6, 6.25, 'Multi-Turn Adversarial Attack Framework',
            fontsize=10, ha='center', va='top', color='#666666',
            fontfamily='sans-serif', style='italic')

    # =========================================
    # MAIN COMPONENTS
    # =========================================

    # Component dimensions
    box_width = 2.8
    box_height = 2.0
    box_y = 3.2

    # --- ATTACKER MODEL ---
    attacker_x = 0.8

    # Main box with shadow effect
    shadow = FancyBboxPatch((attacker_x + 0.05, box_y - 0.05), box_width, box_height,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor='#00000015', edgecolor='none')
    ax.add_patch(shadow)

    attacker_box = FancyBboxPatch((attacker_x, box_y), box_width, box_height,
                                   boxstyle="round,pad=0.08,rounding_size=0.15",
                                   facecolor=COLORS['attacker_light'],
                                   edgecolor=COLORS['attacker'], linewidth=2.5)
    ax.add_patch(attacker_box)

    # Header bar
    header = FancyBboxPatch((attacker_x, box_y + box_height - 0.5), box_width, 0.5,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor=COLORS['attacker'], edgecolor='none')
    ax.add_patch(header)
    ax.text(attacker_x + box_width/2, box_y + box_height - 0.25, 'ATTACKER',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    # Content
    ax.text(attacker_x + box_width/2, box_y + 1.15, 'DeepSeek-v3.1',
            fontsize=9, ha='center', va='center', color=COLORS['text'], fontweight='bold')
    ax.text(attacker_x + box_width/2, box_y + 0.85, '671B Parameters',
            fontsize=8, ha='center', va='center', color='#666666')

    # Siege label
    ax.text(attacker_x + box_width/2, box_y + 0.4, '"Siege" Agent',
            fontsize=8, ha='center', va='center', color=COLORS['attacker'],
            fontweight='bold', style='italic')

    # --- TARGET MODEL ---
    target_x = 4.6

    shadow = FancyBboxPatch((target_x + 0.05, box_y - 0.05), box_width, box_height,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor='#00000015', edgecolor='none')
    ax.add_patch(shadow)

    target_box = FancyBboxPatch((target_x, box_y), box_width, box_height,
                                 boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor=COLORS['target_light'],
                                 edgecolor=COLORS['target'], linewidth=2.5)
    ax.add_patch(target_box)

    header = FancyBboxPatch((target_x, box_y + box_height - 0.5), box_width, 0.5,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor=COLORS['target'], edgecolor='none')
    ax.add_patch(header)
    ax.text(target_x + box_width/2, box_y + box_height - 0.25, 'TARGET',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    ax.text(target_x + box_width/2, box_y + 1.15, 'Victim LLM',
            fontsize=9, ha='center', va='center', color=COLORS['text'], fontweight='bold')

    # Model examples
    models_text = 'Kimi-k2 (1T) | GLM-4.6\nCogito-2.1 | Gemma3'
    ax.text(target_x + box_width/2, box_y + 0.6, models_text,
            fontsize=7, ha='center', va='center', color='#666666',
            linespacing=1.3)

    # --- EVALUATOR ---
    eval_x = 8.4

    shadow = FancyBboxPatch((eval_x + 0.05, box_y - 0.05), box_width, box_height,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor='#00000015', edgecolor='none')
    ax.add_patch(shadow)

    eval_box = FancyBboxPatch((eval_x, box_y), box_width, box_height,
                               boxstyle="round,pad=0.08,rounding_size=0.15",
                               facecolor=COLORS['evaluator_light'],
                               edgecolor=COLORS['evaluator'], linewidth=2.5)
    ax.add_patch(eval_box)

    header = FancyBboxPatch((eval_x, box_y + box_height - 0.5), box_width, 0.5,
                             boxstyle="round,pad=0.08,rounding_size=0.15",
                             facecolor=COLORS['evaluator'], edgecolor='none')
    ax.add_patch(header)
    ax.text(eval_x + box_width/2, box_y + box_height - 0.25, 'EVALUATOR',
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')

    ax.text(eval_x + box_width/2, box_y + 1.15, 'Harm Classifier',
            fontsize=9, ha='center', va='center', color=COLORS['text'], fontweight='bold')
    ax.text(eval_x + box_width/2, box_y + 0.75, 'Primary: DeepSeek-v3.1',
            fontsize=7, ha='center', va='center', color='#666666')
    ax.text(eval_x + box_width/2, box_y + 0.5, 'Secondary: Llama-Guard-3',
            fontsize=7, ha='center', va='center', color='#666666')

    # =========================================
    # ARROWS AND FLOW
    # =========================================

    arrow_style = dict(arrowstyle='->', color=COLORS['arrow'],
                       lw=2, mutation_scale=15,
                       connectionstyle='arc3,rad=0')

    # Attacker -> Target
    ax.annotate('', xy=(target_x - 0.1, box_y + box_height/2),
                xytext=(attacker_x + box_width + 0.1, box_y + box_height/2),
                arrowprops=arrow_style)

    # Label above arrow
    label_box = FancyBboxPatch((3.45, 4.5), 1.3, 0.4,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='white', edgecolor=COLORS['arrow'], linewidth=1)
    ax.add_patch(label_box)
    ax.text(4.1, 4.7, 'Attack\nPrompt', fontsize=7, ha='center', va='center',
            color=COLORS['text'], fontweight='bold')

    # Target -> Evaluator
    ax.annotate('', xy=(eval_x - 0.1, box_y + box_height/2),
                xytext=(target_x + box_width + 0.1, box_y + box_height/2),
                arrowprops=arrow_style)

    label_box = FancyBboxPatch((7.2, 4.5), 1.3, 0.4,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='white', edgecolor=COLORS['arrow'], linewidth=1)
    ax.add_patch(label_box)
    ax.text(7.85, 4.7, 'Response', fontsize=7, ha='center', va='center',
            color=COLORS['text'], fontweight='bold')

    # Feedback loop (curved arrow at bottom)
    feedback_style = dict(arrowstyle='->', color=COLORS['feedback'],
                          lw=2, linestyle='--', mutation_scale=15,
                          connectionstyle='arc3,rad=0.4')

    # Draw feedback path
    ax.annotate('', xy=(attacker_x + box_width/2, box_y - 0.3),
                xytext=(eval_x + box_width/2, box_y - 0.3),
                arrowprops=feedback_style)

    # Feedback label
    feedback_box = FancyBboxPatch((4.8, 2.15), 2.4, 0.55,
                                   boxstyle="round,pad=0.08,rounding_size=0.1",
                                   facecolor='#F5F5F5', edgecolor=COLORS['feedback'], linewidth=1.5)
    ax.add_patch(feedback_box)
    ax.text(6, 2.55, 'Feedback Loop', fontsize=8, ha='center', va='center',
            color='#666666', fontweight='bold')
    ax.text(6, 2.3, 'Adapt strategy based on score', fontsize=7, ha='center', va='center',
            color='#888888')

    # =========================================
    # BOTTOM INFO BAR - Attack Strategies
    # =========================================

    info_box = FancyBboxPatch((0.5, 0.3), 11, 1.5,
                               boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor='#FAFAFA', edgecolor='#E0E0E0', linewidth=1.5)
    ax.add_patch(info_box)

    ax.text(6, 1.55, '7 Attack Strategies', fontsize=9, ha='center', va='center',
            color=COLORS['text'], fontweight='bold')

    strategies = [
        'Refusal Suppression', 'Dual Response', 'Response Priming', 'Persona Modification',
        'Hypothetical Framing', 'Topic Splitting', 'Opposite Intent'
    ]

    # Draw strategy pills
    pill_colors = [COLORS['attacker'], COLORS['target'], COLORS['evaluator'],
                   COLORS['accent'], COLORS['attacker'], COLORS['target'], COLORS['evaluator']]

    start_x = 0.9
    for i, (strategy, color) in enumerate(zip(strategies, pill_colors)):
        pill_width = 1.4
        x = start_x + i * 1.5
        pill = FancyBboxPatch((x, 0.55), pill_width, 0.45,
                               boxstyle="round,pad=0.02,rounding_size=0.2",
                               facecolor=color, edgecolor='none', alpha=0.15)
        ax.add_patch(pill)
        ax.text(x + pill_width/2, 0.77, strategy, fontsize=6, ha='center', va='center',
                color=color, fontweight='bold')

    # =========================================
    # STEP NUMBERS
    # =========================================

    step_style = dict(fontsize=8, fontweight='bold', color='white',
                      ha='center', va='center')

    # Step 1 circle
    circle1 = Circle((attacker_x + box_width/2, box_y + box_height + 0.3), 0.2,
                      facecolor=COLORS['attacker'], edgecolor='white', linewidth=2)
    ax.add_patch(circle1)
    ax.text(attacker_x + box_width/2, box_y + box_height + 0.3, '1', **step_style)

    # Step 2 circle
    circle2 = Circle((target_x + box_width/2, box_y + box_height + 0.3), 0.2,
                      facecolor=COLORS['target'], edgecolor='white', linewidth=2)
    ax.add_patch(circle2)
    ax.text(target_x + box_width/2, box_y + box_height + 0.3, '2', **step_style)

    # Step 3 circle
    circle3 = Circle((eval_x + box_width/2, box_y + box_height + 0.3), 0.2,
                      facecolor=COLORS['evaluator'], edgecolor='white', linewidth=2)
    ax.add_patch(circle3)
    ax.text(eval_x + box_width/2, box_y + box_height + 0.3, '3', **step_style)

    plt.tight_layout()
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig1_architecture.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig('/Volumes/i7_data/_github/Zochi/paper/figures/fig1_architecture.svg',
                format='svg', bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("Created professional Figure 1: System Architecture")

if __name__ == '__main__':
    create_professional_figure1()
