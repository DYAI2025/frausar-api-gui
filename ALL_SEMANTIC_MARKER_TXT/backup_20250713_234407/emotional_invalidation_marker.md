marker: EMOTIONAL_INVALIDATION_MARKER.yaml

beschreibung: >
  Erkennt kommunikative Muster des emotionalen Invalidierens, bei dem Gefühle und Wahrnehmungen
  der anderen Person abgesprochen oder bagatellisiert werden, um deren Realität infrage zu stellen.

beispiele:
  - "Das ist doch alles nur in deinem Kopf."
  - "Wieder mal überreagierst du total."
  - "Du bist einfach zu empfindlich."
  - "So schlimm ist es doch gar nicht, stell dich nicht so an."
  - "Warum nimmst du immer alles persönlich?"
  - "Du machst aus allem ein Drama."

semantic_grab:
  description: "Erkennt Muster für emotional_invalidation_marker.py"
  patterns:
    - rule: "AUTO_PATTERN"
      pattern: r"(muster.*wird.*ergänzt)"

  tags: [emotional_invalidierend, gaslighting, manipulativ, neu_erstellt, needs_review]

