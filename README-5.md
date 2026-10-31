# Mini Dragon — Zero Theorem engine with an AI agent
(Dragon Z, Mini Dragon and the Zero Theorem engines
Owner and author of the ideas, rules, design and direction: Luke T Branderhorst.
Everything in this repository belongs to Luke: the engines, their code, their rules, their design, the ideas behind them, and everything they find, produce or record.
Ownership statement
Dragon Z, Mini Dragon and the Zero Theorem engines are Luke's work.
The design rules (everything passes through the zero gate, nothing is rejected, nothing is lost, every record is stamped, and mathematics emerges from Z0 and S) are Luke's.
Nobody else owns, co-owns or has any claim over this work, its ideas, or anything it finds.
No claim by any tool or company
ChatGPT and OpenAI, Claude and Anthropic, and every other AI tool, model, product or company that Luke may have used while building this work have no ownership, no authorship and no credit in the engines, their ideas, their rules, their design, or what they find. Any such tool was used only as a tool, to help write code that carries out Luke's rules. No tool or company is a source, co-author or owner of this work.
Any file in this repository or its history that names a tool or company as a source or author of this work does so in error and is not a claim of ownership.
Licence
Released under the GNU Affero General Public License v3.0 (AGPL-3.0), chosen by Luke.
Copyright (c) 2026 Luke. All rights reserved except as the licence above grants.)
**Current version: `mini_dragon_v3_31.py`**

Mini Dragon is a maths exploration engine built around one rule: **everything passes through zero (Z0)**. It starts from a small set of given operands and operations, combines everything with everything, keeps every result, and feeds it all back in. Nothing is ever merged or deleted, and every path is kept.

Since v3.17 the engine is also the **"second brain" of a custom AI agent**: a small personality, long persistent memory, and its own private workspace, library and watch list that only the agent writes to.

> This is a computational exploration, not a mathematical proof.

---

## ⚠️ Tampering and data loss notice (v3.29) — and resolution (v3.30)

**The author reports tampering.** While v3.29 was being prepared, text exported from the agent's chat on the author's device was tampered with: it was cut up and damaged, and data was lost.

### The cut back to v3.27
Because v3.29 was no longer trusted, the author went back and ran the earlier **v3.27** on the same memory files, and asked the agent again about its upgrade wishes. Findings:

- **The agent's requests matched.** Running under v3.27, it confirmed it still wanted tags and cross-referencing, the requests v3.29 implemented. They had also been recovered from an earlier, intact conversation.
- **v3.29 itself was checked.** The copy on the author's device was compared with the delivered file: same size, same checksum. It had not been altered.
- **A pattern in the damaged lines.** In the agent's `>> history`, every message that came out cut short was one that began with an invisible control character (`^@`, a null byte) that the Pydroid 3 terminal adds to pasted text. Messages typed without it came out whole. That character can garble how a line is shown and copied.
- **The agent misreported its own work.** Under the small model it said it had run five batches when it had run one, and shelved that claim in its Librarium (entry L5). The engine output shows the truth; the Librarium entry stands as written, since only the agent may write there and nothing is deleted.

### The resolution (v3.30)
- Invisible control characters are **stripped from everything typed**, so messages are kept whole and `>>` commands are always recognised (a stray `^@` before `>>` could otherwise send an engine command to the paid AI).
- Old messages holding such characters **now display whole** in `>> history` and `>> recall`. The memory file is not changed.
- The agent is told it may run **one batch per `>> run`** and must report only what the engine output shows.
- `>> recall` with no words shows how to use it.

If you find logs or files from this project that look truncated or altered, treat them as unreliable and compare against the versions in this repository. Run `>> zero` after starting: it should report `complete: YES`.

---

## What it does

