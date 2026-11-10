import {raiz as _raiz, ruta as _ruta} from '../../comun/proyecto.mjs';
process.chdir(_raiz);
// Codec Marshal del MCP, con respaldo de escritura del mismo proveedor.
import {readRxdataFile,writeRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
import {fileURLToPath} from 'url';
const p=fileURLToPath(new URL('../../../../Data/System.rxdata',import.meta.url));
const s=await readRxdataFile(p);
while(s.switches.length<=112)s.switches.push('');
await writeRxdataFile(p,s);
console.log('System: 112 interruptores; rangos previos intactos.');
