          // ── Word-anchored cue lookup: W("trade", 2) = start of the 2nd "trade" ──
          const WORDS = __WORDS__;
          const norm = (x) => x.toLowerCase().replace(/[^a-z0-9']/g, "");
          function W(word, n) {
            let k = 0;
            for (const w of WORDS) if (norm(w[0]) === word && ++k === (n || 1)) return w[1];
            throw new Error("cue word not found: " + word + " #" + (n || 1));
          }
          function WE(word, n) { let k = 0; for (const w of WORDS) if (norm(w[0]) === word && ++k === (n || 1)) return w[2]; throw new Error("cue " + word); }
          const CUTS = __CUTS__;

          // ── Cue sheet (all derived from spoken words) ──
          const T = {
            c1in: 0, one: W("one"), trade1: W("trade"), ahead: W("ahead"), getting: W("getting"), successful1: W("successful"), c1out: W("iske") - 0.05,
            two: W("2"), three: W("3"), six: W("6"), c2out: W("iss") - 0.05,
            iss: W("iss"), video1: W("video"), prep: W("preparation"), ektrade: W("ek"), proper1: W("proper"), entry: W("entry"), exit: W("exit"), execution: W("execution"), c34out: WE("sath") + 0.25,
            lets: W("let's"), start: W("start"), c5out: WE("guys", 2) + 0.15,
            aapko: W("aapko", 3), bas: W("bas"), ek2: W("ek", 3), important: W("important"), reason: W("reason"),
            main: W("main", 2), wo: W("wo"), tak: W("tak"), thousands: W("thousands"), padega: WE("padega"),
            because: W("because"), koi: W("koi"), aaj: W("aaj"), kal: W("kal"), mahine2: W("mahine", 2), nahi2: W("nahi", 2),
            beg1: W("beginner's"), luck1: W("luck"), sabke: W("sabke"), andar: W("andar"),
            you3: W("you", 3), successful3: W("successful", 3), downfall: W("downfall"), wo2: W("wo", 2),
          };
          T.c6in = T.aapko - 0.3; T.c6out = T.main - 0.08;
          T.c7in = T.main - 0.05; T.c7out = T.because - 0.08;
          T.c8in = T.because - 0.08; T.c8out = T.beg1 - 0.4;
          T.c9in = T.beg1 - 0.3; T.c9out = T.you3 - 0.12;
          T.c10in = T.you3 - 0.12;

          // ── Framing engine: zoom cuts + face-safe reframes ──
          // side = which side a card occupies; the face is pushed to the opposite side.
          const SIDE = [[T.c1in, T.c1out, "L"], [T.c1out, T.c2out, "R"], [T.c2out, T.c34out, "L"], [T.c6in, T.c6out, "L"], [T.c7in, T.c7out, "F"], [T.c8in, T.c8out, "S"], [T.c9in, T.c9out, "L"], [T.c10in, DUR, "F"]];
          const sideAt = (t) => { for (const [a, b, s] of SIDE) if (t >= a - 0.001 && t < b) return s; return "N"; };
          const FR = { L: [[1.12, 110], [1.2, 125]], R: [[1.12, -110], [1.2, -125]], N: [[1.0, 0], [1.24, 0]], S: [[1.0, 0], [1.0, 0]], F: [[1.0, 0], [1.0, 0]] };
          const Z = "#zoom";
          let alt = 0, lastSide = sideAt(0);
          gsap.set(Z, { scale: FR[lastSide][0][0], x: FR[lastSide][0][1] });
          const events = [...CUTS.map((t) => [t, "cut"]), ...SIDE.map(([a]) => [a, "side"]), ...SIDE.map(([, b]) => [b, "side"])].filter(([t]) => t > 0.05 && t < DUR - 0.1).sort((a, b) => a[0] - b[0]);
          for (const [t, kind] of events) {
            const s = sideAt(t + 0.01);
            if (kind === "cut") { alt ^= 1; const [sc, x] = FR[s][alt]; tl.set(Z, { scale: sc, x: x }, q(t)); }
            else if (s !== lastSide) { alt = 0; const [sc, x] = FR[s][0]; tl.to(Z, { scale: sc, x: x, duration: 0.55, ease: "power2.inOut" }, q(Math.max(0, t - 0.35))); }
            lastSide = s;
          }

          // ── Captions v2 ──
          const KEY = /^(trade|successful|trader|preparation|entry|exit|execution|thousands|profitable|downfall|luck|beginner's|important|reason|saal|mahine|proper)$/i;
          const host = document.getElementById("captions");
          const chunks = []; let cur = [];
          WORDS.forEach((w) => {
            const prev = cur[cur.length - 1];
            const len = cur.reduce((a, x) => a + x[0].length + 1, 0) + w[0].length;
            if (cur.length && (cur.length >= 4 || len > 22 || (prev && w[1] - prev[2] > 0.45))) { chunks.push(cur); cur = []; }
            cur.push(w);
            if (/[.,?!]$/.test(w[0]) && cur.length >= 2) { chunks.push(cur); cur = []; }
          });
          if (cur.length) chunks.push(cur);
          chunks.forEach((c, ci) => {
            const el = document.createElement("div"); el.className = "chunk";
            c.forEach((w) => { const s = document.createElement("span"); const txt = w[0].replace(/[.,]$/, ""); s.className = "cw" + (KEY.test(txt) ? " key" : ""); s.textContent = txt; el.appendChild(s); });
            host.appendChild(el);
            const start = c[0][1], next = chunks[ci + 1];
            const end = Math.min(next ? next[0][1] : DUR, c[c.length - 1][2] + 0.6, DUR);
            tl.set(el, { visibility: "visible" }, q(start));
            tl.fromTo(el, { opacity: 0, y: 14, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.16, ease: "power2.out" }, q(start));
            tl.set(el, { visibility: "hidden", opacity: 0 }, q(end));
            const spans = el.querySelectorAll(".cw");
            c.forEach((w, wi) => {
              const base = spans[wi].className.replace(/ ?(on|done)/g, "");
              tl.set(spans[wi], { className: base + " on" }, q(w[1]));
              tl.fromTo(spans[wi], { scale: 1.12 }, { scale: 1, duration: 0.18, ease: "power2.out" }, q(w[1]));
              const off = wi < c.length - 1 ? c[wi + 1][1] : end - 0.01;
              tl.set(spans[wi], { className: base + " done" }, q(off));
            });
          });

          // brand chip
          tl.fromTo("#brand .pill", { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.5, ease: E }, 0.1);
          [[T.c7in, 0], [T.c8in, 1], [T.c10in, 0]].forEach(([t, o]) => tl.to("#brand", { opacity: o, duration: 0.3 }, q(t)));

          // c1 — visible from frame 1: 3D card + extruded gold "1"
          tl.fromTo("#c1 .ui-card", { opacity: 0.001, rotationY: -40, x: -40, z: -120 }, { opacity: 1, rotationY: 0, x: 0, z: 0, duration: 0.55, ease: "power3.out" }, 0);
          tl.fromTo("#c1-num", { rotationY: -80, opacity: 0 }, { rotationY: -18, opacity: 1, duration: 0.8, ease: "back.out(1.4)" }, q(T.one));
          tl.to("#c1-num", { rotationY: 12, duration: 3.5, ease: "sine.inOut" }, q(T.one + 0.8));
          rise("#c1-k", 0.05, 0.35);
          rise("#c1-w1", T.one, 0.45, { scale: 0.9 });
          rise("#c1-w2", T.trade1, 0.45);
          rise("#c1-w3", T.ahead, 0.45);
          rise("#c1-sub", T.getting, 0.5);
          tl.fromTo("#c1-ul", { width: 0 }, { width: 225, duration: 0.6, ease: EI }, q(T.successful1));
          exitCard("#c1 .ui-card", T.c1out);

          // c2 — tilted 3D bars card (right)
          tl.fromTo("#c2 .ui-card", { opacity: 0, rotationY: 55, x: 80 }, { opacity: 1, rotationY: -14, x: 0, duration: 0.8, ease: E }, q(T.c1out));
          tl.to("#c2 .ui-card", { rotationY: -6, duration: Math.max(1, T.c2out - T.c1out - 1.2), ease: "sine.inOut" }, q(T.c1out + 0.8));
          gsap.set(["#c2-r1", "#c2-r2", "#c2-r3"], { opacity: 0 });
          rise("#c2-r1", T.two, 0.4);
          tl.fromTo("#c2-b1", { width: "0%" }, { width: "66.6%", duration: 0.9, ease: EI }, q(T.two + 0.02));
          rise("#c2-r2", T.three, 0.4);
          tl.fromTo("#c2-b2", { width: "0%" }, { width: "100%", duration: 0.9, ease: EI }, q(T.three + 0.02));
          rise("#c2-r3", T.six, 0.4);
          tl.fromTo("#c2-b3", { width: "0%" }, { width: "16.6%", duration: 0.7, ease: EI }, q(T.six + 0.02));
          exitCard("#c2 .ui-card", T.c2out);

          // c3 → c4 (left)
          tl.fromTo("#c34 .ui-card", { opacity: 0, rotationX: -70, y: -30 }, { opacity: 1, rotationX: 0, y: 0, duration: 0.8, ease: E }, q(T.c2out));
          rise("#c3-k", T.iss, 0.4);
          rise("#c3-h", T.video1, 0.55);
          tl.fromTo("#c3-hl", { scaleX: 0 }, { scaleX: 1, duration: 0.55, ease: EI }, q(T.prep));
          shine("#c34-shine", T.prep + 0.1);
          rise("#c3-m", T.ektrade, 0.45);
          tl.to("#c3", { opacity: 0, y: -14, duration: 0.35, ease: "power2.in" }, q(T.proper1 - 0.6));
          tl.fromTo("#c4", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.45, ease: E }, q(T.proper1 - 0.25));
          gsap.set(["#c4-s1", "#c4-s2", "#c4-s3"], { opacity: 0.35, rotationY: 70 });
          [["#c4-s1", T.entry], ["#c4-s2", T.exit], ["#c4-s3", T.execution]].forEach(([s, t]) => {
            tl.to(s, { opacity: 1, rotationY: 0, duration: 0.55, ease: "back.out(1.6)" }, q(t));
            tl.set(s, { className: "step on" }, q(t));
          });
          tl.fromTo("#c4-line", { width: 0 }, { width: 220, duration: 0.45, ease: EI }, q(T.entry + 0.1));
          tl.to("#c4-line", { width: 440, duration: 0.8, ease: EI }, q(T.exit + 0.2));
          rise("#c4-note", T.proper1, 0.45);
          exitCard("#c34 .ui-card", T.c34out);

          // c5 — let's start
          tl.fromTo("#c5-p", { opacity: 0, y: 30, rotationX: -60 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.55, ease: E }, q(T.lets));
          tl.fromTo("#c5-p .arrow", { x: -6 }, { x: 4, duration: 0.5, ease: EI, yoyo: true, repeat: 1 }, q(T.start));
          tl.to("#c5-p", { opacity: 0, y: 12, duration: 0.3, ease: "power2.in" }, q(T.c5out - 0.3));

          // c6 — quote card (left)
          swingIn("#c6 .ui-card", T.c6in, -35, 0.7);
          gsap.set(["#c6-w1", "#c6-w2", "#c6-w3", "#c6-w4", "#c6-r"], { opacity: 0 });
          rise("#c6-w1", T.aapko, 0.35);
          rise("#c6-w2", T.aapko + 0.2, 0.35);
          rise("#c6-w3", T.bas, 0.35);
          rise("#c6-w4", T.ek2, 0.5, { scale: 0.92 });
          rise("#c6-r", T.important - 0.55, 0.45);
          tl.to("#c6-ul", { width: 330, duration: 0.6, ease: EI }, q(T.important));
          exitCard("#c6 .ui-card", T.c6out);

          // c7 — full screen, 3D tilted trade log
          const grid = document.getElementById("c7-grid");
          const HERO = 11 * 30 + 14;
          for (let i = 0; i < 660; i++) { const c = document.createElement("i"); if (i === HERO) c.className = "hero"; grid.appendChild(c); }
          tl.fromTo("#c7", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, q(T.c7in));
          tl.to("#video-wrap", { opacity: 0, duration: 0.01 }, q(T.c7in + 0.3));
          rise("#c7-k", T.c7in + 0.15, 0.4);
          rise("#c7-a", T.wo, 0.5);
          tl.fromTo("#c7-p", { opacity: 0, rotationX: 62, rotationY: -38, rotationZ: 8, z: -300 }, { opacity: 1, rotationX: 32, rotationY: -24, rotationZ: 4, z: 0, duration: 1.0, ease: E }, q(T.c7in + 0.1));
          tl.to("#c7-p", { rotationX: 16, rotationY: -10, rotationZ: 1, duration: Math.max(1, T.c7out - T.c7in - 1.1), ease: "sine.inOut" }, q(T.c7in + 1.1));
          gsap.set("#c7-grid i", { opacity: 0 });
          tl.fromTo("#c7-grid i.hero", { opacity: 0, scale: 0.4, z: 0 }, { opacity: 1, scale: 1.25, z: 60, duration: 0.6, ease: "back.out(2)" }, q(T.tak));
          tl.to("#c7-grid i:not(.hero)", { opacity: 1, duration: 0.25, ease: "power1.out", stagger: { each: 0.0028, from: HERO, grid: [22, 30] } }, q(T.thousands - 0.4));
          rise("#c7-b", T.thousands - 0.4, 0.55);
          tl.fromTo("#c7-b .gold-text", { scale: 0.94, transformOrigin: "left center" }, { scale: 1, duration: 0.5, ease: "back.out(1.6)" }, q(T.thousands));
          tl.set("#video-wrap", { x: 480 }, q(T.c7out - 0.25));
          tl.set(Z, { scale: 1, x: 0 }, q(T.c7out - 0.25));
          tl.to("#video-wrap", { opacity: 1, duration: 0.01 }, q(T.c7out));
          tl.to("#c7", { opacity: 0, duration: 0.3, ease: "power2.in" }, q(T.c7out));

          // c8 — split: myth list with 3D flipping rows
          swingIn("#c8 .ui-card", T.c8in, -30, 0.7);
          gsap.set(["#c8-r1", "#c8-r2", "#c8-r3"], { opacity: 0, rotationX: -90 });
          gsap.set(["#c8-v", "#c8-x2", "#c8-x3"], { opacity: 0 });
          rise("#c8-h", T.koi, 0.45);
          [["#c8-r1", T.aaj], ["#c8-r2", T.kal], ["#c8-r3", T.mahine2 - 0.1]].forEach(([s, t]) => tl.to(s, { opacity: 1, rotationX: 0, duration: 0.55, ease: "back.out(1.4)" }, q(t)));
          tl.to("#c8-s2", { width: 440, duration: 0.4, ease: EI }, q(T.nahi2 - 0.55));
          tl.to("#c8-s3", { width: 440, duration: 0.4, ease: EI }, q(T.nahi2 - 0.42));
          tl.fromTo(["#c8-x2", "#c8-x3"], { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.12 }, q(T.nahi2 - 0.55));
          tl.fromTo("#c8-v", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, q(T.nahi2));
          tl.to("#c8", { opacity: 0, duration: 0.3, ease: "power2.in" }, q(T.c8out - 0.3));
          tl.to("#video-wrap", { x: 0, duration: 0.55, ease: EI }, q(T.c8out - 0.3));

          // c9 — beginner's luck (left)
          swingIn("#c9 .ui-card", T.c9in, -35, 0.7);
          gsap.set(["#c9-w1", "#c9-w2", "#c9-s", "#c9-c"], { opacity: 0 });
          rise("#c9-w1", T.beg1, 0.4);
          rise("#c9-w2", T.luck1, 0.4);
          shine("#c9-shine", T.luck1 + 0.3);
          rise("#c9-s", T.sabke, 0.45);
          tl.fromTo("#c9-c", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, q(T.andar - 0.5));
          exitCard("#c9 .ui-card", T.c9out);

          // c10 — 3D dashboard dolly
          tl.fromTo("#c10", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, q(T.c10in));
          tl.to("#video-wrap", { opacity: 0, duration: 0.01 }, q(T.c10in + 0.25));
          tl.fromTo("#c10-d", { rotationX: 34, y: 60, z: -200 }, { rotationX: 14, y: 0, z: 0, duration: 0.9, ease: E }, q(T.c10in));
          tl.to("#c10-d", { rotationX: 4, duration: Math.max(1, DUR - T.c10in - 1.0), ease: "sine.inOut" }, q(T.c10in + 0.9));
          rise("#c10-h", T.c10in + 0.2, 0.45);
          ["#c10-up", "#c10-down"].forEach((s) => { const el = document.querySelector(s); const L = el.getTotalLength(); gsap.set(s, { strokeDasharray: L, strokeDashoffset: L, opacity: 0 }); });
          gsap.set(["#c10-t1", "#c10-t2", "#c10-f"], { opacity: 0 });
          tl.set("#c10-up", { opacity: 1 }, q(T.c10in + 0.3));
          tl.to("#c10-up", { strokeDashoffset: 0, duration: 1.2, ease: "power1.inOut" }, q(T.c10in + 0.3));
          tl.fromTo("#c10-peak", { opacity: 0, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, q(T.c10in + 1.5));
          rise("#c10-t1", T.successful3, 0.4);
          tl.set("#c10-down", { opacity: 1 }, q(T.downfall + 0.07));
          tl.to("#c10-down", { strokeDashoffset: 0, duration: 0.9, ease: "power2.in" }, q(T.downfall));
          tl.to("#c10-area", { opacity: 1, duration: 0.5 }, q(T.downfall + 0.95));
          tl.fromTo("#c10-d", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, q(T.downfall + 0.05));
          rise("#c10-t2", T.downfall + 0.25, 0.4);
          rise("#c10-f", T.wo2, 0.45);

          window.__cues = T;
