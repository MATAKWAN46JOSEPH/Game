import { h } from "preact";
import htm from "htm";
import Room from "./components/Room.js";

const html = htm.bind(h);

export default function App() {
  return html`
    <${Room} />
  `;
}