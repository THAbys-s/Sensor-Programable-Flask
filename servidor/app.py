import sqlite3
from flask import Flask, request, g, jsonify, url_for
from math import ceil

app = Flask(__name__)

resultados_por_pag = 10

def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}

def abrirConexion():
  if 'db' not in g:
     g.db = sqlite3.connect("valores_api.sqlite")
     g.db.row_factory = dict_factory
  return g.db

def cerrarConexion(e=None):
   db = g.pop('db', None)
   if db is not None:
       db.close()


@app.route("/")
def hello_world():
     return "<p>Hello, World!</p>"

@app.route("/api/sensor", methods=['POST'])
def sensor():
    db = abrirConexion()
    datos = request.json
    nombre = datos['nombre']
    valor = datos['valor']

    print(f"Nombre: {nombre}, Valor: {valor}")
    db.execute("""INSERT INTO tabla_ejemplo (nombre, valor)
                  VALUES (?, ?)""", (nombre, valor))
    db.commit()
    cerrarConexion()
    
    res = {'resultado': 'ok'}

    return jsonify(res)


@app.route("/api/sensor/<int:id>")
def sensor_valor(id):
   db = abrirConexion()
   cursor = db.execute("""SELECT id, nombre FROM tabla_ejemplo
                           WHERE id = ?""", (id,))
   fila = cursor.fetchone()
   cerrarConexion()
   if fila == None:
      return f"Persona inexistente (id: {id})", 404
   res = {'id' : fila['id'],
          'nombre': fila['nombre'],
          'url': url_for('valores_ejemplo', id=id, _external=True)}
   return jsonify(res)


@app.route("/api/sensor/pagina")
def paginado_sensor():
    args = request.args
    pagina = int(args.get('page', '1'))
    descartar = (pagina-1) * resultados_por_pag
    db = abrirConexion()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS cant FROM tabla_ejemplo;")
    cant = cursor.fetchone()['cant']
    paginas = ceil(cant / resultados_por_pag)

    if pagina < 1 or pagina > paginas:
       return f"Página inexistente: {pagina}", 400

    cursor.execute(""" SELECT id, nombre 
                        FROM tabla_ejemplo LIMIT ? OFFSET ?; """, 
                        (resultados_por_pag,descartar))
    lista = cursor.fetchall()
    cerrarConexion()
    siguiente = None
    anterior = None
    if pagina > 1:
       anterior = url_for('', page=pagina-1, _external=True)
    if pagina < paginas:
       siguiente = url_for('sensor', page=pagina+1, _external=True)
    info = { 'count' : cant, 'pages': paginas,
             'next' : siguiente, 'prev' : anterior }
    res = { 'info' : info, 'results' : lista}
    return jsonify(res)