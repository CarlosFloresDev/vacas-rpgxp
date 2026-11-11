// Correcciones localizadas. Conserva bytes de textos originales y clases Marshal.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
import {toPlain,toRuby} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
import {raiz} from './proyecto.mjs';
process.chdir(raiz);
const base='diseno/respaldos/antes_jugabilidad/Data/';
if(!fs.existsSync(base+'Map002.rxdata'))throw Error('Falta respaldo previo');
const raw={},plain={},changes=[];
function read(n){if(!raw[n]){raw[n]=load(fs.readFileSync('Data/'+n+'.rxdata'),{string:'binary',hash:'map'});plain[n]=toPlain(raw[n]);}return plain[n];}
function set(n,keys,value,reason,mapa){
 let a=read(n),b=raw[n];for(const k of keys.slice(0,-1)){a=a[k];b=b instanceof Map?b.get(Number(k)):Array.isArray(b)?b[k]:b[Symbol.for('@'+k)];}
 const k=keys.at(-1);if(JSON.stringify(a[k])===JSON.stringify(value))return;
 changes.push({archivo:n,mapa,ruta:keys,antes:a[k],despues:value,motivo:reason});a[k]=value;
 if(b instanceof Map)b.set(Number(k),toRuby(value));else if(Array.isArray(b))b[k]=toRuby(value);else b[Symbol.for('@'+k)]=toRuby(value);
}
function flags(ts,id,pass,prio,mapa,why){
 const t=read('Tilesets')[ts];for(const [key,val] of [['passages',pass],['priorities',prio]]){
  if(t[key].data[id]===val)continue;
  changes.push({archivo:'Tilesets',mapa,tileset:ts,tile:id,campo:key,antes:t[key].data[id],despues:val,motivo:why});
  t[key].data[id]=val;raw.Tilesets[ts][Symbol.for('@'+key)]=toRuby(t[key]);
 }
}
// La ventana se activa a través de la cajonera, como un mostrador XP.
const m2=read('Map002'),t2=read('Tilesets')[m2.tileset_id];
const under=m2.data.data[3+3*m2.width+m2.width*m2.height];
flags(m2.tileset_id,under,t2.passages.data[under]|128,t2.priorities.data[under],2,'Ventana accesible sobre la cajonera; conserva bloqueo');
// Las vacas permanecen dentro del corral, junto a la valla para poder mirarlas.
const m7=read('Map007'),t7=read('Tilesets')[m7.tileset_id];
for(const [id,x] of [[5,5],[6,7],[7,12],[8,15],[9,21],[10,26],[11,24]]){
 set('Map007',['events',String(id),'x'],x,'Interacción desde la valla',7);
 set('Map007',['events',String(id),'y'],8,'Interacción desde la valla',7);
 for(const z of [0,1,2]){const tid=m7.data.data[x+7*m7.width+z*m7.width*m7.height];if(tid&&(t7.passages.data[tid]&15)===15)flags(m7.tileset_id,tid,t7.passages.data[tid]|128,t7.priorities.data[tid],7,'Valla como counter; no abre el corral');}
}
set('Map007',['events','17','y'],5,'Cubo junto al pasillo accesible',7);
set('Map007',['events','11','pages',1,'list'],
 [{_class:'RPG::EventCommand',code:0,indent:0,parameters:[]}],
 'La vaca ya salio: quitar vision inyectada en su pagina vacia; sigue disponible en las otras vacas',7);
// La vaca del fondo arranca cuatro casillas más al norte: mismo destino de ruta.
const routeIndex=m7.events['14'].pages[0].list.findIndex(c=>c.code===209&&c.parameters[0]===11);
const route=m7.events['14'].pages[0].list[routeIndex].parameters[1];
if(route.list.filter(c=>c.code===4).length===9){
 let removed=0;const list=route.list.filter(c=>!(c.code===4&&removed++<4));
 set('Map007',['events','14','pages',0,'list',routeIndex,'parameters',1,'list'],list,'Conservar destino de la manga después de acercar la vaca a la valla',7);
}
// Muebles añadidos por revision_mapas.py sin huella en mapas de persecución.
// Solo baldosas exclusivas del atlas de cada mapa: nunca se cambia suelo compartido.
const footprints={2:[[2,6],[3,6],[17,7],[1,17],[10,19],[11,19],[11,12]],7:[[1,3],[9,4],[19,4],[27,15]],8:[[7,3],[8,3],[19,3],[20,3],[28,3],[2,18],[14,20],[28,19],[29,19],[35,19]],9:[[7,3],[17,3],[27,3],[28,3],[25,17]],14:[[1,5],[2,5],[15,10],[9,3],[10,3]]};
const applied=[];
for(const [midStr,cells] of Object.entries(footprints)){
 const mid=Number(midStr),name='Map'+String(mid).padStart(3,'0'),m=read(name),t=read('Tilesets')[m.tileset_id];
 for(const [x,y] of cells){const id=m.data.data[x+y*m.width+m.width*m.height];
  // Muebles omitidos por el generador o sustituidos por un objeto original.
  const first=mid===2?592:448;
  if(id<first)continue;
  assert.equal(m.data.data.filter(v=>v===id).length,1,'Tile de decoración no exclusivo');
  flags(m.tileset_id,id,t.passages.data[id]|15,0,mid,'Huella de mueble grande de la revisión de arte');
  applied.push({mapa:mid,x,y,tile:id});
 }
}
// El lavabo no indicaba dónde estaba el encargo si se examinaba antes de las órdenes.
const lavabo=m2.events['11'];
const elseIndex=lavabo.pages[0].list.findIndex(c=>c.code===411);
set('Map002',['events','11','pages',0,'list',elseIndex+1,'parameters',0],
 'El jarabe de madre esta detras del espejo.', 'Hacer localizable el jarabe antes de recibir las ordenes',2);
set('Map002',['events','11','pages',0,'list',elseIndex+2,'parameters',0],
 'Primero debo hablar con ella.', 'Indicar la condicion real: switch 2',2);
if(process.argv.includes('--aplicar')){
 for(const n of Object.keys(raw)){if(!changes.some(c=>c.archivo===n))continue;const bytes=dump(raw[n]);assert.deepStrictEqual(load(bytes,{string:'binary',hash:'map'}),raw[n]);fs.writeFileSync('Data/'+n+'.rxdata',bytes);}
 const previous='diseno/verificaciones/correcciones_jugabilidad.json';
 if(changes.length){const old=fs.existsSync(previous)?JSON.parse(fs.readFileSync(previous,'utf8')).cambios:[];fs.writeFileSync(previous,JSON.stringify({cambios:old.concat(changes),huellas:applied},null,2)+'\n');}
}
console.log(JSON.stringify({aplicado:process.argv.includes('--aplicar'),cambios:changes.length,por_mapa:Object.fromEntries([...new Set(changes.map(c=>c.mapa))].sort((a,b)=>a-b).map(m=>[m,changes.filter(c=>c.mapa===m).length]))}));