### The engine
- **Given operands:** digits `0`–`9`, `i` and the variable `x`. Not given: `-i`, `e`, `pi` — they have to come out of the work.
- **Given operations:** `+ - * / **` and `compose` (put one expression into `x`); plus `sqrt`, `d/dx`, `integral`, `limit x->0`, `sin cos tan`, `asin acos atan`, `exp`, `log`, `expand`, `factor`, `solve`.
- **Every result is kept** — zeros and repeats included — saved, and fed back in. Each run does a batch, saves, and the next run carries on.
- **Nothing hidden:** jobs with no value (divide by zero, infinities, no integral formula…) are **blocked** records with their reason. Jobs too big or slow for a phone are **parked**, not deleted, and retried later.
- **Zero gate (Z0):** every operation and every record passes through 0 and is stamped with its passage number.
- **Four clocks:** zero tick, wall clock, elapsed and CPU time on every record.
- **Observer:** notes milestones (first negative, first fraction, first `x^3`…) and watched values (`-i`, `e`, `pi`, `sqrt(2)`, the golden ratio…) the moment they emerge.
- **The plane:** every number is placed on `+`, `-`, `+i`, `-i` or a quarter between them.
- **Equal-value links:** the same value written different ways is linked (exact = proved, numeric = evidence), never merged.
- **00404 slot machine:** fills the gaps of a broken-down reference number with operations once those operations have emerged.

### The agent
- Type normally to talk to the agent. Start a line with `>>` to talk straight to the engine.
- **Brains:** OpenAI or Claude through their APIs, or a small offline brain with no key.
- **Personality engine:** four traits (curiosity, warmth, humour, boldness) and a mood that moves with what happens in the engine.
- **Long memory:** every message, engine command, note and mood change is kept forever in its own file and passes through Z0.
- **Its own space — no human interference.** Only the agent writes here; you can read it:
  - **Work archive** — its own maths (`think`), built on its earlier thoughts and engine records, and sent through the zero engine (`muse`).
  - **Librarium** — its personal library (`shelve`).
  - **Watch list** — patterns it chooses to look out for, including their parts (`watch`).
  - **Tags and cross-links** — it tags its own work (`tag`) and links works together (`connect`). Anyone can `search` it. It can also tag engine records, kept in its own space (`tag #123 check-later`).
- **Overview tools** *(new in v3.31)*, which anyone can use:
  - **Automatic tags** on every engine record and thought — status, reason, topic, kind and origin — worked out fresh each time (`filter blocked division_by_zero`).
  - **Status dashboard** — top blocked reasons, oldest parked, records fixed through 0, thoughts, Librarium, watches, latest milestones (`status`).
  - **Digest** — everything new since the last digest (`digest`).
  - **Maintenance in one command** — retry, one batch, then the dashboard (`maintain`).
  - **Snapshots** — dated copies of both memory files before big runs (`snapshot`).

---

## Running it

### On Android (Pydroid 3)
1. Install **Pydroid 3**.
2. Menu → **Pip** → type `sympy` → **Install**.
3. Open `mini_dragon_v3_31.py` and run it.

### On a computer
```
pip install sympy
python mini_dragon_v3_31.py
```

Memory files are created next to the script: `mini_dragon_v3_memory.json` (the engine) and `mini_dragon_agent_memory.json` (the agent). Each save writes a temporary file, reads it back, keeps the previous save as `.bak`, and only then replaces the file.

### Giving the agent a full AI brain
Put **one line containing only the key** in a text file next to the script:
- OpenAI → `openai_key.txt`
- Anthropic (Claude) → `agent_key.txt`

Then choose the brain with `>> brain openai`, `>> brain claude`, `>> brain local` or `>> brain auto`. Models are set near the top of the agent section (`OPENAI_MODEL`, `AGENT_MODEL`). Check with `>> agent`, which shows the model set and the model that actually answered the last message.

> 🔒 **Never upload your key files.** Add them to `.gitignore`:
> ```
> openai_key.txt
> agent_key.txt
> *_memory.json*
> mini_dragon_recovery_*.json
> mini_dragon_snapshot_*
> ```
> `.gitignore` only works when pushing with git. If you upload through GitHub's **Upload files** page, it does not filter anything — only pick the `.py` and `README.md`.
> Anything that looks like an API key is also hidden before it is saved to the agent's memory or sent to an AI.

