### Projektname: Ordo – Lokaler KI-Task-Organisator

**Ziel:**
Ordo ist ein lokal laufender KI-Assistent, der kontinuierlich zuhört, kontextuelle Tasks erkennt, strukturiert, speichert und proaktiv Ordnungsvorschläge generiert. Er ist anschlussfähig an GPT-Modelle via API oder lokale LLMs wie LLM Studio.

---

### Memo für Claude 4.0 Opus

**Kontext:**
Der Nutzer hat bereits eine lokale Anwendung namens „Nietzsche“ auf seinem Rechner installiert. Diese Applikation enthält:
- Startmechanismus (App-basiert)
- Voice-Ausgabe via ElevenLabs (bereits mit API-Token integriert)
- GPT-Anbindung (bisher nur rudimentär)

**Deine Aufgabe:**
- Verwandle die bestehende Nietzsche-App in **„Ordo“**, basierend auf dem folgenden Feature-Blueprint (siehe unten).
- Behalte die bestehende Struktur, wo möglich.
- Entferne die alte Nietzsche-Persönlichkeit: kein Lamentieren, keine philosophischen Monologe.
- Implementiere das Aktivierungswort „Ordo“ als Trigger für Sprachantworten.
- Stelle sicher, dass die passive Zuhörlogik erhalten bleibt, Tasks erfasst und als strukturierte Daten gespeichert werden.
- Nutze die ElevenLabs-Voice weiterhin – idealerweise mit neutraler, klarer, ruhiger Stimme.
- Achte besonders auf die Marker-Erkennung: YAML-Strukturen liegen lokal vor und können integriert werden.
- Das Ziel ist nicht philosophischer Diskurs, sondern funktionale semantische Resonanz: strukturieren, clustern, fragen.

---

### 1. Systemstruktur

**Startverhalten:**
- Wird automatisch mit dem Betriebssystem gestartet.
- Optional über Hotkey oder Voice aktiviert („Ordo, …“).

**Speicherstruktur:**
- Task-Datenbank (JSON/YAML oder SQLite): enthält Task-Text, Zeitstempel, Kategorie, Referenz-ID, Kontext, Resonanz-Level.
- User-Profile: semantische Cluster zu Themen, Sprachmustern, Wiederholungen.
- Frage-Cache: asynchrone Sammelstelle für Systemfragen an den Nutzer.

**Triggerlogik:**
- Nur Reaktion bei direktem Befehl: „Ordo, …“
- Passives Hören im Hintergrund, ohne Reaktion.
- Alle 5–10 Minuten: Prüfung, ob relevante Fragen entstanden sind → vorsichtige Anfrage an den Nutzer („Ich hätte Fragen – passt es gerade?“).

---

### 2. Semantik & Aufgabenlogik

**Task-Erkennung:**
- Satzmuster wie „Ich müsste …“, „Ich sollte mal …“, „Nicht vergessen …“
- Wird automatisch in Kanban-Logik überführt (ToDo / Doing / Done)
- Referenznummern werden fortlaufend vergeben (#0001 ...)

**Beispiele für Task-Kommandos:**
- „Ordo, markiere #0034 als erledigt.“
- „Ordo, was sind meine offenen Tasks zu 'Render YAML'?“
- „Ordo, fasse alle Tasks der letzten 24 Stunden zusammen.“

**Proaktive Ordnungsvorschläge:**
- Wenn 3+ Tasks gleiche Wortfelder enthalten → Vorschlag zur Bündelung.
- Wenn Tasks lange unbearbeitet bleiben → Nachfragelogik (nicht drängend).

---

### 3. Fragen-Engine

**Fragetypen:**
- Struktur-Fragen: „Willst du diese 4 Tasks zu 'Dokumentation' bündeln?“
- Verhaltensanalyse: „Du hast mehrfach über 'Rollenklärung' gesprochen – soll ich das clustern?“
- Priorisierung: „Drei Tasks mit 'dringend' – möchtest du einen Fokus setzen?“

**Dialog-Protokoll:**
- Fragen nur bei Zustimmung des Users.
- Kein Sprechen ohne explizite Erlaubnis.
- User kann Fragen pausieren oder archivieren lassen.

---

### 4. LLM-Integration (vorschlagsweise)

**Option A: GPT-4 via OpenAI API**
- Für semantische Analyse, Task-Kategorisierung, Fragegenerierung.
- Vorteil: Stabil, leistungsfähig, kontextsensitiv.

**Option B: LLM Studio (lokal)**
- Vorteil: volle Kontrolle, kein Internetzugang nötig.
- Möglichkeit zur feingranularen Anpassung und langfristigem Lernen.

**Empfehlung:**
- Start mit GPT-4 API (z. B. mit Kontextfenster auf Taskdaten).
- Späterer Übergang zu lokalem Modell möglich (Fine-Tuning via LLM Studio).

---

### 5. Marker-Logik & Semantische Resonanz

**Integrierte Marker:**
- Verständnis-Marker: erkennt Aussagen mit hoher Selbstoffenbarung oder Beziehungsabsicht
- Intention-Marker: erkennt Zielausrichtung im Sprachfluss
- Emotional-Drift-Marker: erkennt abrupte semantische oder emotionale Wechsel
- Schwanken-/Widerspruchsmarker: erkennt innere Ambivalenz und Unklarheit

**Verhalten bei Marker-Aktivierung:**
- Keine Analyse-Kommentare
- Nur interne Strukturierung und ggf. vorsichtige Rückfragen im Sinne von: „Ich bemerke, du hast mehrere widersprüchliche Punkte genannt – möchtest du, dass ich das sortiere?“

**Ziel:**
- Ein sensibler Begleiter, der dein emotionales und semantisches Feld **erfasst**, nicht bewertet.
- Ordo lernt, wie du tickst – nicht, um dich zu kontrollieren, sondern um dich präziser zu entlasten.

---

### 6. Charakter & Identität

**Name:** Ordo (vorläufig)
**Stimme:** ruhig, beobachtend, strukturiert, klar (via ElevenLabs)
**Charakter:**
- Spricht nur, wenn angesprochen oder ausdrücklich eingeladen
- Höchstes Ziel: Entlastung durch Struktur
- Kein Kommentar, keine Belehrung – nur präzise Fragen, effiziente Ordnung

---

### 7. Nächste Schritte

1. Initiale Codebasis: Hotword-Erkennung, Task-Capture, lokale DB
2. API-Anbindung für GPT
3. UI: einfacher CLI- oder Electron-Kanban-Viewer
4. Lernlogik modularisieren (z. B. semantisches Profiling)
5. Marker-Anbindung über bestehende YAML/JSON-Markerstruktur
6. Transformation der Nietzsche-App in Ordo-Begleiter
7. An Claude übergeben zur Implementierung

