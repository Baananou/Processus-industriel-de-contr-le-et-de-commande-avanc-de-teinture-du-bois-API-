# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db
from flask_cors import CORS, cross_origin

# Initialize Flask app
app = Flask(__name__)
CORS(app)

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


@app.route('/user', methods=['GET'])
@cross_origin()
def get_user():
    """
    get_user() : Retrieve all data from the "user" location in Firebase Realtime Database.
    """
    try:
        args = request.args
        user_data = user_ref.get()

        if user_data:
            if 'read' in args:
                read_value = user_data.get('READ', {}).get(args['read'])
                return jsonify({"value": read_value}), 200

            if 'write' in args:
                write_value = user_data.get('WRITE', {}).get(args['write'])
                return jsonify({"value": write_value}), 200

            return jsonify(user_data), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user', methods=['POST'])
@cross_origin()
def update_user():
    """
    update_user() : Update data in the "user" location in Firebase Realtime Database.
    """
    try:
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')
        child = data.get('child')

        if key and value and child:
            if child.lower() == 'read':
                # Update the value of the specified key in the "READ" property
                user_ref.child('READ').update({key: value})
            elif child.lower() == 'write':
                # Update the value of the specified key in the "WRITE" property
                user_ref.child('WRITE').update({key: value})
            else:
                return jsonify({"error": "Invalid 'child' value"}), 400

            return jsonify({"message": "Value updated successfully"}), 200
        else:
            return jsonify({"error": "Invalid request body"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/melangeur', methods=['GET'])
@cross_origin()
def get_melangeur():
    """
    get_melangeur() : Retrieve all data from the "melangeur" location in Firebase Realtime Database.
    """
    try:
        args = request.args
        melangeur_data = melangeur_ref.get()

        if melangeur_data:
            if 'input' in args:
                input_value = melangeur_data.get('input', {}).get(args['input'])
                return jsonify({"value": input_value}), 200

            if 'output' in args:
                output_value = melangeur_data.get('output', {}).get(args['output'])
                return jsonify({"value": output_value}), 200

            return jsonify(melangeur_data), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/melangeur', methods=['POST'])
@cross_origin()
def post_melangeur():
    """
    post_melangeur() : Update data in the "melangeur" location in Firebase Realtime Database.
    """
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


@app.route('/colorant', methods=['GET'])
@cross_origin()
def get_colorant():
    """
    get_colorant() : Retrieve all data from the "colorant" location in Firebase Realtime Database.
    """
    try:
        args = request.args
        colorant_data = colorant_ref.get()

        if colorant_data:
            if 'input' in args:
                input_value = colorant_data.get('input', {}).get(args['input'])
                return jsonify({"value": input_value}), 200

            if 'output' in args:
                output_value = colorant_data.get('output', {}).get(args['output'])
                return jsonify({"value": output_value}), 200

            return jsonify(colorant_data), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/colorant', methods=['POST'])
@cross_origin()
def post_colorant():
    """
    post_colorant() : Update data in the "colorant" location in Firebase Realtime Database.
    """
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

@app.route('/recette', methods=['GET'])
@cross_origin()
def get_recette():
    """
    get_recette() : Retrieve all data from the "recette" location in Firebase Realtime Database.
    """
    try:
        args = request.args
        recette_data = recette_ref.get()

        if recette_data:
            if 'input' in args:
                input_value = recette_data.get('input', {}).get(args['input'])
                return jsonify({"value": input_value}), 200

            if 'output' in args:
                output_value = recette_data.get('output', {}).get(args['output'])
                return jsonify({"value": output_value}), 200

            return jsonify(recette_data), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recette', methods=['POST'])
@cross_origin()
def post_recette():
    """
    post_recette() : Update data in the "recette" location in Firebase Realtime Database.
    """
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


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
