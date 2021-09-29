import re
from pathlib import Path

import click
from mako.template import Template

from novelsave_sources import novel_source_types, metadata_source_types

BASE_DIR = Path(__file__).parent

README_MAKO = BASE_DIR / 'README.md.mako'
README_FILE = BASE_DIR / 'README.md'

NOVEL_MODULE = 'novelsave_sources.sources.novel.'
NOVEL_INIT_MAKO = BASE_DIR / 'novelsave_sources/sources/novel/__init__.py.mako'

METADATA_MODULE = 'novelsave_sources.sources.metadata.'
METADATA_INIT_MAKO = BASE_DIR / 'novelsave_sources/sources/metadata/__init__.py.mako'


def unindent(text: str) -> str:
    start_pattern = re.compile(r'^ *% *(for|if)')
    end_pattern = re.compile(r'^ *% *(end)')

    indent = 4
    indent_context = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if start_pattern.match(line):
            indent_context += indent
        elif end_pattern.match(line):
            indent_context -= indent
        elif line.startswith(' ' * indent_context):
            lines[i] = line[indent_context:]

    return '\n'.join(lines) + '\n'


def render(mako_file: Path, **kwargs):
    text = Template(filename=str(mako_file), preprocessor=unindent).render(**kwargs)

    rendered_file = mako_file.parent / mako_file.stem
    with rendered_file.open('wb') as f:
        f.write(text.replace('\r', '').encode('utf-8'))

    print(f'{mako_file.relative_to(BASE_DIR)} -> {rendered_file.relative_to(BASE_DIR)}')


@click.group()
def cli():
    pass


@cli.command(name='compile')
def compile_():
    """Compile all mako files"""
    sources = sorted(novel_source_types(), key=lambda s: s.__name__)
    meta_sources = sorted(metadata_source_types(), key=lambda s: s.__name__)

    render(NOVEL_INIT_MAKO, sources=sources)
    render(METADATA_INIT_MAKO, meta_sources=meta_sources)
    render(README_MAKO, sources=sources, meta_sources=meta_sources)


if __name__ == '__main__':
    cli()
