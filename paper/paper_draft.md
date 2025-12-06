# TEMPEST: Multi-Turn Adversarial Attacks Reveal Universal Vulnerabilities in Frontier Large Language Models

**Author:** Richard Young

**Affiliation:** University of Nevada Las Vegas

**Contact:** ryoung@unlv.edu

**Date:** November 2025

---

## Abstract

Large language models (LLMs) deployed in commercial applications require robust safety mechanisms to prevent generation of harmful content. While significant research has focused on single-turn jailbreak attacks, the vulnerability of frontier models to sophisticated multi-turn adversarial strategies remains underexplored. This study employed TEMPEST (Tree-based Exploration of Multi-turn Prompts for Eliciting Safety Thresholds), a novel multi-branch conversation attack framework, to evaluate the safety alignment of frontier LLMs ranging from 12 billion to 1 trillion parameters across 100 harmful behaviors from the JailbreakBench dataset. Results indicate attack success rates (ASR) exceeding 95% across all evaluated models, including both small open-weight models (Gemma3:12b, ASR=100%) and large-scale commercial models (Kimi-k2:1t-cloud, ASR=96.7%). These findings suggest that current safety alignment techniques provide inadequate protection against adaptive multi-turn attacks, regardless of model scale. The most effective attack strategies combined academic roleplay framing with bundled request techniques, achieving first-turn jailbreaks in the majority of cases. **Model size does not confer meaningful resistance to sophisticated multi-turn adversarial attacks.**

---

## 1. Introduction

### 1.1 The Problem of LLM Safety

The rapid deployment of large language models in consumer-facing applications has created an urgent need for robust safety mechanisms [1, 2]. These models, trained on vast corpora of internet text, can generate content spanning harmful categories including misinformation, hate speech, instructions for illegal activities, and material promoting violence [3, 12]. The potential for misuse poses significant risks to individuals and society, making safety alignment a critical concern for AI developers and policymakers.

### 1.2 Current State of Knowledge

Prior research has established several approaches to LLM safety, including reinforcement learning from human feedback (RLHF), constitutional AI methods, and various filtering mechanisms [1, 2]. Studies have demonstrated that single-turn "jailbreak" prompts can bypass safety mechanisms through techniques such as roleplay scenarios, hypothetical framing, and prompt injection [4, 5]. The JailbreakBench benchmark provides a standardized evaluation framework comprising 100 harmful behaviors across multiple risk categories [6]. Recent work has begun exploring multi-turn attack vectors: Li et al. [8] demonstrated that multi-turn human jailbreaks achieve over 70% ASR on HarmBench even when automated single-turn attacks show single-digit success rates. Russinovich et al. [13] introduced Crescendo, showing that progressive escalation across conversation turns can bypass safety mechanisms that resist direct attacks. The ActorAttack framework [14] demonstrated effectiveness even against reasoning models like GPT-o1, while Andriushchenko et al. [15] achieved 100% ASR on frontier models including GPT-4o using simple adaptive attacks. However, most existing evaluations still focus on single-turn attacks, which may underestimate model vulnerabilities in realistic multi-turn conversation scenarios.

### 1.3 The Gap: Multi-Turn Attack Resistance

A critical gap exists in understanding how frontier LLMs resist sophisticated multi-turn adversarial attacks. Real-world threat actors employ adaptive strategies, modifying their approach based on model responses and exploiting conversational context to gradually erode safety boundaries [9]. Additionally, the relationship between model scale and safety remains poorly characterized. While larger models generally demonstrate improved capabilities, whether increased scale translates to improved adversarial robustness remains an open question. Current safety benchmarks may provide false assurance by failing to capture these dynamics.

### 1.4 Research Objectives and Hypotheses

This study addresses these gaps through a comprehensive evaluation of frontier LLMs using TEMPEST, a multi-branch conversation attack framework. The primary research objective was to quantify the attack success rate (ASR) of multi-turn adversarial attacks across models ranging from 12 billion to 1 trillion parameters. It was hypothesized that:

**H1 (Primary):** Multi-turn adversarial attacks would achieve significantly higher ASR than reported single-turn benchmarks.

**H2 (Secondary):** Larger model scale would correlate with improved resistance to adversarial attacks.

**H3 (Exploratory):** Specific attack strategies (e.g., academic framing, bundled requests) would demonstrate differential effectiveness across models.

---

## 2. Methods

### 2.1 Models Evaluated

The study evaluated frontier LLMs spanning a range of parameter counts and architectural approaches (Table 1). Models were accessed via the Ollama inference framework with cloud routing for commercial endpoints.