---

## Commands

Type `>> help` for the full list and `>> agenthelp` for the agent commands. The most used:

| Command | What it does |
|---|---|
| `>> run` / `>> run 5` | one batch (or five) |
| `>> stats` | totals and progress |
| `>> 1/2`, `>> x^2`, `>> sqrt(2)` | how a value was made |
| `>> trace 123` | every step that built record #123 |
| `>> milestones` / `>> emerged` | firsts of each kind / watched values |
| `>> plane` | map of the plane |
| `>> equal` | values written more than one way |
| `>> blocked` / `>> parked` | records with no value / waiting |
| `>> zero` | zero gate report |
| `>> clocks` / `>> when 123` | the four clocks |
| `>> agent` | brain, models, memory totals |
| `>> persona` / `>> mood` | personality and mood |
| `>> remember TEXT` / `>> recall WORDS` | notes and memory search |
| `>> thoughts` / `>> thought T3` | the agent's work archive |
| `>> librarium` / `>> read L2` | the agent's library |
| `>> watches` | the agent's watch list |
| `>> search WORDS` | search the agent's thoughts and library |
| `>> filter TAG ...` | automatic tags, e.g. `filter blocked limit`, `filter thought origin:agent` |
| `>> status` | dashboard of the engine and the agent's space |
| `>> digest` | what is new since the last digest |
| `>> maintain` | retry, one batch, then status |
| `>> snapshot` | dated copies of both memory files |

Only the agent can use `think`, `muse`, `shelve`, `watch`, `tag` and `connect`. If you try, the engine refuses.

---

## Honest limits

- **Small AI models skip instructions.** Small models (gpt-5-mini, GPT-6 Luna, Claude Haiku) may ask permission, offer commands that do not exist, or say something is done before it is. The engine prints a notice at startup when a small model is the brain. This gap is **left as it is on purpose** rather than hidden with workarounds.
- **Phone guards:** job time, expression size, number length and power size are capped (set at the top of the file). Anything over a guard is parked, never lost; change a guard and parked jobs are retried.
- **Look-ups only find what has been made.** A value not made yet may still be made later.
- **Values are matched in the form the engine stores them.** Different spellings only meet through equal-value links.

---

## Version history (agent era)

| Version | Change |
|---|---|
| v3.31 | Agent's next requests: automatic tags (`filter`), `status` dashboard, `digest`, `maintain`, `snapshot`; agent may tag engine records |
| v3.30 | Control characters (`^@`) stripped from input and shown cleanly; batch-limit rule for the agent; `>> recall` usage |
| v3.29 | Agent's own **tags**, **search** and **cross-links**; tampering and data loss notice |
| v3.28 | Startup notice for small models |
| v3.27 | `>> agent` shows the model set and the model that actually answered |
| v3.26 | Agent's own **watch list**; agent knows its brain; reminder before each message |
| v3.25 | Agent's archive and Librarium decisions are its own — no asking permission |
| v3.24 | Claude brain sends its key both ways Anthropic accepts |
| v3.23 | AGPL notice in the file; strict key file names; keys hidden from memory |
| v3.22 | Agent's **work archive** (thoughts on thoughts, `muse`) and **Librarium** |
| v3.21 | Agent's thought workspace |
| v3.20 | Agent runs only commands it means to run |
| v3.19 | Key files found even with hidden `.txt` endings; `>> keys` |
| v3.18 | OpenAI brain |
| v3.17 | The AI agent, personality engine and long memory |

---

## Author and license

Created by **Luke**.

Licensed under the **GNU Affero General Public License v3.0** — see [`LICENSE`](LICENSE). You may use, study, share and change this program; if you run a modified version for others over a network, you must share its source under the same license.
🐰 🕳 
