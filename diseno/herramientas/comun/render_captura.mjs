// Lee Data/Graphics/RTP y escribe solamente la captura indicada.
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {raiz, ruta} from './proyecto.mjs';
const mapId=Number(process.argv[2] || 1);
if(!Number.isInteger(mapId) || mapId<1)throw Error('Indicar un ID de mapa positivo');
const dest=path.resolve(raiz,process.argv[3] || `diseno/capturas/actos/comprobacion_mapa${mapId}.png`);
const base=path.resolve(raiz,'diseno/capturas');
if(!dest.startsWith(base+path.sep) || path.extname(dest)!=='.png')throw Error('La salida debe ser un PNG dentro de diseno/capturas/');
fs.mkdirSync(path.dirname(dest),{recursive:true});
const result=spawnSync(process.execPath,[ruta('diseno/herramientas/comun/rx.mjs'),'render_map',JSON.stringify({mapId,drawEvents:true,outPath:dest})],{cwd:raiz,encoding:'utf8',windowsHide:true});
process.stdout.write(result.stdout || '');process.stderr.write(result.stderr || '');
if(result.error)throw result.error;
process.exitCode=result.status ?? 1;
