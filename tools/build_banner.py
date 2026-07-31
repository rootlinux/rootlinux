#!/usr/bin/env python3
"""Generate dark.svg and light.svg, the animated hero banner for this profile.

Run from the repo root:

    python3 tools/build_banner.py

Both files come from this one source, so they can never drift apart. To change
the banner, edit the data at the top (ROLES, META, SKILLS, TUX) and re-run —
do not hand-edit the SVGs.

--- The one rule that matters -------------------------------------------------

GitHub embeds README SVGs inside <img>. In that context the SMIL animation
clock can stay pinned at t=0: the animations exist but never advance, so what
renders is the FIRST KEYFRAME of every animation.

Therefore: every animation's t=0 frame must be a valid rendering on its own.

Concretely that rules out two things that look natural but render the banner
blank on the profile page:

  * elements that start at opacity="0" and rely on a delayed <animate> to
    appear — their first frame is "invisible", so that is all you ever see;
  * clip-path reveals (the classic typing effect) — with the clock frozen all
    the clip rects sit at their first frame at once, so every phrase in a
    rotation renders on top of the others.

Role rotation is an opacity crossfade instead, and role 1 carries no opacity
attribute at all, so it survives alone when the clock is frozen.
"""

# --- content -----------------------------------------------------------------

NAME = "Berke"
HANDLE = "rootlinux"
TAGLINE = "Everything real starts at the root."
PROMPT = "guest@rootlinux:~$ sudo whoami"
PROMPT_REPLY = "root. don&#8217;t ask how."

ROLES = [
    "Computer Engineering Student",
    "Offensive Security &amp; Red Team",
    "Full-Stack Developer",
]

# (icon path drawn in a 16x16 box, label)
META = [
    ('<path d="M8 15s5.5-5 5.5-8.6A5.5 5.5 0 0 0 2.5 6.4C2.5 10 8 15 8 15z"/>'
     '<circle cx="8" cy="6.3" r="2"/>', "Istanbul, Turkey"),
    ('<path d="M1.5 5.8 8 2.8l6.5 3L8 8.8 1.5 5.8z"/>'
     '<path d="M4.2 7.2v3.6c0 1.1 1.7 1.9 3.8 1.9s3.8-.8 3.8-1.9V7.2"/>',
     "Computer Engineering"),
    ('<circle cx="8" cy="8" r="5.8"/><circle cx="8" cy="8" r="1.9"/>',
     "Building iceq &#8212; E2EE messenger w/ panic-wipe security"),
    ('<rect x="1.6" y="3.6" width="12.8" height="9.2" rx="1.8"/>'
     '<path d="M2.2 4.8 8 9l5.8-4.2"/>', "berkeesahin@proton.me"),
]

# (heading, [row of (label, brand dot colour)]).  "TEXT" means "the theme's
# primary text colour", so Next.js reads white on dark and near-black on light.
SKILLS = [
    ("LANGUAGES", [
        [("Python", "#3776AB"), ("C/C++", "#00599C"),
         ("TypeScript", "#3178C6"), ("Bash", "#4EAA25")],
    ]),
    ("BACKEND &amp; INFRA", [
        [("FastAPI", "#05998B"), ("Next.js", "TEXT"), ("PostgreSQL", "#4169E1"),
         ("Redis", "#DC382D"), ("Docker", "#2496ED")],
    ]),
    ("SECURITY &amp; REVERSING", [
        [("Kali Linux", "#367BF0"), ("Burp Suite", "#FF6633"),
         ("Wireshark", "#1679A7"), ("Ghidra", "#FF6E00")],
        [("gdb / pwndbg", "#A42E2B"), ("Metasploit", "#2596CD"),
         ("Signal Protocol", "#3A76F0"), ("WebAuthn", "#6C4BB6")],
    ]),
]

