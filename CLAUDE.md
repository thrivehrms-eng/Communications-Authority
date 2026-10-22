# Communications Authority of Kenya — website rebuild

Static rebuild of https://ca.programmer.co.ke/ in HTML, CSS and vanilla JavaScript (no frameworks, no build step).

## Source of truth
- **Build instructions:** `docs/homepage-build-instructions.md`. Follow it exactly. Current scope is the homepage only.
- **Brand lock:** use only CA's logo, the CA colour tokens and the CA fonts (Inter + Maitree 700) defined in that file. The concept site (media-harbour.com) supplies layout and behaviour only, never colours or fonts.
- **Visual references:** `docs/reference/concept/` (layout and behaviour) and `docs/reference/current-site/` (brand).
- **Background:** `docs/homepage-audit.md` (an audit of the current site; its Part B is superseded).

## Conventions
- British English. Never invent facts, figures or URLs; use marked placeholders (`data-placeholder="true"`) and list them in `docs/content-todo.md`.
- WCAG 2.2 AA. All motion must be pausable or respect `prefers-reduced-motion`.
- BEM class names with a `ca-` prefix; one ES module per concern under `assets/js/`.
- Work in the phases listed in the build instructions and stop for review after each phase.
