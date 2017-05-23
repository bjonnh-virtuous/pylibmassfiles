This is a python library and support scripts that allow manual and automated conversion of mass spectrometry databases/libraries formats.

It has been created to convert MGF libraries to MAT (and maybe it will just do that if nobody wants to continue working on it).


* File formats to manage
- [ ] Table format (TXT)
- [ ] NIST MS format (MSP)
- [ ] MAT format (improved from MSP)
- [ ] Massbank format (TXT)
- [ ] Mascot format (MGF)
- [ ] CFM-ID output
* MSP Description
"""
BLOCK1
<newline>
BLOCK2
…
"""

Block structure:
"""
NAME:
PRECURSORMZ:
PRECURSORTYPE:
IONMODE: Positive or Negative
Num Peaks: x (where x is number of peaks)
mz intensity pairs (tab, comma or space delimited)
"""

Other possible fields:
INSTRUMENTTYPE:
INSTRUMENT:
SMILES:
INCHIKEY:
COLLISIONENERGY:
FORMULA:
RETENTIONTIME:
SPECTRUMTYPE: (ex Centroid)
Comment

* MAT format
allows to put both MS1 and MS2 in the DB
adds the required parameter "MSTYPE:" 
that should be MS1 and MS2 

MS1 and MS2 have to follow each other.
example

"""
NAME:…
…
MSTYPE: MS1
Num Peaks: 2
123 456
789 410
MSTYPE: MS2
Num Peaks: 2
60 41
123 456
"""


« If you want to perform the MS/MS peak annotation with the known structure,
prepare two fields including FORMULA and SMILES. The formula and SMILES of the
neutralized structure should be made.» (source:
http://prime.psc.riken.jp/Metabolomics_Software/MS-FINDER/MSFINDER-Tutorial-VS2.pdf)

