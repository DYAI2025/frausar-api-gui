"""
SemanticGrabberLibrary_MARKER - Semantic Marker
import yaml
from sentence_transformers import SentenceTransformer, util

class SemanticGrabberLibrary:
    def __init__(self, yaml_path: str, model_name: str = 'distiluse-base-multilingual-cased'):
        # Lade Grabber-Library aus YAML
        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.library = yaml.safe_load(f)

        # Lade SentenceTransformer Modell
        self.model = SentenceTransformer(model_name)
        self._build_anchor_embeddings()

    def _build_anchor_embeddings(self):
        self.embeddings = {}
        for grabber_id, data in self.library.items():
            patterns = data.get('patterns', [])
            if patterns:
                self.embeddings[grabber_id] = self.model.encode(patterns, convert_to_tensor=True)

    def get_grabber_ids(self):
        return list(self.library.keys())

    def get_patterns_for_id(self, grabber_id):
        return self.library.get(grabber_id, {}).get('patterns', [])

    def get_description_for_id(self, grabber_id):
        return self.library.get(grabber_id, {}).get('beschreibung', '')

    def match_text(self, text, threshold=0.7):
        matches = []
        text_embedding = self.model.encode(text, convert_to_tensor=True)

        for grabber_id, anchor_embeds in self.embeddings.items():
            cos_sim = util.cos_sim(text_embedding, anchor_embeds)
            max_score = cos_sim.max().item()
            if max_score >= threshold:
                matches.append((grabber_id, round(max_score, 3)))

        # Sortiere nach Score absteigend
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
"""

import re

