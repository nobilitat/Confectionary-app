import psycopg2


class ConnectToDatabase:
    """Подключение к базе данных"""

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.connect = None

    def connect_db(self):
        self.connect = psycopg2.connect(
            host="localhost",
            port="5432",
            database="confectionery_db",
            user=self.login,
            password=self.password)

        return self.connect

    def close(self):
        self.connect.close()
