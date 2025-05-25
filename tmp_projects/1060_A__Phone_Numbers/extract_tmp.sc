
var cpg = CpgLoader.load("/Users/minjoonkim/Desktop/final_project/DL_project/tmp_projects/1060_A__Phone_Numbers/cpg.bin")
val names = cpg.identifier.name.l ++ cpg.call.name.l ++ cpg.literal.code.l
val types = cpg.identifier.typeFullName.l ++ cpg.call.typeFullName.l ++ cpg.literal.typeFullName.l
val out = names.zip(types)
import better.files._
File("/Users/minjoonkim/Desktop/final_project/DL_project/tmp_projects/1060_A__Phone_Numbers/token_types.csv")
  .writeText("token,type\n" + out.map { case (t, ty) => s"$t,$ty" }.mkString("\n"))
