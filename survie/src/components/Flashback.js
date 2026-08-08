import { h } from "preact";
import htm from "htm";
import { useEffect } from "preact/hooks";

const html = htm.bind(h);

export default function Flashback({ flash, onClose }) {
  useEffect(() => {
    const t = setTimeout(() => {
      // auto close after 4.5s
      onClose();
    }, 4500);
    return () => clearTimeout(t);
  }, []);

  return html`
    <div style="position:absolute; inset:18px; display:flex; align-items:center; justify-content:center; pointer-events:auto;">
      <div style="width:100%; height:100%; background:linear-gradient(0deg, rgba(0,0,0,0.6), rgba(0,0,0,0.2)); border-radius:12px; display:flex; align-items:center; justify-content:center;">
        <div style="width:90%; background:rgba(10,10,10,0.9); border-radius:12px; padding:16px; box-sizing:border-box; border:1px solid rgba(255,255,255,0.03);">
          <h3 style="margin:0 0 8px 0; font-size:18px; color:#ffdede;">${flash.title}</h3>
          <p style="margin:0 0 12px 0; color:#efeae5; line-height:1.4;">${flash.text}</p>
          <div style="display:flex; justify-content:flex-end;">
            <button onClick=${onClose} style="background:#222; color:#fff; border-radius:8px; padding:8px 12px; border:1px solid rgba(255,255,255,0.03);">Fermer</button>
          </div>
        </div>
      </div>
    </div>
  `;
}