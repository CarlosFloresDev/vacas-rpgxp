import { readRxdataRaw } from "file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js";
import { dump } from "file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js";
import fs from "fs";
const p = "D:/descargas/Proyectos personales/Vacas/Data/Scripts.rxdata";
const arr = await readRxdataRaw(p);
const name = (e) => Buffer.from(e[1]).toString("utf8");
const idx = arr.findIndex(e => name(e).startsWith("ZZ_Prueba"));
console.log("total", arr.length, "harness idx", idx);
if (idx >= 0) { arr.splice(idx, 1); fs.writeFileSync(p, dump(arr)); }
const again = await readRxdataRaw(p);
console.log(again.slice(-6).map(name));
