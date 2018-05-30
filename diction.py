#!/usr/bin/env python3
import configparser
import argparse
import urllib.request
import json
import os
import collections
import webbrowser


def loadConfig(file):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(file)
    return config


def parseArgs():
    relatedTypes = ["synonym", "antonym", "variant", "equivalent", "cross-reference", "related-word", "rhyme", "form", "etymologically-related-term", "hypernym", "hyponym", "inflected-form", "primary", "same-context", "verb-form", "verb-stem"]
    ap = argparse.ArgumentParser()
    ap.add_argument("word", nargs=1)
    ap.add_argument("-c", "--useCannonical", action="store_true")
    ap.add_argument("-l", "--limit", type=int, nargs="?")
    ap.add_argument("-o", "--options", nargs="?")
    ap.add_argument("-e", "--examples", action="store_true")
    ap.add_argument("-d", "--definitions", action="store_true")
    ap.add_argument("-r", "--relatedWords", choices=relatedTypes, nargs="*")
    ap.add_argument("-p", "--pronunciations", action="store_true")
    ap.add_argument("-hy", "--hyphenation", action="store_true")
    ap.add_argument("-f", "--frequency", type=int, nargs=2) # NOT IMPLEMENTED
    ap.add_argument("-ph", "--phrases", action="store_true")
    ap.add_argument("-et", "--etymologies", action="store_true") # NOT IMPLEMENTED
    ap.add_argument("-a", "--audio", action="store_true") # NOT IMPLEMENTED
    ap.add_argument("-rd", "--reverseDictionary", action="store_true") # NOT IMPLEMENTED
    ap.add_argument("-rw", "--randomWord", action="store_true")
    ap.add_argument("-rws", "--randomWords", action="store_true")
    ap.add_argument("-ww", "--wordwrap", type=int, nargs=1)
    opts = ap.parse_args()
    return vars(opts)


def makeRequest(word, section, options, params):
    base = "https://api.wordnik.com/v4/"
    endpoint = "word.json"
    word += "/"
    if section in ["reverseDictionary", "randomWord", "randomWords"]:
        endpoint = "words.json"
        word = ""
    sectionParams = options.items(section)
    getParams = {k: v for k, v in sectionParams if v != ""}
    if params["limit"] is not None:
        getParams["limit"] = str(params["limit"])
    if params["useCannonical"]:
        getParams["useCannonical"] = "true" if getParams["useCannonical"] == "false" else "false"
    if section == "relatedWords":
        if params["relatedWords"]:
            getParams["relationshipTypes"] = ",".join(params["relatedWords"])
    getParams["api_key"] = options["api"]["apikey"]
    getList = []
    for k, v in getParams.items():
        getList.append("=".join([k, v]))
    getString = "&".join(getList)
    url = "{0}{1}/{2}{3}?{4}".format(base, endpoint, word, section, getString)
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))


def wordwrap(line, length):
    if len(line) < length:
        print(" | " + line)
    else:
        while len(line) > length:
            line = " | " + line
            space = line[0:length].rfind(" ")
            print(line[0:space])
            line = line[space+1:]
        print(" | " + line)


def displayInfo(section, response, length):
    #if section == "examples":
    #    #
    if section == "definitions":
        a = 0
        print("=== Definitions ===\n")
        definitions = {}
        for define in response:
            sd = define["sourceDictionary"]
            if sd not in definitions:
                definitions[sd] = {}
                definitions[sd]["attribution"] = define["attributionText"]
                definitions[sd]["list"] = []
            a+=1
            definitions[sd]["list"].append([define["partOfSpeech"] if "partOfSpeech" in define else "", define["text"] if "text" in define else define["extendedText"]])
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
            wordwrap(", ".join(relation["words"]) + "\n", length)
    if section == "pronunciations":
        print("=== Pronunciations ===\n")
        for phonic in response:
            wordwrap(phonic["rawType"] + ": " + phonic["raw"], length)
    if section == "hyphenation":
        print("=== Hyphenation ===\n")
        final = []
        for hyphen in response:
            final.append(hyphen["text"])
        wordwrap("-".join(final) + "\n", length)
    if section == "phrases":
        print("=== Phrases ===\n")
        for phrase in response:
            wordwrap(phrase["gram1"] + " " + phrase["gram2"] + "\n", length)
    if section == "reverseDictionary":
        print(response)
    if section == "randomWord":
        print("=== Random Word ===\n")
        wordwrap(response["word"] + "\n", length)
    if section == "randomWords":
        print("=== Random Words ===\n")
        for word in response:
            wordwrap(word["word"] + "\n", length)


def main():
    os.chdir(os.path.dirname(__file__))
    arguments = parseArgs()
    filteredArgs = {k: v for k, v in arguments.items() if v is not None and v is not False}
    options = loadConfig(arguments["options"] if "options" in filteredArgs else "diction.ini")
    getParams = list((collections.Counter(filteredArgs.keys()) & collections.Counter(options.sections())).elements())
    length = arguments["wordwrap"][0] if arguments["wordwrap"] is not None else 100
    for section in getParams:
        response = makeRequest(arguments["word"][0], section, options, arguments)
        displayInfo(section, response, length)


if __name__ == "__main__":
    main()
