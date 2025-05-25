import argparse
from datasets import load_dataset
import os
import json

def main():
    # 1) 커맨드라인 파서 설정
    parser = argparse.ArgumentParser(
        description="DeepMind code_contests에서 C++ 솔루션을 다운로드합니다."
    )
    parser.add_argument(
        "num_samples",
        type=int,
        nargs="?",
        default=100,
        help="추출할 C++ 솔루션 개수 (기본값: 100)"
    )
    args = parser.parse_args()
    max_samples = args.num_samples

    # 2) 데이터셋 로드 및 저장 디렉토리 준비
    dataset = load_dataset("deepmind/code_contests", split="train")
    save_dir = "joern_inputs_cpp"
    os.makedirs(save_dir, exist_ok=True)

    CPP_LANG_ID = 2
    saved_problems = []

    # 3) 다운로드 루프
    for sample in dataset:
        name = sample["name"].replace("/", "_")  # 안전한 파일 이름
        lang_ids = sample["solutions"].get("language", [])
        codes    = sample["solutions"].get("solution", [])

        # 가장 먼저 등장하는 C++ 솔루션 하나만 저장
        for lang_id, code in zip(lang_ids, codes):
            if lang_id == CPP_LANG_ID:
                filename = f"{name}.cpp"
                with open(os.path.join(save_dir, filename), "w") as f:
                    f.write(code)
                saved_problems.append(name)
                break

        # 원하는 개수만큼 모였으면 중단
        if len(saved_problems) >= max_samples:
            break

    print(f"✅ 저장된 C++ 솔루션 수: {len(saved_problems)}")

    # 4) 초기 solutions.json 생성 (빈 token2type)
    solutions = {name: {"token2type": {}} for name in saved_problems}
    solutions_path = "solutions.json"
    with open(solutions_path, "w", encoding="utf-8") as jf:
        json.dump(solutions, jf, ensure_ascii=False, indent=2)

    print(f"✅ {solutions_path} 생성 완료: {len(solutions)} entries")


if __name__ == "__main__":
    main()
