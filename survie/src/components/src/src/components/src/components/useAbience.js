import { useState, useEffect, useRef } from "preact/hooks";

/*
  Simple ambient engine using Web Audio for subtle textures:
  - low rumble
  - occasional creak
  - distant child whisper (short noise burst)
  - radio hiss (bandpass noise)
*/
export default function useAmbience() {
  const ctxRef = useRef(null);
  const masterRef = useRef(null);
  const rumbleRef = useRef(null);
  const mutedRef = useRef(false);
  const [muted, setMuted] = useState(false);

  useEffect(() => {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    ctxRef.current = ctx;
    const master = ctx.createGain();
    master.gain.value = 0.5;
    master.connect(ctx.destination);
    masterRef.current = master;

    // rumble: low noise through lowpass
    const noise = createNoiseBuffer(ctx);
    const src = ctx.createBufferSource();
    src.buffer = noise;
    src.loop = true;
    const lp = ctx.createBiquadFilter();
    lp.type = "lowpass"; lp.frequency.value = 120;
    const gain = ctx.createGain(); gain.gain.value = 0.08;
    src.connect(lp); lp.connect(gain); gain.connect(master);
    src.start();
    rumbleRef.current = { src, gain };

    // start suspended; resume on first interaction
    function resume() { if (ctx.state === "suspended") ctx.resume(); window.removeEventListener("pointerdown", resume); }
    window.addEventListener("pointerdown", resume);

    return () => {
      try { src.stop(); ctx.close(); } catch (e) {}
      window.removeEventListener("pointerdown", resume);
    };
  }, []);

  function createNoiseBuffer(ctx) {
    const b = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const d = b.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * 0.35;
    return b;
  }

  function playCreak() {
    const ctx = ctxRef.current;
    if (!ctx) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    gain.gain.value = 0;
    osc.type = "sine";
    osc.frequency.value = 200;
    osc.connect(gain);
    gain.connect(masterRef.current);
    osc.start();
    const now = ctx.currentTime;
    gain.gain.cancelScheduledValues(now);
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.14, now + 0.06);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    osc.frequency.exponentialRampToValueAtTime(40, now + 1.2);
    setTimeout(() => { try { osc.stop(); } catch (e) {} }, 1400);
  }

  function playChildWhisper() {
    const ctx = ctxRef.current;
    if (!ctx) return;
    // short filtered noise burst
    const noise = createNoiseBuffer(ctx);
    const src = ctx.createBufferSource();
    src.buffer = noise;
    const bp = ctx.createBiquadFilter();
    bp.type = "bandpass"; bp.frequency.value = 900;
    const gain = ctx.createGain(); gain.gain.value = 0;
    src.connect(bp); bp.connect(gain); gain.connect(masterRef.current);
    src.start();
    const now = ctx.currentTime;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.06);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    setTimeout(() => { try { src.stop(); } catch (e) {} }, 1400);
  }

  function playRadio() {
    const ctx = ctxRef.current;
    if (!ctx) return;
    const noise = createNoiseBuffer(ctx);
    const src = ctx.createBufferSource();
    src.buffer = noise;
    src.loop = false;
    const bp = ctx.createBiquadFilter();
    bp.type = "bandpass"; bp.frequency.value = 1200;
    const gain = ctx.createGain(); gain.gain.value = 0;
    src.connect(bp); bp.connect(gain); gain.connect(masterRef.current);
    src.start();
    const now = ctx.currentTime;
    gain.gain.linearRampToValueAtTime(0.22, now + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.5);
    setTimeout(() => { try { src.stop(); } catch (e) {} }, 2600);
  }

  function playDoorSlide() {
    const ctx = ctxRef.current;
    if (!ctx) return;
    const osc = ctx.createOscillator();
    osc.type = "triangle";
    const gain = ctx.createGain(); gain.gain.value = 0;
    const bp = ctx.createBiquadFilter(); bp.type = "lowpass"; bp.frequency.value = 600;
    osc.connect(bp); bp.connect(gain); gain.connect(masterRef.current);
    osc.start();
    const now = ctx.currentTime;
    gain.gain.linearRampToValueAtTime(0.16, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    osc.frequency.setValueAtTime(300, now);
    osc.frequency.exponentialRampToValueAtTime(60, now + 1.2);
    setTimeout(() => { try { osc.stop(); } catch (e) {} }, 1400);
  }

  function toggleMute() {
    mutedRef.current = !mutedRef.current;
    setMuted(mutedRef.current);
    if (masterRef.current) masterRef.current.gain.value = mutedRef.current ? 0 : 0.5;
  }

  return {
    playCreak,
    playChildWhisper,
    playRadio,
    playDoorSlide,
    toggleMute,
    muted,
  };
}