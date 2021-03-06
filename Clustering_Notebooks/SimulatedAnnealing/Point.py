class Point(object):
    def __init__(self, id, dimension, assignment):
        self.ID = id
        self.dimension = dimension
        self.assignment = assignment
        self.next = None

    def __str__(self):
        return str(self.assignment)

    def __repr__(self):
        return '{},{}'.format(self.dimension, self.assignment)

    def to_dict(self):
        new_dict = dict()
        new_dict.update({"ID": self.ID, "assignment": self.assignment})
        for k in range(len(self.dimension)):
            current_str = "x"+str(k+1)
            new_dict.update({current_str: self.dimension[k]})
        return new_dict

    def set_assignment(self, val):
        self.assignment = val

    def set_next(self, val):
        if val != self.assignment:
            self.next = val
            return True
        return False

    def reset(self):
        self.next = None

    def update(self):
        if self.next is not None:
            self.assignment = self.next
        self.next = None

    def get_assignment(self):
        if self.next is None:
            return self.assignment
        return self.next

    def clone(self):
        return Point(self.dimension, self.assignment)

