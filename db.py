import sqlite3


connection = sqlite3.connect('amul.db')

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY, 
    name TEXT, 
    quantity INTEGER,
    available INTEGER
)
""")
'''
values = [('6707b8bbc52548002b77284c', 'Amul Kool Protein Milkshake | Kesar, 180 mL | Pack of 30', 11, 1),
          ('651d0d19e8ac81a61d2d70b5',
           'Amul High Protein Blueberry Shake, 200 mL | Pack of 30', 821, 1),
          ('680a084bbbe4c5003e328a07',
           'Amul Kool Protein Milkshake | Arabica Coffee, 180 mL | Pack of 8', 0, 0),
          ('680a09192d0f920024bfeb8a',
           'Amul Kool Protein Milkshake | Kesar, 180 mL | Pack of 8', 0, 0),
          ('67581f01324dd1002b57c776',
           'Amul Kool Protein Milkshake | Chocolate, 180 mL | Pack of 30', 9, 0),
          ('6636020d5c0420e92d79ebdd',
           'Amul High Protein Paneer, 400 g | Pack of 2', 0, 0),
          ('667bb533dedd432ff59d8dc3',
           'Amul High Protein Paneer, 400 g | Pack of 24', 9, 0),
          ('67110d0a2db6df00243e660e',
           'Amul Whey Protein Gift Pack, 32 g | Pack of 10 sachets', 8, 0),
          ('6523d849dfbc5f6c6222d9c8',
           'Amul Whey Protein, 32 g | Pack of 30 Sachets', -2, 0),
          ('66192d8e9fd1739d5b99ee7b',
           'Amul Whey Protein, 32 g | Pack of 60 Sachets', 0, 0),
          ('6775370db3ace500bdf1ddbc',
           'Amul Chocolate Whey Protein Gift Pack, 34 g | Pack of 10 sachets', 0, 0),
          ('666d72e43f9749cf28eff026',
           'Amul Chocolate Whey Protein, 34 g | Pack of 30 sachets', 0, 0),
          ('676d4b585a4549003e2ee4e9',
           'Amul Chocolate Whey Protein, 34 g | Pack of 60 sachets', 0, 0),
          ('66bcad006760c5002bc81922',
           'Amul High Protein Plain Lassi, 200 mL | Pack of 30', -5, 0),
          ('63410e732677af79f687339b',
           'Amul High Protein Buttermilk, 200 mL | Pack of 30', 2, 0),
          ('651d0a21e8ac81a61d2d1a74',
           'Amul High Protein Rose Lassi, 200 mL | Pack of 30', -4, 0),
          ('6662a0bc04f4cdcc138d3ae3',
           'Amul High Protein Milk, 250 mL | Pack of 8', 0, 0),
          ('66604f96d4be68c55752933c',
           'Amul High Protein Milk, 250 mL | Pack of 32', 6, 0)
          ]


cursor.executemany("""
INSERT INTO items VALUES(?,?,?,?)
               """, values)
'''

cursor.execute("SELECT * FROM items where available = 1")

print(cursor.fetchall())

connection.commit()

connection.close()
