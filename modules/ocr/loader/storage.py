storage = None


class OCRStorage:
    def __init__(self):
        self.txn = None

    @staticmethod
    def get_instance():
        global storage
        if storage is None:
            print("Creating OCRStorage instance")
            storage = OCRStorage()
        return storage
