---
name: compose-nigun
description: Compose a brand-new, original melody in one of two styles — Sephardic-Andalusian or the style of Baal HaSulam's nigunim — (asking the user which first) for the "Staff to Keys" piano app and add it to the NIGUNIM list in index.html. Use this whenever the user asks for a new song, tune, nigun, niggun or melody "in that style", "like the Psalm 23 one", for a psalm (Tehillim), prayer or verse, or says things like "write me another one", "make a new song for the app", "compose something in freygish/Hijaz", "a new song like Baal HaSulam's / like Chamol or Pitchu Li" — even if they don't say "nigunim" or "add it". Also use it when they want to learn a song from a YouTube video or recording whose melody isn't clearly traditional: offer an original tune in that style instead of copying it.
---

# Compose a new nigun for Staff to Keys

The goal: write a fresh melody the user can learn on piano, in the musical style they asked for, and drop it straight into the app's song list (`NIGUNIM` in `index.html`) so it shows up after a page reload.

## 1. Keep it original

The melody must be your own new tune. Don't transcribe, download, or rebuild a melody from a recording, video, or modern song, and don't "change a few notes" of an existing tune — style is free to borrow, specific melodies aren't. If the user points at a recording, use only the *style* they describe (mode, mood, tempo, instruments named in the title) — there's no need to listen to it.

Words (the `words` field) may only be public-domain texts: Tanakh (Tehillim etc.), siddur/liturgy, or the user's own words. Keep it to a verse or two with a source in parentheses, e.g. `(תהלים כג, א–ב)`. Leave `words` out if unsure.

Name it honestly: `by` = "Original tune in the <style> style" (e.g. "Original tune in the slow Hasidic style"), and `attribText` says it's a new melody written for this page.

## 2. Ask the user which style

Before writing anything, ask with the AskUserQuestion tool (one question, two options) — even if a style was used earlier in the conversation, because the user wants to choose each time:

- **Sephardic-Andalusian** — Middle-Eastern Hijaz sound, like "Mizmor LeDavid (Psalm 23)".
- **Baal HaSulam style** — like "Chamol Al Ma'asecha" and "Pitchu Li" in the Baal HaSulam section.

If the user hasn't said which text or psalm the song is for, ask that in the same AskUserQuestion call (a second question, e.g. a few psalm suggestions; "Other" lets them type their own). Then follow the matching style below.

### Sephardic-Andalusian

- Mode: E freygish (Hijaz): E F G♯ A B C D. The F–G♯ step is the signature sound.
- Chords: Andalusian cadence Am–G–F–E; Dm–E; phrases end on E over an E chord.
- Lines move mostly by step, with short 16th-note turns. Tempo 60–76, 4/4.
- Shape the parts as a story, e.g. calm → dark (walk down Am–G–F–E) → confident and high.

### Baal HaSulam style

