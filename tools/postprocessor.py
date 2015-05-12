# postprocessor.py is a refactored version of the OpenDSA preprocessor created by efouh.
# This script is designed to be run after Sphinx has generated all the HTML files.
# It corrects the chapter and section numbers for titles and hyperlinks using the data
# contained in page_chapter.json

import sys
import os
import re
import codecs
import json
import xml.dom.minidom as minidom
from pprint import pprint
from xml.etree.ElementTree import ElementTree, SubElement, Element
from bs4 import BeautifulSoup
import tarfile
import shutil
import urlparse

__author__ = 'breakid'


# Reads the starting section number and section prefix from index.rst
def parse_index_rst(source_dir):
  # Read contents of index.rst
  with open(source_dir + 'index.rst', 'r') as index_rst_file:
    index_rst = index_rst_file.readlines()

  directive = False
  sectnum = 0
  prefix = ''

  for line in index_rst:
    if '.. sectnum::' in line or '.. chapnum::' in line:
      directive = True
    elif ':prefix:' in line:
      prefix = re.split('prefix:', line, re.IGNORECASE)[1].strip()
    elif ':start:' in line:
      sectnum = int(re.split('start:', line, re.IGNORECASE)[1]) - 1

  if not directive:
    print 'Error: No .. sectnum:: or .. chapnum:: directive in index.rst. Please include the directive and try again.'
    sys.exit(1)

  return (sectnum, prefix)


# Updates the index.html page
def update_index_html(dest_dir, sectnum):
  # Process index.html separately from the modules files
  try:
    with open(dest_dir + 'index.html', 'r') as index_html_file:
      index_html = index_html_file.readlines()
  except IOError:
    with open(dest_dir + 'index.xml', 'r') as index_html_file:
      index_html = index_html_file.readlines()

  for line_num, line in enumerate(index_html):
    #inject css rule to remove haiku's orange bullets
    if '</head>' in line:
      index_html[line_num] = line.replace('</head>','<style>\nul li {\n\tbackground: none;\n\tlist-style-type: none;\n}\n</style>\n</head>')
    elif 'class="section"' in line:
      sectnum += 1
    elif 'RegisterBook' in line:
      #remove registerbook page from TOC
      index_html[line_num] = ''
    elif 'hide-from-toc' in line:
      #remove stub chapter title 
      if '<h1>' in index_html[line_num-1]:
        index_html[line_num-1] = ''
    elif 'class="toctree-l' in line and 'Gradebook' not in line and 'TODO List' not in line:
      title = re.split('>', re.split('</a>', line, re.IGNORECASE)[0], re.IGNORECASE)[-1]
      new_title = '%s.' % sectnum + title
      index_html[line_num] = line.replace(title, new_title)

  # Write the modified contents back to index.html
  with open(dest_dir + 'index.html', 'wb') as index_html_file:
    index_html_file.writelines(index_html)


# Update the headers and navigation hyperlinks in module HTML files
def update_mod_html(file_path, data, prefix):
  # Read contents of module HTML file
  with open(file_path, 'r') as html_file:
    html = html_file.readlines()

  mod_name = os.path.splitext(os.path.basename(file_path))[0]

  ignore_mods = ['index', 'Gradebook', 'search', 'RegisterBook']

  link_pattern = re.compile('<a.+href="(?P<href>.*).html">(?P<text>.*)</a>')
  title_pattern = re.compile('<title>(?P<title>.*)</title>')
  h2_pattern = re.compile('<span>(?P<header>.*)</span>')
  header_pattern = re.compile('<h\d>(?P<header>.*)<a')

  for line_num, line in enumerate(html):
    if 'id="prevmod"' in line or 'id="nextmod"' in line or 'id="prevmod1"' in line or 'id="nextmod1"' in line:
      m = re.search(link_pattern, line)
      link_text = m.group('text')
      link_mod = m.group('href')

      if link_mod in data and link_mod not in ['index', 'Gradebook', 'ToDo', 'RegisterBook']:
        new_link_text = '%s.' % data[link_mod][1] + link_text
        html[line_num] = line.replace(link_text, new_link_text)

      if link_mod in ['RegisterBook']:
        html[line_num] = line.replace(link_text, "")


    if '&lt;anchor-text&gt;' in line:
      line_args = re.split('&lt;anchor-text&gt;|&lt;/anchor-text&gt;', line)
      texts = re.split(':', line_args[1])
      if len(texts) == 2:
        html[line_num] = line.replace(texts[1] + '</em>', texts[0] + '</em>')
      html[line_num] = html[line_num].replace(line_args[1], '')
      html[line_num] = html[line_num].replace('&lt;anchor-text&gt;', '')
      html[line_num] = html[line_num].replace('&lt;/anchor-text&gt;', '') 

    if mod_name in data and mod_name not in ignore_mods:
      (chap_title, chap_num) = data[mod_name]

      if '<title>' in line:
        title = re.search(title_pattern, line).group('title')
        numbered_title = '%s.' % chap_num + title
        html[line_num] = line.replace(title, numbered_title)
      elif '<h2 class="heading"><span>' in line:
        heading = re.search(h2_pattern, line).group('header')
        header = '%s %s %s' % (prefix, chap_num, chap_title)
        html[line_num] = line.replace(heading, header)

      if re.search(header_pattern, line):
        section_title = re.search(header_pattern, line).group('header')
        new_section_title = '%s.' % chap_num + section_title
        html[line_num] = line.replace(section_title, new_section_title)

  # Replace original HTML file with modified contents
  with open(file_path, 'wb') as html_file:
    html_file.writelines(html)


