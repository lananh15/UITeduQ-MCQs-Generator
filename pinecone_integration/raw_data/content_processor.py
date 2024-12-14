from common.handlers.llm_handler_base import LLMHandlerBase
from typing import List, Dict, Tuple
import random

class ContentProcessor(LLMHandlerBase):
    # Tạo ra danh sách các câu hỏi dựa trên nội dung đầu vào
    def generate_questions(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
        all_content = self._combine_content(pinecone_results)
        print(all_content)
        if self._count_tokens(all_content) <= 3800:
            return self._generate_questions_direct(all_content, num_questions)
        else:
            return self._generate_questions_chunked(pinecone_results, num_questions)

    # Tổng hợp các câu hỏi có được sau mỗi chunk
    def _generate_questions_chunked(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
        all_questions = []
        chunks = self._chunk_content(pinecone_results)
        
        for chunk in chunks:
            chunk_questions = self._generate_questions_direct(chunk, 5)
            all_questions.extend(chunk_questions)
        
        if len(all_questions) < num_questions:
            full_content = "\n\n".join(chunks)
            additional_questions = self._generate_questions_direct(full_content, num_questions - len(all_questions))
            all_questions.extend(additional_questions)
        
        random.shuffle(all_questions)
        return all_questions[:num_questions]

    # Chia nội dung ra thành các chunk nếu nội dung quá dài
    def _chunk_content(self, pinecone_results: List[Dict]) -> List[str]:
        chunks = []
        for result in pinecone_results:
            metadata = result.get('metadata', {})
            content = metadata.get('text', '')
            
            # Thêm nội dung vào danh sách chunks
            chunks.append(content)
            
        return chunks

    # Kết hợp nội dung từ nhiều kết quả tìm kiếm Pinecone thành một chuỗi văn bản tổng hợp
    def _combine_content(self, pinecone_results: List[Dict]) -> str:
        contents = []
        for result in pinecone_results:
            metadata = result['metadata']
            content = metadata.get('text', '')
            contents.append(content)
        return "\n\n".join(contents)
