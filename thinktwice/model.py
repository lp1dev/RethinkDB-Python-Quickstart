import rethinkdb as r
from thinktwice.exceptions import ThinkTwiceException


class Model:
    index = None
    table = None
    one_per_index = True

    def __init__(self):
        self.__db_create()

    def __db_create(self):
        if self.index is not None:
            if self.one_per_index and len(list(r.table(self.table).get_all(self.export()[self.index],
                                                                           index=self.index).run())):
                raise ThinkTwiceException(
                    'There is already an item in the table %s with the index %s' % (
                        self.table, self.export()[self.index]), 409)
        r.table(self.table).insert(self.export(True)).run()

    def export(self, export_all=False):
        return {}
