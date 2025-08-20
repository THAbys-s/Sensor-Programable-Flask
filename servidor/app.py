import sqlite3
from flask import Flask, request, g, jsonify, url_for

app = Flask(__name__)

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
