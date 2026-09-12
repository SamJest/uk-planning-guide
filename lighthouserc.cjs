module.exports = {
  ci: {
    collect: {
      startServerCommand: 'node scripts/serve_site.cjs artifacts/phase-0-canary-site 8768',
      startServerReadyPattern: 'Serving',
      url: [
        'http://127.0.0.1:8768/',
        'http://127.0.0.1:8768/england/councils/colchester/',
        'http://127.0.0.1:8768/wales/projects/dropped-kerbs/cardiff/',
        'http://127.0.0.1:8768/scotland/projects/garden-rooms/city-of-edinburgh/',
        'http://127.0.0.1:8768/england/tools/planning-route-check/'
      ],
      numberOfRuns: 1
    },
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:performance': ['error', { minScore: 0.8 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }]
      }
    },
    upload: { target: 'filesystem', outputDir: './reports/phase-0/lighthouse' }
  }
};
