
## :computer: Dùng chatbot hỗ trợ sinh câu hỏi
### 1. Lưu dữ liệu thô từ file data/qtda_raw.txt lên Pinecone (nếu muốn dùng index của riêng bạn trên pinecone, nếu không hãy xem mục số 2)  
  - Run file **save_raw_data_to_pinecone.py** để có thể lưu dữ liệu từ file **data/qtda_raw.txt** lên Pinecone theo các vector. Chatbot sẽ sử dụng dữ liệu trên Pinecone để tạo câu hỏi cho môn học.  

  **Lưu ý:** Thay đổi API key, tên index khác từ tài khoản Pinecone và có thể sử dụng openai_api_key của riêng bạn.  
  - Để làm được, bạn cần phải có tài khoản trên https://www.pinecone.io/ và tạo index. Sau đó thay đổi các giá trị **api_key**, **index_name**, **dimension** (nếu dùng mô hình text-embedding-ada-002 của openAI thì giữ nguyên 1536), **cloud** và **region** trong đoạn code dưới đây của file **save_structured_data_to_pinecone.py** sao cho phù hợp.
  ```python
    # Khởi tạo Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    # Kết nối đến index đã tồn tại
    index_name = "generate-quizz-with-raw-data"
    # Kiểm tra xem index có tồn tại không và xóa nếu có
    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)
    # Tạo mới nếu chưa tồn tại
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # Đảm bảo dimension khớp với model embedding bạn sử dụng
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
 
  ```  

  - Ngoài ra, cũng cần thay đổi **index** trong đoạn code dưới đây của file **app.py**  
  ```python
    def main():
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

        llm_handler = ContentProcessor(OPENAI_API_KEY, GOOGLE_API_KEY, ANTHROPIC_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("generate-quizz-with-raw-data")

        openai_client = OpenAI(api_key=OPENAI_API_KEY)

        app = PineconeQuizzSearchApp(llm_handler, index, openai_client)
        app.run()
  ```  

### 2. Sử dụng chatbot  
- Run file **app.py** và truy cập vào http://127.0.0.1:5000/ để dùng chatbot ở localhost.
**Lưu ý:** Nếu bạn Run file mà gặp lỗi **Error: Cannot import name 'Pinecone' from 'pinecone'** thì hãy chạy thêm dòng lệnh trong Terminal:
```bash
pip install "pinecone-client[grpc]" --upgrade
```
- Các cú pháp để dùng chatbot:  
  - **Xem các chương mà chatbot hỗ trợ:** `chương hỗ trợ`
  - **Tạo số lượng câu hỏi cho keyword bất kì:** `keyword: [keyword]: [số lượng câu hỏi (tối đa 15)]`  
- Bạn có thể chọn chế độ sinh câu hỏi như Gemini, Claude hoặc ChatGPT nếu bạn muốn.  
  ![chatbot](https://github.com/user-attachments/assets/b6b5d0be-e748-41c5-be33-528d92a93c14)  

