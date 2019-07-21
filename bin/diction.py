#!/usr/bin/env python3
import configparser
import argparse
import urllib.request
import urllib.parse
import json
import os
import collections
import sys
import webbrowser
import codecs
import textwrap


def loadConfig(file):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(file)
    return config


def parseArgs():
    relatedTypes = ["synonym", "antonym", "variant", "equivalent", "cross-reference", "related-word", "rhyme", "form", "etymologically-related-term", "hypernym", "hyponym", "inflected-form", "primary", "same-context", "verb-form", "verb-stem"]
    partsOfSpeech = ["noun", "adjective", "verb", "adverb", "interjection", "pronoun", "preposition", "abbreviation", "affix", "article", "auxiliary-verb", "conjunction", "definite-article", "family-name", "given-name", "idiom", "imperative", "noun-plural", "noun-posessive", "past-participle", "phrasal-prefix", "proper-noun", "proper-noun-plural", "proper-noun-posessive", "suffix", "verb-intransitive", "verb-transitive"]
    ap = argparse.ArgumentParser()
    ap.add_argument("word", nargs="*")
    ap.add_argument("-c", "--useCanonical", action="store_true")
    ap.add_argument("-l", "--limit", type=int, nargs="?")
    ap.add_argument("-ww", "--wordwrap", type=int, nargs=1)
    ap.add_argument("-e", "--examples", action="store_true")
    ap.add_argument("-te", "--topExample", action="store_true")
    ap.add_argument("-d", "--definitions", choices=partsOfSpeech, nargs="*")
    ap.add_argument("-r", "--relatedWords", choices=relatedTypes, nargs="*")
    ap.add_argument("-p", "--pronunciations", action="store_true")
    ap.add_argument("-hy", "--hyphenation", action="store_true")
    ap.add_argument("-f", "--frequency", type=int, nargs="*")
    ap.add_argument("-ph", "--phrases", action="store_true")
    ap.add_argument("-et", "--etymologies", action="store_true")
    ap.add_argument("-a", "--audio", action="store_true")
    ap.add_argument("-rd", "--reverseDictionary", action="store_true")
    ap.add_argument("-rw", "--randomWord", action="store_true")
    ap.add_argument("-rws", "--randomWords", action="store_true")
    ap.add_argument("-s", "--scrabbleScore", action="store_true")
    opts = ap.parse_args()
    return vars(opts)


def getGetString(section, options, arguments):
    sectionParams = options.items(section)
    getParams = {k: v for k, v in sectionParams if v != ""}
    if arguments["limit"] is not None:
        getParams["limit"] = str(arguments["limit"])
    if arguments["useCanonical"]:
        getParams["useCanonical"] = "true" if getParams["useCanonical"] == "false" else "false"
    if section == "relatedWords":
        if arguments["relatedWords"]:
            getParams["relationshipTypes"] = ",".join(arguments["relatedWords"])
    if section == "definitions":
        if arguments["definitions"]:
            getParams["partOfSpeech"] = ",".join(arguments["definitions"])
    if section == "reverseDictionary":
        getParams["query"] = arguments["query"]
    if section == "frequency":
        getParams["startYear"] = arguments["frequency"][0] if 0 in range(len(arguments["frequency"])) else getParams["startYear"]
        getParams["endYear"] = arguments["frequency"][1] if 1 in range(len(arguments["frequency"])) else getParams["endYear"]
    getParams["api_key"] = options["api"]["apikey"]
    return urllib.parse.urlencode(getParams)


def makeRequest(word, section, options, arguments):
    base = "https://api.wordnik.com/v4/"
    endpoint = "word.json"
    if section == "reverseDictionary":
        arguments["query"] = word
    word += "/"
    if section in ["reverseDictionary", "randomWord", "randomWords"]:
        endpoint = "words.json"
        word = ""
    getString = getGetString(section, options, arguments)
    url = f"{base}{endpoint}/{word}{section}?{getString}"
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))


def wordwrap(line, length):
    lines = textwrap.wrap(line, width=length - 3)
    for line in lines:
        print(" | " + line)


