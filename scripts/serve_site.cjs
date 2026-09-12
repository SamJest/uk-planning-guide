// Local production-style static preview: compression, MIME types and real 404s.
const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const zlib = require('node:zlib');
const {promisify} = require('node:util');
const gzip = promisify(zlib.gzip);
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8',
  '.js':'text/javascript; charset=utf-8','.json':'application/json','.svg':'image/svg+xml',
  '.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.xml':'application/xml',
  '.txt':'text/plain; charset=utf-8','.pdf':'application/pdf','.ico':'image/x-icon'};
function createSiteServer(directory) {
  const root = path.resolve(directory);
  return http.createServer(async (req,res) => {
    if (!['GET','HEAD'].includes(req.method)) {res.writeHead(405);res.end();return;}
    try {
      const pathname = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
      const parts = pathname.split(/[\\/]/);
      if(parts.some(p => p.startsWith('.') && p !== '.well-known')) throw Error('Invalid path');
      let file = path.resolve(root,'.' + pathname);
      if(!file.startsWith(root + path.sep) && file !== root) throw Error('Outside root');
      let status = 200;
      try {
        const info = await fs.stat(file);
        if(info.isDirectory()) {
          if(!pathname.endsWith('/')) {res.writeHead(301,{Location:pathname+'/'});res.end();return;}
          file = path.join(file,'index.html');
        }
        await fs.access(file);
      } catch { file = path.join(root,'404.html'); status = 404; }
      let body = await fs.readFile(file);
      const type = types[path.extname(file)] || 'application/octet-stream';
      const headers = {'Content-Type':type,'Vary':'Accept-Encoding','X-Content-Type-Options':'nosniff'};
      if(/\bgzip\b/.test(req.headers['accept-encoding'] || '') && /text|json|xml|svg/.test(type)) {
        body = await gzip(body); headers['Content-Encoding'] = 'gzip';
      }
      headers['Content-Length'] = body.length;
      res.writeHead(status,headers);res.end(req.method === 'HEAD' ? undefined : body);
    } catch { res.writeHead(404,{'Content-Type':'text/plain'});res.end('Not found'); }
  });
}
if(require.main === module) {
  const directory = process.argv[2] || 'artifacts/phase-0-canary-site';
  const port = Number(process.argv[3] || 8765);
  createSiteServer(directory).listen(port,'127.0.0.1',()=>console.log(`Serving ${directory} at http://127.0.0.1:${port}`));
}
module.exports = {createSiteServer};
