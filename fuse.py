"""
'fuse.py' drives concept queries and novel relation discovery.

  USAGE: python3 fuse.py
"""

from settings  import LANGUAGE
from operator  import itemgetter
from warnings  import filterwarnings
from wordfreq  import word_frequency as known_freq
from utils     import get_word_freqs, get_concept_page, get_connection_section_freqs,\
                      connection_result_output

MINIMUM_FREQ = 1e-6  # Lower bound on minimum frequency output by 'known_freq'

# Runs fuse
def main():
  # Prompt user for concept and get corresponding Wikipedia page
  concept1, concept1_page = get_concept_page(1)
  concept2, concept2_page = get_concept_page(2)

  # Get word frequencies of each concept's Wikipedia page content
  concept1_word_freqs = get_word_freqs(concept1_page.content)
  concept2_word_freqs = get_word_freqs(concept2_page.content)

  # Compute dot product of word frequency vectors
  dot_prod = 0
  components = {}  # Track each word's contribution to dot product
  for word in concept1_word_freqs:
    if word in concept2_word_freqs:
      norm = known_freq(word, LANGUAGE, minimum=MINIMUM_FREQ)
      components[word] = concept1_word_freqs[word] * concept2_word_freqs[word] / norm
      dot_prod += components[word]

  # Sort components by decreasing normalized frequency
  sorted_words = sorted(components.items(), key=itemgetter(1))[::-1]

  # Get frequency of 'connection' in each section for each concept's Wikipedia page
  connection = sorted_words[0][0]  # Word with strongest relation betw. two pages
  concept1_section_freqs = get_connection_section_freqs(connection, concept1_page)
  concept2_section_freqs = get_connection_section_freqs(connection, concept2_page)

  # Get section titles of section with maximum frequency of connection word
  concept1_section = max(concept1_section_freqs.items(), key=itemgetter(1))[0]
  concept2_section = max(concept2_section_freqs.items(), key=itemgetter(1))[0]

  # Print results of concept relation discovery
  print(connection_result_output(concept1, concept1_section,
                                 concept2, concept2_section, connection))

if __name__ == '__main__':
  filterwarnings("ignore")  # Filters Beautiful Soup warnings
  main()
