
var cpg = CpgLoader.load("/Users/minjoonkim/Desktop/final_project/DL_project/tmp_projects/1101_A__Minimum_Integer/cpg.bin")
val names = cpg.identifier.name.l ++ cpg.call.name.l ++ cpg.literal.code.l
val types = cpg.identifier.typeFullName.l ++ cpg.call.typeFullName.l ++ cpg.literal.typeFullName.l
val out = names.zip(types)
import better.files._
File("/Users/minjoonkim/Desktop/final_project/DL_project/tmp_projects/1101_A__Minimum_Integer/token_types.csv")
  .writeText("token,type\n" + out.map { case (t, ty) => s"$t,$ty" }.mkString("\n"))
