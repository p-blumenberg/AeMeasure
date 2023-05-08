import os
import shutil
import unittest

import aemeasure
from aemeasure import Database, MeasurementSeries


@aemeasure.save
def f(arg, *args, something=0, **kwargs):
    return "result"


class SaveDecoratorTest(unittest.TestCase):
    def _prepare_db(self, path):
        self._clear_db(path)
        return Database(path)

    def _clear_db(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_1(self):
        self._clear_db("./test_db")
        self._prepare_db("./test_db")

        with MeasurementSeries("./test_db"):
            f(1, 2, 3, something=4, something_else=5)
        db = Database("./test_db")

        self.assertEqual(len(db.load()), 1)
        loaded = db.load()[0]
        self.assertEqual(loaded["arg"], 1)
        self.assertEqual(loaded["args"], [2, 3])
        self.assertEqual(loaded["something"], 4)
        self.assertEqual(loaded["kwargs"], {"something_else": 5})
        self.assertEqual(loaded["result"], "result")
        print(loaded)

        self._clear_db("./test_db")
