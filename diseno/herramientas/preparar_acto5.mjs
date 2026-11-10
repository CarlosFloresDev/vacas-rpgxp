// Acto V: amplia System, reserva objetos y clona el tileset 51 como 69. Idempotente.
import {readRxdataFile,writeRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const s=await readRxdataFile('../../Data/System.rxdata');
while(s.switches.length<=175)s.switches.push('');
while(s.variables.length<=64)s.variables.push('');
await writeRxdataFile('../../Data/System.rxdata',s);
const sets=await readRxdataFile('../../Data/Tilesets.rxdata');
if(!sets[69]){
 const t=structuredClone(sets[51]);
 t.id=69;t.name='Acto V: la matanza';t.tileset_name='acto5_matanza';
 t.fog_name='002-Clouds01';t.fog_opacity=22;t.fog_zoom=200;t.fog_sx=1;t.fog_sy=0;
 sets[69]=t;
 await writeRxdataFile('../../Data/Tilesets.rxdata',sets);
}
const d=await readRxdataFile('../../Data/Items.rxdata');
while(d.length<=38){const v=structuredClone(d[d.length-1]);v.id=d.length;d.push(v);}
await writeRxdataFile('../../Data/Items.rxdata',d);
console.log('A5: System 175/64, tileset 69, objetos hasta 38.');
