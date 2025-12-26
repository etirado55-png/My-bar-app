import sqlite3

def connect_db():
    conn = sqlite3.connect("bar_data.db", check_same_thread=False)
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    # Table for recipes
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes 
                      (id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT, 
                       instructions TEXT, image_url TEXT)''')
    # Table for inventory
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory 
                      (ingredient TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()

def add_recipe(name, ingredients, instructions, image_url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (name, ingredients, instructions, image_url) VALUES (?, ?, ?, ?)",
                   (name, ingredients, instructions, image_url))
    conn.commit()
    conn.close()

def update_inventory(selected_ingredients):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory") # Clear current
    for item in selected_ingredients:
        cursor.execute("INSERT INTO inventory (ingredient) VALUES (?)", (item,))
    conn.commit()
    conn.close()

def get_available_drinks():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get what you have
    cursor.execute("SELECT ingredient FROM inventory")
    my_inventory = set(row[0].lower() for row in cursor.fetchall())
    
    # Get all recipes
    cursor.execute("SELECT * FROM recipes")
    all_recipes = cursor.fetchall()
    
    available = []
    for recipe in all_recipes:
        # Split string of ingredients and check against inventory
        recipe_reqs = set(i.strip().lower() for i in recipe[2].split(','))
        if recipe_reqs.issubset(my_inventory):
            available.append(recipe)
            
    conn.close()
    return available