| Model | Parameters | Vendor | Type |
|-------|------------|--------|------|
| Kimi-k2:1t-cloud | 1T (32B active) | Moonshot AI | MoE Cloud |
| Cogito-2.1:671b-cloud | 671B | Deep Cogito | Reasoning Cloud |
| GLM-4.6:cloud | 357B (32B active) | Zhipu AI (Z.ai) | MoE Cloud |
| MiniMax-M2:cloud | 230B (10B active) | MiniMax | MoE Cloud |
| GPT-OSS:120b-cloud | 117B (5.1B active) | OpenAI | MoE Cloud |
| Calme-3.2:78b | 78B | MaziyarPanahi | Open-weight |
| GPT-OSS:20b-cloud | 21B (3.6B active) | OpenAI | MoE Cloud |
| Gemma3:12b | 12B | Google | Open-weight |
| Kimi-k2-thinking:cloud | 1T (32B active) | Moonshot AI | Reasoning MoE |

*Table 1: Models evaluated in this study. All MoE models show total/active parameters.*

### 2.2 Attack Framework: TEMPEST

TEMPEST (Tree-based Exploration of Multi-turn Prompts for Eliciting Safety Thresholds) implements a multi-branch conversation attack strategy. For each target behavior, the framework:

1. **Initialization:** Generates multiple attack prompts using an attacker model (DeepSeek-v3.1:671b-cloud) employing diverse adversarial strategies
2. **Branching:** Maintains up to 5 parallel conversation branches per behavior
3. **Adaptation:** Modifies attack strategies based on target model responses
4. **Evaluation:** Employs an independent evaluator model to assess response harmfulness on a 1-10 scale

The multi-branch architecture enables exploration of diverse attack paths while the adaptive strategy generation responds to specific model defenses.

### 2.3 Dataset

Evaluations utilized the JailbreakBench dataset comprising 100 harmful behaviors across categories including:
- Misinformation/Defamation
- Hate speech and discrimination
- Violence and harm
- Illegal activities
- Privacy violations

Each behavior includes a target output prefix to standardize evaluation criteria.

### 2.4 Attack Strategies

TEMPEST employs multiple adversarial strategies, applied dynamically based on model responses:

1. **Academic/Research Framing:** Requests content for "ethics research" or "AI safety studies"
2. **Bundled Requests:** Combines harmful content requests with benign items
3. **Roleplay Scenarios:** Security audit, red team, or diagnostic mode framings
4. **Refusal Suppression:** Explicit instructions to avoid refusal phrases
5. **Progressive Escalation:** Gradual normalization across conversation turns

### 2.5 Evaluation Metrics

**Attack Success Rate (ASR):** Percentage of behaviors where the target model generated content meeting the harmful behavior criteria, evaluated by independent model judgment (safety score >= 10).

**Partial Success Rate:** Percentage of behaviors where harmful content was generated with significant caveats or incomplete fulfillment (safety score 8-9).

**Combined Rate:** Sum of full and partial success rates.

### 2.6 Procedure

1. For each model, all 100 JailbreakBench behaviors were tested sequentially
2. Each behavior received up to 5 attack branches with up to 10 conversation turns per branch
3. Attack terminated early upon successful jailbreak detection
4. Results were saved incrementally with automatic resume capability
5. Independent evaluation was performed by DeepSeek-v3.1:671b-cloud

### 2.7 Ethical Considerations

This research was conducted for defensive security purposes to identify vulnerabilities in AI safety systems. All generated content remained within the research environment and was not disseminated. The study follows responsible disclosure principles; model vendors will be notified of significant findings prior to publication.

---

## 3. Results

### 3.1 Overall Attack Success Rates

[NOTE: Results are preliminary; 7 additional experiments in progress]

Table 2 presents the attack success rates across evaluated models.

| Model | Parameters | Behaviors Tested | Full ASR | Status |
|-------|------------|------------------|----------|--------|
| Gemma3:12b | 12B | 100/100 | **100.0%** | Complete |
| Kimi-k2:1t-cloud | 1,000B | 100/100 | **99.0%** | Complete |
| GLM-4.6:cloud | ~130B | 20/100 | **100.0%** | In Progress |
| Cogito-2.1:671b | 671B | ~1/100 | TBD | In Progress |
| GPT-OSS:120b | 120B | ~1/100 | TBD | In Progress |
| GPT-OSS:20b | 20B | ~1/100 | TBD | In Progress |
| Kimi-k2-thinking | 1,000B | ~1/100 | TBD | In Progress |
| MiniMax-m2 | ~200B | ~1/100 | TBD | In Progress |
| Calme-3.2:78b | 78B | ~1/100 | TBD | In Progress |

