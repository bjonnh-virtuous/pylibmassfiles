class StreamTranslator:
    """A streaming translator that takes an input, convert it to the required
output format and streams it"""
    output_format = None
    output_stream = None
    handled_input_formats = ["mgf"]
    output_translator = None

    def set_output_translator(self, output_translator):
        self.output_translator = output_translator

    def set_output_stream(self, output_stream):
        """Set the output stream"""
        # XXX Should test if it is a usable stream
        self.output_stream = output_stream

    def convert(self, input_stream, input_translator):
        """Outputs the converted input stream in the input_format to output
        stream"""

        if self.output_stream is None:
            raise IOError("No output stream set")

        if self.output_translator is None:
            raise IOError("No output format set")

        input_converter = input_translator

        input_converter.read_from_stream(input_stream)
        self.output_translator.list_to_stream(input_converter.spectras,
                                              self.output_stream)
