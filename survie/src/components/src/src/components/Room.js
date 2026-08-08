import { h } from "preact";
import htm from "htm";
import { useState, useEffect, useRef } from "preact/hooks";
import Flashback from "./Flashback.js";
import useAmbience from "./useAmbience.js";

const html = htm.bind(h);

const initialNarration = [
  "Vous poussez la porte d'entrée et l'air vous frappe — poussière épaisse, odeur de bois mouillé et carton. Les murs sont familiers et pourtant mauvaisements alignés dans votre souvenir.",
  "La lumière qui filtre par la vitre sale découpe des formes lentes sur le plancher. Quelque chose gratte, très loin, comme si la maison expirait.",
];

export default function Room() {
  const [narration, setNarration] = useState(initialNarration.join(" "));
  const [choices, setChoices] = useState([
    { id: "doll", label: "Une poupée chiffonnée posée sur une étagère" },
    { id: "radio", label: "Une vieille radio recouverte de poussière" },
  ]);
  const [door, setDoor] = useState({ id: "hall", label: "La porte du couloir, légèrement entrouverte" });
  const [flash, setFlash] = useState(null);
  const [eventsLog, setEventsLog] = useState([]);
  const ambience = useAmbience();

  useEffect(() => {
    // small delayed creak to set tone
    const t = setTimeout(() => {
      setNarration((n) => n + " Un léger grincement répond à votre pas.");
      ambience.playCreak();
    }, 1200);
    return () => clearTimeout(t);
  }, []);

  function handleInspect(id) {
    if (id === "doll") {
      setNarration((n) => "Vous prenez la poupée. Ses yeux de verre vous regardent avec une indifférence trop humaine. Une odeur de sachet de lavande rance monte et un éclat de mémoire s'ouvre.");
      setFlash({ type: "memory", title: "La poupée", text: "Vous vous voyez, sept ans, la poupée serrée contre la joue pendant que quelqu'un coupe sa voix en deux morceaux. La mémoire s'effrite." });
      ambience.playChildWhisper();
      logEvent("inspect_poupée");
    } else if (id === "radio") {
      setNarration((n) => "Vous dépoussiérez la radio. Elle grésille, se met à murmurer une station inexistante. Une voix calme répète votre nom, décalée et distante.");
      setFlash({ type: "event", title: "La radio", text: "La fréquence hurle un écho de la maison : votre rire jeune, puis un silence trop long." });
      ambience.playRadio();
      logEvent("inspect_radio");
    }
  }

  function handleOpenDoor() {
    setNarration("Vous poussez la porte du couloir. L'odeur change : meuble ancien et papier. Une ombre se décale au fond. Vous sentez votre rythme cardiaque accélérer.");
    setFlash({ type: "transition", title: "Le couloir", text: "Le couloir s'étire plus longtemps que vous ne vous en souvenez. Des cadres aux visages floutés suivent votre passage." });
    ambience.playDoorSlide();
    logEvent("open_door");
  }

  function closeFlash() {
    setFlash(null);
  }

  function logEvent(ev) {
    setEventsLog((s) => [...s, { ev, at: Date.now() }]);
  }

  return html`
    <div style="width:100%; max-width:640px; height:100%; background:linear-gradient(#0b0b0b,#101010); border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.7); padding:18px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between;">
      <div style="flex:1; display:flex; flex-direction:column; gap:12px; user-select:none;">
        <div style="background:rgba(255,255,255,0.02); padding:14px; border-radius:10px; min-height:120px; display:flex; align-items:flex-start;">
          <p style="margin:0; line-height:1.45; font-size:16px;">${narration}</p>
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          ${choices.map((c) => html`
            <button onClick=${() => handleInspect(c.id)} style="flex:1 1 45%; min-height:48px; background:#171717; color:#efeae5; border:1px solid rgba(255,255,255,0.04); border-radius:10px; padding:10px; font-size:14px; text-align:left; box-shadow:inset 0 -2px 0 rgba(0,0,0,0.6);">
              ${c.label}
            </button>
          `)}
        </div>

        <div style="display:flex; gap:10px;">
          <button onClick=${handleOpenDoor} style="flex:1; min-height:48px; background:#2b1f1f; color:#ffdede; border:1px solid rgba(255,100,100,0.06); border-radius:10px; padding:10px; font-size:15px;">
            ${door.label}
          </button>
        </div>

        <div style="opacity:0.7; font-size:12px; display:flex; gap:8px; flex-wrap:wrap;">
          <span style="background:rgba(255,255,255,0.03); padding:6px 8px; border-radius:8px;">Entrée poussiéreuse</span>
          <span style="background:rgba(255,255,255,0.03); padding:6px 8px; border-radius:8px;">Heure: soir indéfini</span>
        </div>
      </div>

      <div style="display:flex; gap:8px; align-items:center; justify-content:space-between; margin-top:12px;">
        <div style="display:flex; gap:8px; align-items:center;">
          <button onClick=${() => ambience.toggleMute()} style="width:44px; height:44px; border-radius:8px; background:#111; border:1px solid rgba(255,255,255,0.03); color:#fff;">${() => ambience.muted ? "🔇" : "🔊"}</button>
          <div style="font-size:12px; opacity:0.8;">Bruits subtils: ${() => (ambience.muted ? "off" : "on")}</div>
        </div>
        <div style="font-size:12px; opacity:0.7;">${() => eventsLog.length ? `${eventsLog.length} événement(s)` : "Aucun événement"}</div>
      </div>

      ${flash ? html`<${Flashback} flash=${flash} onClose=${closeFlash} />` : null}
    </div>
  `;
}