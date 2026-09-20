"""Checks for the cloud export's privacy boundaries."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_cloud_view import ExportError, build  # noqa: E402


def note(object_id: str, access: str | None, body: str, deadline: str | None = None) -> str:
    lines = ['---', f'object: {object_id}', 'as_of: 2026-09-20', 'status: current']
    if access is not None:
        lines.append(f'ai_access: {access}')
    lines.append('source: Synthetic example')
    if deadline:
        lines.extend(['deadlines:', f'  - "{deadline}"'])
    lines.extend(['---', f'# {object_id} example', '', '## Summary', '', body, '', '## Details', '', body])
    return '\n'.join(lines) + '\n'


class CloudViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / 'private-copy'
        self.output = self.base / 'cloud-copy'
        (self.source / 'Leases').mkdir(parents=True)

    def write(self, relative: str, text: str) -> None:
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_cloud_view_excludes_local_note_and_its_deadline(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', 'cloud_ok', 'Safe example.',
                                                '2027-01-15 | Review safe example'))
        self.write('local_only/U02_Private.md', note('U02', 'local_only', 'PRIVATE_SAMPLE_DETAIL',
                                                       '2027-02-15 | Private follow-up'))
        self.write('local_only/_index.md', '# Private index\n\nPRIVATE_SAMPLE_DETAIL\n')
        included, excluded = build(self.source, self.output)
        self.assertEqual((included, excluded), (1, 1))
        self.assertTrue((self.output / 'Leases/U01_Lease.md').is_file())
        self.assertFalse((self.output / 'local_only').exists())
        self.assertNotIn('PRIVATE_SAMPLE_DETAIL', (self.output / '_index.md').read_text())
        self.assertNotIn('Private follow-up', (self.output / 'Deadlines.md').read_text())
        self.assertIn('Review safe example', (self.output / 'Deadlines.md').read_text())

    def test_missing_classification_fails_closed(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', None, 'Safe example.'))
        with self.assertRaisesRegex(ExportError, 'ai_access'):
            build(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_link_to_local_only_file_blocks_export(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', 'cloud_ok',
                                                '[Restricted note](../local_only/U02_Private.md)'))
        self.write('local_only/U02_Private.md', note('U02', 'local_only', 'PRIVATE_SAMPLE_DETAIL'))
        with self.assertRaisesRegex(ExportError, 'link points outside cloud_ok'):
            build(self.source, self.output)

    def test_common_contact_pattern_blocks_misclassified_note(self) -> None:
        fake_address = 'sample' + '@' + 'example.invalid'
        self.write('Leases/U01_Lease.md', note('U01', 'cloud_ok', fake_address))
        with self.assertRaisesRegex(ExportError, 'email address'):
            build(self.source, self.output)

    def test_no_ai_material_inside_source_blocks_export(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', 'no_ai', 'PRIVATE_SAMPLE_DETAIL'))
        with self.assertRaisesRegex(ExportError, 'outside AI-connected folders'):
            build(self.source, self.output)

    def test_local_only_note_in_topic_folder_blocks_export(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', 'local_only', 'PRIVATE_SAMPLE_DETAIL'))
        with self.assertRaisesRegex(ExportError, 'move local_only notes'):
            build(self.source, self.output)

    def test_output_cannot_be_inside_private_source(self) -> None:
        self.write('Leases/U01_Lease.md', note('U01', 'cloud_ok', 'Safe example.'))
        with self.assertRaisesRegex(ExportError, 'outside the source tree'):
            build(self.source, self.source / 'cloud_exports' / 'new')


if __name__ == '__main__':
    unittest.main()
