from common.handlers.gemini_handler import GeminiHandler
from common.handlers.gpt_handler import GPTHandler
from common.handlers.claude_handler import ClaudeHandler
import tiktoken
from typing import List

class LLMHandlerBase:
    def __init__(self, openai_api_key, google_api_key, anthropic_api_key):
        self.gpt_handler = GPTHandler(openai_api_key) # khởi tạo đối tượng của lớp GPTHandler
        self.gemini_handler = GeminiHandler(google_api_key) # khởi tạo đối tượng của lớp GeminiHandler
        self.anthropic_handler = ClaudeHandler(anthropic_api_key) # khởi tạo đối tượng của lớp ClaudeHandler
        self.current_mode = "ChatGPT"

    # cập nhật LLM theo người dùng chọn
    def set_mode(self, mode: str):
        self.current_mode = mode

    def get_mode(self):
        return self.current_mode

    # Khởi tạo dùng LLM tương ứng với chế độ hiện tại người dùng dùng
    def get_llm(self):
        if self.current_mode == "ChatGPT":
            return self.gpt_handler
        elif self.current_mode == "Gemini":
            return self.gemini_handler
        elif self.current_mode == "Claude":
            return self.anthropic_handler

    # Gửi toàn bộ nội dung tìm được cho LLM
    def _generate_questions_direct(self, content: str, num_questions: int) -> List[str]:
        llm = self.get_llm()
        # bạn có thể bỏ comment dòng phía dưới để in ra tên model được dùng để sinh quizz
        # print(f"\nModel được dùng: {llm}")
        prompt = self._build_prompt(num_questions, content)
        response = llm.invoke(prompt)
        questions = response.content.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

    def _build_prompt(self, num_questions: int, content: str) -> str:
        return f"""Tạo {num_questions} câu hỏi trắc nghiệm dựa trên nội dung sau. Tuân thủ các quy tắc sau:
        1. Mỗi câu hỏi bắt đầu bằng "Câu hỏi:" (không có số).
        2. Sau "Câu hỏi:" là nội dung đầy đủ của câu hỏi.
        3. Mỗi câu hỏi có 4 lựa chọn, bắt đầu bằng A, B, C, D. Tất cả các lựa chọn phải được hiển thị đầy đủ.
        4. Cuối mỗi câu hỏi, chỉ ra đáp án đúng bằng cách viết "Đáp án: [chữ cái]".
        5. Các câu hỏi được phân tách bằng một dòng trống.
        6. Đảm bảo rằng các câu hỏi liên quan trực tiếp đến nội dung được cung cấp, tuyệt đối không được tự chế ra thêm nội dung.

        Nội dung:
        {content}

        Ví dụ format:
        Câu hỏi: Nội dung đầy đủ của câu hỏi ở đây?
        A. Lựa chọn A
        B. Lựa chọn B
        C. Lựa chọn C
        D. Lựa chọn D
        Đáp án: B
        """
    
    # Đếm số lượng token trong nội dung tổng hợp được
    def _count_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))

