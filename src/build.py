# -*- coding: utf-8 -*-
"""
Builds a list of language codes and associated language names in different languages and formats.

"""
import argparse
import importCLDR
import exportCSV, exportJSON, exportTXT, exportXML, exportYAML

# Set defaults
default_source = "cldr" # Currently only 'cldr' is supported
default_language = "*" # A two-letter code, or '*' for all languages
default_fileformat = "*" # 'csv', 'json', 'txt', 'xml', 'yaml', or '*' for all formats

source = ""
language = ""
fileformat = ""

def configure(src, lang, fmt):
  global source, language, fileformat
  source = src
  language = lang
  fileformat = fmt

def execute():
  # For a data import source, only CLDR is implemented
  mappings = importCLDR.execute(language)

  # Run the exporter
  if mappings != None:
    if fileformat == "csv" or fileformat == "*":
      exportCSV.execute(source, mappings)
    if fileformat == "json" or fileformat == "*":
      exportJSON.execute(source, mappings)
    if fileformat == "txt" or fileformat == "*":
      exportTXT.execute(source, mappings)
    if fileformat == "xml" or fileformat == "*":
      exportXML.execute(source, mappings)
    if fileformat == "yaml" or fileformat == "*":
      exportYAML.execute(source, mappings)

def main():
  # Get command line arguments
  parser = argparse.ArgumentParser(add_help=True)
  parser.add_argument('-i', nargs='?', help='profile filename', default=default_source, required=False)
  parser.add_argument('-l', nargs='?', help='language', default=default_language, required=False)
  parser.add_argument('-f', nargs='?', help='file format', default=default_fileformat, required=False)
  opts = parser.parse_args()
  configure(opts.i, opts.l, opts.f)
  execute()

if __name__ == "__main__":
    main()