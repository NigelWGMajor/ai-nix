#!/usr/bin/env python3
"""
DORA - Discovery Observation-Relationship Architecture
Phase 1: Core Scaffolding for Query-Driven Discovery

Main skill entry point.
"""

import sys
import json
from typing import Dict, List, Optional, Tuple, Any

# ==============================================================================
# CONSTANTS
# ==============================================================================

# Realms
REALM_UI = "UI"
REALM_CODE = "Code"
REALM_DATA = "Data"
REALM_SECURITY = "Security"
REALM_CONFIG = "Config"
REALM_GLOSSARY = "Glossary"
REALM_INFRA = "Infra"

ALL_REALMS = [REALM_UI, REALM_CODE, REALM_DATA, REALM_SECURITY,
              REALM_CONFIG, REALM_GLOSSARY, REALM_INFRA]

# Layers
LAYER_ABSTRACT = "Abstract"
LAYER_BROWSE = "Browse"
LAYER_CODEPATH = "CodePath"
LAYER_DATAPATH = "DataPath"
LAYER_EFFECTPATH = "EffectPath"
LAYER_FLOW = "Flow"
LAYER_REFERENCE = "Reference"

ALL_LAYERS = [LAYER_ABSTRACT, LAYER_BROWSE, LAYER_CODEPATH,
              LAYER_DATAPATH, LAYER_EFFECTPATH, LAYER_FLOW, LAYER_REFERENCE]

# Default strength
DEFAULT_STRENGTH = 0.5

# Database directory
DORA_DIR = "~/.claude/dora"

# ==============================================================================
# SESSION STATE (in-memory for Phase 1)
# ==============================================================================

_active_database: Optional[str] = None
_mcp_connected: bool = False


# ==============================================================================
# DATABASE MANAGEMENT
# ==============================================================================

def list_databases() -> List[str]:
    """
    List available DORA databases.

    Returns:
        List of database names (without .db extension)
    """
    # TODO: Implement using Bash tool
    # Run: ls ~/.claude/dora/*.db 2>/dev/null || echo ""
    # Parse output, strip .db extensions
    raise NotImplementedError("Task 1.1.1")


def select_database(databases: List[str]) -> str:
    """
    Prompt user to select or create database.

    Args:
        databases: List of available database names

    Returns:
        Selected or new database name
    """
    # TODO: Implement selection UX
    # - If databases exist: present numbered list
    # - Allow user to select by number or enter new name
    # - Validate database name
    raise NotImplementedError("Task 1.1.2")


def connect_database(name: str) -> bool:
    """
    Connect to DORA database via MCP.

    Args:
        name: Database name (without .db extension)

    Returns:
        True if connection successful, False otherwise
    """
    global _active_database, _mcp_connected

    # TODO: Implement MCP connection
    # Call: mcp__dora-mcp__connect(name=name)
    # Handle success/failure
    # Update global state
    raise NotImplementedError("Task 1.1.3")


def get_active_database() -> Optional[str]:
    """Get currently active database name."""
    return _active_database


def set_active_database(name: str):
    """Set active database name."""
    global _active_database
    _active_database = name


# ==============================================================================
# OBSERVATION ID GENERATION
# ==============================================================================

def generate_ui_id(info: Dict[str, Any]) -> str:
    """
    Generate UI realm observation ID.

    Format: ui.{data-dgat} or ui.{route}.{element}

    Args:
        info: UI observation info dict

    Returns:
        Generated ID (e.g., "ui.profile.photo.upload.button")
    """
    # TODO: Implement
    # - Prefer data-dgat attribute if available
    # - Fallback to route + element type
    raise NotImplementedError("Task 1.2.1")


def generate_code_id(info: Dict[str, Any]) -> str:
    """
    Generate Code realm observation ID.

    Format: code.{namespace}.{class}.{member}

    Args:
        info: Code observation info dict (qualifiedName, filePath, etc.)

    Returns:
        Generated ID (e.g., "code.profile.controller.upload.photo")
    """
    # TODO: Implement
    # - Use qualifiedName if available
    # - Handle missing namespace (use file path)
    raise NotImplementedError("Task 1.2.1")


def generate_data_id(info: Dict[str, Any]) -> str:
    """
    Generate Data realm observation ID.

    Format: data.{schema}.{table}.{column} or data.{schema}.{procedure}

    Args:
        info: Data observation info dict

    Returns:
        Generated ID (e.g., "data.dbo.users.profile_photo_url")
    """
    # TODO: Implement
    raise NotImplementedError("Task 1.2.1")


def generate_security_id(info: Dict[str, Any]) -> str:
    """
    Generate Security realm observation ID.

    Format: security.{type}.{name}

    Args:
        info: Security observation info dict (type, name)

    Returns:
        Generated ID (e.g., "security.ld.show_profile_photo")
    """
    # TODO: Implement
    raise NotImplementedError("Task 1.2.1")


