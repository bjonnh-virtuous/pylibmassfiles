import io

# Status: not working

#

msp_test_ms = """
NAME: challenge-009-ms.mgf
INSTRUMENTTYPE: LC-ESI-QTOF
ACTIVATION: CID
PRECURSORMZ:
PRECURSORTYPE:
IONMODE: Negative
RETENTIONTIME: -1
TITLE: Scan Number: 1
MSTYPE: MS1
Num Peaks: 3
337.1079	100.0
338.1115	23.8
339.1140	4.5
"""

mgf_test_ms = """
# Splash: splash10-000i-0009000000-be74b323e6f3e32b5546
SOURCE_INSTRUMENT=LC-ESI-QTOF
ACTIVATION=CID
FILENAME=challenge-009-ms.mgf
BEGIN IONS
PEPMASS=
RTINSECONDS=-1
CHARGE=-1
TITLE=Scan Number: 1
SCANS=1
337.1079	100.0
338.1115	23.8
339.1140	4.5
END IONS
"""

msp_test_msms = """
NAME: challenge-009-msms.mgf
INSTRUMENTTYPE: LC-ESI-QTOF
ACTIVATION: CID
PRECURSORMZ:
PRECURSORTYPE:
IONMODE: Negative
RETENTIONTIME: -1
TITLE: Scan Number: 1
MSTYPE: MS2
Num Peaks: 9
117.0347	2.3
133.0631	1.7
161.0242	2.5
217.0846	5.9
219.0634	7.3
268.0379	6.1
281.0457	20.3
293.0475	20.1
337.1079	100.0
"""

mgf_test_msms = """
NAME=challenge-009-msms.mgf
# Splash: splash10-000i-0059000000-dcf35fcec5614cef6f45
SOURCE_INSTRUMENT=LC-ESI-QTOF
ACTIVATION=CID
FILENAME=challenge-009-msms.mgf
BEGIN IONS
PEPMASS=
RTINSECONDS=-1
CHARGE=-1
TITLE=Scan Number: 1
SCANS=1
117.0347	2.3
133.0631	1.7
161.0242	2.5
217.0846	5.9
219.0634	7.3
268.0379	6.1
281.0457	20.3
293.0475	20.1
337.1079	100.0
END IONS
"""


class InternalRepr(dict):
    """A class for internal representation of mass data, this is going to move a
lot in here, try not to rely on it yet"""
    POSITIVE = 1
    NEGATIVE = 2

    def __init__(self):
        self.instrument = "Unknown instrument"

    @property
    def instrument(self):
        return self.__instrument

    @instrument.setter
    def instrument(self, x):
        self.__instrument = x

    @property
    def activation(self):
        return self.__activation

    @activation.setter
    def activation(self, x):
        self.__activation = x

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, x):
        self.__name = x

    @property
    def retentiontime(self):
        return self.__retentiontime

    @retentiontime.setter
    def retentiontime(self, x):
        self.__retentiontime = x

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, x):
        self.__mode = x

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, x):
        self.__title = x

    @property
    def scans(self):
        return self.__scans

    @scans.setter
    def scans(self, x):
        self.__scans = x


class MGFTranslator:
    IN_COMPOUND = 1
    IN_ION = 2
    START = 0

    def __init__(self):
        self.spectras = []

    def read_from_stream(self, stream):
        mode = self.START
        current = InternalRepr()
        for line in stream.readlines():
            if line.startswith("#"):  # Comment
                continue

            if line.strip() == "":
                if mode == self.IN_COMPOUND:
                    self.spectras.append(current)
                continue

            if mode == self.START:
                mode = self.IN_COMPOUND

            if mode == self.IN_COMPOUND:
                if line.startswith("SOURCE_INSTRUMENT="):
                    current.instrument = line.split("=")[1].strip()

                elif line.startswith("ACTIVATION="):
                    current.activation = line.split("=")[1].strip()

                elif line.startswith("FILENAME="):
                    current.name = line.split("=")[1].strip()

                elif line.startswith("BEGIN IONS"):
                    mode = self.IN_ION
                    continue
                else:
                    print("Invalid line in compound mode \
                    \"{}\"".format(line.strip()))

            if mode == self.IN_ION:
                if line.startswith("END IONS"):
                    mode = self.IN_COMPOUND

                elif line.startswith("PEPMASS="):
                    pass
                elif line.startswith("RTINSECONDS="):
                    current.retentiontime = line.split("=")[1].strip()
                elif line.startswith("CHARGE="):
                    charge = line.split("=")[1].strip()
                    if charge == "-1":
                        current.mode = InternalRepr.NEGATIVE
                    elif charge == "1+":
                        current.mode = InternalRepr.POSITIVE
                    else:
                        print("Unsupported charge type {}".format(charge))
                elif line.startswith("TITLE="):
                    current.title = line.split("=")[1].strip()
                elif line.startswith("SCANS="):
                    current.scans = line.split("=")[1].strip()
                elif line.translate({ord(x): '' for x in list('0123456789. ')}).strip() == "":
                    print("Ion: {}".format(line))
                else:
                    print("Invalid line in ion mode \
                    \"{}\"".format(line.strip()))

        return(self.spectras)


class StreamTranslator:
    """A streaming translator that takes an input, convert it to the required
output format and streams it"""
    output_format = None
    output_stream = None
    handled_input_formats = ["mgf"]
    handled_output_formats = ["mat"]

    def __init__(self):
        pass

    def set_output_format(self, output_format):
        """Set the output format to output format"""
        if output_format in self.handled_output_formats:
            self.output_format = output_format
        else:
            raise ValueError("Invalid output format")

    def set_output_stream(self, output_stream):
        """Set the output stream"""
        # XXX Should test if it is a usable stream
        self.output_stream = output_stream

    def convert(self, input_stream, input_format):
        """Outputs the converted input stream in the input_format to output
        stream"""

        if self.output_stream is None:
            raise IOError("No output stream set")

        if self.output_format is None:
            raise IOError("No output format set")

        if input_format not in self.handled_input_formats:
            raise ValueError("Invalid input format")

        if input_format == "mgf":
            converter = MGFTranslator()

        # output_stream.write(
        converter.read_from_stream(input_stream)
        print("Will convert to {} later".format(self.output_format))
        # )
        # self.convert_from_mgf(input_stream, output_stream, output_format)




output_stream = io.StringIO()  #open('test.mat', 'w')

stream_translator = StreamTranslator()
stream_translator.set_output_format("mat")
stream_translator.set_output_stream(output_stream)

# This is done that way so we can have multiple input files in different
# formats
# ex: stream_translator.convert(input_stream, input_format)
input_stream = io.StringIO(mgf_test_ms)
stream_translator.convert(input_stream, 'mgf')

input_stream.close()
output_stream.close()
