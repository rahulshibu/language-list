# -*- coding: utf-8 -*-
"""
Creates XML file(s) from the given language code/name mappings.

Order is alphabetical by language code.

"""
import os
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

def execute(source, mappings):
  """Writes the given language code/name mappings to XML files.

  source = string indicating source of the data, for example, 'cldr'
  mappings = list of dictionaries containing mappings"""

  # Set the export directory, relative to this script's directory
  default_directory = "../language/%s/" % source

  for entry in mappings:
    for k, v in entry.iteritems():
      dir = os.path.join(os.path.dirname(__file__), default_directory + k)
      if not os.path.exists(dir):
        os.makedirs(dir)
      with open(dir + "/language.xml", "w") as f:
        top = Element('languages')
        for lang_code, lang_name in sorted(v.iteritems()):
          child = SubElement(top, 'language')
          entry = SubElement(child, 'code')
          entry.text = lang_code
          entrytwo = SubElement(child, 'name')
          entrytwo.text = lang_name.decode('utf-8')
        f.write(prettify(top))

def prettify(elem):
  """Return a pretty-printed XML string for the Element.
  """
  rough_string = ElementTree.tostring(elem, 'utf-8')
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ", encoding='utf-8')