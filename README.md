# Diction
A wordnik commandline client

![Example](https://i.imgur.com/1tx0CbB.gif)

Diction is a python script that acts as a wrapper for Wordnik's [API](https://developer.wordnik.com)  
Best when piped into `less`, because outputs can be pretty long

## Getting Started
 * Download `diction.py` and `diction.ini` and put them somewhere on your computer
   * A zip of the current version is available [here](https://github.com/Rayquaza01/diction/archive/master.zip), or you could run `git clone https://github.com/Rayquaza01/diction` if that's more your style.
 * You may want to add the folder they're in to your [path](https://en.wikipedia.org/wiki/PATH_(variable)) so you can run it from anywhere
   * On windows, you can run `[Environment]::SetEnvironmentVariable( "Path", $env:Path + ";" + (Get-Location).path, [System.EnvironmentVariableTarget]::Machine )` in an Administrator PowerShell to add the current folder to the path.
 * Add your API key to `diction.ini` under the `[api]` header. (You can get an API key at https://developer.wordnik.com)

## Arguments
### word
The word(s) used when calling the API. Multiple words can be entered, separated by spaces.  
This is a positional argument, and must come before all other arguments.  
Ex: `diction.py word example ...`
### useCannonical
Whether to use the canonical version of the word (e.g. cats -> cat)  
This argument overrides the configuration set in `diction.ini`. Each section has its own `useCannonical` option, defaulting to `false`.  
Used as `-c` or `--useCannonical`
Ex: `diction.py words -c ...`
### limit
The amount of results to return per section. Accepts one number as an argument.  
This argument overrides the configuration set in `diction.ini`. Each section has its own `limit` option, with different defaults for each section.  
Used as `-l` or `--limit`
Ex: `diction.py word -l 20 ...`
### wordwrap
The maximum amount of characters to display on a single line. Accepts one number as an argument.
This argument overrides the configuration set in `diction.ini`. The `api` section has a `wordwrap` option, defaulting to `100`.  
Setting the value to `-1` disables wordwrapping.  
Used as `-ww` or `--wordwrap`  
Ex: `diction.py word -ww 80 ...`
### examples
Whether or not to return examples of the word.  
Used as `-e` or `--examples`  
Ex: `diction.py word -e ...`
### topExample
Same as examples, but only returns the first example.  
Used as `-te` or `--topExample`
Ex: `diction.py word -te ...`
### definitions
### relatedWords
### pronunciations
### hyphenation
### frequency
### phrases
### etymologies
### audio
### reverseDictionary
### randomWord
### randomWords
### scrabbleScore
