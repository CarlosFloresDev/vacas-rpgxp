import {raiz as _raiz, ruta as _ruta} from '../../comun/proyecto.mjs';
process.chdir(_raiz);
// Instala temporalmente el arnes en Main y lo restaura incluso si Game falla.
import fs from 'fs';
import {spawn} from 'child_process';
import {Client} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import {StdioClientTransport} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
import {fileURLToPath} from 'url';
const root=fileURLToPath(new URL('../../../../',import.meta.url));
const snap=JSON.parse(fs.readFileSync(new URL('../../../verificaciones/inventario/snapshot.json',import.meta.url),'utf8'));
const main=snap.Scripts.find(s=>s.name==='Main');
const transport=new StdioClientTransport({command:'node',args:['D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/index.js'],env:{...process.env,RPGMAKER_PROJECT_PATH:root,RPGMAKER_RTP_PATH:'D:/SteamLibrary/steamapps/common/RPGXP/rtp'},stderr:'ignore'});
const c=new Client({name:'prueba-rgss',version:'1.0.0'});
await c.connect(transport);
try{
 const logPath=root+'diseno/verificaciones/verificacion_rgss_acto3.txt';
 fs.writeFileSync(logPath,'');
 const code=fs.readFileSync(_ruta('diseno/herramientas/actos/acto3/prueba_acto3.rb'),'utf8').replace(/^\uFEFF/,'');
 await c.callTool({name:'update_script',arguments:{index:main.index,code}});
 const proc=spawn(root+'Game.exe',[],{cwd:root,windowsHide:true,stdio:'ignore'});
 const result=await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{proc.kill();resolve('timeout 45s');},45000);
  proc.on('error',e=>{clearTimeout(timer);reject(e)});
  proc.on('exit',n=>{clearTimeout(timer);resolve('exit '+n)});
 });
 console.log('Game.exe: '+result);
 const log=fs.readFileSync(logPath,'utf8');
 if(!log.includes('OK FIN: Acto III verificado con RGSS104E real') || /^FALLO /m.test(log)){
  throw new Error('La prueba RGSS no terminó correctamente; revisar '+logPath);
 }
}finally{
 await c.callTool({name:'update_script',arguments:{index:main.index,code:main.code}});
 await c.close();
 console.log('Main restaurado.');
}

