import { argv, exit } from 'node:process';

const SITE = 'https://santaclaritaopenhouses.com';
const HOST = 'santaclaritaopenhouses.com';
const KEY = '7c13072f5d5a4a4b89e7b3550054f246';
const KEY_LOCATION = `${SITE}/${KEY}.txt`;

function extractLocs(xml) {
	const matches = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)];
	return matches.map((match) => match[1].trim()).filter(Boolean);
}

async function fetchText(url) {
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to fetch ${url}: ${response.status}`);
	}
	return response.text();
}

async function urlsFromSitemapIndex() {
	const indexXml = await fetchText(`${SITE}/sitemap-index.xml`);
	const sitemapUrls = extractLocs(indexXml);
	const allUrls = [];

	for (const sitemapUrl of sitemapUrls) {
		const sitemapXml = await fetchText(sitemapUrl);
		allUrls.push(...extractLocs(sitemapXml));
	}

	return [...new Set(allUrls)].filter((url) => url.startsWith(SITE));
}

async function submitIndexNow(urlList) {
	const payload = {
		host: HOST,
		key: KEY,
		keyLocation: KEY_LOCATION,
		urlList,
	};

	const response = await fetch('https://api.indexnow.org/indexnow', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json; charset=utf-8',
		},
		body: JSON.stringify(payload),
	});

	if (!response.ok) {
		const text = await response.text();
		throw new Error(`IndexNow error ${response.status}: ${text}`);
	}
}

async function main() {
	const cliUrls = argv.slice(2).filter((value) => value.startsWith('http'));
	const urlList = cliUrls.length > 0 ? cliUrls : await urlsFromSitemapIndex();

	if (urlList.length === 0) {
		console.log('No URLs found to submit.');
		return;
	}

	await submitIndexNow(urlList);
	console.log(`IndexNow submitted ${urlList.length} URL(s).`);
}

main().catch((error) => {
	console.error(error.message);
	exit(1);
});
