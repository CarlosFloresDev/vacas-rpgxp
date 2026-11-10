import fs from 'node:fs';
import assert from 'node:assert/strict';
import zlib from 'node:zlib';
import {fileURLToPath} from 'node:url';
import {load} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=fileURLToPath(new URL('../../',import.meta.url));
const read=p=>load(fs.readFileSync(root+p),{string:'binary',hash:'map'});
const before=read('diseno/respaldos/antes_fase45/Data/Scripts.rxdata');
const after=read('Data/Scripts.rxdata');
const name=r=>Buffer.from(r[1]).toString();
const modified=[];
for(const row of before){
 const now=after.find(r=>name(r)===name(row));assert.ok(now,'Seccion perdida '+name(row));
 assert.deepEqual(now.slice(0,2),row.slice(0,2),'ID/nombre alterado');
 if(!Buffer.from(now[2]).equals(Buffer.from(row[2])))modified.push(name(row));
}
assert.deepEqual(modified,['Vacas_Matadero']);
const added=after.filter(r=>!before.some(b=>name(b)===name(r))).map(name);
assert.deepEqual(added,['Vacas_Cinematicas']);
assert.equal(name(after[after.length-1]),'Main');
for(const [section,file] of [['Vacas_Matadero','05_matadero.rb'],['Vacas_Cinematicas','15_cinematicas.rb']]){
 const row=after.find(r=>name(r)===section);
 assert.ok(zlib.inflateSync(row[2]).equals(fs.readFileSync(root+'diseno/scripts/'+file)),'Fuente diferente');
}
const report={secciones_anteriores:before.length,secciones_actuales:after.length,modificadas:modified,agregadas:added,resto_y_Main_identicos:true};
fs.writeFileSync(root+'diseno/auditoria_instalacion_fase45.json',JSON.stringify(report,null,2));
console.log(report);
