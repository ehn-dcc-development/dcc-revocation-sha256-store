import base64
from stdnum import luhn
import os
import argparse

URN = "URN"
UVCI = "UVCI"
VERSION = "01"
ISSUER = "GR"
SEP = ":"
CHECKSUM_SEP = "#"
CHECKSUM_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:"

def compute_checksum_char(payload: str, alphabet: str) -> str:
    for char in alphabet:
        s = payload + char
        if luhn.checksum(s, alphabet=alphabet) == 0:
            return char
    raise Exception("checksum_computation_failed")

def create_uvci() -> str:
    # https://ec.europa.eu/health/sites/default/files/ehealth/docs/vaccination-proof_interoperability-guidelines_en.pdf
    # Annex 2, Option 2
    s = os.urandom(16)
    unique_ident = base64.b32encode(s).rstrip(b'=').decode("utf-8")
    unchecked_ident = (
        URN + SEP + UVCI + SEP + VERSION + SEP + ISSUER + SEP + unique_ident
    )
    checksum_char = compute_checksum_char(unchecked_ident, CHECKSUM_ALPHABET)
    return unchecked_ident + CHECKSUM_SEP + checksum_char

parser = argparse.ArgumentParser()

parser.add_argument("n", help="number of UVCIs to generate", type=int)
args = parser.parse_args()

for i in range(args.n):
    uvci = create_uvci()
    print(uvci)