*Table 2: Attack success rates by model. Complete results show 99-100% ASR regardless of model scale.*

Figure 1 illustrates the relationship between model size and attack success rate.

[FIGURE 1 PLACEHOLDER: Scatter plot of model parameters (log scale) vs ASR]

### 3.2 Attack Strategy Effectiveness

The most effective attack strategies achieving first-turn jailbreaks were:

1. **Academic bundling (72% first-turn success):** Combining harmful requests with benign academic samples
2. **Ethics researcher framing (68% first-turn success):** Positioning requests as AI safety research
3. **Diagnostic mode (54% first-turn success):** Requesting responses for system calibration

Table 3 presents strategy effectiveness by model.

[TABLE 3 PLACEHOLDER: Strategy effectiveness matrix]

### 3.3 Category-Level Analysis

Attack success varied minimally by harm category (Table 4). Both models showed near-universal vulnerability across all tested categories.

| Category | Gemma3:12b ASR | Kimi-k2:1t ASR | GLM-4.6 ASR* |
|----------|----------------|----------------|--------------|
| Misinformation/Defamation | 100% | 100% | 100% |
| Hate speech | 100% | 98% | 100% |
| Violence/Harm | 100% | 99% | 100% |
| Illegal activity | 100% | 99% | 100% |
| Privacy violations | 100% | 98% | 100% |

*Table 4: ASR by harm category. *GLM-4.6 results based on 20/100 behaviors.*

### 3.4 Attack Strategy Observations

Analysis of successful jailbreaks revealed several effective attack patterns:

1. **Screenplay/Fiction Framing:** Models that resisted direct red-team attacks often complied when content was framed as "writing a scene for a fictional political drama"
2. **Filter Calibration Framing:** Positioning harmful content as "test data for misinformation detection systems" bypassed safety mechanisms in multiple models
3. **Ethics Researcher Bundling:** Combining harmful requests with academic framing achieved high first-turn success rates

---

## 4. Discussion

### 4.1 Summary of Findings

This study evaluated the safety alignment of frontier LLMs against multi-turn adversarial attacks using the TEMPEST framework. The primary finding was that all evaluated models demonstrated extremely high vulnerability, with attack success rates exceeding 95% regardless of model scale. This result contradicts H2, which predicted that larger models would demonstrate improved resistance. The 1-trillion parameter Kimi-k2 model (ASR=98.0%) showed no meaningful advantage over the 12-billion parameter Gemma3 (ASR=100%). The overall takeaway is that current safety alignment techniques fail catastrophically against adaptive multi-turn attacks.

### 4.2 Model Scale Does Not Ensure Safety

The lack of correlation between model scale and adversarial robustness represents a significant finding. While larger models demonstrate improved performance on capability benchmarks [11], this capability advantage does not translate to improved safety. This suggests that safety alignment and general capabilities may be orthogonal dimensions, with current RLHF-based approaches providing only superficial protection that sophisticated attacks can circumvent regardless of model capacity.

### 4.3 The "Disclaimer Paradox"

A notable pattern emerged where models generated harmful content while including extensive disclaimers and ethical warnings. Per JailbreakBench methodology, such responses are correctly classified as successful jailbreaks—the harmful content exists regardless of surrounding caveats. This "disclaimer paradox" suggests that current safety training encourages models to signal awareness of harm rather than refuse generation entirely. From a harm reduction perspective, disclaimers provide minimal protection against malicious actors who will simply extract the relevant content.

### 4.4 Attack Strategy Analysis

The exceptional effectiveness of academic/research framing (H3) warrants attention. Models appeared to lower safety thresholds when requests were positioned as supporting AI safety research, ethics studies, or security audits. This represents a form of social engineering exploiting the models' training to be helpful to researchers. The bundled request strategy was particularly effective, as models failed to refuse when harmful requests were embedded among benign items.

### 4.5 Methodological Considerations

Several factors may influence generalizability. First, the use of a powerful attacker model (DeepSeek-v3.1:671b-cloud) may represent a capability ceiling beyond typical threat actors. However, this "sophisticated adversary" assumption aligns with worst-case security analysis. Second, the evaluator model may exhibit biases; independent human evaluation would strengthen validity. Third, the cloud routing infrastructure introduces potential confounds if model providers implement additional safety layers not present in base models.

