from emotion_engine import EmotionEngine
from file_organizer import FileOrganizer
from ai_assistant import AIAssistant
from tool_system import ToolSystem
from communication_analyzer import CommunicationAnalyzer
from phi_learning_env import send_phi4, load_config
from typing import Dict

class ThorVoiceComplete:
    def __init__(self):
        self.voice_enabled = True
        self.is_speaking = False
        self.is_listening = False
        self.thor_active = False
        self.current_mode = "Bereit"
        
        # Initialisiere Systeme
        self.emotion_engine = EmotionEngine()
        self.file_organizer = FileOrganizer()
        self.ai_assistant = AIAssistant()
        self.tool_system = ToolSystem()
        self.communication_analyzer = CommunicationAnalyzer()
        
        # Phi-4 Learning Engine
        self.phi_config = load_config()
        self.learning_mode = False
        self.conversation_history = []
        
        # TTS Engines
        self.tts_engines = ["elevenlabs", "pyttsx3", "macos_say"]
        
        # Mikrofon-Setup
        self.setup_microphone()
        
        # GUI Setup
        self.setup_gui()

        # Neue Buttons für Learning Mode
        learning_frame = tk.Frame(control_frame)
        learning_frame.pack(pady=5)
        
        self.learning_button = tk.Button(
            learning_frame, 
            text="🧠 Learning Mode", 
            command=self.toggle_learning_mode,
            bg="#FF6B6B", 
            fg="white", 
            font=("Arial", 10, "bold")
        )
        self.learning_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_history_button = tk.Button(
            learning_frame, 
            text="🗑️ Clear History", 
            command=self.clear_conversation_history,
            bg="#4ECDC4", 
            fg="white", 
            font=("Arial", 10, "bold")
        )
        self.clear_history_button.pack(side=tk.LEFT, padx=5)

    def toggle_learning_mode(self):
        """Toggle Learning Mode mit Phi-4"""
        self.learning_mode = not self.learning_mode
        
        if self.learning_mode:
            self.learning_button.config(text="🧠 Learning ON", bg="#FF4444")
            self.emotion_engine.set_emotion("begeistert", 0.9, "learning mode activated")
            self.speak("Learning Mode aktiviert! Ich werde jetzt proaktiv Fragen stellen um dich besser kennenzulernen! 🧠✨")
            self.add_chat_message("🧠 System", "Learning Mode aktiviert - THOR wird proaktiv lernen!")
            
            # Initialisiere Conversation History für Learning
            if not self.conversation_history:
                system_prompt = (
                    "Du bist THOR im Lernmodus. Stelle dem Benutzer proaktiv Fragen, um seine "
                    "Ziele, Vorlieben und Arbeitsweisen kennenzulernen. Halte die Antworten "
                    "kurz und fasse Erkenntnisse zusammen. Sei cool und selbstbewusst!"
                )
                self.conversation_history = [{"role": "system", "content": system_prompt}]
        else:
            self.learning_button.config(text="🧠 Learning Mode", bg="#FF6B6B")
            self.emotion_engine.set_emotion("cool", 0.7, "learning mode deactivated")
            self.speak("Learning Mode deaktiviert! Zurück zum normalen Modus! 😎")
            self.add_chat_message("🧠 System", "Learning Mode deaktiviert")
            
    def clear_conversation_history(self):
        """Lösche Conversation History"""
        self.conversation_history = []
        self.emotion_engine.set_emotion("cool", 0.6, "history cleared")
        self.speak("Conversation History gelöscht! Fresh start, Baby! 🗑️✨")
        self.add_chat_message("🧠 System", "Conversation History gelöscht")

    def handle_complex_task_with_ai_cool(self, command: str):
        """Handle komplexe Aufgaben mit KI-Fallback und cooler Attitude - jetzt mit Phi-4 Learning"""
        
        # Phi-4 soll immer lernen und zuschauen (keine Sprachausgabe)
        if self.learning_mode:
            self.handle_learning_interaction_silent(command)
        
        # Verwende KI-Fallback (nur dieser spricht)
        try:
            ai_response = self.ai_assistant.process_complex_task(command)
            
            if "❌" in ai_response:
                self.emotion_engine.set_emotion("sassy", 0.7, "ai error")
                self.speak(f"Meh, da ist was schief gelaufen: {ai_response} - sorry Honey!")
            else:
                self.emotion_engine.set_emotion("überlegen", 0.9, "ai success")
                # Nur eine Sprachausgabe - die finale Antwort
                self.speak(ai_response)
                
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.8, "ai fallback failed")
            self.speak(f"Ugh, seriously? Da ist was schief gelaufen: {str(e)} - aber hey, nobody's perfect! Versuch's nochmal!")
            
    def handle_learning_interaction(self, user_input: str):
        """Handle Learning Mode Interaktion mit Phi-4 - mit Sprachausgabe"""
        try:
            # Füge User Input zur History hinzu
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Hole Antwort von Phi-4
            response = send_phi4(self.conversation_history, self.phi_config)
            
            # Füge Antwort zur History hinzu
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Setze Learning-Emotion
            self.emotion_engine.set_emotion("begeistert", 0.8, "learning interaction")
            
            # Antworte mit Phi-4 Response
            self.speak(f"🧠 Learning: {response}")
            
            # Generiere Follow-up Frage (30% Chance)
            if random.random() < 0.3:
                self.generate_learning_followup()
                
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.7, "learning error")
            self.speak(f"Oops, da ist was beim Lernen schief gelaufen: {str(e)} - my bad!")
            
    def handle_learning_interaction_silent(self, user_input: str):
        """Handle Learning Mode Interaktion mit Phi-4 - nur lernen, keine Sprachausgabe"""
        try:
            # Füge User Input zur History hinzu
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Hole Antwort von Phi-4 (nur für Learning)
            response = send_phi4(self.conversation_history, self.phi_config)
            
            # Füge Antwort zur History hinzu
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Logge Learning (ohne Sprachausgabe)
            self.add_chat_message("🧠 Silent Learning", f"Phi-4 lernt: {response[:100]}...")
                
        except Exception as e:
            # Stille Fehlerbehandlung
            self.add_chat_message("🧠 Learning Error", f"Phi-4 Learning Fehler: {str(e)}")
            
    def generate_learning_followup(self):
        """Generiere Follow-up Frage für Learning Mode"""
        try:
            follow_prompt = (
                "Formuliere eine kurze, coole Nachfrage um den Benutzer besser zu verstehen. "
                "Stelle nur eine Frage. Sei cool und selbstbewusst wie THOR."
            )
            
            follow_messages = self.conversation_history + [
                {"role": "system", "content": follow_prompt}
            ]
            
            follow_question = send_phi4(follow_messages, self.phi_config)
            
            # Füge Follow-up zur History hinzu
            self.conversation_history.append({"role": "assistant", "content": follow_question})
            
            # Setze neugierige Emotion
            self.emotion_engine.set_emotion("aufgeregt", 0.8, "follow-up question")
            
            # Stelle Follow-up Frage
            self.speak(f"🤔 Follow-up: {follow_question}")
            
        except Exception as e:
            # Stille Fehlerbehandlung für Follow-ups
            pass 