# -*- coding: utf-8 -*-
"""
Creates text file(s) from the given language code/name mappings.

Order is alphabetical by language code.

Example:

Afar (aa)
Abkhazian (ab)
Achinese (ace)
(...)

"""
import os

def execute(source, mappings):
  """Writes the given language code/name mappings to text files.
  
  source = string indicating source of the data, for example, 'cldr'
  mappings = list of dictionaries containing mappings"""

  # Set the export directory, relative to this script's directory
  default_directory = "../language/%s/" % source

  for entry in mappings:
    for k, v in entry.iteritems():
      dir = os.path.join(os.path.dirname(__file__), default_directory + k)
      if not os.path.exists(dir):
        os.makedirs(dir)
      with open(dir + "/language.txt", "w") as f:
        for lang_code, lang_name in sorted(v.iteritems()):
          f.write("%s (%s)\n" % (lang_name, lang_code))
