"""
'utils.py' implements utility methods for the fuse program.
"""

from wikipedia            import page
from string               import punctuation
from settings             import LANGUAGE, Color
from wikipedia.exceptions import DisambiguationError
from wordfreq             import word_frequency as known_freq

COMMON_WORD_FREQ = 0.001  # Lower bound on known frequency to determine if word is common

ENTER_CONCEPT_MSG = '{}Enter Concept {} : {}'

DISAMBIGUATION_ERROR_MSG = \
  '{}{} is too ambiguous. Please choose from one of the following options...{}'

CONNECTION_RESULT_MSG = """
Concept {}"{}"{} and Concept {}"{}"{} connected by Concept {}"{}"{} because:

\t{}"{}"{} related to {}"{}"{} related to {}"{}"{}.
\t{}"{}"{} related to {}"{}"{} related to {}"{}"{}."""

# Returns string cleaned of punctuation/digits
#   @params
#     text <str> : text
#   @return
#     <str> lowercase string w/o punctuation or digits
def clean(text):
  return ''.join(c.lower() for c in text if c not in punctuation and not c.isdigit())

# Returns dictionary of word frequencies in text
#   @params
#     text <str>  : text
#   @return
#     <{str:inti,}> map of word to frequency in text
def get_word_freqs(text):
  words = clean(text.replace('\n', ' ')).split(' ')
  freqs = {}
  for word in words:
    if not word or len(word) < 3 or known_freq(word, LANGUAGE) > COMMON_WORD_FREQ:
      continue
    if word in freqs:
      freqs[word] += 1
    else:
      freqs[word] = 1
  return {w : f / float(len(freqs)) for w,f in freqs.items()}

# Prompts user for concept, returns user-supplied concept and concept's Wikipedia page
#   @params
#     i <int> : number of concept being requsted from user
#   @return
#     (<str>, <WikipediaPage>) tuple containing user-supplied concept
#     and corresponding WikipediaPage object
def get_concept_page(i):
  is_valid = False
  while not is_valid:
    concept = input(ENTER_CONCEPT_MSG.format(Color.OKBLUE, i, Color.ENDC))
    try:
      concept_page = page(concept)
      is_valid = True
    except DisambiguationError as e:
      print(DISAMBIGUATION_ERROR_MSG.format(Color.WARNING, concept, Color.ENDC))
      print('\n'.join(['\t{}'.format(option) for option in e.options]))
  return (concept, concept_page)

# Returns frequency of connection word in each section of concept's page
#   @params
#     connection   <str>           : word to count frequency of in each section
#                                    of concept's page
#     concept_page <WikipediaPage> : wikipedia page of corresponding concept
#   @return
#     <{str:int,}> map of section titles to frequnecy of connection word in section
#     with given title
def get_connection_section_freqs(connection, concept_page):
  concept_section_freqs = {title : 0 for title in concept_page.sections}
  for title in concept_page.sections:
    if concept_page.section(title) and connection in concept_page.section(title):
      concept_section_freqs[title] \
        += get_word_freqs(concept_page.section(title))[connection]
  return concept_section_freqs

# Returns string formatted with result of relation discovery
#   @params
#     concept1         <str> : first concept
#     concept1_section <str> : first concept section title
#     concept2         <str> : second concept
#     concept2_section <str> : second concept section title
#     connnection      <str> : connecting concept
#   @return
#     <str> formatted string with result of relation discovery
def connection_result_output(concept1, concept1_section, \
                             concept2, concept2_section, connection):
  return CONNECTION_RESULT_MSG.format(Color.OKGREEN, concept1, Color.ENDC, \
                                      Color.OKGREEN, concept2, Color.ENDC, \
                                      Color.WARNING, connection, Color.ENDC, \
                                      Color.WARNING, connection, Color.ENDC, \
                                      Color.HEADER, concept1_section, Color.ENDC, \
                                      Color.OKGREEN, concept1, Color.ENDC, \
                                      Color.WARNING, connection, Color.ENDC, \
                                      Color.HEADER, concept2_section, Color.ENDC, \
                                      Color.OKGREEN, concept2, Color.ENDC)
