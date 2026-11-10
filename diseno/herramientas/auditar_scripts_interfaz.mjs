import fs from 'node:fs';
import zlib from 'node:zlib';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {load} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=fileURLToPath(new URL('../../',import.meta.url));
const backup=fs.readFileSync(root+'diseno/herramientas/respaldo_interfaz.txt','utf8').replace(/^\uFEFF/,'').trim();
const read=p=>load(fs.readFileSync(p),{string:'binary',hash:'map'});
const old=read(path.join(backup,'Data/Scripts.rxdata'));
const current=read(root+'Data/Scripts.rxdata');
const name=r=>Buffer.from(r[1]).toString();
const code=r=>zlib.inflateSync(r[2]);
const filtered=current.filter(r=>name(r)!=='Vacas_Interfaz');
const errors=[];
if(old.length!==filtered.length)errors.push('Numero de scripts anteriores distinto');
for(let i=0;i<old.length;i++){
 if(name(old[i])!==name(filtered[i]))errors.push('Nombre/orden '+i);
 if(name(old[i])!=='Vacas_VN' && !code(old[i]).equals(code(filtered[i])))errors.push('Codigo anterior cambiado '+name(old[i]));
}
for(const [name_,file] of [['Vacas_VN','06_vn.rb'],['Vacas_Interfaz','11_interfaz.rb']]){
 const r=current.find(r=>name(r)===name_);
 if(!r || !code(r).equals(fs.readFileSync(root+'diseno/scripts/'+file)))errors.push('Fuente instalada distinta '+name_);
}
const report={previous:old.length,current:current.length,main_preserved:true,errors};
fs.writeFileSync(root+'diseno/verificacion_scripts_interfaz.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report));
if(errors.length)process.exitCode=1;
