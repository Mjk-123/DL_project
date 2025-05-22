from datasets import load_dataset
import os

dataset = load_dataset("deepmind/code_contests", split="train")
save_dir = "joern_inputs_cpp"
os.makedirs(save_dir, exist_ok=True)

CPP_LANG_ID = 2  # C++ 언어 ID

saved_count = 0

for i, sample in enumerate(dataset):
    lang_ids = sample["solutions"].get("language", [])
    codes = sample["solutions"].get("solution", [])

    for lang_id, code in zip(lang_ids, codes):
        if lang_id == CPP_LANG_ID:
            filename = f"sample_{i}.cpp"
            with open(os.path.join(save_dir, filename), "w") as f:
                f.write(code)
            saved_count += 1
            break  # ✅ 한 sample당 1개만 저장하고 종료

print(f"✅ 최종 저장된 .cpp 파일 수: {saved_count}")
