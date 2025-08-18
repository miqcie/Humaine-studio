module.exports = {
  ci: {
    collect: {
      staticDistDir: '_site',
      url: [
        'http://localhost/index.html',
        'http://localhost/weeks-of-life.html'
      ],
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', {minScore: 0.8}],
        'categories:accessibility': ['error', {minScore: 0.9}],
        'categories:best-practices': ['warn', {minScore: 0.8}],
        'categories:seo': ['warn', {minScore: 0.8}],
      }
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};