def displayInfo(section, response, length):
    if section == "examples":
        print("=== Examples ===\n")
        for example in response["examples"]:
            if "title" in example:
                wordwrap(example["title"] + ":", length)
            wordwrap(example["text"], length)
            print(" | ")
            wordwrap(example["url"], length)
            print("")
    if section == "topExample":
        print("=== Top Example ===\n")
        if "title" in response:
            wordwrap(response["title"] + ":", length)
        wordwrap(response["text"], length)
        print(" | ")
        wordwrap(response["url"], length)
        print("")
    if section == "definitions":
        print("=== Definitions ===\n")
        definitions = {}
        for define in response:
            sd = define["sourceDictionary"]
            if sd not in definitions:
                definitions[sd] = {}
                definitions[sd]["attribution"] = define["attributionText"]
                definitions[sd]["list"] = []
            definitions[sd]["list"].append([define["partOfSpeech"] if "partOfSpeech" in define else "", define["text"] if "text" in define else define["extendedText"] if "extendedText" in define else ""])
        for dictionary in definitions:
            for entry in definitions[dictionary]["list"]:
                index = str(definitions[dictionary]["list"].index(entry) + 1) + ". "
                partOfSpeech = entry[0] + ". " if entry[0] != "" else ""
                definition = entry[1]
                wordwrap(index + partOfSpeech + definition, length)
            print(" | \n | " + definitions[dictionary]["attribution"] + "\n")
    if section == "relatedWords":
        print("=== Related Words ===\n")
        for relation in response:
            print(" | " + relation["relationshipType"] + ":")
            wordwrap(", ".join(relation["words"]), length)
            print("")
    if section == "pronunciations":
        print("=== Pronunciations ===\n")
        for phonic in response:
            wordwrap(phonic["rawType"] + ": " + phonic["raw"], length)
            print("")
    if section == "hyphenation":
        print("=== Hyphenation ===\n")
        final = []
        for hyphen in response:
            final.append(hyphen["text"])
        wordwrap("-".join(final), length)
        print("")
    if section == "phrases":
        print("=== Phrases ===\n")
        for phrase in response:
            wordwrap(phrase["gram1"] + " " + phrase["gram2"], length)
            print("")
    if section == "etymologies":
        print("=== Etymologies ===\n")
        for ety in response:
            wordwrap(ety, length)
            print("")
    if section == "reverseDictionary":
        print("=== Reverse Dictionary ===\n")
        wordList = {}
        for item in response["results"]:
            word = item["word"]
            sd = item["sourceDictionary"]
            if word not in wordList:
                wordList[word] = {}
            if sd not in wordList[word]:
                wordList[word][sd] = {}
                wordList[word][sd]["attribution"] = item["attributionText"]
                wordList[word][sd]["list"] = []
            wordList[word][sd]["list"].append([item["partOfSpeech"] if "partOfSpeech" in item else "", item["text"] if "text" in item else item["extendedText"] if "extendedText" in item else ""])
        for word in wordList:
            word_encoded = urllib.parse.quote(word)
            wordwrap(f"=== {word} | https://www.wordnik.com/words/{word_encoded} ===", length)
            print("")
            for dictionary in wordList[word]:
                for entry in wordList[word][dictionary]["list"]:
                    index = str(wordList[word][dictionary]["list"].index(entry) + 1) + ". "
                    partOfSpeech = entry[0] + ". " if entry[0] != "" else ""
                    definition = entry[1]
                    wordwrap(index + partOfSpeech + definition, length)
                print(" | \n | " + wordList[word][dictionary]["attribution"] + "\n")
    if section == "randomWord":
        print("=== Random Word ===\n")
        wordwrap(response["word"], length)
        print("")
    if section == "randomWords":
        print("=== Random Words ===\n")
        for word in response:
            wordwrap(word["word"], length)
            print("")
    if section == "scrabbleScore":
        print("=== Scrabble Score ===\n")
        wordwrap(str(response["value"]), length)
        print("")


def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    arguments = parseArgs()
    filteredArgs = {k: v for k, v in arguments.items() if v is not None and v is not False}
    cfgPath = os.path.expanduser("~/diction.ini")
    if not os.path.isfile(os.path.expanduser(cfgPath)):
        urllib.request.urlretrieve("https://raw.githubusercontent.com/Rayquaza01/diction/master/diction.ini", cfgPath)
        print("Downloaded config to ~/diction.ini. Please add your API key!")
        exit()
    options = loadConfig(os.path.expanduser(cfgPath))
    getParams = list((collections.Counter(filteredArgs.keys()) & collections.Counter(options.sections())).elements())
    length = arguments["wordwrap"][0] if arguments["wordwrap"] is not None else int(options["api"]["wordwrap"])
    words = arguments["word"] if arguments["word"] is not None else [""]
    for word in words:
        word_encoded = urllib.parse.quote(word)
        print(f"=== {word} | https://www.wordnik.com/words/{word_encoded} ===")
        for section in getParams:
            if section not in ["audio", "frequency"]:
                response = makeRequest(word_encoded, section, options, arguments)
                displayInfo(section, response, length)
            else:
                webbrowser.open(f"https://rayquaza01.github.io/diction/?word={word_encoded}&section={section}&{getGetString(section, options, arguments)}")
    print("=== Powered by Wordnik | https://wordnik.com ===")


if __name__ == "__main__":
    main()
