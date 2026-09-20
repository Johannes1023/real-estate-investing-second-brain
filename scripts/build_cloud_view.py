#!/usr/bin/env python3
"""Build a fresh, allowlisted Markdown workspace for a cloud AI assistant."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import sys


TOPIC_FOLDERS = {
    'ActivityLog', 'BuildingManagement', 'Contacts', 'Handovers', 'Insurance',
    'Leases', 'Loans', 'Miscellaneous', 'OperatingCosts', 'Playbooks',
    'Properties', 'Purchases', 'RentReviews', 'Repairs', 'Tenants',
}
ROOT_MARKDOWN = {
    'AGENTS.md', 'AI_ACCESS.md', 'CLAUDE.md', 'Deadlines.md', 'README.md',
    '_hot.md', '_index.md',
}
LOCAL_ONLY_FOLDER = 'local_only'
LOCAL_OVERVIEWS = {'_index.md', '_hot.md', 'Deadlines.md', 'README.md'}
NON_EXPORT_FOLDERS = {'.git', '.obsidian', 'scripts', 'tests', 'private', 'originals', 'backups'}
ACCESS_VALUES = {'cloud_ok', 'local_only', 'no_ai'}
SUSPICIOUS = {
    'email address': re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.I),
    'IBAN-like value': re.compile(r'\b[A-Z]{2}\d{2}(?:[ -]?\d){10,30}\b'),
    'phone-like value': re.compile(r'(?<!\d)(?:\+49|0049|\+1[ -]?)\d[\d /.-]{6,}\d(?!\d)'),
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'credential assignment': re.compile(r'(?im)^\s*(?:password|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*\S+'),
}
LINK = re.compile(r'(?<!!)\[[^]]+\]\(([^)]+)\)')
DEADLINE = re.compile(r'^  - "(\d{4}-\d{2}-\d{2}) \| ([^"]+)"$', re.M)


class ExportError(Exception):
    pass


@dataclass(frozen=True)
class Note:
    path: Path
    relative: Path
    text: str
    object_id: str
    status: str
    access: str
    summary: str
    deadlines: tuple[tuple[str, str], ...]


def metadata_value(frontmatter: str, key: str, relative: Path) -> str:
    found = re.findall(rf'^{re.escape(key)}:([^\n]*)$', frontmatter, re.M)
    if len(found) != 1 or not found[0].strip():
        raise ExportError(f'{relative}: expected exactly one nonempty {key} field')
    return found[0].strip().strip('"\'')


def parse_note(path: Path, source: Path) -> Note:
    if path.is_symlink():
        raise ExportError(f'{path.relative_to(source)}: symbolic links are not allowed')
    relative = path.relative_to(source)
    text = path.read_text(encoding='utf-8')
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise ExportError(f'{relative}: missing YAML frontmatter')
    frontmatter = match.group(1)
    access = metadata_value(frontmatter, 'ai_access', relative)
    if access not in ACCESS_VALUES:
        raise ExportError(f'{relative}: unknown ai_access value {access!r}')
    object_id = metadata_value(frontmatter, 'object', relative)
    status = metadata_value(frontmatter, 'status', relative)
    metadata_value(frontmatter, 'as_of', relative)
    metadata_value(frontmatter, 'source', relative)
    if not path.name.startswith(object_id + '_'):
        raise ExportError(f'{relative}: file name does not match object')
    summary_match = re.search(r'^## Summary\n\n(.+?)(?=\n\n|\Z)', text, re.M | re.S)
    if not summary_match:
        raise ExportError(f'{relative}: missing nonempty Summary')
    summary = ' '.join(summary_match.group(1).split())
    deadlines = tuple(DEADLINE.findall(frontmatter))
    return Note(path, relative, text, object_id, status, access, summary, deadlines)


def discover(source: Path) -> list[Note]:
    notes: list[Note] = []
    for child in source.iterdir():
        if child.is_symlink():
            raise ExportError(f'{child.name}: symbolic links are not allowed')
        if child.is_file():
            if child.suffix == '.md' and child.name not in ROOT_MARKDOWN:
                raise ExportError(f'{child.name}: unrecognized root Markdown file')
            continue
        if not child.is_dir():
            continue
        if child.name in NON_EXPORT_FOLDERS:
            continue
        if child.name == 'no_ai':
            raise ExportError('no_ai/ is inside the AI-connected source; move it outside')
        if child.name != LOCAL_ONLY_FOLDER and child.name not in TOPIC_FOLDERS:
            raise ExportError(f'{child.name}/: unrecognized folder; review before exporting')
        for path in child.rglob('*'):
            if path.is_symlink():
                raise ExportError(f'{path.relative_to(source)}: symbolic links are not allowed')
            if not path.is_file() or path.suffix != '.md' or path.name == '_template.md':
                continue
            if child.name == LOCAL_ONLY_FOLDER and path.parent == child and path.name in LOCAL_OVERVIEWS:
                continue
            note = parse_note(path, source)
            if child.name == LOCAL_ONLY_FOLDER and note.access != 'local_only':
                raise ExportError(f'{note.relative}: files in local_only/ must be local_only')
            if child.name != LOCAL_ONLY_FOLDER and note.access == 'local_only':
                raise ExportError(f'{note.relative}: move local_only notes into local_only/ before exporting')
            if note.access == 'no_ai':
                raise ExportError(f'{note.relative}: no_ai material must live outside AI-connected folders')
            notes.append(note)
    return notes


def check_cloud_notes(source: Path, notes: list[Note]) -> list[Note]:
    selected = [note for note in notes if note.access == 'cloud_ok']
    selected_paths = {note.path.resolve() for note in selected}
    for note in selected:
        for label, pattern in SUSPICIOUS.items():
            if pattern.search(note.text):
                raise ExportError(f'{note.relative}: possible {label} in cloud_ok note; review and reclassify')
        for target in LINK.findall(note.text):
            target = target.split('#', 1)[0]
            if not target:
                continue
            if '://' in target or target.startswith('/'):
                raise ExportError(f'{note.relative}: external or absolute link is not allowed in cloud view')
            resolved = (note.path.parent / target).resolve()
            if not resolved.is_relative_to(source) or resolved not in selected_paths:
                raise ExportError(f'{note.relative}: link points outside cloud_ok notes: {target}')
    return selected


def render_cloud_files(output: Path, selected: list[Note]) -> None:
    for note in selected:
        destination = output / note.relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(note.path, destination)

    (output / 'README.md').write_text(
        '# Cloud AI view\n\nThis workspace was generated from explicitly classified `cloud_ok` notes. '
        'No local-only notes or private overview files were copied. Review this folder before connecting a cloud API. '
        'Edits here do not automatically update the private working copy.\n', encoding='utf-8')
    (output / 'AGENTS.md').write_text(
        '# Cloud AI rules\n\nThis is a cloud-only view. Read and edit only the `cloud_ok` notes present here. '
        'Never request, retrieve, or infer excluded local-only material. Read `_index.md` to route questions; '
        'read `Deadlines.md` for dates. Do not use a local session that has seen restricted data as cloud context.\n',
        encoding='utf-8')
    (output / 'CLAUDE.md').write_text('@AGENTS.md\n', encoding='utf-8')
    (output / '_hot.md').write_text(
        f'# Cloud view snapshot\n\n{len(selected)} explicitly `cloud_ok` topic notes were exported. '
        'No private activity snapshot was copied.\n', encoding='utf-8')

    index_lines = ['# Cloud note index', '', 'Only `cloud_ok` notes are listed.', '',
                   '| Note | Object | Status | AI access | Summary |', '|---|---|---|---|---|']
    for note in sorted(selected, key=lambda item: item.relative.as_posix()):
        label = note.relative.stem.replace('_', ' ')
        summary = note.summary.replace('|', '\\|')
        index_lines.append(f'| [{label}]({note.relative.as_posix()}) | {note.object_id} | {note.status} | cloud_ok | {summary} |')
    (output / '_index.md').write_text('\n'.join(index_lines) + '\n', encoding='utf-8')

    deadline_rows = sorted((date, action, note.object_id, note.relative.as_posix())
                           for note in selected for date, action in note.deadlines)
    deadline_lines = ['# Cloud-safe deadlines', '', 'Only dates from `cloud_ok` notes are listed. No reminders are sent.', '',
                      '| Date | Action | Object | Note |', '|---|---|---|---|']
    for date, action, object_id, relative in deadline_rows:
        deadline_lines.append(f'| {date} | {action.replace("|", "\\|")} | {object_id} | [{Path(relative).stem}]({relative}) |')
    (output / 'Deadlines.md').write_text('\n'.join(deadline_lines) + '\n', encoding='utf-8')


def build(source: Path, output: Path) -> tuple[int, int]:
    source = source.resolve()
    output = output.resolve()
    if not source.is_dir():
        raise ExportError('source must be an existing directory')
    if output == source or output.is_relative_to(source) or source.is_relative_to(output):
        raise ExportError('output must be outside the source tree')
    if output.exists() and any(output.iterdir()):
        raise ExportError('output must be a new or empty directory; stale exports are not overwritten')
    notes = discover(source)
    selected = check_cloud_notes(source, notes)
    output.mkdir(parents=True, exist_ok=True)
    render_cloud_files(output, selected)
    return len(selected), len(notes) - len(selected)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path, help='private working-copy directory')
    parser.add_argument('--output', required=True, type=Path, help='new cloud-view directory outside source')
    args = parser.parse_args()
    try:
        included, excluded = build(args.source, args.output)
    except (ExportError, OSError, UnicodeError) as exc:
        print(f'Cloud view not created: {exc}', file=sys.stderr)
        return 1
    print(f'Cloud view created: {included} cloud_ok notes; {excluded} restricted notes excluded. Review before cloud use.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
