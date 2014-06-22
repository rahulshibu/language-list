# -*- coding: utf-8 -*-
"""
Exporter classes for export of the given data to various different file formats.
"""
import csv, json, os, yaml
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

class Exporter:
  def execute(self):
    raise NotImplementedError("Subclass must implement abstract method")

  # Set the export directory, relative to this script's directory
  def get_directory(self, source):
    return "../language/%s/" % source

class ExportAndroidXML(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to Android XML resource files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    
    # Get language names in English as a dict for inclusion in XML comments
    english_pairs = {}
    for entry in mappings:
      for k, v in entry.iteritems():
        if k == 'en':
          english_pairs = v
          break
    
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + "android/values-" + k)
        if not os.path.exists(dir):
          os.makedirs(dir)
        with open(dir + "/arrays.xml", "w") as f:
          top = Element('resources')
          if k in english_pairs.keys():
            top_comment = ElementTree.Comment(' ' + english_pairs[k].decode('utf-8') + ' (' + k + ') ')
          else:
            top_comment = ElementTree.Comment(' ' + k + ' ')
          top.append(top_comment)
          child = SubElement(top, 'string-array')          
          child.attrib['name'] = 'languages_all'
          for lang_code, lang_name in sorted(v.iteritems()):
            if k in english_pairs.keys():
              comment = ElementTree.Comment(' ' + lang_code + ' - ' + english_pairs[lang_code].decode('utf-8') + ' ')
            else:
              comment = ElementTree.Comment(' ' + lang_code + ' ')
            child.append(comment)
            entry = SubElement(child, 'item')
            entry.text = lang_name.decode('utf-8')
          f.write(self.prettify(top))
  
  def prettify(self, elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

class ExportCSV(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to CSV files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + k)
        if not os.path.exists(dir):
          os.makedirs(dir)
        with open(dir + "/language.csv", "wb") as f:
          csvwriter = csv.writer(f)
          for lang_code, lang_name in sorted(v.iteritems()):
            csvwriter.writerow([lang_code, lang_name])

class ExportJSON(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to JSON files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + k)
        if not os.path.exists(dir):
          os.makedirs(dir)
        with open(dir + "/language.json", "w") as f:
          f.write(json.dumps(v, sort_keys=True))

class ExportTXT(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to text files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + k)
        if not os.path.exists(dir):
          os.makedirs(dir)
        with open(dir + "/language.txt", "w") as f:
          for lang_code, lang_name in sorted(v.iteritems()):
            f.write("%s (%s)\n" % (lang_name, lang_code))

class ExportXML(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to XML files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + k)
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
          f.write(self.prettify(top))

  def prettify(self, elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

class ExportYAML(Exporter):
  def execute(self, mappings, source):
    """Writes the given language code/name mappings to YAML files.

    source = string indicating source of the data, for example, 'cldr'
    mappings = list of dictionaries containing mappings"""
    for entry in mappings:
      for k, v in entry.iteritems():
        dir = os.path.join(os.path.dirname(__file__), self.get_directory(source) + k)
        if not os.path.exists(dir):
          os.makedirs(dir)
        with open(dir + "/language.yaml", "w") as f:
          f.write(yaml.safe_dump(v, default_flow_style=False))
