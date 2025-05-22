import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# 1. 파일 불러오기
df = pd.read_csv("token_types.csv", names=["token", "type"])

# 2. 중복 제거 (동일 token-type 쌍 제거)
df = df.drop_duplicates()

# 3. Label Encoding
le = LabelEncoder()
df["type_id"] = le.fit_transform(df["type"])

# 4. One-hot 생성
num_classes = len(le.classes_)
one_hot = np.eye(num_classes)[df["type_id"]]
df["embedding"] = one_hot.tolist()

# 5. 저장 (JSONL)
df.to_json("token_type_embeddings.json", orient="records", lines=True)

# 6. 예시 출력
print("✅ 타입 수:", num_classes)
print("예시:")
print(df.head(10))
