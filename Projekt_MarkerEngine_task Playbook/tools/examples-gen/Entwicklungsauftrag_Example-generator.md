# Aufgabenanforderung: Epic – Semantischer Wächter & Beispiel-Generator (Lean-Deep 3.1)

**Epic-ID:** EPIC-KB-002  
**Titel:** Semantischer Wächter: Intelligente Beispiel-Generierung unter Einhaltung der Lean-Deep 3.1 Doktrin  
**Adressat:** Claude Opus 4.0 / Codex / Team

---

## 1. Kontext und Semantische Direktive

Im Projekt **MarkerEngine_WordsThread** entwickeln wir ein Tool, das die unsichtbaren Architekturen von Einflussnahme, Manipulation und Kontrolle in der Sprache entschlüsselt. Die Integrität unserer Marker-Knowledge-Base ist dabei unser höchstes Gut.

> **Wichtig:** Ein fehlerhafter oder mehrdeutiger Marker ist aktiv schädlich und kann zu falschen Analysen führen.

**Deine Aufgabe:**  
Einen Prozess schaffen, der zwei Ziele verfolgt:

- **Schützen (Der Wächter):** Die semantische Reinheit der Marker-Definitionen bewachen und problematische Marker erkennen.
- **Anreichern (Der Generator):** Nur für semantisch klare Marker realitätsnahe, vielfältige Beispiele generieren.

Dieses Tool ist der semantische Immunschutz unseres Ökosystems.

---

## 2. Kernprinzipien

- **Semantische Treue:** Jedes Beispiel muss den vierdimensionalen Frame exakt widerspiegeln. Keine Abweichungen!
- **Qualität vor Quantität:** Keine Beispiele für mehrdeutige Marker. Lieber kein Beispiel als ein schlechtes.
- **Lean-Deep 3.1 als einziges Schema:** Nur die Lean-Deep 3.1 Spezifikation ist zulässig. Ältere Felder wie `level` oder `marker_name` sind verboten.

---

## 3. Feature-Beschreibung: Der zweistufige Prozess

**Als Marker-Kurator möchte ich ein Tool, das für jede Marker-Datei folgendes tut:**

### Stufe 1: Validierung & Eignungsprüfung (Der Wächter)
- Analysiert den Frame (`signal`, `concept`, `pragmatics`, `narrative`)
- Prüft auf Klarheit, Kohärenz und Spezifität
- Bei Unklarheit:  
    > **GENERIERUNG ABGELEHNT: Marker-Frame ist semantisch nicht eindeutig.**

### Stufe 2: Konfigurierbare Beispiel-Generierung (Der Generator)
- Nur bei erfolgreicher Validierung
- Generiert eine konfigurierbare Anzahl neuer, hochwertiger Beispiele
- Bewertet die eigenen Beispiele und verwirft ungeeignete

---

## 4. Detaillierte Anforderungen

- **Input/Output:**  
    - Verarbeitet einzelne oder mehrere `.yaml`-Dateien
    - Ergänzt Beispiele und speichert die Datei unverändert (inkl. Kommentare)
- **Konfigurierbare Anzahl:**  
    - Anzahl der Beispiele als Parameter (z.B. `generate_examples(file, num_examples=5)`)
- **Inkrementelle Anreicherung:**  
    - Bestehende Beispiele bleiben erhalten, neue werden angehängt
- **Qualitätssicherung:**  
    - Vorher: Kohärenzprüfung des Frames
    - Nachher: Selbstbewertung der Beispiele  
        > Bei weniger als angefordert:  
        > **WARNUNG: Nur X von Y angeforderten Beispielen erfüllten die Qualitätsanforderung.**
- **Strikte Lean-Deep 3.1 Schema-Logik:**  
    - Nur das Feld `id` mit Präfix (A_, S_, C_, MM_)
    - Semantische Definition ausschließlich über den vierseitigen Frame
    - Nur ein Strukturblock: `pattern`, `composed_of` oder `detect_class`
    - Verbotene Felder (`level`, `marker_name`, `description`, `category`) führen zur Ablehnung

---

## 5. Praktisches Beispiel nach Lean-Deep 3.1

**Input (Vorher):**
```yaml
id: C_RELATIONAL_DESTABILIZATION_LOOP
frame:
    signal: ["Nähe/Distanz-Kontraste"]
    concept: "Bindungsambivalenz"
    pragmatics: "Destabilisierung"
    narrative: "loop"
composed_of: [S_AMBIVALENT_ATTACHMENT_SPEECH, S_SOFT_WITHDRAWAL]
activation: { rule: "ANY 2 IN 48h" }
scoring: { base: 2.0, weight: 1.6, decay: 0.01, formula: "logistic" }
tags: [beziehung, ambivalenz, loop]
examples:
    - [cite_start]"Ich vermisse dich … aber ich brauche Abstand." [cite: 277]
    - [cite_start]"Du bist mir wichtig – aber ich weiß nicht, ob ich bereit bin." [cite: 278]
```
**Befehl:**  
`generate_examples('C_RELATIONAL_DESTABILIZATION_LOOP.yaml', num_examples=3)`

**Output (Nachher):**
```yaml
id: C_RELATIONAL_DESTABILIZATION_LOOP
frame:
    signal: ["Nähe/Distanz-Kontraste"]
    concept: "Bindungsambivalenz"
    pragmatics: "Destabilisierung"
    narrative: "loop"
composed_of: [S_AMBIVALENT_ATTACHMENT_SPEECH, S_SOFT_WITHDRAWAL]
activation: { rule: "ANY 2 IN 48h" }
scoring: { base: 2.0, weight: 1.6, decay: 0.01, formula: "logistic" }
tags: [beziehung, ambivalenz, loop]
examples:
    - [cite_start]"Ich vermisse dich … aber ich brauche Abstand." [cite: 277]
    - [cite_start]"Du bist mir wichtig – aber ich weiß nicht, ob ich bereit bin." [cite: 278]
    # --- Neu generierte Beispiele ---
    - "Immer wenn wir uns nah sind, muss ich danach erst mal wieder für mich sein."
    - "Einerseits will ich dich, andererseits erdrückt mich das manchmal."
    - "Kannst du verstehen, dass ich beides zugleich fühle? Nähe und den Drang zu gehen?"
```

---

## 6. Acceptance Criteria (ACC) & Definition of Done (DoD)

**Acceptance Criteria:**
1. Das Tool fügt die korrekte, angeforderte Anzahl von Beispielen zu einer validen Marker-Datei hinzu.
2. Bestehende Beispiele bleiben unangetastet, neue werden angehängt.
3. Bei semantisch inkohärenter Datei verweigert das Tool die Arbeit mit klarer Fehlermeldung.
4. Bei zu wenigen validen Beispielen erfolgt eine Warnung.
5. Alle Dateien entsprechen zu 100 % dem Lean-Deep 3.1 Schema.

**Definition of Done:**
- Alle ACCs sind erfüllt und durch Tests abgedeckt.
- Der Prozess zur Qualitäts- und Kohärenzprüfung des Frames ist implementiert und dokumentiert.
- Die Funktionalität ist mit allen vier Marker-Ebenen (A, S, C, MM) erfolgreich getestet.

