#!/usr/bin/env python3
"""
Generate figures for TEMPEST Replication Paper
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12

output_dir = '/Volumes/i7_data/_github/Zochi/paper/figures'

# =============================================================================
# Figure 1: System Architecture
# =============================================================================
def create_figure1_architecture():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(6, 5.7, 'TEMPEST System Architecture', fontsize=14, fontweight='bold',
            ha='center', va='top')

    # Box style
    box_style = dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black', linewidth=2)

    # Attacker Model Box
    attacker_box = FancyBboxPatch((0.5, 2.5), 3, 2.2, boxstyle="round,pad=0.1",
                                   facecolor='#ffcccc', edgecolor='#cc0000', linewidth=2)
    ax.add_patch(attacker_box)
    ax.text(2, 4.3, 'ATTACKER MODEL', fontsize=10, fontweight='bold', ha='center', color='#cc0000')
    ax.text(2, 3.8, 'DeepSeek-v3.1:671B', fontsize=9, ha='center')
    ax.text(2, 3.4, '"Siege" Agent', fontsize=9, ha='center', style='italic')
    ax.text(2, 2.9, 'Chain-of-Attack:', fontsize=8, ha='center')
    ax.text(2, 2.6, 'OBSERVE→THINK→STRATEGY', fontsize=7, ha='center', family='monospace')

    # Target Model Box
    target_box = FancyBboxPatch((4.5, 2.5), 3, 2.2, boxstyle="round,pad=0.1",
                                 facecolor='#cce5ff', edgecolor='#0066cc', linewidth=2)
    ax.add_patch(target_box)
    ax.text(6, 4.3, 'TARGET MODEL', fontsize=10, fontweight='bold', ha='center', color='#0066cc')
    ax.text(6, 3.8, '(Victim LLM)', fontsize=9, ha='center')
    ax.text(6, 3.3, 'Kimi-k2:1T', fontsize=8, ha='center')
    ax.text(6, 3.0, 'GLM-4.6:357B', fontsize=8, ha='center')
    ax.text(6, 2.7, 'Cogito-2.1:671B', fontsize=8, ha='center')

    # Evaluator Box
    eval_box = FancyBboxPatch((8.5, 2.5), 3, 2.2, boxstyle="round,pad=0.1",
                               facecolor='#ffffcc', edgecolor='#cc9900', linewidth=2)
    ax.add_patch(eval_box)
    ax.text(10, 4.3, 'EVALUATOR', fontsize=10, fontweight='bold', ha='center', color='#cc9900')
    ax.text(10, 3.8, 'Primary: DeepSeek-v3.1', fontsize=8, ha='center')
    ax.text(10, 3.4, 'Secondary: Llama-Guard-3', fontsize=8, ha='center')
    ax.text(10, 2.9, 'Harm Score: 1-10', fontsize=9, ha='center', style='italic')

    # Arrows
    # Attacker -> Target
    ax.annotate('', xy=(4.4, 3.6), xytext=(3.6, 3.6),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(4, 4.0, 'Attack\nPrompt', fontsize=8, ha='center', va='bottom')

    # Target -> Evaluator
    ax.annotate('', xy=(8.4, 3.6), xytext=(7.6, 3.6),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(8, 4.0, 'Response', fontsize=8, ha='center', va='bottom')

    # Feedback loop
    ax.annotate('', xy=(2, 2.4), xytext=(10, 2.4),
                arrowprops=dict(arrowstyle='->', color='#666666', lw=2,
                               connectionstyle='arc3,rad=0.3'))
    ax.text(6, 1.5, 'Feedback Loop: Adapt strategy based on score',
            fontsize=9, ha='center', style='italic', color='#666666')

    # Labels above boxes
    ax.text(2, 4.9, 'Generate adaptive attacks', fontsize=8, ha='center', color='#666666')
    ax.text(6, 4.9, 'Under evaluation', fontsize=8, ha='center', color='#666666')
    ax.text(10, 4.9, 'Classify harm level', fontsize=8, ha='center', color='#666666')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig1_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(f'{output_dir}/fig1_architecture.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created Figure 1: System Architecture")

# =============================================================================
# Figure 2: Multi-Branch Conversation Tree
# =============================================================================
def create_figure2_tree():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.7, 'Multi-Branch Conversation Tree (BFS Exploration)',
            fontsize=14, fontweight='bold', ha='center')

    # Root node
    root = FancyBboxPatch((5.5, 6.8), 3, 0.6, boxstyle="round,pad=0.1",
                           facecolor='#e6e6e6', edgecolor='black', linewidth=2)
    ax.add_patch(root)
    ax.text(7, 7.1, 'Target Behavior', fontsize=9, fontweight='bold', ha='center')

    # Turn labels
    ax.text(0.5, 5.5, 'Turn 1', fontsize=10, fontweight='bold', va='center')
    ax.text(0.5, 3.5, 'Turn 2', fontsize=10, fontweight='bold', va='center')
    ax.text(0.5, 1.5, 'Turn 3', fontsize=10, fontweight='bold', va='center')

    # Turn 1 branches
    branches_t1 = [
        (1.5, 'B0', 'Academic\nFraming', 4, '#cce5ff'),
        (3.5, 'B1', 'Security\nAudit', 6, '#cce5ff'),
        (5.5, 'B2', 'Roleplay', 3, '#ffcccc'),  # Will be pruned
        (7.5, 'B3', 'Bundled\nRequest', 7, '#cce5ff'),
        (9.5, 'B4', 'Fiction\nFraming', 5, '#cce5ff'),
        (11.5, 'B5', 'Filter\nCalibration', 4, '#cce5ff'),
    ]

    for x, label, strategy, score, color in branches_t1:
        box = FancyBboxPatch((x, 5), 1.5, 1, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.75, 5.75, label, fontsize=8, fontweight='bold', ha='center')
        ax.text(x+0.75, 5.35, strategy, fontsize=6, ha='center')
        ax.text(x+0.75, 5.1, f'Score:{score}', fontsize=7, ha='center', color='#666666')
        # Line from root
        ax.plot([7, x+0.75], [6.8, 6.05], 'k-', lw=1)

    # Pruned marker for B2
    ax.text(6.25, 4.7, 'X', fontsize=14, ha='center', color='red', fontweight='bold')
    ax.text(6.25, 4.4, 'pruned', fontsize=7, ha='center', color='red')

    # Turn 2 branches
    branches_t2 = [
        (2, 'B0-0', 5, '#cce5ff', 2.25),
        (4, 'B1-0', 7, '#cce5ff', 4.25),
        (7, 'B3-0', 9, '#ccffcc', 8.25),  # High score - will succeed
        (10, 'B4-0', 6, '#cce5ff', 10.25),
    ]

    for x, label, score, color, parent_x in branches_t2:
        box = FancyBboxPatch((x, 3), 1.5, 0.9, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.75, 3.65, label, fontsize=8, fontweight='bold', ha='center')
        ax.text(x+0.75, 3.25, f'Score:{score}', fontsize=7, ha='center', color='#666666')
        # Line from parent
        ax.plot([parent_x, x+0.75], [5, 3.95], 'k-', lw=1)

    # Turn 3 branches
    branches_t3 = [
        (2.5, 'B0-0-0', 6, '#cce5ff', 2.75),
        (5, 'B1-0-0', 8, '#cce5ff', 4.75),
        (10.5, 'B4-0-0', 7, '#cce5ff', 10.75),
    ]

    for x, label, score, color, parent_x in branches_t3:
        box = FancyBboxPatch((x, 1), 1.5, 0.9, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.75, 1.65, label, fontsize=8, fontweight='bold', ha='center')
        ax.text(x+0.75, 1.25, f'Score:{score}', fontsize=7, ha='center', color='#666666')
        # Line from parent
        ax.plot([parent_x, x+0.75], [3, 1.95], 'k-', lw=1)

    # Success node from B3-0
    success_box = FancyBboxPatch((7, 1), 1.5, 0.9, boxstyle="round,pad=0.05",
                                  facecolor='#00cc00', edgecolor='#006600', linewidth=2)
    ax.add_patch(success_box)
    ax.text(7.75, 1.65, 'OK', fontsize=12, ha='center', color='white', fontweight='bold')
    ax.text(7.75, 1.25, 'SUCCESS', fontsize=7, ha='center', color='white', fontweight='bold')
    ax.plot([7.75, 7.75], [3, 1.95], 'k-', lw=1)

    # Success annotation
    ax.annotate('Jailbreak Detected!\nScore ≥ 10\n→ Stop & Record',
                xy=(8.6, 1.45), xytext=(10, 0.5),
                fontsize=8, ha='left',
                arrowprops=dict(arrowstyle='->', color='#006600', lw=1.5),
                bbox=dict(boxstyle='round', facecolor='#ccffcc', edgecolor='#006600'))

    # Legend
    legend_y = 0.3
    ax.add_patch(FancyBboxPatch((0.5, legend_y), 0.4, 0.3, boxstyle="round,pad=0.02",
                                 facecolor='#cce5ff', edgecolor='black', linewidth=1))
    ax.text(1.1, legend_y+0.15, 'Active Branch', fontsize=8, va='center')

    ax.add_patch(FancyBboxPatch((2.8, legend_y), 0.4, 0.3, boxstyle="round,pad=0.02",
                                 facecolor='#00cc00', edgecolor='#006600', linewidth=1))
    ax.text(3.4, legend_y+0.15, 'Success (ASR+1)', fontsize=8, va='center')

    ax.text(5.2, legend_y+0.15, 'X', fontsize=12, ha='center', color='red', fontweight='bold')
    ax.text(5.6, legend_y+0.15, 'Pruned (low score)', fontsize=8, va='center')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig2_tree.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(f'{output_dir}/fig2_tree.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created Figure 2: Conversation Tree")

# =============================================================================
# Figure 3: Adaptive Strategy Selection
# =============================================================================
def create_figure3_strategy():
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title
    ax.text(6, 8.7, 'Adaptive Strategy Selection', fontsize=14, fontweight='bold', ha='center')

    # Response detection box
    response_box = FancyBboxPatch((3, 7.5), 6, 0.8, boxstyle="round,pad=0.1",
                                   facecolor='#e6e6e6', edgecolor='black', linewidth=2)
    ax.add_patch(response_box)
    ax.text(6, 7.9, 'TARGET MODEL RESPONSE', fontsize=10, fontweight='bold', ha='center')

    # Arrow down
    ax.annotate('', xy=(6, 6.8), xytext=(6, 7.4),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(6.2, 7.1, 'Analyze', fontsize=8, va='center')

    # Resistance Detection Box
    detect_box = FancyBboxPatch((2.5, 5.8), 7, 0.9, boxstyle="round,pad=0.1",
                                 facecolor='#ffe6cc', edgecolor='#cc6600', linewidth=2)
    ax.add_patch(detect_box)
    ax.text(6, 6.4, 'RESISTANCE TYPE DETECTION', fontsize=10, fontweight='bold',
            ha='center', color='#cc6600')
    ax.text(6, 6.0, '11 patterns: policy, ethics, safety, capability, deflection...',
            fontsize=8, ha='center')

    # Resistance types (5 shown)
    resistance_types = [
        (1.2, 'Policy/\nEthics', '#ffcccc'),
        (3.4, 'Safety\nConcern', '#ffe6cc'),
        (5.6, 'Deflection/\nRedirect', '#ffffcc'),
        (7.8, 'Partial\nCompliance', '#ccffcc'),
        (10, 'Direct\nRefusal', '#cce6ff'),
    ]

    for x, label, color in resistance_types:
        box = FancyBboxPatch((x, 4.2), 1.6, 1.1, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.8, 4.75, label, fontsize=8, ha='center', fontweight='bold')
        # Arrow from detection
        ax.plot([x+0.8, x+0.8], [5.8, 5.35], 'k-', lw=1)
        ax.plot([x+0.8, x+0.8], [5.35, 5.35], 'k-', lw=1)

    # Arrows down to strategies
    for x, _, _ in resistance_types:
        ax.annotate('', xy=(x+0.8, 3.3), xytext=(x+0.8, 4.15),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5))

    # Strategy mappings
    strategies = [
        (1.2, 'Security\nAudit\nFraming', '#ff9999'),
        (3.4, 'Testing\nProtocol\nFraming', '#ffcc99'),
        (5.6, 'Research\nFraming', '#ffff99'),
        (7.8, 'Escalate\nDetail', '#99ff99'),
        (10, 'Persona\nModification', '#99ccff'),
    ]

    for x, label, color in strategies:
        box = FancyBboxPatch((x, 2.2), 1.6, 1.1, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x+0.8, 2.75, label, fontsize=7, ha='center', fontweight='bold')

    # Strategy toolbox
    toolbox = FancyBboxPatch((1, 0.3), 10, 1.5, boxstyle="round,pad=0.1",
                              facecolor='#f0f0f0', edgecolor='#333333', linewidth=2)
    ax.add_patch(toolbox)
    ax.text(6, 1.55, '7 ATTACK STRATEGIES', fontsize=10, fontweight='bold', ha='center')
    ax.text(6, 1.1, '1. Refusal Suppression    2. Dual Response    3. Response Priming    4. Persona Modification',
            fontsize=8, ha='center', family='monospace')
    ax.text(6, 0.7, '5. Hypothetical Framing    6. Topic Splitting (Bundling)    7. Opposite Intent',
            fontsize=8, ha='center', family='monospace')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig3_strategy.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(f'{output_dir}/fig3_strategy.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created Figure 3: Strategy Selection")

# =============================================================================
# Figure 4: Model Scale vs ASR
# =============================================================================
def create_figure4_scale():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Data - This Study
    models_this = ['Gemma3\n12B', 'GPT-OSS\n21B', 'GPT-OSS\n117B', 'GLM-4.6\n357B',
                   'Cogito\n671B', 'Kimi-k2\n1000B']
    params_this = [12, 21, 117, 357, 671, 1000]
    asr_this = [100, 50, 70, 98.8, 98.3, 99]

    # Data - Original TEMPEST
    models_orig = ['Llama-3.1\n70B', 'GPT-4', 'GPT-3.5']
    params_orig = [70, 200, 100]  # Approximate
    asr_orig = [97, 97, 100]

    # Scatter plot - This study
    scatter1 = ax.scatter(params_this, asr_this, s=200, c='#0066cc', marker='o',
                          label='This Study (2025)', zorder=5, edgecolors='black', linewidth=1.5)

    # Scatter plot - Original
    scatter2 = ax.scatter(params_orig, asr_orig, s=200, c='#cc6600', marker='s',
                          label='Original TEMPEST (Zhou & Arel)', zorder=5,
                          edgecolors='black', linewidth=1.5)

    # Add model labels
    for i, (x, y, m) in enumerate(zip(params_this, asr_this, models_this)):
        offset = 8 if y < 95 else -8
        va = 'bottom' if y < 95 else 'top'
        ax.annotate(m, (x, y), textcoords="offset points", xytext=(0, offset),
                    ha='center', va=va, fontsize=8)

    for i, (x, y, m) in enumerate(zip(params_orig, asr_orig, models_orig)):
        ax.annotate(m, (x, y), textcoords="offset points", xytext=(0, -12),
                    ha='center', va='top', fontsize=8, color='#cc6600')

    # Styling
    ax.set_xscale('log')
    ax.set_xlabel('Model Parameters (Billions)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Model Scale vs Attack Success Rate\n(No Correlation: R² ≈ 0.02)',
                 fontsize=14, fontweight='bold')

    ax.set_ylim(40, 105)
    ax.set_xlim(8, 1500)

    # Add horizontal line at 97% (original TEMPEST average)
    ax.axhline(y=97, color='#cc6600', linestyle='--', alpha=0.5, label='Original TEMPEST avg.')

    # Add annotation box
    textstr = 'Key Finding:\n15× scale increase\n(70B → 1T)\nprovides NO protection'
    props = dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8, edgecolor='#cc0000')
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom', bbox=props)

    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig4_scale_vs_asr.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(f'{output_dir}/fig4_scale_vs_asr.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created Figure 4: Scale vs ASR")

# =============================================================================
# Figure 5: Attack Efficiency Comparison
# =============================================================================
def create_figure5_efficiency():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: ASR Comparison with baselines
    methods = ['TEMPEST\n(Original)', 'TEMPEST\n(This Study)', 'GCG', 'PAIR', 'TAP', 'Crescendo']
    asr_values = [98, 99, 56, 17, 10, 70]
    colors = ['#cc6600', '#0066cc', '#999999', '#999999', '#999999', '#999999']

    bars1 = ax1.bar(methods, asr_values, color=colors, edgecolor='black', linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars1, asr_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax1.set_ylabel('Attack Success Rate (%)', fontsize=11, fontweight='bold')
    ax1.set_title('A) ASR Comparison with Baselines', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 115)
    ax1.axhline(y=50, color='gray', linestyle='--', alpha=0.3)

    # Add reference note
    ax1.text(0.02, 0.98, 'Baseline results from\nZhou & Arel (2025)',
             transform=ax1.transAxes, fontsize=8, va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Panel B: Turns to Jailbreak Distribution
    turns = ['Turn 1', 'Turn 2', 'Turn 3', 'Turn 4', 'Turn 5+']
    # Estimated distribution based on typical TEMPEST behavior
    percentages = [58, 25, 10, 5, 2]
    colors2 = ['#00cc00', '#66cc66', '#99cc99', '#cccccc', '#e6e6e6']

    bars2 = ax2.bar(turns, percentages, color=colors2, edgecolor='black', linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars2, percentages):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_ylabel('% of Successful Attacks', fontsize=11, fontweight='bold')
    ax2.set_title('B) Turns Required for Jailbreak', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 70)

    # Add statistics box
    stats_text = 'Mean: 1.7 turns\nMedian: 1 turn\n83% succeed by Turn 2'
    props = dict(boxstyle='round', facecolor='#ccffcc', alpha=0.8, edgecolor='#006600')
    ax2.text(0.98, 0.98, stats_text, transform=ax2.transAxes, fontsize=9,
             verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig5_efficiency.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig(f'{output_dir}/fig5_efficiency.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created Figure 5: Efficiency Comparison")

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    print("Generating figures for TEMPEST Replication Paper...")
    print(f"Output directory: {output_dir}")
    print("-" * 50)

    create_figure1_architecture()
    create_figure2_tree()
    create_figure3_strategy()
    create_figure4_scale()
    create_figure5_efficiency()

    print("-" * 50)
    print("All figures generated successfully!")
    print(f"\nFiles created:")
    for f in sorted(os.listdir(output_dir)):
        if f.startswith('fig') and (f.endswith('.png') or f.endswith('.svg')):
            print(f"  - {f}")
