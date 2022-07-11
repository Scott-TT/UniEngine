class database_config:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

default_config = database_config(user="ogameuser", password="plop", host="localhost", database="uniengine")

