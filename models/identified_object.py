class IdentifiedObject:
    """class doc_string"""

    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid
    
    def __eq__(self, other):
        return type(other) == type(self) and other.oid == self.oid
    
    def __hash__(self):
        return hash(self.oid)
