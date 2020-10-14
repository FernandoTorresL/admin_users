class RecordRow():

    def __init__(self, all_rows, i):
        self._column01 = all_rows[i]
        self._column02 = all_rows[i + 1]
        self._column03 = all_rows[i + 2]
        self._column04 = all_rows[i + 3]
        self._column05 = all_rows[i + 4]

    @property
    def curp(self):
        result = self._column01
        return result.text

    @property
    def matricula(self):
        result = self._column02
        return result.text

    @property
    def nombre(self):
        result = self._column03
        return result.text

    @property
    def cuenta(self):
        result = self._column04
        return result.text

    @property
    def grupo(self):
        result = self._column05
        return result.text
