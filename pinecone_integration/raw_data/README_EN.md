
## :computer: Use the chatbot to generate questions
### Upload raw data from the file data/qtda_raw.txt to Pinecone (if you want to use your own index on Pinecone; otherwise, refer to section 2)  
  - Run the file **save_raw_data_to_pinecone.py** to upload data from the **data/qtda_raw.txt** file to Pinecone. The chatbot will use the data on Pinecone to generate questions for the subject.  

  **Note:** Change the API key, index name from your Pinecone account and optionally use your own openai_api_key.  
  - To do this, you need to have an account on https://www.pinecone.io/ and create an index. Then, modify the values of **api_key**, **index_name**, **dimension** (keep it as 1526 if using OpenAI's text-embedding-ada-002 model), **cloud** and **region** in the code snippet below of the **save_structured_data_to_pinecone.py** file to match your configuration.
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

  - Additionally, you also need to change the **index** in the code snippet below in the **app.py** file:    
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

### 2. Using chatbot  
- Run the **app.py** file and access http://127.0.0.1:5000/ to use the chatbot on localhost.
**Note:** If you encounter the error **Error: Cannot import name 'Pinecone' from 'pinecone'** when running the file, execute the following command in the Terminal::
```bash
pip install "pinecone-client[grpc]" --upgrade
```
- Syntax to use the chatbot:  
  - **View the chapters supported by the chatbot:** `chương hỗ trợ`
  - **Generate a number of questions for any keyword:** `keyword: [keyword]: [số lượng câu hỏi (tối đa 15)]` 
- You can choose the question generation mode as Gemini, Claude, or ChatGPT if you want.  
  ![chatbot](https://github.com/user-attachments/assets/b6b5d0be-e748-41c5-be33-528d92a93c14)

