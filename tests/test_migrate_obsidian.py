import tempfile
import unittest
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

from scripts.migrate_obsidian import convert


class MigrationTests(unittest.TestCase):
    def render(self, source):
        migrated = convert(source, Path("note.md"))
        self.assertEqual(migrated, convert(migrated, Path("note.md")))
        return BeautifulSoup(markdown.markdown(migrated, extensions=[
            "admonition", "pymdownx.details", "pymdownx.highlight", "pymdownx.superfences",
            "tables", "attr_list", "pymdownx.arithmatex",
        ], extension_configs={"pymdownx.arithmatex": {"generic": True}}), "html.parser")

    def test_nested_and_adjacent_callouts(self):
        tree = self.render('> [!note] Outer\n> Text\n>> [!proof]- Proof\n>> - A\n>> - B\n> [!tip]+ Next\n> Tip\n')
        self.assertIsNotNone(tree.select_one('.admonition.note details.note:not([open])'))
        self.assertEqual(len(tree.select('.admonition.note details li')), 2)
        self.assertIsNotNone(tree.select_one('details.tip[open]'))
        self.assertEqual(tree.select_one('details.note summary').text, 'Proof')

    def test_paragraph_followed_by_list(self):
        tree = self.render('**Title**\n- One\n   - Nested\n- Two\n')
        self.assertEqual(len(tree.select('ul > li')), 3)
        self.assertEqual(tree.select_one('ul ul li').text, 'Nested')

    def test_callout_with_incidental_leading_space(self):
        tree = self.render(' > [!info] Title\n > Body\n')
        self.assertEqual(tree.select_one('.admonition.info .admonition-title').text, 'Title')

    def test_multiline_math_after_prose_and_adjacent_blocks(self):
        tree = self.render('Formula: $$\nx^2\n$$$$\ny^2\n$$ After\n\n> [!note]\n> Text\n')
        self.assertEqual(len(tree.select('div.arithmatex')), 2)
        self.assertIsNotNone(tree.select_one('.admonition.note'))

    def test_code_is_literal(self):
        source = '```python\nx = [[1, 2], [3, 4]]\n# > [!note]\n\tprint("$$x$$")\n```\n'
        self.assertEqual(convert(source, Path('note.md')), source)

    def test_code_tabs_survive_callouts(self):
        source = '> [!code]\n> ```python\n> def f():\n> \treturn 1\n> ```\n'
        first = convert(source, Path('note.md'))
        self.assertIn('    \treturn 1', first)
        self.assertEqual(first, convert(first, Path('note.md')))

    def test_indented_fence_with_shallower_code(self):
        tree = self.render('> [!example]\n>     ```python\n> def f():\n>     return 1\n>     ```\n')
        code = tree.select_one('.admonition .highlight pre code')
        self.assertEqual(code.get_text(), 'def f():\n    return 1\n')
        self.assertIsNotNone(code.select_one('span.k'))

    def test_quoted_fence_does_not_interpret_callout_or_wikilink(self):
        tree = self.render('> [!example]\n> ```text\n> [!bug] literal\n> [[missing]]\n> ```\n')
        self.assertEqual(len(tree.select('.admonition')), 1)
        self.assertIn('[!bug] literal\n[[missing]]', tree.select_one('pre code').text)

    def test_blank_tabs_inside_fence_are_stable(self):
        source = '> [!code]\n> ```sql\n> SELECT 1;\n> \t\n> SELECT 2;\n> ```\n'
        first = convert(source, Path('note.md'))
        self.assertEqual(first, convert(first, Path('note.md')))
        self.assertIn('    \t\n', first)

    def test_unclosed_code_fails_before_migration(self):
        with self.assertRaisesRegex(ValueError, 'unclosed code fence'):
            convert('```python\nx = 1\n', Path('note.md'))

    def test_local_note_links(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'note.md'
            (path.parent / 'Chapter8.md').touch()
            result = convert('[[Chapter8|Cycle GAN]] and [chapter](Chapter8)\n', path)
            self.assertEqual(result, '[Cycle GAN](Chapter8.md) and [chapter](Chapter8.md)\n')

    def test_frontmatter(self):
        source = '---\ntags:\n  - test\n---\n\n# Title\n'
        self.assertEqual(convert(source, Path('note.md')), source)

    def test_table(self):
        tree = self.render('Label\n| A | B |\n| --- | --- |\n| x | y |\n')
        self.assertEqual(len(tree.select('table td')), 2)

    def test_math_inside_callout_and_list(self):
        tree = self.render('> [!note]\n> $$x_0^2$$\n\n- Formula: $$f[x_0](x-x_0)$$ then $$y=2$$\n')
        self.assertEqual(len(tree.select('div.arithmatex')), 3)
        self.assertEqual(len(tree.select('li div.arithmatex')), 2)
        self.assertFalse(tree.select('a'))

    def test_image_dimensions_and_missing_attachment(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'note.md'
            (path.parent / 'images').mkdir()
            (path.parent / 'images' / '图.png').touch()
            result = convert('![[旧目录/图.png|336x204]]\n', path)
            self.assertIn('width="336" height="204"', result)
            self.assertIn('images/%E5%9B%BE.png', result)
            self.assertEqual(result, convert(result, path))
            with self.assertRaises(ValueError):
                convert('![[missing.png]]', path)


if __name__ == '__main__':
    unittest.main()
