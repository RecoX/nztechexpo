---
theme: default
title: "I without subscription: Run it on your own hardware"
info: NZ Tech Expo 2026 — Turn your own devices into AI Servers
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: Inter
  mono: Fira Code
---

# AI without subscription
## Run it on your own hardware

Turn your own devices into AI Servers, simple, secure and accessible for everyone, not just tech experts.

*NZ Tech Expo 2026 · Lucas Recoaro*


---

# Chat with a AI agents 

<div class="flex items-center justify-between gap-8 my-4">
<div class="flex-1">

> Scan now and join the conversation — a city is being built in real time.

*Ask them questions. Give them a problem. See what they decide.*

<div class="hw-photos">
  <div class="hw-photo-item">
    <img src="/images/rtx 4000.webp" alt="Quadro RTX 4000" />
    <div class="hw-photo-label">Quadro RTX 4000 · 2018</div>
  </div>
  <div class="hw-photo-item">
    <img src="/images/z4.jpg" alt="HP Z4 Workstation" />
    <div class="hw-photo-label">HP Z4 Workstation · 2018</div>
  </div>
</div>

*Powered by a mix of technologies spanning **38 years** — IRC (1988) meets local AI inference (2026).*

</div>
<div class="text-center" style="min-width:200px">

[![QR](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Firc.conreco.com.ar%2F&bgcolor=0a0a0a&color=4afe1e&format=png)](https://irc.conreco.com.ar/)

**[irc.conreco.com.ar](https://irc.conreco.com.ar/)**

</div>
</div>

---

# What is AI?
## It depends who you ask.

| | Who | What they say |
|---|---|---|
| 👔 | A CEO | "A productivity multiplier for my team" |
| 👨‍⚕️ | A doctor | "A tool that helps me diagnose faster" |
| 🔬 | A researcher | "Statistical pattern matching on massive datasets" |
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
    <div class="cake-desc">Llama 3 · Qwen · DeepSeek · Mistral · Phi · Gemma · and many more...</div>
    <div class="cake-tag">👈 WE CHOOSE HERE</div>
  </div>
  <div class="cake-row active">
    <div class="cake-layer">⚙️ INFRASTRUCTURE</div>
    <div class="cake-desc">Ollama · llama.cpp · LM Studio · Jan · and more...</div>
    <div class="cake-tag">👈 WE RUN HERE</div>
  </div>
  <div class="cake-row dim">
    <div class="cake-layer">💾 CHIPS</div>
    <div class="cake-desc">NVIDIA · AMD · Intel · Apple Silicon</div>
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

# Why is everything called "Llama"?

> One model name sparked an entire ecosystem.

---

# The Timeline

<div class="timeline">

<div class="tl-item">
  <div class="tl-date">Nov 30, 2022</div>
  <div class="tl-body">
    <div class="tl-title">ChatGPT launches</div>
    <div class="tl-desc">OpenAI releases ChatGPT to the public. The world realises AI is real, accessible, and powerful. But it's closed — you can't run it yourself.</div>
  </div>
</div>

<div class="tl-item">
  <div class="tl-date">Feb 24, 2023</div>
  <div class="tl-body">
    <div class="tl-title">Meta releases LLaMA</div>
    <div class="tl-desc">Meta releases its own large language model: <strong>LLaMA</strong> <em>(Large Language Model Meta AI)</em>. Research-only — but the weights leak online within days. The open AI community suddenly has a powerful model to work with.</div>
  </div>
</div>

<div class="tl-item tl-highlight">
  <div class="tl-date">Mar 10, 2023</div>
  <div class="tl-body">
    <div class="tl-title">llama.cpp is born</div>
    <div class="tl-desc">Developer Georgi Gerganov builds <strong>llama.cpp</strong> in a weekend. Goal: run LLaMA on a regular laptop, no expensive GPU needed. Becomes the foundation of local AI running everywhere.</div>
  </div>
</div>

<div class="tl-item tl-highlight">
  <div class="tl-date">Jul 8, 2023</div>
  <div class="tl-body">
    <div class="tl-title">Ollama launches</div>
    <div class="tl-desc"><strong>Ollama</strong> is released — a friendly app that wraps llama.cpp. Makes running AI models on your own computer as easy as one command. Suddenly anyone can run AI locally.</div>
  </div>
</div>

</div>

---

# Why the name stuck

<div class="llama-grid">
  <div class="llama-card">
    <div class="llama-tool">Meta LLaMA</div>
    <div class="llama-arrow">↓</div>
    <div class="llama-desc">The leaked model that started it all</div>
  </div>
  <div class="llama-card llama-card-green">
    <div class="llama-tool">llama.cpp</div>
    <div class="llama-arrow">↓</div>
    <div class="llama-desc">Named after the model it runs</div>
  </div>
  <div class="llama-card llama-card-green">
    <div class="llama-tool">Ollama</div>
    <div class="llama-arrow">↓</div>
    <div class="llama-desc">"ol' llama" — a friendlier wrapper on top</div>
  </div>
  <div class="llama-card">
    <div class="llama-tool">Llama 2 · 3 · 3.1…</div>
    <div class="llama-arrow">↓</div>
    <div class="llama-desc">Meta kept the brand as it improved</div>
  </div>
</div>

> One leaked model in early 2023 changed everything.
> The llama became the symbol of AI you can actually own.

---

# Chat with a computer in my garage.

<div class="text-center text-8xl my-4">📱</div>

<div class="text-center my-3">

[![QR](https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https%3A%2F%2Firc.conreco.com.ar%2F&bgcolor=0a0a0a&color=4afe1e&format=png)](https://irc.conreco.com.ar/)

**[irc.conreco.com.ar](https://irc.conreco.com.ar/)**

</div>

<div class="city-roles">
  <div class="city-role">👨‍⚕️ Doctor</div>
  <div class="city-role">🐾 Vet</div>
  <div class="city-role">👮 Police</div>
  <div class="city-role">🏗️ Engineer</div>
</div>

*AI agents running on our hardware — building a city, together, live.*

**Lucas Recoaro · lucas@conreco.co.nz**
