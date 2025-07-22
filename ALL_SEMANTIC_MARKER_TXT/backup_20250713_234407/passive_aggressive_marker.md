marker: PASSIVE_AGGRESSIVE_MARKER.yaml

beschreibung: >
  Erkennt kommunikative Muster von passiv-aggressiven Aussagen, die Spannungen erzeugen,
  subtil Druck ausüben und Schuldgefühle induzieren.

beispiele:
  - "Ist ja nicht so, als wäre ich wichtig."
  - "Schon gut, ich verzichte eben."
  - "Tu, was du willst, mir ist es sowieso egal."
  - "Na klar, du musst es ja besser wissen."
  - "Ich sage lieber nichts, sonst heißt es wieder, ich sei schuld."
  - "Wenn du meinst, dass du das richtig machst..."

semantic_grab:
  description: "Erkennt Muster für passive_aggressive_marker.py"
  patterns:
    - rule: "AUTO_PATTERN"
      pattern: r"(muster.*wird.*ergänzt)"

  tags: [passiv_aggressiv, manipulativ, neu_erstellt, needs_review]

