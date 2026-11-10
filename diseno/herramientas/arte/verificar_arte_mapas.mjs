import {raiz as _raiz, ruta as _ruta} from '../comun/proyecto.mjs';
process.chdir(_raiz);
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const B='diseno/respaldos/antes_arte_mapas/';
const sym=n=>Symbol.for('@'+n), get=(o,n)=>o[sym(n)];
function read(p){return load(fs.readFileSync(p),{string:'binary',hash:'map'});}
function hash(p){return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');}
const tsPath='Data/Tilesets.rxdata';
if(process.argv.includes('--apply')){
 const original=read(tsPath),before=read(B+tsPath);
 for(const id of [53,54,55])original[id][sym('battleback_name')]=new Uint8Array(Buffer.from('ui_piso'));
 const bytes=dump(original);
 assert.deepStrictEqual(load(bytes,{string:'binary',hash:'map'}),original);
 for(const id of [53,54,55])before[id][sym('battleback_name')]=get(original[id],'battleback_name');
 assert.deepStrictEqual(original,before,'Únicamente tres referencias de battleback');
 fs.writeFileSync(tsPath,bytes);
}
let files=0,unchanged=0;
for(const file of fs.readdirSync('Data').filter(n=>n.endsWith('.rxdata'))){
 const p='Data/'+file,raw=read(p);
 assert.deepStrictEqual(load(dump(raw),{string:'binary',hash:'map'}),raw,'Marshal roundtrip: '+file);
 if(file==='Tilesets.rxdata'){
  const before=read(B+p);
  for(const id of [53,54,55]){
   assert.equal(Buffer.from(get(raw[id],'battleback_name')).toString(),'ui_piso');
   before[id][sym('battleback_name')]=get(raw[id],'battleback_name');
  }
  assert.deepStrictEqual(raw,before,'Datos ajenos a las tres referencias alterados');
 }else{
  assert.equal(hash(p),hash(B+p),'Data debe conservar sus bytes: '+file);unchanged++;
 }
 files++;
}
const ts=read(tsPath), oldts=read(B+tsPath);
for(let i=1;i<ts.length;i++)if(ts[i])for(const key of ['passages','priorities','terrain_tags'])
 assert.deepStrictEqual(get(ts[i],key),get(oldts[i],key),`Tabla ${key} del tileset ${i}`);
for(const [p,h]of Object.entries(JSON.parse(fs.readFileSync(B+'protegidos.json','utf8'))))assert.equal(hash(p),h,p);
const report={result:'OK',marshal_files:files,byte_identical_files:unchanged,maps_byte_identical:32,
 changed_fields:[53,54,55].map(id=>`Tilesets[${id}].battleback_name = ui_piso`),
 passages_priorities_terrain:'idénticos en TODOS los tilesets, incluidas tablas no usadas',
 map_tiles_events:'Map001–Map032 idénticos byte a byte: índices, capas, eventos, páginas, coordenadas y comandos',
 protected:'Vacas.cfg y Scripts.rxdata con hashes originales',engine:'No se ha iniciado ni cerrado Game.exe'};
fs.writeFileSync('diseno/verificaciones/verificacion_arte_mapas_marshal.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report));
