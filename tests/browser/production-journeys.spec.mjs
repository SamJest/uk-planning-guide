import {test, expect} from '@playwright/test';
import fs from 'node:fs/promises';

test('measurement calculator rejects missing data and routes other nations separately', async ({page}) => {
  await page.goto('/tools/permitted-development-calculator/');
  await page.locator('#pd-check-button').click();
  await expect(page.locator('#result')).toContainText('Select a nation');
  await page.locator('#pdJurisdiction').selectOption('england');
  await page.locator('#pd-check-button').click();
  await expect(page.locator('#result')).toContainText('Enter valid measurements');
  for(const [id,value] of Object.entries({depth:'2.5',height:'3.5',eavesHeight:'2.8',boundary:'1'})) await page.locator('#'+id).fill(value);
  await page.locator('#pd-check-button').click();
  await expect(page.locator('#result')).toContainText('No issue in these measurements');
  for(const nation of ['wales','scotland','northern-ireland']) {
    await page.locator('#pdJurisdiction').selectOption(nation);
    await page.locator('#pd-check-button').click();
    await expect(page.locator('#result')).toContainText("Use your nation's guidance");
    await expect(page.locator('#result')).not.toContainText('No issue in these measurements');
  }
});

test('detailed decision tool requires an explicit nation', async ({page}) => {
  await page.goto('/tools/planning-decision-tool/');
  const engine = page.locator('#planning-decision-engine');
  await engine.locator('[data-action="choose-jurisdiction"][data-value="wales"]').click();
  await expect(engine).toContainText('No English rule assessment has been made');
  await expect(engine.locator('[data-action="choose-project"]')).toHaveCount(0);
  await engine.locator('[data-action="choose-jurisdiction"][data-value="england"]').click();
  await expect(engine.locator('[data-action="choose-project"]:visible').first()).toBeVisible();
});

test('guidance form prepares a draft without reporting delivery', async ({page}) => {
  await page.goto('/personalised-planning-guidance/request/');
  const form = page.locator('form[data-guidance-form]');
  for(const select of await form.locator('select[required]').all()) await select.selectOption({index:1});
  for(const input of await form.locator('input[required], textarea[required]').all()) {
    if(await input.getAttribute('type') === 'checkbox') await input.check();
    else await input.fill(await input.getAttribute('type') === 'email' ? 'test@example.com' : 'Test project details');
  }
  await form.locator('button[type="submit"]').click();
  await expect(form.locator('[data-email-draft]')).toContainText('Nothing has been sent yet');
  await expect(form.locator('[data-email-draft] a')).toHaveAttribute('href', /^mailto:guidance@ukplanningguide\.co\.uk\?/);
  await expect(page).not.toHaveURL(/success/);
});

test('sticky save persists a page and export downloads its summary', async ({page}, testInfo) => {
  await page.goto('/tools/');
  if(testInfo.project.name === 'desktop-chromium') {
    await expect(page.locator('[data-sticky-action-bar]')).toBeHidden();
    await page.setViewportSize({width:390,height:844});
  }
  await page.locator('[data-sticky-action="summary_saved"]').click();
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('ukpg:planning-workspace:v1')).saved_pages.some(p => p.path === '/tools/'))).toBe(true);
  const downloadEvent = page.waitForEvent('download');
  await page.locator('[data-sticky-action="council_pack_downloaded"]').click();
  const download = await downloadEvent;
  expect(download.suggestedFilename()).toBe('uk-planning-project-summary.txt');
  const text = await fs.readFile(await download.path(), 'utf8');
  expect(text).toContain('/tools/');
  await page.goto('/my-planning-project/');
  await expect(page.locator('main a[href="/tools/"]').first()).toBeVisible();
});

for (const nation of ['england','wales','scotland','northern-ireland']) {
  test(`route checker completes a real ${nation} journey`, async ({page}) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('/england/tools/planning-route-check/');
    const form = page.locator('#planning-route-check-form');
    await form.locator('[name="project_type"]').selectOption('single-storey-extension');
    await form.locator('[name="property_type"]').selectOption('detached-house');
    await form.locator('[name="jurisdiction"]').selectOption(nation);
    await form.locator('[name="postcode_or_town"]').fill(nation === 'northern-ireland' ? 'BT1 1AA' : 'Example town');
    await form.locator('[name="timeframe"]').selectOption('researching');
    await form.locator('[name="desired_help"]').selectOption('route-only');
    await form.locator('button[type="submit"]').click();
    const result = page.locator('#planning-route-result');
    await expect(result).toBeVisible();
    if(nation === 'northern-ireland') {
      await expect(result.locator('a')).toHaveAttribute('href', /nidirect.gov.uk/);
      await expect(page.locator('#planning-route-help')).toBeHidden();
    } else {
      await expect(result.locator('h2').first()).toHaveText('Planning permission may be needed');
      await expect(result).not.toContainText('Confidence: High');
      await expect(page.locator('#planning-help-form')).toBeVisible();
      if(nation === 'england') {
        const help = page.locator('#planning-help-form');
        await help.locator('[name="name"]').fill('Test User');
        await help.locator('[name="email"]').fill('test@example.com');
        await help.locator('[name="consent_contact"]').check();
        await page.waitForTimeout(2600);
        await help.locator('button[type="submit"]').click();
        const draft = page.locator('#lead-fallback');
        await expect(draft).toContainText('Nothing has been sent yet');
        await expect(draft.locator('a')).toHaveAttribute('href', /^mailto:guidance%40ukplanningguide\.co\.uk/);
        await expect(page).toHaveURL(/planning-route-check/);
      }
    }
    await form.locator('button[type="reset"]').click();
    await expect(result).toBeHidden();
    expect(errors).toEqual([]);
  });
}
