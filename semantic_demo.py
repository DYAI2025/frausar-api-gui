#!/usr/bin/env python3
"""
Semantic Enhancement Demo
========================

Demonstrates the enhanced semantic capabilities of the Frausar Marker system.
"""

from marker_tool import MarkerTool
from knowledge_registry import KnowledgeRegistry

def main():
    print("🧠 Frausar Semantic Enhancement Demo")
    print("=" * 50)
    
    # Initialize tools
    tool = MarkerTool()
    registry = KnowledgeRegistry()
    
    # 1. Rebuild knowledge index
    print("\n1. 🔄 Rebuilding knowledge index...")
    stats = tool.rebuild_knowledge_index()
    print(f"   Indexed: {stats['indexed']} markers")
    print(f"   Domains: {len(stats['domains_found'])}")
    print(f"   Projects: {len(stats['projects_found'])}")
    
    # 2. Semantic search demo
    print("\n2. 🔍 Semantic search demo...")
    results = tool.search_markers_semantically("emotional", 
                                               knowledge_domain="emotional_analysis")
    print(f"   Found {len(results)} emotional analysis markers:")
    for result in results[:3]:
        print(f"   - {result['id']}: {result['description'][:50]}...")
    
    # 3. Agent relationships demo
    print("\n3. 🔗 Agent relationships demo...")
    relationships = tool.get_marker_relationships("MM_AGENT_EMOTIONAL_ANALYZER")
    print(f"   Found {len(relationships)} relationship types:")
    for rel_type, markers in relationships.items():
        print(f"   - {rel_type}: {len(markers)} markers")
    
    # 4. Knowledge documentation demo
    print("\n4. 📚 Knowledge documentation demo...")
    docs = tool.generate_knowledge_documentation()
    lines = docs.split('\n')
    print(f"   Generated {len(lines)} lines of documentation")
    print(f"   Sample: {lines[0]}")
    
    # 5. Domain organization demo
    print("\n5. 📂 Domain organization demo...")
    domains = registry.registry["knowledge_domains"]
    print(f"   Available domains: {len(domains)}")
    for domain_id in list(domains.keys())[:5]:
        marker_count = len(registry.find_markers_by_domain(domain_id))
        print(f"   - {domain_id}: {marker_count} markers")
    
    # 6. Agent capabilities demo
    print("\n6. 🤖 Agent capabilities demo...")
    agents = registry.registry["agents"]
    print(f"   Registered agents: {len(agents)}")
    for agent_id, agent_info in list(agents.items())[:3]:
        capabilities = agent_info.get('capabilities', [])
        print(f"   - {agent_id}: {len(capabilities)} capabilities")
    
    print("\n✅ Semantic Enhancement Demo completed!")
    print("\nThe Frausar Marker system now provides:")
    print("✓ Semantic search and organization")
    print("✓ Agent self-awareness capabilities")
    print("✓ Project context understanding")
    print("✓ Knowledge domain classification")
    print("✓ Automatic documentation generation")
    print("✓ Relationship mapping between markers")

if __name__ == "__main__":
    main()