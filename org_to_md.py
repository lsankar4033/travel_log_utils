"""Converts org subtree corresponding to a travel log entry to markdown to be inserted into an e-mail.

Usage:
  org_to_md.py <org_file>

Options:
  -h --help     Show this screen.

"""
from docopt import docopt
from itertools import islice, takewhile

import re

def _org_line_to_md_line(line):
    def header_replace(matchobj):
        subheader_depth = len(matchobj.group(0))
        # Ensures that first header of entry will have depth of 5 and no headers will have depth > 6
        return "#" * min(subheader_depth + 4, 6)
    line = re.sub(r"(\*+)", header_replace, line)

    def link_replace(matchobj):
        href = matchobj.group(1)
        link_name = matchobj.group(2)
        return "[{}]({})".format(link_name, href)
    line = re.sub(r"\[\[([^\[\]]+)\]\[([^\[\]]+)\]\]", link_replace, line)

    return line

special_line_headings = ["Cities visited: ",
                         "Dates: ",
                         "Photos: ",
                         "Till next time, "]

def _is_special_line(line):
    return any([line.startswith(h) for h in special_line_headings])

def _is_header_line(line):
    return line.startswith("#")

def _is_bullet_point_line(line):
    return line.startswith("- ")

def _is_newline_line(line):
    newline_chars = [char for char in line if char is '\n']
    return len(line) > 0 and len(newline_chars) == len(line)

def _remove_extra_newlines(lines):
    """Remove newlines between lines in a single passage while excluding the following cases:
    - special lines, like the 'Cities visited' and 'Dates' headers
    - newlines after header lines
    - explicit newlines
    - bullet lists
    """
    new_lines = []
    for i, line in enumerate(lines):
        if i is len(lines) - 1:
            new_lines.append(line)

        elif _is_special_line(line):
            new_lines.append(line)

        # Collapse passages, but keep honoring bullet point lists
        else:
            next_line = lines[i+1]

            if _is_bullet_point_line(line) or _is_bullet_point_line(next_line):
                new_lines.append(line)

            elif _is_header_line(line) or _is_header_line(next_line):
                new_lines.append(line)

            elif _is_newline_line(line) or _is_newline_line(next_line):
                new_lines.append(line)

            else:
                new_lines.append(line.strip() + " ")

    return new_lines

def build_markdown_str(org_file):
    org_lines = []
    with open(org_file, "r") as f:
        org_lines = list(f)

    md_lines = [_org_line_to_md_line(line) for line in org_lines]
    md_lines = _remove_extra_newlines(md_lines)

    return "".join(md_lines)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    markdown_str = build_markdown_str(arguments["<org_file>"])

    print(markdown_str)
