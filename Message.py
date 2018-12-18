
class Message():
    def __init__(self, srcID, value):
        self.srcID = srcID
        self.value = value

    def get_src_ID(self):
        return self.srcID

    def get_value(self):
        return self.value
