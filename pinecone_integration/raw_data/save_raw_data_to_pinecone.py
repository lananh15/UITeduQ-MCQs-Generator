import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List
from dotenv import load_dotenv

# Đọc tệp cấu hình
load_dotenv()

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

# Kết nối đến index
index = pc.Index(index_name)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def read_file(file_path: str) -> str:
    # Đọc nội dung từ tệp văn bản
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_into_chunks(text: str) -> List[str]:
    # Chia văn bản thành các chunk nhỏ hơn dựa trên dấu phân tách '\n\n'.
    chunks = text.split('\n\n')
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

def create_embedding(text: str) -> List[float]:
    # Tạo embedding cho văn bản sử dụng OpenAI
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def upload_to_pinecone(chunks: List[str]):
    # Tải các chunk lên Pinecone
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = create_embedding(chunk)
        metadata = {
            "text": chunk,
        }
        vectors.append((f"chunk_{i}", vector, metadata))
    index.upsert(vectors)

# Định nghĩa đường dẫn thư mục chứa script
script_dir = os.path.dirname(__file__)

# Lên 2 cấp thư mục và kết hợp với tên file 'qtda_raw.txt'
file_path = os.path.join(script_dir, '../..', 'data', 'qtda_raw.txt')

# Chuẩn hóa đường dẫn để loại bỏ các thành phần dư thừa (nếu có)
file_path = os.path.abspath(file_path)

# Đọc file
raw_text = read_file(file_path)

# Chia thành các chunk
chunks = split_into_chunks(raw_text)

# Upload lên Pinecone
upload_to_pinecone(chunks)

print(f"Đã xử lý và upload {len(chunks)} chunks lên Pinecone.")
