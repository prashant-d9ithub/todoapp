from mysql.connector import connect

# Database Connection code
try:
    conn = connect(host="localhost", user="root", password="", database="test_fastapi")
    cursor = conn.cursor()

    # Create the 'todos' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS todo (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(120) NOT NULL)''')
    conn.commit()
    cursor.close()

except Exception as e:
    print(f'Error : {e}')
