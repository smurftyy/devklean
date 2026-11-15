# DevKlean hero: the local workbench

One oversized graphite artifact folder anchors a full-width workspace. Its stepped left edge comes from DevKlean’s existing pixel-folder mark. Layered sheets, inset framework marks, fine directory traces, directional edge highlights, and restrained shadows give the SVG depth without WebGL, raster assets, or new dependencies.

The copy stays inside the existing 1200px readable container. The artwork is positioned independently, extends beyond that container, and crops at the hero edges. On phones it moves below the install action, drops the Next.js folder and directory traces, and retains a compact main folder plus one Python fragment. Artwork is decorative, hidden from assistive technology, and cannot intercept pointer input.

## Product grounding

Checked the local repository README, Python package requirements, signature registry, existing site data, shared styles, favicon, and brand component. The depicted artifacts are `node_modules`, `.venv`, and `.next`. Paths and sizes use the existing illustrative workspace data. This is an illustration, not literal terminal output or a scan of the visitor’s machine. The copy and workflow distinguish inspection, review, confirmation, and system trash. Pixel details remain static; they never depict files being destroyed.

## Review screenshots

- [Standard desktop, 1440px](1440.png)
- [Wide desktop, 2560px](2560.png)
- [Desktop, 1920px](1920.png)
- [Desktop, 1280px](1280.png)
- [Small desktop, 1024px](1024.png)
- [Tablet, 768px](768.png)
- [Phone, 390px](390.png)
- [Small phone, 320px](320.png)

Phone screenshots use exact-width iframe viewports to avoid Firefox’s minimum outer-window size. Desktop captures use the corresponding browser window width.

## Verification

See [browser check results](verification.txt). Checks cover native clipboard success, denied clipboard fallback, navigation, expanded installation help, click targeting, overflow, artwork extending beyond the readable container, copy/art separation, and reduced motion. The headline reveals line by line, followed by the supporting copy and install action. Folder entrances are staggered and run once when the workspace enters view. Fine-pointer desktops add restrained mouse-driven depth, reset on pointer exit, scroll, or window blur. Touch layouts keep the one-time entrance. Reduced-motion preferences disable hero entrances, pointer depth, and link-arrow movement. No idle animation loop runs.

`npm run lint`, `npm run build`, and `git diff --check` also pass. Changes are limited to the hero component, its illustration, its stylesheet, and these review artifacts.
