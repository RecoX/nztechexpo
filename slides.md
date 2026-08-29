---
theme: default
title: Your AI, Your Rules
info: NZ Tech Expo 2026 — Running your own AI inference server
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
---

# Do.It.Yourself [AI]
## Running your own AI inference server

*NZ Tech Expo 2026*

---

# Chat with our AI — right now

<div class="text-center text-8xl my-8">📱</div>

<div class="text-center text-4xl font-bold my-4">[ QR CODE ]</div>

*Running on our own hardware. No ChatGPT. No OpenAI.*

> Scan now and start chatting — I'll explain what's happening under the hood while you do.

<br>

*Powered by a mix of technologies spanning **38 years** — IRC (1988) meets local AI inference (2026).*

---

# What is AI?
## It depends who you ask.

| | Who | What they say |
|---|---|---|
| 👔 | A CEO | "A productivity multiplier for my team" |
| 👨‍⚕️ | A doctor | "A tool that helps me diagnose faster" |
| 🔬 | A researcher | "Statistical pattern matching on massive datasets" |
| 🖥️ | A DevOps engineer | "An API I can self-host and plug into my pipeline" |
| 👨‍💻 | A developer | "A process I can call and add into my other processes" |

<br>

**They're all right.**

*But today we're talking about running it yourself.*

---

# AI is a 5-Layer Cake
*— Jensen Huang, NVIDIA · [blogs.nvidia.com](https://blogs.nvidia.com/blog/ai-5-layer-cake/)*

<div class="cake-grid">
  <div class="cake-row active">
    <div class="cake-layer">🛠️ APPLICATIONS</div>
    <div class="cake-desc">IRC bots · AI agents · coding assistants · chat apps · your own tools</div>
    <div class="cake-tag">👈 WE BUILD HERE</div>
  </div>
  <div class="cake-row active">
    <div class="cake-layer">🧠 MODELS</div>
    <div class="cake-desc">Llama 3 · Qwen · DeepSeek · Mistral · Phi · Gemma · open weights</div>
    <div class="cake-tag">👈 WE CHOOSE HERE</div>
  </div>
  <div class="cake-row active">
    <div class="cake-layer">⚙️ INFRASTRUCTURE</div>
    <div class="cake-desc">GPU server · llama.cpp · LiteLLM · OpenAI-compatible API</div>
    <div class="cake-tag">👈 WE RUN HERE</div>
  </div>
  <div class="cake-row dim">
    <div class="cake-layer">💾 CHIPS</div>
    <div class="cake-desc">NVIDIA · AMD · Apple Silicon</div>
    <div class="cake-tag"></div>
  </div>
  <div class="cake-row dim">
    <div class="cake-layer">⚡ ENERGY</div>
    <div class="cake-desc">power · cooling</div>
    <div class="cake-tag"></div>
  </div>
</div>

> "Every successful application pulls on every layer beneath it — all the way down to the power plant."

Big tech is spending **trillions** building this stack. You can join the **top three layers** for the cost of a **second-hand GPU**.

---

# For a developer, AI is a process

```mermaid
graph TD
    A["🖥️ Your App / IRC Chat"]
    A -->|HTTP request| S
    S -->|HTTP response streamed| A

    subgraph INF["⚙️ Inference Server (e.g. Qwen3.8 Max)"]
        S["📡 receives request"]
        S --> C["🔥 GPU VRAM — model runs here"]
        S --> D["🐢 RAM — overflow"]
        S --> E["🧠 CPU — tokenization · routing · I/O"]
    end
```

---

# Hardware? Less than you think.

> 💡 *"The best hardware is what you have immediately available without spending any money"*

<div class="hw2-grid">
<div class="hw2-col">

**What fits where:**

| Size | Model | VRAM | Runs on |
|---|---|---|---|
| XXS | Qwen2.5-0.5B | ~300 MB | Phone, Raspberry Pi |
| XS | Phi-4-mini | ~2 GB | Any laptop, CPU-only |
| M | Llama 3.1 8B | ~5 GB | Gaming GPU |
| L | Qwen3.7 MoE | ~20 GB | 2× Quadro RTX 4000 👈 us |
| XL | Qwen3 32B | ~24 GB | RTX 4090 / 3090 |
| XXL | Qwen3.8 Max | ~40 GB | Multi-GPU server |

<div class="table-source">Source: <a href="https://benchlm.ai">benchlm.ai</a> · best open weight · Aug 15, 2026</div>

- **VRAM** is the bottleneck — fit the model in for full speed
- RAM offload works but is 10–20× slower
- CPU handles tokenization + routing + I/O

</div>
<div class="hw2-col">

**What we actually run:**

```mermaid
graph LR
    Q["🖥️ Quadro RTX 4000\nllama.cpp · Qwen3.7 MoE"]
    T["🖥️ GTX 1080 Ti\nllama.cpp · fast model"]
    L["⚡ LiteLLM"]
    A["🤖 Apps / Agents"]
    C["☁️ Cloud AI\nOpenAI · Anthropic\nMistral · DeepSeek"]

    Q --> L
    T --> L
    C --> L
    L --> A
    A --> L
```

- **Primary**: Qwen3.7 MoE · 22B active
- **Router**: LiteLLM — OpenAI-compatible API
- **Fallback**: Groq / DeepSeek if both busy

</div>
</div>

---

# What does owning the infrastructure give you?

<div class="hero-cards">
  <div class="hero-card">
    <div class="hero-icon">🔒</div>
    <div class="hero-title">Privacy</div>
    <div class="hero-sub">Your data never leaves the building</div>
    <ul class="hero-bullets">
      <li>Prompts stay on your network</li>
      <li>No vendor logging your queries</li>
      <li>GDPR / compliance friendly</li>
    </ul>
  </div>
  <div class="hero-card">
    <div class="hero-icon">💸</div>
    <div class="hero-title">Cost</div>
    <div class="hero-sub">Pay once — not per token, forever</div>
    <ul class="hero-bullets">
      <li>Break-even in weeks vs. API</li>
      <li>Unlimited calls, zero surprise bills</li>
    </ul>
  </div>
  <div class="hero-card">
    <div class="hero-icon">⚡</div>
    <div class="hero-title">Control</div>
    <div class="hero-sub">You decide everything</div>
    <ul class="hero-bullets">
      <li>Swap models in seconds</li>
      <li>No rate limits or outages</li>
      <li>Fine-tune on your own data</li>
    </ul>
  </div>
</div>

<div class="hero-stat">
  Cloud AI charges per token — <strong>every word, every character, every call.</strong><br/>
  Local inference only costs <strong>electricity.</strong>
</div>

---

# Scan. Chat. Ask us anything.

<div class="text-center text-8xl my-8">📱</div>

<div class="text-center text-4xl font-bold my-4">[ QR CODE ]</div>

*The agent you're talking to is running on our hardware — right now.*

<br>

**[your contact / site]**
