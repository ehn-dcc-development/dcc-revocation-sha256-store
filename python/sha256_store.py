import argparse
import fileinput
import bisect

def create_store(sha_values: list[str], d: int) -> list[bytearray]:
    nchars, remainder = divmod(d, 8)
    nchars *= 2 # it's hex encoded, so two chars per byte
    if remainder != 0:
        raise Exception(f"{d} is not a multiple of 8.")
    store = []
    for s in sha_values:
        store.append(bytes.fromhex(s[:nchars]))
    store = sorted(store)
    if len(store) != len(set(store)):
        raise Exception("Collisions found.")
    return store

def find_in_store(store: list[bytearray], value: str, d: int):
    nchars = d // 4 # it's hex encoded, so two chars per byte
    lookup_value = value[:nchars]
    blookup_value = bytes.fromhex(lookup_value)
    i = bisect.bisect_left(store, blookup_value)
    if i != len(store) and store[i] == blookup_value:
        return True
    else:
        return False


parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='*')
args = parser.parse_args()

# Read in a file of SHA-256 hashes and put them into storage.
sha_values = []
for line in fileinput.input(args.input_files):
    sha_values.append(line.strip())

store = create_store(sha_values, 32)

# Test storage:
#   * All SHA-256 that have been input should be found there.
#   * SHA-256 values that have not been input should not be found.
#     We test with an equal number of retrievals and misses
num_found = 0
num_misses = 0
for sha_value in sha_values:
    found = find_in_store(store, sha_value, 32)
    if found:
        num_found += 1
    else:
        print(sha_value)
    miss_sha_value = sha_value
    while miss_sha_value in sha_values:
        miss_sha_value = miss_sha_value[-1] + miss_sha_value[:-1]
    found = find_in_store(store, miss_sha_value, 32)
    if found:
        num_misses += 1
print(num_found, num_misses, len(sha_values))
