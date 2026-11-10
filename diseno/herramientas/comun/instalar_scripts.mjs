// Vista previa por defecto. --aplicar instala SOLO las secciones ya existentes.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import assert from 'node:assert/strict';
import {raiz, ruta} from './proyecto.mjs';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const manifest=JSON.parse(fs.readFileSync(ruta('diseno/scripts/manifest.json'),'utf8'));
const target=ruta('Data/Scripts.rxdata'), original=fs.readFileSync(target);
const rows=load(original,{string:'binary',hash:'map'});
for(const entry of manifest){
 assert.equal(Buffer.from(rows[entry.index][1]).toString(),entry.name,'Orden de Scripts.rxdata distinto');
 const source=fs.readFileSync(ruta(entry.file),'utf8');
 rows[entry.index][2]=new Uint8Array(zlib.deflateSync(Buffer.from(source)));
}
const bytes=dump(rows);
assert.deepStrictEqual(load(bytes,{string:'binary',hash:'map'}),rows);
if(process.argv.includes('--aplicar')){
 const backup=path.join(raiz,'diseno/respaldos','scripts_'+new Date().toISOString().replace(/[:.]/g,'_'));
 fs.mkdirSync(backup,{recursive:true});
 fs.writeFileSync(path.join(backup,'Scripts.rxdata'),original,{flag:'wx'});
 const temp=target+'.tmp';
 try {fs.writeFileSync(temp,bytes,{flag:'wx'});fs.renameSync(temp,target);}
 finally {if(fs.existsSync(temp))fs.unlinkSync(temp);}
 console.log('Instaladas '+manifest.length+' secciones. Respaldo: '+backup);
}else console.log('Vista previa OK: '+manifest.length+' secciones, orden y Marshal comprobados. Para instalar: --aplicar');
