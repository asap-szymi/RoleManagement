import Role


class User:
    def __init__(self, id: int, first_name: str = "", last_name: str = "", email: str = "", password: str = ""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.roles = []

    # fetch user data from database using id
    def fetch(self, database):
        mycursor = database.cursor()

        sql = f"SELECT * FROM users WHERE id={self.id}"
        mycursor.execute(sql)
        data = mycursor.fetchall()[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.email = data[3]
        self.password = data[4]

        self.fetchRoles(database)

        return data

    # add user to database
    def add(self, database):
        mycursor = database.cursor()

        # check if user id and email are free
        sql = 'SELECT * FROM users WHERE id=%s OR email=%s'
        val = (self.id, self.email)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if self.email != "" and self.password != "" and len(result) == 0:
            sql = 'INSERT INTO users (id, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)'
            val = (self.id, self.first_name, self.last_name, self.email, self.password)
            mycursor.execute(sql, val)
            database.commit()
            return 1
        else:
            print("User with this id or email already exists OR email or password are missing")
            return 0

    # delete user from database
    def delete(self, database):
        mycursor = database.cursor()
        sql = f"DELETE FROM users WHERE id={self.id}"
        mycursor.execute(sql)
        database.commit()

    # fetch user roles from database
    def fetchRoles(self, database):
        mycursor = database.cursor()

        # get user roles
        sql = f"SELECT r.id, r.name FROM users_to_roles as ur LEFT JOIN roles as r ON ur.role_id = r.id WHERE user_id = {self.id}"
        mycursor.execute(sql)

        roles = mycursor.fetchall()
        for role in roles:
            r = Role.Role(role[0], role[1])
            self.roles.append(r)

        return roles

    # assign user a new role
    def addRole(self, role: Role, database):
        # check if user-role pair already exists

        mycursor = database.cursor()
        sql = 'SELECT * FROM users_to_roles WHERE user_id=%s AND role_id=%s'
        val = (self.id, role.id)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if len(result) == 0 and role not in self.roles:
            self.roles = self.roles.append(role)

            mycursor = database.cursor()
            sql = "INSERT INTO users_to_roles (user_id, role_id) VALUES (%s, %s)"
            val = (self.id, role.id)
            mycursor.execute(sql, val)

            database.commit()
            print(f"Role {role.name} added to user {self.first_name} {self.last_name}")
            return 0
        else:
            print(f"User {self.first_name} {self.last_name} already is {role.name}")
            return 1

    # remove role from user
    def removeRole(self, role: Role, database):
        found = False
        for r in self.roles:
            if r.id == role.id:
                found = True
                break

        if found:
            self.roles.remove(r)

            mycursor = database.cursor()
            sql = f"DELETE FROM users_to_roles WHERE user_id={self.id} AND role_id={role.id}"
            mycursor.execute(sql)
            database.commit()
            print(f"User {self.first_name} {self.last_name} is no longer {role.name}")
        else:
            print(f"User {self.first_name} {self.last_name} is not {role.name}")

    def __str__(self):
        r = []
        for role in self.roles:
            r.append(role.name)

        return (f'Id: {self.id}'
                f'\nName: {self.first_name} {self.last_name}'
                f'\nEmail: {self.email}'
                f'\nRoles: {" ".join(r)}')
