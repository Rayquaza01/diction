#!/usr/bin/env python3
import configparser
import argparse
import urllib.request
import json
import os
os.chdir(os.path.dirname(__file__))
base = "https://api.wordnik.com/v4/"
relatedTypes = ["", "synonym", "antonym", "variant", "equivalent", "cross-reference", "related-word", "rhyme", "form", "etymologically-related-term", "hypernym", "hyponym", "inflected-form", "primary", "same-context", "verb-form", "verb-stem"]
argumentList = {}


def loadConfig(file):
    config = configparser.ConfigParser()
    config.read(file)
    argumentList["apikey"] = config["api"]["apikey"]


def parseArgs():
    ap = argparse.ArgumentParser()
    ap.addArgument("word", nargs="+")
    ap.addArgument("-d", "--definitions", action="store_true", nargs="?")
    ap.addArgument("-r", "--relatedWords", choices=relatedTypes)
