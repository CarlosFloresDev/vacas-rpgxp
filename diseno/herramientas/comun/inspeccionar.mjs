import fs from 'fs';
import path from 'path';
import zlib from 'zlib';
import assert from 'node:assert/strict';
import {readRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
import {raiz as root} from './proyecto.mjs';
const readonly = process.argv.includes('--solo-lectura');
let snapshot={};
for(const file of fs.readdirSync(path.join(root,'Data')).filter(x=>x.endsWith('.rxdata'))){
 const bytes=fs.readFileSync(path.join(root,'Data',file));
 const raw=load(bytes,{string:'binary',hash:'map'});
 const again=load(dump(raw),{string:'binary',hash:'map'});
 assert.deepStrictEqual(again,raw,'Round-trip semantico: '+file);
 if(file==='Scripts.rxdata'){
  snapshot.Scripts=raw.map((s,i)=>({index:i,name:Buffer.from(s[1]).toString(),code:zlib.inflateSync(s[2]).toString()}));
 }else snapshot[file.replace('.rxdata','')]=await readRxdataFile(path.join(root,'Data',file));
}
if (!readonly) {
 const output=path.join(root,'diseno/verificaciones/inventario');
 const scripts=path.join(root,'diseno/verificaciones/scripts_motor');
 fs.mkdirSync(output,{recursive:true});
 fs.mkdirSync(scripts,{recursive:true});
 fs.writeFileSync(path.join(output,'snapshot.json'),JSON.stringify(snapshot));
 for(const s of snapshot.Scripts)fs.writeFileSync(path.join(scripts,String(s.index).padStart(3,'0')+'.rb'),s.code);
}
console.log('Snapshot y round-trip en memoria: '+Object.keys(snapshot).length+' archivos. '+snapshot.Scripts.length+' scripts.');
