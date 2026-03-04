# The Crucible — Full Documentation

See README.md for quick start. This file contains the complete technical reference.

## Debate Script Template

The `generate-debate.py` script creates a self-contained `debate.py` with:
- 3 personas with different models and system prompts
- 12-15 structured topics that progress from broad to specific
- Automatic checkpoints every 50 rounds
- Final position papers at completion
- Crash recovery from checkpoints

## Role Design

### Adversary
- Attacks arguments, not arguers
- Specific objections with scenarios and counterexamples
- Escalates across rounds (surface → structural → systemic)
- NEVER fully concedes — tactical retreat only
- One challenge per turn, 2-4 paragraphs

### Researcher
- Leads with evidence (data, research, case studies)
- Steelmans adversary's argument before responding
- Distinguishes certainty levels explicitly
- Minimal concessions — never concedes core thesis
- One response per turn, 3-5 paragraphs

### Strategist
- Identifies 3-5 cruxes (core disagreements)
- Scores each round (adversary vs researcher)
- Steelmans BOTH sides
- Must pick a side — no "both sides have merit" cop-outs
- Delivers actionable verdict with confidence level

## Cross-Provider Diversity

Best debates use different model FAMILIES:
- Local: Qwen vs Mistral vs Llama
- Cloud: Claude vs GPT vs Gemini

Same-family models share training biases → echo chamber.

## Post-Debate Synthesis

After a long debate completes, you'll want a synthesis. Options:
1. Feed the transcript + final positions to a strong cloud model (Claude Opus, GPT-4, etc.)
2. Use the Strategist's final position as the synthesis
3. Use OpenClaw to spawn a synthesis agent that reads all outputs

The synthesis should include:
- Executive Summary
- Key Arguments by Position (with quotes from transcript)
- Points of Convergence
- Unresolved Tensions
- Novel Insights
- Verdict
