import sqlite3
import os
import csv
import numpy as np
import math
import warnings

class Backend(object):
    def __init__(self, db_path):
        self.db_path = db_path

        # Create SQLite database if not yet exist
        if os.path.exists(db_path) is not True:
            self.__init_database()
        
    def __init_database(self):
        if os.path.isdir("./Database") is False:
            os.mkdir("./Database")

        # Open database
        db_connection = sqlite3.connect(self.db_path)
        db_cursor = db_connection.cursor()

        # Create user table
        create_user_table = """CREATE TABLE user(
            user_id INTEGER PRIMARY KEY,
            user_name TEXT
        );"""
        db_cursor.execute(create_user_table)
        insert_user = [
            (1, "Alice"),
            (2, "Bob")
        ]
        db_cursor.executemany("INSERT INTO user VALUES (?, ?)", insert_user)

        # Create inventory type table
        create_inv_type_table = """CREATE TABLE inventory_type(
            type_id INTEGER PRIMARY KEY,
            type_name TEXT,
            type_parent_type INTEGER
        );"""
        db_cursor.execute(create_inv_type_table)   
        insert_inventory_types = [
            (1, "Food", 0),
            (2, "Drink", 0),
            (3, "Object", 0),
            (4, "Others", 0),
            (5, 'Sandwich', 1),
            (6, 'Salad', 1),
            (7, 'Coffee', 2),
            (8, 'Fruit', 1),
            (9, 'Snack', 1),
            (10, 'Stationary', 2),
            (11, 'Soft drink', 2)
        ]     
        db_cursor.executemany("INSERT INTO inventory_type VALUES (?, ?, ?);", insert_inventory_types)

        # Create inventory table
        create_inv_table = """CREATE TABLE inventory(
            product_id INTEGER PRIMARY KEY,
            product_type_code INTEGER,
            product_name TEXT,
            product_price INTEGER,
            product_description TEXT,
            product_quantity INTEGER,
            FOREIGN KEY(product_type_code) REFERENCES inventory_type(type_id)
        );"""
        db_cursor.execute(create_inv_table)
        with open('./Inventory/inventory.csv', newline='') as inv_csvfile:
            inv_csvreader = csv.reader(inv_csvfile, delimiter = ',', quotechar = '|')
            is_first_row = True
            for inv_row in inv_csvreader:
                dummy_product_description = 'Netus cras Aliquam malesuada ad malesuada nostra id natoque posuere.'
                if is_first_row is True:
                    is_first_row = False
                else:
                    insert_inv_el = "INSERT INTO inventory VALUES (" + inv_row[0] + ", " + inv_row[1] + ", \"" + inv_row[2] + "\", " + inv_row[3] + ", \"" + dummy_product_description + "\", 5);"
                    db_cursor.execute(insert_inv_el)

        # Create active sessions table
        create_active_user_table = """CREATE TABLE active_session(
            session_id INTEGER PRIMARY KEY,
            user_id INTEGER
        );"""
        db_cursor.execute(create_active_user_table)

        # Create basket table
        create_basket_table = """CREATE TABLE basket(
            basket_id INTEGER PRIMARY KEY,
            basket_product_id INTEGER,
            basket_session_id INTEGER,
            basket_product_quantity INTEGER,
            FOREIGN KEY(basket_session_id) REFERENCES active_session(session_id)
            FOREIGN KEY(basket_product_id) REFERENCES inventory(product_id)
        );"""
        db_cursor.execute(create_basket_table)

        # DEBUG
        # print("All inventory elements:")
        # inv_data = db_cursor.execute("SELECT * FROM inventory;")
        # for row in inv_data:
        #     print(row)
        # print("All inventory types:")
        # inv_data = db_cursor.execute("SELECT * FROM inventory_type;")
        # for row in inv_data:
        #     print(row)

        # Close database
        db_connection.commit()
        db_connection.close()
        return None

    def get_inventory(self):
        db_connection = sqlite3.connect(self.db_path)
        db_cursor = db_connection.cursor()

        # DEBUG
        # db_cursor.execute("DELETE FROM inventory WHERE product_id = 18")

        total_inventory = db_cursor.execute("SELECT * FROM inventory;")
        total_inventory = total_inventory.fetchall()
        total_inventory_num = len(total_inventory)

        shelf_col_limit = 8
        shelf_row = 3
        # Replace total_inventory_num with total_typed_inventory_num to do nicer arrangerment
        shelf_col_min = math.ceil(total_inventory_num / shelf_row)

        if shelf_col_limit > shelf_col_min:
            shelf_col = shelf_col_limit
        else:
            shelf_col = shelf_col_min

        shelf_total = shelf_row * shelf_col
        shelf = np.empty((shelf_row, shelf_col), dtype=InventoryElement)
        # DEBUG
        # shelf_debug = np.empty((shelf_row, shelf_col))
        for index in range(shelf_total):
            row = index // shelf_col
            col = index % shelf_col
            if index < total_inventory_num:
                shelf[row, col] = InventoryElement(*total_inventory[index])
                # DEBUG
                # shelf_debug[row, col] = total_inventory[index][0]
            else:
                # Empty object
                shelf[row, col] = InventoryElement()
                # DEBUG
                # shelf_debug[row, col] = 0

        # Split shelf into pages (2d -> 3d)
        shelf_page = 2
        shelf = np.array(np.split(shelf, shelf_page, 1))

        # DEBUG
        # shelf_debug = np.array(np.split(shelf_debug, shelf_page, 1))
        # with np.printoptions(threshold = np.inf):
        #     print(shelf_debug)

        db_connection.close()
        return shelf

    def debug_inventory(self, shelf):
        shelf = np.array(np.concatenate(shelf, 1))
        for row in range(np.shape(shelf)[0]):
            for col in range(np.shape(shelf)[1]):
                print("%2d" % shelf[row, col].index, end = " ")
            print()

        return None

    def start_session(self, user_id):
        db_connection = sqlite3.connect(self.db_path)
        db_cursor = db_connection.cursor()

        # If there's no active session for the user, create a new one, otherwise pass
        has_active_session = db_cursor.execute("SELECT * FROM active_session WHERE user_id = " + str(user_id) + ";")
        if has_active_session.fetchall() == []:
            db_cursor.execute("INSERT INTO active_session (user_id) VALUES (" + str(user_id) + ");")

        # DEBUG
        # inv_data = db_cursor.execute("SELECT * FROM active_session;")
        # print(inv_data.fetchall())

        db_connection.commit()
        db_connection.close()
        return None

    def add_item_to_basket(self, product_id, user_id):
        db_connection = sqlite3.connect(self.db_path)
        db_cursor = db_connection.cursor()

        # Get session ID
        session_id = db_cursor.execute("SELECT session_id FROM active_session WHERE user_id = ?;", [(user_id)]).fetchone()[0]

        # Remove one from inventory table
        quantity = db_cursor.execute("SELECT product_quantity FROM inventory WHERE product_id = ?;", [(product_id)]).fetchone()[0]
        if quantity > 0:
            db_cursor.execute("UPDATE inventory SET product_quantity = ? WHERE product_id = ?;", [(quantity - 1), (product_id)])
            # Add one to inventory table
            item_in_basket = db_cursor.execute("SELECT basket_product_quantity FROM basket WHERE basket_product_id = ? AND basket_session_id = ?;", [(product_id), (session_id)]).fetchone()
            if item_in_basket is None:
                db_cursor.execute("INSERT INTO basket (basket_product_id, basket_session_id, basket_product_quantity) VALUES (?, ?, ?);", [(product_id), (session_id), (1)])
            else:
                basket_quantity = item_in_basket[0]
                db_cursor.execute("UPDATE basket SET basket_product_quantity = ? WHERE basket_product_id = ?;", [(basket_quantity + 1), (product_id)])
        else:
            warnings.warn("WARNING: Attempt to add item to basket when inventory is empty")

        # DEBUG
        # print("All inventory elements:")
        # inv_data = db_cursor.execute("SELECT * FROM inventory;")
        # for row in inv_data:
        #     print(row)
        # print("All basket elements:")
        # inv_data = db_cursor.execute("SELECT * FROM basket;")
        # for row in inv_data:
        #     print(row)

        db_connection.commit()
        db_connection.close()

    def return_item_to_inventory(self, user_id):
        db_connection = sqlite3.connect(self.db_path)
        db_cursor = db_connection.cursor()

        # Get session ID
        session_id = db_cursor.execute("SELECT session_id FROM active_session WHERE user_id = ?;", [(user_id)]).fetchone()[0]

        # Get session's basket content
        session_basket = db_cursor.execute("SELECT basket_product_id, basket_product_quantity FROM basket WHERE basket_session_id = ?", [(session_id)]).fetchall()
        if session_basket != []:
            # Delete from basket
            db_cursor.execute("DELETE FROM basket WHERE basket_session_id = ?", [(session_id)])

            # Add to inventory
            print(session_basket)
            for (index, quantity) in session_basket:
                inv_quantity = db_cursor.execute("SELECT product_quantity FROM inventory WHERE product_id = ?;", [(index)]).fetchone()[0]
                db_cursor.execute("UPDATE inventory SET product_quantity = ? WHERE product_id = ?;", [(inv_quantity + quantity), (index)])

        # DEBUG
        # print("All inventory elements:")
        # inv_data = db_cursor.execute("SELECT * FROM inventory;")
        # for row in inv_data:
        #     print(row)
        # print("All basket elements:")
        # inv_data = db_cursor.execute("SELECT * FROM basket;")
        # for row in inv_data:
        #     print(row)

class InventoryElement(object):
    def __init__(self, index = 0, type = -1, name = "n/a", price = 0, description = "n/a", quantity = 0):
        self.index = index
        self.name = name
        self.type = type
        self.price = price
        self.description = description
        self.quantity = quantity

    def debug(self):
        print(self.index)
        print(self.type)
        print(self.name)
        print(self.price)
        print(self.description)
        print(self.quantity)
    
if __name__ == '__main__':
    backend = Backend(r"./Database/susu_shop.db")
    backend.start_session(2)
    shelf = backend.get_inventory()
    # backend.debug_inventory(shelf)

    backend.add_item_to_basket(10, 2)
    backend.add_item_to_basket(1, 2)
    backend.add_item_to_basket(1, 2)

    backend.return_item_to_inventory(2)
    # DEBUG:
    os.remove("./Database/susu_shop.db")
