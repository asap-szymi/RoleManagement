import Functionality


class Role:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.functions = []

    def __str__(self):
        f = []
        for func in self.functions:
            f.append(func.name)

        f = '\n'.join(f)

        return (f"Id: {self.id} Name: {self.name}"
               f"\nFunctionalities:\n{f}")

    def fetch(self, database):
        mycursor = database.cursor()
        sql = f"SELECT f.id, f.name FROM roles_to_function as rf LEFT JOIN functionalities as f ON rf.function_id = f.id WHERE role_id = {self.id}"
        mycursor.execute(sql)

        funcs = mycursor.fetchall()
        for func in funcs:
            f = Functionality.Functionality(func[0], func[1])
            self.functions.append(f)

        return funcs
