import json
import re
import os

# Đọc dữ liệu từ file .txt (model là tên model sinh ra quizz)
input_file = '../generate-quizzes-chatbot/evaluate/pinecone-with-raw-data/quizzes-txt/model_quizzes.txt'
with open(input_file, encoding='utf-8') as file:
    content = file.read()

# Tách các câu hỏi
questions = re.split(r'\d+\.\s*Câu hỏi:', content)[1:]

# Tạo danh sách để lưu các câu hỏi và tùy chọn
quizzes = []

for question in questions:
    # Tách câu hỏi và các lựa chọn
    parts = question.split('\n')
    
    # Lấy nội dung câu hỏi
    quiz_question = parts[0].strip()
    
    # Lấy các lựa chọn
    options = []
    for part in parts[1:]:
        if part.startswith(('A.', 'B.', 'C.', 'D.')):
            options.append(part[2:].strip())
    
    # Thêm câu hỏi vào danh sách
    quizzes.append({
        "quiz_question": quiz_question,
        "options": options
    })

# Tạo cấu trúc JSON
data = {
    "quizzes": quizzes
}

# Xác định đường dẫn đầu ra
output_dir = '../generate-quizzes-chatbot/evaluate/pinecone-with-raw-data/quizzes-json'
output_file = os.path.join(output_dir, 'model_quizzes.json')

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(output_dir, exist_ok=True)

# Ghi dữ liệu vào file .json
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Dữ liệu đã được lưu vào {output_file}")