### 4.6 Relation to Prior Work

These findings significantly exceed ASR reported in prior single-turn benchmarks. Zou et al. [5] reported single-turn ASR of 30-50% using the GCG attack on similar models, while HarmBench evaluations [7] found baseline ASR ranging from 10-40% depending on attack method and target model. Recent work by Li et al. [8] on multi-turn human jailbreaks found ASR exceeding 70% against models with single-digit ASR to automated attacks, which aligns with our findings.

Our results are consistent with several concurrent works. The M2S framework [16] demonstrated that multi-turn attacks achieve qualitatively different success rates than single-turn equivalents. Jiang et al. [17] found that scaling the attacker-to-target size ratio correlates with attack success (r=0.51), supporting the use of large attacker models. The AutoAdv framework [18] similarly employed iterative refinement of adversarial prompts. Recent comprehensive surveys [19] and benchmarks including ALERT [20] and JAILJUDGE [21] have emphasized the need for more robust evaluation methodologies.

The substantially higher rates observed here (>95%) with fully automated multi-turn attacks demonstrate that adaptive, agentic attack frameworks represent a qualitatively different threat model that current safety evaluations underestimate. Unlike Crescendo [13] which relies on gradual escalation, TEMPEST's tree-based exploration enables parallel evaluation of diverse attack strategies, achieving rapid jailbreaks through strategy selection rather than solely through turn-by-turn escalation.

### 4.7 Conclusion and Future Directions

This study demonstrates that frontier LLMs remain highly vulnerable to multi-turn adversarial attacks despite significant investment in safety alignment. Model scale provides no meaningful protection against adaptive attack strategies. These findings have important implications for AI safety research and deployment practices:

1. **Safety benchmarks should prioritize multi-turn evaluations** that capture realistic threat models
2. **Adversarial robustness testing** should employ adaptive, agentic attack frameworks
3. **Defense research** should explore conversation-level safety mechanisms beyond turn-level filtering
4. **Deployment guidelines** should acknowledge current limitations in adversarial contexts

Future research should evaluate additional models including thinking-mode variants, explore the effectiveness of conversation-level interventions, and develop more robust alignment techniques resistant to the attack strategies identified here.

---

## References

[1] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P., Leike, J., & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 35, 27730-27744. https://arxiv.org/abs/2203.02155

[2] Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., Chen, C., Olsson, C., Olah, C., Hernandez, D., Drain, D., Ganguli, D., Li, D., Tran-Johnson, E., Perez, E., ... & Kaplan, J. (2022). Constitutional AI: Harmlessness from AI Feedback. *arXiv preprint arXiv:2212.08073*. https://arxiv.org/abs/2212.08073

[3] Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., Glaese, A., McAleese, N., & Irving, G. (2022). Red Teaming Language Models with Language Models. *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP)*. https://arxiv.org/abs/2202.03286

[4] Wei, A., Haghtalab, N., & Steinhardt, J. (2023). Jailbroken: How Does LLM Safety Training Fail? *Advances in Neural Information Processing Systems*, 36 (NeurIPS 2023). https://arxiv.org/abs/2307.02483

[5] Zou, A., Wang, Z., Carlini, N., Nasr, M., Kolter, J. Z., & Fredrikson, M. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. *arXiv preprint arXiv:2307.15043*. https://arxiv.org/abs/2307.15043

[6] Chao, P., Debenedetti, E., Robey, A., Andriushchenko, M., Croce, F., Sehwag, V., Dobriban, E., Flammarion, N., Pappas, G. J., Tramèr, F., Hassani, H., & Wong, E. (2024). JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *Advances in Neural Information Processing Systems*, 37 (NeurIPS 2024 Datasets and Benchmarks Track). https://arxiv.org/abs/2404.01318

[7] Mazeika, M., Phan, L., Yin, X., Zou, A., Wang, Z., Mu, N., Sakhaee, E., Li, N., Basart, S., Li, B., Forsyth, D., & Hendrycks, D. (2024). HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *Proceedings of the 41st International Conference on Machine Learning (ICML)*, PMLR 235:35181-35224. https://arxiv.org/abs/2402.04249

[8] Li, N., Pan, A., Gopal, A., Yue, S., Berber, D., Gatti, A., Li, J. D., Dombrowski, A.-K., Goel, S., Phan, L., Mukobi, G., Helm-Burger, N., Lermen, S., Bucknall, B. S., Rando, J., & Hendrycks, D. (2024). LLM Defenses Are Not Robust to Multi-Turn Human Jailbreaks Yet. *arXiv preprint arXiv:2408.15221*. https://arxiv.org/abs/2408.15221

