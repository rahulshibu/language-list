# -*- coding: utf-8 -*-
"""
Importer classes for retrieving language code/name mappings from a data source.
"""
import elementtree.ElementTree as ET
import os, requests, sys, zipfile

class Importer:
  def execute(self):
    raise NotImplementedError("Subclass must implement abstract method")

class ImportCLDR(Importer):
  """
  Imports language code/name mappings from Unicode CLDR data.
  Skips alternate names for languages. Only the first language name for a language code is reported.
  """
  # Download location for CLDR data file
  download_location = "http://unicode.org/Public/cldr/latest/core.zip"

  # Path within zip file where language files -- for example, "en.xml" -- are located
  zipfile_path = "common/main/"

  # String identifying the data source
  source = "cldr"

  def execute(self, language):
    """Retrieve and import language data.

    language = A single language code, or '*' for all languages

    Returns: list of dictionaries
    """
    download_location = self.download_location
    source = self.source
    zipfile_path = self.zipfile_path
    pathname, filename = os.path.split(download_location)
    # Warning: If zip file exists in current directory, it will not be re-downloaded
    if not os.path.exists(filename):
      # Download the file
      r = requests.get(download_location)
      if r.status_code != 200:
        sys.exit("Downoad failed.")
      fh = open(filename, "wb")
      fh.write(r.content)
      fh.close()

    # Get the file from zip: /common/main/en.xml
    zf = zipfile.ZipFile(filename, 'r')
    if language == '*':
      try:
        l = list()
        for f in zf.namelist():
          xml_data = ''
          if f[0:len(zipfile_path)] == zipfile_path:
            path, file = os.path.split(f)
            lang = file[:-len('.xml')]
            xml_data = zf.read(zipfile_path + file)
            if xml_data != None:
              extracted_data = self.extract_data(xml_data)
              if extracted_data != None:
                mappings = dict([(lang, extracted_data)])
                l.append(mappings)
        return (l, source)
      finally:
        zf.close()

    if language != '*':
      try:
        xml_data = zf.read(zipfile_path + language + '.xml')
        if xml_data != None:
          extracted_data = self.extract_data(xml_data)
          if extracted_data == None:
            return None
          mappings = dict([(language, extracted_data)])
          l = list()
          l.append(mappings)
          return (l, source)
      finally:
        zf.close()

  def extract_data(self, xml_data):
    """Import the data from XML into a dictionary

    xml_data: string containing all XML from CLDR for a language code or locale code"""
    root = ET.fromstring(xml_data)
    try:
      langs = root.find('localeDisplayNames').find('languages')
    except AttributeError:
      return None
    if langs is None:
      return None
    mappings = dict()
    for child in langs:
      # Skip alternate names. For example, code 'az' has 'Azerbaijani' and alternate name 'Azeri'
      try:
        child.attrib['alt']
        continue
      except:
        pass
      mappings[child.attrib['type']] = child.text.encode("utf-8")
    if len(mappings) == 0:
      return None
    return mappings
