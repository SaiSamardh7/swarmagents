# Requirements: Lumen Landing Page

Source: brief.md (Task 1). Deliverable: single-page landing page for Lumen, a note-taking app. One `index.html` (CSS inline or `styles.css`; JS optional). No frameworks, no build step.

## 1. User Stories

- US-1: As a visitor, I want to see the product name, a tagline, and a clear call-to-action immediately, so I understand what Lumen is and how to start.
- US-2: As a visitor, I want a short list of key features, so I can judge whether Lumen fits my needs.
- US-3: As a visitor, I want to compare Free, Pro, and Team pricing tiers, so I can choose a plan.
- US-4: As a visitor, I want answers to common questions, so I can resolve doubts without contacting anyone.
- US-5: As a visitor, I want a footer with basic site information, so I can find secondary info and feel the site is legitimate.
- US-6: As a mobile visitor, I want the page to adapt to my screen, so I can read and tap everything comfortably.
- US-7: As a visitor using a screen reader or keyboard, I want a well-structured, navigable page, so I can use it without a mouse or sight.
- US-8: As a site owner, I want the page to have no build step or framework, so it can be hosted anywhere as static files.

## 2. Acceptance Criteria

### Structure and constraints
- AC-001: The deliverable includes a file named `index.html` that opens correctly directly from the filesystem in a modern browser.
- AC-002: CSS is either inline in `<style>` or in a single `styles.css` referenced by relative path; JS, if any, is inline or a local file.
- AC-003: No frameworks, libraries loaded from CDNs, or build tooling are used or required.
- AC-004: The top-level sections appear in this DOM order: hero, features, pricing, FAQ, footer.
- AC-005: Each section is identifiable by a distinct landmark or id (e.g. `id="hero"`, `id="features"`, `id="pricing"`, `id="faq"`, footer as `<footer>`).

### Hero
- AC-006: The hero displays the product name "Lumen".
- AC-007: The hero displays a tagline (one sentence) describing the app.
- AC-008: The hero contains a call-to-action implemented as an `<a>` element with a non-empty `href` and descriptive visible text.
- AC-009: The hero is the first section in the page body content.

### Features
- AC-010: The features section contains exactly 3 features.
- AC-011: Each feature has a heading and a short description.
- AC-012: The features section has its own section heading.

### Pricing
- AC-013: The pricing section contains exactly 3 tiers, named Free, Pro, and Team, in that order.
- AC-014: Each tier shows its name, a price (Free shows a zero price), and a list of at least 2 included items.
- AC-015: Each tier has a call-to-action link or button with descriptive text.
- AC-016: The pricing section has its own section heading.

### FAQ
- AC-017: The FAQ contains at least 3 question-and-answer pairs.
- AC-018: Each question is visibly distinguishable from its answer and each answer is non-empty.
- AC-019: If questions are collapsible, they are operable by keyboard and expose expanded/collapsed state (native `<details>/<summary>` satisfies this); if not collapsible, all answers are visible by default.
- AC-020: The FAQ section has its own section heading.

### Footer
- AC-021: The footer is the last section and uses a `<footer>` element.
- AC-022: The footer contains a copyright line including "Lumen" and a year.
- AC-023: Any footer links have a non-empty `href` and descriptive text.