def update_TOC(source_dir, dest_dir, data = None):
  (sectnum, prefix) = parse_index_rst(source_dir)

  update_index_html(dest_dir, sectnum)

  if not data:
    # Load the JSON data used to store chapter number and title information
    with open('page_chapter.json', 'r') as page_chapter_file:
      data = json.load(page_chapter_file)

  html_files = [file for file in os.listdir(dest_dir) if file.endswith('.html')]

  for file in html_files:
    update_mod_html(dest_dir + file, data, prefix)


def update_TermDef(glossary_file, terms_dict):
  with codecs.open(glossary_file, 'r', 'utf-8') as html_glossary:
    mod_data = html_glossary.readlines()
  i = 0
  while i < len(mod_data):
    line = mod_data[i].strip()
    if line.startswith('<dt'):
      tokens = re.split('</dt>', line)
      token = re.split('>', tokens[0])
      term = token[len(token) -1]
      if term in terms_dict:
        term_def = ''
        i += 1
        endofdef = False
        while (i < len(mod_data) and not endofdef):
          if '</dd>' in  mod_data[i]:  
            term_def += mod_data[i].split('</dd>')[0] + '</dd>'
            endofdef = True
          else:
            term_def += mod_data[i]
          i += 1
        terms_dict[term] = str(term_def)
        i-= 1
    i += 1
    
def update_edx_file(path, modules):
  # Read contents of module HTML file
  with codecs.open(path, 'r', 'utf-8') as html_file:
    html = html_file.read()
  
  # Get the module name and create its subfolder
  mod_name = os.path.splitext(os.path.basename(path))[0]
  print mod_name
  
  # Strip out the script, style, link, and meta tags
    
  
  soup = BeautifulSoup(html)
  
  # Strip out Script, Style, and Link tags
  for tag in ('script', 'link', 'style'):
    for s in soup(tag):
      s.extract()
  
  # Redirect href urls
  for link in soup.find_all('a'):
    if 'href' not in link.attrs:
        # Really? No href? Is that even valid HTML?
        continue
    href = link['href']
    #TODO: Check if we need to add chapter folders to the URL
    # Skip dummy urls redirecting to itself
    if href == '#':
      continue
    elif href.startswith('#'):
      # Do something with an internal page link
      continue
    elif href.startswith('mailto:'):
      continue
    elif href.startswith('http://'):
      continue
    elif href.startswith('../'):
      continue
    elif href.endswith('.rst'):
      continue
    else:
      if '#' in href:
        external, internal = href.split('#', 1)
      else:
        external, internal = href, ''
      if external.endswith('.html'):
        link['href'] = '../../'+'#'.join((external[:-5],internal))
        
      # Do something with the actual href
  
  
  '''
  TODO: Add the references to these broken-up files in the final course zip
  '''
  # Breaking file into components
  section_divs = [i for l in soup.find_all('div', class_='section') 
                    for i in l.find_all(recursive=False)]
  exercise_data = {}
  found_counter = 0
  if section_divs:
    chunked_html_files = []
    for section in section_divs:
      # If we find a slideshow or practice exercise, then write it out to a file
      if section.name == 'div' and 'data-type' in section.attrs and section['data-type'] in ('ss', 'pe'):
        path_html = os.path.join(os.path.dirname(path), '{}-{}.html'.format(mod_name, found_counter))
        with codecs.open(path_html, 'w', 'utf-8') as o:
          o.writelines(chunked_html_files)
        name = section['id']
        exercise_data[name] = {key: section[key] for key in section.attrs}
        chunked_html_files = []
        found_counter += 1
      else:
        chunked_html_files.append(str(section).decode('utf-8'))
    path_html = os.path.join(os.path.dirname(path), '{}-{}.html'.format(mod_name, found_counter))
    with codecs.open(path_html, 'w', 'utf-8') as o:
      o.writelines(chunked_html_files)
    chunked_html_files = []
  else:
    print "Failed to find any 'div' tags with a 'section' class."
    path_html = os.path.join(os.path.dirname(path), '{}-{}.html'.format(mod_name, found_counter))
    with codecs.open(path_html, 'w', 'utf-8') as o:
      o.writelines(html)
      
  # Delete the file on the way out
  #os.remove(path)
  return exercise_data
    
