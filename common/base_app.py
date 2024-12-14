from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os

class QuizzSearchAppBase:
    def __init__(self, llm_handler):
        self.app = Flask(__name__, template_folder='../common/templates', static_folder='../common/static')
        CORS(self.app)
        self.llm_handler = llm_handler
        
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/chat', 'chat', self.chat, methods=['POST'])

    def index(self):
        return render_template('index.html')

    def chat(self):
        message = request.form['message']

        if message.lower() == 'chương hỗ trợ':
            return self._handle_chapter_structure()
        elif message.lower().startswith('keyword:'):
            return self._handle_questions_with_keyword(message, 15)
        
        elif message.lower() == 'mode':
            return jsonify({"response": f"Chế độ hiện tại: {self.llm_handler.get_mode()}"})
        elif message.lower() == 'mode: chatgpt':
            self.llm_handler.set_mode("ChatGPT")
            return jsonify({"response": "Đã chuyển sang chế độ: ChatGPT"})
        elif message.lower() == 'mode: gemini':
            self.llm_handler.set_mode("Gemini")
            return jsonify({"response": "Đã chuyển sang chế độ: Gemini"})
        elif message.lower() == 'mode: claude':
            self.llm_handler.set_mode("Claude")
            return jsonify({"response": "Đã chuyển sang chế độ: Claude"})
        elif message.lower() == 'reset mode':
            self.llm_handler.set_mode("ChatGPT")
            return jsonify({"response": ""})
        else:
            return jsonify({"response": "Cú pháp không hợp lệ. Vui lòng thử lại."})

    def _handle_chapter_structure(self):
        raise NotImplementedError
    
    def find_excel_file(self, filename):
        for root, dirs, files in os.walk('/'):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def _handle_questions(self, message, question_type, max_questions):
        raise NotImplementedError

    # Hàm xử lý và sinh câu hỏi dựa trên keyword (chỉ dùng cho pinecone với raw data)
    def _handle_questions_with_keyword(self, message, max_questions):
        raise NotImplementedError
    
    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=5000)