### Responsive
- AC-024: The document `<head>` contains `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- AC-025: The CSS contains at least one `@media` query that changes layout.
- AC-026: At a 320px viewport width there is no horizontal scrolling and no clipped content.
- AC-027: At 375px, features and pricing tiers stack in a single column.
- AC-028: At 1024px or wider, features and pricing tiers display in a multi-column layout.
- AC-029: Text is at least 16px base size on mobile and remains readable when browser zoom is 200%.

### Accessibility
- AC-030: `<html>` has a `lang` attribute (e.g. `lang="en"`).
- AC-031: The page has exactly one `<h1>`, located in the hero.
- AC-032: Heading levels do not skip (h1, then h2 per section, h3 for sub-items).
- AC-033: Every `<img>` has an `alt` attribute; informative images have meaningful text, decorative images have `alt=""`. If no images are used, this criterion is satisfied vacuously.
- AC-034: The document has a non-empty `<title>`.
- AC-035: Text/background color contrast meets WCAG 2.1 AA (4.5:1 normal text, 3:1 large text and UI component boundaries).
- AC-036: All interactive elements are reachable and operable by keyboard in a logical tab order.
- AC-037: Interactive elements show a visible focus indicator.
- AC-038: Link and button text is descriptive out of context (no bare "click here").
- AC-039: Semantic landmarks are used (`<header>` or hero region, `<main>`, `<section>` with accessible names, `<footer>`).
- AC-040: Information is not conveyed by color alone.
- AC-041: Any animation respects `prefers-reduced-motion`; no auto-playing media.
- AC-042: The page has no console errors on load.

## 3. Functional Requirements by Section

### FR-HERO
- FR-H1: Render product name "Lumen" and a single `<h1>` (the h1 may contain the name, with tagline as a separate `<p>`).
- FR-H2: Render a concise tagline conveying note-taking value.
- FR-H3: Render a primary CTA link (e.g. "Get started free") pointing to `#pricing` or a sign-up URL placeholder.
- FR-H4: Optional supporting copy of at most 2 sentences. Hero must be visible without scrolling on a 375x667 viewport for name, tagline, and CTA.

### FR-FEATURES
- FR-F1: Section heading (h2) such as "Features".
- FR-F2: Exactly 3 feature items, each with an h3 and 1-2 sentence description (e.g. fast capture, organization/search, sync across devices).
- FR-F3: Optional icons must be decorative (`alt=""` or `aria-hidden`).

### FR-PRICING
- FR-P1: Section heading (h2) "Pricing".
- FR-P2: Exactly 3 tier cards: Free, Pro, Team. Each has h3 name, price with billing period (e.g. "$0", "$8 / month", "$15 / user / month"), feature list (`<ul>`), and CTA.
- FR-P3: One tier (Pro) may be highlighted as recommended; the highlight must be indicated in text, not color alone.
- FR-P4: Prices are placeholder content and consistent in format across tiers.

### FR-FAQ
- FR-Q1: Section heading (h2) "FAQ" or "Frequently asked questions".
- FR-Q2: At least 3 Q&A pairs covering topics such as pricing/free plan, data privacy/security, offline or device support.
- FR-Q3: Recommended implementation: `<details><summary>` per question.

### FR-FOOTER
- FR-FT1: `<footer>` containing copyright text with "Lumen" and the year.
- FR-FT2: Optional links (e.g. Privacy, Terms, Contact) using valid `href` values.

### FR-GLOBAL
- FR-G1: Consistent typography and spacing; system font stack acceptable.
- FR-G2: Optional in-page navigation anchors must target existing ids.
- FR-G3: Optional skip link ("Skip to main content") as first focusable element, targeting `<main>`.

## 4. Accessibility Requirements (summary)

- ARQ-1: Target WCAG 2.1 AA.
- ARQ-2: `html[lang]`, one `h1`, logical heading hierarchy, descriptive `<title>`.
- ARQ-3: All images have `alt`; decorative images use empty alt.
- ARQ-4: Native semantic elements preferred over ARIA; ARIA used only where native semantics are insufficient.
- ARQ-5: Full keyboard operability with visible focus; skip link recommended.
- ARQ-6: Color contrast per AC-035; do not rely on color alone.
- ARQ-7: Responsive text sizing in relative units; supports 200% zoom without loss of content.
- ARQ-8: Respect `prefers-reduced-motion`.

## 5. Out of Scope

Real authentication or payment, backend, analytics, multi-page navigation, CMS, localization, framework tooling.

## 6. Verification Notes

Criteria AC-001 through AC-005, AC-008, AC-010, AC-013, AC-017, AC-024, AC-025, AC-030, AC-031, AC-033 are mechanically checkable by HTML/CSS parsing. Remaining criteria require browser or manual inspection.
