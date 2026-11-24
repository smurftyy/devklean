# Custom Domain Transition (`devklean.smurftyy.dev`)

The code-side cutover is done: the landing page's canonical URL, Open Graph URLs, JSON-LD, `robots.txt`, and `sitemap.xml` now default to `https://devklean.smurftyy.dev` via [site.config.ts](./site.config.ts), and the old host (`https://devklean.vercel.app`) permanently redirects there via [vercel.json](./vercel.json).

**Do not release this to `main` until `https://devklean.smurftyy.dev` is actually live and serving over HTTPS** — the dashboard steps below (1–5, 8) must happen first, or the new default origin and the redirect will point at a host that isn't serving yet.

## Code-side changes (done)

- [x] `site.config.ts`: `DEFAULT_SITE_ORIGIN` set to `https://devklean.smurftyy.dev`; the no-longer-needed `PLANNED_SITE_ORIGIN` removed.
- [x] `.env.example`: `VITE_SITE_ORIGIN` default updated to `https://devklean.smurftyy.dev`.
- [x] `vercel.json`: permanent redirect added from `devklean.vercel.app` to `https://devklean.smurftyy.dev/:path*` (preview-deployment `noindex` header rule unchanged).
- [x] User-facing links elsewhere in the repo (`README.md` website badge) updated to the new domain.
- [x] Verified in a local build (`npm run build`): `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, JSON-LD `url`, `robots.txt`'s `Sitemap:` line, and `sitemap.xml` all resolve to `https://devklean.smurftyy.dev`.

## Remaining dashboard steps (Vercel + DNS + Search Console)

1. **Add the domain in Vercel:** Open the DevKlean web project in Vercel → **Settings → Domains** and add `devklean.smurftyy.dev`.
2. **Copy the Vercel DNS target:** Record the exact DNS record (`CNAME` or `A`) Vercel specifies for that project. Do not guess the target or alter unrelated records on `smurftyy.dev`.
3. **Create the DNS record:** Add the `devklean` record at the authoritative DNS provider for `smurftyy.dev`.
4. **Verify ownership if prompted:** Add any TXT verification record Vercel requests, then confirm verification succeeds.
5. **Confirm HTTPS:** Wait for Vercel to provision the TLS certificate and verify `https://devklean.smurftyy.dev/` loads cleanly over HTTPS with valid assets (`/og-image.png`, `/favicon.ico`, `/site.webmanifest`).
6. ~~Switch production metadata to the new origin~~ — done in code (see above); set `VITE_SITE_ORIGIN=https://devklean.smurftyy.dev` in Vercel **Production** environment variables as well, so the deployed build matches the repo default.
7. ~~Enable the permanent old-host redirect~~ — done in code (see [vercel.json](./vercel.json)).
8. **Verify Search Console:** Verify ownership of `https://devklean.smurftyy.dev` in Google Search Console and submit `https://devklean.smurftyy.dev/sitemap.xml`.
