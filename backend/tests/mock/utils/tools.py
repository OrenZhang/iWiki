from constents import SHORT_CHAR_LENGTH
from utils.tools import simple_uniq_id


class SimpleUniqIdMock:
    ids = []

    def __init__(self):
        uid = simple_uniq_id(SHORT_CHAR_LENGTH)
        uid2 = simple_uniq_id(SHORT_CHAR_LENGTH)
        self.ids = [uid, uid, uid2]

    def simple_uniq_id(self, *args, **kwargs):
        id = self.ids[0]
        self.ids = self.ids[1:]
        return id
