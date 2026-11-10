// Ubicación del proyecto independiente del directorio de trabajo del comando.
import {fileURLToPath} from 'node:url';
export const raiz = fileURLToPath(new URL('../../../', import.meta.url));
export const ruta = relativa => fileURLToPath(new URL('../../../' + relativa, import.meta.url));
export const sinCabecera = bytes => Buffer.from(Buffer.from(bytes).toString('utf8').replace(/^# === VACAS: FUENTE VIGENTE ===\r?\n[\s\S]*?# === FIN CABECERA ===\r?\n/,''));
