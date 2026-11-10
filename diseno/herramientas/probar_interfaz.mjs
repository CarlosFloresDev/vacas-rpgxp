// Prueba exclusiva; restaura byte por byte Scripts.rxdata aunque falle Game.exe.
import fs from 'node:fs';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import zlib from 'node:zlib';
import {load,dump} from 'file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/vendor/marshal/index.js';
const root=fileURLToPath(new URL('../../',import.meta.url));
const scripts=root+'Data/Scripts.rxdata';
const original=fs.readFileSync(scripts);
const rows=load(original,{string:'binary',hash:'map'});
const last=rows.findIndex(r=>Buffer.from(r[1]).toString()==='Main');
const source=fs.readFileSync(new URL(process.argv[2] || 'prueba_interfaz.rb',import.meta.url),'utf8');
// Cada script registra carga/errores: diagnostica tambien fallos anteriores a Main.
for(let i=0;i<rows.length;i++){
 const code=i===last?source:zlib.inflateSync(rows[i][2]).toString();
 rows[i][2]=zlib.deflateSync(Buffer.from('begin\nFile.open("diseno/ui_carga.txt","a") { |f| f.puts("Script '+i+'") }\n'+code+'\nrescue Exception => e\nFile.open("diseno/ui_carga.txt","a") { |f| f.puts(e.class.to_s+": "+e.message); f.puts(e.backtrace) }\nraise\nend\n'));
}
try {
 fs.writeFileSync(root+'diseno/ui_carga.txt','');
 fs.writeFileSync(scripts,dump(rows));
 const p=spawn(root+'Game.exe',[],{cwd:root,windowsHide:true,stdio:'ignore'});
 const result=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>{p.kill();resolve('timeout 180s');},180000);
   p.on('error',reject);p.on('exit',n=>{clearTimeout(timer);resolve('exit '+n);});
 });
 console.log('Game.exe: '+result);
 console.log(fs.readFileSync(root+'diseno/ui_carga.txt','utf8').split('\n').slice(-15).join('\n'));
 if(fs.existsSync(root+'diseno/verificacion_interfaz.txt'))console.log(fs.readFileSync(root+'diseno/verificacion_interfaz.txt','utf8').split('\n').slice(-15).join('\n'));
 if(!process.argv[2]) {
   const log=fs.readFileSync(root+'diseno/verificacion_interfaz.txt','utf8');
   if(!log.includes('OK FIN INTERFAZ RGSS104E') || log.includes('FALLO '))throw Error('Fallo de integracion RGSS; consultar verificacion_interfaz.txt');
 }
} finally {
 fs.writeFileSync(scripts,original);
 console.log('Scripts.rxdata restaurado byte por byte.');
}
