import json

# 1. JSON 로드
with open("/home/dongsubkim/project/labels_output.json", "r") as f:
    data = eval(f.read())  # JSON이 아닌 Scala-style 출력이므로 eval 사용

# 2. label 추출
labels = [item["label"] for item in data]

# 3. 유니크한 타입 리스트
unique_labels = sorted(set(labels))
print("라벨 목록:", unique_labels)

# 4. One-hot 인덱스 매핑
label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}

# 5. One-hot 변환
def one_hot(label):
    vec = [0] * len(unique_labels)
    vec[label_to_idx[label]] = 1
    return vec

embedding_vectors = [one_hot(label) for label in labels]

# 6. 예시 출력
print("예시 라벨:", labels[:5])
print("예시 임베딩:", embedding_vectors[:5])
