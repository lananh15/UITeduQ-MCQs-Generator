import json
from rouge_score import rouge_scorer

def read_json_file(filename):
    print(f"Đang đọc file: {filename}")  # Debug print
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    content = ""
    for quiz in data['quizzes']:
        content += quiz['quiz_question'] + "\n"
        content += "\n".join(quiz['options']) + "\n\n"
    return content.strip()

def read_txt_file(filename):
    print(f"Đang đọc file: {filename}")  # Debug print
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Đọc nội dung từ file TXT (dữ liệu thô)
txt_content = read_txt_file('../generate-quizzes-chatbot/data/qtda_raw.txt')

# Danh sách các file JSON và tên mô hình tương ứng
json_files = [
    ('../generate-quizzes-chatbot/evaluate/pinecone-with-raw-data/quizzes-json/gpt_quizzes.json', 'ChatGPT'),
    ('../generate-quizzes-chatbot/evaluate/pinecone-with-raw-data/quizzes-json/claude_quizzes.json', 'Claude'),
    ('../generate-quizzes-chatbot/evaluate/pinecone-with-raw-data/quizzes-json/gemini_quizzes.json', 'Gemini')
]

# Tạo đối tượng tính toán ROUGE
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Tính và in điểm ROUGE cho từng mô hình
for json_file, model_name in json_files:
    print(f"\nĐang xử lý mô hình: {model_name}")  # Debug print
    json_content = read_json_file(json_file)
    scores = scorer.score(txt_content, json_content)
    
    print(f"Kết quả ROUGE cho {model_name}:")
    print(f"ROUGE-1: {scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2: {scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L: {scores['rougeL'].fmeasure:.4f}")