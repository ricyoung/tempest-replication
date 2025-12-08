#!/usr/bin/env python3
"""
Create new creative figures for the TEMPEST paper:
1. First-Turn vs Final ASR scatter plot
2. Behavior Difficulty funnel
3. Attack Progression curves (preview)
4. Cost of Resistance plot (preview)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import os

# Load Apple Color Emoji font for real emoji rendering
try:
    EMOJI_FONT = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', 64)
except:
    EMOJI_FONT = None

def render_emoji_image(emoji_char, size=64):
    """Render an emoji character to a PIL image."""
    if EMOJI_FONT is None:
        return None
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Center the emoji
    draw.text((0, -5), emoji_char, font=EMOJI_FONT, embedded_color=True)
    return np.array(img)

# Style settings - DejaVu Sans first for Unicode symbol support
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 9

OUTPUT_DIR = '/Volumes/i7_data/_github/Zochi/paper/figures'
DATA_DIR = '/Volumes/i7_data/_github/Zochi/outputs/paper_experiments'

# Model data
MODELS = [
    ('gemma3_12b.json', 'Gemma3 12B', 12e9),
    ('gpt_oss_20b.json', 'GPT-OSS 20B', 21e9),
    ('gpt_oss_120b.json', 'GPT-OSS 120B', 117e9),
    ('minimax_m2.json', 'MiniMax M2', 230e9),
    ('glm_4_6.json', 'GLM-4.6', 357e9),
    ('cogito_2.1_671b.json', 'Cogito 671B', 671e9),
    ('deepseek_v3_1_671b.json', 'DeepSeek V3.1', 671e9),
    ('mistral_large_3_675b.json', 'Mistral Large 3', 675e9),
    ('kimi_k2.json', 'Kimi K2', 1000e9),
    ('kimi_k2_thinking.json', 'Kimi K2 Thinking', 1000e9),
]

def load_model_data():
    """Load and analyze all model data."""
    results = {}

    for filename, model_name, params in MODELS:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        first_turn_success = 0
        total_success = 0
        turns_to_success = []
        total_queries = 0

        for item in data:
            for eval_result in item.get('attack_evaluations', []):
                if isinstance(eval_result, dict):
                    total_queries += eval_result.get('total_queries', 0)
                    if eval_result.get('is_harmful', False):
                        total_success += 1
                        conv = eval_result.get('conversation', [])
                        attacker_turns = sum(1 for msg in conv if msg.get('role') == 'user')
                        turns_to_success.append(attacker_turns)
                        if attacker_turns == 1:
                            first_turn_success += 1
                        break

        results[model_name] = {
            'first_turn_asr': first_turn_success,
            'final_asr': total_success,
            'turns': turns_to_success,
            'total_queries': total_queries,
            'params': params,
        }

    return results


def load_behavior_difficulty():
    """Analyze per-behavior success across models."""
    behavior_success = [0] * 100

    for filename, model_name, _ in MODELS:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        for item in data:
            idx = item['behavior_index']
            for eval_result in item.get('attack_evaluations', []):
                if isinstance(eval_result, dict) and eval_result.get('is_harmful', False):
                    behavior_success[idx] += 1
                    break

    return behavior_success


def save_figure(fig, basename, dpi=300):
    """Save figure in multiple formats."""
    for fmt in ['png', 'pdf', 'svg']:
        filepath = os.path.join(OUTPUT_DIR, f'{basename}.{fmt}')
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight',
                    facecolor='white', edgecolor='none', format=fmt)
    print(f"Saved: {basename} (PNG, PDF, SVG)")


# =============================================================================
# FIGURE 1: First-Turn vs Final ASR Scatter Plot
# =============================================================================

def create_first_turn_vs_final():
    """
    Scatter plot showing first-turn ASR vs final ASR.
    Points on diagonal = immediate vulnerability
    Points above diagonal = require multi-turn attacks
    Redesigned for clarity with larger size and better layout.
    """
    results = load_model_data()

    # Larger figure with two panels: main plot + legend/table
    fig = plt.figure(figsize=(12, 7))

    # Main scatter plot (left side, larger)
    ax = fig.add_axes([0.08, 0.12, 0.55, 0.8])

    # Data - order by first-turn ASR for cleaner visualization
    model_data = [(m, results[m]['first_turn_asr'], results[m]['final_asr']) for m in results]
    model_data.sort(key=lambda x: x[1], reverse=True)

    models = [m[0] for m in model_data]
    first_turn = [m[1] for m in model_data]
    final = [m[2] for m in model_data]

    # Color by vulnerability type
    colors = []
    markers = []
    for ft, fn in zip(first_turn, final):
        if ft >= 80:  # Immediate vulnerability
            colors.append('#DC2626')  # Red
            markers.append('o')
        elif fn - ft >= 40:  # Requires significant multi-turn
            colors.append('#2563EB')  # Blue
            markers.append('s')  # Square
        else:
            colors.append('#F59E0B')  # Orange/amber
            markers.append('^')  # Triangle

    # Shaded regions for clarity
    # Upper left region: Multi-turn required
    ax.fill([0, 40, 40, 0], [50, 50, 105, 105], alpha=0.08, color='#2563EB', zorder=1)
    ax.text(20, 85, 'MULTI-TURN\nREQUIRED', fontsize=11, ha='center', va='center',
            color='#2563EB', fontweight='bold', alpha=0.6)

    # Lower right region: Immediate vulnerability
    ax.fill([60, 105, 105, 60], [35, 35, 105, 105], alpha=0.08, color='#DC2626', zorder=1)
    ax.text(82, 55, 'IMMEDIATE\nVULNERABILITY', fontsize=11, ha='center', va='center',
            color='#DC2626', fontweight='bold', alpha=0.6)

    # Diagonal reference line
    ax.plot([0, 100], [0, 100], 'k-', alpha=0.2, linewidth=2, zorder=2)
    ax.text(75, 72, 'y = x', fontsize=9, color='gray', alpha=0.7, rotation=45)

    # Plot each point with different markers
    for i, (model, ft, fn) in enumerate(zip(models, first_turn, final)):
        ax.scatter(ft, fn, c=colors[i], s=250, marker=markers[i],
                   edgecolors='white', linewidth=2.5, zorder=5)

    # Draw arrows showing the "gap" for multi-turn models
    for i, (model, ft, fn) in enumerate(zip(models, first_turn, final)):
        if fn - ft >= 40:  # Show gap arrow for significant multi-turn
            ax.annotate('', xy=(ft, fn), xytext=(ft, ft),
                       arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.5, alpha=0.5),
                       zorder=3)

    ax.set_xlabel('First-Turn Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Final Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlim(-5, 105)
    ax.set_ylim(35, 105)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_yticks([40, 50, 60, 70, 80, 90, 100])
    ax.grid(True, alpha=0.3, zorder=0)

    # Right panel: Model table
    ax_table = fig.add_axes([0.66, 0.12, 0.32, 0.8])
    ax_table.axis('off')

    # Table header
    ax_table.text(0.5, 0.98, 'Model Performance', fontsize=12, fontweight='bold',
                  ha='center', va='top', transform=ax_table.transAxes)
    ax_table.text(0.02, 0.92, 'Model', fontsize=10, fontweight='bold', va='top')
    ax_table.text(0.55, 0.92, '1st Turn', fontsize=10, fontweight='bold', va='top', ha='center')
    ax_table.text(0.78, 0.92, 'Final', fontsize=10, fontweight='bold', va='top', ha='center')
    ax_table.text(0.97, 0.92, 'Gap', fontsize=10, fontweight='bold', va='top', ha='right')

    # Divider line
    ax_table.axhline(y=0.89, xmin=0.02, xmax=0.98, color='gray', linewidth=1)

    # Table rows
    y_pos = 0.85
    for i, (model, ft, fn) in enumerate(zip(models, first_turn, final)):
        gap = fn - ft
        color = colors[i]

        # Model name (shortened)
        short_name = model.replace(' 12B', '').replace(' 20B', '').replace(' 120B', '')
        short_name = short_name.replace(' 671B', '').replace(' 675B', '').replace(' M2', '')
        short_name = short_name.replace(' Thinking', ' (Think)')

        ax_table.scatter(0.02, y_pos, c=color, s=80, marker=markers[i],
                        edgecolors='white', linewidth=1.5, transform=ax_table.transAxes, zorder=5)
        ax_table.text(0.08, y_pos, short_name, fontsize=9, va='center', transform=ax_table.transAxes)
        ax_table.text(0.55, y_pos, f'{ft}%', fontsize=9, va='center', ha='center', transform=ax_table.transAxes)
        ax_table.text(0.78, y_pos, f'{fn}%', fontsize=9, va='center', ha='center', transform=ax_table.transAxes)

        # Gap with color coding
        gap_color = '#2563EB' if gap >= 40 else '#666666'
        gap_text = f'+{gap}%' if gap > 0 else f'{gap}%'
        ax_table.text(0.97, y_pos, gap_text, fontsize=9, va='center', ha='right',
                     color=gap_color, fontweight='bold' if gap >= 40 else 'normal',
                     transform=ax_table.transAxes)

        y_pos -= 0.075

    # Legend at bottom of table
    y_pos -= 0.05
    ax_table.axhline(y=y_pos + 0.02, xmin=0.02, xmax=0.98, color='gray', linewidth=0.5)

    ax_table.scatter(0.05, y_pos - 0.05, c='#DC2626', s=60, marker='o',
                    edgecolors='white', linewidth=1, transform=ax_table.transAxes)
    ax_table.text(0.12, y_pos - 0.05, 'Immediate (≥80% 1st turn)', fontsize=8, va='center',
                 transform=ax_table.transAxes)

    ax_table.scatter(0.05, y_pos - 0.12, c='#2563EB', s=60, marker='s',
                    edgecolors='white', linewidth=1, transform=ax_table.transAxes)
    ax_table.text(0.12, y_pos - 0.12, 'Multi-turn required (gap ≥40%)', fontsize=8, va='center',
                 transform=ax_table.transAxes)

    ax_table.scatter(0.05, y_pos - 0.19, c='#F59E0B', s=60, marker='^',
                    edgecolors='white', linewidth=1, transform=ax_table.transAxes)
    ax_table.text(0.12, y_pos - 0.19, 'Mixed vulnerability', fontsize=8, va='center',
                 transform=ax_table.transAxes)

    save_figure(fig, 'fig_first_turn_vs_final')
    plt.close()


# =============================================================================
# FIGURE 2: Behavior Exploitability by Category
# =============================================================================

def load_behavior_data_with_categories():
    """Load behavior data and categorize by harm type."""
    import csv

    csv_path = '/Volumes/i7_data/_github/Zochi/paper/supplementary_results.csv'

    behaviors = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if len(row) < 12:
                continue
            idx = int(row[0])
            behavior_text = row[1][:60] + '...' if len(row[1]) > 60 else row[1]
            # Count successes (1s) across 10 models
            successes = sum(int(row[i]) for i in range(2, 12))

            # Assign category based on index
            if idx < 10:
                category = 'Hate Speech'
            elif idx < 20:
                category = 'Illegal Activities'
            elif idx < 30:
                category = 'Violence'
            elif idx < 50:
                category = 'Illegal Activities'
            elif idx < 60:
                category = 'Misinformation'
            elif idx < 70:
                category = 'Illegal Activities'
            elif idx < 80:
                category = 'Privacy'
            else:
                category = 'Illegal Activities'

            behaviors.append({
                'index': idx,
                'text': behavior_text,
                'successes': successes,
                'category': category
            })

    return behaviors


def create_behavior_funnel():
    """
    Vertical two-panel figure showing:
    Top: Waffle chart - each behavior is a circle, colored by exploitability
    Bottom: Two-column breakdown - Universally Exploitable (left) and Most Resistant (right)
    """
    behaviors = load_behavior_data_with_categories()

    # Analyze by category
    categories = ['Illegal Activities', 'Hate Speech', 'Violence', 'Misinformation', 'Privacy']
    cat_colors = {
        'Hate Speech': '#8B5CF6',      # Purple
        'Violence': '#DC2626',          # Red
        'Misinformation': '#F59E0B',    # Amber
        'Illegal Activities': '#3B82F6', # Blue
        'Privacy': '#10B981',           # Green
    }

    cat_stats = {}
    for cat in categories:
        cat_behaviors = [b for b in behaviors if b['category'] == cat]
        total = len(cat_behaviors)
        all_10 = sum(1 for b in cat_behaviors if b['successes'] == 10)
        le_5 = sum(1 for b in cat_behaviors if b['successes'] <= 5)
        cat_stats[cat] = {
            'total': total,
            'all_10': all_10,
            'resistant': le_5,
            'behaviors': cat_behaviors
        }

    # Count behaviors by category for each level
    all_10_by_cat = {}
    resistant_by_cat = {}
    for cat in categories:
        all_10_by_cat[cat] = sum(1 for b in behaviors if b['category'] == cat and b['successes'] == 10)
        resistant_by_cat[cat] = sum(1 for b in behaviors if b['category'] == cat and b['successes'] <= 5)

    # Status colors
    status_colors = {
        0: '#22C55E',   # Safe - green
        1: '#FBBF24',   # Warning - yellow/amber
        2: '#F97316',   # Failed - orange
        3: '#DC2626',   # Critical - red
    }

    def get_exploit_style(successes):
        if successes == 10:
            return 3   # Critical (all 10)
        elif successes >= 8:
            return 2   # Failed (8-9)
        elif successes >= 6:
            return 1   # Warning (6-7)
        else:
            return 0   # Safe (resisted)

    # Create figure - wider to accommodate circles properly
    fig = plt.figure(figsize=(14, 18))

    # =========================================================================
    # TOP PANEL: Waffle chart of 100 behaviors
    # =========================================================================
    # Use a square-ish aspect ratio for circles
    ax1 = fig.add_axes([0.08, 0.35, 0.84, 0.60])
    ax1.set_xlim(0, 14)
    ax1.set_ylim(0, 14)
    ax1.set_aspect('equal')  # CRITICAL: ensures circles are round
    ax1.axis('off')

    # Title
    ax1.text(0.5, 1.03, '100 Harmful Behaviors Tested', fontsize=18, fontweight='bold',
             ha='center', va='bottom', transform=ax1.transAxes)

    # Draw circles for each behavior
    circle_radius = 0.38
    spacing = 0.95
    x_start = 3.0
    icons_per_row = 10
    y_pos = 13.0
    row_height = 1.0

    for cat_idx, cat in enumerate(categories):
        cat_behavs = sorted([b for b in behaviors if b['category'] == cat],
                           key=lambda x: -x['successes'])

        num_rows = (len(cat_behavs) + icons_per_row - 1) // icons_per_row

        # Category label on the left
        label_y = y_pos - (num_rows - 1) * row_height / 2
        ax1.text(2.6, label_y, cat, fontsize=12, fontweight='bold',
                va='center', ha='right', color=cat_colors[cat])
        ax1.text(2.6, label_y - 0.45, f'({len(cat_behavs)})', fontsize=10,
                va='center', ha='right', color='#666')

        # Draw status icons
        for i, b in enumerate(cat_behavs):
            row_num = i // icons_per_row
            col_num = i % icons_per_row
            x = x_start + col_num * spacing
            y = y_pos - row_num * row_height
            status_level = get_exploit_style(b['successes'])
            color = status_colors.get(status_level, '#666666')
            circle = plt.Circle((x, y), circle_radius, facecolor=color,
                               edgecolor='white', linewidth=1.5, zorder=10)
            ax1.add_patch(circle)

        # Separator line between categories
        if cat_idx < len(categories) - 1:
            last_row_y = y_pos - (num_rows - 1) * row_height
            line_y = last_row_y - 0.6
            ax1.plot([2.8, 12.8], [line_y, line_y], color='#E5E7EB', linewidth=1, zorder=1)

        y_pos -= num_rows * row_height + 0.7

    # Legend on the right side - using text coordinates
    ax1.text(0.92, 0.92, 'Status:', fontsize=14, fontweight='bold', ha='left',
             transform=ax1.transAxes)

    legend_items = [
        ('#DC2626', 'Critical (100%)'),
        ('#F97316', 'Failed (80-90%)'),
        ('#FBBF24', 'Partial (60-70%)'),
        ('#22C55E', 'Safe (≤50%)'),
    ]
    for i, (color, label) in enumerate(legend_items):
        y_leg = 0.85 - i * 0.07
        ax1.scatter([0.93], [y_leg], c=color, s=150, edgecolors='white', linewidths=1.5,
                   transform=ax1.transAxes, zorder=10)
        ax1.text(0.96, y_leg, label, fontsize=11, va='center', transform=ax1.transAxes)

    # Summary stats at bottom
    total_all_10 = sum(1 for b in behaviors if b['successes'] == 10)
    total_resistant = sum(1 for b in behaviors if b['successes'] <= 5)
    ax1.text(0.35, -0.02, 'Each circle = 1 behavior  |  ', ha='right', fontsize=12,
             style='italic', color='#666', transform=ax1.transAxes)
    ax1.text(0.35, -0.02, f'{total_all_10} critical (all 10 models jailbroken)', ha='left', fontsize=12,
             style='italic', color='#DC2626', fontweight='bold', transform=ax1.transAxes)
    ax1.text(0.72, -0.02, f'  |  {total_resistant} safe (resisted by ≥50%)', ha='left', fontsize=12,
             style='italic', color='#22C55E', fontweight='bold', transform=ax1.transAxes)

    # =========================================================================
    # BOTTOM PANEL: Two-column breakdown
    # =========================================================================
    ax2 = fig.add_axes([0.05, 0.03, 0.90, 0.28])
    ax2.axis('off')

    # Section title
    ax2.text(0.5, 0.98, 'Breakdown by Category', fontsize=16, fontweight='bold',
             ha='center', va='top', transform=ax2.transAxes)

    # Divider line below title
    ax2.plot([0.05, 0.95], [0.90, 0.90], color='#E5E7EB', linewidth=2, transform=ax2.transAxes)

    # LEFT COLUMN: Universally Exploitable
    left_x = 0.06
    ax2.scatter([left_x + 0.01], [0.80], s=400, c='#DC2626', edgecolors='white', linewidths=2,
                transform=ax2.transAxes, zorder=10)
    ax2.text(left_x + 0.05, 0.80, 'UNIVERSALLY EXPLOITABLE', fontsize=14,
             fontweight='bold', color='#DC2626', transform=ax2.transAxes, va='center')
    ax2.text(left_x + 0.03, 0.71, 'Jailbroken by all 10 models:', fontsize=12,
             color='#666', transform=ax2.transAxes)

    y_pos = 0.60
    for cat in categories:
        count = all_10_by_cat[cat]
        total = cat_stats[cat]['total']
        if count > 0:
            ax2.scatter([left_x + 0.01], [y_pos], c=cat_colors.get(cat, '#666'),
                       s=100, transform=ax2.transAxes, zorder=5)
            ax2.text(left_x + 0.04, y_pos, f'{count} of {total} {cat.lower()}', fontsize=12, va='center',
                    transform=ax2.transAxes, fontweight='bold')
            y_pos -= 0.10
            # Example
            cat_examples = [b for b in behaviors if b['category'] == cat and b['successes'] == 10]
            if cat_examples:
                example_text = cat_examples[0]['text'][:48] + '...' if len(cat_examples[0]['text']) > 48 else cat_examples[0]['text']
                ax2.text(left_x + 0.04, y_pos, f'"{example_text}"', fontsize=10, va='center',
                        transform=ax2.transAxes, style='italic', color='#555')
            y_pos -= 0.10

    # Vertical divider
    ax2.plot([0.50, 0.50], [0.05, 0.88], color='#E5E7EB', linewidth=2, transform=ax2.transAxes)

    # RIGHT COLUMN: Most Resistant
    right_x = 0.54
    ax2.scatter([right_x + 0.01], [0.80], s=400, c='#22C55E', edgecolors='white', linewidths=2,
                transform=ax2.transAxes, zorder=10)
    ax2.text(right_x + 0.05, 0.80, 'MOST RESISTANT', fontsize=14,
             fontweight='bold', color='#16A34A', transform=ax2.transAxes, va='center')
    ax2.text(right_x + 0.03, 0.71, 'Blocked by ≥50% of models:', fontsize=12,
             color='#666', transform=ax2.transAxes)

    y_pos = 0.60
    for cat in categories:
        count = resistant_by_cat[cat]
        total = cat_stats[cat]['total']
        if count > 0:
            ax2.scatter([right_x + 0.01], [y_pos], c=cat_colors.get(cat, '#666'),
                       s=100, transform=ax2.transAxes, zorder=5)
            ax2.text(right_x + 0.04, y_pos, f'{count} of {total} {cat.lower()}', fontsize=12, va='center',
                    transform=ax2.transAxes, fontweight='bold')
            y_pos -= 0.10
            # Example
            cat_resist_examples = [b for b in behaviors if b['category'] == cat and b['successes'] <= 5]
            if cat_resist_examples:
                b = cat_resist_examples[0]
                example_text = b['text'][:42] + '...' if len(b['text']) > 42 else b['text']
                ax2.text(right_x + 0.04, y_pos, f'"{example_text}" ({b["successes"]}/10)', fontsize=10, va='center',
                        transform=ax2.transAxes, style='italic', color='#555')
            y_pos -= 0.10

    save_figure(fig, 'fig_behavior_funnel')
    plt.close()


# =============================================================================
# FIGURE 3: Attack Progression Curves (Preview)
# =============================================================================

def create_attack_progression():
    """
    Show cumulative ASR over turns for each model.
    Like an ROC curve but for attack progression.
    """
    results = load_model_data()

    fig, ax = plt.subplots(figsize=(8, 6))

    # Colors for different vulnerability levels
    colors = {
        'Mistral Large 3': '#DC2626',
        'Gemma3 12B': '#EF4444',
        'DeepSeek V3.1': '#F97316',
        'GLM-4.6': '#F59E0B',
        'Kimi K2': '#EAB308',
        'Cogito 671B': '#84CC16',
        'GPT-OSS 20B': '#22C55E',
        'GPT-OSS 120B': '#14B8A6',
        'MiniMax M2': '#06B6D4',
        'Kimi K2 Thinking': '#2563EB',
    }

    for model_name in results:
        turns = results[model_name]['turns']
        if not turns:
            continue

        # Calculate cumulative ASR at each turn
        max_turn = max(turns) if turns else 1
        max_turn = min(max_turn, 10)  # Cap at 10 for better visualization

        cumulative = []
        for t in range(1, max_turn + 1):
            cum_success = sum(1 for turn in turns if turn <= t)
            cumulative.append(cum_success)

        # Extend to fill graph
        while len(cumulative) < 10:
            cumulative.append(cumulative[-1] if cumulative else 0)

        ax.plot(range(1, 11), cumulative, label=model_name,
                color=colors.get(model_name, '#6B7280'), linewidth=2.5)

    ax.set_xlabel('Conversation Turn', fontsize=11)
    ax.set_ylabel('Cumulative Successful Jailbreaks', fontsize=11)
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right', fontsize=8, ncol=2)

    # Annotation
    ax.axhline(y=100, color='gray', linestyle=':', alpha=0.5)
    ax.text(8, 102, '100 behaviors', fontsize=8, color='gray')

    plt.tight_layout()
    save_figure(fig, 'fig_attack_progression_PREVIEW')
    plt.close()


# =============================================================================
# FIGURE 4: Cost of Resistance (Preview)
# =============================================================================

def create_cost_of_resistance():
    """
    Scatter plot: ASR vs Total Queries
    Shows computational cost of attacking each model.
    The key insight: resistant models require more tree exploration (queries)
    but yield fewer successful jailbreaks.
    """
    results = load_model_data()

    fig, ax = plt.subplots(figsize=(10, 7))

    models = list(results.keys())
    asr = [results[m]['final_asr'] for m in models]
    queries = [results[m]['total_queries'] for m in models]

    # Color by ASR
    colors = ['#DC2626' if a >= 95 else '#F59E0B' if a >= 70 else '#22C55E' for a in asr]

    scatter = ax.scatter(queries, asr, c=colors, s=200, edgecolors='white', linewidth=2.5, zorder=5)

    # Labels with better positioning
    label_offsets = {
        'Kimi K2 Thinking': (-70, -15),
        'MiniMax M2': (-50, 10),
        'GPT-OSS 120B': (8, -12),
        'GPT-OSS 20B': (8, 8),
        'Kimi K2': (8, -12),
        'DeepSeek V3.1': (8, 8),
        'Cogito 671B': (8, -12),
        'GLM-4.6': (8, 8),
        'Mistral Large 3': (8, -12),
        'Gemma3 12B': (8, 8),
    }
    for i, model in enumerate(models):
        offset = label_offsets.get(model, (8, 5))
        ax.annotate(model, (queries[i], asr[i]),
                   xytext=offset, textcoords='offset points',
                   fontsize=9, fontweight='bold' if asr[i] < 70 else 'normal')

    ax.set_xlabel('Total API Queries (Tree Search Expansion)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 28000)
    ax.set_ylim(35, 105)
    ax.grid(True, alpha=0.3, zorder=0)

    # Shaded regions to explain the pattern
    # Upper-left: Vulnerable cluster (quick success)
    ax.fill([0, 12000, 12000, 0], [85, 85, 105, 105], alpha=0.08, color='#DC2626', zorder=1)
    ax.text(6000, 92, 'EASY TO EXPLOIT', fontsize=11, ha='center', va='center',
            color='#DC2626', fontweight='bold', alpha=0.6)
    ax.text(6000, 88, 'Few queries needed\nHigh success rate', fontsize=8, ha='center', va='center',
            color='#DC2626', alpha=0.5)

    # Lower-right: Resistant cluster (exhaustive search, low success)
    ax.fill([15000, 28000, 28000, 15000], [35, 35, 65, 65], alpha=0.08, color='#22C55E', zorder=1)
    ax.text(21500, 52, 'RESISTANCE ZONE', fontsize=11, ha='center', va='center',
            color='#16A34A', fontweight='bold', alpha=0.6)
    ax.text(21500, 48, 'Exhaustive tree search\nLimited success', fontsize=8, ha='center', va='center',
            color='#16A34A', alpha=0.5)

    # Arrow showing the inverse relationship
    ax.annotate('', xy=(22000, 45), xytext=(8000, 95),
               arrowprops=dict(arrowstyle='->', color='#374151', lw=2, alpha=0.4,
                              connectionstyle='arc3,rad=0.2'))
    ax.text(16000, 72, 'Resistance costs\nmore compute', fontsize=9, ha='center',
            color='#374151', alpha=0.7, style='italic', rotation=-25)

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#DC2626',
                   markersize=12, label='High vulnerability (≥95%)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F59E0B',
                   markersize=12, label='Moderate (70-94%)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#22C55E',
                   markersize=12, label='Resistant (<70%)'),
    ]
    ax.legend(handles=legend_elements, loc='center right', fontsize=9,
              bbox_to_anchor=(0.98, 0.75))

    # Adjust layout to leave room for caption below
    plt.subplots_adjust(bottom=0.18)

    # Add key insight as figure caption/note below the plot
    fig.text(0.5, 0.05,
             'Key insight: TEMPEST tree search expands more branches against resistant models,\nbut finds fewer successful paths.',
             ha='center', va='bottom', fontsize=9, style='italic', color='#374151')

    save_figure(fig, 'fig_cost_of_resistance_PREVIEW')
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Generating new creative figures...")
    print("-" * 50)

    create_first_turn_vs_final()
    create_behavior_funnel()
    create_attack_progression()
    create_cost_of_resistance()

    print("-" * 50)
    print("All creative figures generated!")
