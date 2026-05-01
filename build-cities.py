#!/usr/bin/env python3
"""
Mirvan city pages generator.

Reads cities.json and emits one /property-management-software/<slug>/index.html
per city, plus updates the root sitemap.xml.

Run: python3 build-cities.py
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).parent
CITIES = json.loads((ROOT / "cities.json").read_text())
OUT_DIR = ROOT / "property-management-software"
OUT_DIR.mkdir(exist_ok=True)


def page_html(c: dict) -> str:
    title = f"Property Management Software in {c['city']} | Mirvan"
    desc = (
        f"Mirvan builds custom property management software for {c['city']} "
        f"operators. Internal tools, tenant portals, and AI platforms designed "
        f"around the {c['stateAbbr']} regulatory landscape."
    )
    canonical = f"https://mirvaninc.com/property-management-software/{c['slug']}/"

    regs_html = "\n".join(
        f"""          <li class="reg">
            <h3 class="reg__name">{r['name']}</h3>
            <p class="reg__detail">{r['detail']}</p>
          </li>"""
        for r in c["regulations"]
    )

    neighborhoods_html = " · ".join(c["neighborhoods"])

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://mirvaninc.com/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Property Management Software",
                "item": "https://mirvaninc.com/property-management-software/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{c['city']}",
                "item": canonical,
            },
        ],
    }

    local_business_ld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"Mirvan — Property Management Software in {c['city']}",
        "url": canonical,
        "image": "https://mirvaninc.com/og.png",
        "description": desc,
        "areaServed": {
            "@type": "City",
            "name": c["city"],
            "containedInPlace": {
                "@type": "State",
                "name": c["state"],
            },
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "San Diego",
            "addressRegion": "CA",
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": c["lat"],
            "longitude": c["lng"],
        },
        "serviceType": f"Custom property management software development for {c['city']}",
    }

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="auto">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)" />
  <meta name="theme-color" content="#fafafa" media="(prefers-color-scheme: light)" />

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="property management software {c['city']}, custom property management software {c['stateAbbr']}, {c['city']} proptech, property manager software {c['city']}, AppFolio alternative {c['city']}, Buildium alternative {c['city']}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://mirvaninc.com{c['ogImage']}" />
  <meta property="og:image:secure_url" content="https://mirvaninc.com{c['ogImage']}" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{c['city']}, {c['stateAbbr']}" />
  <meta property="og:site_name" content="Mirvan" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://mirvaninc.com{c['ogImage']}" />
  <meta name="twitter:image:alt" content="{c['city']}, {c['stateAbbr']}" />

  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=JetBrains+Mono:wght@400;500&family=Inter+Tight:wght@300;400;500;600&display=swap" rel="stylesheet" />

  <script type="application/ld+json">
{json.dumps(local_business_ld, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_ld, indent=2)}
  </script>

  <script>
    (function () {{
      try {{
        var stored = localStorage.getItem('mirvan-theme');
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        var theme = stored || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
      }} catch (e) {{
        document.documentElement.setAttribute('data-theme', 'light');
      }}
    }})();
  </script>

  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="nav" role="banner">
    <div class="nav__inner">
      <a href="/" class="nav__logo" aria-label="Mirvan home">
        <span class="nav__mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square">
            <path d="M4 26 L4 6 L16 18 L28 6 L28 26" />
          </svg>
        </span>
        <span class="nav__wordmark">Mirvan</span>
      </a>

      <nav class="nav__links" aria-label="Primary">
        <a href="/#work">Work</a>
        <a href="/#services">Services</a>
        <a href="/#approach">Approach</a>
        <a href="/#contact">Contact</a>
      </nav>

      <div class="nav__actions">
        <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle color theme" title="Toggle theme">
          <svg class="icon-sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
          </svg>
          <svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        </button>
        <a href="#contact" class="btn btn--primary nav__cta">Start a project</a>
      </div>
    </div>
  </header>

  <main id="main">

    <!-- BREADCRUMB -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <div class="breadcrumb__inner">
        <a href="/">Mirvan</a>
        <span aria-hidden="true">/</span>
        <a href="/property-management-software/">Property Management Software</a>
        <span aria-hidden="true">/</span>
        <span class="breadcrumb__current">{c['city']}</span>
      </div>
    </nav>

    <!-- HERO IMAGE -->
    <section class="hero-image" aria-hidden="true">
      <div class="hero-image__frame">
        <img
          src="{c['image']}"
          alt="{c['city']}, {c['stateAbbr']}"
          loading="eager"
          fetchpriority="high"
          decoding="async"
        />
        <div class="hero-image__overlay"></div>
        <div class="hero-image__caption">
          <span class="hero-image__dot"></span>
          <span>{c['city']}, {c['stateAbbr']}</span>
        </div>
      </div>
    </section>

    <!-- HERO -->
    <section class="hero hero--city" aria-labelledby="hero-title">
      <div class="hero__grid" aria-hidden="true">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
      </div>
      <div class="hero__inner reveal">
        <p class="eyebrow">
          <span class="dot" aria-hidden="true"></span>
          Property management software · {c['city']}, {c['stateAbbr']}
        </p>

        <h1 id="hero-title" class="hero__title">
          {c['hero']}
        </h1>

        <p class="hero__lede">
          {c['intro']}
        </p>

        <div class="hero__cta">
          <a href="#contact" class="btn btn--primary">Start a project →</a>
          <a href="/#services" class="btn btn--ghost">See what we build</a>
        </div>

        <dl class="hero__stats">
          <div>
            <dt>Market</dt>
            <dd>{c['marketStat']}</dd>
          </div>
          <div>
            <dt>Signal</dt>
            <dd>{c['marketStatLabel']}</dd>
          </div>
          <div>
            <dt>Coverage</dt>
            <dd>{c['metro']}</dd>
          </div>
        </dl>
      </div>
    </section>

    <!-- PAIN POINT -->
    <section class="section section--alt" aria-labelledby="pain-title">
      <div class="section__inner">
        <div class="section__head reveal">
          <p class="eyebrow">The honest take</p>
          <h2 id="pain-title" class="section__title">
            {c['painPoint']}
          </h2>
        </div>
      </div>
    </section>

    <!-- REGULATIONS -->
    <section class="section" aria-labelledby="reg-title">
      <div class="section__inner">
        <header class="section__head reveal">
          <p class="eyebrow">01 — Compliance, automated</p>
          <h2 id="reg-title" class="section__title">
            The {c['stateAbbr']} rulebook,<br />encoded in your software.
          </h2>
          <p class="section__lede">
            Most platforms ship a generic compliance module and expect you to bend your operations around it. We do the opposite — we read the statute, talk to your team, and build the workflow that fits.
          </p>
        </header>

        <ol class="regs reveal">
{regs_html}
        </ol>
      </div>
    </section>

    <!-- SERVICES (shared) -->
    <section class="section section--alt" aria-labelledby="services-title">
      <div class="section__inner">
        <header class="section__head reveal">
          <p class="eyebrow">02 — What we build for {c['city']} operators</p>
          <h2 id="services-title" class="section__title">
            Three ways we work<br />with operators.
          </h2>
        </header>

        <div class="cards">
          <article class="card reveal">
            <span class="card__num">i.</span>
            <h3 class="card__title">Custom Internal Tools</h3>
            <p class="card__body">
              Replace the spreadsheet your ops team really runs the {c['city']} portfolio on. Lease tracking, maintenance routing, owner reporting — built around your workflow.
            </p>
            <ul class="card__list">
              <li>Multi-property dashboards</li>
              <li>Owner & tenant portals</li>
              <li>Maintenance & vendor workflows</li>
            </ul>
          </article>

          <article class="card reveal">
            <span class="card__num">ii.</span>
            <h3 class="card__title">Integration & Automation</h3>
            <p class="card__body">
              Make AppFolio, Buildium, QuickBooks, and your bank actually talk to each other. We build the connective tissue between systems you already pay for.
            </p>
            <ul class="card__list">
              <li>API integrations</li>
              <li>Reconciliation automation</li>
              <li>Reporting pipelines</li>
            </ul>
          </article>

          <article class="card reveal">
            <span class="card__num">iii.</span>
            <h3 class="card__title">AI-Native Platforms</h3>
            <p class="card__body">
              Tenant communication, lease parsing, predictive maintenance, deal underwriting — built around AI from day one, not bolted on.
            </p>
            <ul class="card__list">
              <li>Document intelligence</li>
              <li>Conversational interfaces</li>
              <li>Predictive workflows</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <!-- COVERAGE -->
    <section class="section" aria-labelledby="coverage-title">
      <div class="section__inner">
        <div class="coverage reveal">
          <p class="eyebrow">03 — Coverage</p>
          <h2 id="coverage-title" class="section__title">
            Operators across the {c['city']} metro.
          </h2>
          <p class="coverage__list">{neighborhoods_html}</p>
          <p class="coverage__note">If you operate in {c['metro']}, we can help.</p>
        </div>
      </div>
    </section>

    <!-- CONTACT -->
    <section id="contact" class="section section--contact" aria-labelledby="contact-title">
      <div class="section__inner">
        <div class="contact reveal">
          <p class="eyebrow">04 — Get in touch</p>
          <h2 id="contact-title" class="contact__title">
            Have a {c['ctaCity']} portfolio worth automating?<br />Let's talk for thirty minutes.
          </h2>
          <p class="contact__lede">
            No pitch deck. A real conversation about whether software can move the needle for your {c['city']} operation — and whether we're the right team to build it.
          </p>
          <div class="contact__cta">
            <a href="mailto:hello@mirvaninc.com?subject=Mirvan%20%E2%80%94%20{c['city'].replace(' ', '%20')}%20Inquiry" class="btn btn--primary btn--lg">hello@mirvaninc.com</a>
            <p class="contact__note">Replies within one business day, San Diego time.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

__FOOTER_HTML__

  <script src="/main.js" defer></script>
</body>
</html>
"""


