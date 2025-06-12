from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def muat_dan_proses_kamus(file_path='kamus.json'):
    kamus_indo_ke_osing = {}
    kamus_osing_ke_indo = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_kamus_asli = json.load(f)

        # 1. Membuat kamus Indo -> Osing yang case-insensitive
        for kunci, nilai in data_kamus_asli.items():
            kamus_indo_ke_osing[kunci.lower()] = nilai.split(',')[0].strip()

        # 2. Membuat kamus Osing -> Indo secara otomatis
        for kunci_indo, nilai_osing in kamus_indo_ke_osing.items():
            # Jika ada beberapa padanan kata (dipisah koma), kita ambil yang pertama
            kata_osing_utama = nilai_osing.lower()
            if kata_osing_utama not in kamus_osing_ke_indo:
                kamus_osing_ke_indo[kata_osing_utama] = kunci_indo

        print(f"Kamus berhasil dimuat dan diproses dari {file_path}")
        return kamus_indo_ke_osing, kamus_osing_ke_indo

    except FileNotFoundError:
        print(f"ERROR: File {file_path} tidak ditemukan. Menggunakan kamus kosong.")
        return {}, {}
    except Exception as e:
        print(f"Terjadi error saat memuat kamus: {e}")
        return {}, {}

# Muat kamus saat aplikasi pertama kali berjalan
kamus_indo_osing, kamus_osing_indo = muat_dan_proses_kamus()


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    input_text = data.get('text', '').lower().strip()
    from_osing = data.get('fromOsing', True)

    print(f"Menerima teks: '{input_text}', Arah: {'Osing -> Indo' if from_osing else 'Indo -> Osing'}")

    translated_text = ""
    # 3. Gunakan kamus yang sesuai berdasarkan flag 'fromOsing'
    if from_osing:
        # Menerjemahkan dari Bahasa Osing ke Bahasa Indonesia
        translated_text = kamus_osing_indo.get(input_text, f"'{input_text}' tidak ditemukan di kamus Osing")
    else:
        # Menerjemahkan dari Bahasa Indonesia ke Bahasa Osing
        translated_text = kamus_indo_osing.get(input_text, f"'{input_text}' tidak ditemukan di kamus Indonesia")

    response_data = {
        "text": translated_text,
        "confidence": 0.98
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)