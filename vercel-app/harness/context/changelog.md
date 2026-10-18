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
