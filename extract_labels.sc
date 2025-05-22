import better.files._

// 1. 노드 수집
val methodNodes = cpg.method.l.map(n => Map("code" -> n.name, "label" -> "METHOD"))
val identifierNodes = cpg.identifier.l.map(n => Map("code" -> n.name, "label" -> "IDENTIFIER"))
val literalNodes = cpg.literal.l.map(n => Map("code" -> n.code, "label" -> "LITERAL"))
val callNodes = cpg.call.l.map(n => Map("code" -> n.code, "label" -> "CALL"))

// 2. 리스트 합치기
val allNodes = methodNodes ++ identifierNodes ++ literalNodes ++ callNodes

// 3. JSON string 직접 생성
val asJson = allNodes.map(m =>
  s"""{"code": "${m("code").replace("\"", "\\\"")}", "label": "${m("label")}"}"""
).mkString("[", ",", "]")

// 4. 저장
File("/home/dongsubkim/project/labels_output.json").write(asJson)
