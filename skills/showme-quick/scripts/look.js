#!/usr/bin/env node
/* Look at a built deck the way the room will: a screenshot of every slide (all builds shown),
   the overview grid, and the layout bugs only a real browser can see.

   Usage:  node look.js <deck-dir | index.html> [out-dir]

   Writes slide-NN.png and grid.png to out-dir (default <deck-dir>/.look/) and prints one line
   per problem:
     - content that spills past the slide edge (clipped on the projector)
     - a slide the runtime had to shrink to fit (too much on it)
     - text rendered below 14px on the 1280x720 canvas (unreadable from the back)
     - JavaScript errors
   Exit code 1 when it finds a problem. Needs Playwright (npm i -g playwright, or any
   global install — the script looks in `npm root -g` itself). */
const path = require("path"), fs = require("fs"), cp = require("child_process");
function load() {
  try { return require("playwright"); } catch (e) {}
  try { return require(path.join(cp.execSync("npm root -g").toString().trim(), "playwright")); } catch (e) {}
  console.error("look.js: Playwright not found. Install it (npm i -g playwright) or skip the visual check and say so.");
  process.exit(2);
}
(async () => {
  const arg = process.argv[2];
  if (!arg) { console.error("usage: node look.js <deck-dir|index.html> [out-dir]"); process.exit(2); }
  const file = path.resolve(fs.statSync(arg).isDirectory() ? path.join(arg, "index.html") : arg);
  const out = path.resolve(process.argv[3] || path.join(path.dirname(file), ".look"));
  fs.mkdirSync(out, { recursive: true });
  const { chromium } = load();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const problems = [];
  page.on("pageerror", e => problems.push(`JavaScript error: ${e.message}`));
  await page.goto("file://" + file);
  await page.waitForTimeout(700);
  await page.mouse.move(640, 360); await page.waitForTimeout(3000);   // let the controls fade
  const n = await page.evaluate(() => document.querySelectorAll(".slide").length);
  for (let i = 0; i < n; i++) {
    await page.evaluate(i => { location.hash = "#" + (i + 1); }, i);
    await page.waitForTimeout(250);
    const r = await page.evaluate(i => {
      const s = document.querySelectorAll(".slide")[i];
      s.querySelectorAll("[data-build]").forEach(e => e.classList.add("shown"));
      const k = s.getBoundingClientRect().width / 1280, box = s.getBoundingClientRect(), res = { spill: [], small: [], shrunk: false };
      const fit = s.querySelector(".sfit");
      if (fit && /scale\(/.test(fit.style.transform)) res.shrunk = fit.style.transform;
      s.querySelectorAll(".sfit *").forEach(e => {
        const b = e.getBoundingClientRect();
        if (!b.width || getComputedStyle(e).visibility === "hidden") return;
        if (b.right > box.right + 2 || b.bottom > box.bottom + 2 || b.left < box.left - 2)
          res.spill.push("<" + e.tagName.toLowerCase() + "> " + (e.textContent || "").trim().slice(0, 40));
        if (e.children.length === 0 && (e.textContent || "").trim() && !e.closest("svg,.chart,.notes")) {
          const fs = parseFloat(getComputedStyle(e).fontSize) * (fit && fit.style.transform ? parseFloat((fit.style.transform.match(/scale\(([\d.]+)/) || [0, 1])[1]) : 1);
          if (fs < 14) res.small.push(Math.round(fs) + "px \"" + e.textContent.trim().slice(0, 30) + "\"");
        }
      });
      return res;
    }, i);
    await page.waitForTimeout(450);
    await page.screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, "0")}.png`) });
    const tag = `[slide ${i + 1}]`;
    if (r.spill.length) problems.push(`${tag} content spills past the slide edge: ${[...new Set(r.spill)].slice(0, 3).join(" | ")}`);
    if (r.shrunk) problems.push(`${tag} the runtime shrank this slide to fit (${r.shrunk}) — move text to the notes or split it`);
    if (r.small.length) problems.push(`${tag} text below 14px on the canvas: ${[...new Set(r.small)].slice(0, 3).join(" | ")}`);
  }
  await page.keyboard.press("o"); await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(out, "grid.png"), fullPage: true });
  await browser.close();
  console.log(`screenshots: ${n} slides + grid in ${out}`);
  problems.forEach(p => console.log("LOOK  " + p));
  console.log(problems.length ? `\n${problems.length} visual problem(s) — fix them in parts/ and re-run` : "\nno visual problems found — still open grid.png and look");
  process.exit(problems.length ? 1 : 0);
})();
