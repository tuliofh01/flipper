import sqlite3
import string
import random

# Function to generate unique codes
def generateUniqueCodes(columnLength):
    allAsciiChars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    codeSet = set()
    codes = []

    while len(codes) < columnLength:
        auxString = ""
        for _ in range(6):
            auxString += random.choice(allAsciiChars)

        if auxString not in codeSet:
            codeSet.add(auxString)
            codes.append(auxString)

    return codes

# Specify the desired column length (e.g., 50000 for 50,000 unique codes)
columnLength = 50000

# Generate two columns of unique codes
column1 = generateUniqueCodes(columnLength)
column2 = generateUniqueCodes(columnLength)

# Create a SQLite database and connect to it
conn = sqlite3.connect('../assets/database.db')
cursor = conn.cursor()

# Create a "codes" table with columns code1, code2, and date
cursor.execute('''
    CREATE TABLE codes (
        code1 TEXT UNIQUE,
        code2 TEXT UNIQUE,
        date DATETIME
    )
''')

# Insert data into the "codes" table with the date column initialized as NULL
for code1, code2 in zip(column1, column2):
    cursor.execute('INSERT INTO codes (code1, code2, date) VALUES (?, ?, NULL)',
                   (code1, code2))

# Commit the changes and close the database connection
conn.commit()
conn.close()
