"""Build self-contained GitHub README graphics; no network or packages needed.

The diagrams illustrate the documented testing workflows. They are not live
test results. UI glyphs come from the vendored, MIT-licensed Phosphor icons.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
GREEN = "#48d99a"
TEXT = "#edf5f0"
MUTED = "#a4b9ac"


def icon(name, x, y, size, color=GREEN):
    source = (ASSETS / "icons" / f"{name}.svg").read_text()
    paths = source.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return f'<g transform="translate({x} {y}) scale({size / 256})" fill="{color}">{paths}</g>'


def text(x, y, value, size=24, color=TEXT, weight=400, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def svg(name, width, height, title, description, content, motion=False):
    animation = """
      @media (prefers-reduced-motion: no-preference) {
        .flow-signal { animation: signal 8s ease-in-out infinite; }
        .flow-signal:nth-of-type(2) { animation-delay: -2s; }
        .flow-signal:nth-of-type(3) { animation-delay: -4s; }
        .flow-signal:nth-of-type(4) { animation-delay: -6s; }
        @keyframes signal { 0%, 100% { opacity: .3; } 35%, 60% { opacity: 1; } }
      }
    """ if motion else ""
    result = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <linearGradient id="surface" x2="1" y2="1"><stop stop-color="#101b16"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
    <linearGradient id="panel" x2="0" y2="1"><stop stop-color="#1c3428"/><stop offset="1" stop-color="#122019"/></linearGradient>
    <radialGradient id="wash"><stop stop-color="#244b36" stop-opacity=".65"/><stop offset="1" stop-color="#244b36" stop-opacity="0"/></radialGradient>
  </defs>
  <style>text {{ font-family: {FONT}; }}{animation}</style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" fill="url(#surface)" stroke="#2b4033"/>
  {content}
</svg>'''
    (ASSETS / name).write_text(result + "\n")


def node(cx, cy, label, width=116):
    return f'''<rect x="{cx-width/2}" y="{cy-29+7}" width="{width}" height="58" rx="12" fill="#070e0a" opacity=".5"/>
      <rect x="{cx-width/2}" y="{cy-29}" width="{width}" height="58" rx="12" fill="url(#panel)" stroke="#426b51"/>
      {text(cx, cy+8, label, 24, weight=600, text_anchor="middle")}'''


hero = '<ellipse cx="980" cy="220" rx="300" ry="205" fill="url(#wash)"/>'
hero += text(52, 64, "UMANG RAJ / QUALITY ENGINEER & SDET", 19, GREEN, 600, letter_spacing="2")
hero += text(48, 172, "Quality in", 83, weight=700, letter_spacing="-3")
hero += text(48, 265, "every layer.", 83, GREEN, 700, letter_spacing="-3")
hero += text(52, 337, "Automation. Investigation. Evidence.", 26, MUTED)
hero += '<path d="M790 130 960 225 1120 130M790 320 960 225 1120 320" fill="none" stroke="#395a46" stroke-width="2"/>'
hero += '<circle cx="960" cy="232" r="73" fill="#070e0a" opacity=".5"/><circle cx="960" cy="225" r="73" fill="url(#panel)" stroke="#48d99a" stroke-width="1.5"/>'
hero += text(960, 237, "QE", 43, GREEN, 650, text_anchor="middle")
for cx, cy, label in [(790, 130, "UI"), (1120, 130, "API"), (790, 320, "DATABASE"), (1120, 320, "LOGS")]:
    hero += node(cx, cy, label, 162 if label == "DATABASE" else 116)
for cx, cy in [(875, 177), (1040, 177), (875, 272), (1040, 272)]:
    hero += f'<circle class="flow-signal" cx="{cx}" cy="{cy}" r="5" fill="{GREEN}"/>'
svg("profile-hero.svg", 1280, 420, "Umang Raj | Quality Engineer & SDET", "Quality in every layer. A testing workflow connects interfaces, APIs, databases and logs. Its subtle signals are static when reduced motion is preferred.", hero, True)

mobile = '<ellipse cx="580" cy="365" rx="230" ry="180" fill="url(#wash)"/>'
mobile += text(36, 56, "UMANG RAJ / QE & SDET", 24, GREEN, 600, letter_spacing="2")
mobile += text(32, 156, "Quality in", 86, weight=700, letter_spacing="-3")
mobile += text(32, 254, "every layer.", 86, GREEN, 700, letter_spacing="-3")
mobile += '<path d="M112 370h544" stroke="#395a46" stroke-width="3"/>'
for cx, label in [(112, "UI"), (294, "API"), (476, "DATA"), (658, "LOGS")]:
    mobile += node(cx, 370, label, 138)
mobile += text(36, 486, "Automation. Investigation. Evidence.", 29, MUTED)
svg("profile-hero-mobile.svg", 768, 550, "Umang Raj | Quality Engineer & SDET", "Quality in every layer. UI, API, data and log validation.", mobile)

def button(name, label, symbol, primary=False):
    color = "#0d2117" if primary else TEXT
    bg = GREEN if primary else "#122019"
    content = f'<rect x="1" y="1" width="174" height="46" rx="9" fill="{bg}" stroke="{GREEN if primary else "#426b51"}"/>'
    content += icon(symbol, 16, 13, 22, color)
    content += text(49, 30, label, 17, color, 600)
    svg(name, 176, 48, label, label, content)

button("portfolio-link.svg", "Portfolio", "globe", True)
button("linkedin-link.svg", "LinkedIn", "linkedin-logo")

ai = '<ellipse cx="990" cy="145" rx="260" ry="140" fill="url(#wash)"/>'
ai += text(36, 49, "AI FOR QE / LOCAL PROTOTYPE", 20, GREEN, 600, letter_spacing="1.5")
ai += text(34, 116, "AI Test Failure Triage", 58, weight=650, letter_spacing="-1")
ai += text(38, 186, "Test logs + JUnit XML", 30, MUTED)
ai += icon("arrow-up-right", 425, 153, 42)
ai += text(496, 186, "Evidence + next check", 30, MUTED)
ai += icon("test-tube", 1060, 76, 96)
ai += '<path d="M38 231h1124" stroke="#2b4937"/>'
svg("project-triage.svg", 1200, 264, "Open AI Test Failure Triage", "A local QE prototype that reads test logs and JUnit XML and suggests investigation steps. Evaluated on synthetic examples.", ai)

for name, title, subtitle, symbol in [
    ("project-bdd.svg", "Mayors BDD Automation", "Gherkin scenarios | Cucumber | JUnit", "git-branch"),
    ("project-testng.svg", "Selenium & TestNG", "Page objects | Runners | ExtentReports", "test-tube"),
]:
    card = text(36, 69, title, 49, weight=650, letter_spacing="-1")
    card += text(38, 122, subtitle, 27, MUTED)
    card += icon(symbol, 1060, 42, 76)
    svg(name, 1200, 166, f"Open {title}", subtitle, card)

print("Built responsive hero, workflow graphics, project cards and link buttons.")
