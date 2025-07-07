const fs = require('fs');

// Read the full database
const fullData = JSON.parse(fs.readFileSync('CookieGUARD-Clean/site-database.json', 'utf8'));

// Create optimized version - keep only essential data
const optimizedData = {
  version: fullData.version,
  generatedAt: fullData.generatedAt,
  totalSites: fullData.totalSites,
  sites: {}
};

// For each site, keep only the most important data
Object.entries(fullData.sites).forEach(([domain, data]) => {
  optimizedData.sites[domain] = {
    rating: data.rating,
    cookieCount: data.cookieCount,
    hasBanner: data.hasBanner,
    // Simplified stats - only counts
    stats: {
      tracking: data.cookieStats.tracking,
      analytics: data.cookieStats.analytics,
      essential: data.cookieStats.essential
    },
    // Only include banner info if banner exists
    banner: data.hasBanner ? {
      buttons: data.bannerInfo?.buttonCount || 0,
      hasAccept: data.bannerInfo?.hasAccept || false,
      hasReject: data.bannerInfo?.hasReject || false,
      hasSettings: data.bannerInfo?.hasSettings || false
    } : null
  };
});

// Write optimized version
fs.writeFileSync('CookieGUARD-Clean/site-database.json', JSON.stringify(optimizedData, null, 2));

console.log('✅ Database optimized!');
console.log(`Original sites: ${Object.keys(fullData.sites).length}`);
console.log(`Optimized sites: ${Object.keys(optimizedData.sites).length}`);

// Show file size reduction
const originalSize = fs.statSync('backend/results/cookieguard-extension-data.json').size;
const optimizedSize = fs.statSync('CookieGUARD-Clean/site-database.json').size;
console.log(`Size reduction: ${originalSize} -> ${optimizedSize} bytes (${Math.round((1-optimizedSize/originalSize)*100)}% smaller)`);

// Test a few entries
console.log('\n🎯 Sample entries:');
['google.de', 'linkedin.com', 'bild.de'].forEach(domain => {
  if (optimizedData.sites[domain]) {
    const site = optimizedData.sites[domain];
    console.log(`${domain}: ${site.rating} | Cookies: ${site.cookieCount} | Banner: ${site.hasBanner ? '✅' : '❌'}`);
  }
});