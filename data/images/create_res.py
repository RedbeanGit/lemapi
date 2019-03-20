#!/usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = "Julien Dubois"
__version__ = "0.1.0"

import glob
import json


def main():
	filenames = []
	for filename in glob.iglob('./**/*.png', recursive=True):
		filename = filename.split("/")
		filenames.append(filename[1:])

	with open("resources.json", "w") as file:
		file.write(json.dumps(filenames))


if __name__ == "__main__":
	main()