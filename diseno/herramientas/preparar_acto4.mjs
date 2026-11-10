import {readRxdataFile,writeRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const s=await readRxdataFile('Data/System.rxdata');
while(s.switches.length<=144)s.switches.push('');
while(s.variables.length<=56)s.variables.push('');
await writeRxdataFile('Data/System.rxdata',s);
const sets=await readRxdataFile('Data/Tilesets.rxdata');
if(!sets[68]){
 const t=structuredClone(sets[51]);
 t.id=68;t.name='Acto IV: alcantarillas';t.tileset_name='acto4_alcantarillas';
 t.autotile_names=['','','','','','',''];t.panorama_name='';
 t.fog_name='002-Clouds01';t.fog_opacity=24;t.fog_zoom=200;t.fog_sx=1;t.fog_sy=-1;
 t.battleback_name='mente_tunel';
 for(const key of ['passages','priorities','terrain_tags']){
  t[key]={_class:'Table',dim:1,xsize:416,ysize:1,zsize:1,data:new Array(416).fill(0)};
 }
 t.priorities.data[0]=5;
 for(const n of [4,5,6,7,11,12,15])t.passages.data[384+n]=15;
 for(const n of [8,10,13,14])t.priorities.data[384+n]=1;
 sets[68]=t;
 await writeRxdataFile('Data/Tilesets.rxdata',sets);
}
console.log('A4: System ampliado; tileset 68 preparado con colisiones explicitas.');
for(const [name,last] of [['Items',34],['Enemies',17],['Troops',17]]){
 const d=await readRxdataFile('Data/'+name+'.rxdata');
 while(d.length<=last){const v=structuredClone(d[d.length-1]);v.id=d.length;d.push(v);}
 await writeRxdataFile('Data/'+name+'.rxdata',d);
}
