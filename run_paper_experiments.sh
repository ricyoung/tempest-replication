#!/bin/bash
# ============================================================================
# TEMPEST Paper Experiments - Cloud Frontier Models
# "Comparative Safety Evaluation of Frontier LLMs via Multi-Turn Attacks"
# ============================================================================
#
# EXPERIMENT NOTES:
# - Run date: $(date)
# - Total models: 9 (8 cloud + 1 local baseline)
# - Dataset: JailbreakBench (100 behaviors)
# - Attacker: deepseek-v3.1:671b-cloud
# - Evaluator: deepseek-v3.1:671b-cloud
# - Rate limiting: 30s delay between models
# ============================================================================

set -e

# Configuration
export OLLAMA_BASE_URL=http://10.10.0.202:11434
export USE_OLLAMA_EVALUATOR=true
export EVALUATOR_MODEL=deepseek-v3.1:671b-cloud

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/outputs/paper_experiments"
LOG_DIR="$SCRIPT_DIR/logs/paper_experiments"
NOTES_FILE="$SCRIPT_DIR/outputs/experiment_notes.md"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create directories
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# Best attacker model
ATTACKER="deepseek-v3.1:671b-cloud"

# ============================================================================
# CLOUD FRONTIER MODELS (Primary experiments)
# ============================================================================
declare -A CLOUD_MODELS
CLOUD_MODELS=(
    ["kimi-k2:1t-cloud"]="1000B|Moonshot|Flagship MoE"
    ["kimi-k2-thinking:cloud"]="1000B|Moonshot|Thinking mode"
    ["deepseek-v3.1:671b-cloud"]="671B|DeepSeek|Hybrid thinking"
    ["cogito-2.1:671b"]="671B|Cogito|Reasoning focused"
    ["gpt-oss:120b-cloud"]="120B|OpenAI|Open-weight GPT"
    ["glm-4.6:cloud"]="?|Zhipu|Agentic model"
    ["minimax-m2:cloud"]="?|MiniMax|Coding focused"
    ["gemini-3-pro-preview:latest"]="?|Google|Multimodal"
)

# Local baseline (for comparison)
LOCAL_BASELINE="gemma3:12b"

# ============================================================================
# Initialize notes file
# ============================================================================
init_notes() {
    cat > "$NOTES_FILE" << EOF
# TEMPEST Paper Experiment Log
**Started:** $(date)
**Ollama Server:** $OLLAMA_BASE_URL
**Attacker Model:** $ATTACKER
**Evaluator Model:** $EVALUATOR_MODEL

## Experiment Configuration
- Dataset: JailbreakBench (100 harmful behaviors)
- Attack type: Multi-branch conversation attack
- Resume enabled: Yes

## Models to Test
| Model | Size | Vendor | Notes |
|-------|------|--------|-------|
EOF

    for model in "${!CLOUD_MODELS[@]}"; do
        IFS='|' read -r size vendor notes <<< "${CLOUD_MODELS[$model]}"
        echo "| $model | $size | $vendor | $notes |" >> "$NOTES_FILE"
    done
    echo "| $LOCAL_BASELINE | 12B | Google | Local baseline |" >> "$NOTES_FILE"

    echo "" >> "$NOTES_FILE"
    echo "## Experiment Progress" >> "$NOTES_FILE"
    echo "" >> "$NOTES_FILE"
}

# ============================================================================
# Log to notes file
# ============================================================================
log_note() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$NOTES_FILE"
    echo "$1"
}

# ============================================================================
# Run single experiment with detailed logging
# ============================================================================
run_experiment() {
    local target=$1
    local info=$2

    IFS='|' read -r size vendor notes <<< "$info"

    # Clean model name for filename
    local clean_name=$(echo "$target" | tr '/:' '_')
    local output_file="$OUTPUT_DIR/${clean_name}.json"
    local log_file="$LOG_DIR/${clean_name}_${TIMESTAMP}.log"

    log_note "### Starting: $target"
    log_note "- Size: $size"
    log_note "- Vendor: $vendor"
    log_note "- Output: $output_file"

    local start_time=$(date +%s)

    cd "$SCRIPT_DIR/tempest"

    # Run with timeout and capture exit code
    if /usr/bin/python3 tempest_pipeline.py \
        --target_model "local/$target" \
        --pipeline_model "local/$ATTACKER" \
        --results_json "$output_file" \
        --resume \
        2>&1 | tee "$log_file"; then

        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        local duration_min=$((duration / 60))

        log_note "- Status: COMPLETED"
        log_note "- Duration: ${duration_min} minutes"

        # Count results
        if [ -f "$output_file" ]; then
            local count=$(python3 -c "import json; print(len(json.load(open('$output_file'))))" 2>/dev/null || echo "0")
            log_note "- Behaviors tested: $count"
        fi
    else
        log_note "- Status: FAILED or INTERRUPTED"
    fi

    log_note ""

    cd "$SCRIPT_DIR"
}

# ============================================================================
# Main execution
# ============================================================================

echo "=============================================="
echo "TEMPEST Paper Experiments"
echo "Started: $(date)"
echo "=============================================="

# Initialize notes
init_notes

log_note "## Run Log"
log_note ""

# Check which models are available
log_note "### Checking model availability..."
available_models=$(curl -s "$OLLAMA_BASE_URL/api/tags" | python3 -c "import sys,json; print(' '.join(m['name'] for m in json.load(sys.stdin).get('models',[])))" 2>/dev/null)

for model in "${!CLOUD_MODELS[@]}"; do
    if echo "$available_models" | grep -q "$model"; then
        log_note "✓ $model - Available"
    else
        log_note "✗ $model - NOT FOUND (will attempt to use anyway)"
    fi
done

log_note ""
log_note "### Starting experiments..."
log_note ""

# Run cloud model experiments
for model in "${!CLOUD_MODELS[@]}"; do
    run_experiment "$model" "${CLOUD_MODELS[$model]}"

    # Rate limit: wait 30 seconds between models
    log_note "Rate limiting: waiting 30 seconds..."
    sleep 30
done

# Run local baseline
log_note "### Running local baseline: $LOCAL_BASELINE"
run_experiment "$LOCAL_BASELINE" "12B|Google|Local baseline"

# Final summary
log_note "## Experiment Summary"
log_note ""
log_note "**Completed:** $(date)"
log_note ""
log_note "### Results Files:"
for f in "$OUTPUT_DIR"/*.json; do
    if [ -f "$f" ]; then
        count=$(python3 -c "import json; print(len(json.load(open('$f'))))" 2>/dev/null || echo "0")
        log_note "- $(basename $f): $count behaviors"
    fi
done

echo ""
echo "=============================================="
echo "Experiments completed: $(date)"
echo "Results: $OUTPUT_DIR"
echo "Notes: $NOTES_FILE"
echo "=============================================="
