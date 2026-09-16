---
theme: default
title: "AI without subscription: Run it on your own hardware"
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

<!-- ─────────────────────────────────────────────
  1. INTRO
───────────────────────────────────────────── -->

# AI without subscription
## Run it on your own hardware

Turn your own devices into AI Servers, simple, secure and accessible for everyone, not just tech experts.

<div class="text-center" style="min-width:200px">

[![QR](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Firc.conreco.com.ar%2F&bgcolor=0a0a0a&color=4afe1e&format=png)](https://irc.conreco.com.ar/)

**[irc.conreco.com.ar](https://irc.conreco.com.ar/)**

</div>

*NZ Tech Expo 2026 · Lucas Recoaro*

---

<!-- ─────────────────────────────────────────────
  2. WHAT IS AI — question
───────────────────────────────────────────── -->

# What is AI?

<div class="text-center text-5xl my-12">🤔</div>

---

<!-- ─────────────────────────────────────────────
  2. WHAT IS AI — answers
───────────────────────────────────────────── -->

# What is AI?
## It depends who you ask.

<table class="ai-table" v-click>
  <thead>
    <tr><th></th><th>Who</th><th>What they say</th></tr>
  </thead>
  <tbody>
    <tr><td>👔</td><td>A CEO</td><td>"A productivity multiplier for my team"</td></tr>
    <tr><td>👨‍⚕️</td><td>A doctor</td><td>"A tool that helps me diagnose faster"</td></tr>
    <tr><td>🔬</td><td>A researcher</td><td>"Statistical pattern matching on massive datasets"</td></tr>
    <tr><td>👨‍💻</td><td>A developer</td><td>"A process I can call and add into my other software"</td></tr>
  </tbody>
</table>

<div v-click class="mt-6">

**They're all right.**

</div>

<div v-click>

*But today we're talking about running it yourself.*

</div>

---

<!-- ─────────────────────────────────────────────
  3. 5-LAYER CAKE
───────────────────────────────────────────── -->

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

You can join the **top three layers** for the cost of a **second-hand GPU**.

---

<!-- ─────────────────────────────────────────────
  4. WHAT DOES OWNING THE INFRASTRUCTURE GIVE YOU?
───────────────────────────────────────────── -->

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

<div v-click class="hero-stat">
  Cloud AI charges per token — <strong>every word, every character, every call.</strong><br/>
  Local inference only costs <strong>electricity.</strong>
</div>

<div v-click class="sovereignty-note">
  🌏 <strong>Data sovereignty</strong> — your data stays in your country, on your hardware, under your laws. Not on a server somewhere else.
</div>

---

<!-- ─────────────────────────────────────────────
  5. WHAT IS A MODEL?
───────────────────────────────────────────── -->

# What is a model?

<div class="model-file-opener" v-click>
  <div class="model-file-icon">💾</div>
  <div class="model-file-text">
    A model is just a file.<br/>
    Like a PDF or an MP3 —<br/>
    except instead of a document or a song,<br/>
    it contains everything a machine<br/>
    <span class="strike">learned</span> <strong>processed</strong> from reading the internet.
  </div>
</div>

---

# What is a model?
## One file. Four things inside.

<div class="model-explainer">

<v-click>
<div class="model-box">
  <div class="model-icon">[ arch ]</div>
  <div class="model-content">
    <div class="model-title">Architecture</div>
    <div class="model-desc">The blueprint. Defines the shape — how many layers, how wide, how attention works. It's just a config file.</div>
  </div>
</div>
</v-click>

<v-click>
<div class="model-box">
  <div class="model-icon">[ weights ]</div>
  <div class="model-content">
    <div class="model-title">Weights</div>
    <div class="model-desc">Billions of numbers. The result of training — everything the model processed is stored here. This is the big file you download.</div>
  </div>
</div>
</v-click>

<v-click>
<div class="model-box">
  <div class="model-icon">[ tokens ]</div>
  <div class="model-content">
    <div class="model-title">Tokeniser</div>
    <div class="model-desc">Converts input into numbers the model can process. Models only ever see numbers.</div>
  </div>
</div>
</v-click>

<v-click>
<div class="model-box">
  <div class="model-icon">[ quant ]</div>
  <div class="model-content">
    <div class="model-title">Quantisation info</div>
    <div class="model-desc">Instructions for how the weights were compressed. Different flavours of the same model, runs on less RAM. Same model, lighter to carry.</div>
  </div>
</div>
</v-click>

</div>

---

<!-- ─────────────────────────────────────────────
  6a. TYPES OF MODELS
───────────────────────────────────────────── -->

# Models come in different shapes
## Not every model does the same thing

<div class="model-shapes">

<div class="model-shape" v-click>
  <div class="model-shape-icon">[ LLM ]</div>
  <div class="model-shape-name">Language</div>
  <div class="model-shape-desc">Text in, text out. Chat, summarise, write, reason, answer questions.</div>
</div>

<div class="model-shape" v-click>
  <div class="model-shape-icon">[ audio ]</div>
  <div class="model-shape-name">Audio</div>
  <div class="model-shape-desc">Speech to text, text to speech, or sound classification.</div>
</div>

<div class="model-shape" v-click>
  <div class="model-shape-icon">[ image ]</div>
  <div class="model-shape-name">Image</div>
  <div class="model-shape-desc">Understand or generate images. Describe a photo, detect objects, create art.</div>
</div>

<div class="model-shape model-shape-highlight" v-click>
  <div class="model-shape-icon">[ multi ]</div>
  <div class="model-shape-name">Multimodal</div>
  <div class="model-shape-desc">All of the above in one model. Text, images, audio — send anything, get anything back.</div>
</div>

</div>

---

<!-- ─────────────────────────────────────────────
  6b. NOT ALL MODELS ARE EQUAL
───────────────────────────────────────────── -->

# Not all models are equal
## Closed, open weight, and open source

<div class="model-types">

<div class="model-type" v-click>
  <div class="model-type-icon">[ closed ]</div>
  <div class="model-type-name">Proprietary / Closed</div>
  <div class="model-type-examples">GPT-4 · Claude · Gemini</div>
  <div class="model-type-desc">You send your data to their servers. You can't download or inspect the weights. Pay per use.</div>
  <div class="model-type-tag model-type-red">weights hidden · data leaves your network</div>
</div>

<div class="model-type" v-click>
  <div class="model-type-icon">[ open-w ]</div>
  <div class="model-type-name">Open Weight</div>
  <div class="model-type-examples">Llama 3 · Mistral · Qwen · Phi</div>
  <div class="model-type-desc">Weights are public — you can download and run locally. But the training data and full process aren't disclosed.</div>
  <div class="model-type-tag model-type-yellow">weights public · training data private</div>
</div>

<div class="model-type" v-click>
  <div class="model-type-icon">[ open-s ]</div>
  <div class="model-type-name">Open Source</div>
  <div class="model-type-examples">OLMo · Falcon · BLOOM</div>
  <div class="model-type-desc">Weights <em>and</em> training data and code are fully public. True open source — you can reproduce it from scratch.</div>
  <div class="model-type-tag model-type-green">weights + data + code all public</div>
</div>

</div>

<div v-click class="mt-4 text-center text-sm" style="color: var(--nz-grey)">

For running locally, <strong>open weight</strong> is what matters most — the weights are what you actually run.

</div>

---

<!-- ─────────────────────────────────────────────
  7. SIZE DOES MATTER
───────────────────────────────────────────── -->

# Size does matter
## Think of it like clothing sizes

<div class="clothes-grid">

<div class="clothes-card" v-click>
  <div class="clothes-size">XS</div>
  <div class="clothes-range">1B – 4B</div>
  <div class="clothes-model">Phi-4 Mini · Gemma 4 E4B</div>
  <div class="clothes-desc">Runs on a mobile phone, Raspberry Pi, even CPU-only. Simple Q&amp;A, summaries, weak machines.</div>
</div>

<div class="clothes-card" v-click>
  <div class="clothes-size">S</div>
  <div class="clothes-range">7B – 8B</div>
  <div class="clothes-model">Qwen3 8B · Mistral 7B</div>
  <div class="clothes-desc">Runs on 16 GB RAM. Chat, documents, everyday tasks. The laptop sweet spot.</div>
</div>

<div class="clothes-card clothes-card-highlight" v-click>
  <div class="clothes-size">M</div>
  <div class="clothes-range">14B – 27B</div>
  <div class="clothes-model">Qwen3 14B · Qwen3.8-27B</div>
  <div class="clothes-desc">Fits on one gaming GPU. Good reasoning, code, complex instructions. 4 points behind the world #1.</div>
  <div class="clothes-tag">👈 where we play</div>
</div>

<div class="clothes-card" v-click>
  <div class="clothes-size">L</div>
  <div class="clothes-range">70B</div>
  <div class="clothes-model">Llama 3.3 70B · DeepSeek V4 Flash</div>
  <div class="clothes-desc">Needs 96 GB RAM or a Mac Studio. Near-cloud quality on a desktop machine.</div>
</div>

<div class="clothes-card" v-click>
  <div class="clothes-size">XL</div>
  <div class="clothes-range">400B – 2T+</div>
  <div class="clothes-model">Llama 4 · Kimi K3 · Qwen3.8 Max</div>
  <div class="clothes-desc">Needs a server rack. Frontier Models.</div>
</div>

</div>

<div v-click class="clothes-verdict">
  The best model is what you can use today with the hardware you already own.
</div>

---

<!-- ─────────────────────────────────────────────
  8. WHY "LLAMA"? + TIMELINE
───────────────────────────────────────────── -->

# Why is everything called "Llama"?

<div class="llama-fun" style="margin-bottom: 1.25rem">
  <img src="/images/la_llama_que_llama.webp" class="llama-fun-img" alt="La llama que llama" />
  <div class="llama-fun-text">One model name sparked an entire ecosystem.<br/><span style="font-size:1rem; color: var(--nz-grey)">Also… llamas are just fun. 🦙</span></div>
</div>

<div class="timeline">

<div class="tl-item" v-click>
  <div class="tl-date">Nov 30, 2022</div>
  <div class="tl-body">
    <div class="tl-title">ChatGPT launches</div>
    <div class="tl-desc">The world realises AI is real and powerful. But it's closed — you can't run it yourself.</div>
  </div>
</div>

<div class="tl-item" v-click>
  <div class="tl-date">Feb 24, 2023</div>
  <div class="tl-body">
    <div class="tl-title">Meta releases LLaMA</div>
    <div class="tl-desc">Research-only — but the weights leak online within days. The open AI community suddenly has a powerful model to work with.</div>
  </div>
</div>

<div class="tl-item tl-highlight" v-click>
  <div class="tl-date">Mar 10, 2023</div>
  <div class="tl-body">
    <div class="tl-title">llama.cpp is born</div>
    <div class="tl-desc">Georgi Gerganov builds <strong>llama.cpp</strong> in a weekend — run LLaMA on a regular laptop, no expensive GPU needed.</div>
  </div>
</div>

<div class="tl-item tl-highlight" v-click>
  <div class="tl-date">Jul 8, 2023</div>
  <div class="tl-body">
    <div class="tl-title">Ollama launches</div>
    <div class="tl-desc"><strong>Ollama</strong> wraps llama.cpp into one command. Suddenly anyone can run AI locally.</div>
  </div>
</div>

</div>

---

<!-- ─────────────────────────────────────────────
  9. HOW TO RUN A MODEL
───────────────────────────────────────────── -->

# How to run a model

<div v-click class="infra-concept">
  These tools all do one thing: <strong>load a model file and let you use it.</strong><br/>
  That's it. The model is just a file on your disk. The software loads it into your hardware and runs it.
</div>

<div class="infra-list" v-click>
  <div class="infra-item">
    <span class="infra-item-name">llama.cpp</span>
    <span class="infra-item-sep">—</span>
    <span class="infra-item-desc">command line</span>
  </div>
  <div class="infra-item" style="color: var(--nz-green)">
    <span class="infra-item-name">Ollama</span>
    <span class="infra-item-sep">—</span>
    <span class="infra-item-desc">one command, runs as a local server</span>
  </div>
  <div class="infra-item">
    <span class="infra-item-name">LM Studio</span>
    <span class="infra-item-sep">—</span>
    <span class="infra-item-desc">desktop app with a GUI</span>
  </div>
  <div class="infra-item">
    <span class="infra-item-name">Jan</span>
    <span class="infra-item-sep">—</span>
    <span class="infra-item-desc">desktop app, open source</span>
  </div>
</div>


---

<!-- ─────────────────────────────────────────────
  10. TAKEAWAYS
───────────────────────────────────────────── -->

# What to take away from today

<v-clicks>

- **AI is not magic** — it's a file of numbers predicting the next word
- **You don't need the cloud** — small models run on hardware you already own
- **Open weight models are good enough** — for most real-world tasks
- **Privacy + cost + control** — three problems solved at once

</v-clicks>

---

<!-- ─────────────────────────────────────────────
  11. END / CONTACT
───────────────────────────────────────────── -->

# Thank you! - Tēnā koutou.

- **Lucas Recoaro**
- **lucas@conreco.com.ar**
- **https://www.conreco.com.ar**
