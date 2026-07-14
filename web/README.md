# devklean — landing page

The marketing site for [devklean](https://github.com/smurftyy/devklean), the
open-source CLI that finds regenerable development artifacts and moves them to
your system trash. This folder is a self-contained
[Vite](https://vite.dev) + React + TypeScript single-page app; it does not
import from or depend on the Python package next to it.

Everything shown on the page — commands, flags, risk/confidence values, the
workspace-health formula — is sourced from the real tool. See the top-level
[`README.md`](../README.md) and `src/devklean/` for the source of truth.

## Develop

```bash
npm install
npm run dev      # serves on http://localhost:3000
```

## Build

```bash
npm run build    # emits a static bundle to dist/
npm run preview  # serve the built bundle locally
```

## Other scripts

```bash
npm run lint     # tsc --noEmit type-check
npm run clean    # remove the dist/ build output
```

## Stack

- Vite 6 + React 19
- Tailwind CSS v4 (`@tailwindcss/vite`)
- [motion](https://motion.dev) for animation
- [lucide-react](https://lucide.dev) for icons
