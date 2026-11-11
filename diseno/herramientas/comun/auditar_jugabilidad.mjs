// Auditor offline: lee Marshal actual, nunca depende del snapshot histórico.
import fs from 'node:fs';
import path from 'node:path';
import {raiz} from './proyecto.mjs';
import {readRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
process.chdir(raiz);
export const D=[[2,0,1],[4,-1,0],[6,1,0],[8,0,-1]];
export const S={};
for(const f of fs.readdirSync('Data').filter(f=>f.endsWith('.rxdata')&&f!=='Scripts.rxdata').sort()) S[f.slice(0,-7)]=await readRxdataFile('Data/'+f);
export const maps=Object.keys(S).filter(k=>/^Map\d+$/.test(k)).map(k=>[Number(k.slice(3)),S[k]]);
export function stateFor(p){
 const c=p.condition,sw=new Set(),v={};
 if(c.switch1_valid)sw.add(c.switch1_id);
 if(c.switch2_valid)sw.add(c.switch2_id);
 if(c.variable_valid)v[c.variable_id]=c.variable_value;
 return {sw,v,self:c.self_switch_valid?c.self_switch_ch:null};
}
export function active(e,s,target){return [...e.pages].reverse().find(p=>{
 const c=p.condition;return (!c.switch1_valid||s.sw.has(c.switch1_id))&&(!c.switch2_valid||s.sw.has(c.switch2_id))&&(!c.variable_valid||(s.v[c.variable_id]||0)>=c.variable_value)&&(!c.self_switch_valid||(e.id===target&&s.self===c.self_switch_ch));
});}
export class Grid {
 constructor(m,s,target){this.m=m;this.t=S.Tilesets[m.tileset_id];this.ev=Object.values(m.events).map(e=>[e,active(e,s,target)]).filter(a=>a[1]);}
 valid(x,y){return x>=0&&y>=0&&x<this.m.width&&y<this.m.height;}
 tiles(x,y){return [2,1,0].map(z=>this.m.data.data[x+y*this.m.width+z*this.m.width*this.m.height]);}
 pass(x,y,d){
  if(!this.valid(x,y))return false;
  const bit=d?(1<<(d/2-1))&15:0;
  const ids=this.ev.filter(([e,p])=>e.x===x&&e.y===y&&!p.through).map(([e,p])=>p.graphic.tile_id).concat(this.tiles(x,y));
  for(const id of ids){const a=this.t.passages.data[id],b=this.t.priorities.data[id];if(a===undefined||(a&bit)||(a&15)===15)return false;if(b===0)return true;}return true;
 }
 step(x,y,d,dx,dy){return this.pass(x,y,d)&&this.pass(x+dx,y+dy,10-d)&&!this.ev.some(([e,p])=>e.x===x+dx&&e.y===y+dy&&!p.through&&p.graphic.character_name);}
 flood(seed){const q=[seed],seen=new Set([seed.join(',')]);for(let n=0;n<q.length;n++){const [x,y]=q[n];for(const [d,dx,dy] of D){const k=[x+dx,y+dy].join(',');if(!seen.has(k)&&this.step(x,y,d,dx,dy)){seen.add(k);q.push([x+dx,y+dy]);}}}return seen;}
 over(e,p){return (!p.graphic.character_name||p.through)&&this.pass(e.x,e.y,0);}
 counter(x,y){return this.valid(x,y)&&this.tiles(x,y).some(id=>this.t.passages.data[id]&128);}
 interact(e,p,seen){if(this.over(e,p))return seen.has([e.x,e.y].join(','));return D.some(([d,dx,dy])=>seen.has([e.x+dx,e.y+dy].join(','))||(this.counter(e.x+dx,e.y+dy)&&seen.has([e.x+2*dx,e.y+2*dy].join(','))));}
}
export const entries={};
function entry(mid,x,y,source){(entries[mid]??=[]).push({x,y,source});}
entry(S.System.start_map_id,S.System.start_x,S.System.start_y,'System');
const pictures=[],providers={items:{},switches:{},variables:{}},requirements={items:new Set(),switches:new Set()};
for(const [mid,m] of maps)for(const e of Object.values(m.events))for(const [pi,p] of e.pages.entries())for(const c of p.list){
 const a=c.parameters,loc={mapa:mid,evento:e.id,pagina:pi+1};
 if(c.code===201&&a[0]===0)entry(a[1],a[2],a[3],loc);
 if([231,232].includes(c.code))pictures.push({...loc,codigo:c.code,parametros:a});
 if(c.code===126&&a[1]===0)(providers.items[a[0]]??=[]).push(loc);
 if(c.code===121&&a[2]===0)for(let i=a[0];i<=a[1];i++)(providers.switches[i]??=[]).push(loc);
 if(c.code===122)for(let i=a[0];i<=a[1];i++)(providers.variables[i]??=[]).push(loc);
 if(c.code===111&&a[0]===8)requirements.items.add(a[1]);
 if(c.code===111&&a[0]===0)requirements.switches.add(a[1]);
}
const errors=[],checks=[],warnings=[];
for(const [mid,m] of maps){
 const seeds=[...new Map((entries[mid]||[]).map(e=>[[e.x,e.y].join(','),e])).values()];
 for(const e of Object.values(m.events))for(const [pi,p] of e.pages.entries()){
  if(p.trigger>2||!p.list.some(c=>![0,108,408].includes(c.code)))continue;
  const st=stateFor(p),g=new Grid(m,st,e.id);
  if(active(e,st,e.id)!==p){warnings.push({mapa:mid,evento:e.id,pagina:pi+1,tipo:'pagina_sombreada_en_estado_minimo'});continue;}
  const results=seeds.map(s=>({desde:[s.x,s.y],alcanzable:g.interact(e,p,g.flood([s.x,s.y]))}));
  const row={mapa:mid,evento:e.id,nombre:e.name,pagina:pi+1,xy:[e.x,e.y],entradas:results};checks.push(row);
  const libre=results.filter(r=>!(mid===2&&['1,4','7,3','10,5'].includes(r.desde.join(','))));
  if(!results.some(r=>r.alcanzable)||libre.some(r=>!r.alcanzable))errors.push({...row,tipo:'interaccion_inaccesible'});
 }
 const g=new Grid(m,{sw:new Set(),v:{},self:null});
 for(const s of seeds){
  const hidden=mid===2&&['1,4','7,3','10,5'].includes([s.x,s.y].join(','));
  if(!g.valid(s.x,s.y)||(!hidden&&!D.some(([d,dx,dy])=>g.step(s.x,s.y,d,dx,dy))))errors.push({mapa:mid,tipo:'destino_sin_salida',entrada:s});
 }
 for(let y=0;y<m.height;y++)for(let x=0;x<m.width;x++){
  const ids=g.tiles(x,y);if(ids.some(id=>id>=384&&g.t.priorities.data[id]>0&&(g.t.passages.data[id]&15)===0))warnings.push({mapa:mid,tipo:'superpuesto_transitable_revisar',xy:[x,y],tiles:ids});
 }
}
// Productores Ruby: las llamadas se conservan como evidencia, no se ejecuta eval.
const sources=fs.readdirSync('diseno/scripts').filter(f=>f.endsWith('.rb')).sort().map(f=>[f,fs.readFileSync('diseno/scripts/'+f,'utf8')]);
const constants={};
for(const [file,src] of sources)for(const m of src.matchAll(/\b([A-Z][A-Z_0-9]+)\s*=\s*(\d+)/g))constants[m[1]]=Number(m[2]);
for(const [file,src] of sources){
 const lines=src.split('\n');
 for(const [i,line] of lines.entries()){
  for(const m of line.matchAll(/\$game_switches\[([^\]]+)\]\s*=\s*(.+)/g)){
   const id=/^\d+$/.test(m[1])?Number(m[1]):constants[m[1].split('::').at(-1)];
   if(id&&m[2].trim()!=='false')(providers.switches[id]??=[]).push({script:file,linea:i+1,expresion:m[2]});
  }
  for(const m of line.matchAll(/gain_item\(\s*(\d+)\s*,\s*([1-9]\d*)/g))(providers.items[Number(m[1])]??=[]).push({script:file,linea:i+1});
 }
}
const missionChecks=[];
for(let id=1;id<=40;id++){
 const list=providers.items[id]||[];
 const reachable=list.filter(loc=>loc.script||checks.some(c=>c.mapa===loc.mapa&&c.evento===loc.evento&&c.pagina===loc.pagina&&c.entradas.some(e=>e.alcanzable))||S['Map'+String(loc.mapa).padStart(3,'0')].events[loc.evento].pages[loc.pagina-1].trigger>=3);
 missionChecks.push({tipo:'objeto',id,proveedores:reachable,ok:reachable.length>0});
 if(!reachable.length)errors.push({tipo:'objeto_sin_proveedor_accesible',id});
}
for(const id of [...requirements.switches].sort((a,b)=>a-b)){
 const list=providers.switches[id]||[];
 missionChecks.push({tipo:'switch',id,proveedores:list,ok:list.length>0});
 if(!list.length)errors.push({tipo:'switch_sin_productor',id});
}
const rulesPath='diseno/herramientas/comun/jugabilidad_reglas.json';
if(fs.existsSync(rulesPath))for(const r of JSON.parse(fs.readFileSync(rulesPath,'utf8')).huellas){
 const m=S['Map'+String(r.mapa).padStart(3,'0')],g=new Grid(m,{sw:new Set(),v:{},self:null});
 if(g.pass(r.x,r.y,0))errors.push({tipo:'mueble_atravesable',...r});
}
const report={version:2,alcance:'Geometría RGSS1 por página y estados mínimos, desde cada entrada libre. Bush 0x40 no bloquea; counter 0x80 extiende interacción. Las prioridades no implican colisión. Productores de misión: evidencia estática de páginas accesibles y asignaciones Ruby; la ejecución de ramas se prueba con recorrido_fase45.rb y prueba_acto6.rb, no mediante esta aproximación estática.',mapas:maps.length,errores_bloqueantes:errors.length,errores:errors,comprobaciones:checks,entradas:entries,advertencias:warnings,misiones:{comprobaciones:missionChecks,proveedores:providers,requeridos:{items:[...requirements.items].sort((a,b)=>a-b),switches:[...requirements.switches].sort((a,b)=>a-b)}},pictures};
fs.mkdirSync('diseno/verificaciones',{recursive:true});
fs.writeFileSync('diseno/verificaciones/auditoria_jugabilidad.json',JSON.stringify(report,null,2)+'\n');
const lines=[`Mapas: ${maps.length}; páginas: ${checks.length}; errores: ${errors.length}; avisos visuales: ${warnings.length}`,...maps.map(([id])=>`Mapa ${id}: ${errors.filter(e=>e.mapa===id).length} errores`),...errors.map(e=>JSON.stringify(e))];
fs.writeFileSync('diseno/verificaciones/auditoria_jugabilidad.txt',lines.join('\n')+'\n');
console.log(lines.slice(0,33).join('\n'));
if(process.argv[1]===path.resolve('diseno/herramientas/comun/auditar_jugabilidad.mjs'))process.exitCode=errors.length?1:0;
