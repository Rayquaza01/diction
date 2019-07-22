# Diction
A wordnik commandline client

![Example](https://i.imgur.com/1tx0CbB.gif)

Diction is a python script that acts as a wrapper for Wordnik's [API](https://developer.wordnik.com)  
Best when piped into `less`, because outputs can be pretty long

## Getting Started
 * Run `pip3 install git+https://github.com/Rayquaza01/diction` or `pip3 install diction`
 * Run `diction.py` to download a sample config file to `~/diction.ini`
 * Add your API key to the config file

## Arguments
Multiple arguments can be sent at a time. `diction.py word example -d -r` returns definitions and related words for both "word" and "example".

### word
The word(s) used when calling the API. Multiple words can be entered, separated by spaces.  
This is a positional argument, and must come before all other arguments.  
Ex: `diction.py word example ...`

### useCanonical
Use the canonical version of the word (e.g. cats -> cat)  
This argument overrides the configuration set in `diction.ini`. Each section has its own `useCanonical` option, defaulting to `false`.  
Used as `-c` or `--useCanonical`

### limit
The amount of results to return per section. Accepts one number as an argument.  
This argument overrides the configuration set in `diction.ini`. Each section has its own `limit` option, with different defaults for each section.  
Used as `-l` or `--limit`  
Ex: `diction.py word -l 20 ...`

### wordwrap
The maximum amount of characters to display on a single line. Accepts one number as an argument.  
This argument overrides the configuration set in `diction.ini`. The `api` section has a `wordwrap` option, defaulting to `80`.  
Setting the value to `-1` disables wordwrapping.  
Used as `-ww` or `--wordwrap`  
Ex: `diction.py word -ww 100 ...`

### examples
Whether to return examples of the word.  
Used as `-e` or `--examples`

### topExample
Same as examples, but only returns the first example.  
Used as `-te` or `--topExample`

### definitions
Whether to return definitions. Accepts parts of speech as arguments, space separated. See `reference.md`  
Used as `-d` or `--definitions`  
Ex: `diction.py word -d noun verb ...`  
Ex: `diction.py word -d ...`

### relatedWords
Whether to return related words. Accepts related types as arguments, space separated. See `reference.md`  
Used as `-r` or `--relatedWords`  
Ex: `diction.py word -r synonym antonym ...`

### pronunciations
Whether to return pronunciation of the word.  
Used as `-p` or `--pronunciations`

### hyphenation
Whether to return hyphenation of the word.  
Used as `-hy` or `--hyphenation`

### frequency
Whether to open a webpage with a graph of the word's frequency. Takes a start year and an end year as arguments, or defaults to the years specified in the config.  [Chart.js](https://www.chartjs.org) is used to make the graph.  
Used as `-f` or `--frequency`  
Ex: `diction.py -f 1800 2012 ...`

### phrases
Whether to return two word phrases containing the word.  
Used as `-ph` or `--phrases`

### etymologies
Whether to return the etymologies of the word.  
Used as `-et` or `--etymologies`

### audio
Whether to open a webpage with audio files of pronunciations.  
Used as `-a` or `--audio`

### randomWord
Whether to return a random word. The word argument has no affect on this.
Used as `-rw` or `--randomWord`

### randomWords
Same as randomWord, but with more than one word. The word argument has no affect on this.  
Used as `-rws` or `--randomWords`

### scrabbleScore
Whether to return the word's scrabble score.  
Used as `-s` or `--scrabbleScore`

# Acknowledgements
Built using Python 3  
Uses [Chart.js](https://www.chartjs.org) for frequency graph (MIT)  
[![Powered by Wordnik](https://www.wordnik.com/img/wordnik_badge_a1.png)](https://wordnik.com)
