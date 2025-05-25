import json
from sklearn.preprocessing import LabelEncoder

# 1) 기존 JSON 불러오기
with open("solutions.json", encoding="utf-8") as f:
    solutions = json.load(f)

# 2) 모든 타입 수집
all_types = set()
for entry in solutions.values():
    all_types.update(entry["token2type"].values())

# 3) LabelEncoder로 정수 ID 생성
le = LabelEncoder()
le.fit(list(all_types))
type2id = {t: int(i) for i, t in enumerate(le.classes_)}  # t→id 맵

# (선택) 매핑도 JSON으로 저장하고 싶다면
with open("type2id.json", "w", encoding="utf-8") as f:
    json.dump(type2id, f, ensure_ascii=False, indent=2)

# 4) solutions의 값들을 문자열→정수로 변환
for entry in solutions.values():
    entry["token2type"] = {tok: type2id[typ] 
                           for tok, typ in entry["token2type"].items()}

# 5) 같은 파일에 덮어쓰기
with open("solutions.json", "w", encoding="utf-8") as f:
    json.dump(solutions, f, ensure_ascii=False, indent=2)

print(f"✅ solutions.json 업데이트 완료 ({len(type2id)}개 타입 매핑 생성)") 
