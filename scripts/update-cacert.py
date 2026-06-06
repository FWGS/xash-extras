#!/usr/bin/env python3
# encoding: utf-8

import hashlib
import os
import sys
import urllib.request

CACERT_URL = "https://curl.se/ca/cacert.pem"
CACERT_SHA256_URL = "https://curl.se/ca/cacert.pem.sha256"
DEST = "cacert.pem"

def fetch(url):
	with urllib.request.urlopen(url, timeout=30) as resp:
		if resp.status != 200:
			raise RuntimeError(f"GET {url} returned {resp.status}")
		return resp.read()

def main():
	repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	dest = os.path.join(repo_root, DEST)

	print(f"fetching {CACERT_URL}")
	pem = fetch(CACERT_URL)

	print(f"fetching {CACERT_SHA256_URL}")
	sha_line = fetch(CACERT_SHA256_URL).decode("ascii").strip()
	# format is "<hex>  cacert.pem"
	expected = sha_line.split()[0].lower()

	actual = hashlib.sha256(pem).hexdigest().lower()
	if actual != expected:
		print(f"SHA-256 mismatch! expected {expected}, got {actual}", file=sys.stderr)
		sys.exit(1)
	print(f"SHA-256 OK: {actual}")

	with open(dest, "wb") as f:
		f.write(pem)
	print(f"wrote {len(pem)} bytes to {dest}")
	print("commit the change in xash-extras and bump the submodule in the engine repo.")

if __name__ == "__main__":
	main()
