#!/usr/bin/env python3
"""
KNOWLEDGE CLI - Command Line Interface for Knowledge Registry
============================================================

Provides command-line access to the enhanced knowledge registry system
for agents and users to discover, search, and interact with markers.

Usage:
    python knowledge_cli.py search "emotional analysis"
    python knowledge_cli.py domain emotional_analysis
    python knowledge_cli.py agent analyzer
    python knowledge_cli.py docs agent_emotional_analyzer
    python knowledge_cli.py rebuild
"""

import argparse
import sys
from pathlib import Path
from knowledge_registry import KnowledgeRegistry
from marker_v3_1_manager import MarkerV31Manager


def search_command(registry: KnowledgeRegistry, args):
    """Handle search command."""
    results = registry.search_markers(
        args.query,
        domains=args.domains.split(',') if args.domains else None,
        agent_types=args.agent_types.split(',') if args.agent_types else None,
        levels=[int(l) for l in args.levels.split(',')] if args.levels else None
    )
    
    print(f"🔍 Search results for '{args.query}':")
    print(f"Found {len(results)} markers\n")
    
    for i, result in enumerate(results[:args.limit], 1):
        print(f"{i}. **{result['id']}** (Level {result['level']}, Score: {result['score']})")
        print(f"   Domain: {result['knowledge_domain'] or 'Not specified'}")
        print(f"   Description: {result['description']}")
        print(f"   Match reasons: {', '.join(result['match_reasons'])}")
        print(f"   File: {result['file_path']}")
        print()


def domain_command(registry: KnowledgeRegistry, args):
    """Handle domain command."""
    markers = registry.find_markers_by_domain(args.domain)
    
    print(f"📂 Markers in domain '{args.domain}':")
    print(f"Found {len(markers)} markers\n")
    
    for marker in markers:
        print(f"- **{marker['id']}** (Level {marker['level']})")
        print(f"  {marker['description']}")
        print()


def agent_command(registry: KnowledgeRegistry, args):
    """Handle agent command."""
    markers = registry.find_markers_by_agent_type(args.agent_type)
    
    print(f"🤖 Markers for agent type '{args.agent_type}':")
    print(f"Found {len(markers)} markers\n")
    
    for marker in markers:
        print(f"- **{marker['id']}** (Level {marker['level']})")
        print(f"  {marker['description']}")
        print()


def related_command(registry: KnowledgeRegistry, args):
    """Handle related markers command."""
    related = registry.find_related_markers(args.marker_id)
    
    print(f"🔗 Related markers for '{args.marker_id}':")
    print(f"Found {len(related)} related markers\n")
    
    for marker in related:
        print(f"- **{marker['id']}** (Level {marker['level']})")
        print(f"  Relationship: {marker['relationship_type']}")
        print(f"  Description: {marker['description']}")
        print()


def docs_command(registry: KnowledgeRegistry, args):
    """Handle documentation command."""
    doc = registry.generate_agent_documentation(args.agent_id)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(doc)
        print(f"📄 Documentation written to {args.output}")
    else:
        print(doc)


def rebuild_command(registry: KnowledgeRegistry, args):
    """Handle rebuild command."""
    print("🔄 Rebuilding knowledge registry...")
    stats = registry.rebuild_index()
    
    print(f"✅ Rebuild completed:")
    print(f"   Processed: {stats['processed']} files")
    print(f"   Indexed: {stats['indexed']} markers")
    print(f"   Errors: {stats['errors']}")
    print(f"   Domains found: {len(stats['domains_found'])}")
    print(f"   Projects found: {len(stats['projects_found'])}")
    print(f"   Agent types found: {len(stats['agents_found'])}")


def list_command(registry: KnowledgeRegistry, args):
    """Handle list command."""
    if args.type == 'domains':
        print("📂 Available knowledge domains:")
        for domain_id, domain_info in registry.registry["knowledge_domains"].items():
            marker_count = len(registry.find_markers_by_domain(domain_id))
            print(f"- **{domain_id}**: {domain_info['description']} ({marker_count} markers)")
    
    elif args.type == 'agents':
        print("🤖 Registered agents:")
        for agent_id, agent_info in registry.registry["agents"].items():
            print(f"- **{agent_id}** ({agent_info['agent_type']})")
            print(f"  Capabilities: {', '.join(agent_info['capabilities'])}")
            print(f"  Access level: {agent_info['access_level']}")
    
    elif args.type == 'projects':
        print("📋 Registered projects:")
        for project_id, project_info in registry.registry["projects"].items():
            print(f"- **{project_id}** ({project_info['domain']})")
            print(f"  Scope: {project_info['scope']}")
            print(f"  Markers: {len(project_info.get('markers', []))}")
    
    elif args.type == 'stats':
        metadata = registry.registry["metadata"]
        print("📊 Registry statistics:")
        print(f"- Total markers: {metadata['total_markers']}")
        print(f"- Knowledge domains: {len(registry.registry['knowledge_domains'])}")
        print(f"- Registered agents: {len(registry.registry['agents'])}")
        print(f"- Projects: {len(registry.registry['projects'])}")
        print(f"- Last updated: {metadata['last_updated']}")


