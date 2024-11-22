from pymysql import connect
from pymysql.cursors import DictCursor


class Database:
    def __init__(self,
                 DB_NAME=str,
                 DB_USER=str,
                 DB_PASSWORD=str,
                 DB_HOST=str,
                 DB_PORT=int) -> None:
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT

    @property
    def connection(self):
        return connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            cursorclass=DictCursor
        )

    def execute(self,
                sql: str,
                args: tuple = (),
                commit: bool = False,
                fetchone: bool = False,
                fetchmany: bool = False,
                fetchall: bool = False) -> None | dict | tuple:
        database = self.connection
        cursor = database.cursor()
        cursor.execute(sql, args)
        data = None

        if fetchall:
            data = cursor.fetchall()
        elif fetchone:
            data = cursor.fetchone()
        else:
            data = None

        if commit:
            database.commit()

        return data

    def register_user(self,
                      telegram_id: int,
                      telegram_full_name: str) -> None:
        sql = """
        INSERT INTO users (telegram_id, telegram_full_name)
        VALUES (%s, %s)
        """
        self.execute(sql, (telegram_id, telegram_full_name), commit=True)

    def create_users_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            telegram_id VARCHAR(100) UNIQUE,
            telegram_full_name VARCHAR(255),
            position BOOLEAN DEFAULT False,
            page_number INT,
            balance DECIMAL(10, 2) DEFAULT '20000.00',
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            gender VARCHAR(100),
            primium INT DEFAULT 0
        )
        """
        self.execute(sql)


    def update_user_page(self, page: int, telegram_id):
        sql = """
            UPDATE users SET 
            page_number = %s
            WHERE telegram_id = %s
        """
        return self.execute(sql, (page, telegram_id), commit=True)

    def get_user(self, telegram_id: int):
        sql  = """
            SELECT * FROM users WHERE telegram_id = %s
        """

        return self.execute(sql, fetchone=True)



    def create_city_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS city (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(200),
                owner INT NOT NULL REFERENCES users(telegram_id),
                CONSTRAINT city_name_users_id_uniqe UNIQUE(owner, city_name) 
            )
        """
        self.execute(sql)

    def add_city(self, city_name, telegram_id):
        sql = """
            INSERT INTO city (city_name, owner) VALUES (%s, %s)
        """
        return self.execute(sql, (city_name, telegram_id), commit=True)

    def select_city_delete(self, telegram_id, city_name):
        sql =  """
            DELETE FROM city WHERE owner = %s AND city_name = %s ;
        """

        return self.execute(sql, (telegram_id, city_name), commit=True)

    def all_delete_city_user(self, telegram_id):
        sql = """
            delete * from city where telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), commit=True)


    def get_city_user(self, telegram_id, city_name):
        sql = """
            select * from city where owner = %s and city_name = %s
        """
        return self.execute(sql, (telegram_id, city_name), fetchone=True)


    def register_city(self, telegram_id, city_name):
        user = self.get_user(telegram_id)
        user_id = user.get('id')

        sql = """
            INSERT INTO city (owner, city_name) VALUES
            (%s, %s)
        """
        return self.execute(sql, (user_id, city_name), commit=True)



    def sql_check_user(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def user_info(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def update_user_data(self, first_name: str, last_name: str, gender: str, telegram_id: str):
        sql = """
            UPDATE users SET 
            first_name = %s, 
            last_name = %s,
            gender = %s
            where telegram_id = %s
        """
        return self.execute(sql, (first_name, last_name, gender, telegram_id), commit=True)

    def update_user_balance(self, balance, telegram_id):
        sql = """
            UPDATE users SET 
            balance = %s
            WHERE telegram_id = %s
        """
        return self.execute(sql, (balance, telegram_id), commit=True)



    def is_primium(self, primium: int, telegram_id: int):
        sql = """
            UPDATE users SET 
            primium = %s
            where telegram_id = %s
        """
        return self.execute(sql, (primium, telegram_id), commit=True)
    def reklama_users(self):
        sql = """
            SELECT telegram_id FROM users;
        """
        return self.execute(sql, fetchall=True)


    def all_user(self):
        sql = """
            SELECT telegram_id from users
        """
        return self.execute(sql, fetchall=True)


db = Database(
    DB_NAME='secret_chat_db',
    DB_USER='root',
    DB_PASSWORD='1871724143_Shahzod',
    DB_HOST='localhost',
    DB_PORT=3306
)

db.create_users_table()
db.create_city_table()
