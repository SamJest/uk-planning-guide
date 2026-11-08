import { readFileSync } from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const { primary_routes: routes } = JSON.parse(readFileSync('data/canary/wave1-corpus.json', 'utf8'));
const records = JSON.parse(readFileSync('data/canary/page-records.json', 'utf8'));
for (const route of routes) {
  test(`${route} evidence labels and responsive reading`, async ({ page }, testInfo) => {
    const record = records.find(p => p.route_path === route);
    await page.goto(route);
    for (const claim of record.claims) {
      const nodes = page.locator(`[data-claim-id="${claim.claim_id}"]`);
      expect(await nodes.count()).toBeGreaterThan(0);
      for (const node of await nodes.all()) {
        await expect(node).toHaveAttribute('data-evidence-status', claim.evidence_status);
        await expect(node).toContainText(claim.text);
        await expect(node).toContainText(claim.evidence_status === 'verified' ? 'Evidence checked.' : 'Not verified.');
      }
    }
    await page.keyboard.press('Tab');
    expect(await page.evaluate(() => document.activeElement?.tagName)).not.toBe('BODY');
    expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze()).violations).toEqual([]);
    for (const width of [320, 360, 768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
      if (testInfo.project.name === 'desktop-chromium') {
        await testInfo.attach(`evidence-${width}`, { body: await page.screenshot({ fullPage: true, animations: 'disabled' }), contentType: 'image/png' });
      }
    }
  });
}
