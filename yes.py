from datasets import load_dataset

# 데이터셋 로드
dataset = load_dataset("deepmind/code_contests", split="train")

# 하나의 샘플 꺼내기
sample = dataset[0]

# 샘플에 어떤 키(필드)가 있는지 출력해보기
print(sample.keys())
