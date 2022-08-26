class Functionality:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Id: {self.id} Name: {self.name}"