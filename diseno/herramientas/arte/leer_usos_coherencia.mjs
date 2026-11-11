// Solo lectura de Marshal. Nunca importa constructores ni escribe Data.
import {readRxdataFile} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/utils/rxdata.js';
import fs from 'node:fs';
const result={};
for(const name of fs.readdirSync('Data').filter(n=>n.endsWith('.rxdata') && n!=='Scripts.rxdata')){
  result[name.slice(0,-7)]=await readRxdataFile('Data/'+name);
}
fs.writeFileSync('diseno/verificaciones/coherencia_datos_lectura.json',JSON.stringify(result));
