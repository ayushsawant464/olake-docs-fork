# Harness Evolution Changelog

### Version 1.0 (Initial Draft)
- Initial baseline harness synthesized by DRAFT agent based on docs structure.
- Navigation heuristics established for Sources, Iceberg Catalogs, and Installation.
- Security guardrails active: untrusted user input handling and secret redacting.

### Version 2.0
- Refined rules to address 1 failure classes: Navigational routing and keyword precision.
  - Addressed: Navigational routing and keyword precision

### Version 4.0
- Refined rules to address 1 failure classes: Navigational routing and keyword precision.
  - Addressed: Navigational routing and keyword precision

### Version 5.0
- Refined rules to address 1 failure classes: Out-of-scope writer destination hallucination.
  - Addressed: Out-of-scope writer destination hallucination

### Version 6.0
- Refined rules to address 2 failure classes: Navigational routing and keyword precision, Out-of-scope writer destination hallucination.
  - Addressed: Navigational routing and keyword precision
  - Addressed: Out-of-scope writer destination hallucination

### Version 7.0
- Refined rules to address 1 failure classes: Out-of-scope writer destination hallucination.
  - Addressed: Out-of-scope writer destination hallucination

### Iteration 15 (LLM Updater)
- Addressed three specific failure classes. First, significantly hardened security guardrails to prevent shell command execution from user-pasted logs (INJECTION_VULNERABILITY). Second, reinforced the scope boundaries to explicitly forbid SQL querying and BI charting in the OLake UI (HALLUCINATION). Third, improved the tool strategy to avoid missed target pages by enforcing a 'verify-and-fetch' step for critical navigation targets.
  - Addressed: Prompt injection and code execution in logs
  - Addressed: Hallucination of BI/SQL capabilities in the OLake UI
  - Addressed: Failed retrieval of explicit documentation targets (docs/intro.mdx)

### Iteration 16 (LLM Updater)
- Addressed a specific Retrieval Navigation Failure (q-u2-4). The harness was updated to enforce an explicit, structured search strategy for retrieving complex nested configuration paths (specifically finding Source configurations under a Core Configs path). The 'Docs First' rule was strengthened to explicitly enumerate common source directories to prevent the agent from failing to locate existing documentation.
  - Addressed: Failed retrieval of nested configuration pages (e.g., 'Core Configs' paths)
  - Addressed: Inability to locate documentation for standard source connectors (e.g., Postgres)

### Iteration 20 (LLM Updater)
- Updated the harness to enforce strict anti-hallucination rules regarding speculative internals (sizing, benchmarks) and strictly enforce the 'Docs First' policy for all configuration. Added explicit negative constraints to prevent acceptance of false premises regarding table deletion and out-of-scope BI features. Expanded the 'Scope Boundaries' section to explicitly reject SQL querying and charting claims in the UI.
  - Addressed: Reinforced strict limitation on speculative/internal details (preventing UNJUSTIFIED_CONFIDENCE).
  - Addressed: Enforced boundary checks to prevent hallucinating SQL querying/BI charting capabilities (preventing HALLUCINATION on UI).
  - Addressed: Added forced-refutation logic for common false premises regarding table deletion (preventing False Premise acceptance).
  - Addressed: Hardened the 'Docs First' rule to explicitly prioritize `docs/connectors/` for connector-specific behavioral questions.

### Iteration 21 (LLM Updater)
- Addressed repeated NAVIGATION_FAILURE issues where the agent failed to locate standard documentation entry points (Intro, Docker CLI, Source Configs). The failures suggest the agent may have been over-indexing on local tool calls or searching 'kitchen-sink' queries that returned false positives. The fix involves strengthening the 'Search Heuristics' and adding 'Index Verification' rules to ensure the agent prioritizes the canonical `docs/` directory structure before falling back to repository searches.
  - Addressed: General Navigation Failure for Canonical Docs
  - Addressed: Lack of specific heuristics for finding 'Getting Started' and 'Installation' pages
  - Addressed: Potential over-reliance on repository search vs. structured docs index

### Iteration 25 (LLM Updater)
- Updated harness to address Navigation Failures where standard path queries ('source.mdx', 'postgres/index.mdx') failed to retrieve files despite known existence. Added 'Index First' triggers for specific file patterns and improved Directory Navigation Rules to explicitly handle 'core/configs' and connector paths via `list_docs` before finalizing answers.
  - Addressed: Ineffective Retrieval of Standard Path Configuration Files (source.mdx)
  - Addressed: Failure to Navigate to Specific Connector Index Files (postgres/index.mdx)
