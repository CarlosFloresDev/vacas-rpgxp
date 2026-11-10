import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const s=n=>Symbol.for('@'+n);
for(const[kind,ids,prefix]of[['Items',Array.from({length:40},(_,i)=>i+1),'vacas_item_'],['Skills',Array.from({length:10},(_,i)=>i+61),'vacas_habilidad_']]){
 const p='Data/'+kind+'.rxdata',b='diseno/respaldos/antes_arte_final/'+p,raw=load(fs.readFileSync(p),{string:'binary',hash:'map'});
 for(const id of ids){
  const name=prefix+String(id).padStart(2,'0');
  if(!fs.existsSync('Graphics/Icons/'+name+'.png'))throw Error('Falta '+name);
  raw[id][s('icon_name')]=new Uint8Array(Buffer.from(name));
 }
 const bytes=dump(raw);assert.deepStrictEqual(load(bytes,{string:'binary',hash:'map'}),raw);
 if(!fs.existsSync(b)){fs.mkdirSync(path.dirname(b),{recursive:true});fs.copyFileSync(p,b);}
 fs.writeFileSync(p,bytes);
}
console.log('40 objetos y10 habilidades con icono propio; solo campos icon_name, Marshal sin recodificar textos.');

