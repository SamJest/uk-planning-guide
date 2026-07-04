module.exports = {
  ci: {
    collect: {
      staticDistDir: './artifacts/phase-0-canary-site',
      url: [
        'http://localhost/',
        'http://localhost/england/councils/colchester/',
        'http://localhost/wales/projects/dropped-kerbs/cardiff/',
        'http://localhost/scotland/projects/garden-rooms/city-of-edinburgh/',
        'http://localhost/england/tools/planning-route-check/'
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