def register_agent_command(registry: KnowledgeRegistry, args):
    """Handle agent registration command."""
    capabilities = args.capabilities.split(',') if args.capabilities else []
    
    registry.register_agent(
        args.agent_id,
        args.agent_type,
        capabilities,
        args.description or "",
        args.access_level or "standard"
    )
    
    print(f"✅ Agent '{args.agent_id}' registered successfully")


def register_project_command(registry: KnowledgeRegistry, args):
    """Handle project registration command."""
    markers = args.markers.split(',') if args.markers else None
    
    registry.register_project(
        args.project_id,
        args.domain,
        args.scope,
        args.description or "",
        markers
    )
    
    print(f"✅ Project '{args.project_id}' registered successfully")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Knowledge Registry CLI - Semantic marker discovery and management",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--marker-dir', default='./markers',
                       help='Directory containing marker files')
    parser.add_argument('--registry-file', default='./knowledge_registry.json',
                       help='Registry file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search markers')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--domains', help='Filter by domains (comma-separated)')
    search_parser.add_argument('--agent-types', help='Filter by agent types (comma-separated)')
    search_parser.add_argument('--levels', help='Filter by levels (comma-separated)')
    search_parser.add_argument('--limit', type=int, default=10, help='Limit results')
    
    # Domain command
    domain_parser = subparsers.add_parser('domain', help='List markers in domain')
    domain_parser.add_argument('domain', help='Domain name')
    
    # Agent command
    agent_parser = subparsers.add_parser('agent', help='List markers for agent type')
    agent_parser.add_argument('agent_type', help='Agent type')
    
    # Related command
    related_parser = subparsers.add_parser('related', help='Find related markers')
    related_parser.add_argument('marker_id', help='Marker ID')
    
    # Documentation command
    docs_parser = subparsers.add_parser('docs', help='Generate documentation')
    docs_parser.add_argument('agent_id', nargs='?', help='Agent ID (optional)')
    docs_parser.add_argument('--output', help='Output file path')
    
    # Rebuild command
    subparsers.add_parser('rebuild', help='Rebuild registry index')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List registry contents')
    list_parser.add_argument('type', choices=['domains', 'agents', 'projects', 'stats'],
                           help='What to list')
    
    # Register agent command
    reg_agent_parser = subparsers.add_parser('register-agent', help='Register new agent')
    reg_agent_parser.add_argument('agent_id', help='Agent ID')
    reg_agent_parser.add_argument('agent_type', help='Agent type')
    reg_agent_parser.add_argument('--capabilities', help='Capabilities (comma-separated)')
    reg_agent_parser.add_argument('--description', help='Agent description')
    reg_agent_parser.add_argument('--access-level', help='Access level')
    
    # Register project command
    reg_project_parser = subparsers.add_parser('register-project', help='Register new project')
    reg_project_parser.add_argument('project_id', help='Project ID')
    reg_project_parser.add_argument('domain', help='Project domain')
    reg_project_parser.add_argument('scope', help='Project scope')
    reg_project_parser.add_argument('--description', help='Project description')
    reg_project_parser.add_argument('--markers', help='Associated markers (comma-separated)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize registry
    registry = KnowledgeRegistry(args.marker_dir, args.registry_file)
    
    # Execute command
    try:
        if args.command == 'search':
            search_command(registry, args)
        elif args.command == 'domain':
            domain_command(registry, args)
        elif args.command == 'agent':
            agent_command(registry, args)
        elif args.command == 'related':
            related_command(registry, args)
        elif args.command == 'docs':
            docs_command(registry, args)
        elif args.command == 'rebuild':
            rebuild_command(registry, args)
        elif args.command == 'list':
            list_command(registry, args)
        elif args.command == 'register-agent':
            register_agent_command(registry, args)
        elif args.command == 'register-project':
            register_project_command(registry, args)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()