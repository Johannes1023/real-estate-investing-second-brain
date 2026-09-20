# AI access and data classification

This repository is a synthetic demonstration. Its live notes contain no real sensitive data and all use `ai_access: cloud_ok`. In a **separate private working copy**, classify each note before connecting an AI assistant.

| `ai_access` | Examples in a real private copy | Local AI | Cloud API | Storage rule |
|---|---|---|---|---|
| `cloud_ok` | Non-sensitive summaries deliberately approved for cloud processing | Read and edit | Read and edit in the cloud view | May be exported after review |
| `local_only` | Tenant identities, exact property details, private amounts or correspondence that the landlords permit an offline model to process | Read and edit in the private working copy | No access | Keep in `local_only/` or another private location; never commit to this demo |
| `no_ai` | Passwords, recovery codes, full bank or identity numbers, unredacted originals, or anything the landlords exclude from AI | No access | No access | Keep outside every AI-connected folder |

**Missing or unrecognized `ai_access` means no AI access.** The class applies to the entire note, including its title, filename, summary, metadata, links, and deadlines. A summary derived from `local_only` information is also `local_only` until a person explicitly writes and approves a separate non-sensitive summary. Never downgrade a note automatically.

Keep derived files separate as well. Root `_index.md`, `_hot.md`, `Deadlines.md`, and `ActivityLog/` contain only `cloud_ok` facts. A verified local assistant may create `local_only/_index.md`, `local_only/_hot.md`, `local_only/Deadlines.md`, and `local_only/ActivityLog/` for restricted material. The `local_only/` directory is ignored by Git in this example. Do not rely on that ignore rule as protection if files were already committed or manually force-added.

## Two physically separate AI workflows

1. **Local workflow:** Connect a verified local AI/LLM to the private working copy. It can read and update `cloud_ok` and `local_only` notes. Keep `no_ai` records outside its accessible folders. Verify that model inference, embeddings, logs, backups, plugins, and fallback services do not send the sensitive context to a remote provider.
2. **Cloud workflow:** Run `scripts/build_cloud_view.py` from the private working copy to create a **new** directory containing only `cloud_ok` notes and newly generated overview files. Inspect that directory. Connect the cloud assistant only to this exported directory, never to the private working copy or a parent directory.
3. **Keep sessions separate:** A conversation that has already seen `local_only` material must not later call a cloud model or cloud-connected tool with that context. Start a fresh cloud session using only the reviewed cloud view.

The public-safe labels in this GitHub demo do not grant access to a private file. Metadata guides the workflow; **the separate directory is the actual access boundary**. `.gitignore` reduces accidental commits but is not a security boundary either.

## Worked classification example

This example is text only. It is **not** a live note and contains no real private values:

```yaml
---
object: U04
as_of: 2026-09-20
status: current
ai_access: local_only
source: Private document reference SAMPLE-U04-LOCAL
---
```

The corresponding private note could contain a tenant's real identity or a detailed payment discussion and be edited by a verified local model. The cloud view omits the entire file, its summary, and its deadlines. If a cloud-readable note links to it, the exporter stops rather than creating a broken or revealing link.

## Export command

```bash
python3 scripts/build_cloud_view.py --source /path/to/private-working-copy --output /path/to/new-cloud-view
```

The exporter requires an empty destination outside the source, checks every topic note's class, excludes `local_only` and `no_ai`, checks relative links among selected notes, and rejects common secret/contact patterns in `cloud_ok` content. It then builds a new `_index.md` and `Deadlines.md` from selected notes only. The checks cannot recognize every sensitive fact, especially names, addresses, unusual identifiers, or context that identifies a person. **Human review of the output remains required.**

Edits made by a cloud assistant in the exported copy do not automatically update the private working copy. Review each proposed change before applying it there; preserve the original note's classification or make it more restrictive. Run `Update` after accepted changes.
