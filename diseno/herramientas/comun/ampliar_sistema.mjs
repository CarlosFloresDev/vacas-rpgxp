import {raiz as _raiz, ruta as _ruta} from './proyecto.mjs';
process.chdir(_raiz);
// Extension del sistema usando el codec Marshal oficial del MCP.
import {readRxdataFile,writeRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
import {fileURLToPath} from 'url';
const p=fileURLToPath(new URL('../../../Data/System.rxdata',import.meta.url));
const s=await readRxdataFile(p);
while(s.switches.length<=80)s.switches.push('');
await writeRxdataFile(p,s);
console.log('System: '+(s.switches.length-1)+' interruptores disponibles.');