def pretty_print_xml(data, file_path):
    ElementTree(data).write(file_path)
    xml = minidom.parse(file_path)
    with open(file_path, 'w') as resaved_file:
        # [23:] omits the stupid xml header
        resaved_file.write(xml.toprettyxml()[23:])
    
def make_edx(config):
  dest_dir = config.book_dir + config.rel_book_output_path
  # Iterate through all of the existing files
  ignore_files = ('Gradebook.html', 'search.html', 'conceptMap.html',
                  'genindex.html', 
                  'RegisterBook.html', 'Bibliography.html')
  html_files = [path for path in os.listdir(dest_dir)
                if path.endswith('.html') and path not in ignore_files]
  exercises = {}
  for path in html_files:
    file_path = os.path.join(dest_dir, path)
    exercises[path] = update_edx_file(file_path, tuple(html_files)+ignore_files)
  
  # Create the directories
  os.mkdir(os.path.join(dest_dir, 'chapter/'))
  os.mkdir(os.path.join(dest_dir, 'sequential/'))
  os.mkdir(os.path.join(dest_dir, 'course/'))
  
  # Create the course.xml toplevel file
  course_file_path = os.path.join(dest_dir, 'course.xml')
  course_xml = Element('course', {'url_name': config.title,
                                   'org': 'VirginiaTech',
                                   'course': config.title})
  pretty_print_xml(course_xml, course_file_path)
  
  top_file_path = os.path.join(dest_dir, 'course', config.title+'.xml')
  top_xml = Element('course', {'advanced_modules': 
                               '["jsav", "module", "content"]',
                               'display_name': config.title,
                               'start': "2015-01-01T00:00:00Z"})
  
  # Index
  book_index = {'Table of Contents': {'next': '', 'prev': ''}}
  previous_name = 'Table of Contents'
  for chapter_name, sections in config.chapters.items():
    for section_name, section_data in sections.items():
      sequential_name = section_name.replace('/', '_')
      book_index[sequential_name] = {
        'prev': previous_name
      }
      book_index[previous_name]['next'] = sequential_name
      previous_name = sequential_name
  book_index[previous_name]['next'] = ""
  
  # Create table-of-contents
  SubElement(top_xml, 'chapter', {'url_name': 'Table_of_Contents'})
  chapter_xml = Element('chapter', {'display_name': 'Table of Contents'})
  SubElement(chapter_xml, 'sequential', {'url_name': 'Table_of_Contents'})
  sequential_xml = Element('sequential', {'display_name': 'Table of Contents'})
  vertical_xml = SubElement(sequential_xml, 'vertical', {'url_name': 'Table_of_Contents_vertical'})
  module_xml = SubElement(vertical_xml, 'module', {'url_name': 'Table_of_Contents_module'})
  SubElement(module_xml, 'content', {
                    'xblock-family': "xblock.v1",
                    'long_name': "OpenDSA Navigation Bar",
                    "content_type": "topnav",
                    "prev_link": book_index['Table of Contents']['prev'],
                    "next_link": book_index['Table of Contents']['next'],
                    "toc_link": 'Table_of_Contents'
                    })
  SubElement(module_xml, 'content', {
                        'short_name': '{}-0'.format('index'),
                        'xblock-family': "xblock.v1",
                        'long_name': "{} OpenDSA Content".format('Table of Contents')
                        })
  pretty_print_xml(sequential_xml, os.path.join(dest_dir, 'sequential', 'Table_of_Contents.xml'))
  pretty_print_xml(chapter_xml, os.path.join(dest_dir, 'chapter', 'Table_of_Contents.xml'))
  
  # Course -> Chapter -> Sequential -> Vertical -> Module -> Exercise
  # Create the chapter files
  for chapter_name, sections in config.chapters.items():
    chapter_file_path = os.path.join(dest_dir, 'chapter', chapter_name+'.xml')
    chapter_xml = Element('chapter', {'display_name': chapter_name})
    SubElement(top_xml, 'chapter', {'url_name': chapter_name})
    # Create the sequential files
    for section_name, section_data in sections.items():
        subsection_name = section_name.split('/')[-1]
        sequential_name = section_name.replace('/', '_')
        sequential_file_path = os.path.join(dest_dir, 'sequential', sequential_name+'.xml')
        SubElement(chapter_xml, 'sequential', {'url_name': sequential_name})
        sequential_xml = Element('sequential', {'display_name': sequential_name})
        vertical_xml = SubElement(sequential_xml, 'vertical', {'url_name': sequential_name+'_vertical'})
        module_xml = SubElement(vertical_xml, 'module', {'url_name': sequential_name+'_module'})
        # Add in each exercise
        SubElement(module_xml, 'content', {
                    'xblock-family': "xblock.v1",
                    'long_name': "OpenDSA Navigation Bar",
                    "content_type": "topnav",
                    "prev_link": book_index[sequential_name]['prev'],
                    "next_link": book_index[sequential_name]['next'],
                    "toc_link": 'toc'
                    })
        SubElement(module_xml, 'content', {
                        'url_name': '{}-0'.format(subsection_name),
                        'xblock-family': "xblock.v1",
                        'long_name': "{} OpenDSA Content".format(section_name)
                        })
        for index, (name, exercise) in enumerate(section_data['exercises'].items(), 1):
            pdata = exercises[subsection_name+'.html'][name]
            params = urlparse.parse_qs(pdata.get('data-frame-src','?').split('?', 1)[1])
            params = {k: v[0] for k, v in params.items()}
            exer_options = exercise.get('exer_options', {})
            SubElement(module_xml, 'jsav',
                       {'url_name': name,
                        'xblock-family': "xblock.v1",
                        'problem_width': pdata.get('data-frame-width', ''),
                        'problem_height': pdata.get('data-frame-height', ''),
                        'threshold': pdata.get('data-threshold', ''),
                        'points': pdata.get('data-points', ''),
                        'required': pdata.get('data-required', ''),
                        'long_name': pdata.get('data-long-name', ""),
                        'display_name': pdata.get('data-long-name', ""),
                        # TODO: where do js_resources come from?
                        'js_resources': pdata.get('js_resources', ""),
                        'problem_url': pdata.get('problem_url', "/AV/"+chapter_name+"/"),
                        'short_name': name,
                        'showhide': pdata.get('data-showhide', ""),
                        # JXOP-debug?
                        'JOP_lang': str(params.get('JOP-lang', "")),
                        'JXOP_feedback': str(params.get('JXOP-feedback', "")),
                        'JXOP_fixmode': str(params.get('JXOP-fixmode', "")),
                        'JXOP_code': str(params.get('JXOP-code', ""))
                        })
            SubElement(module_xml, 'content', {
                        'url_name': '{}-{}'.format(subsection_name, index),
                        'xblock-family': "xblock.v1",
                        'long_name': "{} OpenDSA Content".format(section_name)
                        })
        pretty_print_xml(sequential_xml, sequential_file_path)
    pretty_print_xml(chapter_xml, chapter_file_path)
  pretty_print_xml(top_xml, top_file_path)
    
  mod_name = os.path.join(dest_dir, '..', config.book_name+'.tar.gz')
  with tarfile.open(mod_name, 'w:gz') as tar:
      tar.add(os.path.join(dest_dir, 'course.xml'),
              arcname = '2015S/course.xml')
      for a_directory in ('chapter', 'sequential', 'course'):
          for a_path in os.listdir(os.path.join(dest_dir, a_directory)):
              a_full_path = os.path.join(a_directory, a_path)
              tar.add(os.path.join(dest_dir, a_full_path),
                      arcname=os.path.join('2015S', a_directory, a_path))
  shutil.rmtree(os.path.join(dest_dir, 'chapter/'))
  shutil.rmtree(os.path.join(dest_dir, 'sequential/'))
  shutil.rmtree(os.path.join(dest_dir, 'course/'))
  os.remove(os.path.join(dest_dir, 'course.xml'))
    
def main(argv):
  if len(argv) != 3:
    print "ERROR. Usage: %s <source directory> <destination directory>\n" % argv[0]
    sys.exit(1)

  update_TOC(argv[1], argv[2])


if __name__ == "__main__":
   sys.exit(main(sys.argv))
