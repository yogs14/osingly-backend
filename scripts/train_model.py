import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

# --- 1. KONFIGURASI ---
# Model dasar yang akan kita fine-tune. Model ini sudah mengerti Bahasa Indonesia.
MODEL_DASAR = "Helsinki-NLP/opus-mt-id-en" 
NAMA_FILE_KORPUS = "../data/korpus_paralel.csv"
NAMA_MODEL_OUTPUT = "model-indonesia-ke-osing"
# Prefix yang dibutuhkan oleh beberapa model T5/BART. Untuk MarianMT, bisa string kosong.
PREFIX = "" 

print("--- Memulai Proses Pelatihan Model ---")

# --- 2. MEMUAT DAN MEMPROSES DATA ---
print(f"1. Memuat korpus dari {NAMA_FILE_KORPUS}...")
df = pd.read_csv(NAMA_FILE_KORPUS)
dataset = Dataset.from_pandas(df)

train_test_split = dataset.train_test_split(test_size=0.1)
dataset_dict = DatasetDict({
    'train': train_test_split['train'],
    'eval': train_test_split['test']
})
print("Dataset berhasil dimuat dan dibagi:")
print(dataset_dict)

# --- 3. TOKENISASI ---
print(f"\n2. Memuat tokenizer dari model dasar '{MODEL_DASAR}'...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DASAR)

def preprocess_function(examples):
    """Fungsi untuk mentokenisasi teks input dan target"""
    inputs = [PREFIX + doc for doc in examples["indonesia"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

    # Tokenisasi target (label)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["osing"], max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

print("Melakukan tokenisasi pada dataset...")
tokenized_datasets = dataset_dict.map(preprocess_function, batched=True)
print("Tokenisasi selesai.")


# --- 4. PELATIHAN (FINE-TUNING) ---
print(f"\n3. Memuat model dasar '{MODEL_DASAR}' untuk fine-tuning...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DASAR)

training_args = Seq2SeqTrainingArguments(
    output_dir=NAMA_MODEL_OUTPUT,
    eval_strategy="epoch",          
    learning_rate=2e-5,             
    
    per_device_train_batch_size=1,  
    per_device_eval_batch_size=1,   
    gradient_accumulation_steps=4,  
    fp16=True,                      
    
    num_train_epochs=5,             
    logging_steps=100,              
    
    weight_decay=0.01,
    save_total_limit=3,
    predict_with_generate=True,
    push_to_hub=False,
)

# Data collator untuk membuat batch data secara dinamis
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

# Membuat instance Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["eval"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

print("\n4. Memulai fine-tuning model...")
trainer.train()
print("Pelatihan selesai.")


# --- 5. MENYIMPAN MODEL ---
print(f"\n5. Menyimpan model dan tokenizer ke folder '{NAMA_MODEL_OUTPUT}'...")
trainer.save_model(NAMA_MODEL_OUTPUT)
tokenizer.save_pretrained(NAMA_MODEL_OUTPUT)
print("--- Proses Selesai ---")