from translators.MATTranslator import MATTranslator
from translators.MGFTranslator import MGFTranslator
from tools.StreamTranslator import StreamTranslator

import io

msp_test_ms = """NAME: challenge-009-ms.mgf
INSTRUMENTTYPE: LC-ESI-QTOF
ACTIVATION: CID
PRECURSORMZ: 
PRECURSORTYPE:
IONMODE: Negative
RETENTIONTIME: -1
TITLE: Scan Number: 1
SCANS: 1
MSTYPE: MS1
Num Peaks: 3
337.1079 100.0
338.1115 23.8
339.114 4.5

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

msp_test_msms = """NAME: challenge-009-msms.mgf
INSTRUMENTTYPE: LC-ESI-QTOF
ACTIVATION: CID
PRECURSORMZ: 
PRECURSORTYPE:
IONMODE: Negative
RETENTIONTIME: -1
TITLE: Scan Number: 1
SCANS: 1
MSTYPE: MS2
Num Peaks: 9
117.0347 2.3
133.0631 1.7
161.0242 2.5
217.0846 5.9
219.0634 7.3
268.0379 6.1
281.0457 20.3
293.0475 20.1
337.1079 100.0

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

mat_test_merged = """NAME: challenge-009-merged
INSTRUMENTTYPE: LC-ESI-QTOF
ACTIVATION: CID
PRECURSORMZ: 
PRECURSORTYPE:
IONMODE: Negative
RETENTIONTIME: -1
TITLE: Scan Number: 1
SCANS: 1
MSTYPE: MS1
Num Peaks: 3
337.1079 100.0
338.1115 23.8
339.114 4.5
MSTYPE: MS2
Num Peaks: 9
117.0347 2.3
133.0631 1.7
161.0242 2.5
217.0846 5.9
219.0634 7.3
268.0379 6.1
281.0457 20.3
293.0475 20.1
337.1079 100.0

"""


class Test_MGF2MSP:
    def test_ms(self):
        output_stream = io.StringIO()

        input_translator = MGFTranslator("MS1")
        stream_translator = StreamTranslator()

        output_translator = MATTranslator()

        stream_translator.set_output_stream(output_stream)
        stream_translator.set_output_translator(output_translator)

        input_stream = io.StringIO(mgf_test_ms)
        stream_translator.convert(input_stream, input_translator)
        input_stream.close()
        output_stream.flush()

        output_stream.seek(0)
        output = output_stream.read()
        print(output)
        print(msp_test_ms)
        assert output == msp_test_ms

    def test_msms(self):
        output_stream = io.StringIO()

        input_translator = MGFTranslator("MS2")
        stream_translator = StreamTranslator()

        output_translator = MATTranslator()

        stream_translator.set_output_stream(output_stream)
        stream_translator.set_output_translator(output_translator)

        input_stream = io.StringIO(mgf_test_msms)
        stream_translator.convert(input_stream, input_translator)
        input_stream.close()
        output_stream.flush()

        output_stream.seek(0)
        output = output_stream.read()
        assert output == msp_test_msms

    def test_merged_msms(self):
        output_stream = io.StringIO()

        input_translator_ms1 = MGFTranslator("MS1")
        input_translator_ms2 = MGFTranslator("MS2")

        output_translator = MATTranslator()

        spectras_ms1 = input_translator_ms1.read_from_stream(io.StringIO(mgf_test_ms))
        spectras_ms2 = input_translator_ms2.read_from_stream(io.StringIO(mgf_test_msms))

        spectras_ms1[0].grab_ions(spectras_ms2[0])
        spectras_ms1[0].name = "challenge-009-merged"
        output_translator.list_to_stream(spectras_ms1,
                                         output_stream)
        output_stream.flush()

        output_stream.seek(0)
        output = output_stream.read()
        assert output == mat_test_merged
