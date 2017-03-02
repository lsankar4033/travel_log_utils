"""Converts org subtree corresponding to a travel log entry to markdown to be inserted into an e-mail.

Usage:
  org_to_md.py <input_file> <entry_heading>

Options:
  -h --help     Show this screen.

"""
from docopt import docopt
from itertools import islice, takewhile

import re

def _is_subheader_fn(header_depth):
    # TODO - implement curried fn
    pass

def build_markdown_str(org_file, entry_heading):
    org_lines = []
    with open(org_file, "r") as f:
        org_lines = list(f)

    # Figure out what line the entry starts at
    entry_pattern = r"(\*+)\s*({})\s*".format(entry_heading)
    entry_matches = [(i, re.fullmatch(entry_pattern, l).groups())
                      for i, l in enumerate(org_lines) if re.fullmatch(entry_pattern, l)]
    if len(entry_matches) == 0:
        return False

    # Information about entry header line
    (start, (header, entry_name)) = entry_matches[0]
    entry_header_depth = len(header)

    # Figure out what line the entry ends at
    entry_to_doc_end = org_lines[start+1:]
    entry_to_end = takewhile(_is_subheader_fn(entry_header_depth), org_lines)
    end = len(entry_to_end) + 1

    entry_lines = islice(org_lines, start, end)
    print(entry_lines)

    # TODO
    # find number of '*'s and take all following lines until we first encounter a line with <= '*'s
    # (islice on original list)

    # TODO convert '*'s to '#'s and links from [[]] to []()

    return "foo"

if __name__ == "__main__":
    arguments = docopt(__doc__)
    markdown_str = build_markdown_str(arguments["<org_file>"], arguments["<entry_heading>"])

    if not markdown_str:
        print("Couldn't find entry with heading {}".format(arguments["<entry_heading>"]))
    else:
        print(markdown_str)
