/**
 * Centralized public site origin and verified metadata configuration.
 *
 * Production host: https://devklean.smurftyy.dev
 *
 * The previous host, https://devklean.vercel.app, now permanently redirects
 * here (see vercel.json). Override via VITE_SITE_ORIGIN in the environment
 * if a different origin is ever needed (e.g. a preview deployment).
 */
export const DEFAULT_SITE_ORIGIN = 'https://devklean.smurftyy.dev';

export const SITE_META = {
  name: 'DevKlean',
  title: 'DevKlean — Cross-stack Artifact Cleanup',
  description:
    'Find and inspect regenerable dependencies, caches, and build artifacts across development stacks. Move selected files to system trash with DevKlean.',
  themeColor: '#111111',
  ogImagePath: '/og-image.png',
  ogImageAlt: 'DevKlean monochrome pixel-dissolving folder mark and wordmark with Cross-stack artifact cleanup.',
  repoUrl: 'https://github.com/smurftyy/devklean',
  licenseUrl: 'https://github.com/smurftyy/devklean/blob/main/LICENSE',
  pypiUrl: 'https://pypi.org/project/devklean/',
  softwareVersion: '1.1.0',
} as const;

export function resolveSiteOrigin(env: Record<string, string | undefined>): string {
  const configured = env.VITE_SITE_ORIGIN?.trim();
  const base = configured && configured.length > 0 ? configured : DEFAULT_SITE_ORIGIN;
  return base.replace(/\/+$/, '');
}

export function isPreviewDeployment(env: Record<string, string | undefined>): boolean {
  return env.VERCEL_ENV === 'preview' || env.VITE_SITE_NOINDEX === 'true';
}

export function buildSoftwareJsonLd(siteOrigin: string): string {
  const payload = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: SITE_META.name,
    description: SITE_META.description,
    url: `${siteOrigin}/`,
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'Linux, macOS, Windows',
    softwareVersion: SITE_META.softwareVersion,
    license: SITE_META.licenseUrl,
    sameAs: SITE_META.repoUrl,
    downloadUrl: SITE_META.pypiUrl,
  };
  return JSON.stringify(payload, null, 2);
}

export function buildRobotsTxt(siteOrigin: string, isPreview: boolean): string {
  if (isPreview) {
    return ['User-agent: *', 'Disallow: /', ''].join('\n');
  }
  return ['User-agent: *', 'Allow: /', '', `Sitemap: ${siteOrigin}/sitemap.xml`, ''].join('\n');
}

export function buildSitemapXml(siteOrigin: string): string {
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    '  <url>',
    `    <loc>${siteOrigin}/</loc>`,
    '  </url>',
    '</urlset>',
    '',
  ].join('\n');
}
