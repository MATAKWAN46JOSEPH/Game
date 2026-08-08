import { h, render } from "preact";
import htm from "htm";
import App from "./App.js";

const html = htm.bind(h);

// mount
render(html`<${App} />`, document.getElementById("app"));