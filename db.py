import sqlite3
import config

product_dict = config.product_dict
initial_db = 'id INTEGER PRIMARY KEY'
tables = {
    'Users': {
        'login': 'TEXT',
        'number': 'TEXT',
        'town': 'TEXT',
        'street': 'TEXT',
        'cash': 'REAL'
    },
    'Basket': product_dict,
    'Products': {
        'name': 'TEXT',
        'price_id': 'INTEGER',
        'photo': 'TEXT',
        'description': 'TEXT',
        'sticker': 'TEXT',
        'min_amount': 'INTEGER',
        'add_call': 'TEXT',
        'delete_call': 'TEXT',
        'all_delete_call': 'TEXT'
    }
}


class BotDataBase:

    def __init__(self, connect):
        self.connect = connect
        # noinspection PyBroadException
        try:
            cursor = self.connect.cursor()
            for table in tables.keys():
                cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table, initial_db))
                for k, v in tables[table].items():
                    cursor.execute("ALTER TABLE {} ADD {} {}".format(table, k, v))
            print('Таблицы были успешно созданы!')
        except sqlite3.OperationalError:
            print('Ошибка. Открыть или создать таблицыв в БД не удалось. Скорее всего, все таблицы уже созданы.')
            self.connect.commit()

    def check_db(self, message):
        cursor = self.connect.cursor()
        check_user_id = message.chat.id
        cursor.execute(f"SELECT id FROM Users WHERE id = {check_user_id}")
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def check_basket(self, id_user):
        cursor = self.connect.cursor()
        for product in tables['Basket'].keys():
            cursor.execute(f"SELECT {product} FROM Basket WHERE id = {id_user}")
            if int(str(cursor.fetchone()[0])) > 0:
                return True
        else:
            return False

    def create_user(self, temp_data):
        cursor = self.connect.cursor()
        cursor.execute(f"INSERT INTO Users VALUES (?,?,?,?,?,?);", [temp_data['user_id'],
                                                                    temp_data['first_name'],
                                                                    temp_data['phone_number'],
                                                                    'NOPE',
                                                                    'NOPE',
                                                                    0.00])
        cursor.execute(f"INSERT INTO Basket VALUES(?,?,?,?,?,?,?,?,?,?,?,?);", [temp_data['user_id'], 0, 0,
                                                                              0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.connect.commit()

    def update_db(self, id_user, new_item):
        cursor = self.connect.cursor()
        data_users = {'id': """UPDATE Users SET id = ? WHERE id = ?""",
                      'login': """UPDATE Users SET login = ? WHERE id = ?""",
                      'number': """UPDATE Users SET number = ? WHERE id = ?""",
                      'town': """UPDATE Users SET town = ? WHERE id = ?""",
                      'street': """UPDATE Users SET street = ? WHERE id = ?"""}
        for item in new_item.keys():
            temp = (new_item[item], id_user,)
            cursor.execute(data_users[item], temp)
        self.connect.commit()

    def get_data_db(self, id_user, table):
        # отдает кортеж с данными.
        # для Users: 0 - id, 1 - login, 2 - number, 3 - town, 4 - street, 5 - cash
        # для Basket: 0 - id, 1..n - товары
        cursor = self.connect.cursor()
        temp = ()
        if table == 'Users':
            get_items = """SELECT * FROM Users WHERE id = ?"""
            cursor.execute(get_items, (id_user,))
            temp = cursor.fetchone()
        elif table == 'Basket':
            get_items = """SELECT * FROM Basket WHERE id = ?"""
            cursor.execute(get_items, (id_user,))
            temp = cursor.fetchone()
        cursor.close()
        return temp

    def get_product_data(self, id_prod):
        cursor = self.connect.cursor()
        get_product = """SELECT * FROM Products WHERE id = ?"""
        cursor.execute(get_product, (id_prod,))
        temp = cursor.fetchone()
        cursor.close()
        return temp

    def count_prods(self):
        cursor = self.connect.cursor()
        cursor.execute("""SELECT * FROM Products""")
        return len(cursor.fetchall())

    def create_product(self):
        cursor = self.connect.cursor()
        cursor.execute(f"INSERT INTO Products VALUES (?,?,?,?,?,?,?,?,?,?);", [1, 'CheckName',
                                                                               8, "https://i.imgur.com/GzBhhGc.png",
                                                                               'Описание', 'sticker_id', 2,
                                                                               'sticker_id_add', 'sticker_id_delete',
                                                                               'sticker_id_delete_all'])
        self.connect.commit()

    def add_basket(self, id_user, product, amount):
        cursor = self.connect.cursor()
        cursor.execute(f"""SELECT {product} FROM Basket WHERE id = {id_user} """)
        temp_amount = int(cursor.fetchone()[0]) + amount
        cursor.execute(f"""UPDATE Basket SET {product} = {temp_amount} WHERE id = {id_user}""")
        self.connect.commit()

    def remove_basket(self, id_user, product):
        cursor = self.connect.cursor()
        cursor.execute(f"""SELECT {product} FROM Basket WHERE id = {id_user}""")
        temp_amount = int(cursor.fetchone()[0]) - 1
        cursor.execute(f"""UPDATE Basket SET {product} = {temp_amount} WHERE id = {id_user}""")
        self.connect.commit()

    def delete_all_basket(self, id_user, product):
        cursor = self.connect.cursor()
        cursor.execute(f"""UPDATE Basket SET {product} = 0 WHERE id = {id_user}""")
        self.connect.commit()


water_db = BotDataBase(connect=sqlite3.connect('water.db', check_same_thread=False))
