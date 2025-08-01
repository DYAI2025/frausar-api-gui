#!/usr/bin/env python3
"""
KNOWLEDGE REGISTRY - Semantic Organization and Discovery System
==============================================================

Enhances the Hive quality and organization of the knowledge storage for GPTs.
Makes the system more extensible and understandable for connected agents.

Features:
- Semantic indexing and categorization
- Agent and project metadata management
- Knowledge domain classification
- Discovery and search capabilities
- Relationship mapping between markers
- Auto-generated documentation for agents
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from collections import defaultdict
import re

from marker_v3_1_manager import MarkerV31Manager


class KnowledgeRegistry:
    """
    Central registry for semantic knowledge organization and discovery.
    
    Provides enhanced organization, semantic relationships, and discovery
    capabilities for the Lean-Deep v3.1 marker system.
    """
    
    def __init__(self, marker_directory: str = "./markers", registry_file: str = "./knowledge_registry.json"):
        """
        Initialize the Knowledge Registry.
        
        Args:
            marker_directory: Directory containing marker files
            registry_file: File to store the registry index
        """
        self.marker_dir = Path(marker_directory)
        self.registry_file = Path(registry_file)
        self.v31_manager = MarkerV31Manager()
        
        # Registry data structure
        self.registry = {
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_markers": 0
            },
            "agents": {},           # Agent profiles and capabilities
            "projects": {},         # Project contexts and scopes
            "knowledge_domains": {}, # Domain classifications
            "semantic_network": {},  # Relationships between markers
            "discovery_index": {},   # Search and discovery index
            "markers": {}           # Marker metadata and references
        }
        
        # Knowledge domains for better organization
        self.default_domains = {
            "emotional_analysis": "Emotional and psychological patterns",
            "behavior_patterns": "Behavioral analysis and detection",
            "time_management": "Time-related expressions and patterns",
            "communication": "Communication and interaction patterns",
            "task_management": "Task organization and workflow",
            "decision_making": "Decision processes and logic",
            "learning_patterns": "Learning and knowledge acquisition",
            "system_meta": "System and framework metadata"
        }
        
        # Agent types for capability organization
        self.agent_types = {
            "analyzer": "Pattern analysis and detection agents",
            "generator": "Content and response generation agents", 
            "classifier": "Classification and categorization agents",
            "coordinator": "Workflow and task coordination agents",
            "specialist": "Domain-specific expert agents",
            "meta": "System management and meta-analysis agents"
        }
        
        self.load_registry()
    
    def load_registry(self) -> None:
        """Load existing registry or create new one."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    loaded_registry = json.load(f)
                    # Merge with default structure to handle version updates
                    self._merge_registry_structure(loaded_registry)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load registry ({e}), creating new one")
                self._initialize_default_registry()
        else:
            self._initialize_default_registry()
    
    def save_registry(self) -> None:
        """Save registry to file."""
        self.registry["metadata"]["last_updated"] = datetime.now().isoformat()
        
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def rebuild_index(self) -> Dict[str, Any]:
        """
        Rebuild the complete knowledge index from marker files.
        
        Returns:
            Statistics about the rebuild process
        """
        stats = {
            "processed": 0,
            "indexed": 0,
            "errors": 0,
            "domains_found": set(),
            "projects_found": set(),
            "agents_found": set()
        }
        
        # Reset registry data
        self.registry["markers"] = {}
        self.registry["semantic_network"] = {}
        self.registry["discovery_index"] = defaultdict(list)
        
        # Process all marker files
        for marker_file in self.marker_dir.glob("*.yaml"):
            stats["processed"] += 1
            
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                if marker_data:
                    self._index_marker(marker_data, marker_file.stem)
                    stats["indexed"] += 1
                    
                    # Collect statistics
                    if "knowledge_domain" in marker_data:
                        stats["domains_found"].add(marker_data["knowledge_domain"])
                    if "project_context" in marker_data and marker_data["project_context"].get("project_id"):
                        stats["projects_found"].add(marker_data["project_context"]["project_id"])
                    if "agent_metadata" in marker_data and marker_data["agent_metadata"].get("agent_type"):
                        stats["agents_found"].add(marker_data["agent_metadata"]["agent_type"])
                        
            except Exception as e:
                stats["errors"] += 1
                print(f"Error processing {marker_file}: {e}")
        
        # Update registry metadata
        self.registry["metadata"]["total_markers"] = stats["indexed"]
        
        # Auto-populate knowledge domains
        self._update_knowledge_domains(stats["domains_found"])
        
        self.save_registry()
        
        # Convert sets to lists for JSON serialization
        stats["domains_found"] = list(stats["domains_found"])
        stats["projects_found"] = list(stats["projects_found"])
        stats["agents_found"] = list(stats["agents_found"])
        
        return stats
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str], 
                      description: str = "", access_level: str = "standard") -> None:
        """
        Register an agent in the knowledge system.
        
        Args:
            agent_id: Unique agent identifier
            agent_type: Type of agent (analyzer, generator, etc.)
            capabilities: List of agent capabilities
            description: Agent description
            access_level: Access level (standard, elevated, admin)
        """
        self.registry["agents"][agent_id] = {
            "agent_type": agent_type,
            "capabilities": capabilities,
            "description": description,
            "access_level": access_level,
            "registered_at": datetime.now().isoformat(),
            "associated_markers": []
        }
        self.save_registry()
    
    def register_project(self, project_id: str, domain: str, scope: str, 
                        description: str = "", markers: List[str] = None) -> None:
        """
        Register a project context in the knowledge system.
        
        Args:
            project_id: Unique project identifier
            domain: Project domain
            scope: Project scope description
            description: Project description
            markers: Associated marker IDs
        """
        self.registry["projects"][project_id] = {
            "domain": domain,
            "scope": scope,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "markers": markers or []
        }
        self.save_registry()
    
    def find_markers_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Find all markers in a specific knowledge domain."""
        results = []
        for marker_id, marker_info in self.registry["markers"].items():
            if marker_info.get("knowledge_domain") == domain:
                results.append({
                    "id": marker_id,
                    "name": marker_info.get("name", ""),
                    "description": marker_info.get("description", ""),
                    "level": marker_info.get("level", 0),
                    "file_path": marker_info.get("file_path", "")
                })
        return results
    
    def find_markers_by_agent_type(self, agent_type: str) -> List[Dict[str, Any]]:
        """Find all markers suitable for a specific agent type."""
        results = []
        for marker_id, marker_info in self.registry["markers"].items():
            marker_agent_type = marker_info.get("agent_metadata", {}).get("agent_type", "")
            if marker_agent_type == agent_type or not marker_agent_type:  # Include generic markers
                results.append({
                    "id": marker_id,
                    "name": marker_info.get("name", ""),
                    "description": marker_info.get("description", ""),
                    "level": marker_info.get("level", 0),
                    "file_path": marker_info.get("file_path", "")
                })
        return results
    
    def find_related_markers(self, marker_id: str) -> List[Dict[str, Any]]:
        """Find markers related to the given marker."""
        relationships = self.registry["semantic_network"].get(marker_id, {})
        related = []
        
        for rel_type, marker_list in relationships.items():
            for related_id in marker_list:
                if related_id in self.registry["markers"]:
                    marker_info = self.registry["markers"][related_id]
                    related.append({
                        "id": related_id,
                        "name": marker_info.get("name", ""),
                        "description": marker_info.get("description", ""),
                        "relationship_type": rel_type,
                        "level": marker_info.get("level", 0)
                    })
        
        return related
    
    def generate_agent_documentation(self, agent_id: str = None) -> str:
        """
        Generate documentation for agents about available knowledge.
        
        Args:
            agent_id: Specific agent ID, or None for general documentation
            
        Returns:
            Formatted documentation string
        """
        doc = ["# Knowledge Registry Documentation", ""]
        
        if agent_id and agent_id in self.registry["agents"]:
            agent_info = self.registry["agents"][agent_id]
            doc.extend([
                f"## Agent: {agent_id}",
                f"Type: {agent_info['agent_type']}",
                f"Capabilities: {', '.join(agent_info['capabilities'])}",
                f"Access Level: {agent_info['access_level']}",
                ""
            ])
            
            # Find relevant markers for this agent
            relevant_markers = self.find_markers_by_agent_type(agent_info['agent_type'])
            if relevant_markers:
                doc.append("### Relevant Markers:")
                for marker in relevant_markers[:10]:  # Limit to top 10
                    doc.append(f"- **{marker['id']}** (Level {marker['level']}): {marker['description']}")
                doc.append("")
        
        # Knowledge domains overview
        doc.extend([
            "## Knowledge Domains",
            ""
        ])
        
        for domain_id, domain_info in self.registry["knowledge_domains"].items():
            markers_in_domain = len(self.find_markers_by_domain(domain_id))
            doc.append(f"### {domain_id.replace('_', ' ').title()}")
            doc.append(f"Description: {domain_info.get('description', 'No description')}")
            doc.append(f"Markers: {markers_in_domain}")
            doc.append("")
        
        # Projects overview
        if self.registry["projects"]:
            doc.extend([
                "## Projects",
                ""
            ])
            
            for project_id, project_info in self.registry["projects"].items():
                doc.append(f"### {project_id}")
                doc.append(f"Domain: {project_info['domain']}")
                doc.append(f"Scope: {project_info['scope']}")
                doc.append(f"Markers: {len(project_info.get('markers', []))}")
                doc.append("")
        
        # Statistics
        doc.extend([
            "## Registry Statistics",
            f"- Total Markers: {self.registry['metadata']['total_markers']}",
            f"- Knowledge Domains: {len(self.registry['knowledge_domains'])}",
            f"- Registered Agents: {len(self.registry['agents'])}",
            f"- Projects: {len(self.registry['projects'])}",
            f"- Last Updated: {self.registry['metadata']['last_updated']}",
            ""
        ])
        
        return "\n".join(doc)
    
    def search_markers(self, query: str, domains: List[str] = None, 
                      agent_types: List[str] = None, levels: List[int] = None) -> List[Dict[str, Any]]:
        """
        Search markers with semantic and contextual filtering.
        
        Args:
            query: Search query string
            domains: Filter by knowledge domains
            agent_types: Filter by agent types
            levels: Filter by marker levels
            
        Returns:
            List of matching markers with relevance scoring
        """
        results = []
        query_lower = query.lower()
        
        for marker_id, marker_info in self.registry["markers"].items():
            score = 0
            match_reasons = []
            
            # Text matching
            if query_lower in marker_info.get("name", "").lower():
                score += 3
                match_reasons.append("name")
            if query_lower in marker_info.get("description", "").lower():
                score += 2
                match_reasons.append("description")
            if any(query_lower in tag.lower() for tag in marker_info.get("tags", [])):
                score += 2
                match_reasons.append("tags")
            if any(query_lower in tag.lower() for tag in marker_info.get("discovery_tags", [])):
                score += 1
                match_reasons.append("discovery_tags")
            
            # Apply filters
            if domains and marker_info.get("knowledge_domain") not in domains:
                continue
            if agent_types and marker_info.get("agent_metadata", {}).get("agent_type") not in agent_types:
                continue
            if levels and marker_info.get("level") not in levels:
                continue
            
            if score > 0:
                results.append({
                    "id": marker_id,
                    "name": marker_info.get("name", ""),
                    "description": marker_info.get("description", ""),
                    "level": marker_info.get("level", 0),
                    "knowledge_domain": marker_info.get("knowledge_domain", ""),
                    "score": score,
                    "match_reasons": match_reasons,
                    "file_path": marker_info.get("file_path", "")
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    
    def _index_marker(self, marker_data: Dict[str, Any], marker_id: str) -> None:
        """Index a single marker in the registry."""
        # Extract key information
        marker_info = {
            "id": marker_data.get("id", marker_id),
            "name": marker_data.get("name", ""),
            "description": marker_data.get("description", ""),
            "level": marker_data.get("level", 0),
            "category": marker_data.get("category", ""),
            "tags": marker_data.get("tags", []),
            "knowledge_domain": marker_data.get("knowledge_domain", ""),
            "semantic_weight": marker_data.get("semantic_weight", 1.0),
            "discovery_tags": marker_data.get("discovery_tags", []),
            "agent_metadata": marker_data.get("agent_metadata", {}),
            "project_context": marker_data.get("project_context", {}),
            "file_path": f"{marker_id}.yaml",
            "indexed_at": datetime.now().isoformat()
        }
        
        self.registry["markers"][marker_id] = marker_info
        
        # Index semantic relationships
        relationships = marker_data.get("semantic_relationships", [])
        if relationships:
            self.registry["semantic_network"][marker_id] = {
                "related_to": relationships,
                "composed_of": marker_data.get("composed_of", []),
                "used_by": []  # Will be populated by reverse references
            }
        
        # Update discovery index
        self._update_discovery_index(marker_id, marker_info)
    
    def _update_discovery_index(self, marker_id: str, marker_info: Dict[str, Any]) -> None:
        """Update the discovery index with marker information."""
        # Index by level
        self.registry["discovery_index"][f"level_{marker_info['level']}"].append(marker_id)
        
        # Index by category
        if marker_info["category"]:
            self.registry["discovery_index"][f"category_{marker_info['category'].lower()}"].append(marker_id)
        
        # Index by domain
        if marker_info["knowledge_domain"]:
            self.registry["discovery_index"][f"domain_{marker_info['knowledge_domain']}"].append(marker_id)
        
        # Index by agent type
        agent_type = marker_info.get("agent_metadata", {}).get("agent_type", "")
        if agent_type:
            self.registry["discovery_index"][f"agent_{agent_type}"].append(marker_id)
        
        # Index by tags
        for tag in marker_info.get("tags", []) + marker_info.get("discovery_tags", []):
            if tag:
                self.registry["discovery_index"][f"tag_{tag.lower()}"].append(marker_id)
    
    def _update_knowledge_domains(self, found_domains: Set[str]) -> None:
        """Update knowledge domains with discovered domains."""
        # Add default domains
        for domain_id, description in self.default_domains.items():
            if domain_id not in self.registry["knowledge_domains"]:
                self.registry["knowledge_domains"][domain_id] = {
                    "description": description,
                    "auto_created": True
                }
        
        # Add discovered domains
        for domain in found_domains:
            if domain and domain not in self.registry["knowledge_domains"]:
                self.registry["knowledge_domains"][domain] = {
                    "description": f"Auto-discovered domain: {domain}",
                    "auto_created": True
                }
    
    def _merge_registry_structure(self, loaded_registry: Dict[str, Any]) -> None:
        """Merge loaded registry with current structure, preserving data."""
        # Update metadata
        if "metadata" in loaded_registry:
            self.registry["metadata"].update(loaded_registry["metadata"])
        
        # Preserve existing sections
        for section in ["agents", "projects", "knowledge_domains", "semantic_network", "discovery_index", "markers"]:
            if section in loaded_registry:
                self.registry[section] = loaded_registry[section]
    
    def _initialize_default_registry(self) -> None:
        """Initialize registry with default knowledge domains and structure."""
        self._update_knowledge_domains(set())
        self.save_registry()


# CLI functionality for testing
def test_knowledge_registry():
    """Test the knowledge registry functionality."""
    print("🧠 Testing Knowledge Registry...")
    
    registry = KnowledgeRegistry()
    
    # Test rebuilding index
    print("\n1. Rebuilding index...")
    stats = registry.rebuild_index()
    print(f"   Processed: {stats['processed']} files")
    print(f"   Indexed: {stats['indexed']} markers")
    print(f"   Domains found: {stats['domains_found']}")
    print(f"   Projects found: {stats['projects_found']}")
    
    # Test agent registration
    print("\n2. Registering test agent...")
    registry.register_agent(
        "test_analyzer", 
        "analyzer", 
        ["pattern_detection", "emotional_analysis"],
        "Test analyzer agent for emotional patterns"
    )
    
    # Test project registration
    print("\n3. Registering test project...")
    registry.register_project(
        "emotional_intelligence",
        "emotional_analysis",
        "Comprehensive emotional pattern detection and analysis"
    )
    
    # Test search
    print("\n4. Testing search...")
    results = registry.search_markers("emotional", domains=["emotional_analysis"])
    print(f"   Found {len(results)} markers for 'emotional'")
    for result in results[:3]:
        print(f"   - {result['id']}: {result['description']} (score: {result['score']})")
    
    # Test documentation generation
    print("\n5. Generating documentation...")
    doc = registry.generate_agent_documentation("test_analyzer")
    print(f"   Generated {len(doc.split('\n'))} lines of documentation")
    
    print("\n✅ Knowledge Registry test completed!")


if __name__ == "__main__":
    test_knowledge_registry()