## 1. 기본 채팅
# import ollama
#
# user_input = input("질의를 하세요: ")
# stream = ollama.generate(model='llama3', prompt=user_input)
# print(stream['response'])
# movie 데이터 로드
import pandas as pd
import time
print("파일읽기")
df = pd.read_csv("./kdrama.csv")

print("내용필터링")
filter_df = df.drop(["Aired Date", "Aired On", "Duration", "Content Rating", "Production companies", "Rank"], axis=1);

import chromadb
print("db파일경로지정")
client = chromadb.PersistentClient(path="../data")

print("컬렉션 생성")
collection = client.get_or_create_collection(
    name="k-drama",
    metadata={"hnsw:space": "cosine"}
)

# 데이터 준비
# 인덱스
ids = []
# 메타데이터
doc_meta = []
# 벡터로 변환 저장할 텍스트 데이터로 ChromaDB에 Embedding 데이터가 없으면 자동으로 벡터로 변환해서 저장한다고 한다.
documents = []
print("벡터로 변환작업")
seq =0
for idx in range(len(filter_df)):
    item = filter_df.iloc[idx]
    id = item['Name'].lower().replace(' ', '-')
    document = f"{item['Name']}: {item['Synopsis']} : {str(item['Cast']).strip().lower()} : {str(item['Genre']).strip().lower()}"
    meta = {
        "rating": item['Rating']
    }
    ids.append(id)
    time.sleep(0.1)
    print("1초휴식"+str(seq))
    doc_meta.append(meta)
    time.sleep(0.1)
    print("1초휴식" + str(seq))
    documents.append(document)
    seq= seq + 1

print("벡터변환내용 DB저장")
# DB 저장
collection.add(
    documents=documents,
    metadatas=doc_meta,
    ids=ids
)
print(document)
print("사용자에게 입력정보")

user_info = input("질의 하세요: ")

print("입력정보에 대한 답변 추출")
# DB 쿼리
result = collection.query(
    query_texts=[user_info],
    n_results=5,
)

print(result)