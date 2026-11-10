// Data debe estar respaldada antes de invocar esta instalacion.
import fs from 'node:fs';
import zlib from 'node:zlib';
import {fileURLToPath} from 'node:url';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=fileURLToPath(new URL('../../',import.meta.url));
if(!fs.existsSync(root+'diseno/herramientas/respaldo_interfaz.txt'))throw Error('Falta respaldo registrado');
const path=root+'Data/Scripts.rxdata';
const rows=load(fs.readFileSync(path),{string:'binary',hash:'map'});
for(const [file,name] of [['06_vn.rb','Vacas_VN'],['11_interfaz.rb','Vacas_Interfaz']]){
 const code=zlib.deflateSync(fs.readFileSync(root+'diseno/scripts/'+file));
 const old=rows.find(r=>Buffer.from(r[1]).toString()===name);
 if(old) old[2]=code;
 else rows.splice(rows.findIndex(r=>Buffer.from(r[1]).toString()==='Main'),0,[197601,Buffer.from(name),code]);
}
fs.writeFileSync(path,dump(rows));
console.log('Vacas_VN e Interfaz instalados; Main conservado.');
