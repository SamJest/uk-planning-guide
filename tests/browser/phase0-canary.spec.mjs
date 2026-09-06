import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(
  readFileSync(path.resolve(here, '../../data/canary/routes.json'), 'utf8')
);
const routes = manifest.publish_routes;
const records = JSON.parse(
  readFileSync(path.resolve(here, '../../data/canary/page-records.json'), 'utf8')
);
const byPath = new Map(records.map((record) => [record.route_path, record]));
const visualRoutes = new Set([
  '/permitted-development/north-yorkshire/',
  '/conservation-areas/glasgow-city/',
  '/councils/sheffield/',
  '/tools/'
]);

for (const route of routes) {
  test(`${route} contract, keyboard, accessibility and visual`, async ({ page }, testInfo) => {
    const response = await page.goto(route, { waitUntil: 'domcontentloaded' });
    expect(response?.status()).toBe(200);

    const record = byPath.get(route);
    expect(record, `Missing record for ${route}`).toBeTruthy();
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      new RegExp(`${record.canonical_path.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`)
    );
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('main')).toBeVisible();

    const robotsMeta = page.locator('meta[name="robots"]');
    const robots = (await robotsMeta.count()) ? (await robotsMeta.getAttribute('content')) || '' : '';
    expect(robots.toLowerCase().includes('noindex')).toBe(record.index_status === 'noindex');

    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.tagName || '');
    expect(focused).not.toBe('BODY');

    const axe = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(axe.violations).toEqual([]);

    if (visualRoutes.has(route)) {
      const slug = route.replace(/^\/+|\/+$/g, '').replaceAll('/', '__');
      await expect(page).toHaveScreenshot(`${slug}.png`, {
        fullPage: true,
        animations: 'disabled',
        maxDiffPixelRatio: 0.01
      });
    }

    await testInfo.attach('route-contract', {
      body: JSON.stringify({ route, index_status: record.index_status }, null, 2),
      contentType: 'application/json'
    });
  });
}

test('planning route checker remains operable', async ({ page }) => {
  await page.goto('/england/tools/planning-route-check/');
  const controls = page.locator('input, select, textarea, button');
  expect(await controls.count()).toBeGreaterThan(0);
});

test('analytics bootstrap is present without sending a test hit', async ({ page }) => {
  await page.goto('/');
  const html = await page.content();
  expect(html).toContain('G-GXRZWRNWD7');
});
