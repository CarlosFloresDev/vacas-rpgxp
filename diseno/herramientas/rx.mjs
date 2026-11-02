// node rx.mjs <tool> '<json>'  |  node rx.mjs --batch file.json  (array of [tool, args])
import { Client } from "file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js";
import { StdioClientTransport } from "file:///D:/DevTools/mcp/rpgmaker-xp/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js";
import fs from "fs";
const transport = new StdioClientTransport({ command: "node", args: ["D:/DevTools/mcp/rpgmaker-xp/node_modules/rpgmaker-xp-mcp/dist/index.js"],
  env: { ...process.env, RPGMAKER_PROJECT_PATH: "D:/descargas/Proyectos personales/Vacas", RPGMAKER_RTP_PATH: "D:/SteamLibrary/steamapps/common/RPGXP/rtp" }, stderr: "ignore" });
const client = new Client({ name: "cli", version: "1.0.0" });
await client.connect(transport);
const a = process.argv.slice(2);
async function call(tool, args) {
  const res = await client.callTool({ name: tool, arguments: args || {} });
  for (const c of res.content) console.log(c.type === "text" ? c.text : `[${c.type}]`);
  if (res.isError) { console.log("!!ERROR in " + tool); }
  return res;
}
if (a[0] === "--list") {
  const { tools } = await client.listTools();
  const name = a[1];
  for (const t of tools) if (!name || name.split(",").includes(t.name)) console.log("## " + t.name + "\n" + t.description + "\n" + (name ? JSON.stringify(t.inputSchema) : ""));
} else if (a[0] === "--batch") {
  const list = JSON.parse(fs.readFileSync(a[1], "utf8"));
  for (const [t, ar] of list) { const r = await call(t, ar); if (r.isError) break; }
} else {
  await call(a[0], a[1] ? JSON.parse(a[1]) : {});
}
await client.close();