Modeled on the two real Baal HaSulam nigunim already in the app (`chamol` and `pitchu` in NIGUNIM — read them in index.html to hear the style in your head, but write new phrases; don't reuse their bars or motifs). What gives them their sound:

- **Mode and colour change:** start in a minor or freygish colour (e.g. A freygish with B♭ and C♯ inside D minor, or plain D minor), then a later part **opens up into the major** (D major) or climbs to the high register for a bright, uplifted section. Pick one: minor-only and inward (like Pitchu Li), or freygish → major (like Chamol).
- **Chords:** D minor with the descending B♭–C–Dm cadence, Gm–A7–Dm, A7 as the turn-back chord; in the major part D–G–A7.
- **Rhythm:** a run of 8th notes falling by step that lands on a long held note (half or dotted half) — "quick words, then a long sigh". Repeated notes on the same pitch for declaiming the words (`D5/q D5/q F5/q`). Dotted 8th + 16th pick-ups into the next phrase (`D5/8. E5/16`). Short rests inside a phrase as breaths.
- **Form:** a refrain part that comes back between new parts (e.g. A, B, C, B, D, B — vary the refrain's first bar a little each time), and/or parts with first and second endings: give the ending sections `"volta": 1` / `"volta": 2` and list them in `form` right after their part (e.g. `"A", "A-end1", "A", "A-end2"`).
- **Meter:** mostly 4/4, with an occasional `[3/4]` bar to stretch a phrase (switch back with `[4/4]`). A triplet ornament (`T3[ C5/16 D5/16 C5/16 ]`) here and there.
- Tempo 72–84, 3–4 parts, 8 bars each (an ending section is 1 bar). Words: a psalm verse or a short piyyut line.
- Write `by` as "Original tune in the style of Baal HaSulam's nigunim" — an original tune must not appear under his name.

Writing tips that make it sound right and stay learnable:
- 2–3 parts (A, B, C), 4 or 8 bars each. `form` decides what actually plays, so list a part twice to play it twice; `"rep": 1` only draws repeat signs on the sheet, so add it to the parts you list twice.
- Range about one and a half octaves, mostly C4–F5, mostly steps with a few leaps of a 3rd/4th/5th.
- Give each part a mood (e.g. calm → dark → confident) and say so in `about`.
- Ornaments as short 16th-note turns (`B4/16 C5/16`), sparingly.
- Final note of the song is the mode's home note, held long.

## 3. Write the song JSON

Save it to a temp file (e.g. in the scratchpad), not into the repo. Shape — this is the real Psalm 23 entry trimmed down:

```json
{
  "id": "mizmor23", "t": "Mizmor LeDavid (Psalm 23)", "short": "Mizmor 23", "he": "מזמור לדוד",
  "by": "Original tune in Sephardic-Andalusian style", "group": "ai",
  "attribText": "A new melody written for this page in the Sephardic-Andalusian style (E freygish). The words are Psalm 23.",
  "key": "E freygish", "time": 4, "tempo": 66, "pick": "",
  "sec": [
    {"id": "A", "lab": "A", "rep": 1,
     "n": "E4/q F4/8 G#4/8 A4/h | B4/8 A4/8 G#4/8 A4/8 F4/q E4/q",
     "c": "E | Dm E"},
    {"id": "B", "lab": "B",
     "n": "A4/q A4/8 B4/8 C5/q C5/q | D5/8 C5/8 B4/8 A4/8 B4/h",
     "c": "Am | G"}
  ],
  "form": ["A", "A", "B"], "lev": 2,
  "warm": ["E4", "F4", "G#4", "A4", "B4"], "warmName": "E freygish: E F G♯ A B",
  "about": "Plain-English description of the mood of each part, for the player.",
  "words": "מִזְמוֹר לְדָוִד: ה׳ רֹעִי לֹא אֶחְסָר (תהלים כג, א)"
}
```

Field notes:
- `id`: new, lowercase, no spaces. `he`: Hebrew title. `short`: ≤ ~14 characters.
- `group`: always `ai`. Every song this skill makes goes in the "AI created" section of the Nigunim page, so it's never mixed up with real traditional nigunim (the script refuses any other group).
- `key`: "<Note> freygish", "<Note> minor", etc. The text before " (" shows on the song card.
- `time` = quarter-note beats per bar; `tempo` = bpm. `lev` 1–5 = difficulty.
- `warm`: the 5 notes under the right hand (thumb to pinky) for the warm-up; `warmName` names them.
- `pick`: optional pick-up bar (shorter than a full bar), e.g. `"A4/8"`.

Note format (`n`): bars separated by `|`. Token = `<pitch>/<dur>[/<finger>][~]`, pitch like `C#5`, `Bb4`, or `R` for a rest. Durations: `w h. h q. q 8. 8 16`. `~` ties to the next note. `[3/4]` at the start of a bar changes the meter; `T3[ ... ]` is a triplet. Every bar must add up exactly to the meter.

Chords (`c`): one `|`-separated group per bar, 1–2 chords per bar, names matching `^[A-G](b|#)?(m|dim)?7?$` (e.g. `E`, `Am`, `Bb`, `F#dim`, `A7`). Choose chords that contain the melody's strong-beat notes.

## 4. Check and add it

Run the bundled script from the repo root. It checks every bar's length, chord names, bar counts, form, unique id, and then appends the song to the end of `NIGUNIM`:

```bash
python3 -I .claude/skills/compose-nigun/scripts/add_song.py <song.json> index.html --check   # check only
python3 -I .claude/skills/compose-nigun/scripts/add_song.py <song.json> index.html           # check + add
```

The second argument can be any copy of index.html (handy for trying things out). If it prints "NOT ADDED", fix the listed problems and rerun. After adding, it also checks that the page's script still parses ("Page script check: OK"); if that fails, undo with `git checkout index.html` and look again.

## 5. Tell the user

Short and plain: the song's name, mode, tempo, what each part feels like, that it's in the Nigunim page under "AI created", and to reload the page. Offer tweaks (slower, lower, longer, more ornaments). Don't commit unless asked; if asked, commit message describes the new song in plain words.
