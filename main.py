import mysql.connector

import Functionality
import Role
import User

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="RoleManagement",
)

def fetchUsers(database):
    mycursor = database.cursor()

    sql = f"SELECT * FROM users"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    users = []

    for user in data:
        u = User.User(user[0])
        u.fetch(mydb)
        users.append(u)

    return users

def fetchRoles(database):
    mycursor = database.cursor()

    sql = f"SELECT * FROM roles"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    roles = []

    for role in data:
        r = Role.Role(role[0],role[1])
        roles.append(r)

    return roles

def fetchFunc(database):
    mycursor = database.cursor()

    sql = f"SELECT * FROM functionalities"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    funcs = []

    for func in data:
        r = Functionality.Functionality(func[0],func[1])
        funcs.append(r)

    return funcs

users = fetchUsers(mydb)
roles = fetchRoles(mydb)
funcs = fetchFunc(mydb)

for r in roles: r.fetch(mydb)

print("Users:")
for u in users:
    print(u)

print("\nRoles:")
for r in roles:
    print(r)

print("\nFunctionalities:")
for f in funcs:
    print(f)

mydb.close()
