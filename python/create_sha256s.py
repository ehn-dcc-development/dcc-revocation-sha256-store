import fileinput
import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='*')
args = parser.parse_args()

for line in fileinput.input(args.input_files    ):
    print(hashlib.sha256(line.strip().encode()).hexdigest().upper())


