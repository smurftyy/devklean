# Custom Domain Transition (`devklean.smurftyy.dev`)

The landing page currently defaults its canonical URL, Open Graph URLs, JSON-LD, `robots.txt`, and `sitemap.xml` to the live origin `https://devklean.vercel.app` via [site.config.ts](./site.config.ts).

Do **not** switch production metadata or enable the old-host redirect until `https://devklean.smurftyy.dev` is live and serving over HTTPS.

## Cutover Checklist (Vercel + DNS + Search Console)

1. **Add the domain in Vercel:** Open the DevKlean web project in Vercel → **Settings → Domains** and add `devklean.smurftyy.dev`.
2. **Copy the Vercel DNS target:** Record the exact DNS record (`CNAME` or `A`) Vercel specifies for that project. Do not guess the target or alter unrelated records on `smurftyy.dev`.
3. **Create the DNS record:** Add the `devklean` record at the authoritative DNS provider for `smurftyy.dev`.
4. **Verify ownership if prompted:** Add any TXT verification record Vercel requests, then confirm verification succeeds.
5. **Confirm HTTPS:** Wait for Vercel to provision the TLS certificate and verify `https://devklean.smurftyy.dev/` loads cleanly over HTTPS with valid assets (`/og-image.png`, `/favicon.ico`, `/site.webmanifest`).
6. **Switch production metadata to the new origin:**
   - Set `VITE_SITE_ORIGIN=https://devklean.smurftyy.dev` in Vercel **Production** environment variables (and optionally update `DEFAULT_SITE_ORIGIN` in [site.config.ts](./site.config.ts)), then redeploy production.
   - Verify the built HTML `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, JSON-LD `url`, `robots.txt`, and `sitemap.xml` all resolve to `https://devklean.smurftyy.dev`.
7. **Enable the permanent old-host redirect:** Add the following `redirects` block to [vercel.json](./vercel.json) only after `https://devklean.smurftyy.dev` is serving cleanly. Scoping `has` to `host: "devklean.vercel.app"` preserves paths and query strings (`:path*`) and avoids redirecting local development or preview deployments:

   ```json
   "redirects": [
     {
       "source": "/:path*",
       "has": [
         {
           "type": "host",
           "value": "devklean.vercel.app"
         }
       ],
       "destination": "https://devklean.smurftyy.dev/:path*",
       "permanent": true
     }
   ]
   ```

8. **Verify Search Console:** Verify ownership of `https://devklean.smurftyy.dev` in Google Search Console and submit `https://devklean.smurftyy.dev/sitemap.xml`.
