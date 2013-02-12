# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 13:37:20 2013

@author: Robert
"""
import argparse
import importCLDR
import exportTXT

# Set defaults
default_source = "cldr" # Currently only 'cldr' is supported
default_language = "*" # A two-letter code, or '*' for all languages
default_fileformat = "*" # Currently only 'txt' is supported

source = ""
language = ""
fileformat = ""

def configure(src, lang, fmt):
  global source, language, fileformat
  source = src
  language = lang
  fileformat = fmt
    
def execute():
  if source == "*" or source == "cldr":
    # Run the importer for CLDR
    mappings = importCLDR.execute(language)  
  
  # Run the exporter
  if mappings != None:
    exportTXT.execute(source, mappings)


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