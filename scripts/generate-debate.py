#!/usr/bin/env python3
"""Generate a Crucible debate script for a given topic.

Usage:
    python3 generate-debate.py "Your debate topic" \
        --models qwen2.5:32b,nous-hermes2-mixtral,qwen3:8b \
        --duration 8 \
        --output ./my-debate/
"""

import argparse
import os
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "prompts")


def load_prompt(role: str) -> str:
    path = os.path.join(PROMPTS_DIR, f"{role}.md")
    with open(path) as f:
        return f.read()


def generate_debate_script(topic: str, models: list[str], duration_hours: int) -> str:
    adversary_prompt = load_prompt("adversary").replace('"""', '\\"\\"\\"')
    researcher_prompt = load_prompt("researcher").replace('"""', '\\"\\"\\"')
    strategist_prompt = load_prompt("strategist").replace('"""', '\\"\\"\\"')

    return textwrap.dedent(f'''\
#!/usr/bin/env python3
"""
The Crucible — Adversarial Debate
Topic: {topic}
Models: {', '.join(models)}
Duration: {duration_hours} hours
"""

import json
import os
import time
import datetime
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DURATION_HOURS = {duration_hours}
CHECKPOINT_INTERVAL = 50  # rounds between checkpoints

PERSONAS = {{
    "Adversary": {{
        "model": "{models[0]}",
        "system": """{adversary_prompt}""",
        "color": "\\033[91m",  # red
    }},
    "Researcher": {{
        "model": "{models[1]}",
        "system": """{researcher_prompt}""",
        "color": "\\033[94m",  # blue
    }},
    "Strategist": {{
        "model": "{models[2]}",
        "system": """{strategist_prompt}""",
        "color": "\\033[93m",  # yellow
    }},
}}

TOPICS = [
    "Opening positions: What is your initial stance on: {topic}",
    "Historical context: What precedents or historical parallels inform this debate?",
    "Core assumptions: What hidden assumptions underlie each position?",
    "Economic implications: What are the financial and economic consequences?",
    "Second-order effects: What indirect consequences are being overlooked?",
    "Risk analysis: What are the worst-case scenarios?",
    "Stakeholder impact: Who benefits and who loses?",
    "Implementation challenges: What practical barriers exist?",
    "Counter-examples: What evidence contradicts each position?",
    "Technological factors: How does technology change the calculus?",
    "Ethical dimensions: What moral considerations apply?",
    "Long-term trajectory: What does this look like in 10-20 years?",
    "Synthesis: Given everything discussed, what is the strongest position?",
    "Final position papers: State your definitive position with supporting evidence.",
]

RESET = "\\033[0m"


def ollama_chat(model: str, system: str, messages: list[dict], temperature: float = 0.8) -> str:
    """Send a chat request to Ollama."""
    resp = requests.post(
        f"{{OLLAMA_URL}}/api/chat",
        json={{
            "model": model,
            "messages": [{{"role": "system", "content": system}}] + messages,
            "stream": False,
            "options": {{"temperature": temperature, "num_predict": 800}},
        }},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def save_checkpoint(transcript: str, round_num: int, output_dir: str):
    """Save a checkpoint of the debate."""
    os.makedirs(os.path.join(output_dir, "checkpoints"), exist_ok=True)
    path = os.path.join(output_dir, "checkpoints", f"checkpoint-round-{{round_num}}.txt")
    with open(path, "w") as f:
        f.write(transcript)
    print(f"  💾 Checkpoint saved: round {{round_num}}")


def run_debate():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    transcript_path = os.path.join(output_dir, "transcript.txt")
    os.makedirs(os.path.join(output_dir, "final_positions"), exist_ok=True)

    start_time = time.time()
    end_time = start_time + (DURATION_HOURS * 3600)
    transcript = f"# Crucible Debate: {topic}\\n"
    transcript += f"Started: {{datetime.datetime.utcnow().isoformat()}}Z\\n"
    transcript += f"Models: {{', '.join(p['model'] for p in PERSONAS.values())}}\\n\\n"

    round_num = 0
    topic_idx = 0

    print(f"🔥 The Crucible — {{DURATION_HOURS}}h debate starting")
    print(f"   Topic: {topic}")
    print(f"   Models: {{', '.join(p['model'] for p in PERSONAS.values())}}")
    print()

    while time.time() < end_time:
        current_topic = TOPICS[topic_idx % len(TOPICS)]
        topic_idx += 1
        transcript += f"\\n{'='*60}\\n"
        transcript += f"## Topic {{topic_idx}}: {{current_topic}}\\n"
        transcript += f"{'='*60}\\n\\n"

        for role_name, persona in PERSONAS.items():
            if role_name == "Strategist" and topic_idx < len(TOPICS):
                continue  # Strategist only speaks on synthesis topics

            round_num += 1
            elapsed_h = (time.time() - start_time) / 3600
            remaining_h = max(0, (end_time - time.time()) / 3600)
            print(f"  {{persona['color']}}[Round {{round_num}}] {{role_name}} ({{persona['model']}}) — "
                  f"{{elapsed_h:.1f}}h elapsed, {{remaining_h:.1f}}h remaining{{RESET}}")

            messages = [
                {{"role": "user", "content": f"TOPIC: {topic}\\n\\nCURRENT DISCUSSION: {{current_topic}}\\n\\n"
                 f"TRANSCRIPT SO FAR:\\n{{transcript[-8000:]}}\\n\\n"
                 f"Write your Round {{round_num}} contribution. Stay in character."}}
            ]

            try:
                response = ollama_chat(persona["model"], persona["system"], messages)
                transcript += f"### {{role_name}} ({{persona['model']}}) — Round {{round_num}}\\n\\n"
                transcript += response + "\\n\\n"
                print(f"    ✅ {{len(response)}} chars")
            except Exception as e:
                print(f"    ❌ Error: {{e}}")
                transcript += f"### {{role_name}} — Round {{round_num}} [ERROR: {{e}}]\\n\\n"

            # Save transcript after every round
            with open(transcript_path, "w") as f:
                f.write(transcript)

            if round_num % CHECKPOINT_INTERVAL == 0:
                save_checkpoint(transcript, round_num, output_dir)

            time.sleep(2)  # prevent Ollama overload

            if time.time() >= end_time:
                break

    # Final position papers
    print("\\n📝 Generating final position papers...")
    for role_name, persona in PERSONAS.items():
        print(f"  {{persona['color']}}{{role_name}} writing final position...{{RESET}}")
        messages = [
            {{"role": "user", "content": f"TOPIC: {topic}\\n\\n"
             f"FULL TRANSCRIPT:\\n{{transcript[-12000:]}}\\n\\n"
             f"The debate is over. Write your FINAL POSITION PAPER (800-1200 words). "
             f"Summarize your strongest arguments, acknowledge what you concede, "
             f"and state your definitive conclusion."}}
        ]
        try:
            response = ollama_chat(persona["model"], persona["system"], messages, temperature=0.6)
            # Save individual position
            pos_path = os.path.join(output_dir, "final_positions", f"{{role_name.lower()}}.md")
            with open(pos_path, "w") as f:
                f.write(f"# Final Position: {{role_name}}\\n\\n{{response}}")
            transcript += f"\\n## Final Position: {{role_name}}\\n\\n{{response}}\\n"
            print(f"    ✅ {{len(response)}} chars")
        except Exception as e:
            print(f"    ❌ Error: {{e}}")

    # Save final transcript
    with open(transcript_path, "w") as f:
        f.write(transcript)

    elapsed = (time.time() - start_time) / 3600
    print(f"\\n🏁 Debate complete! {{round_num}} rounds in {{elapsed:.1f}} hours")
    print(f"   Transcript: {{transcript_path}}")
    print(f"   Final positions: {{os.path.join(output_dir, 'final_positions')}}/")


if __name__ == "__main__":
    run_debate()
''')


