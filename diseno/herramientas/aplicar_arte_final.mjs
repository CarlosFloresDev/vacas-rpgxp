// Modifica campos gráficos sin recodificar textos del Marshal original.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=path.resolve('.');
const B=path.join(root,'diseno/respaldos/antes_arte_final');
const patches=JSON.parse(fs.readFileSync('diseno/herramientas/arte_final_patch.json','utf8'));
const sym=n=>Symbol.for('@'+n);
function get(o,k){return o[sym(k)];}
function set(o,k,v){o[sym(k)]=v;}
function read(n){return load(fs.readFileSync('Data/'+n+'.rxdata'),{string:'binary',hash:'map'});}
function write(n,raw){
 const file='Data/'+n+'.rxdata',b=path.join(B,file);
 if(!fs.existsSync(b)){fs.mkdirSync(path.dirname(b),{recursive:true});fs.copyFileSync(file,b);}
 const bytes=dump(raw);
 assert.deepStrictEqual(load(bytes,{string:'binary',hash:'map'}),raw);
 fs.writeFileSync(file,bytes);
}
function table(obj,d){
 const buf=Buffer.alloc(20+d.data.length*2);
 [d.dim,d.xsize,d.ysize,d.zsize,d.data.length].forEach((v,i)=>buf.writeUInt32LE(v,i*4));
 d.data.forEach((v,i)=>buf.writeInt16LE(v,20+i*2));obj.userDefined=new Uint8Array(buf);
}
const enemies=read('Enemies');
const names={18:'turno_noche',19:'res_cuenta',20:'gancho_respira',21:'cripps_matarife',33:'censo_bocas',34:'mesa_exige',35:'rey_sin_rostro',36:'numero_cadena',37:'puerta_muerde'};
for(const [id,key] of Object.entries(names)){set(enemies[id],'battler_name',new Uint8Array(Buffer.from('enemigo_'+key)));set(enemies[id],'battler_hue',0);}
write('Enemies',enemies);
let replacements=0;
function portrait(x){
 if(x instanceof Uint8Array){
  const t=Buffer.from(x).toString('latin1');
  const v=t.replace(/\\P\[madre_neutral\]/g,()=>{replacements++;return '\\P[madre_envejecida_neutral]';});
  return v===t?x:new Uint8Array(Buffer.from(v,'latin1'));
 }
 if(x instanceof Map){for(const [k,v] of x)x.set(k,portrait(v));}
 else if(Array.isArray(x)){for(let i=0;i<x.length;i++)x[i]=portrait(x[i]);}
 else if(x && typeof x==='object' && !x.userDefined){for(const k of Object.getOwnPropertySymbols(x))x[k]=portrait(x[k]);}
 return x;
}
for(let id=22;id<=32;id++){
 const name='Map'+String(id).padStart(3,'0'),raw=read(name);
 table(get(raw,'data'),patches[name].data);
 if(id===30)portrait(get(raw,'events'));
 write(name,raw);
}
const ts=read('Tilesets');
for(const id of [69,70])for(const key of ['passages','priorities','terrain_tags'])table(get(ts[id],key),patches['Tileset'+id][key]);
write('Tilesets',ts);
const system=read('System');
for(const [k,v] of Object.entries({title_name:'vacas_titulo',gameover_name:'vacas_gameover',windowskin_name:'ui_windowskin',battleback_name:'mente_matadero',battler_name:'steven_mente'}))set(system,k,new Uint8Array(Buffer.from(v)));
write('System',system);
console.log('9 enemigos con arte exclusivo/hue0; 11 tablas de mapa; 2 tablas de tileset; '+replacements+' retratos VI; defaults gráficos System propios. Textos binarios preservados.');

