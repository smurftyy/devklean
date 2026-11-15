import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig, loadEnv, Plugin } from 'vite';
import {
  buildRobotsTxt,
  buildSitemapXml,
  buildSoftwareJsonLd,
  isPreviewDeployment,
  resolveSiteOrigin,
} from './site.config';

function siteMetadataPlugin(siteOrigin: string, isPreview: boolean): Plugin {
  const robotsMeta = isPreview
    ? '<meta name="robots" content="noindex, nofollow" />'
    : '<meta name="robots" content="index, follow" />';
  const jsonLd = buildSoftwareJsonLd(siteOrigin);
  const robotsTxt = buildRobotsTxt(siteOrigin, isPreview);
  const sitemapXml = buildSitemapXml(siteOrigin);

  return {
    name: 'devklean-site-metadata',
    transformIndexHtml(html) {
      return html
        .replace(/__SITE_ORIGIN__/g, siteOrigin)
        .replace('<!--ROBOTS_META-->', robotsMeta)
        .replace('__JSON_LD__', jsonLd);
    },
    configureServer(server) {
      server.middlewares.use('/robots.txt', (_req, res) => {
        res.setHeader('Content-Type', 'text/plain; charset=utf-8');
        res.end(robotsTxt);
      });
      server.middlewares.use('/sitemap.xml', (_req, res) => {
        res.setHeader('Content-Type', 'application/xml; charset=utf-8');
        res.end(sitemapXml);
      });
    },
    generateBundle() {
      this.emitFile({
        type: 'asset',
        fileName: 'robots.txt',
        source: robotsTxt,
      });
      this.emitFile({
        type: 'asset',
        fileName: 'sitemap.xml',
        source: sitemapXml,
      });
    },
  };
}

export default defineConfig(({ mode }) => {
  const fileEnv = loadEnv(mode, __dirname, '');
  const mergedEnv: Record<string, string | undefined> = {
    ...fileEnv,
    ...process.env,
  };
  const siteOrigin = resolveSiteOrigin(mergedEnv);
  const isPreview = isPreviewDeployment(mergedEnv);

  return {
    plugins: [react(), tailwindcss(), siteMetadataPlugin(siteOrigin, isPreview)],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    server: {
      // HMR is disabled in AI Studio via DISABLE_HMR env var.
      // Do not modify—file watching is disabled to prevent flickering during agent edits.
      hmr: process.env.DISABLE_HMR !== 'true',
      // Disable file watching when DISABLE_HMR is true to save CPU during agent edits.
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
  };
});