def main():
    parser = argparse.ArgumentParser(description="Generate a Crucible debate script")
    parser.add_argument("topic", help="The debate topic")
    parser.add_argument("--models", default="qwen2.5:32b,nous-hermes2-mixtral,qwen3:8b",
                        help="Comma-separated list of 3 Ollama models")
    parser.add_argument("--duration", type=int, default=8, help="Duration in hours")
    parser.add_argument("--output", default="./debate/", help="Output directory")
    args = parser.parse_args()

    models = args.models.split(",")
    if len(models) != 3:
        parser.error("Exactly 3 models required (adversary, researcher, strategist)")

    os.makedirs(args.output, exist_ok=True)

    script = generate_debate_script(args.topic, models, args.duration)
    output_path = os.path.join(args.output, "debate.py")
    with open(output_path, "w") as f:
        f.write(script)
    os.chmod(output_path, 0o755)

    print(f"✅ Debate script generated: {output_path}")
    print(f"   Topic: {args.topic}")
    print(f"   Models: {', '.join(models)}")
    print(f"   Duration: {args.duration}h")
    print(f"\nTo run:")
    print(f"   cd {args.output}")
    print(f"   nohup python3 debate.py > debate.log 2>&1 &")
    print(f"   tail -f debate.log")


if __name__ == "__main__":
    main()
