// Solo administra su propio Game.exe; no busca ni cierra procesos ajenos.
import fs from 'node:fs';import {spawn} from 'node:child_process';import zlib from 'node:zlib';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=fileURLToPath(new URL('../../',import.meta.url));
const path=root+'Data/Scripts.rxdata',original=fs.readFileSync(path);
const retained=['Vacas_finales.dat','Vacas_finales.tmp'].map(p=>[root+p,fs.existsSync(root+p)?fs.readFileSync(root+p):null]);
const cfg=fs.readFileSync(root+'Vacas.cfg');
const rows=load(original,{string:'binary',hash:'map'});
const main=rows.findIndex(r=>Buffer.from(r[1]).toString()==='Main');
rows[main][2]=zlib.deflateSync(fs.readFileSync(new URL('prueba_acto6.rb',import.meta.url)));
try{
 fs.writeFileSync(path,dump(rows));
 const proc=spawn(root+'Game.exe',[],{cwd:root,windowsHide:true,stdio:'ignore'});
 const result=await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{proc.kill();resolve('timeout 120s');},120000);
  proc.on('error',e=>{clearTimeout(timer);reject(e);});
  proc.on('exit',n=>{clearTimeout(timer);resolve('exit '+n);});
 });
 console.log('Game.exe propio: '+result);
 const log=fs.readFileSync(root+'diseno/verificacion_rgss_acto6.txt','utf8');
 console.log(log.split('\n').slice(-8).join('\n'));
 if(!log.includes('OK FIN: Acto VI verificado con RGSS real') || /^FALLO /m.test(log))throw Error('Fallo RGSS: consultar verificacion_rgss_acto6.txt');
}finally{
 fs.writeFileSync(path,original);
 for(const [p,bytes] of retained){if(bytes===null){if(fs.existsSync(p))fs.unlinkSync(p);}else fs.writeFileSync(p,bytes);}
 if(!cfg.equals(fs.readFileSync(root+'Vacas.cfg')))throw Error('Vacas.cfg cambió durante el arnés');
 console.log('Scripts y archivo de finales restaurados; Vacas.cfg idéntico.');
}
