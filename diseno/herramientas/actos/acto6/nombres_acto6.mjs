import {raiz as _raiz, ruta as _ruta} from '../../comun/proyecto.mjs';
process.chdir(_raiz);
import {readRxdataFile as read,writeRxdataFile as write} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
const p='Data/MapInfos.rxdata';const infos=await read(p);
const names=['Túneles profundos: la raíz','Ciudad tomada: el nuevo turno','El piso: la última cena','Galería de compuertas','Rey-dios: el altar'];
names.forEach((n,i)=>{infos[i+28].name=n;});await write(p,infos);
console.log('Nombres Unicode de mapas 28-32 instalados.');
