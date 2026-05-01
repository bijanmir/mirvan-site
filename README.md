# Mirvan LLC — mirvaninc.com

A static marketing site for Mirvan LLC, built for deployment on Cloudflare Pages.

## Stack

- Static HTML / CSS / vanilla JS — zero build step, zero dependencies
- Google Fonts: Fraunces (display), Inter Tight (sans), JetBrains Mono (mono)
- Black-and-white editorial aesthetic with light/dark mode

## Features

- Mobile-first responsive layout
- Light/dark mode that follows system preference and can be overridden manually (moon/sun icon)
- No flash of incorrect theme (theme set inline before paint)
- Accessible: skip link, focus styles, semantic HTML, reduced-motion support
- SEO-ready: meta tags, Open Graph, Twitter cards, JSON-LD (Organization + ProfessionalService), sitemap.xml, robots.txt
- Performant: no JS frameworks, fonts preconnected, immutable cache headers via `_headers`

## File structure

```
.
├── index.html      # main page
├── styles.css      # all styles
├── main.js         # theme toggle + scroll reveals
├── favicon.svg     # site icon
├── robots.txt      # search engine directives
├── sitemap.xml     # search engine sitemap
└── _headers        # Cloudflare caching + security headers
```

## Deploying to Cloudflare Pages

1. Push this directory to a new GitHub repo (e.g. `mirvan-site`).
2. In Cloudflare → Workers & Pages → Create → Pages → Connect to Git.
3. Select the repo. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave blank)*
   - **Build output directory:** `/`
   - **Root directory:** `/`
4. Save and Deploy. You'll get a `*.pages.dev` URL.
5. In the Pages project → Custom domains → add `mirvaninc.com` and `www.mirvaninc.com`. Cloudflare auto-creates the DNS records (you're already on Cloudflare Registrar).
6. SSL provisions automatically.

## Editing copy later

All copy lives in `index.html`. The site is intentionally one file so you can rewrite headlines without hunting through components.
