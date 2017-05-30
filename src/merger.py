#!/usr/bin/python3
"""Merge two mgf files, one with ms one with msms and produce a MAT file"""

from translators.MATTranslator import MATTranslator
from translators.MGFTranslator import MGFTranslator
import io
import sys
import argparse



parser = argparse.ArgumentParser(
    description='Merge two mgf (ms and msms) in one mat'
)


parser.add_argument('-1','--ms1', type=str, nargs=1,
                    help='The input MS spectra',
                    required=True)
parser.add_argument('-2','--ms2', type=str, nargs=1,
                    help='The input MSMS spectra',
                    required=True)
parser.add_argument('-n','--name', type=str, nargs='?',
                    help='Name of the resulting spectra',
                    default="Merged spectra")
parser.add_argument('-o', '--output-file', type=str, nargs='?',
                    help='Output file name if absent, outputs to stdout')

args = parser.parse_args()

output_translator = MATTranslator()
input_translator_ms1 = MGFTranslator("MS1")
input_translator_ms2 = MGFTranslator("MS2")

if args.output_file:
    try:
        output_stream = open(args.output_file, 'w')
    except IOError:
        print("Impossible to open output file {}.".format(args.output_file),
              file=sys.stderr)
        sys.exit(2)
else:
    output_stream = sys.stdout
try:
    with open(args.ms1[0], 'r') as f:
        spectras_ms1 = input_translator_ms1.read_from_stream(f)
except IOError:
    print("Cannot open MS1 spectra {}".format(args.ms1[0]), file=sys.stderr)
    sys.exit(2)

try:
    with open(args.ms2[0], 'r') as f:
        spectras_ms2 = input_translator_ms2.read_from_stream(f)
except IOError:
    print("Cannot open MS2 spectra {}".format(args.ms2[0]), file=sys.stderr)
    sys.exit(2)

spectras_ms1[0].grab_ions(spectras_ms2[0])
spectras_ms1[0].name = args.name
output_translator.list_to_stream(spectras_ms1,
                                 output_stream)
output_stream.close()
