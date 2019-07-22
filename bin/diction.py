#!/usr/bin/env python3
import configparser
import argparse
import urllib.request
import urllib.parse
import json
import os
import sys
import webbrowser
import textwrap
# fix output on windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def loadConfig(file):
    config = configparser.ConfigParser()
    # keep case sensitivity
    config.optionxform = str
    config.read(file)
    return config


def parseArgs():
    # types of related words, for -r arg
    relatedTypes = ["synonym", "antonym", "variant", "equivalent", "cross-reference", "related-word", "rhyme", "form", "etymologically-related-term", "hypernym", "hyponym", "inflected-form", "primary", "same-context", "verb-form", "verb-stem"]
    # parts of speech, for -d arg
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
    ap.add_argument("-rw", "--randomWord", action="store_true")
    ap.add_argument("-rws", "--randomWords", action="store_true")
    ap.add_argument("-s", "--scrabbleScore", action="store_true")
    opts = ap.parse_args()
    return vars(opts)


def getGetString(section, options, arguments):
    # section is the API endpoint
    # options is the config file
    # arguments is the command line args

    # creates the query params to pass to the API
    sectionParams = options.items(section)
    getParams = {k: v for k, v in sectionParams if v != ""}
    # fall back to config file if option not provided as cmd argument
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
    if section == "frequency":
        getParams["startYear"] = arguments["frequency"][0] if 0 in range(len(arguments["frequency"])) else getParams["startYear"]
        getParams["endYear"] = arguments["frequency"][1] if 1 in range(len(arguments["frequency"])) else getParams["endYear"]
    getParams["api_key"] = options["api"]["apikey"]
    return urllib.parse.urlencode(getParams)


def makeRequest(word, section, options, arguments):
    # make the request to the API
    base = "https://api.wordnik.com/v4/"
    endpoint = "word.json"
    word += "/"
    # change endpoint for rd, rw, and rws
    if section in ["randomWord", "randomWords"]:
        endpoint = "words.json"
        word = ""
    getString = getGetString(section, options, arguments)
    url = f"{base}{endpoint}/{word}{section}?{getString}"
    # return response parsed as json
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))


def wordwrap(line, length):
    # print without exceeding a set amount of chars (usually 80)
    lines = textwrap.wrap(line, width=length - 3)
    for line in lines:
        print(" | " + line)


def displayInfo(section, response, length):
    # display the actual response
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
        # sort definitions by source dictionary
        # this is so that definitions from the same dictionary appear together
        for define in response:
            # skip items without a definition
            if "text" not in define or define["text"] == "":
                if "extendedText" not in define or define["extendedText"] == "":
                    continue
                else:
                    text = define["extendedText"]
            else:
                text = define["text"]


            sd = define["sourceDictionary"]
            # put attribution text with dictionaries
            if sd not in definitions:
                definitions[sd] = {
                    "attribution": define["attributionText"],
                    "list": []
                }
            # add part of speech and definition to definition list
            definitions[sd]["list"].append([
                define["partOfSpeech"] if "partOfSpeech" in define else "",
                text
            ])
        # print definitions
        for dictionary in definitions:
            for entry in definitions[dictionary]["list"]:
                index = str(definitions[dictionary]["list"].index(entry) + 1) + ". "
                # display part of speech if exists
                partOfSpeech = entry[0] + ". " if entry[0] != "" else ""
                definition = entry[1]
                wordwrap(index + partOfSpeech + definition, length)
            # display dictionary attribution
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
    arguments = parseArgs()
    filteredArgs = {k: v for k, v in arguments.items() if v is not None and v is not False}
    cfgPath = os.path.expanduser("~/diction.ini")
    # download sample config file to ~/diction.ini if it doesn't exist
    if not os.path.isfile(cfgPath):
        urllib.request.urlretrieve("https://raw.githubusercontent.com/Rayquaza01/diction/master/diction.ini", cfgPath)
        print("Downloaded config to ~/diction.ini. Please add your API key!")
        exit()
    options = loadConfig(cfgPath)

    # filter to get only params that are both in the config file and the command line args
    getParams = []
    for sec in options.sections():
        if sec in filteredArgs.keys():
            getParams.append(sec)

    # fall back to opts if wordwrap is not in args
    length = arguments["wordwrap"][0] if arguments["wordwrap"] is not None else int(options["api"]["wordwrap"])
    words = arguments["word"]
    # use a default word if no word is given.
    if len(words) == 0:
        words = ["diction"]
    for word in words:
        word_encoded = urllib.parse.quote(word)
        print(f"=== {word} | https://www.wordnik.com/words/{word_encoded} ===")
        for section in getParams:
            if section not in ["audio", "frequency"]:
                # make web request and display response
                response = makeRequest(word_encoded, section, options, arguments)
                displayInfo(section, response, length)
            else:
                # open a web page if displaying audio or frequency
                webbrowser.open(f"https://rayquaza01.github.io/diction/?word={word_encoded}&section={section}&{getGetString(section, options, arguments)}")
    print("=== Powered by Wordnik | https://wordnik.com ===")


if __name__ == "__main__":
    main()
