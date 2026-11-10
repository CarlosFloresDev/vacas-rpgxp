import {raiz as _raiz, ruta as _ruta} from '../comun/proyecto.mjs';
process.chdir(_raiz);
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {load} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const s=n=>Symbol.for('@'+n),B='diseno/respaldos/antes_arte_final/';
function read(p){return load(fs.readFileSync(p),{string:'binary',hash:'map'});}
let checked=0,portraits=0;
function replace(x){
 if(x instanceof Uint8Array){
  const a=Buffer.from(x).toString('latin1'),b=a.replace(/\\P\[madre_neutral\]/g,()=>{portraits++;return '\\P[madre_envejecida_neutral]';});
  return a===b?x:new Uint8Array(Buffer.from(b,'latin1'));
 }
 if(x instanceof Map){for(const[k,v]of x)x.set(k,replace(v));}
 else if(Array.isArray(x)){for(let i=0;i<x.length;i++)x[i]=replace(x[i]);}
 else if(x&&typeof x==='object'&&!x.userDefined){for(const k of Object.getOwnPropertySymbols(x))x[k]=replace(x[k]);}
 return x;
}
for(const name of ['Items','Skills','Enemies','Tilesets','System',...Array.from({length:11},(_,i)=>'Map'+String(i+22).padStart(3,'0'))]){
 const p='Data/'+name+'.rxdata',before=read(B+p),after=read(p);
 if(name==='Items'||name==='Skills'){
  const ids=name==='Items'?Array.from({length:40},(_,i)=>i+1):Array.from({length:10},(_,i)=>i+61);
  for(const id of ids)before[id][s('icon_name')]=after[id][s('icon_name')];
 }else if(name==='Enemies'){
  for(const id of [18,19,20,21,33,34,35,36,37])for(const k of ['battler_name','battler_hue'])before[id][s(k)]=after[id][s(k)];
 }else if(name==='Tilesets'){
  for(const id of [69,70])for(const k of ['passages','priorities','terrain_tags'])before[id][s(k)]=after[id][s(k)];
 }else if(name==='System'){
  for(const k of ['title_name','gameover_name','windowskin_name','battleback_name','battler_name'])before[s(k)]=after[s(k)];
 }else{
  before[s('data')]=after[s('data')];
  if(name==='Map030')replace(before[s('events')]);
 }
 assert.deepStrictEqual(before,after,'Cambio ajeno al arte o recodificación de texto: '+name);checked++;
}
const report={files:checked,portrait_references:portraits,result:'OK',scope:'Comparación Marshal binaria semántica: solo cambian campos gráficos, tablas de tiles y seis claves de retrato; todos los demás bytes de texto/objetos se preservan.'};
fs.writeFileSync('diseno/verificaciones/verificacion_arte_final_marshal.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report));