def generate_config_id(info: Dict[str, Any]) -> str:
    """
    Generate Config realm observation ID.

    Format: config.{namespace}.{setting}

    Args:
        info: Config observation info dict

    Returns:
        Generated ID (e.g., "config.app.max_photo_size")
    """
    # TODO: Implement
    raise NotImplementedError("Task 1.2.1")


def generate_glossary_id(info: Dict[str, Any]) -> str:
    """
    Generate Glossary realm observation ID.

    Format: glossary.{domain}.{concept}

    Args:
        info: Glossary observation info dict

    Returns:
        Generated ID (e.g., "glossary.profile.photo_management")
    """
    # TODO: Implement
    raise NotImplementedError("Task 1.2.1")


def generate_infra_id(info: Dict[str, Any]) -> str:
    """
    Generate Infra realm observation ID.

    Format: infra.{type}.{name}

    Args:
        info: Infra observation info dict

    Returns:
        Generated ID (e.g., "infra.blob.profile_photos")
    """
    # TODO: Implement
    raise NotImplementedError("Task 1.2.1")


def generate_observation_id(realm: str, info: Dict[str, Any]) -> str:
    """
    Generate observation ID for given realm.

    Args:
        realm: Observation realm
        info: Realm-specific info dict

    Returns:
        Generated ID
    """
    generators = {
        REALM_UI: generate_ui_id,
        REALM_CODE: generate_code_id,
        REALM_DATA: generate_data_id,
        REALM_SECURITY: generate_security_id,
        REALM_CONFIG: generate_config_id,
        REALM_GLOSSARY: generate_glossary_id,
        REALM_INFRA: generate_infra_id,
    }

    if realm not in generators:
        raise ValueError(f"Invalid realm: {realm}. Must be one of {ALL_REALMS}")

    return generators[realm](info)


# ==============================================================================
# INFO FIELD BUILDERS
# ==============================================================================

def build_ui_info(element_type: str, selector: str = None,
                  route: str = None, parent_component: str = None) -> Dict[str, Any]:
    """Build UI observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_code_info(qualified_name: str, file_path: str = None,
                    line_number: int = None, signature: str = None) -> Dict[str, Any]:
    """Build Code observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_data_info(table_name: str = None, field_name: str = None,
                    data_type: str = None, nullable: bool = None) -> Dict[str, Any]:
    """Build Data observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_config_info(key: str, source: str = None, default_value: Any = None,
                      scope: str = None) -> Dict[str, Any]:
    """Build Config observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_security_info(type_: str, name: str, description: str = None,
                        default_value: Any = None, scope: str = None) -> Dict[str, Any]:
    """Build Security observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_glossary_info(domain: str, concept: str, definition: str = None,
                        related_terms: List[str] = None) -> Dict[str, Any]:
    """Build Glossary observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


def build_infra_info(type_: str, name: str, endpoint: str = None,
                     technology: str = None) -> Dict[str, Any]:
    """Build Infra observation info dict."""
    # TODO: Implement
    raise NotImplementedError("Task 1.2.3")


# ==============================================================================
# OBSERVATION CRUD
# ==============================================================================

def create_observation(realm: str, info: Dict[str, Any],
                      strength: float = DEFAULT_STRENGTH) -> str:
    """
    Create observation in graph.

    Args:
        realm: Observation realm
        info: Realm-specific info dict
        strength: Confidence value (0.0-1.0)

    Returns:
        Observation ID
    """
    # TODO: Implement
    # 1. Generate ID
    # 2. Call mcp__dora-mcp__observe(id, realm, strength, info)
    # 3. Handle errors
    # 4. Return ID
    raise NotImplementedError("Task 1.2.2")


# ==============================================================================
# RELATIONSHIP CRUD
# ==============================================================================

def create_link(source_id: str, target_id: str, layer: str,
                strength: float = DEFAULT_STRENGTH) -> bool:
    """
    Create link between observations.

    Args:
        source_id: Source observation ID
        target_id: Target observation ID
        layer: Relationship layer
        strength: Confidence value (0.0-1.0)

    Returns:
        True if successful
    """
    # TODO: Implement
    # 1. Validate layer
    # 2. Optionally verify observations exist
    # 3. Call mcp__dora-mcp__link(source_id, target_id, layer, strength)
    # 4. Handle errors
    raise NotImplementedError("Task 1.3.1")


# ==============================================================================
# CANDIDATE SEARCH & DUPLICATE PREVENTION
# ==============================================================================

