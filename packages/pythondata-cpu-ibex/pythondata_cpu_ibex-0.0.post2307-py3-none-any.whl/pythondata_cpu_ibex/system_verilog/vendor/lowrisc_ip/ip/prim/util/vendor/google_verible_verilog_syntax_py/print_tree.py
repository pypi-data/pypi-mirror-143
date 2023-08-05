#!/usr/bin/env python3
# Copyright 2017-2020 The Verible Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pretty-print Verilog Concrete Syntax Tree

Usage: print_tree.py PATH_TO_VERIBLE_VERILOG_SYNTAX \\
                     VERILOG_FILE [VERILOG_FILE [...]]

Visualizes tree generated by ``verible-verilog-syntax --export_json ...``.
Values enclosed in ``[]`` are node tags. ``@(S-E)`` marks token's start (S)
and end (E) byte offsets in source code. When a token's text in source code
is not the same as its tag, the text is printed in single quotes.
"""

import sys

import anytree

import verible_verilog_syntax


def process_file_data(path: str, data: verible_verilog_syntax.SyntaxData):
  """Print tree representation to the console.

  The function uses anytree module (which is a base of a tree implementation
  used in verible_verilog_syntax) method to print syntax tree representation
  to the console.

  Args:
    path: Path to source file (used only for informational purposes)
    data: Parsing results returned by one of VeribleVerilogSyntax' parse_*
          methods.
  """
  print(f"\033[1;97;7m{path} \033[0m\n")
  if data.tree:
    for prefix, _, node in anytree.RenderTree(data.tree):
      print(f"\033[90m{prefix}\033[0m{node.to_formatted_string()}")
    print()


def main():
  if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} PATH_TO_VERIBLE_VERILOG_SYNTAX " +
          "VERILOG_FILE [VERILOG_FILE [...]]")
    return 1

  parser_path = sys.argv[1]
  files = sys.argv[2:]

  parser = verible_verilog_syntax.VeribleVerilogSyntax(executable=parser_path)
  data = parser.parse_files(files, options={"gen_tree": True})

  for file_path, file_data in data.items():
    process_file_data(file_path, file_data)


if __name__ == "__main__":
  sys.exit(main())
