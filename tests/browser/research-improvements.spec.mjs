import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const slug of ['fences-and-walls','driveways','solar-panels','garden-rooms']) {
  test(`${slug} survey remains readable and downloadable`,async ({page})=>{
    await page.route('https://www.googletagmanager.com/**',route=>route.abort());
    expect((await page.goto(`/${slug}/`,{waitUntil:'domcontentloaded'})).status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    const section=page.locator('#project-evidence-checklist');
    await expect(section).toBeVisible();
    await expect(section.locator('dt')).toHaveCount(4);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
    const axe=await new AxeBuilder({page}).include('#project-evidence-checklist').analyze();
    expect(axe.violations).toEqual([]);
    const response=await page.request.get(`/downloads/${slug}-survey.txt`);
    expect(response.status()).toBe(200);
    expect(await response.text()).toContain('Authority response, source document and date:');
  });
}

test('Tamworth enquiry has evidence steps without a guessed risk score',async({page})=>{
  await page.goto('/hmos/staffordshire/tamworth/article-4/',{waitUntil:'domcontentloaded'});
  const section=page.locator('#scenario-summary');
  await expect(section).toContainText('Existing lawful use');
  await expect(section).toContainText('boundary map');
  await expect(section).not.toContainText('Likely risk level');
  const axe=await new AxeBuilder({page}).include('#scenario-summary').analyze();
  expect(axe.violations).toEqual([]);
});