def search_candidates(realm: str, info: Dict[str, Any],
                     limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for candidate observations.

    Args:
        realm: Observation realm
        info: Search info dict
        limit: Maximum candidates to return

    Returns:
        List of candidate observations with match scores
    """
    # TODO: Implement
    # Call mcp__dora-mcp__candidates(realm, info, limit)
    # Parse response
    raise NotImplementedError("Task 1.4.1")


def find_best_match(candidates: List[Dict[str, Any]], realm: str,
                   info: Dict[str, Any]) -> Optional[str]:
    """
    Find best matching candidate using realm-specific heuristics.

    Args:
        candidates: List of candidate observations
        realm: Observation realm
        info: Info dict for comparison

    Returns:
        Best match observation ID, or None if no good match
    """
    # TODO: Implement matching heuristics per realm
    # - Code: exact qualifiedName or proximity on filePath+lineNumber
    # - UI: exact data-dgat or fuzzy on route+elementType
    # - Data: exact schema.table.column
    # - Config/Security: exact type+name
    raise NotImplementedError("Task 1.4.2")


def get_or_create_observation(realm: str, info: Dict[str, Any],
                              strength: float = DEFAULT_STRENGTH) -> Tuple[str, bool]:
    """
    Get existing observation or create new one.

    Args:
        realm: Observation realm
        info: Realm-specific info dict
        strength: Confidence value if creating new

    Returns:
        (observation_id, was_created)
    """
    # TODO: Implement
    # 1. Search candidates
    # 2. Find best match
    # 3. If match found: return existing ID, False
    # 4. If no match: create new, return new ID, True
    raise NotImplementedError("Task 1.4.3")


# ==============================================================================
# GRAPH TRAVERSAL
# ==============================================================================

def traverse_from(observation_id: str, direction: str = "both",
                 depth: int = 3, layers: List[str] = None) -> Dict[str, Any]:
    """
    Traverse graph from observation.

    Args:
        observation_id: Starting observation ID
        direction: "downstream", "upstream", or "both"
        depth: Maximum traversal depth
        layers: List of layers to filter (None = all)

    Returns:
        Subgraph dict with observations and links
    """
    # TODO: Implement
    # Call mcp__dora-mcp__traverse(id, direction, depth, layers)
    # Parse response
    raise NotImplementedError("Task 1.6.1")


def format_subgraph(subgraph: Dict[str, Any]) -> str:
    """
    Format subgraph as readable markdown.

    Args:
        subgraph: Subgraph dict from traverse

    Returns:
        Formatted markdown string
    """
    # TODO: Implement
    # Display observations and links grouped by layer
    raise NotImplementedError("Task 1.6.2")


# ==============================================================================
# QUERY-DRIVEN DISCOVERY
# ==============================================================================

def search_graph_for_question(question: str) -> List[Dict[str, Any]]:
    """
    Search graph for observations relevant to question.

    Args:
        question: User's question

    Returns:
        List of relevant observations
    """
    # TODO: Implement
    # Extract keywords, search candidates across realms
    raise NotImplementedError("Task 1.5.2")


def explore_codebase(question: str, existing_observations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Explore codebase to answer question.

    Args:
        question: User's question
        existing_observations: Observations already in graph

    Returns:
        Evidence dict with discovered elements and connections
    """
    # TODO: Implement exploration strategy
    # Use Grep, Read, codebase-memory-mcp based on question type
    raise NotImplementedError("Task 1.5.3")


def capture_discovery(evidence: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Capture discoveries as observations and links.

    Args:
        evidence: Evidence dict from exploration

    Returns:
        (list of observation IDs, list of link dicts)
    """
    # TODO: Implement
    # For each discovered element: get_or_create_observation
    # For each connection: create_link
    raise NotImplementedError("Task 1.5.4")


def synthesize_answer(question: str, observations: List[str],
                     links: List[Dict[str, Any]], evidence: Dict[str, Any]) -> str:
    """
    Synthesize answer from graph data and evidence.

    Args:
        question: Original question
        observations: Observation IDs involved
        links: Links created/traversed
        evidence: Raw evidence from exploration

    Returns:
        Formatted markdown answer with references
    """
    # TODO: Implement
    # Combine graph data with evidence, format as markdown
    raise NotImplementedError("Task 1.5.5")


# ==============================================================================
# COMMAND HANDLERS
# ==============================================================================

def cmd_dora_status(args: List[str]) -> str:
    """
    Handle /dora command.

    Args:
        args: Command arguments

    Returns:
        Status output as markdown
    """
    # TODO: Implement
    # Check for --switch flag
    # Show status or prompt for database selection
    raise NotImplementedError("Task 1.1.5, 1.1.6")


def cmd_dora_query(question: str) -> str:
    """
    Handle /dora-query command.

    Args:
        question: User's question

    Returns:
        Answer with observation references as markdown
    """
    # TODO: Implement full query flow
    # 1. Ensure database connected
    # 2. Search graph
    # 3. Explore if needed
    # 4. Capture discoveries
    # 5. Synthesize answer
    raise NotImplementedError("Task 1.5.6")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    """Main entry point for DORA skill."""

    if len(sys.argv) < 2:
        print("Usage: dora.py <command> [args...]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    try:
        if command == "status":
            output = cmd_dora_status(args)
        elif command == "query":
            if not args:
                print("Error: /dora-query requires a question")
                sys.exit(1)
            question = " ".join(args)
            output = cmd_dora_query(question)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

        print(output)

    except NotImplementedError as e:
        print(f"Not yet implemented: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
