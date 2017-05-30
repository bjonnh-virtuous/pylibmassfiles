class MATTranslator:
    """Converter to MAT format. Only do writing for now"""
    READER = 0
    WRITER = 1
    mstype = ""

    def set_mstype(self, mstype):
        self.mstype = mstype

    def internal_to_stream(self, internal, stream):
        if internal.name:
            stream.write("NAME: {}\n".format(
                internal.name))
        if internal.instrument:
            stream.write("INSTRUMENTTYPE: {}\n".format(
                internal.instrument))
        if internal.activation:
            stream.write("ACTIVATION: {}\n".format(
                internal.activation))

        # This is mandatory

        stream.write("PRECURSORMZ: {}\n".format(
                internal.precursormass))
        stream.write("PRECURSORTYPE:\n")
        mode = ""
        if internal.mode == internal.POSITIVE:
            mode = "Positive"
        elif internal.mode == internal.NEGATIVE:
            mode = "Negative"
        stream.write("IONMODE: {}\n".format(mode))

        if internal.retentiontime:
            stream.write("RETENTIONTIME: {}\n".format(
                internal.retentiontime))

        if internal.title:
            stream.write("TITLE: {}\n".format(
                internal.title))

        if internal.scans:
            stream.write("SCANS: {}\n".format(
                internal.scans))

        # Internal mstype overrides the translator type
        if internal.mstype:
            stream.write("MSTYPE: {}\n".format(
                internal.mstype))
        elif self.mstype:
            stream.write("MSTYPE: {}\n".format(
                self.mstype))

        if internal.ions:
            stream.write("Num Peaks: {}\n".format(len(internal.ions)))
            for ion in internal.ions:
                if len(ion) > 2 and ion[2] != "":
                    stream.write("{} {} {}\n".format(*ion))
                else:
                    stream.write("{} {}\n".format(*ion))
        stream.write("\n")
    def list_to_stream(self, internals, stream):
        for internal in internals:
            self.internal_to_stream(internal, stream)
