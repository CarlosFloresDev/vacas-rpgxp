// Un solo proceso Vacas.exe. No abre/cierra Game.exe ni escribe Vacas.cfg.
import fs from 'node:fs';
import {spawn} from 'node:child_process';
import crypto from 'node:crypto';
import {raiz} from './proyecto.mjs';
process.chdir(raiz);
const path='mkxp.json',config=fs.readFileSync(path);
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const protectedFiles=['Game.exe','RGSS104E.dll','Game.ini','Vacas.cfg','Save1.rxdata'];
const before=Object.fromEntries(protectedFiles.map(p=>[p,hash(p)]));
let proc;
try {
 const settings=JSON.parse(config);
 settings.customScript='diseno/herramientas/comun/arranque_prueba_hd.rb';
 fs.writeFileSync(path,JSON.stringify(settings,null,2));
 proc=spawn(raiz+'Vacas.exe',[],{cwd:raiz,windowsHide:true,stdio:['ignore','pipe','pipe']});
 const log=fs.createWriteStream('diseno/verificaciones/hd_motor.log');
 proc.stdout.pipe(log);proc.stderr.pipe(log);
 console.log('Unico Vacas.exe propio, PID '+proc.pid);
 const timer=setTimeout(()=>proc.kill(),600000);
 await new Promise((resolve,reject)=>{proc.on('error',reject);proc.on('exit',code=>{console.log('Salida '+code);resolve();});});
 clearTimeout(timer);log.end();
} finally {
 fs.writeFileSync(path,config);
 const changed=protectedFiles.filter(p=>before[p]!==hash(p));
 fs.writeFileSync('diseno/verificaciones/hd_integridad.json',JSON.stringify({before,changed},null,2));
 if(changed.length)throw Error('Archivos protegidos cambiados: '+changed);
 console.log('Configuracion HD restaurada. Archivos protegidos identicos.');
}
