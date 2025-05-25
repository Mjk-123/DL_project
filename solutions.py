import os
import re
import json
import subprocess
import shutil

def safe_dir_name(name: str) -> str:
    """파일시스템용 안전 이름으로 변환"""
    return re.sub(r"[^A-Za-z0-9_-]", "_", name)

# ────────────────────────────────────────────────────────────────────────────
# 경로 설정
base_dir            = "/Users/minjoonkim/Desktop/final_project/DL_project"
cpp_dir             = os.path.join(base_dir, "joern_inputs_cpp")
tmp_root            = os.path.join(base_dir, "tmp_projects")
joern_dir           = "/Users/minjoonkim/Desktop/final_project/joern"
joern_parse         = os.path.join(joern_dir, "joern-parse")
joern_exec          = os.path.join(joern_dir, "joern")
solutions_json_path = os.path.join(base_dir, "solutions.json")
# ────────────────────────────────────────────────────────────────────────────

# 1) 전체 CPG 생성 (한 번만)
print("▶️ Generating global CPG from all .cpp files …")
subprocess.run([joern_parse, cpp_dir], check=True)

# Joern-parse가 기본적으로 생성하는 CPG 위치 (현재 작업 디렉토리 기준)
global_cpg = os.path.join(base_dir, "cpg.bin")
if not os.path.exists(global_cpg):
    raise FileNotFoundError(f"Expected global CPG at {global_cpg}")

# 2) 문제별로 CPG 복사 & 토큰 추출
solutions = {}
cpp_files = [f for f in os.listdir(cpp_dir) if f.endswith(".cpp")]

for cpp_file in cpp_files:
    name      = cpp_file[:-4]
    safe_name = safe_dir_name(name)
    cpp_path  = os.path.join(cpp_dir, cpp_file)
    tmp_dir   = os.path.join(tmp_root, safe_name)
    os.makedirs(tmp_dir, exist_ok=True)

    # 2-1) .cpp 복사
    shutil.copy(cpp_path, tmp_dir)

    # 2-2) global CPG 복사 → 문제별 cpg.bin
    dest_cpg = os.path.join(tmp_dir, "cpg.bin")
    shutil.copy(global_cpg, dest_cpg)
    print(f"[✅ CPG COPIED] {name}")

    # 2-3) extract_tmp.sc 생성
    script_path = os.path.join(tmp_dir, "extract_tmp.sc")
    extract_script = f"""
var cpg = CpgLoader.load("{dest_cpg}")
val names = cpg.identifier.name.l ++ cpg.call.name.l ++ cpg.literal.code.l
val types = cpg.identifier.typeFullName.l ++ cpg.call.typeFullName.l ++ cpg.literal.typeFullName.l
val out = names.zip(types)
import better.files._
File("{tmp_dir}/token_types.csv")
  .writeText("token,type\\n" + out.map {{ case (t, ty) => s"$t,$ty" }}.mkString("\\n"))
"""
    with open(script_path, "w") as f:
        f.write(extract_script)

    # 2-4) Joern 스크립트 실행
    subprocess.run(
        [joern_exec, "--script", script_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # 2-5) token_types.csv 읽어서 딕셔너리화
    token_csv = os.path.join(tmp_dir, "token_types.csv")
    token2type = {}
    if os.path.exists(token_csv):
        with open(token_csv) as f:
            next(f)
            for line in f:
                line = line.strip()
                if not line or "," not in line:
                    continue
                tok, ty = line.split(",", 1)
                token2type[tok] = ty
    else:
        print(f"[⚠️ NO TOKENS] {name}: token_types.csv missing")

    solutions[name] = {"token2type": token2type}

# 3) solutions.json 저장
with open(solutions_json_path, "w") as f:
    json.dump(solutions, f, indent=2)

print(f"\n✅ Completed: {len(solutions)} entries written to solutions.json")
