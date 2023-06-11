# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://waialys-default-rtdb.europe-west1.firebasedatabase.app/'  # Replace with your Firebase Realtime Database URL
})

# Get a reference to the Firebase Realtime Database
ref = db.reference()

user_ref = ref.child('user')
melangeur_ref = ref.child('melangeur')
colorant_ref = ref.child('colorant')
recette_ref = ref.child('recette')


@app.route('/adduser', methods=['POST'])
def create():
    """
        create() : Add data to Firebase Realtime Database with request body.
        Ensure you pass a custom ID as part of the JSON body in the POST request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        # Check if required fields are present in the JSON payload
        if 'id' not in request.json:
            return jsonify({"error": "Missing 'id' field"}), 400
        if 'nom' not in request.json:
            return jsonify({"error": "Missing 'nom' field"}), 400
        if 'prenom' not in request.json:
            return jsonify({"error": "Missing 'prenom' field"}), 400
        if 'matricule' not in request.json:
            return jsonify({"error": "Missing 'matricule' field"}), 400

        # Extract the required fields from the JSON payload
        id = request.json['id']
        nom = request.json['nom']
        prenom = request.json['prenom']
        matricule = request.json['matricule']

        # Set default values for optional fields
        presence = request.json.get('presence', 0)
        done = request.json.get('done', 0)
        error = request.json.get('error', 0)

        # Create a dictionary representing the user data
        user_data = {
            'nom': nom,
            'prenom': prenom,
            'matricule': matricule,
            'presence': presence,
            'done': done,
            'error': error
        }

        # Save the user data to the Firebase Realtime Database using the custom ID
        user_ref.child(id).set(user_data)

        return jsonify({"success": True}), 200
    except KeyError as e:
        missing_field = str(e)
        return jsonify({"error": f"Missing '{missing_field}' field"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getuser/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """
        get_user(user_id) : Retrieve user data from Firebase Realtime Database based on user ID.
    """
    try:
        user_data = user_ref.child(user_id).get()

        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/melangeur', methods=['GET', 'POST'])
def get_melangeur():
    """
        get_melangeur() : Retrieve all data from the "melangeur" location in Firebase Realtime Database.
    """
    if request.method == 'POST':
        try:
            # Extract the request data
            data = request.json

            # Iterate over the input fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('input', {}).items():
                melangeur_ref.child('input').child(key).set(value)

            # Iterate over the output fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('output', {}).items():
                melangeur_ref.child('output').child(key).set(value)

            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            melangeur_data = melangeur_ref.get()

            if melangeur_data:
                return jsonify(melangeur_data), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/colorant', methods=['GET', 'POST'])
def get_colorant():
    """
        get_colorant() : Retrieve all data from the "colorant" location in Firebase Realtime Database.
    """
    if request.method == 'POST':
        try:
            # Extract the request data
            data = request.json

            # Iterate over the input fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('input', {}).items():
                colorant_ref.child('input').child(key).set(value)

            # Iterate over the output fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('output', {}).items():
                colorant_ref.child('output').child(key).set(value)

            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            colorant_data = colorant_ref.get()

            if colorant_data:
                return jsonify(colorant_data), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/recette', methods=['GET', 'POST'])
def get_recette():
    """
        get_recette() : Retrieve all data from the "recette" location in Firebase Realtime Database.
    """
    if request.method == 'POST':
        try:
            # Extract the request data
            data = request.json

            # Iterate over the input fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('input', {}).items():
                recette_ref.child('input').child(key).set(value)

            # Iterate over the output fields and update the corresponding fields in the Firebase Realtime Database
            for key, value in data.get('output', {}).items():
                recette_ref.child('output').child(key).set(value)

            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            recette_data = recette_ref.get()

            if recette_data:
                return jsonify(recette_data), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