# Tux on a 31-column monospace grid. Rows are padded to exactly 31 characters;
# the beak and feet cells are left blank here and painted by AMBER below, at
# the same character positions, so they can carry Tux's amber without needing
# a second fill inside one <text>.
TUX = [
    "              ...              ",
    "             :::::             ",
    "          @@@@@@@@@@@          ",
    "        @@@@@@@@@@@@@@@        ",
    "       @@@           @@@       ",
    "      @@@   @@@ @@@   @@@      ",
    "      @@    @o@ @o@    @@      ",
    "      @@    @@@ @@@    @@      ",
    "      @@               @@      ",
    "      @@@             @@@      ",
    "       @@@           @@@       ",
    "       @@@@         @@@@       ",
    "      @@@@           @@@@      ",
    "     @@@@             @@@@     ",
    "    @@@@               @@@@    ",
    "   @@@@                 @@@@   ",
    "  @@@@                   @@@@  ",
    "  @@@@                   @@@@  ",
    " @@@@                     @@@@ ",
    " @@@@                     @@@@ ",
    " @@@@                     @@@@ ",
    "  @@@@                   @@@@  ",
    "  @@@@@                 @@@@@  ",
    "   @@@@@@             @@@@@@   ",
    "    @@@@@@@@       @@@@@@@@    ",
    "       @@@@@@@@@@@@@@@@@       ",
    "          @@@@@@@@@@@          ",
]
AMBER = {                                    # row index -> amber glyphs
     8: "            ooooooo            ",   # beak
     9: "             ooooo             ",
    24: "%%%%                      %%%%",    # feet, splaying outward
    25: "%%%%%%%                %%%%%%%",
    26: "%%%%%%%%               %%%%%%%%",
}

# --- themes ------------------------------------------------------------------

# Tux's own colours: a black-and-white body with an amber beak and feet, on a
# terminal-black card. "tux" is the two stops of the body gradient and is kept
# separate from "accent" so the body can stay Tux-coloured while the interface
# takes the amber.
DARK = dict(
    name="dark",
    card="#0A0A0C", panel="#141418", text="#F5F5F7", muted="#8B8B94",
    accent="#FCBF49", accent2="#F5843C", amber="#FCBF49",
    blobs=("#F5843C", "#FCBF49", "#B45309"),
    tux=("#FFFFFF", "#9CA3AF"),          # white -> grey, readable on black
    left_panel=("#ffffff", "0.02"), border=("#ffffff", "0.08"),
    hairline=("#ffffff", "0.06"), pill=("#ffffff", "0.04"),
    titlebar=("#ffffff", "0.02"), glass="0.06",
    shimmer=("#ffffff", "0.55"), scanline="0.06", blob=1.0,
    noise="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0",
)
LIGHT = dict(
    name="light",
    card="#FFFFFF", panel="#FAFAFA", text="#18181B", muted="#52525B",
    accent="#B45309", accent2="#EA580C", amber="#C2740B",
    blobs=("#FBBF24", "#FB923C", "#FDE68A"),
    tux=("#3F3F46", "#18181B"),          # dark body on white, as Tux is drawn
    left_panel=("#FAFAFA", "0.7"), border=("#18181B", "0.10"),
    hairline=("#18181B", "0.08"), pill=("#FFFFFF", "0.9"),
    titlebar=("#18181B", "0.025"), glass="0.75",
    shimmer=("#B45309", "0.40"), scanline="0.05", blob=0.34,
    noise="0 0 0 0 0.06  0 0 0 0 0.09  0 0 0 0 0.16  0 0 0 0.035 0",
)

# --- layout ------------------------------------------------------------------

W, H = 1180, 610
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,sans-serif"
TUX_X, TUX_Y0, TUX_DY = 248, 140.0, 13.2
PILL_H, PILL_GAP, DOT_X, LABEL_X, PAD_R, CHAR_W = 30, 8, 16, 28, 14, 6.7
PANEL_R = 1132          # right edge available to the terminal panel's content


def blob(t, colour, peak):
    return round(peak * t["blob"], 3)


