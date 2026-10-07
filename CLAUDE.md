# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Staff to Keys": a single-page piano-learning app (sheet music → keyboard) focused on nigunim (Jewish melodies, with Hebrew titles). There is no build, no package manager, no tests, no linter. Everything lives in two files:

- `index.html` — the whole app: CSS in one `<style>` block, markup for six views, then one big IIFE `<script>` (`'use strict'`).
- `settings.js` — the app's only persistence: `window.STK_SETTINGS = {...}`, committed to git.

To run it, open `index.html` in a browser (or serve the folder statically, e.g. `python3 -m http.server`). USB MIDI and the "linked folder" Save need Chrome/Edge on a computer.

## Persistence model (important)

Nothing is stored in the browser. `index.html` loads `settings.js?v=<timestamp>` via `document.write` before the main script. At runtime:

- `SetFile` holds all state in an in-memory `Map` keyed by `stk.*` strings; `lsGet`/`lsSet` are the accessors (named after localStorage, but they do not touch it).
- `SETTINGS_MAP` maps the readable `display` keys in `settings.js` to internal `stk.*` keys, allowed values, and defaults. Adding a display setting means adding it here (and to the header comment that `Saver.fileText()` writes).
- `Store` is the progress document (`stk.progress.v1` → `progress` in the file). Change it via `Store.change(fn, quiet)`; listeners registered with `Store.on`.
- "quiet" writes (practice-time counter, last opened song) are kept but don't mark the page unsaved.
- `Saver` (end of the script) serializes everything back into a new `settings.js`, writing it into a folder picked once via the File System Access API (handle kept in IndexedDB), or downloading it as a fallback. The user then commits and pushes it.

Commits titled "Record practice session" are just updated `settings.js` files from the app's Save button.

## Script layout

The main script is organized into sections marked `/* ---------------- name ---------------- */`; grep for them to navigate. Main modules (mostly IIFE singletons):

- Core: pitch helpers, `Audio`, `Kb` (on-screen keyboard dock), `Seq` (timed playback), `Mode` (only one active tool at a time — tools call `Mode.set(tool)` and must implement `stop()`).
- Data: `NIGUNIM` — a large literal array of songs. `SONGS = NIGUNIM.map(buildSong)`. `MySongs` adds user-imported songs (MusicXML/MIDI) stored in `Store.s.my` and keeps `SONGS`/`NIGUNIM` in sync.
- Views: `View.go(name)` switches between `#v-today`, `#v-nigunim`, `#v-drills`, `#v-chords`, `#v-plan`, `#v-learn` (hash routing). Modules: `Today` (session builder/runner), `Player` (sheet music + learning ladder), drills, `ChordLib` (chord shapes/inversions → `chordShapes` in settings), `Plan` (12-week plan), learn.
- Extras: USB MIDI input, keyboard/page-turner pedal shortcuts, full screen, wake lock.

## Song notation format

Each song section has `n` (notes) and `c` (chords), with bars separated by `|`:

- Note token: `<pitch>/<dur>[/<finger>][~]`, e.g. `C#5/8`, `Bb4/q.`, `R/h` (rest). Durations: `w h. h q. q 8. 8 16` (see `DURS`). Trailing `~` = tie.
- `[3/4]` at the start of a bar changes the meter; `T3[ ... ]` is a triplet (nestable).
- Chords: names matching `^[A-G](b|#)?(m|dim)?7?$` (see `chordInfo`).
- Section fields: `rep` (repeat), `volta` (1st/2nd ending), `lab` (label).

## Gotchas

- `Store.connect()` (cloud sync via `window.claude.use('db')`) is never called — leftover code; the file is the only store.
- `Store.s.inv` is working-only and is stripped from `settings.js` on Save.
- The page keeps state in memory and overwrites `settings.js` on Save, so hand edits to the file are lost if the page is open. Reload the page after editing it.

## Conventions

- Code style is dense: short helper names (`$`, `$$`, `h`, `esc`, `clamp`), long one-line functions. Match it.
- Comments and UI text are written in plain, non-technical English for the end user (who is also the repo owner).
- Commit messages describe the user-visible change in plain words.
