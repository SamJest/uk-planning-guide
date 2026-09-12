const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const {createSiteServer} = require('../scripts/serve_site.cjs');
test('preview serves compressed content, canonical directory URLs and real missing-page status', async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(),'ukpg-preview-'));
  const server = createSiteServer(dir);
  try {
    await fs.mkdir(path.join(dir,'guide'));
    await fs.writeFile(path.join(dir,'guide','index.html'),'<h1>Guide</h1>');
    await fs.writeFile(path.join(dir,'404.html'),'<h1>Not found</h1>');
    await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
    const base = 'http://127.0.0.1:'+server.address().port;
    const page = await fetch(base+'/guide/');
    assert.equal(page.status,200);
    assert.equal(page.headers.get('content-encoding'),'gzip');
    assert.equal(await page.text(),'<h1>Guide</h1>');
    assert.equal((await fetch(base+'/guide',{redirect:'manual'})).status,301);
    assert.equal((await fetch(base+'/missing/')).status,404);
    assert.equal((await fetch(base+'/.git/config')).status,404);
  } finally {
    await new Promise(resolve => server.close(resolve));
    await fs.rm(dir,{recursive:true});
  }
});
