import re
from pathlib import Path

from mako.template import Template

from novelsave_sources import (
    metadata_source_types,
    novel_source_types,
    rejected_sources,
)

BASE_DIR = Path(__file__).parent.parent

README_MAKO = BASE_DIR / "README.md.mako"
README_FILE = BASE_DIR / "README.md"


def unindent(text: str) -> str:
    start_pattern = re.compile(r"^ *% *(for|if)")
    end_pattern = re.compile(r"^ *% *(end)")

    indent = 4
    indent_context = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if start_pattern.match(line):
            indent_context += indent
        elif end_pattern.match(line):
            indent_context -= indent
        elif line.startswith(" " * indent_context):
            lines[i] = line[indent_context:]

    return "\r\n".join(lines) + "\r\n"


def render(mako_file: Path, **kwargs):
    text = Template(filename=str(mako_file), preprocessor=unindent).render(**kwargs)

    rendered_file = mako_file.parent / mako_file.stem
    with rendered_file.open("wb") as f:
        f.write(text.encode("utf-8"))

    print(f"{mako_file.relative_to(BASE_DIR)} -> {rendered_file.relative_to(BASE_DIR)}")


def cli():
    pass


def compile():
    """Compile all mako files"""
    sources = sorted(novel_source_types(), key=lambda s: (s.lang, s.base_urls[0]))
    meta_sources = sorted(
        metadata_source_types(), key=lambda s: (s.lang, s.base_urls[0])
    )

    render(
        README_MAKO,
        sources=sources,
        meta_sources=meta_sources,
        rejected=rejected_sources,
    )


if __name__ == "__main__":
    compile()