def footer_cities_html() -> str:
    return "\n".join(
        f'            <li><a href="/property-management-software/{c["slug"]}/">{c["city"]}<span class="footer__state">{c["stateAbbr"]}</span></a></li>'
        for c in CITIES
    )


def footer_html() -> str:
    return f"""  <footer class="footer" role="contentinfo">
    <div class="footer__inner">

      <div class="footer__top">
        <h2 class="footer__wordmark">Mirvan<em>.</em></h2>
        <p class="footer__tagline">Custom software for property management companies — built in San Diego, deployed across the country.</p>
      </div>

      <div class="footer__cols">
        <nav class="footer__cities" aria-label="Markets we serve">
          <p class="footer__col-label">Markets</p>
          <ul>
{footer_cities_html()}
          </ul>
        </nav>

        <nav class="footer__nav" aria-label="Site">
          <p class="footer__col-label">Company</p>
          <ul>
            <li><a href="/#work">Selected work</a></li>
            <li><a href="/#services">Services</a></li>
            <li><a href="/#approach">Approach</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>

        <div class="footer__contact">
          <p class="footer__col-label">Get in touch</p>
          <a href="mailto:hello@mirvaninc.com">hello@mirvaninc.com</a>
          <p class="footer__contact-meta">San Diego, California<br/>Replies within one business day</p>
        </div>
      </div>

      <div class="footer__bottom">
        <div class="footer__brand">
          <span class="nav__mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square">
              <path d="M4 26 L4 6 L16 18 L28 6 L28 26" />
            </svg>
          </span>
          <span>Mirvan LLC</span>
        </div>
        <p class="footer__meta">
          <span>© <span id="year"></span> Mirvan LLC</span>
          <span aria-hidden="true">·</span>
          <span>All rights reserved</span>
        </p>
      </div>

    </div>
  </footer>"""


