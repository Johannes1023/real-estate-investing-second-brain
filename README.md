# Real Estate Investing Second Brain

A complete, **synthetic** Markdown example for seven rental units managed by **two landlords**. It demonstrates how to organize facts, find answers, track deadlines, and run periodic reviews with an AI assistant. Every unit ID, tenant label, area, amount, date, event, and document reference is invented. No source documents or real personal, address, contact, banking, or contract details are included.

## The concept

Each fact lives in a short topic note. An assistant follows [AGENTS.md](AGENTS.md): read the current snapshot, use the index to find the relevant note, and open only that note for an ordinary question. The system is plain Markdown, so it also works in a text editor or Obsidian. There is no database, background process, or automatic reminder service.

The example uses unit IDs `U01` through `U07` in one imaginary building (`BUILDING`). `Landlord A` and `Landlord B` are generic roles. Adapt these IDs and roles for your own properties; they do not describe any actual ownership structure.

## Repository map

| File or folder | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Reading, writing, privacy, and workflow rules for an AI assistant |
| [_hot.md](_hot.md) | Compact current snapshot and next actions |
| [_index.md](_index.md) | Question routing, unit overview, and links to every topic note |
| [Deadlines.md](Deadlines.md) | Example deadlines collected from note metadata |
| [AI_ACCESS.md](AI_ACCESS.md) | Data classes and separate local/cloud AI workflows |
| [scripts/build_cloud_view.py](scripts/build_cloud_view.py) | Creates a fresh cloud-readable copy containing only `cloud_ok` notes |
| 15 topic folders | Completed synthetic notes plus a category-specific `_template.md` |

Every topic note has YAML metadata, a title, a short `Summary`, and relevant fields. For example:

```yaml
---
object: U02
as_of: 2026-09-20
status: current
ai_access: cloud_ok
source: Synthetic example
deadlines:
  - "2027-01-15 | Check completed faucet repair"
---
```

`status` can be `open`, `current`, or `outdated`. `ai_access` is `cloud_ok`, `local_only`, or `no_ai`; a missing value is treated as denied. `source` is a short pointer, never an embedded original document. `deadlines` is optional. Unit notes start with their ID, such as `U01_Lease.md`; shared building notes start with `BUILDING_`.

## What the filled example covers

All seven units have a completed profile, tenant-group note, lease, 2025 operating-cost reconciliation, and purchase summary. Three units illustrate financing, and U03 illustrates a proposed index-rent calculation. Building-wide examples cover management, insurance, roles, a document map, playbooks, and a review log. A repair and a move-in show event records. All amounts and dates are internally consistent synthetic values.

Try these questions with an assistant pointed at this folder:

- “What is the current example rent for U03, and which note supports it?”
- “Which units have a synthetic loan balance?”
- “What example deadlines are coming up?”
- “How would the two landlords record a tenant turnover?”

## Operating the Second Brain

| Command | Assistant behavior |
|---|---|
| Ordinary question | Read `_hot.md`, `_index.md`, and only the relevant note. Cite the note and its `as_of` date. |
| `Update` | Rebuild the note list and `Deadlines.md`, then check links, metadata, mismatches, conflicts, and possible private data. |
| `Monthly review` | Interview the landlords about stale, open, or time-sensitive entries, at most four questions per round. Apply answers and run `Update`. |
| `Fill in` | Ask for missing facts in small rounds, update only confirmed values, then run `Update`. |

These are instructions for the AI assistant, not executable scripts. Changes made by hand are welcome; run `Update` afterward. Dates in `Deadlines.md` are a snapshot and do not send notifications.

## Local AI and cloud AI

A fully local AI or LLM may read **and edit** sensitive `local_only` notes in a private working copy, provided its inference, logs, retrieval, and tools really stay local. A cloud API must receive only `cloud_ok` material. `no_ai` material is kept outside every AI-connected folder. Restricted notes and their indexes, deadlines, and activity summaries live under the Git-ignored `local_only/` directory; root overviews remain cloud-safe. All notes committed to this demo are synthetic and marked `cloud_ok`.

Use **separate workspaces and sessions**: connect a local assistant to the private working copy, and connect a cloud assistant only to a fresh export. With Python 3.10 or newer, the exporter selects only notes explicitly marked `cloud_ok`, builds a new cloud-safe index and deadline list, and rejects missing classifications or links to excluded notes:

```bash
python3 scripts/build_cloud_view.py --source /path/to/private-working-copy --output /path/to/new-cloud-view
```

The output folder must be new and outside the private source folder. Review it before sending it to a cloud provider. Classification is a routing rule, **not** encryption or a guarantee that text marked `cloud_ok` contains no sensitive facts. See [AI_ACCESS.md](AI_ACCESS.md) for the full policy and a worked local-only example.

## Reuse it safely

1. On GitHub, choose **Use this template** to create your own repository, or copy the structure into a **separate private working folder**. Keep this repository as a synthetic reference. Choose private visibility for real working data.
2. Replace every synthetic ID and value in the private copy, or remove example notes and start from the category templates. Review `AGENTS.md` there and adapt its demo-only rules to your own privacy policy. Classify each note before either AI reads it.
3. Store original contracts, scans, photos, IDs, account details, and contact information outside the AI-readable folder. Use private document references instead of embedding originals.
4. Review what your AI provider may receive before connecting a folder. Avoid simultaneous edits to the same note; `Update` checks for conflict copies.
5. Run `Update` after edits and `Monthly review` when you want to check aging facts. Check real deadlines and legal requirements against current local rules and your own documents.

This example is not legal, tax, or financial advice. Tax records and bookkeeping are outside its scope. A `.gitignore` file does not prevent real information typed into a Markdown note from entering Git history; inspect changes before committing.
