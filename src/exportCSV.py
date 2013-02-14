# -*- coding: utf-8 -*-
"""
Creates CSV file(s) from the given language code/name mappings.

Ordering is alphabetical by langauge code.

"""
import csv, os

def execute(source, mappings):
  """Writes the given language code/name mappings to CSV files.

  source = string indicating source of the data, for example, 'cldr'
  mappings = list of dictionaries containing mappings"""

  # Set the export directory, relative to this script's directory
  default_directory = "../language/%s/" % source

  for entry in mappings:
    for k, v in entry.iteritems():
      dir = os.path.join(os.path.dirname(__file__), default_directory + k)
      if not os.path.exists(dir):
        os.makedirs(dir)
      #csvwriter = csv.writer(dir + "/language.xml")
      with open(dir + "/language.csv", "wb") as f:
        #csv.DictWriter(f, fieldnames=('code', 'name'), restval='raise')
        csvwriter = csv.writer(f)
        for lang_code, lang_name in sorted(v.iteritems()):
          csvwriter.writerow([lang_code, lang_name])