def write_sitemap():
    urls = ['<url><loc>https://mirvaninc.com/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>']
    for c in CITIES:
        urls.append(
            f'  <url><loc>https://mirvaninc.com/property-management-software/{c["slug"]}/</loc>'
            f'<changefreq>monthly</changefreq><priority>0.8</priority></url>'
        )
    body = "\n  ".join(urls)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {body}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(sitemap)


def write_index_hub():
    """Generates /property-management-software/index.html — the parent hub page."""
    cards = "\n".join(
        f"""          <a class="hub-card reveal" href="/property-management-software/{c['slug']}/">
            <div class="hub-card__media">
              <img src="{c['image']}" alt="{c['city']}, {c['stateAbbr']}" loading="lazy" decoding="async" />
              <div class="hub-card__media-label">
                <h3 class="hub-card__media-city">{c['city']}</h3>
                <span class="hub-card__media-state">{c['stateAbbr']}</span>
              </div>
            </div>
            <div class="hub-card__body">
              <p class="hub-card__metro">{c['metro']}</p>
              <p class="hub-card__cta"><span>View {c['city']} page</span></p>
            </div>
          </a>"""
        for c in CITIES
    )

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="auto">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>Property Management Software by City | Mirvan</title>
  <meta name="description" content="Mirvan builds custom property management software for operators across the country. Find your market — San Diego, LA, Phoenix, Las Vegas, Austin, Dallas–Fort Worth, Miami, and Tampa." />
  <link rel="canonical" href="https://mirvaninc.com/property-management-software/" />
  <meta name="robots" content="index, follow" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=JetBrains+Mono:wght@400;500&family=Inter+Tight:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <script>
    (function () {{
      try {{
        var stored = localStorage.getItem('mirvan-theme');
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', stored || (prefersDark ? 'dark' : 'light'));
      }} catch (e) {{ document.documentElement.setAttribute('data-theme', 'light'); }}
    }})();
  </script>
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" role="banner">
    <div class="nav__inner">
      <a href="/" class="nav__logo">
        <span class="nav__mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"><path d="M4 26 L4 6 L16 18 L28 6 L28 26" /></svg>
        </span>
        <span class="nav__wordmark">Mirvan</span>
      </a>
      <nav class="nav__links" aria-label="Primary">
        <a href="/#work">Work</a><a href="/#services">Services</a><a href="/#approach">Approach</a><a href="/#contact">Contact</a>
      </nav>
      <div class="nav__actions">
        <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle theme">
          <svg class="icon-sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
          <svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <a href="/#contact" class="btn btn--primary nav__cta">Start a project</a>
      </div>
    </div>
  </header>

  <main id="main">
    <!-- BREADCRUMB -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <div class="breadcrumb__inner">
        <a href="/">Mirvan</a>
        <span aria-hidden="true">/</span>
        <span class="breadcrumb__current">Property Management Software</span>
      </div>
    </nav>

    <section class="hero hero--city">
      <div class="hero__grid" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <div class="hero__inner reveal">
        <p class="eyebrow"><span class="dot" aria-hidden="true"></span>Markets we serve</p>
        <h1 class="hero__title">Custom software for property managers, market by market.</h1>
        <p class="hero__lede">Different cities, different rules, different operators. Pick yours and we'll show you what's possible.</p>
      </div>
    </section>

    <section class="section">
      <div class="section__inner">
        <div class="hub-grid">
{cards}
        </div>
      </div>
    </section>
  </main>

  <footer class="footer" role="contentinfo">
    <div class="footer__inner">

      <div class="footer__top">
        <h2 class="footer__wordmark">Mirvan<em>.</em></h2>
        <p class="footer__tagline">Custom software for property management companies — built in San Diego, deployed across the country.</p>
      </div>

      <div class="footer__cols">
        <nav class="footer__cities" aria-label="Markets we serve">
          <p class="footer__col-label">Markets</p>
          <ul>
