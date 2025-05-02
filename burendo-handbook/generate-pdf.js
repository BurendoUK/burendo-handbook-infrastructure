const puppeteer = require('puppeteer');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

const urls = fs.readFileSync('urls.txt', 'utf-8').split('\n').filter(Boolean);

(async () => {
  const browser = await puppeteer.launch();
  const pdfBuffers = [];

  for (const url of urls) {
    console.log(`📄 Rendering ${url}`);
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });

    const buffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      margin: { top: '1cm', bottom: '1cm', left: '1.5cm', right: '1.5cm' },
    });

    pdfBuffers.push(buffer);
    await page.close();
  }

  await browser.close();

  // Merge all PDFs
  const mergedPdf = await PDFDocument.create();
  for (const buffer of pdfBuffers) {
    const pdf = await PDFDocument.load(buffer);
    const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    pages.forEach((p) => mergedPdf.addPage(p));
  }

  const finalPdf = await mergedPdf.save();
  fs.writeFileSync('handbook.pdf', finalPdf);
  console.log('✅ handbook.pdf generated!');
})();
