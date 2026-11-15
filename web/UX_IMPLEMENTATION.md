# Landing page UX pass

## Context and scope

Implement the UX critique while preserving the existing monochrome redesign. Motion remains a separate future pass. Planning and follow-up review were delegated to an agent; implementation was checked against the local CLI source rather than assuming product behavior from the website.

CLI sources consulted: `../pyproject.toml`, `../README.md`, `../src/devklean/cli/parser.py`, `../src/devklean/cli/commands/clean.py`, `../src/devklean/cli/confirmation.py`, and the signature registry.

## Plan and implementation

1. **Explain the product immediately.** Identify it as a developer CLI, retain the headline, remove the duplicated hero scan, and keep the ecosystem strip.
2. **Make installation actionable.** Put Python requirements, platform support, and expandable pipx/pip guidance beside the CTA. Show copy success with the next command and a manual-copy fallback on failure.
3. **Complete the journey.** Keep a single Scan/Analyze/Explain walkthrough, followed by a visible preview → confirm → result guide. Standard cleanup confirms the discovered batch; per-folder interactive selection is macOS/Linux only. Trash must be emptied to reclaim disk space.
4. **Improve narrow layouts.** Use compact horizontal tabs, wrap command paths, preserve touch targets, and reduce repeated section spacing.
5. **Clarify risk.** Make lockfile conflicts prominent. Explain that signature confidence is fixed registry metadata, not a probability of safe removal.
6. **Correct the calculator.** Count artifact directories; a Next.js project can contribute both dependencies and build output. Allow empty input while editing, disable controls at bounds, announce results, and link back to installation.
7. **Finish supporting interactions.** Give technical disclosures distinct accessible names, align FAQ wording with CLI behavior, and add labeled GitHub icons to navigation and footer links.

## Validation

- TypeScript check and production build.
- Browser checks for tab keyboard navigation, focusable panels, copy success/failure, calculator limits/reset, and installation help.
- Responsive review at 320, 390, 768, 1024, and 1440 CSS pixels. Narrow widths use exact iframe viewports to avoid Firefox's minimum outer-window size.
- Agent follow-up review against actual CLI behavior.

The website's sample workspace and calculator remain illustrative. Clipboard error/success paths are checked with a deterministic browser stub; these checks do not establish clipboard permission behavior in every browser.
