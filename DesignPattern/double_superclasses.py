

class BSuper:
    def __init__(self):
        self.var = 'I am B'

    def large_b(self):
        print(self.var)


class BChild(BSuper):
    def __init__(self):
        super().__init__()
        self.sub_var = 'just b'

    def small_b(self):
        print(self.sub_var)


class ASuper:
    def __init__(self):
        # b_inst as non type
        self.b_inst = None

    def set_b(self, _b: BSuper):
        # b_inst as different types for each of super and child
        self.b_inst: BSuper = _b

    def use_b(self):
        self.b_inst.large_b()


class AChild(ASuper):
    def __init__(self):
        super().__init__()

    def set_b(self, _b: BChild):
        # b_inst as different types for each of super and child
        self.b_inst: BChild = _b

    def use_small_b(self):
        self.b_inst.small_b()


if __name__ == '__main__':
    a = AChild()
    b = BChild()
    a.set_b(b)
    a.use_b()
    a.use_b()
