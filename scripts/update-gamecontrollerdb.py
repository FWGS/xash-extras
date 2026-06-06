#!/usr/bin/env python3
# encoding: utf-8

import os
import urllib.request

GCDB_URL = "https://raw.githubusercontent.com/mdqinc/SDL_GameControllerDB/master/gamecontrollerdb.txt"
DEST = "gamecontrollerdb.txt"

def fetch(url):
	with urllib.request.urlopen(url, timeout=30) as resp:
		if resp.status != 200:
			raise RuntimeError(f"GET {url} returned {resp.status}")
		return resp.read()

def main():
	repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	dest = os.path.join(repo_root, DEST)

	print(f"fetching {GCDB_URL}")
	data = fetch(GCDB_URL)

	with open(dest, "wb") as f:
		f.write(data)
	print(f"wrote {len(data)} bytes to {dest}")
	print("commit the change in xash-extras and bump the submodule in the engine repo.")

if __name__ == "__main__":
	main()
