from flask import Flask, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

NAMA_MODEL_LOKAL = './models/model-indonesia-ke-osing'
print("Memuat model terjemahan...")
try:
    device = 0 if torch.cuda.is_available() else -1 
    translator = pipeline(
        "translation", 
        model=NAMA_MODEL_LOKAL, 
        tokenizer=NAMA_MODEL_LOKAL,
        device=device
    )
    print("Model berhasil dimuat.")
except Exception as e:
    print(f"Error saat memuat model: {e}")
    translator = None

@app.route('/translate', methods=['POST'])
def translate_text():
    if not translator:
        return jsonify({"error": "Model tidak tersedia atau gagal dimuat."}), 500

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    input_text = data.get('text', '')
    # Untuk saat ini, kita hanya mendukung Indo -> Osing
    # Flag fromOsing bisa diabaikan atau digunakan untuk validasi
    from_osing = data.get('fromOsing', False) 

    if from_osing:
        return jsonify({"error": "Terjemahan Osing ke Indonesia belum diimplementasikan."}), 400

    print(f"Menerima teks untuk diterjemahkan: '{input_text}'")

    try:
        # Melakukan terjemahan menggunakan pipeline
        result = translator(input_text, max_length=128)
        translated_text = result[0]['translation_text']
        
        print(f"Hasil terjemahan: '{translated_text}'")

        response_data = {
            "text": translated_text,
            "confidence": None
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"Error saat melakukan terjemahan: {e}")
        return jsonify({"error": "Terjadi kesalahan internal saat menerjemahkan."}), 500


if __name__ == '__main__':
    # host='0.0.0.0' agar bisa diakses dari luar container/VM
    app.run(host='0.0.0.0', port=5000, debug=False)