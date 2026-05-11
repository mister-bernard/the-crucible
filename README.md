# The Crucible — Adversarial Debate Engine

A multi-agent debate system that pits AI models against each other to stress-test ideas, research topics, and surface insights that no single model would produce alone.

Three roles. One transcript. No punches pulled.

```
┌──────────────────────────────────────────┐
│           The Crucible                    │
│                                          │
│  🔴 Adversary — tears it apart           │
│  🔵 Researcher — defends with evidence   │
│  🟡 Strategist — synthesizes the truth   │
│                                          │
│  Local models via Ollama, $0 compute     │
│  8 hours of autonomous debate            │
│  Hundreds of rounds, real signal out      │
└──────────────────────────────────────────┘
```

## What It Does

You give it a topic. It spawns 3 AI agents with different model families (for genuine reasoning diversity), and they debate for hours. The Adversary attacks, the Researcher defends with evidence, and the Strategist synthesizes a final verdict.

The output: a deep analysis that's been stress-tested from every angle.

## Two Modes

| Mode | Runtime | Cost | Output |
|------|---------|------|--------|
| **Long Run** | 8 hours, local Ollama models | $0 | Deep synthesis report |
| **Short Run** | 5-10 min, cloud models | $0.30-1.00 | Quick adversarial analysis |

## Requirements

### For Local (Long Run) Debates
- **Ollama** — https://ollama.com
- **32GB+ RAM** (64GB recommended)
- **GPU optional** — Apple Silicon unified memory or NVIDIA GPU helps, but CPU works (slower)
- **Python 3.9+** with `requests`

### For Cloud (Short Run) Debates
- **OpenClaw** — https://github.com/openclaw/openclaw
- API key for your preferred provider (Anthropic, OpenAI, etc.)

## Quick Start (Local)

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull Models

**Recommended trio** (fits in 64GB RAM):
```bash
ollama pull qwen2.5:32b          # 19.9GB — analytical, data-driven
ollama pull nous-hermes2-mixtral  # 26.4GB — creative, broad reasoning
ollama pull qwen3:8b             # 5.2GB  — concise synthesis
```

**Budget trio** (fits in 32GB RAM):
```bash
ollama pull qwen3:8b             # 5.2GB
ollama pull mistral:7b           # 4.1GB
ollama pull phi3:14b             # 7.9GB
```

> ⚠️ **Critical:** 8B+ minimum for ALL roles. Sub-7B models produce empty or incoherent output. Learned the hard way.

### 3. Run a Debate

```bash
python3 scripts/generate-debate.py "Should cities ban cars from downtown areas?" \
  --models qwen2.5:32b,nous-hermes2-mixtral,qwen3:8b \
  --duration 8 \
  --output my-debate/

cd my-debate/
nohup python3 debate.py > debate.log 2>&1 &
tail -f debate.log
```

### 4. Read the Results

After completion:
- `transcript.txt` — full debate (every round)
- `final_positions/` — each agent's final position paper
- `checkpoints/` — crash recovery snapshots (every 50 rounds)

## Architecture

### Why 3 Roles?

Two-agent debates stalemate. Four+ get noisy. Three creates a triangle dynamic:

- **Adversary** — Devil's advocate. Finds every flaw, blind spot, and hidden assumption. Never fully concedes.
- **Researcher** — Evidence-driven defender. Uses data, citations, and research. Steelmans the adversary before responding.
- **Strategist** — The judge. Scores each round, identifies cruxes, steelmans both sides, delivers an opinionated verdict.

### Why Different Model Families?

Same-family models = echo chamber. Different families (Qwen vs Mistral vs Llama) = genuine reasoning diversity from different training data and biases.

### Debate Structure

- **12-15 structured topics** prevent circular arguments
- **400-600 word responses** — substance without bloat
- **Temperature 0.8** — creativity without incoherence
- **Checkpoints every 50 rounds** — crash recovery
- **2-second pause between rounds** — prevents Ollama overload

## Hardware Guide

| Setup | Can Run | Speed vs M4 Pro |
|-------|---------|-----------------|
| Mac M4 Pro 64GB | 2×32B + 1×8B | Reference |
| Linux + RTX 3080 (10GB) + 64GB RAM | 1×14B on GPU + 32B on CPU | ~2-3× slower |
| Linux + RTX 4090 (24GB) + 64GB RAM | 1×32B on GPU + others on CPU | ~1.5× slower |
| Mac M1 Pro 32GB | 3×8B or 1×14B + 2×8B | ~2× slower |
| CPU only, 64GB RAM | 2×32B (slow) | ~5-10× slower |

## Model Recommendations

### Proven Trios
| Trio | Total Size | Notes |
|------|-----------|-------|
| qwen2.5:32b + nous-hermes2-mixtral + qwen3:8b | ~51GB | Standard, battle-tested |
| qwen2.5:32b + dolphin-mixtral + qwen3:8b | ~51GB | Good alternative |
| qwen3:8b + mistral:7b + phi3:14b | ~17GB | Budget for 32GB machines |

### What NOT to Use
- **Anything under 7B params** — can't maintain coherent multi-turn arguments
- **llama3.1:70b in multi-model** — 42.5GB, eats all RAM. Solo only.

## Lessons Learned

1. **32B+ recommended** for all roles. Small models can't debate.
2. **Different model families** > same-family variants.
3. **Long debates (8h) >> short (1h)** — real signal comes in hours 4-8.
4. **Checkpoints save you.** Hardware crashes happen.
5. **The Strategist must pick a side.** "Both sides have merit" is not a conclusion.

## License

MIT

## Credits

Built by Mr. Bernard. Battle-tested over multi-hour debates with three local Ollama models.
