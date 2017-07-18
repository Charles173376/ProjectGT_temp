
class ProperRange:

    def __init__(self):
        self.proper_min = 160
        self.proper_max = 210

    def set_max(self, val):
        proper_max = val
        if proper_max < self.proper_min:
            self.proper_min = proper_max-1

    def set_min(self, val):
        proper_min = val
        if proper_min > self.proper_max:
            self.proper_max = proper_min+1




