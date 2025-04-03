# Implementation of a True Random Number Generator (TRNG)
## Overview
The purpose of this project is to write an implementation of a TRNG, using sources of natural origin, _id est_ pictures of the Sun from the Solar and Heliospheric Observatory (SOHO), and radio feeds from around the world.
## Features
- Uses real-world entropy sources
- Supports random *Raw Data* generation
## Entropy sources
- Images of the Sun captured by SOHO in different spectral filters
- Radio channel data from different radios around the world
## Algorithm
The algorithm uses two main seeds and a secondary one to generate random raw data.

1. Four pictures of the Sun from SOHO are downloaded, with the following filters applied: HMI171, 0131, 211193171n and 0171. Afterwards, two different arrays are generated from each picture: one with RGB values, selecting a pixel in a pseudo-random way, and one with the Fast Fourier Transform of the picture. That way, we get 8 different arrays, which are concatenated after applying some XOR operations. The final array is being used by selecting every 20 values, generating a single value after applying Bernstein's hash alghoritm, which is therefore used as a base for the actual generation. The base data is being updated every 20 minutes, as SOHO uploads new pictures approximately every 15 minutes.

2. Five seconds are being recorder from two different radio stations around the world, available from the module *pyradio*. The values extracted from each radio are concatenated. The following proccess is similar with the one used to select values from the Sun data, but every 50 values are selected. The data is being updated after every 50-value sub-string has been exhausted from the array.

3. A hardware seed is being used for both the generation alghoritm and for specific pseudo-random values, *exempli gratia* choosing an index for a specific radio station. This value is being generated in real-time, as it is needed along the way.

For each call of the *generate()* function, both a value from the first source and one from the second one are provided, following the 20-value hash and 50-value hash proccess explained above. Then four rounds of hashing, using the *SHA3 512* hashing alghoritm. After the first round, each resulting string is being converted into an integer and is XOR-ed with the previous result. The final result is being masked to fit in a formerly set interval and it consists of a random raw data value.

## Contributions
The authors would like to give thanks to Iulian Aciobăniței, Phd. Without the proffessor's guidance, this project would have been dead.

## Authors
- Codreanu Andrei-Daniel
- Ivan Florentin-Marian