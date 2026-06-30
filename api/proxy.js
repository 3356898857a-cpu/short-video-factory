// Vercel Serverless Function - CORS Proxy
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const url = req.query.url || req.body?.url;
  if (!url) return res.status(400).json({ error: 'Missing url param' });

  try {
    const headers = { ...req.headers };
    delete headers.host; delete headers.origin; delete headers.referer;
    const r = await fetch(url, { method: req.method, headers, body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined });
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