def build(t):
    dot_of = lambda c: t["text"] if c == "TEXT" else c
    o = []
    w = o.append

    w(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'xmlns="http://www.w3.org/2000/svg">')
    w(f'  <title>{NAME} ({HANDLE}) - Computer Engineering student, offensive '
      f'security and red team, building iceq</title>')

    # -- defs --
    w('  <defs>')
    w(f'    <clipPath id="cardClip"><rect x="1" y="1" width="{W - 2}" '
      f'height="{H - 2}" rx="28"/></clipPath>')
    w('    <clipPath id="leftClip"><rect x="24" y="24" width="448" height="562" rx="20"/></clipPath>')
    w('    <clipPath id="termClip"><rect x="496" y="24" width="660" height="562" rx="16"/></clipPath>')
    w('    <filter id="glowSoft" x="-40%" y="-40%" width="180%" height="180%">')
    w('      <feGaussianBlur stdDeviation="1.1" result="blur"/>')
    w('      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    w('    </filter>')
    w('    <filter id="noiseFilter" x="0" y="0" width="100%" height="100%">')
    w('      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" '
      'stitchTiles="stitch" result="noise"/>')
    w(f'      <feColorMatrix in="noise" type="matrix" values="{t["noise"]}"/>')
    w('    </filter>')
    tux1, tux2 = t["tux"]
    w('    <linearGradient id="tuxGradient" gradientUnits="userSpaceOnUse" x1="120" y1="0" x2="380" y2="0">')
    for off, c in (("0%", tux1), ("50%", tux2), ("100%", tux1)):
        w(f'      <stop offset="{off}" stop-color="{c}"/>')
    w('      <animateTransform attributeName="gradientTransform" type="translate" '
      'values="-130 0;130 0;-130 0" dur="7s" repeatCount="indefinite"/>')
    w('    </linearGradient>')
    sc, so = t["shimmer"]
    w(f'    <linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">')
    for off, op in (("0%", "0"), ("45%", "0"), ("50%", so), ("55%", "0"), ("100%", "0")):
        w(f'      <stop offset="{off}" stop-color="{sc}" stop-opacity="{op}"/>')
    w(f'      <animateTransform attributeName="gradientTransform" type="rotate" '
      f'values="0 590 305;360 590 305" dur="6s" repeatCount="indefinite"/>')
    w('    </linearGradient>')
    w('    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">')
    w(f'      <stop offset="0%" stop-color="#ffffff" stop-opacity="{t["glass"]}"/>')
    w('      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>')
    w('    </linearGradient>')
    b1, b2, b3 = t["blobs"]
    for gid, colour, peak in (("blob1", b1, 0.30), ("blob2", b2, 0.28),
                              ("blob3", b3, 0.22), ("blobAccent", t["accent"], 0.30)):
        w(f'    <radialGradient id="{gid}" cx="50%" cy="50%" r="50%">')
        w(f'      <stop offset="0%" stop-color="{colour}" stop-opacity="{blob(t, colour, peak)}"/>')
        w(f'      <stop offset="100%" stop-color="{colour}" stop-opacity="0"/>')
        w('    </radialGradient>')
    w('  </defs>')
    w('')

    # -- card + ambient background --
    w(f'  <rect x="0" y="0" width="{W}" height="{H}" rx="28" fill="{t["card"]}"/>')
    w('  <g clip-path="url(#cardClip)">')
    for cx, cy, r, gid, vals, dur in (
        (150, 150, 180, "blob1", "0,0;30,20;-10,25;0,0", 18),
        (1000, 480, 200, "blob2", "0,0;-25,-15;15,-30;0,0", 22),
        (600, 550, 150, "blob3", "0,0;20,-10;-15,10;0,0", 16),
    ):
        w(f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})">'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="{vals}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    w(f'    <rect x="0" y="-10" width="{W}" height="3" fill="{t["accent"]}" opacity="{t["scanline"]}">'
      f'<animate attributeName="y" values="-10;{H + 10}" dur="7s" repeatCount="indefinite"/></rect>')
    w(f'    <rect x="0" y="0" width="{W}" height="{H}" filter="url(#noiseFilter)" opacity="0.04">'
      f'<animate attributeName="opacity" values="0.03;0.05;0.03" dur="6s" repeatCount="indefinite"/></rect>')
    w(f'    <g fill="{t["accent"]}">')
    for cx, cy, r, op, dur, delay, alt in (
        (100, 500, 2, 0.4, 5, 0, False), (380, 80, 1.5, 0.3, 6, 0.6, False),
        (900, 300, 2.5, 0.3, 7, 1.2, True), (1080, 180, 1.5, 0.4, 5.5, 1.8, False),
        (560, 560, 2, 0.3, 8, 2.4, True), (850, 520, 1.5, 0.35, 6.5, 3, False),
    ):
        fill = f' fill="{t["accent2"]}"' if alt else ""
        w(f'      <circle cx="{cx}" cy="{cy}" r="{r}" opacity="{op}"{fill}>'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="0,0;0,-14;0,0" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/></circle>')
    w('    </g>')
    w('  </g>')
    bc, bo = t["border"]
    w(f'  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="none" '
      f'stroke="url(#shimmer)" stroke-width="2"/>')
    w(f'  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="none" '
      f'stroke="{bc}" stroke-opacity="{bo}" stroke-width="1"/>')
    w('')

    # -- left panel: ASCII Tux --
    lc, lo = t["left_panel"]
    hc, ho = t["hairline"]
    w('  <g clip-path="url(#leftClip)">')
    w(f'    <rect x="24" y="24" width="448" height="562" fill="{lc}" fill-opacity="{lo}"/>')
    w('    <rect x="24" y="24" width="448" height="100" fill="url(#glass)"/>')
    w('  </g>')
    w(f'  <rect x="24" y="24" width="448" height="562" rx="20" fill="none" '
      f'stroke="{hc}" stroke-opacity="{ho}"/>')
    for cx, gid, delay in ((230, "blobAccent", "0s"), (266, "blob2", "0.5s")):
        w(f'  <circle cx="{cx}" cy="320" r="150" fill="url(#{gid})">'
          f'<animate attributeName="opacity" values="0.7;1;0.7" dur="5s" '
          f'repeatCount="indefinite" begin="{delay}"/></circle>')
    w(f'  <text x="{TUX_X}" y="88" text-anchor="middle" font-family="{MONO}" '
      f'font-size="13" fill="{t["muted"]}">{PROMPT}</text>')
    w(f'  <text x="{TUX_X}" y="110" text-anchor="middle" font-family="{MONO}" '
      f'font-size="14" font-weight="700" fill="{t["accent"]}">{PROMPT_REPLY}</text>')
    w(f'  <g font-family="{MONO}" font-size="12" text-anchor="middle">')
    w('    <animateTransform attributeName="transform" type="translate" '
      'values="0,0;0,-6;0,0" dur="5s" repeatCount="indefinite"/>')
    w('    <g fill="url(#tuxGradient)" filter="url(#glowSoft)">')
    for i, row in enumerate(TUX):
        if row.strip():
            w(f'      <text xml:space="preserve" x="{TUX_X}" '
              f'y="{round(TUX_Y0 + i * TUX_DY, 1)}">{row}</text>')
    w('    </g>')
    w(f'    <g fill="{t["amber"]}" filter="url(#glowSoft)">')
    for i, row in sorted(AMBER.items()):
        w(f'      <text xml:space="preserve" x="{TUX_X}" '
          f'y="{round(TUX_Y0 + i * TUX_DY, 1)}">{row}</text>')
    w('    </g>')
    w('  </g>')
    w(f'  <text x="{TUX_X}" y="512" text-anchor="middle" font-family="{MONO}" '
      f'font-size="15" fill="{t["accent"]}">&#9612;'
      f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></text>')
    w(f'  <text x="{TUX_X}" y="548" text-anchor="middle" font-family="{SANS}" '
      f'font-size="12" font-style="italic" fill="{t["muted"]}">{TAGLINE}</text>')
    w('')

    # -- right panel: terminal --
    w('  <g clip-path="url(#termClip)">')
    w(f'    <rect x="496" y="24" width="660" height="562" fill="{t["panel"]}" fill-opacity="0.92"/>')
    tc, to = t["titlebar"]
    w(f'    <rect x="496" y="24" width="660" height="40" fill="{tc}" fill-opacity="{to}"/>')
    w('    <rect x="496" y="24" width="660" height="120" fill="url(#glass)"/>')
    for cx, c in ((516, "#FF5F56"), (536, "#FFBD2E"), (556, "#27C93F")):
        w(f'    <circle cx="{cx}" cy="44" r="6" fill="{c}"/>')
    w('  </g>')
    w(f'  <rect x="496" y="24" width="660" height="562" rx="16" fill="none" '
      f'stroke="{bc}" stroke-opacity="{bo}"/>')
    w('')
    w(f'  <g font-family="{SANS}">')
    w(f'    <text x="524" y="104" font-size="26" font-weight="700" '
      f'fill="{t["text"]}">Hi &#128075; I&#8217;m {NAME}</text>')
    w('')

    # role rotation — see the module docstring for why this is not clip-path
    cycle, anims = 9, [
        'values="1;1;0;0;1" keyTimes="0;0.31;0.35;0.96;1"',
        'values="0;0;1;1;0;0" keyTimes="0;0.31;0.35;0.64;0.68;1"',
        'values="0;0;1;1;0" keyTimes="0;0.64;0.68;0.96;1"',
    ]
    w(f'    <g font-size="20" font-weight="500" fill="{t["accent"]}">')
    for i, (role, anim) in enumerate(zip(ROLES, anims)):
        hidden = "" if i == 0 else ' opacity="0"'   # role 1 must survive a frozen clock
        w(f'      <text x="524" y="148"{hidden}>{role}'
          f'<tspan dx="6">&#9612;<animate attributeName="opacity" values="1;0;1" '
          f'dur="1s" repeatCount="indefinite"/></tspan>'
          f'<animate attributeName="opacity" {anim} dur="{cycle}s" repeatCount="indefinite"/></text>')
    w('    </g>')
    w('')

    w(f'    <g font-size="15" fill="{t["muted"]}">')
    for i, (icon, label) in enumerate(META):
        y = 190 + i * 26
        w(f'      <g transform="translate(524,{y - 12})" stroke="{t["accent"]}" stroke-width="1.4" '
          f'fill="none" stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
        w(f'      <text x="550" y="{y}">{label}</text>')
    w('    </g>')
    w('')

    pc, po = t["pill"]
    y = 296
    for heading, rows in SKILLS:
        w(f'    <text x="524" y="{y}" font-size="10" letter-spacing="2" '
          f'fill="{t["muted"]}">{heading}</text>')
        for cells in rows:
            y += 8
            x = 520
            for label, dot in cells:
                width = round(LABEL_X + len(label.replace("&amp;", "&")) * CHAR_W + PAD_R)
                w(f'      <g><rect x="{x}" y="{y}" width="{width}" height="{PILL_H}" rx="15" '
                  f'fill="{pc}" fill-opacity="{po}" stroke="{t["accent"]}" stroke-opacity="0.3"/>'
                  f'<circle cx="{x + DOT_X}" cy="{y + PILL_H // 2}" r="4" fill="{dot_of(dot)}"/>'
                  f'<text x="{x + LABEL_X}" y="{y + 20}" font-size="12.5" '
                  f'fill="{t["text"]}">{label}</text></g>')
                x += width + PILL_GAP
            if x > PANEL_R:
                raise SystemExit(f"skills row overflows the panel: {heading} ends at x={x}")
            y += PILL_H + 6
        y += 14

    gh = ("M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
          "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 "
          "17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 "
          "1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-"
          "2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 "
          "3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 "
          "3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 "
          "1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627"
          "-5.373-12-12-12")
    if y + 34 > 586:
        raise SystemExit(f"social chip overflows the panel: bottom would be {y + 34}")
    w(f'    <g><rect x="520" y="{y}" width="208" height="34" rx="17" fill="{pc}" '
      f'fill-opacity="{po}" stroke="{t["accent"]}" stroke-opacity="0.3"/>'
      f'<g transform="translate(536,{y + 9}) scale(0.667)" fill="{t["text"]}"><path d="{gh}"/></g>'
      f'<text x="568" y="{y + 22}" font-size="14" fill="{t["text"]}">github.com/{HANDLE}</text></g>')
    w('  </g>')
    w('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    # Parses only this script's own output — no untrusted input, no DTD, no
    # entity declarations — so the stdlib parser is used purely as a
    # well-formedness check (it catches unbalanced tags and bad escaping).
    from xml.etree import ElementTree

    for theme in (DARK, LIGHT):
        svg = build(theme)
        ElementTree.fromstring(svg)
        path = f'{theme["name"]}.svg'
        with open(path, "w") as fh:
            fh.write(svg)
        print(f"wrote {path} ({len(svg):,} bytes)")
