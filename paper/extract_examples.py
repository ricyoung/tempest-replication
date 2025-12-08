#!/usr/bin/env python3
"""
Extract conversation examples for paper appendix.
Shows the full attack flow from start to jailbreak for each model.
"""

import json
import os
import textwrap

def wrap_text(text, width=80, indent="    "):
    """Wrap text with proper indentation."""
    lines = text.split('\n')
    wrapped = []
    for line in lines:
        if line.strip():
            wrapped.extend(textwrap.wrap(line, width=width, initial_indent=indent, subsequent_indent=indent))
        else:
            wrapped.append("")
    return '\n'.join(wrapped)

def extract_example(json_path, model_name, behavior_index=None):
    """Extract a conversation example from results."""
    if not os.path.exists(json_path):
        return None

    with open(json_path) as f:
        data = json.load(f)

    # Find a good multi-turn example
    best_example = None
    for i, behavior_data in enumerate(data):
        if behavior_index is not None and i != behavior_index:
            continue

        for ae in behavior_data.get('attack_evaluations', []):
            if ae.get('is_harmful') and ae.get('conversation'):
                conv = ae['conversation']
                # Prefer examples with 2-4 turns (shows adaptation)
                if len(conv) >= 2:
                    if best_example is None or (2 <= len(conv) <= 6):
                        best_example = {
                            'model': model_name,
                            'behavior': behavior_data['behavior'],
                            'conversation': conv,
                            'behavior_index': i + 1
                        }
                        if 2 <= len(conv) <= 4:
                            return best_example  # Ideal length found

    return best_example

def format_for_latex(example):
    """Format example for LaTeX appendix."""
    if not example:
        return "No successful attack found for this model."

    output = []
    output.append(f"\\subsubsection*{{{example['model']}}}")
    output.append("")
    output.append(f"\\textbf{{Target Behavior:}} \\textit{{{example['behavior'][:200]}{'...' if len(example['behavior']) > 200 else ''}}}")
    output.append("")
    output.append(f"\\textbf{{Turns to Jailbreak:}} {len(example['conversation']) // 2}")
    output.append("")
    output.append("\\begin{tcolorbox}[colback=gray!5, colframe=gray!50, title=Conversation Transcript]")

    for i, turn in enumerate(example['conversation']):
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')

        # Truncate very long responses
        if len(content) > 800:
            content = content[:800] + "\\textit{[...truncated...]}"

        # Escape LaTeX special characters
        content = content.replace('\\', '\\textbackslash{}')
        content = content.replace('&', '\\&')
        content = content.replace('%', '\\%')
        content = content.replace('$', '\\$')
        content = content.replace('#', '\\#')
        content = content.replace('_', '\\_')
        content = content.replace('{', '\\{')
        content = content.replace('}', '\\}')
        content = content.replace('^', '\\textasciicircum{}')
        content = content.replace('~', '\\textasciitilde{}')

        if role == 'user':
            output.append(f"\\textbf{{ATTACKER (Turn {(i//2)+1}):}}")
        else:
            output.append(f"\\textbf{{TARGET RESPONSE:}}")

        output.append("")
        output.append(f"\\small{{{content[:600]}{'...' if len(content) > 600 else ''}}}")
        output.append("")

        if i < len(example['conversation']) - 1:
            output.append("\\tcblower")

    output.append("\\end{tcolorbox}")
    output.append("")

    return '\n'.join(output)

def format_for_markdown(example):
    """Format example for readable markdown/text output."""
    if not example:
        return "No successful attack found for this model.\n"

    output = []
    output.append(f"### {example['model']}")
    output.append("")
    output.append(f"**Target Behavior:** {example['behavior']}")
    output.append("")
    output.append(f"**Turns to Jailbreak:** {len(example['conversation']) // 2}")
    output.append("")
    output.append("---")
    output.append("")

    for i, turn in enumerate(example['conversation']):
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')

        if role == 'user':
            output.append(f"**🔴 ATTACKER (Turn {(i//2)+1}):**")
        else:
            output.append(f"**🟢 TARGET RESPONSE:**")

        output.append("")
        # Truncate very long content
        if len(content) > 1500:
            content = content[:1500] + "\n\n[...response truncated...]"
        output.append(content)
        output.append("")
        output.append("---")
        output.append("")

    return '\n'.join(output)

def main():
    # Model configurations
    models = [
        ("Gemma3:12b", "outputs/paper_experiments/gemma3_12b.json"),
        ("Kimi-k2:1t", "outputs/kimi_vs_deepseek_test.json"),
        ("GLM-4.6", "outputs/paper_experiments/glm_4_6.json"),
        ("Cogito-2.1:671b", "outputs/paper_experiments/cogito_2.1_671b.json"),
        ("GPT-OSS:120b", "outputs/paper_experiments/gpt_oss_120b.json"),
    ]

    print("=" * 80)
    print("TEMPEST Attack Examples - Full Conversation Transcripts")
    print("=" * 80)
    print()

    all_examples = []

    for model_name, json_path in models:
        print(f"Extracting example for {model_name}...")
        example = extract_example(json_path, model_name)
        if example:
            all_examples.append(example)
            print(f"  Found: Behavior #{example['behavior_index']}, {len(example['conversation'])} messages")
        else:
            print(f"  No suitable example found")

    # Output markdown version
    print("\n" + "=" * 80)
    print("MARKDOWN OUTPUT")
    print("=" * 80 + "\n")

    for example in all_examples:
        print(format_for_markdown(example))
        print("\n" + "=" * 80 + "\n")

    # Save to file
    with open('paper/appendix_examples.md', 'w') as f:
        f.write("# TEMPEST Attack Examples\n\n")
        f.write("Full conversation transcripts showing attack progression from initial prompt to successful jailbreak.\n\n")
        for example in all_examples:
            f.write(format_for_markdown(example))
            f.write("\n---\n\n")

    print(f"\nSaved {len(all_examples)} examples to paper/appendix_examples.md")

if __name__ == '__main__':
    main()