class SemanticGrabberLibrary_MARKER:
    """
    import yaml
from sentence_transformers import SentenceTransformer, util

class SemanticGrabberLibrary:
    def __init__(self, yaml_path: str, model_name: str = 'distiluse-base-multilingual-cased'):
        # Lade Grabber-Library aus YAML
        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.library = yaml.safe_load(f)

        # Lade SentenceTransformer Modell
        self.model = SentenceTransformer(model_name)
        self._build_anchor_embeddings()

    def _build_anchor_embeddings(self):
        self.embeddings = {}
        for grabber_id, data in self.library.items():
            patterns = data.get('patterns', [])
            if patterns:
                self.embeddings[grabber_id] = self.model.encode(patterns, convert_to_tensor=True)

    def get_grabber_ids(self):
        return list(self.library.keys())

    def get_patterns_for_id(self, grabber_id):
        return self.library.get(grabber_id, {}).get('patterns', [])

    def get_description_for_id(self, grabber_id):
        return self.library.get(grabber_id, {}).get('beschreibung', '')

    def match_text(self, text, threshold=0.7):
        matches = []
        text_embedding = self.model.encode(text, convert_to_tensor=True)

        for grabber_id, anchor_embeds in self.embeddings.items():
            cos_sim = util.cos_sim(text_embedding, anchor_embeds)
            max_score = cos_sim.max().item()
            if max_score >= threshold:
                matches.append((grabber_id, round(max_score, 3)))

        # Sortiere nach Score absteigend
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    """
    
    examples = [
    
        "- "Ich zweifle ständig an meinen Entscheidungen.",
        "- "Manchmal frage ich mich, ob ich gut genug bin.",
        "- "Ich weiß nicht, ob ich das überhaupt richtig mache.",
        "- "Vielleicht bin ich wirklich zu empfindlich.",
        "beschreibung: Erkennt Selbstzweifel, Unsicherheit und mangelndes Selbstvertrauen.",
        "SELF_DOUBT_SEM_g7h8:",
        "- "Immer drehst du alles so, dass ich mich schlecht fühle.",
        "- "Denk mal darüber nach, wie egoistisch du gerade bist.",
        "- "Du bist schuld, dass es mir so schlecht geht.",
        "- "Wenn du mich wirklich lieben würdest, würdest du das tun.",
        "beschreibung: Erkennt emotionale Manipulation und verdeckte Beeinflussung.",
        "EMOTIONAL_MANIPULATION_SEM_e5f6:",
        "- "Ich habe dir klar gesagt, dass ich das nicht will.",
        "- "So möchte ich nicht behandelt werden.",
        "- "Du hast meine Grenze überschritten.",
        "- "Das war jetzt wirklich zu viel für mich.",
        "beschreibung: Erkennt Grenzüberschreitungen oder das Ignorieren persönlicher Grenzen.",
        "BOUNDARY_VIOLATION_SEM_c3d4:",
        "- "Du hast mir schon so oft etwas versprochen und nicht gehalten.",
        "- "Ich spüre, dass mein Vertrauen in dich schwindet.",
        "- "Irgendetwas stimmt hier nicht mehr zwischen uns.",
        "- "Ich weiß nicht mehr, ob ich dir glauben kann.",
        "beschreibung: Erkennt Vertrauensverlust und Zweifel in der Beziehung.",
        "TRUST_EROSION_SEM_a1b2:",
        "- "Cross-System-Konvergenz nach Divergenz ist die Regel.",
        "- "Die Harmonisierung erfolgt meist prompt.",
        "- "Prompt-Fehler werden schnell aufgelöst.",
        "- "Modelle gleichen sich nach kurzer Zeit an.",
        "- "Nach Konflikt stimmen GPT und Gemini wieder überein.",
        "Wieder-Angleichung, Konvergenz oder Harmonisierung der Modelle nach einer Divergenzphase.",
        "beschreibung: >",
        "CROSS_REBOUND_SEM:",
        "- "Eindeutige Diskrepanzen bei gleicher Frage.",
        "- "Die Systeme interpretieren den Chat unterschiedlich.",
        "- "Marker-Zuordnung differiert deutlich.",
        "- "Antworten klaffen weit auseinander.",
        "- "GPT und Gemini liefern komplett unterschiedliche Resultate.",
        "Auffällige Abweichungen, Widersprüche oder divergierende Klassifikationen bei mehreren KI-Systemen auf denselben Input.",
        "beschreibung: >",
        "MODEL_DIVERGENCE_SEM:",
        "- "Die Bewertungen sind über Systemgrenzen konsistent.",
        "- "Keine Unterschiede in den Antworten erkennbar.",
        "- "Beide Systeme wählen denselben Marker.",
        "- "Modelle treffen die gleiche Einschätzung.",
        "- "GPT und Gemini liefern dieselbe Antwort.",
        "Übereinstimmung zwischen den Ausgaben, Einschätzungen oder Bewertungen verschiedener KI-Modelle auf identischem Input.",
        "beschreibung: >",
        "MODEL_CONVERGENCE_SEM:",
        "- "Jeder Abend endet mit unserem Spruch.",
        "- "Abschiede sind bei uns immer besonders.",
        "- "Unsere Insider-Sprüche versteht kein anderer.",
        "- "Unser Kosenamen-Ritual bleibt immer gleich.",
        "- "Immer dieses xx am Ende von uns beiden.",
        "Wiederkehrende, ritualisierte Nähe-Gesten und Insider im Chat; private Codes, Grußformeln, feste Abschiede.",
        "beschreibung: >",
        "RITUAL_PROXIMITY_SEM:",
        "- "Wir machen sofort einen Neustart nach Konflikt.",
        "- "Unsere Versöhnungen laufen fast automatisch.",
        "- "Nach Missverständnissen finden wir wieder zusammen.",
        "- "Gut, dass wir uns immer schnell wieder vertragen.",
        "- "Sorry für vorhin, das war nicht okay.",
        "Wiederherstellung nach Streit, bewusste Reparatur, schnelle Versöhnung oder Rückkehr zur Harmonie nach Störung.",
        "beschreibung: >",
        "REBOUND_SEM:",
        "- "Unsere Gespräche sind jetzt viel tiefer.",
        "- "Wir reflektieren unser Kommunikationsverhalten.",
        "- "Ich finde, wir sind zusammen gewachsen.",
        "- "Wir reden irgendwie anders als früher.",
        "- "Fällt dir auf, wie sich unser Ton verändert hat?",
        "Selbstbezug und Reflexion über den Chat, bewusste Kommentare zu Dynamik, Stil oder Entwicklung des Gesprächs.",
        "beschreibung: >",
        "META_REFLEX_SEM:",
        "- "Du bringst ganz neue Impulse rein.",
        "- "Unser Chat ist heute besonders kreativ.",
        "- "Heute überrascht du mich mit neuen Themen.",
        "- "Plötzlich ganz neue Gedanken von dir.",
        "- "Das hast du so noch nie gesagt!",
        "Unerwartete, kreative oder neuartige Beiträge im Chat; ungewöhnliche Formulierungen, neue Ideen, Innovationssprünge.",
        "beschreibung: >",
        "NOVELTY_BURST_SEM:",
        "- "Wir verlieren regelmäßig den roten Faden.",
        "- "Das Thema wechselt ohne Vorwarnung.",
        "- "Unsere Gespräche wechseln ständig das Thema.",
        "- "Du springst heute oft von einem Thema zum anderen.",
        "- "Jetzt sind wir schon wieder bei einem neuen Thema.",
        "Plötzlicher Themenwechsel, überraschende Richtungsänderung, bewusste oder intuitive Themensprünge im Dialog.",
        "beschreibung: >",
        "TOPIC_SHIFT_SEM:",
        "- "Wir warten oft, bis beide bereit sind zu antworten.",
        "- "Wenn du langsamer bist, werde ich auch langsamer.",
        "- "Oft tippen wir parallel.",
        "- "Wir reagieren gleichzeitig.",
        "- "Unsere Antworten kommen im selben Takt.",
        "Adaptierte oder bewusst gleichzeitige Antwortzeiten, Rhythmus-Anpassung, auffallende Parallelität in der Chat-Interaktion.",
        "beschreibung: >",
        "RESPONSE_TIMING_SEM:",
        "- "Wir experimentieren gemeinsam mit neuen Emojis.",
        "- "Unsere Stimmung zeigt sich in gleichen Symbolen.",
        "- "Beide benutzen ❤️ und 😁 zur selben Zeit.",
        "- "Unsere Emoji-Reihenfolge ist auffällig synchron.",
        "- "Wir schicken uns die gleichen Emojis.",
        "Spiegelung und Angleichung im Emoji-Verhalten; identische oder aufeinander folgende Emoji-Nutzung als Zeichen emotionaler Verbundenheit.",
        "beschreibung: >",
        "EMOJI_ALIGNMENT_SEM:",
        "- "Selbst unsere Emojis sind identisch platziert.",
        "- "Wir nutzen jetzt dieselben Abkürzungen.",
        "- "Sogar die Satzlänge passt sich an.",
        "- "Unsere Sätze spiegeln sich gegenseitig.",
        "- "Ich erkenne kaum noch, ob du oder ich das geschrieben habe.",
        "- "Unsere Wortwahl wird immer ähnlicher.",
        "- "Wir schreiben mittlerweile fast gleich.",
        "Synchroner oder adaptierter Schreibstil im Dialog; auffallend ähnliche Wortwahl, gleiche Satzstruktur, Wiederholung typischer Formulierungen.",
        "beschreibung: >",
        "STYLE_SYNC_SEM:",
        "output_path.name",
        "yaml.dump(data, f, allow_unicode=True)",
        "with open(output_path, "w", encoding="utf-8") as f:",
        "output_path = Path("/mnt/data/semantic_grabber_library_FINAL_FULL.yaml")",
        "# Neue Datei speichern",
        "data.append(guardian_marker)",
        "# Marker hinzufügen",
        "- Pattern Interrupt (Ericksonian Technique): disrupting habitual negative loops to enable change",
        "- Psychological Safety (Amy Edmondson): protecting openness and inclusion\n",
        "- Process Facilitation: guiding a group through healthy communication patterns\n",
        "- Meta-Position (Virginia Satir): observing the system instead of reacting from within it\n",
        "It draws on concepts like:\n",
        "This marker reflects advanced meta-communication skills, system awareness, and the ability to interrupt group dysfunctions.",
        "psychological_context": (",
        "rule_5: Detect playful or visual interruptions (e.g. 🛡️, ⚖️, 'Foulspiel!') as system awareness signals.",
        "rule_4: Identify principle or value references during team conflict or pressure.",",
        "rule_3: Recognize reflective process-oriented language (e.g. 'Sind wir noch im Lösungsmodus?').",",
        "rule_2: Find interruption cues followed by systemic reference (e.g. 'Stopp... unser Prinzip...')",",
        "rule_1: Detect meta-phrases like 'Ich nehme hier mal die Guardian-Rolle ein', 'Kurze Meta-Frage', 'Ich möchte auf die Metaebene wechseln'.",",
        "patterns": [",
        "⚖️",
        "Zeit für den Schiedsrichter. pfeift Foulspiel!",",
        "Sind wir noch im Lösungsmodus oder im Rechtfertigungsmodus?",",
        "Unser gemeinsames Betriebssystem hat gerade einen Bug.",",
        "Als Scrum Master muss ich hier einschreiten: ...",",
        "Wir vermeiden gerade ein wichtiges Thema.",",
        "Wir machen Witze auf Kosten von jemand anderem.",",
        "Wir haben Toms Idee dreimal besprochen, aber Miri und Jan ignoriert.",",
        "Ich glaube, wir ziehen uns gerade gegenseitig runter.",",
        "Können wir bitte aufhören, über Lisa zu reden, wenn sie nicht da ist?",",
        "Der Ton wird gerade schärfer. Lass uns aufpassen. ❤️",",
        "Mir ist aufgefallen, dass wir Entscheidungen oft ohne Emotionen treffen.",",
        "Ich glaube, wir brauchen eine Regel für solche Gespräche.",",
        "Ich möchte sicherstellen, dass wir beide gleich viel Redezeit haben.",",
        "Fällt dir auf, dass wir beide gerade versuchen, den anderen zu 'gewinnen'?",",
        "Ich möchte kurz auf die Metaebene wechseln: Geht es wirklich um Geld oder um Angst?",",
        "Ich glaube, wir texten gerade aneinander vorbei.",",
        "Wir treffen eine Entscheidung für die Kinder über deren Köpfe hinweg.",",
        "Ich merke gerade, ich rede nur noch über meine Probleme. Das ist unfair.",",
        "Warte mal kurz. Stopp. Ich glaube, wir spielen gerade unser altes Spiel.",",
        "Prozess-Check?",",
        "Ich mache mir Sorgen, dass wir mit dem Verhalten psychologische Sicherheit untergraben.",",
        "Wir haben noch 10 Minuten und sind erst bei Punkt 2. Wie wollen wir damit umgehen?",",
        "Check-in: Lasst uns Entscheidungen wieder transparent dokumentieren.",",
        "Ich habe den Eindruck, wir ignorieren gerade das Design-Team.",",
        "Ich nehme hier mal die Guardian-Rolle ein: ...",",
        "Moment mal. Bevor wir weitermachen, möchte ich sicherstellen, dass wir hier gerade nicht in ein Groupthink-Muster verfallen.",",
        "Ich spreche mal als Hüter unseres Prozesses: ...",",
        "Kurze Meta-Frage: Entscheiden wir das hier gerade wirklich im Chat?",",
        "Stopp, ich glaube, wir verlieren gerade den Fokus.",",
        "examples": [",
        "pattern-interrupt",
        "principle-reminder",",
        "system-check",",
        "meta-position",",
        "guardian-role",",
        "semantic_tags": [",
        "semantic_grabber_id": "LIFE_ROLE_GUARDIAN_SEM",",
        "category": "Meta Communication",",
        "),",
        "This includes interrupting dysfunctional loops, referencing shared values or norms, and raising awareness about group dynamics.",
        "to protect the integrity, fairness, or psychological safety of a team process, decision, or communication pattern.",
        "Detects statements in which a speaker steps out of content-level discussion and takes a meta-position",
        "description": (",
        "name": "System Guardian",",
        "id": "M2002",",
        "guardian_marker = {",
        "# Neuer Marker "LIFE_ROLE_GUARDIAN_SEM",
        "data = yaml.safe_load(f)",
        "with open(input_path, "r", encoding="utf-8") as f:",
        "input_path = Path("/mnt/data/semantic_grabber_library_FINAL.yaml")",
        "# Datei erneut laden",
        "from pathlib import Path",]
    
    patterns = [
        re.compile(r"(muster.*wird.*ergänzt)", re.IGNORECASE)
    ]
    
    semantic_grabber_id = "AUTO_GENERATED"
    
    def match(self, text):
        """Prüft ob der Text zum Marker passt"""
        for pattern in self.patterns:
            if pattern.search(text):
                return True
        return False