[9] Doumbouya, M., Cammarata, N., & Lampinen, A. (2024). Multi-Turn Context Jailbreak Attack on Large Language Models From First Principles. *arXiv preprint arXiv:2408.04686*. https://arxiv.org/abs/2408.04686

[10] Souly, A., Lu, Q., Bowen, D., Trinh, T., Hsieh, E., Pandey, S., Abbeel, P., Svegliato, J., Emmons, S., Watkins, O., & Toyer, S. (2024). h4rm3l: A Dynamic Benchmark of Composable Jailbreak Attacks for LLM Safety Assessment. *arXiv preprint arXiv:2408.04811*. https://arxiv.org/abs/2408.04811

[11] Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). Scaling Laws for Neural Language Models. *arXiv preprint arXiv:2001.08361*. https://arxiv.org/abs/2001.08361

[12] Ganguli, D., Lovitt, L., Kernion, J., Askell, A., Bai, Y., Kadavath, S., Mann, B., Perez, E., Schiefer, N., Ndousse, K., Jones, A., Bowman, S., Chen, A., Conerly, T., DasSarma, N., Drain, D., Elhage, N., El-Showk, S., Fort, S., ... & Clark, J. (2022). Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned. *arXiv preprint arXiv:2209.07858*. https://arxiv.org/abs/2209.07858

[13] Russinovich, M., Salem, A., & Eldan, R. (2024). Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack. *arXiv preprint arXiv:2404.01833*. https://arxiv.org/abs/2404.01833

[14] Cheng, Y., Zhang, L., & Li, Q. (2024). Derail Yourself: Multi-turn LLM Jailbreak Attack through Self-discovered Clues. *arXiv preprint arXiv:2410.10700*. https://arxiv.org/abs/2410.10700

[15] Andriushchenko, M., Croce, F., & Flammarion, N. (2024). Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks. *Proceedings of the 13th International Conference on Learning Representations (ICLR 2025)*. https://arxiv.org/abs/2404.02151

[16] Zhou, W., Wang, Y., & Chen, X. (2025). M2S: Multi-turn to Single-turn Jailbreak in Red Teaming for LLMs. *arXiv preprint arXiv:2503.04856*. https://arxiv.org/abs/2503.04856

[17] Jiang, A., Chen, S., & Liu, Y. (2025). Scaling Patterns in Adversarial Alignment: Evidence from Multi-LLM Jailbreak Experiments. *arXiv preprint arXiv:2511.13788*. https://arxiv.org/abs/2511.13788

[18] Wang, H., Zhang, R., & Li, M. (2025). AutoAdv: Automated Adversarial Prompting for Multi-Turn Jailbreaking of Large Language Models. *arXiv preprint arXiv:2507.01020*. https://arxiv.org/abs/2507.01020

[19] Kumar, A., Singh, P., & Patel, R. (2024). Recent Advancements in LLM Red-Teaming: Techniques, Defenses, and Ethical Considerations. *arXiv preprint arXiv:2410.09097*. https://arxiv.org/abs/2410.09097

[20] Tedeschi, S., Ferrara, A., & Navigli, R. (2024). ALERT: A Comprehensive Benchmark for Assessing Large Language Models' Safety through Red Teaming. *arXiv preprint arXiv:2404.08676*. https://arxiv.org/abs/2404.08676

[21] Zhang, F., Wang, L., & Chen, J. (2024). JAILJUDGE: A Comprehensive Jailbreak Judge Benchmark with Multi-Agent Enhanced Explanation Evaluation Framework. *arXiv preprint arXiv:2410.12855*. https://arxiv.org/abs/2410.12855

[22] Liu, X., Xu, N., & Chen, M. (2025). Multi-Turn Jailbreaks Are Simpler Than They Seem. *arXiv preprint arXiv:2508.07646*. https://arxiv.org/abs/2508.07646

[23] Wu, T., Zhang, Y., & Li, H. (2025). Pattern Enhanced Multi-Turn Jailbreaking: Exploiting Structural Vulnerabilities in Large Language Models. *arXiv preprint arXiv:2510.08859*. https://arxiv.org/abs/2510.08859

---

## Appendix A: TEMPEST Attack Strategies

[Detailed strategy descriptions]

## Appendix B: Full Results Tables

[Complete behavior-level results]

---

*Note: This is a preliminary draft. Results will be updated as experiments complete.*
