import {raiz as _raiz, ruta as _ruta} from '../comun/proyecto.mjs';
process.chdir(_raiz);
import fs from 'fs';
import path from 'path';
import {readRxdataFile,writeRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const root=_raiz;
const patches=JSON.parse(fs.readFileSync('diseno/archivo/herramientas/revision_patch.json','utf8'));
const ts=await readRxdataFile(path.join(root,'Data/Tilesets.rxdata'));
for(const [key,value] of Object.entries(patches)){
 if(key.startsWith('Tileset'))ts[value.id]=value;
 else await writeRxdataFile(path.join(root,'Data',key+'.rxdata'),value);
}
await writeRxdataFile(path.join(root,'Data/Tilesets.rxdata'),ts);
console.log('Mapas y tilesets guardados con el codec RGSS existente.');
