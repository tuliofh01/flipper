import sqlite3
from datetime import datetime

# Connect to the SQLite database
database_path = "../assets/database.db"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

def update_date(code1):
    try:
        # Get the current datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve the value of 'code2' based on 'code1'
        cursor.execute("SELECT code2 FROM your_table WHERE code1 = ?", (code1))
        row = cursor.fetchone()

        if row:
            code2_value = row[0]

            # Update the 'date' column with the current datetime
            cursor.execute("UPDATE codes SET date = ? WHERE code1 = ?", (current_datetime, code1))
            connection.commit()

            print(f"Valor de 'código 2' para 'código 1' {code1}: {code2_value}")
        else:
            print(f"Nenhum código encontrado, confira erros de digitação.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    code1_input = input("Insira o código a ser correspondido: ")
    update_date(code1_input)
    input("Aperte ENTER para sair.")
