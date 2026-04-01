# MagnetarPrometheus Shared Schemas

This directory is reserved for language-neutral workflow schemas, graph representations, and contract artifacts shared by the backend runtime and the future UI builder.

Initial expected contents:

- workflow definition schema
- node and edge graph schema for visual editing
- run and execution schema (jobs, runs, execution inspection)
- module manifest schema
- validation and versioning notes

## Versioning Notes

The runtime schemas and metadata use canonical version stamps rather than simple semantic versions when representing high-level product builds. The canonical format is `yyyy.MM.dd HH:mm:sss`.

Note that standard Python components in the SDK will continue to use PEP-440 compliant semantic versions (`0.1.0`) in their `pyproject.toml` files for packaging purposes, while exposing the product canonical version dynamically at runtime.
