from flask import Flask, jsonify, request

app = Flask(__name__)

data = [
    {
        "id": 1,
        "titulo": "Naruto",
        "puntaje": 9,
        "tipo": "Serie",
        "season": "2",
        "generos": ["Accion", "Aventura"]
    },
    {
        "id": 2,
        "titulo": "Shingeki no Kyojin",
        "puntaje": 10,
        "tipo": "Serie",
        "season": "1",
        "generos": ["Accion", "Fantasia","Drama"]
    },
    {
        "id": 3,
        "titulo": "Death Note",
        "puntaje": 9,
        "tipo": "Serie",
        "season": "1",
        "generos": ["Misterio", "Thriller"]
    }
]

# GET 
@app.route('/anime', methods=['GET'])
def get_anime():
    return jsonify({'anime': data})

# GET id
@app.route('/anime/<int:anime_id>', methods=['GET'])
def get_anime_id(anime_id):
    anime = next((item for item in data if item['id'] == anime_id), None)
    if anime is None:
        return jsonify({'error': 'Anime no encontrado'}), 404
    return jsonify({'anime': anime})

# POST 

def anime_existe(id, titulo):
    return any(anime['id'] == id or anime['titulo'] == titulo for anime in data)

@app.route('/anime', methods=['POST'])
def crear_anime():
    nuevo = request.json
    if anime_existe(nuevo['id'], nuevo['titulo']):
        return jsonify({'error': 'El anime ya existe'}), 400

    data.append(nuevo)
    return jsonify({'mensaje': 'Anime creado correctamente'}), 201

# PUT id 

def anime_exists(key, value):
    return next((item for item in data if item[key] == value), None)

@app.route('/anime/<int:anime_id>', methods=['PUT'])
def update_anime(anime_id):
    anime = next((item for item in data if item['id'] == anime_id), None)
    if anime is None:
        return jsonify({'error': 'Anime no encontrado'}), 404

    campos_requeridos = ['id', 'titulo', 'puntaje', 'tipo', 'season', 'generos']
    actualizar_data = request.json

    if not all(field in actualizar_data for field in campos_requeridos):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    anime.update(actualizar_data)
    return jsonify({'mensaje': 'Anime actualizado correctamente'})

# PATCH id
@app.route('/anime/<int:anime_id>', methods=['PATCH'])
def patch_anime(anime_id):
    anime = next((item for item in data if item['id'] == anime_id), None)
    if anime is None:
        return jsonify({'error': 'Anime no encontrado'}), 404
    actualizar_anime = request.json
    anime.update(actualizar_anime)
    return jsonify({'mensaje': 'Anime actualizado correctamente'})

# DELETE id
@app.route('/anime/<int:anime_id>', methods=['DELETE'])
def delete_anime(anime_id):
    anime = next((item for item in data if item['id'] == anime_id), None)
    if anime is None:
        return jsonify({'error': 'Anime no encontrado'}), 404
    data.remove(anime)
    return jsonify({'mensaje': 'Anime eliminado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
