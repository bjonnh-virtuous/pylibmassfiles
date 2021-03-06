class InternalRepr():
    """A class for internal representation of mass data, this is going to move a
lot in here, try not to rely on it yet"""
    POSITIVE = 1
    NEGATIVE = 2
    DEFAULT_MSTYPE = 1

    def __init__(self):
        self.instrument = "Unknown instrument"
        self.ions = {}
        self.mstypes = [""]
        self.mstype = self.DEFAULT_MSTYPE
        self.title = ""
        self.mode = 0
        self.name = ""
        self.filename = ""
        self.retentiontime = ""
        self.activation = ""
        self.scans = 0
        self.precursormass = ""

    @property
    def mstype(self):
        return self.__mstype
    @mstype.setter
    def mstype(self, mstype):
        self.__mstype = mstype

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
        """If name is empty, return filename if no filename return 'Unknown'"""
        if self.__name == "":
            if self.__filename == "":
                return "Unknown"
            else:
                return self.__filename
        return self.__name

    @name.setter
    def name(self, x):
        self.__name = x

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, x):
        self.__filename = x

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

    @property
    def mstypes(self):
        return self.__mstypes

    @mstypes.setter
    def mstypes(self, x):
        self.__mstypes = x

    def mstypes_add(self, x):
        if x not in self.__mstypes:
            self.__mstypes.append(x)

    @property
    def precursormass(self):
        return self.__precursormass

    @precursormass.setter
    def precursormass(self, x):
        self.__precursormass = x

    def add_ion(self, ion, value, formula=None, mstype=None):
        """Add ion of type *mstype* in the storage"""
        if mstype is None:
            mstype = self.mstype  # We take the default mstype if not specified
        if mstype not in self.ions:
            self.ions[mstype] = []
        self.ions[mstype].append([ion, value, formula])

    def grab_ions(self, internalr):
        """Grab the ions from *internalr* (a InternalRepr too) and add them to the
        current one"""
        for mstype in internalr.ions:
            if mstype not in self.ions:
                self.ions[mstype] = []

            self.ions[mstype] += internalr.ions[mstype]
