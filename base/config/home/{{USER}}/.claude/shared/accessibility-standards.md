# Accessibility Standards

Practical accessibility (a11y) guidance for `ui-ux-engineer`, `software-engineer`, and the dedicated `accessibility-specialist` agent. Target: **WCAG 2.1 Level AA** as a baseline, AAA where the cost is reasonable.

Accessibility is non-negotiable for public-facing products in most jurisdictions (EU EAA, US ADA, UK Equality Act). Treat it as a quality gate, not a feature.

## The Four POUR Principles

WCAG groups requirements under four principles:

- **Perceivable** — users can perceive the content (visual, auditory, tactile).
- **Operable** — users can operate the interface (keyboard, voice, switch, touch).
- **Understandable** — content and behavior are predictable and clear.
- **Robust** — works across assistive technologies (screen readers, magnifiers, voice control).

## Quick Wins (do these always)

### Semantic HTML first
- Use the right element: `<button>` for actions, `<a>` for navigation, `<input type="checkbox">` for toggles.
- A `<div>` with a click handler is **not** a button. It misses keyboard focus, role announcement, and Enter/Space activation.
- Headings (`<h1>`–`<h6>`) form a logical outline. Don't skip levels.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`. One `<main>` per page.

### Keyboard
- **Every interactive element must be reachable and operable with the keyboard alone.**
- Tab order follows visual order. Avoid positive `tabindex` values.
- Focus must be visible — don't remove `:focus-visible` outlines without replacing them.
- Common keys: Enter/Space activate, Escape closes overlays, arrows navigate within composite widgets.

### Color & contrast
- Text contrast: **4.5:1** for body, **3:1** for large text (≥18pt or 14pt bold).
- Non-text contrast: **3:1** for UI components and graphical objects against adjacent colors.
- Don't use color as the *only* means of conveying information. Pair with icon, text, or pattern.

### Alternative text
- Every meaningful image has `alt`. Decorative images use `alt=""` (empty, not absent).
- Icons-as-buttons need an accessible name (`aria-label` or visually-hidden text).
- Complex images (charts, diagrams) need a longer description in surrounding text or `<figcaption>`.

### Forms
- Every input has a `<label>` (visible) or `aria-label` (when visually labeled differently).
- Errors are programmatically associated (`aria-describedby`) and announced (`role="alert"` or `aria-live`).
- Group related inputs with `<fieldset>` + `<legend>`.
- Don't rely on placeholder text as a label — placeholders disappear on input.

## ARIA — use sparingly

The first rule of ARIA: **don't use ARIA when native HTML works.** Most accessibility issues come from over-applied or wrong ARIA.

When you must:
- `aria-label` / `aria-labelledby` for naming
- `aria-describedby` for supplementary description
- `aria-live="polite"` for non-urgent announcements; `assertive` for errors
- `role="dialog"` + focus management for modals
- `aria-expanded`, `aria-controls`, `aria-current` on dynamic widgets

Avoid:
- `role="button"` on a `<div>` — use `<button>`
- `aria-hidden="true"` on focusable elements (creates ghost focus)
- Redundant `role` matching native semantics

## Patterns to Get Right

### Modal dialogs
- Trap focus inside while open
- Return focus to the trigger on close
- Escape closes
- Background content marked `inert` (or `aria-hidden="true"`)
- `role="dialog"` + `aria-labelledby` (the heading) + `aria-describedby` (the body)

### Custom dropdowns / combos
- Default to native `<select>` or `<input list="…">` if it fits — they're free a11y.
- Otherwise follow the WAI-ARIA Combobox pattern strictly.

### Skip links
- "Skip to main content" link as the first focusable element on every page.

### Loading & async
- Announce significant state changes via `aria-live` regions.
- Don't shift focus unexpectedly — only on user-initiated actions.

### Motion & animation
- Respect `prefers-reduced-motion`. Disable parallax, autoplay, and large transitions.
- No content flashing more than 3 times per second (seizure risk).

## Testing

Manual testing beats automated testing. Run all three:

1. **Keyboard-only walk-through** — tab through the entire flow without a mouse.
2. **Screen-reader test** — VoiceOver (macOS/iOS), NVDA (Windows), or TalkBack (Android). Pick one and learn it.
3. **Automated audit** — axe-core (browser extension or CI), Lighthouse, Pa11y. These catch ~30% of issues; the other 70% need a human.

## Acceptance Criteria for UI Stories

Every UI story should include accessibility acceptance criteria. Defaults:

- [ ] Reachable and operable with keyboard alone
- [ ] Focus is always visible and follows logical order
- [ ] All interactive elements have an accessible name
- [ ] Color contrast meets WCAG AA
- [ ] Errors are announced to assistive tech
- [ ] Works with VoiceOver / NVDA on the supported browsers
- [ ] Works with `prefers-reduced-motion: reduce`
- [ ] Page passes axe-core with no violations

## Common Anti-Patterns

- Custom controls without keyboard handlers
- Click handlers on `<div>` or `<span>`
- Removing focus indicators "for design"
- Using only color to indicate state (red error, green success — needs icon/text too)
- Inaccessible custom dropdowns and date pickers
- Modal dialogs without focus trap or Escape handling
- Carousel and tabs without arrow-key navigation
- Auto-playing audio or video
- Time-limited interactions without warning or extension option
- `aria-label` overriding meaningful visible text

## Definition of Done — A11y

A UI feature is **not done** until:

1. It passes manual keyboard navigation
2. It passes screen-reader announcement check
3. axe-core CI check is green
4. Reduced-motion variant exists or is N/A
5. Color contrast verified for all text and meaningful non-text
6. Acceptance criteria above are met
