class DuplicateOid(Exception):
    """"Exception intended to be thrown when a duplicate object is added to a collection """
    def __init__(self, message, oid):
        super().__init__(message)
        self.oid = oid