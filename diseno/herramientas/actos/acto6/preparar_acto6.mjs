import {raiz as _raiz, ruta as _ruta} from '../../comun/proyecto.mjs';
process.chdir(_raiz);
// Reservas posteriores a la BD real: no reemplazar los enemigos RTP 22-32.
import {readRxdataFile as read,writeRxdataFile as write} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const root=new URL('../../../../Data/',import.meta.url);
const p=n=>decodeURIComponent(new URL(n+'.rxdata',root).pathname).replace(/^\//,'');
const s=await read(p('System'));
while(s.switches.length<=199)s.switches.push('');
while(s.variables.length<=69)s.variables.push('');
await write(p('System'),s);
const sets=await read(p('Tilesets'));
if(!sets[70]){sets[70]=structuredClone(sets[69]);Object.assign(sets[70],{id:70,name:'Acto VI: Rey-dios',tileset_name:'acto6_reydios',fog_opacity:12});await write(p('Tilesets'),sets);}
for(const [kind,max] of [['Items',40],['Enemies',37],['Troops',37]]){
 const d=await read(p(kind));
 while(d.length<=max){const v=structuredClone(d[kind==='Items'?29:13]);v.id=d.length;d.push(v);}
 await write(p(kind),d);
}
console.log('A6 reservado: mapas desde 28, tileset70, sw176-199, vars65-69, items39-40, enemigos/tropas33-37.');
