# DCC revocation storage based on SHA256 bits

Implementation of storage scheme for DCC revocation lists. The scheme
was suggested by [Sevastiano Vigna](https://vigna.di.unimi.it/) as
more efficient solution, in terms of space, than Bloom filters.

The idea is to use `d` bits from the SHA-256 representation of the DCC
to be revoked. Bloom filters need 1.44d bits per element to achieve 
precision 2^-d. If we store the lower bits of the SHAs in sorted
order, we get:

1. Logarithmic-time check (by binary search).
2. Precision 2^-d using d bits per SHA (33% less space than Bloom filters).
3. If updates are needed, they can be done by sending d-bits codes to
   delete  and codes to add, which cannot be done with Bloom filters
   (so there is no need to send the entire filter again).

The implementation is trivial. Most of the committed code is test
scaffolding.

* `create_uvcis.py` creates a set of random UVCIs (IDs of certificates
  to be revoked).

* `create_sha256s.py` creates the corresponding SHA-256 values. 

* `sha256_store.py` takes SHA-256 values, enters them into storage and
  then checks that:
    * all the entered values are indeed in storage
    * other values are not

The code has been tested for 10,000 revocations, using 32 bits from
each SHA-256 value.