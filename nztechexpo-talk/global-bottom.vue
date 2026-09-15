<template>
  <!-- NZ Tech Expo logo — bottom right -->
  <img
    src="/nztechexpo-logo.png"
    alt="NZ Tech Expo"
    style="
      position: fixed;
      bottom: 14px;
      right: 20px;
      width: 120px;
      opacity: 0.75;
      pointer-events: none;
      z-index: 100;
    "
  />

  <!-- IRC footer — bottom left -->
  <div style="
    position: fixed;
    bottom: 10px;
    left: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 100;
    opacity: 0.85;
  ">
    <img
      src="https://api.qrserver.com/v1/create-qr-code/?size=48x48&data=https%3A%2F%2Firc.conreco.com.ar%2F&bgcolor=0a0a0a&color=4afe1e&format=png"
      alt="QR irc.conreco.com.ar"
      style="width: 48px; height: 48px; border-radius: 4px;"
    />
    <a
      href="https://irc.conreco.com.ar/"
      target="_blank"
      style="
        color: #4afe1e;
        font-size: 0.65rem;
        font-weight: 700;
        text-decoration: none;
        letter-spacing: 0.04em;
        font-family: 'Fira Code', monospace;
        line-height: 1.3;
      "
    >irc.conreco.com.ar</a>
  </div>
</template>
