# -*- coding: utf-8 -*-
"""
Builds a set of files in several formats, each of which contains a list of language codes and
a corresponding list of language names.
"""
import argparse
from Importer import *
from Exporter import *

# Set default
default_language = "*" # A two-letter language code, or '*' for all languages

# The list of importers to use (but only ClDR is currently implemented)
importers = [ImportCLDR()]

# The list of exporters to use
exporters = [ExportCSV(), ExportJSON(), ExportTXT(), ExportXML(), ExportYAML()]

language = ""

def configure(lang):
  global language
  language = lang

def execute():
  data_sets = []

  # Import using importers for all data sources
  for importer in importers:
    (mappings, source) = importer.execute(language)
    data_sets.append((mappings, source))

  # Export using exporters for all data output formats
  for data_set in data_sets:
    mappings = data_set[0]
    source = data_set[1]
    if mappings != None:
      for exporter in exporters:
        exporter.execute(mappings, source)

def main():
  # Get command line arguments
  parser = argparse.ArgumentParser(add_help=True)
  parser.add_argument('-l', nargs='?', help='language', default=default_language, required=False)
  opts = parser.parse_args()
  configure(opts.l)
  execute()

if __name__ == "__main__":
    main()