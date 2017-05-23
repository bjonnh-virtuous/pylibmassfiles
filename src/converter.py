# Status: not working

# Idea:

input_format = "mgf"
output_format = "mat"

input_stream = open('test.mgf', 'r')
output_stream = open('test.mat', 'w')

class InternalRepr(dict):
    """A class for internal representation of mass data, this is going to move a
lot in here, try not to rely on it yet"""
    def __init__():
        pass

class StreamTranslator:
    """A streaming translator that takes an input, convert it to the required
output format and streams it"""
    input_format = None
    output_format = None
    handled_input_formats = ["mgf"]
    handled_output_formats = ["mat"]

    def __init__():
        pass

    def set_output_format(self, output_format):
        """Set the output format to output format"""
        if output_format in self.handled_output_formats:
            self.output_format = output_format
        else:
            raise ValueError("Invalid output format")

    def convert(self, input_stream, input_format):
        """Outputs the converted input stream in the input_format to output
        stream"""

        if output_stream is None:
            raise IOError("No output stream set")

        if output_format is None:
            raise IOError("No output format set")

        if input_format not in self.handled_input_formats:
            raise ValueError("Invalid input format")

        if input_format == "mgf":
            self.convert_from_mgf(input_stream, output_stream, output_format)


stream_translator = StreamTranslator()
stream_translator.set_output_format(output_format)
stream_translator.set_output_stream(output_stream)
# This is done that way so we can have multiple input files in different
# formats
# ex: stream_translator.convert(input_stream, input_format)

stream_translator.convert(input_stream)
input_stream.close()
output_stream.close()
