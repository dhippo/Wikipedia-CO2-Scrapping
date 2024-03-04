import os
import mysql.connector

def enregistrer_en_bdd(structured_data):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), 
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emissions_by_country")
    row_count = cursor.fetchone()[0]

    if row_count > 20:
        print("Données déjà complétées en base de données")
    else:
        insert_query = "INSERT INTO emissions_by_country (country_name, territorial_approach, territorial_approach_by_inhabitant, consumption_approach) VALUES (%s, %s, %s, %s)"
        for row in structured_data:
            cursor.execute(insert_query, row)
        conn.commit()
        print("Insertion réussie.")

    cursor.close()
    conn.close()
