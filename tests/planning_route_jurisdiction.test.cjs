const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const code=fs.readFileSync('assets/js/planning-route-check.js','utf8').replace('  if (document.readyState === "loading") {','  window.testRoute = {evaluateRoute, renderResult};\n  if (document.readyState === "loading") {');
const sandbox={window:{},document:{readyState:'loading',addEventListener(){}}};
vm.runInNewContext(code,sandbox);
const {evaluateRoute,renderResult}=sandbox.window.testRoute;
const base={project_type:'single-storey-extension',property_type:'detached-house',restrictions:[],postcode_or_town:'Example town'};
test('NI and missing jurisdictions do not inherit a GB route',()=>{
  for(const jurisdiction of ['northern-ireland','',undefined]){
    const result=evaluateRoute({...base,jurisdiction});
    assert.equal(result.unsupported,true);
    assert.doesNotMatch(renderResult(result,base),/href="\/councils\//);
  }
  assert.equal(evaluateRoute({...base,jurisdiction:'england',postcode_or_town:'BT1 1AA'}).unsupported,true);
});
test('supported jurisdictions retain the route checker without an unverified high rating',()=>{
  for(const jurisdiction of ['england','wales','scotland']){
    const answers={...base,jurisdiction}; const result=evaluateRoute(answers);
    assert.notEqual(result.unsupported,true);
    assert.equal(result.confidence,'Low');
    assert.doesNotMatch(renderResult(result,answers),/route-confidence/);
  }
});
