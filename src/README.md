# Pylibmassfiles

A library and a standalone converter for converting mass spectrometry library files.

Currently the formats supported are:

Input:
 * mgf : Masscot
 
Output:
 * mat : Enhanced NIST-inspired format used by MSFINDER
 
## Usage of the standalone converter

To convert a series of mgf files inside a single mat file:

$ python ./converter.py -o output.mat file1.mgf file2.mgf…

Or to stdout

$ python ./converter.py file1.mgf file2.mgf…

