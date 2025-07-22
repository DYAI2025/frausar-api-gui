marker: NAME\_MARKER.yaml

&#x20;

"beschreibung": (

"Erkennt kommunikative Muster von freundlich-sympathischem Flirten ohne Grenzüberschreitung. "\
\
Beispiele

"Ist ja nicht so, als wäre ich wichtig."

- Schon gut, ich verzichte eben."
- "Tu, was du willst, mir ist es sowieso egal."
- "Na klar, du musst es ja besser wissen."
- "Ich sage lieber nichts, sonst heißt es wieder, ich sei schuld."
- "Wenn du meinst, dass du das richtig machst..."\
  \
  semantic\_grab:

  description: "Erkennt Muster für social\_interaction.py"

  patterns:

  \- rule: "AUTO\_PATTERN"

  pattern: r"(muster.\*wird.\*ergänzt)"

  tags: [neu\_erstellt, needs\_review]
