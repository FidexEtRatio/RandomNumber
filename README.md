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

1. Four pictures of the Sun from SOHO are downloaded, with the following filters applied: HMI171, 0131, 211193171n and 0171. Afterwards, two different arrays are generated from each picture: one with RGB values, selecting a pixel in a pseudo-random way, and one with the Fast Fourier Transform of the picture. That way, we get 8 different arrays, which are concatenated after applying some XOR operations. The final array is being used by selecting every 20 values, generating a single value after applying Bernstein's hash alghoritm, which is therefore used as a base for the actual generation

2. Five seconds are being recorder from two different radio stations around the world, available from the module *pyradio*.