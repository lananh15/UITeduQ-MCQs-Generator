# Đánh Giá Tổng Quan Mô Hình Chatbot Sinh Câu Hỏi Trắc Nghiệm Môn Quản Lý Dự Án Với Dữ Liệu Thô Lưu Trữ Trong Pinecone.
## ⚙️ Cài Đặt

### Cài Đặt rouge_score

```bash
pip install rouge_score
```

## 🧑‍💻 Sử Dụng

### Chuẩn Bị Tệp Văn Bản (TXT)

1. Tạo các câu hỏi được sinh ra từ 3 mô hình chatbot (ChatGPT, ClaudeAI, Gemini) với dữ liệu thô được lưu trữ trong Pinecone.
2. Lưu các câu hỏi này vào thư mục `quizzes-txt` dưới dạng tệp văn bản (TXT) tương ứng với từng mô hình:
   - Câu hỏi từ ChatGPT: `gpt_quizzes.txt`
   - Câu hỏi từ ClaudeAI: `claude_quizzes.txt`
   - Câu hỏi từ Gemini: `gemini_quizzes.txt`

### Chuẩn Bị Tệp JSON

1. Chạy tệp `txt2json.py` để chuyển đổi dữ liệu từ các tệp TXT sang tệp JSON.
2. Tệp JSON sẽ được lưu vào thư mục `quizzes-json` với tên mô hình tương ứng:
   - Tệp TXT của ChatGPT (`gpt_quizzes.txt`) sẽ chuyển thành `gpt_quizzes.json`
   - Tệp TXT của ClaudeAI (`claude_quizzes.txt`) sẽ chuyển thành `claude_quizzes.json`
   - Tệp TXT của Gemini (`gemini_quizzes.txt`) sẽ chuyển thành `gemini_quizzes.json`

### Đo Lường ROUGE

1. Chạy tệp `metric.py` để đo lường ROUGE cho các câu hỏi được sinh ra bởi 3 mô hình:
   - ChatGPT (`gpt_quizzes.json`)
   - ClaudeAI (`claude_quizzes.json`)
   - Gemini (`gemini_quizzes.json`)

```bash
python metric.py
```

2. Các kết quả như hình bên dưới sẽ cho biết điểm ROUGE từng bộ câu hỏi của mỗi mô hình, giúp bạn đánh giá và so sánh chất lượng của các mô hình chatbot trong việc sinh ra câu hỏi.  
![result](https://github.com/user-attachments/assets/5fe1cec1-fb9c-4caf-9237-9af15cf1e2d5)

