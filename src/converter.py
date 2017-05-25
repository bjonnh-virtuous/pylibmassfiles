#!/usr/bin/python3
"""Convert mass spectral library formats"""

import sys
import argparse
from translators.MATTranslator import MATTranslator
from translators.MGFTranslator import MGFTranslator
from tools.StreamTranslator import StreamTranslator

import io


supported_input_formats = ['mgf']
supported_output_formats = ['mat']

parser = argparse.ArgumentParser(
    description='Convert mass spectral library formats'
)


parser.add_argument('-I','--input-format', type=str, nargs=1,
                    help='The input format',
                    choices=['mgf'])
parser.add_argument('-O','--output-format', type=str, nargs=1,
                    help='The output format',
                    default='mat',
                    choices=['mat'])
parser.add_argument('-o', '--output-file', type=str, nargs='?',
                    help='Output file name if absent, outputs to stdout')
parser.add_argument('files', metavar='files', type=str, nargs='+',
                    help='inputfiles')

args = parser.parse_args()


if args.input_format == "mgf":
    input_translator_type = MGFTranslator
else:
    input_translator_type = None


if args.output_format == "mat":
    output_translator = MATTranslator()
else:
    print("Please specify a valid translator!",
          file=sys.stderr)
    sys.exit(2)


if args.output_file:
    try:
        output_stream = open(args.output_file, 'w')
    except IOError:
        print("Impossible to open output file {}.".format(args.output_file),
              file=sys.stderr)
        sys.exit(2)
else:
    output_stream = sys.stdout

stream_translator = StreamTranslator()
stream_translator.set_output_stream(output_stream)
stream_translator.set_output_translator(output_translator)

for filename in args.files:

    if not input_translator_type:
        if filename.endswith('.mgf'):
            input_translator_type = MGFTranslator
        else:
            print("Impossible to determine format of input file {}".format(
                filename), file=sys.stderr)
            continue
    try:
        with open(filename, 'r') as f:
            stream_translator.convert(f, input_translator_type)
    except IOError:
        print("Impossible to open file {}, skipping it".format(filename),
              file=sys.stderr)
        sys.exit()

output_stream.close()
