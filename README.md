This is a python library and support scripts that allow manual and automated conversion of mass spectrometry databases/libraries formats.

It has been created to convert MGF libraries to MAT (and maybe it will just do that if nobody wants to continue working on it).


* File formats to manage
- [ ] Table format (TXT)
- [ ] NIST MS format (MSP)
- [ ] MAT format (improved from MSP)
- [ ] Massbank format (TXT)
- [ ] Mascot format (MGF)
- [ ] CFM-ID output

## Usage of the standalone converter

To convert a series of mgf files inside a single mat file:

    $ cd src
    $ python ./converter.py -o output.mat file1.mgf file2.mgf…

Or to stdout

    $ cd src
    $ python ./converter.py file1.mgf file2.mgf…

The mstype (default MS1) can be specified with option -t

    $ cd src
    $ python ./converter.py -t MS2 file1.mgf file2.mgf…

## Usage of the merger

To merge one ms and a msms (only works with MGF as input and MAT as output for now):

    $ cd src
    $ python ./merger.py -1 ms1.mgf -2 ms2.mgf -o output.mat -n "Name of the merged"
    
Or to stdout:

    $ cd src
    $ python ./merger.py -1 ms1.mgf -2 ms2.mgf -n "Name of the merged"


Name is used to give a name to the merged spectrum

# Formats descriptors 

## MSP Description

    BLOCK1
    <newline>
    BLOCK2
    …


### Block structure

    NAME:
    PRECURSORMZ:
    PRECURSORTYPE:
    IONMODE: Positive or Negative
    Num Peaks: x (where x is number of peaks)
    mz intensity pairs (tab, comma or space delimited)


### Other possible fields:

    INSTRUMENTTYPE:
    INSTRUMENT:
    SMILES:
    INCHIKEY:
    COLLISIONENERGY:
    FORMULA:
    RETENTIONTIME:
    SPECTRUMTYPE: (ex Centroid)
    Comment


## MAT format

allows to put both MS1 and MS2 in the DB
adds the required parameter "MSTYPE:" 
that should be MS1 and MS2 

MS1 and MS2 have to follow each other.
example


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


« If you want to perform the MS/MS peak annotation with the known structure,
prepare two fields including FORMULA and SMILES. The formula and SMILES of the
neutralized structure should be made.» (source:
http://prime.psc.riken.jp/Metabolomics_Software/MS-FINDER/MSFINDER-Tutorial-VS2.pdf)

