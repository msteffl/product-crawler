var fs = require('fs');
var os = require("os");

const scraperObject = {
  categories: [
    {
      url: '<url>',
      name: 'CHEMISCH-TECHNISCHE'
    },
    {
      url: '<url>',
      name: 'KFZ-TEILE'
    }
  ],
  results: [],
  output: fs.createWriteStream('output.csv', {
    flags: 'a' // 'a' means appending (old data will be preserved)
  }),
  async scraper(browser) {

    fs.writeFileSync('output.csv','url;category' + os.EOL);

    for (const category of this.categories) {
      await getAllProductsFromCategory(category.url, this.results, this.output, category.name);
    }

    async function getAllProductsFromCategory(url, results, output, category) {
      const pageLinks = await getPageUrls(url);

      if (pageLinks.length === 0) {
        results.push(url)
        console.log(url);
        output.write(url + ";" + category + os.EOL);
      } else {
        for (const link of pageLinks) {
          await getAllProductsFromCategory(link, results, output, category)
        };
      }
      return url
    }

    async function getPageUrls(link) {
      let page = await browser.newPage();
      try {
        // console.log(`Navigating to ${link}...`);
        // Navigate to the selected page
        await page.goto(link);
        await page.waitForSelector('#catalogContent', { timeout: 1000 });
        let urls = await page.$$eval('#catalogContent > div', links => {
          links = links.map(el => el.querySelector('a').href)
          return links;
        });
        return urls;
      } catch (error) {
        return []
      } finally {
        await page.close();
      }
    }
  }
}

module.exports = scraperObject;