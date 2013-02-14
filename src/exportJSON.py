# -*- coding: utf-8 -*-
"""
Creates JSON file(s) from the given language code/name mappings.

Order is alphabetical by language code.

"""
import json, os

def execute(source, mappings):
  """Writes the given language code/name mappings to JSON files.

  source = string indicating source of the data, for example, 'cldr'
  mappings = list of dictionaries containing mappings"""

  # Set the export directory, relative to this script's directory
  default_directory = "../language/%s/" % source

  for entry in mappings:
    for k, v in entry.iteritems():
      dir = os.path.join(os.path.dirname(__file__), default_directory + k)
      if not os.path.exists(dir):
        os.makedirs(dir)
      with open(dir + "/language.json", "w") as f:
        f.write(json.dumps(v, sort_keys=True))