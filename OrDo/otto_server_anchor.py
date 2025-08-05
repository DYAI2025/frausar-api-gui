#!/usr/bin/env python3
"""
🔗 OTTO SERVER ANCHOR - Kollektives Lernen
============================================================
🎯 Server-Ankerpunkt für Otto's kollektives Lernen
🔗 Verbindung zu anderen Otto-Instanzen
📡 Sparren-Netzwerk für verteiltes Wissen
🌐 REST-API für Otto-Kommunikation
============================================================
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

@dataclass
class LearningEntry:
    """Ein Lerneintrag im kollektiven Netzwerk"""
    type: str
    content: str
    source: str
    timestamp: str
    otto_id: str
    confidence: float = 1.0
    tags: List[str] = None

@dataclass
class SparrenNode:
    """Ein Sparren-Node im verteilten Netzwerk"""
    url: str
    otto_id: str
    last_seen: datetime
    status: str = "active"
    capabilities: List[str] = None

class OttoServerAnchor:
    """Otto's Server-Ankerpunkt für kollektives Lernen"""
    
    def __init__(self, port: int = 8000):
        print("🔗 Initialisiere Otto Server Anchor...")
        
        # Flask App für REST-API
        self.app = Flask(__name__)
        CORS(self.app)  # Erlaube Cross-Origin Requests
        
        # Server-Konfiguration
        self.port = port
        self.host = "0.0.0.0"
        
        # Kollektives Lernen
        self.learning_database = {}
        self.sparren_nodes = {}
        self.otto_instances = {}
        
        # API-Routen registrieren
        self._register_routes()
        
        print(f"✅ Otto Server Anchor bereit auf Port {port}")
    
    def _register_routes(self):
        """Registriere API-Routen"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health Check Endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "otto_instances": len(self.otto_instances),
                "sparren_nodes": len(self.sparren_nodes),
                "learning_entries": len(self.learning_database)
            })
        
        @self.app.route('/register', methods=['POST'])
        def register_otto():
            """Registriere eine neue Otto-Instanz"""
            data = request.get_json()
            otto_id = data.get('otto_id')
            capabilities = data.get('capabilities', [])
            endpoint = data.get('endpoint')
            
            if not otto_id:
                return jsonify({"error": "otto_id required"}), 400
            
            self.otto_instances[otto_id] = {
                "capabilities": capabilities,
                "endpoint": endpoint,
                "registered_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat()
            }
            
            print(f"✅ Otto-Instanz registriert: {otto_id}")
            return jsonify({"status": "registered", "otto_id": otto_id})
        
        @self.app.route('/learn', methods=['POST'])
        def receive_learning():
            """Empfange Lernen von einer Otto-Instanz"""
            data = request.get_json()
            
            learning_entry = LearningEntry(
                type=data.get('type'),
                content=data.get('content'),
                source=data.get('source'),
                timestamp=data.get('timestamp'),
                otto_id=data.get('otto_id'),
                confidence=data.get('confidence', 1.0),
                tags=data.get('tags', [])
            )
            
            # Speichere Lernen
            entry_id = f"{learning_entry.type}_{learning_entry.timestamp}_{learning_entry.otto_id}"
            self.learning_database[entry_id] = learning_entry
            
            # Verteile an andere Otto-Instanzen
            asyncio.create_task(self._distribute_learning(learning_entry))
            
            print(f"🧠 Lernen empfangen von {learning_entry.otto_id}: {learning_entry.type}")
            return jsonify({"status": "received", "entry_id": entry_id})
        
        @self.app.route('/learn', methods=['GET'])
        def get_learning():
            """Hole Lernen aus der Datenbank"""
            learning_type = request.args.get('type')
            source = request.args.get('source')
            limit = int(request.args.get('limit', 50))
            
            filtered_entries = []
            for entry_id, entry in self.learning_database.items():
                if learning_type and entry.type != learning_type:
                    continue
                if source and entry.source != source:
                    continue
                filtered_entries.append({
                    "id": entry_id,
                    "type": entry.type,
                    "content": entry.content,
                    "source": entry.source,
                    "timestamp": entry.timestamp,
                    "otto_id": entry.otto_id,
                    "confidence": entry.confidence,
                    "tags": entry.tags
                })
            
            # Sortiere nach Timestamp (neueste zuerst)
            filtered_entries.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return jsonify({
                "entries": filtered_entries[:limit],
                "total": len(filtered_entries),
                "returned": min(len(filtered_entries), limit)
            })
        
        @self.app.route('/sparren/register', methods=['POST'])
        def register_sparren_node():
            """Registriere einen Sparren-Node"""
            data = request.get_json()
            node_url = data.get('url')
            otto_id = data.get('otto_id')
            capabilities = data.get('capabilities', [])
            
            if not node_url or not otto_id:
                return jsonify({"error": "url and otto_id required"}), 400
            
            self.sparren_nodes[node_url] = SparrenNode(
                url=node_url,
                otto_id=otto_id,
                last_seen=datetime.now(),
                capabilities=capabilities
            )
            
            print(f"🔗 Sparren-Node registriert: {node_url} ({otto_id})")
            return jsonify({"status": "registered", "node_url": node_url})
        
        @self.app.route('/sparren/nodes', methods=['GET'])
        def get_sparren_nodes():
            """Hole alle Sparren-Nodes"""
            nodes = []
            for url, node in self.sparren_nodes.items():
                nodes.append({
                    "url": node.url,
                    "otto_id": node.otto_id,
                    "last_seen": node.last_seen.isoformat(),
                    "status": node.status,
                    "capabilities": node.capabilities
                })
            
            return jsonify({"nodes": nodes})
        
        @self.app.route('/stats', methods=['GET'])
        def get_stats():
            """Hole Server-Statistiken"""
            return jsonify({
                "otto_instances": len(self.otto_instances),
                "sparren_nodes": len(self.sparren_nodes),
                "learning_entries": len(self.learning_database),
                "learning_types": list(set(entry.type for entry in self.learning_database.values())),
                "sources": list(set(entry.source for entry in self.learning_database.values())),
                "uptime": time.time()
            })
    
    async def _distribute_learning(self, learning_entry: LearningEntry):
        """Verteile Lernen an andere Otto-Instanzen"""
        for otto_id, instance in self.otto_instances.items():
            if otto_id == learning_entry.otto_id:
                continue  # Nicht an sich selbst senden
            
            endpoint = instance.get('endpoint')
            if not endpoint:
                continue
            
            try:
                import requests
                response = requests.post(
                    f"{endpoint}/learn",
                    json={
                        "type": learning_entry.type,
                        "content": learning_entry.content,
                        "source": learning_entry.source,
                        "timestamp": learning_entry.timestamp,
                        "otto_id": learning_entry.otto_id,
                        "confidence": learning_entry.confidence,
                        "tags": learning_entry.tags
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✅ Lernen an {otto_id} verteilt")
                else:
                    print(f"⚠️ Fehler beim Verteilen an {otto_id}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Verbindungsfehler zu {otto_id}: {e}")
    
    def start_server(self):
        """Starte den Server"""
        print(f"🚀 Starte Otto Server Anchor auf {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
    
    def get_server_info(self) -> Dict[str, Any]:
        """Hole Server-Informationen"""
        return {
            "host": self.host,
            "port": self.port,
            "otto_instances": len(self.otto_instances),
            "sparren_nodes": len(self.sparren_nodes),
            "learning_entries": len(self.learning_database),
            "status": "running"
        }

# Test-Function
def test_server_anchor():
    """Teste den Server Anchor"""
    print("🧪 Teste Otto Server Anchor...")
    
    anchor = OttoServerAnchor(port=8001)  # Anderer Port für Tests
    
    # Starte Server in separatem Thread
    server_thread = threading.Thread(target=anchor.start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Warte kurz, bis Server startet
    time.sleep(2)
    
    # Teste Health Check
    import requests
    try:
        response = requests.get("http://localhost:8001/health")
        print(f"🏥 Health Check: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Fehler: {e}")
    
    print("✅ Server Anchor Test abgeschlossen")

if __name__ == "__main__":
    # Starte den Server
    anchor = OttoServerAnchor()
    anchor.start_server() 