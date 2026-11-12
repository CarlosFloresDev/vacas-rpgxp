// Captura nativa aislada: solo modifica temporalmente mkxp.json.
import fs from 'node:fs';
import {spawn,spawnSync} from 'node:child_process';
import crypto from 'node:crypto';
import {raiz} from './proyecto.mjs';
process.chdir(raiz);
const config=fs.readFileSync('mkxp.json');
const files=['Game.exe','Vacas.cfg','Save1.rxdata',...fs.readdirSync('Data').filter(x=>x.endsWith('.rxdata') && x!=='Scripts.rxdata').map(x=>'Data/'+x)];
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const before=Object.fromEntries(files.map(p=>[p,hash(p)]));
let proc,timer;
const started=Date.now();
const lock='diseno/verificaciones/ui_captura.lock';
const lockFd=fs.openSync(lock,'wx');
fs.writeFileSync(lockFd,config);fs.closeSync(lockFd);
const stop=()=>proc?.kill();
process.on('SIGINT',stop);process.on('SIGTERM',stop);
try {
 const settings=JSON.parse(config);
 Object.assign(settings,{customScript:'diseno/herramientas/comun/capturar_ui.rb',fullscreen:false,defScreenW:1280,defScreenH:720,dataPathOrg:'Vacas',dataPathApp:'Auditoria'});
 fs.writeFileSync('mkxp.json',JSON.stringify(settings,null,2));
 const log=fs.createWriteStream('diseno/verificaciones/ui_motor.log');
 fs.mkdirSync('diseno/verificaciones/ui_runtime',{recursive:true});
 proc=spawn(raiz+'Vacas.exe',[],{cwd:raiz,windowsHide:true,env:{...process.env,APPDATA:raiz+'diseno/verificaciones/ui_runtime',LOCALAPPDATA:raiz+'diseno/verificaciones/ui_runtime',SDL_AUDIODRIVER:'dummy',ALSOFT_DRIVERS:'null'},stdio:['ignore','pipe','pipe']});
 proc.stdout.pipe(log);proc.stderr.pipe(log);
 console.log('Vacas.exe propio: '+proc.pid);
 timer=setTimeout(()=>proc.kill(),180000);
 await new Promise((resolve,reject)=>{proc.on('error',reject);proc.on('exit',resolve);});
 log.end();
} finally {
 clearTimeout(timer);
 fs.writeFileSync('mkxp.json',config);
 fs.unlinkSync(lock);
 process.off('SIGINT',stop);process.off('SIGTERM',stop);
 const changed=files.filter(p=>before[p]!==hash(p));
 fs.writeFileSync('diseno/verificaciones/ui_integridad.json',JSON.stringify({before,changed},null,2));
 if(changed.length)throw Error('Cambios protegidos: '+changed);
 console.log('mkxp.json restaurado; archivos protegidos intactos.');
}
const reportPath='diseno/verificaciones/auditoria_ui.json';
const fresh=fs.existsSync(reportPath) && fs.statSync(reportPath).mtimeMs>=started;
const report=fresh ? JSON.parse(fs.readFileSync(reportPath,'utf8')) : null;
if(!report?.motor_real || !report.pantallas?.length){
 console.error('No se generaron capturas nativas. Consulte diseno/verificaciones/ui_motor.log.');
 process.exitCode=1;
} else {
 const result=spawnSync('python',['diseno/herramientas/comun/lamina_ui.py'],{stdio:'inherit'});
 const metricErrors=report.pantallas.reduce((n,p)=>n+[...p.ventanas,...(p.sprites || [])].reduce((m,w)=>m+w.errores.length,0),0);
 process.exitCode=result.status ?? 1;
 if(report.errores.length || metricErrors)process.exitCode=1;
}

