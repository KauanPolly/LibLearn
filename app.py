import base64
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Carregar os quatro modelos
model_am = tf.keras.models.load_model('AD.h5')
model_ny = tf.keras.models.load_model('NR.h5')
model_numbers = tf.keras.models.load_model('1-4.h5')
model_semi_movimento = tf.keras.models.load_model('semim.h5')  # Novo modelo para J, H, X, Z

# Rótulos que correspondem às classes do modelo
labels_am = ['A', 'B', 'C', 'D']  # Para AMf.h5
labels_ny = ['N', 'O', 'P', 'R'] 
labels_numbers = ['1', '2', '3', '4']  # Para numerosf.h5
labels_semi_movimento = ['J', 'H', 'X', 'Z']  # Para semim.h5

# Função para processar a imagem recebida e preparar para o modelo
def preprocess_image(image_data):
    if "data:image" in image_data:
        image_data = image_data.split(",")[1]
    
    try:
        img = Image.open(BytesIO(base64.b64decode(image_data)))

        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            raise ValueError(f"Modo de imagem inesperado: {img.mode}")

        img = img.resize((224, 224))  # Ajuste conforme o esperado pelos modelos
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar
        return img_array
    except Exception as e:
        raise ValueError(f"Erro ao processar a imagem: {str(e)}")

# Rota para servir a página HTML principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para receber a imagem e fazer a previsão
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        image_data = data.get('image')
        model_type = data.get('model', 'AM')  # Padrão para o modelo A-M

        if not image_data:
            return jsonify({'error': 'Nenhuma imagem fornecida.'}), 400

        processed_image = preprocess_image(image_data)

        # Escolher o modelo correto com base no botão selecionado
        if model_type == 'AM':
            predictions = model_am.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = labels_am[predicted_class_index]
        elif model_type == 'NY':
            predictions = model_ny.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = labels_ny[predicted_class_index]
        elif model_type == 'Num':
            predictions = model_numbers.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = labels_numbers[predicted_class_index]
        elif model_type == 'SemiMovimento':  # Novo modelo
            predictions = model_semi_movimento.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = labels_semi_movimento[predicted_class_index]
        else:
            return jsonify({'error': 'Modelo desconhecido.'}), 400

        # Retornar o resultado da previsão
        return jsonify({'result': predicted_class_label})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
