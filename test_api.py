import requests
import pytest

BASE_URL = "http://127.0.0.1:5000" 

kata_uji = {
    "Ancam": "ancas",
    "Basah": "kepos",
    "Entah": "embuh",
    "Enakan": "alung",
    "Enggan": "sungkan",
    "Akan": "arep",
    "Aku": "isun, sun, hun",
    "Bablas": "larad",
    "Balapan": "gyalapan",
    "Bagusan": "banguryan",
    "Bening": "kening",
    "Bibi": "bik",
    "Bedug": "jedhor",
    "Berhenti": "mandek",
    "Berhubung": "sarehne",
    "Betah": "pernah",
    "Bekas": "lungsuran",
    "Ingkar": "suloyo",
    "Ingat": "eleng, iling",
    "Ibu": "mak",
    "Istri": "rabi",
    "Impas": "pakpok",
    "Injak": "idek"
}

# Test Case 1: Memastikan endpoint /translate berhasil untuk kata yang ada
@pytest.mark.parametrize("osing, indonesia", kata_uji.items())
def test_translate_from_osing_success(osing, indonesia):
    """Menguji terjemahan Osing -> Indonesia untuk kata yang valid."""
    # Data yang akan dikirim ke API
    payload = {"text": osing, "fromOsing": True}
    
    # Kirim request POST ke server
    response = requests.post(f"{BASE_URL}/translate", json=payload)
    
    # Verifikasi (Assertion)
    assert response.status_code == 200  # Pastikan status response adalah 200 OK
    response_json = response.json()
    assert "text" in response_json     # Pastikan ada 'key' "text" di response
    assert response_json["text"] == indonesia # Pastikan hasil terjemahannya benar

# Test Case 2: Memastikan endpoint mengembalikan pesan 'tidak ditemukan' untuk kata yang tidak ada
def test_translate_word_not_found():
    """Menguji terjemahan untuk kata yang tidak ada di kamus."""
    payload = {"text": "katayangpastiasing", "fromOsing": True}
    response = requests.post(f"{BASE_URL}/translate", json=payload)
    
    assert response.status_code == 200
    # Pastikan respons mengandung pesan 'tidak ditemukan'
    assert "tidak ditemukan" in response.json()["text"]

# Test Case 3: Memastikan request tanpa 'text' akan gagal
def test_translate_bad_request():
    """Menguji request dengan format yang salah (tanpa 'text')."""
    payload = {"fromOsing": True} # Tidak ada key "text"
    response = requests.post(f"{BASE_URL}/translate", json=payload)
    
    # API harus mengembalikan error 400 Bad Request
    assert response.status_code == 400