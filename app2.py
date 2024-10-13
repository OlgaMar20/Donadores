from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__, template_folder='templetes')

# Configuración de la conexión a PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'railway'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'ZabAclIwcqEYJYyiJPMbqOyeuEIzJmkK'),
            host=os.getenv('DB_HOST', 'postgres.railway.internal'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    tipo_sangre = request.args.get('tipo_sangre')
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with conn.cursor() as cur:
            # Consulta a la base de datos
            cur.execute('''
                SELECT nombre, tipo_sangre, latitud, longitud
                FROM usuarios
                WHERE tipo_sangre = %s
            ''', (tipo_sangre,))

            donantes = cur.fetchall()

            # Convertir los resultados a formato JSON
            resultados = [
                {
                    'nombre': donante[0],
                    'tipo_sangre': donante[1],
                    'latitud': donante[2],
                    'longitud': donante[3]
                }
                for donante in donantes
            ]

    except psycopg2.Error as e:
        return jsonify({'error': f'Database query failed: {e}'}), 500
    finally:
        conn.close()

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