__FOOTER_CITIES__
          </ul>
        </nav>

        <nav class="footer__nav" aria-label="Site">
          <p class="footer__col-label">Company</p>
          <ul>
            <li><a href="/#work">Selected work</a></li>
            <li><a href="/#services">Services</a></li>
            <li><a href="/#approach">Approach</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>

        <div class="footer__contact">
          <p class="footer__col-label">Get in touch</p>
          <a href="mailto:hello@mirvaninc.com">hello@mirvaninc.com</a>
          <p class="footer__contact-meta">San Diego, California<br/>Replies within one business day</p>
        </div>
      </div>

      <div class="footer__bottom">
        <div class="footer__brand">
          <span class="nav__mark" aria-hidden="true"><svg viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"><path d="M4 26 L4 6 L16 18 L28 6 L28 26" /></svg></span>
          <span>Mirvan LLC</span>
        </div>
        <p class="footer__meta">
          <span>© <span id="year"></span> Mirvan LLC</span>
          <span aria-hidden="true">·</span>
          <span>All rights reserved</span>
        </p>
      </div>

    </div>
  </footer>

  <script src="/main.js" defer></script>
</body>
</html>
"""
    html = html.replace("__FOOTER_CITIES__", footer_cities_html())
    (OUT_DIR / "index.html").write_text(html)


def main():
    fh = footer_html()
    for c in CITIES:
        page_dir = OUT_DIR / c["slug"]
        page_dir.mkdir(exist_ok=True)
        html = page_html(c).replace("__FOOTER_HTML__", fh)
        (page_dir / "index.html").write_text(html)
        print(f"  ✓ {c['slug']}/index.html")
    write_index_hub()
    print(f"  ✓ property-management-software/index.html (hub)")
    write_sitemap()
    print(f"  ✓ sitemap.xml updated ({len(CITIES) + 1} URLs)")
    print(f"\nDone. Generated {len(CITIES)} city pages.")


if __name__ == "__main__":
    main()
