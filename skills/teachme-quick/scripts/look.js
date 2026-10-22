#!/usr/bin/env node
/* Look at a built course the way a reader will: screenshots plus the layout bugs a script
   can only see in a real browser.

   Usage:  node look.js <course-dir | index.html> [out-dir]

   Writes a desktop (light) screenshot of the top of every chapter and a phone (dark)
   screenshot of every WHOLE chapter to out-dir (default <course-dir>/.look/), and prints one
   line per problem:
     - the page scrolls sideways on a phone, and which element causes it
     - a table a phone reader has to scroll sideways to read
     - diagram text rendered below 9px (unreadable)
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
  if (!arg) { console.error("usage: node look.js <course-dir|index.html> [out-dir]"); process.exit(2); }
  const file = path.resolve(fs.statSync(arg).isDirectory() ? path.join(arg, "index.html") : arg);
  const out = path.resolve(process.argv[3] || path.join(path.dirname(file), ".look"));
  fs.mkdirSync(out, { recursive: true });
  const { chromium } = load();
  const browser = await chromium.launch();
  const problems = [], shots = [];
  for (const [name, vp, scheme] of [["desktop", { width: 1280, height: 800 }, "light"],
                                    ["phone", { width: 390, height: 844 }, "dark"]]) {
    const page = await browser.newPage({ viewport: vp, colorScheme: scheme });
    page.on("pageerror", e => problems.push(`[${name}] JavaScript error: ${e.message}`));
    await page.goto("file://" + file);
    await page.waitForTimeout(500);
    const n = await page.evaluate(() => document.querySelectorAll(".chapter").length);
    const r = { over: [], tiny: [], hidden: [], wide: [] };
    /* the reader shows one view at a time: the contents (#home), then each chapter by its id */
    for (let i = -1; i < n; i++) {
      await page.evaluate(i => {
        document.documentElement.style.scrollBehavior = "auto";
        const ch = document.querySelectorAll(".chapter")[i];
        location.hash = i < 0 ? "home" : ch.id;
      }, i);
      await page.waitForTimeout(200);
      const f = path.join(out, `${name}-${i < 0 ? "cover" : "ch" + (i + 1)}.png`);
      if (name === "phone" && i >= 0) {
        /* the whole chapter, cut into screen-sized pieces so each image stays readable:
           phone-ch2-1.png, phone-ch2-2.png, … — scroll and photograph the viewport, since a
           fullPage capture of a long page times out */
        await page.setViewportSize({ width: vp.width, height: 1400 });
        const h = await page.evaluate(() => document.documentElement.scrollHeight);
        for (let k = 0, y = 0; y < h; k++, y += 1340) {
          const g = f.replace(/\.png$/, `-${k + 1}.png`);
          await page.evaluate(y => window.scrollTo(0, y), y);
          await page.waitForTimeout(80);
          try { await page.screenshot({ path: g, timeout: 15000 }); shots.push(g); }
          catch (e) { problems.push(`[${name}] could not photograph ${path.basename(g)}: ${e.message.split("\n")[0]}`); }
        }
        await page.setViewportSize(vp);
        await page.evaluate(() => window.scrollTo(0, 0));
      } else {
        try { await page.screenshot({ path: f, timeout: 15000 }); shots.push(f); }
        catch (e) { problems.push(`[${name}] could not photograph ${path.basename(f)}: ${e.message.split("\n")[0]}`); }
      }
      const got = await page.evaluate(() => {
        const res = { over: [], tiny: [], hidden: [], wide: [] }, W = innerWidth;
        const view = document.querySelector(".chapter.on") || document.querySelector(".cover");
        const where = e => (e.closest(".chapter") || {}).id || "contents";
        if (document.documentElement.scrollWidth > W + 1) {
          view.querySelectorAll("*").forEach(e => {
            const b = e.getBoundingClientRect();
            if (b.right > W + 1 && !e.closest("pre,.tw,figure,.tree,.math,.derive,.annot,.tabs-h") && e.children.length === 0)
              res.over.push(where(e) + " <" + e.tagName.toLowerCase() + "> " + (e.textContent || "").trim().slice(0, 50));
          });
        }
        /* real code may scroll (wrapping would break its indentation); a URL or a line of output
           in a plain block should not */
        if (W < 500) view.querySelectorAll(".code.plain pre").forEach(p => {
          /* highlighted code is one span.ln per line, with no newline characters left in it */
          const lines = p.querySelectorAll(".ln").length || (p.textContent || "").trim().split("\n").length;
          if (lines <= 3 && p.scrollWidth > p.clientWidth + 4) res.hidden.push(where(p) + ": " + (p.textContent || "").trim().slice(0, 40));
        });
        if (W < 500) view.querySelectorAll(".tw").forEach(t => {
          if (t.scrollWidth > t.clientWidth + 4) res.wide.push(where(t) + " (" + t.querySelectorAll("tr:first-child > *").length + " columns)");
        });
        view.querySelectorAll("figure svg text").forEach(t => {
          const h = t.getBoundingClientRect().height;
          if (h && h < 9) res.tiny.push(where(t) + ": " + t.textContent.trim().slice(0, 30));
        });
        return res;
      });
      for (const k of Object.keys(r)) r[k].push(...got[k]);
    }
    [...new Set(r.over)].slice(0, 6).forEach(o => problems.push(`[${name}] page scrolls sideways — widened by ${o}`));
    if (r.hidden.length) problems.push(`[${name}] short code block(s) scroll sideways on a phone and hide their end: ${r.hidden.join(" | ")} — use inline <code> (it wraps) or lang-text`);
    if (r.wide.length) problems.push(`[${name}] table(s) scroll sideways on a phone: ${r.wide.join(", ")} — readers miss the right-hand columns; use ≤4 short columns or split the table`);
    if (r.tiny.length) problems.push(`[${name}] ${r.tiny.length} diagram label(s) render under 9px, e.g. ${r.tiny.slice(0, 3).join(" | ")} — draw fewer, bigger labels`);
    await page.close();
  }
  await browser.close();
  console.log(`screenshots: ${shots.length} in ${out}`);
  problems.forEach(p => console.log("LOOK  " + p));
  console.log(problems.length ? `\n${problems.length} visual problem(s) — fix them in parts/ and re-run` : "\nno visual problems found — still open the screenshots and look");
  process.exit(problems.length ? 1 : 0);
})();
