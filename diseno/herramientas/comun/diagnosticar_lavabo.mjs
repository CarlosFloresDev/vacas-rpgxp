// Evidencia del bug original sin restaurar ni modificar datos del juego.
import fs from 'node:fs';
import {S,Grid,stateFor} from './auditar_jugabilidad.mjs';
import {readRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const result={};
for(const [label,dir] of [['antes','diseno/respaldos/antes_jugabilidad/Data'],['actual','Data']]){
  S.Map002=await readRxdataFile(dir+'/Map002.rxdata');
  S.Tilesets=await readRxdataFile(dir+'/Tilesets.rxdata');
  const m=S.Map002,e=m.events[11],g=new Grid(m,stateFor(e.pages[0]),11);
  const seen=g.flood([6,12]);
  result[label]={tileset:m.tileset_id,lavabo:{xy:[e.x,e.y],paginas:e.pages.map(p=>({condicion:p.condition,grafico:p.graphic,through:p.through,trigger:p.trigger,comandos:p.list}))},
    aproximacion_13_4:seen.has('13,4'),interaccion:g.interact(e,e.pages[0],seen),
    tiles:[3,4,5].map(y=>({xy:[13,y],capas:g.tiles(13,y),pasable:g.pass(13,y,0)})),
    bloqueador49:{xy:[m.events[49].x,m.events[49].y],paginas:m.events[49].pages.map(p=>({through:p.through,condicion:p.condition}))}};
}
fs.writeFileSync('diseno/verificaciones/diagnostico_lavabo.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(Object.fromEntries(Object.entries(result).map(([k,v])=>[k,{aproximacion:v.aproximacion_13_4,interaccion:v.interaccion}]))));
