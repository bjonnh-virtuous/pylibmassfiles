from InternalRepr import InternalRepr


class MGFTranslator:
    """Convert from MGF format. Only do reading for now.
    Optimized for CASMI MGFs, many options are missing"""
    IN_COMPOUND = 1
    IN_ION = 2
    START = 0
    READER = 1
    WRITER = 0

    def __init__(self):
        self.spectras = []

    def read_from_stream(self, stream):
        mode = self.START
        current = InternalRepr()
        for line in stream.readlines():
            if line.startswith("#"):  # Comment
                continue

            if line.strip() == "":
                continue

            if mode == self.START:
                mode = self.IN_COMPOUND

            if mode == self.IN_COMPOUND:
                if line.startswith("SOURCE_INSTRUMENT="):
                    current.instrument = line.split("=")[1].strip()

                elif line.startswith("ACTIVATION="):
                    current.activation = line.split("=")[1].strip()

                elif line.startswith("FILENAME="):
                    current.filename = line.split("=")[1].strip()

                elif line.startswith("NAME="):
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
                    self.spectras.append(current)
                    current = InternalRepr()

                elif line.startswith("PEPMASS="):
                    current.precursormass = line.split("=")[1].strip()
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
                elif line.translate({ord(x): '' for x in list(
                        '0123456789. ')}).strip() == "":
                    ions = line.strip().split()
                    try:
                        if len(ions) >= 2:
                            formula = " ".join(ions[2:])
                        else:
                            formula = ""

                        current.add_ion(float(ions[0]), float(ions[1]),
                                        formula)
                    except ValueError:
                        print("Invalid ion format: {}".format(line.strip()))

                else:
                    print("Invalid line in ion mode \
                    \"{}\"".format(line.strip()))

        return(self.spectras)
