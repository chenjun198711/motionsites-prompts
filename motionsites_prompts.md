# MotionSites 免费提示词汇总

共 114 个免费提示词

---

## 1. Interactive Discovery

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `interactive-discovery`

```
Build a full-screen, dark-themed hero section for a geology brand called **Lithos**, using **React 18 + TypeScript + Vite + Tailwind CSS** and **lucide-react** for icons. The signature feature is a **cursor-following spotlight that reveals a second image** through a soft circular mask on top of a base image. Match every detail below exactly.

### Fonts
Add this to the top of `src/index.css`, then `@tailwind base/components/utilities`:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,400;1,500;1,600&display=swap');
* { font-family: 'Inter', sans-serif; }
.font-playfair { font-family: 'Playfair Display', serif; }
```
- Body/UI font: **Inter**.
- Display/wordmark accent: **Playfair Display, italic**.

### Asset URLs (use these exactly)
- Base image (`BG_IMAGE_1`):
  `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_195923_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png&w=1280&q=85`
- Reveal image (`BG_IMAGE_2`):
  `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_201152_bba90a12-bf12-459f-91f0-51f237dbaf3b.png&w=1280&q=85`

### Layout & structure
Root wrapper: `min-h-screen bg-white tracking-[-0.02em]`, inline `fontFamily: "'Inter', sans-serif"`.

**Section** (`<section>`): `relative w-full overflow-hidden h-screen bg-black`, inline `style={{ height: '100dvh' }}`. Layers, by z-index:
1. **Base image** (`z-10`): `absolute inset-0 bg-center bg-cover bg-no-repeat`, background = `BG_IMAGE_1`.
2. **Reveal layer** (`z-30`): a `RevealLayer` component (see below) showing `BG_IMAGE_2`.
3. **Heading** (`z-50`): `absolute top-[14%] left-0 right-0 flex flex-col items-center text-center px-5 pointer-events-none`. An `<h1>` with `text-white leading-[0.95]` containing two block spans:
   - Line 1: `block font-playfair italic font-normal text-5xl sm:text-7xl md:text-8xl`, inline `letterSpacing: '-0.05em'`, text **"Layers hold"**.
   - Line 2: `block font-normal text-5xl sm:text-7xl md:text-8xl -mt-1`, inline `letterSpacing: '-0.08em'`, text **"tales of time"**.
4. **Bottom-left paragraph** (`z-50`): `hidden sm:block absolute bottom-14 left-10 md:left-14 max-w-[260px]`. `<p className="text-sm text-white/80 leading-relaxed">` — "Every layer of sediment records a chapter of our planet, from ancient seabeds to drifting ash, layered across millions of years beneath us."
5. **Bottom-right block** (`z-50`): `absolute bottom-10 sm:bottom-24 left-5 right-5 sm:left-auto sm:right-10 md:right-14 max-w-full sm:max-w-[260px] flex flex-col items-start gap-4 sm:gap-5`. Contains a `<p className="text-xs sm:text-sm text-white/80 leading-relaxed">` — "Our interactive maps let you peel back the crust to trace how stones, fossils, and deep time combine to shape the ground beneath your feet." — and a **Start Digging** button: `bg-[#e8702a] hover:bg-[#d2611f] text-white text-sm font-medium px-7 py-3 rounded-full transition-all hover:scale-[1.03] active:scale-95 hover:shadow-lg hover:shadow-[#e8702a]/30`.

### The cursor spotlight reveal (core mechanic)
In the parent, define `const SPOTLIGHT_R = 260;` and track the mouse with smoothing:
- Refs: `mouse` (raw), `smooth` (eased), `rafRef`; state `cursorPos` (init `{x:-999,y:-999}`).
- `mousemove` listener stores raw `e.clientX/clientY`.
- A `requestAnimationFrame` loop lerps: `smooth.x += (mouse.x - smooth.x) * 0.1` (same for y), then `setCursorPos`. Clean up listener + cancel RAF on unmount.

`RevealLayer({ image, cursorX, cursorY })`:
- Holds a hidden `<canvas>` (`absolute inset-0 pointer-events-none`, `style={{display:'none'}}`) sized to `window.innerWidth/Height` on mount + resize.
- A reveal `<div>` (`absolute inset-0 bg-center bg-cover bg-no-repeat z-30 pointer-events-none`) with the reveal image as background.
- On every render: clear canvas, build a **radial gradient** at `(cursorX, cursorY)` from radius 0 → `SPOTLIGHT_R` with stops:
  `0 → rgba(255,255,255,1)`, `0.4 → 1`, `0.6 → 0.75`, `0.75 → 0.4`, `0.88 → 0.12`, `1 → 0`.
  Fill an arc of radius `SPOTLIGHT_R` with it. Then `canvas.toDataURL()` and apply it as `maskImage`/`webkitMaskImage` on the reveal div with `maskSize: '100% 100%'`. This makes the second image visible only inside the soft glowing circle that trails the cursor.

### Navigation (fixed, over hero)
`<nav className="fixed top-0 left-0 right-0 z-[100] flex items-center justify-between p-4 sm:p-5">`:
- **Left**: an inline SVG logo (26×26, viewBox `0 0 256 256`, `fill="#ffffff"`, path `M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z`) + wordmark `<span className="text-white text-2xl font-playfair italic">Lithos</span>`.
- **Center pill** (`hidden md:flex absolute left-1/2 -translate-x-1/2 bg-white/20 backdrop-blur-md border border-white/30 rounded-full px-2 py-2 items-center gap-1`): buttons **Course** (active: full white text), then **Field Guides, Geology, Plans, Live Tour** (`text-white/80 ... hover:bg-white/20 hover:text-white transition-colors`, `px-4 py-1.5 rounded-full text-sm font-medium`).
- **Right (desktop)**: `hidden md:block bg-white text-gray-900 text-sm font-semibold px-6 py-2.5 rounded-full hover:bg-gray-100` — **Sign Up**.

### Animations (premium, on load)
Add to `index.css`:
```css
@keyframes heroReveal { 0%{opacity:0;transform:translateY(28px);filter:blur(12px)} 100%{opacity:1;transform:translateY(0);filter:blur(0)} }
@keyframes heroFadeUp { 0%{opacity:0;transform:translateY(20px)} 100%{opacity:1;transform:translateY(0)} }
@keyframes heroZoom { 0%{transform:scale(1.12)} 100%{transform:scale(1)} }
.hero-anim { opacity:0; animation-fill-mode:forwards; animation-timing-function:cubic-bezier(0.16,1,0.3,1); }
.hero-reveal { animation-name:heroReveal; animation-duration:1.1s; }
.hero-fade { animation-name:heroFadeUp; animation-duration:1s; }
.hero-zoom { animation:heroZoom 1.8s cubic-bezier(0.16,1,0.3,1) forwards; }
@media (prefers-reduced-motion: reduce){ .hero-anim,.hero-zoom{ animation:none; opacity:1; } }
```
Apply:
- Base image div → add `hero-zoom` (slow Ken Burns zoom-out).
- Heading line 1 → `hero-anim hero-reveal`, inline `animationDelay: '0.25s'`; line 2 → same with `'0.42s'` (blur-rise, staggered).
- Bottom-left paragraph wrapper → `hero-anim hero-fade`, `animationDelay: '0.7s'`.
- Bottom-right wrapper → `hero-anim hero-fade`, `animationDelay: '0.85s'`.

### Responsiveness
- Heading scales `text-5xl` → `sm:text-7xl` → `md:text-8xl`.
- Center nav pill and desktop Sign Up are `hidden` below `md`; the mobile hamburger is `md:hidden`.
- Bottom-left paragraph is `hidden sm:block`; bottom-right block is full-width on mobile (`left-5 right-5`) and right-anchored from `sm`.
- Use `100dvh` so mobile browser chrome doesn't clip the section.
```

---

## 2. Bold Studio

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `bold-studio`

```
Build a fullscreen hero landing page for a creative agency called "VANGUARD" using React, Tailwind CSS, and Vite. The page should be a single viewport-height section with a looping background video and all content overlaid on top.

**Background video:**
Use this exact CloudFront URL as a fullscreen `<video>` element with `autoPlay`, `muted`, `loop`, and `playsInline` attributes, set to `object-cover` to fill the entire viewport:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260606_154941_df1a96e1-a06f-450c-bd02-d863414cc1a0.mp4
```

**Fonts (loaded in index.html):**
1. "FSP DEMO - PODIUM Sharp 4.11" from `https://db.onlinewebfonts.com/c/8b75d9dcff6a48c35a46656192adf019?family=FSP+DEMO+-+PODIUM+Sharp+4.11` -- used for the brand name and main heading. Create a `.font-podium` utility class for it and register it in tailwind.config.js as `fontFamily.podium`.
2. "Inter" from Google Fonts (weights 400, 500, 600, 700) -- used for body text, nav links, stats, and CTAs. Register it in tailwind.config.js as `fontFamily.inter`.

**Icons:** Use `lucide-react` for all icons: `ArrowUpRight`, `Award`, `Crown`, and `X`.

**Navbar:**
- Horizontal bar at the top with responsive padding (`px-6 sm:px-10 lg:px-16`, `py-5 lg:py-7`).
- Left: brand name "VANGUARD" in `font-podium`, white, bold, uppercase, `text-2xl sm:text-3xl`, `tracking-wider`.
- Center (hidden below `md`): four nav links -- "Projects", "Studio", "Offerings", "Inquire" -- in `font-inter`, `text-sm`, `text-white/80`, `tracking-widest`, uppercase, with `hover:text-white` transition.
- Right (hidden below `md`): a "GET IN TOUCH" link with an `ArrowUpRight` icon, styled as a bordered button (`border border-white/30 hover:border-white/60`, `px-6 py-3`, `text-xs`, `tracking-widest`, uppercase, `hover:bg-white/10`).
- Right (visible below `md`): a hamburger button made of three white `div` bars (`w-6 h-0.5`, `w-6 h-0.5`, `w-4 h-0.5` with `space-y-1.5`).

**Mobile Menu Overlay (below `md` only):**
- Fixed fullscreen overlay (`fixed inset-0 z-50`) with `bg-black/95 backdrop-blur-sm`.
- Toggles visibility via React `useState` -- when open: `opacity-100 visible`, when closed: `opacity-0 invisible`, with `transition-all duration-500`.
- Header row matches the navbar: brand name on left, `X` close icon on right.
- Centered vertically: each of the 4 nav links rendered in `font-podium`, `text-4xl sm:text-5xl`, white, uppercase, with staggered entrance animations using inline `style` -- each item gets `transitionDelay: i * 80 + 100ms`, `opacity` and `translateY(20px)` transitions based on the open state.
- Below the links: a "GET IN TOUCH" bordered button with the same staggered animation pattern.
- All links call `setMenuOpen(false)` on click.

**Hero Content (vertically centered, left-aligned):**
All hero elements use staggered `animate-fade-up` animations (defined in CSS as `@keyframes fade-up` translating from `translateY(30px), opacity:0` to `translateY(0), opacity:1` over `0.8s ease-out`). Each successive element has an additional `0.2s` delay. Elements start with `opacity: 0` and use `animation-fill-mode: forwards`.

1. **Tagline:** A `Crown` icon (lucide, `w-4 h-4`, `text-white/70`) followed by "World-Class Digital Collective" in `text-white/70`, `text-xs sm:text-sm`, `font-inter`, `tracking-[0.3em]`, uppercase. Uses `animate-fade-up` (no delay). Has `mb-6 lg:mb-8`.

2. **Main Heading:** Three lines in `font-podium`, white, uppercase, `leading-[0.92]`, `tracking-tight`, each using `text-[clamp(2.8rem,8vw,7rem)]`:
   - "Design."
   - "Disrupt."
   - "Conquer."
   Uses `animate-fade-up-delay-1` (0.2s delay).

3. **Subtext:** "We build fierce brand identities" (line break) "that don't just turn heads --" then bold white "they lead." in `text-white/70`, `text-sm sm:text-base`, `font-inter`, `leading-relaxed`, `max-w-md`. Uses `animate-fade-up-delay-2` (0.4s delay). `mt-6 lg:mt-8`.

4. **CTA Row:** Uses `animate-fade-up-delay-3` (0.6s delay), `mt-8 lg:mt-10`, `flex flex-wrap items-center gap-4 sm:gap-6`.
   - Black button "SEE OUR WORK" with `ArrowUpRight` icon. `bg-black hover:bg-neutral-900`, `px-5 sm:px-7 py-3 sm:py-4`, `text-[11px] sm:text-xs`, `tracking-widest`, uppercase. Arrow has `group-hover:translate-x-0.5 group-hover:-translate-y-0.5` transition.
   - Beside it (hidden on mobile, `hidden sm:flex`): an `Award` icon (`w-8 h-8`, `text-white/50`) with two lines of text: "Top-Rated" / "Brand Studio" in `text-white/60`, `text-xs`, `tracking-wider`, uppercase.

5. **Stats Row:** Uses `animate-fade-up-delay-4` (0.8s delay), `mt-8 sm:mt-10 lg:mt-14`, `flex flex-wrap gap-6 sm:gap-12 lg:gap-16`. Three stats:
   - "250+" / "Brands Transformed"
   - "95%" / "Client Retention"
   - "10+" / "Years in the Game"
   Values in `font-inter`, white, `text-2xl sm:text-4xl lg:text-5xl`, bold, `tracking-tight`. Labels in `text-white/50`, `text-[9px] sm:text-xs`, `tracking-widest`, uppercase, `mt-1`.

**CSS Animations (defined in index.css under `@layer utilities`):**
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes scale-in {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
```
With classes: `.animate-fade-up` (0s delay), `.animate-fade-up-delay-1` through `.animate-fade-up-delay-4` (0.2s increments, starting `opacity: 0`), `.animate-fade-in`, `.animate-fade-in-delay`.

**Responsive behavior:**
- Full layout is mobile-first with breakpoints at `sm` (640px), `md` (768px), and `lg` (1024px).
- Nav links and "GET IN TOUCH" button show at `md`+; hamburger shows below `md`.
- Award badge hides on mobile (`hidden sm:flex`).
- All text sizes, paddings, gaps, and margins scale up through `sm:` and `lg:` prefixes.
- Stats and CTA row use `flex-wrap` to prevent overflow on small screens.

Make everything fully mobile responsive. Use a single `App.tsx` component with `useState` for the menu toggle. No routing needed.
```

---

## 3. Prisma Creative Studio

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: landing
- **ID**: `prisma-landing`

```
Create a React + Vite + TypeScript + Tailwind CSS landing page for a creative studio called "Prisma". The page has 3 sections: Hero, About, and Features. Use framer-motion for animations and lucide-react for icons. The design is dark, moody, and cinematic with a warm cream color palette.

FONTS

Load two Google Fonts in index.html:

Almarai (weights: 300, 400, 700, 800) -- used as the global default font
Instrument Serif (italic only) -- used for italic accent text in the About section
In index.css, set the global font family:


* { font-family: 'Almarai', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif; }
In tailwind.config.js, extend:

colors.primary: #DEDBC8 (warm cream, used for all primary text and accents)
fontFamily.serif: ['"Instrument Serif"', 'serif']
COLOR SYSTEM

Background: black (#000000) globally, #101010 for the About card, #212121 for Features cards
Primary text color: #E1E0CC (applied via inline style, slightly different from Tailwind primary)
Tailwind primary: #DEDBC8 (used for utility classes like text-primary, text-primary/70)
Gray text: text-gray-400, text-gray-500
Navbar link color: rgba(225, 224, 204, 0.8) with hover: #E1E0CC
CUSTOM CSS UTILITIES (index.css)

Two SVG noise texture utilities:

.noise-overlay: fractal noise (baseFrequency: 0.85, numOctaves: 3) used as overlay on hero video
.bg-noise: fractal noise (baseFrequency: 0.9, numOctaves: 4) used as subtle background in Features section
Both use inline SVG data URIs with feTurbulence filter.

SECTION 1: HERO

Full viewport height (h-screen). The entire section has p-4 md:p-6 padding creating an inset effect. Inside is a container with rounded-2xl md:rounded-[2rem] and overflow-hidden.

Background video:

URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_170732_8a9ccda6-5cff-4628-b164-059c500a2b41.mp4
autoPlay loop muted playsInline, object-cover, fills entire container
Noise overlay on top: .noise-overlay with opacity-[0.7] mix-blend-overlay pointer-events-none
Gradient overlay: bg-gradient-to-b from-black/30 via-transparent to-black/60
Navbar:

Absolutely positioned at top center
Black background pill that hangs from top edge: bg-black rounded-b-2xl md:rounded-b-3xl px-4 py-2 md:px-8
5 nav items: "Our story", "Collective", "Workshops", "Programs", "Inquiries"
Text size: text-[10px] sm:text-xs md:text-sm
Gap between items: gap-3 sm:gap-6 md:gap-12 lg:gap-14
Link color: rgba(225, 224, 204, 0.8), hover: #E1E0CC (inline styles)
Hero Content (bottom-aligned):

Absolutely positioned at bottom: absolute bottom-0 left-0 right-0
12-column grid: left 8 columns for heading, right 4 columns for text + button
Giant heading "Prisma" using WordsPullUp component:
Responsive sizes: text-[26vw] sm:text-[24vw] md:text-[22vw] lg:text-[20vw] xl:text-[19vw] 2xl:text-[20vw]
font-medium leading-[0.85] tracking-[-0.07em]
Color: #E1E0CC
Has a superscript asterisk (*) on the final "a" of "Prisma": positioned with absolute top-[0.65em] -right-[0.3em] text-[0.31em]
Pull-up animation: each word slides up from y:20 with staggered delay of 0.08s, triggered by useInView
Description paragraph (right column):
"Prisma is a worldwide network of visual artists, filmmakers and storytellers bound not by place, status or labels but by passion and hunger to unlock potential through our unique perspectives."
text-primary/70 text-xs sm:text-sm md:text-base, line-height: 1.2
Framer motion: fade up from y:20, delay 0.5s, custom ease [0.16, 1, 0.3, 1]
CTA Button "Join the lab":
Pill shape: bg-primary rounded-full
Black text, font-medium, text-sm sm:text-base
Right side has a black circle (bg-black rounded-full w-9 h-9 sm:w-10 sm:h-10) containing a white/cream ArrowRight icon
Hover: gap increases (hover:gap-3), circle scales up (group-hover:scale-110)
Framer motion: fade up from y:20, delay 0.7s, same custom ease
SECTION 2: ABOUT

bg-black, padded section with centered content
Inner card: bg-[#101010], centered text, max-w-6xl
Top: small label "Visual arts" in text-primary, text-[10px] sm:text-xs
Main heading uses WordsPullUpMultiStyle component with 3 segments:
"I am Marcus Chen," -- font-normal (Almarai)
"a self-taught director." -- italic font-serif (Instrument Serif italic)
"I have skills in color grading, visual effects, and narrative design." -- font-normal
Container: text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl max-w-3xl mx-auto leading-[0.95] sm:leading-[0.9]
Each word animates in with pull-up effect (y:20 to y:0), staggered at 0.08s delay
Body paragraph below with scroll-linked character opacity animation:
Text: "Over the last seven years, I have worked with Parallax, a Berlin-based production house that crafts cinema, series, and Noir Studio in Paris. Together, we have created work that has earned international acclaim at several major festivals."
text-[#DEDBC8], text-xs sm:text-sm md:text-base
Each character is individually wrapped in an AnimatedLetter component
Uses useScroll with target offset ['start 0.8', 'end 0.2']
Each character's opacity transitions from 0.2 to 1 based on scroll position, creating a progressive text reveal effect
Character staggering: charProgress = index / totalChars, range [charProgress - 0.1, charProgress + 0.05]
SECTION 3: FEATURES

min-h-screen bg-black, with subtle .bg-noise overlay at opacity-[0.15]
Header text uses WordsPullUpMultiStyle:
Line 1: "Studio-grade workflows for visionary creators." in cream
Line 2: "Built for pure vision. Powered by art." in text-gray-500
Both: text-xl sm:text-2xl md:text-3xl lg:text-4xl font-normal
4-column card grid (lg:h-[480px], gap-3 sm:gap-2 md:gap-1):

Each card has staggered entrance animation: scale from 0.95 + fade in, triggered by useInView (once, margin "-100px"), staggered at 0.15s intervals with ease [0.22, 1, 0.36, 1].

Card 1 - Video card: Full video background (URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260406_133058_0504132a-0cf3-4450-a370-8ea3b05c95d4.mp4), autoPlay loop muted playsInline, object-cover. Bottom text: "Your creative canvas." in #E1E0CC.

Card 2 - "Project Storyboard." (01): bg-[#212121], small image icon at top (https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171918_4a5edc79-d78f-4637-ac8b-53c43c220606.png&w=1280&q=85, 10x10 sm:12x12 rounded), title with number, 4 checklist items with green Check icons, "Learn more" link with rotated arrow (-45deg).

Card 3 - "Smart Critiques." (02): Same layout as Card 2. Icon: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171741_ed9845ab-f5b2-4018-8ce7-07cc01823522.png&w=1280&q=85. 3 checklist items about AI analysis, creative notes, tool integrations.

Card 4 - "Immersion Capsule." (03): Same layout. Icon: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260405_171809_f56666dc-c099-4778-ad82-9ad4f209567b.png&w=1280&q=85. 3 checklist items about notification silencing, ambient soundscapes, schedule syncing.

All feature card checklist items use Check icon from lucide-react in text-primary color, with text-gray-400 description text. "Learn more" buttons use ArrowRight rotated -45deg.

SHARED ANIMATION COMPONENTS

WordsPullUp: Splits text by spaces, each word is a motion.span that slides up (y:20 to 0) with staggered delay. Uses useInView (once: true). Supports showAsterisk prop that adds a superscript * after the last character "a" of the final word.

WordsPullUpMultiStyle: Takes an array of {text, className} segments, splits all into individual words preserving per-word className. Same pull-up animation. Words are wrapped in inline-flex flex-wrap justify-center.

RESPONSIVE BREAKPOINTS

The page is fully responsive across mobile, tablet, and desktop. Cards in Features switch from 1-col (mobile) to 2-col (md) to 4-col (lg). Hero text scales from 26vw down to 19vw. Navbar items compress with smaller gaps on mobile. All padding, font sizes, and spacing use Tailwind responsive prefixes (sm/md/lg/xl/2xl).

TECH STACK

Vite + React 18 + TypeScript
Tailwind CSS 3
framer-motion (for all animations: pull-up text, fade-in, scroll-linked opacity, card entrances)
lucide-react (ArrowRight, Check icons)
```

---

## 4. 3D Jack Portfolio

- **Category**: Portfolio
- **Type**: hero
- **Page Type**: landing
- **ID**: `3d-jack-portfolio-hero`

```
Build a 3D Creator portfolio landing page for "Jack" using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React. The page has a dark theme (#0C0C0C background) with the font Kanit (Google Fonts, weights 300-900). The page title is "Jack -- 3D Creator".

GLOBAL STYLES
Background: #0C0C0C on html, body, #root, and the main wrapper
Font family: 'Kanit', sans-serif
Global reset: box-sizing border-box, margin 0, padding 0
CSS class .hero-heading: gradient text using background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%) with -webkit-background-clip: text and -webkit-text-fill-color: transparent
Main wrapper has overflowX: 'clip'
SECTION ORDER
HeroSection
MarqueeSection
AboutSection
ServicesSection
ProjectsSection
1. HERO SECTION
Full viewport height (h-screen), flex column layout with overflowX: clip.

Navbar: Horizontal nav bar with 4 links -- "About", "Price", "Projects", "Contact" -- evenly spaced with justify-between. Text color #D7E2EA, font-medium, uppercase, tracking-wider. Sizes: text-sm md:text-lg lg:text-[1.4rem]. Padding: px-6 md:px-10 pt-6 md:pt-8. Hover: opacity 70% with 200ms transition.

Hero Heading: Massive h1 with text "Hi, i'm jack" (lowercase "i", curly apostrophe via &apos;). Uses the .hero-heading gradient text class. Font-black, uppercase, tracking-tight, leading-none, whitespace-nowrap, w-full. Font sizes: text-[14vw] sm:text-[15vw] md:text-[16vw] lg:text-[17.5vw]. Margin top: mt-6 sm:mt-4 md:-mt-5. Wrapped in overflow-hidden container.

Bottom bar: Flexbox justify-between items-end with pb-7 sm:pb-8 md:pb-10:

Left: paragraph text "a 3d creator driven by crafting striking and unforgettable projects", color #D7E2EA, font-light, uppercase, tracking-wide, leading-snug. Font size: clamp(0.75rem, 1.4vw, 1.5rem). Max-width: max-w-[160px] sm:max-w-[220px] md:max-w-[260px].
Right: ContactButton component (see below)
Hero Portrait: Centered absolutely. Uses a Magnet component (mouse-following magnetic effect) wrapping an image. Image URL: https://shrug-person-78902957.figma.site/_components/v2/d24c01ad3a56fc65e942a1f501eb73db42d7cf9a/Rectangle_40443.81459862.png. Magnet settings: padding 150, strength 3, activeTransition "transform 0.3s ease-out", inactiveTransition "transform 0.6s ease-in-out". Positioning: absolute left-1/2 -translate-x-1/2 z-10. Width: w-[280px] sm:w-[360px] md:w-[440px] lg:w-[520px]. On mobile: top-1/2 -translate-y-1/2. On sm+: sm:top-auto sm:translate-y-0 sm:bottom-0.

FadeIn animations: Navbar fades in with delay 0, y -20. Heading: delay 0.15, y 40. Left text: delay 0.35, y 20. Contact button: delay 0.5, y 20. Portrait: delay 0.6, y 30.

2. MARQUEE SECTION
Two rows of images that scroll horizontally based on page scroll position. Background #0C0C0C. Padding: pt-24 sm:pt-32 md:pt-40 pb-10.

21 GIF images from motionsites.ai (exact URLs):


https://motionsites.ai/assets/hero-space-voyage-preview-eECLH3Yc.gif
https://motionsites.ai/assets/hero-codenest-preview-Cgppc2qV.gif
https://motionsites.ai/assets/hero-vex-ventures-preview-BczMFIiw.gif
https://motionsites.ai/assets/hero-stellar-ai-v2-preview-DjvxjG3C.gif
https://motionsites.ai/assets/hero-asme-preview-B_nGDnTP.gif
https://motionsites.ai/assets/hero-transform-data-preview-Cx5OU29N.gif
https://motionsites.ai/assets/hero-vitara-preview-Cjz2QYyU.gif
https://motionsites.ai/assets/hero-terra-preview-BFjrCr7T.gif
https://motionsites.ai/assets/hero-skyelite-preview-DHaZIgUv.gif
https://motionsites.ai/assets/hero-aethera-preview-DknSlcTa.gif
https://motionsites.ai/assets/hero-designpro-preview-D8c5_een.gif
https://motionsites.ai/assets/hero-stellar-ai-preview-D3HL6bw1.gif
https://motionsites.ai/assets/hero-xportfolio-preview-D4A8maiC.gif
https://motionsites.ai/assets/hero-orbit-web3-preview-BXt4OttD.gif
https://motionsites.ai/assets/hero-nexora-preview-cx5HmUgo.gif
https://motionsites.ai/assets/hero-evr-ventures-preview-DZxeVFEX.gif
https://motionsites.ai/assets/hero-planet-orbit-preview-DWAP8Z1P.gif
https://motionsites.ai/assets/hero-new-era-preview-CocuDUm9.gif
https://motionsites.ai/assets/hero-wealth-preview-B70idl_u.gif
https://motionsites.ai/assets/hero-luminex-preview-CxOP7ce6.gif
https://motionsites.ai/assets/hero-celestia-preview-0yO3jXO8.gif
Row 1: first 11 images, tripled for seamless scrolling. Moves RIGHT on scroll (translateX(offset - 200)).
Row 2: remaining 10 images, tripled. Moves LEFT on scroll (translateX(-(offset - 200))).
Scroll offset calculated as: (window.scrollY - sectionTop + window.innerHeight) * 0.3
Each image tile: 420px x 270px, rounded-2xl, object-cover, lazy loaded.
Gap between tiles: gap-3. Gap between rows: gap-3.
Uses willChange: 'transform' for performance. Scroll listener is passive.
3. ABOUT SECTION
Full-height centered section with min-h-screen, padding px-5 sm:px-8 md:px-10 py-20.

Four decorative 3D images positioned absolutely in corners:

Top-left: Moon icon -- https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/moon_icon.11395d36.png -- w-[120px] sm:w-[160px] md:w-[210px], positioned top-[4%] left-[1%] sm:left-[2%] md:left-[4%]. FadeIn: delay 0.1, x -80, y 0, duration 0.9.
Bottom-left: 3D object -- https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/p59_1.4659672e.png -- w-[100px] sm:w-[140px] md:w-[180px], positioned bottom-[8%] left-[3%] sm:left-[6%] md:left-[10%]. FadeIn: delay 0.25, x -80, y 0, duration 0.9.
Top-right: Lego icon -- https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/lego_icon-1.703bb594.png -- w-[120px] sm:w-[160px] md:w-[210px], positioned top-[4%] right-[1%] sm:right-[2%] md:right-[4%]. FadeIn: delay 0.15, x 80, y 0, duration 0.9.
Bottom-right: 3D group -- https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/Group_134-1.2e04f3ce.png -- w-[130px] sm:w-[170px] md:w-[220px], positioned bottom-[8%] right-[3%] sm:right-[6%] md:right-[10%]. FadeIn: delay 0.3, x 80, y 0, duration 0.9.
Heading: "About me" using .hero-heading gradient text, font-black, uppercase, leading-none, tracking-tight, centered. Font size: clamp(3rem, 12vw, 160px). FadeIn: delay 0, y 40.

Animated paragraph: Uses a character-by-character scroll-driven opacity animation. Text: "With more than five years of experience in design, i focus on branding, web design, and user experience, i truly enjoy working with businesses that aim to stand out and present their best image. Let's build something incredible together!" -- color #D7E2EA, font-medium, centered, leading-relaxed, max-w-[560px], font size clamp(1rem, 2vw, 1.35rem). Each character animates from opacity 0.2 to 1 based on scroll progress, with scroll offset ['start 0.8', 'end 0.2'].

Contact button below the text block. Gap between heading/text: gap-10 sm:gap-14 md:gap-16. Gap between text block and button: gap-16 sm:gap-20 md:gap-24.

4. SERVICES SECTION
White background (#FFFFFF), with rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px] top corners. Padding: px-5 sm:px-8 md:px-10 py-20 sm:py-24 md:py-32.

Heading: "Services" in #0C0C0C, font-black, uppercase, centered, font size clamp(3rem, 12vw, 160px). Margin bottom: mb-16 sm:mb-20 md:mb-28.

5 service items in a vertical list, max-w-5xl, centered:

01 - 3D Modeling: "Creation of detailed objects, characters, or environments tailored to specific client needs, ideal for games, products, and visualizations."
02 - Rendering: "High-quality, photorealistic renders that showcase designs with custom lighting, textures, and materials to bring concepts to life."
03 - Motion Design: "Dynamic animations and motion graphics that add energy and storytelling to brands, products, and digital experiences."
04 - Branding: "Crafting cohesive visual identities -- from logos to full brand systems -- that communicate a clear and memorable presence."
05 - Web Design: "Designing clean, modern, and conversion-focused websites with attention to layout, typography, and user experience."
Each item: horizontal layout with number (font-black, font size clamp(3rem, 10vw, 140px), color #0C0C0C) on the left and name + description stacked vertically on the right. Name: font-medium, uppercase, font size clamp(1rem, 2.2vw, 2.1rem). Description: font-light, leading-relaxed, max-w-2xl, font size clamp(0.85rem, 1.6vw, 1.25rem), opacity 0.6. Items separated by 1px borders (rgba(12, 12, 12, 0.15)). Padding: py-8 sm:py-10 md:py-12. Staggered FadeIn: each item delays by i * 0.1.

5. PROJECTS SECTION
Dark background (#0C0C0C), rounded top corners rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px], pulled up with -mt-10 sm:-mt-12 md:-mt-14, z-10.

Heading: "Project" (singular) using .hero-heading gradient, same styling as other headings.

3 sticky-stacking project cards that scale down as you scroll past them (card stacking effect using Framer Motion useScroll and useTransform). Each card is sticky top-24 md:top-32 inside an h-[85vh] container.

Scale calculation: targetScale = 1 - (totalCards - 1 - index) * 0.03. Each card offset by top: ${index * 28}px.

Each card has: rounded-[40px] sm:rounded-[50px] md:rounded-[60px], border-2 border-[#D7E2EA], background #0C0C0C, padding p-4 sm:p-6 md:p-8.

Card layout:

Top row: Number (huge, same style as services), category label, project name, and a "Live Project" ghost button (rounded-full, border-2 #D7E2EA, uppercase, tracking-widest).
Bottom row: Two-column image grid -- left column (40% width) has 2 stacked images, right column (60%) has 1 tall image. All images have heavy border radius rounded-[40px] sm:rounded-[50px] md:rounded-[60px]. Left top image height: clamp(130px, 16vw, 230px). Left bottom image height: clamp(160px, 22vw, 340px).
Project data with CloudFront image URLs:

Project 01 - "Nextlevel Studio" (Client):

Col1 image 1: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055344_5eff02e0-87a5-41ce-b64f-eb08da8f33db.png&w=1280&q=85
Col1 image 2: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055431_11d841fd-8b41-46a5-82e4-b04f2407a7d8.png&w=1280&q=85
Col2 image: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055451_e317bf2d-28d4-48cc-86b0-6f72f25b6327.png&w=1280&q=85
Project 02 - "Aura Brand Identity" (Personal):

Col1 image 1: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055654_911201c5-36d9-4bc6-bac7-331adfce159f.png&w=1280&q=85
Col1 image 2: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055723_5ceda0b8-d9c2-4665-b2e3-83ba19ba76d1.png&w=1280&q=85
Col2 image: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055753_adc5dcbd-a8e6-49c0-b43a-9b030d835cea.png&w=1280&q=85
Project 03 - "Solaris Digital" (Client):

Col1 image 1: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055759_963cfb0b-4bd1-4b0f-9d0a-09bd6cf95b2f.png&w=1280&q=85
Col1 image 2: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_060108_438f781a-9846-4dcc-89ab-c4e6cb830f5b.png&w=1280&q=85
Col2 image: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260412_055818_9d062121-ad7e-46b9-999a-1a6a692ef1ee.png&w=1280&q=85
REUSABLE COMPONENTS
ContactButton: Rounded-full pill button with gradient background linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%), inner box-shadow 0px 4px 4px rgba(181, 1, 167, 0.25), 4px 4px 12px #7721B1 inset, white 2px outline with -3px offset. Text: white, font-medium, uppercase, tracking-widest. Sizes: px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4, text text-xs sm:text-sm md:text-base. Label: "Contact Me".

LiveProjectButton: Ghost/outline pill button. Rounded-full, border-2 border-[#D7E2EA], text color #D7E2EA, font-medium, uppercase, tracking-widest. Sizes: px-8 py-3 sm:px-10 sm:py-3.5, text text-sm sm:text-base. Hover: bg-[#D7E2EA]/10. Label: "Live Project".

FadeIn: Framer Motion wrapper using whileInView with viewport={{ once: true, margin: "50px", amount: 0 }}. Accepts delay, duration (default 0.7), x (default 0), y (default 30). Easing: [0.25, 0.1, 0.25, 1]. Uses motion.create() for dynamic element types.

Magnet: Mouse-following magnetic hover effect. Tracks mouse position relative to element center, applies translate3d transform divided by strength factor. Activates when cursor is within padding distance of element edge. Smooth transition in (0.3s ease-out) and out (0.6s ease-in-out). Uses willChange: 'transform'.

AnimatedText: Character-by-character scroll-reveal text animation. Each character goes from opacity 0.2 to 1 based on its position in the text relative to scroll progress. Uses Framer Motion useScroll targeting the paragraph element with offset ['start 0.8', 'end 0.2']. Each character uses invisible placeholder + absolute positioned animated span.

KEY DEPENDENCIES
react, react-dom (^18.3.1)
framer-motion (^12.38.0)
lucide-react (^0.344.0)
tailwindcss (^3.4.1)
vite, typescript
RESPONSIVE BREAKPOINTS
All sections use Tailwind's default breakpoints (sm: 640px, md: 768px, lg: 1024px) with mobile-first approach. Heavy use of clamp() for fluid typography. The entire design scales gracefully from mobile to ultra-wide screens.
```

---

## 5. Velorah

- **Category**: Agency
- **Type**: hero
- **Page Type**: hero
- **ID**: `velorah-hero`

```
Create a single-page hero section with a fullscreen looping background video, glassmorphic navigation, and cinematic typography. Use React + Vite + Tailwind CSS + TypeScript with shadcn/ui.

Video Background:

Fullscreen <video> element with autoPlay, loop, muted, playsInline
Source URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4
Positioned absolute inset-0 w-full h-full object-cover z-0

Fonts:

Import from Google Fonts: Instrumental Serif (display) and Inter weights 400/500 (body)
CSS variables: --font-display: 'Instrument Serif', serif and --font-body: 'Inter', sans-serif
Body uses var(--font-body), headings use inline fontFamily: "'Instrument Serif', serif"

Color Theme (dark, HSL values for CSS variables):

--background: 201 100% 13% (deep navy blue)
--foreground: 0 0% 100% (white)
--muted-foreground: 240 4% 66% (muted gray)
--primary: 0 0% 100%, --primary-foreground: 0 0% 4%
--secondary: 0 0% 10%, --muted: 0 0% 10%, --accent: 0 0% 10%
--border: 0 0% 18%, --input: 0 0% 18%

Navigation Bar:

relative z-10, flex row, justify-between, px-8 py-6, max-w-7xl mx-auto
Logo: "Velorah®" (® as <sup className="text-xs">), text-3xl tracking-tight, Instrument Serif font, text-foreground
Nav links (hidden on mobile, md:flex): Home (active, text-foreground), Studio, About, Journal, Reach Us — all text-sm text-muted-foreground with hover:text-foreground transition-colors
CTA button: "Begin Journey", liquid-glass rounded-full px-6 py-2.5 text-sm text-foreground, hover:scale-[1.03]

Hero Section:

relative z-10, flex column, centered, text-center, px-6 pt-32 pb-40 py-[90px]
H1: "Where dreams rise through the silence." — text-5xl sm:text-7xl md:text-8xl, leading-[0.95], tracking-[-2.46px], max-w-7xl, font-normal, Instrument Serif. The words "dreams" and "through the silence." wrapped in <em className="not-italic text-muted-foreground"> for color contrast
Subtext: text-muted-foreground text-base sm:text-lg max-w-2xl mt-8 leading-relaxed — "We're designing tools for deep thinkers, bold creators, and quiet rebels. Amid the chaos, we build digital spaces for sharp focus and inspired work."
CTA button: "Begin Journey", liquid-glass rounded-full px-14 py-5 text-base text-foreground mt-12, hover:scale-[1.03] cursor-pointer

Liquid Glass Effect (CSS class .liquid-glass):

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

Animations (CSS keyframes + classes):

@keyframes fade-rise {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }

H1 gets animate-fade-rise
Subtext gets animate-fade-rise-delay
Hero CTA button gets animate-fade-rise-delay-2

Layout: No decorative blobs, radial gradients, or overlays. Minimalist, cinematic, vertically centered hero. The video provides all visual depth.
```

---

## 6. Aetheris Voyage

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `aetheris-voyage-hero`

```
Build Prompt: Cinematic Space-Travel Landing Page
Build a single-page landing site with two full-height sections (Hero + Capabilities), both using looping background videos with custom JS crossfade, a shared liquid-glass design system, and Framer Motion entrance animations.

Tech stack (pinned, CDN-only)
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
<script src="https://unpkg.com/framer-motion@11.11.17/dist/framer-motion.js"></script>
<script>window.Motion = window.FramerMotion;</script>
Body is bg: #000. Page is a React app mounted on #root, all components are <script type="text/babel"> files exporting via window.X = X.

Fonts
Google Fonts:

family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600
Tailwind config adds:

font-heading → 'Instrument Serif', serif (always italic in use)
font-body → 'Barlow', sans-serif
Default border radius override: DEFAULT: "9999px" (so bare rounded → pill).

Liquid-glass utilities (exact CSS, in a <style> block)
Two variants — .liquid-glass (subtle, for nav/chips/cards) and .liquid-glass-strong (heavier blur, for primary CTA):

.liquid-glass {
background: rgba(255,255,255,0.01);
background-blend-mode: luminosity;
backdrop-filter: blur(4px);
-webkit-backdrop-filter: blur(4px);
border: none;
box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
position: relative;
overflow: hidden;
}
.liquid-glass::before {
content: "";
position: absolute; inset: 0;
border-radius: inherit;
padding: 1.4px;
background: linear-gradient(180deg,
rgba(255,255,255,0.45) 0%,
rgba(255,255,255,0.15) 20%,
rgba(255,255,255,0) 40%,
rgba(255,255,255,0) 60%,
rgba(255,255,255,0.15) 80%,
rgba(255,255,255,0.45) 100%);
-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
-webkit-mask-composite: xor;
mask-composite: exclude;
pointer-events: none;
}
.liquid-glass-strong { /* same but: */
backdrop-filter: blur(50px);
box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);
}
.liquid-glass-strong::before { /* same but 0.5 / 0.2 / 0 / 0 / 0.2 / 0.5 stops */ }
FadingVideo component (custom JS crossfade, no CSS transitions)
Wraps a <video autoPlay muted playsInline preload="auto"> starting at opacity: 0. Behavior:

FADE_MS = 500, FADE_OUT_LEAD = 0.55 seconds.
fadeTo(target, duration) uses requestAnimationFrame; reads current opacity from http://video.style.opacity so each new fade resumes from wherever the last one left off. Each call calls cancelAnimationFrame on the previous rAF id before starting.
On loadeddata: set opacity 0, play(), fadeTo(1).
On timeupdate: if fadingOutRef not set and duration - currentTime <= 0.55 and > 0, flip the ref and fadeTo(0).
On ended: set opacity 0; after setTimeout(100ms) reset currentTime = 0, play(), clear fadingOutRef, fadeTo(1).
loop attribute is OFF (we implement looping manually via ended).
Cleanup on unmount: cancel rAF, remove listeners.
Section 1 — Hero (full viewport, black bg)
Background video (120% width/height, top-aligned, centered horizontally — focal point is the top of frame):

src: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_080021_d598092b-c4c2-4e53-8e46-94cf9064cd50.mp4
class: absolute left-1/2 top-0 -translate-x-1/2 object-cover object-top z-0
style: { width: "120%", height: "120%" }
No overlay. z-10 layer holds: Navbar → Hero content (flex-1, centered) → Partners.

Navbar (fixed top-4, px-8 / lg:px-16, z-50)
Left: 48×48 liquid-glass circle with italic serif lowercase "a" (Instrument Serif).
Center (desktop only): liquid-glass pill, px-1.5 py-1.5, holding 5 text links — Home, Voyages, Worlds, Innovation, Plan Launch — each px-3 py-2 text-sm font-medium text-white/90 font-body. Followed by a white pill button Claim a Spot + ArrowUpRight icon (bg-white text-black, whitespace-nowrap).
Right: 48×48 invisible spacer to balance logo.
Hero content (centered, pt-24 px-4)
All animated with Framer Motion, initial: {filter: blur(10px), opacity: 0, y: 20}, easeOut.

Badge (delay 0.4s): liquid-glass rounded-full pill. Contains white pill chip "New" (bg-white text-black px-3 py-1 text-xs font-semibold) + text "Maiden Crewed Voyage to Mars Arrives 2026" (text-sm text-white/90, pr-3).
Headline — BlurText component (word-by-word animation, see below). Text: "Venture Past Our Sky Across the Universe". Classes: text-6xl md:text-7xl lg:text-[5.5rem] font-heading italic text-white leading-[0.8] max-w-2xl justify-center tracking-[-4px].
Subheading (delay 0.8s, mt-4 text-sm md:text-base text-white max-w-2xl font-body font-light leading-tight): "Discover the universe in ways once unimaginable. Our pioneering vessels and breakthrough engineering bring deep-space exploration within reach—secure and extraordinary."
CTAs (delay 1.1s, flex items-center gap-6 mt-6):
Primary: liquid-glass-strong rounded-full px-5 py-2.5 text-sm font-medium text-white with "Start Your Voyage" + ArrowUpRight (h-5 w-5).
Secondary: bare text link, "View Liftoff" + Play icon (h-4 w-4, filled).
Stats row (delay 1.3s, flex items-stretch gap-4 mt-8): two liquid-glass cards, p-5 w-[220px] rounded-[1.25rem], each:
Top: white 28×28 outline SVG icon (clock for card 1, globe for card 2).
Bottom: large number in Instrument Serif italic white (text-4xl tracking-[-1px] leading-none): "34.5 Min" / "2.8B+". Label below (text-xs text-white font-body font-light mt-2): "Average Videos Watch Time" / "Users Across the Globe".
Partners (bottom of hero, delay 1.4s)
flex flex-col items-center gap-4 pb-8:

liquid-glass rounded-full chip (px-3.5 py-1 text-xs font-medium text-white): "Collaborating with top aerospace pioneers globally".
Row of 5 names in Instrument Serif italic white, text-2xl md:text-3xl tracking-tight, gap-12/md:gap-16: Aeon · Vela · Apex · Orbit · Zeno.
BlurText component (word-by-word blur-in)
IntersectionObserver triggers on 10% visibility. Splits text by spaces. Each word is a motion.span with:

initial: {filter: 'blur(10px)', opacity: 0, y: 50}
3-step keyframes to {filter: 'blur(5px)', opacity: 0.5, y: -5} → {filter: 'blur(0px)', opacity: 1, y: 0}
duration: 0.7 (stepDuration 0.35 × 2), times: [0, 0.5, 1], ease: easeOut
Stagger: delay = (i * 100) / 1000 seconds
display: inline-block, marginRight: 0.28em (not non-breaking-space — letter-spacing -4px eats nbsp).
Parent <p> is display: flex; flexWrap: wrap; justifyContent: center; rowGap: 0.1em.
Section 2 — Capabilities (min-h-screen, black bg)
Background video (full-bleed, no 120% scale):

src: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4
class: absolute inset-0 w-full h-full object-cover z-0
Same FadingVideo treatment. No overlay.

Content (relative z-10 px-8 md:px-16 lg:px-20 pt-24 pb-10 flex flex-col min-h-screen):

Header (mb-auto):

Kicker: text-sm font-body text-white/80 mb-6 → // Capabilities
Heading: font-heading italic text-white text-6xl md:text-7xl lg:text-[6rem] leading-[0.9] tracking-[-3px]:
Production
evolved
(two lines, <br/> between).
Three cards (grid grid-cols-1 md:grid-cols-3 gap-6 mt-16): each is liquid-glass rounded-[1.25rem] p-6 min-h-[360px] flex flex-col.

Top row of each card (flex items-start justify-between gap-4):

Left: 44×44 nested liquid-glass square (rounded-[0.75rem]) with a white Material Icons SVG (fill currentColor, h-6 w-6 text-white). Use random Material icons — these three used:
AI Scenery: image icon — path M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21H5Zm1-4h12l-3.75-5-3 4L9 13l-3 4Z
Batch Production: movie icon — path M4 6.47 5.76 10H20v8H4V6.47M22 4h-4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.89-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4Z
Smart Lighting: lightbulb icon — path M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1Zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7Z
Right: flex flex-wrap justify-end gap-1.5 max-w-[70%] — 4 small liquid-glass pill tags (rounded-full px-3 py-1 text-[11px] text-white/90 font-body whitespace-nowrap):
Card 1: Natural Context · Photo Realism · Infinite Settings · Eco-Vibe
Card 2: Scale Fast · Visual Consistency · Time Saver · Ready to Post
Card 3: Ray Tracing · Physical Shadows · Studio Quality · Sunlight Sync
Middle: flex-1 spacer.

Bottom of each card (mt-6):

Title h3: font-heading italic text-white text-3xl md:text-4xl tracking-[-1px] leading-none — "AI Scenery" / "Batch Production" / "Smart Lighting"
Body p (mt-3 text-sm text-white/90 font-body font-light leading-snug max-w-[32ch]):
"AI analyzes your product to create indistinguishable natural environments — from Icelandic cliffs to misty forests."
"Style your entire product line in minutes. Create a unified visual identity for catalogues and social media without weeks of retouching."
"Automatic lighting and material adjustment. Achieve flawless integration with realistic shadows and sunlight."
Icons (inline lucide-style SVGs, currentColor stroke)
ArrowUpRight: 24×24, M7 17L17 7 + M7 7h10v10, strokeWidth 2, round caps.
Play: 24×24 filled polygon 6 4 20 12 6 20 6 4.
Notes
All text white; no green, no gradient backgrounds.
No CSS transitions on the videos — fades must be rAF-driven per the FadingVideo spec.
Videos are full-bleed with no dark overlay; contrast comes from the liquid-glass chrome.
Framer Motion dev warnings about list keys can be suppressed with a console.error filter wrapper — they're benign.
The detailed prompt above captures every element, style, animation, video URL, and font to recreate the landing page exactly.
```

---

## 7. VEX Ventures

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `vex-ventures-hero`

```
Recreate this hero section exactly. Here are the complete specifications:

Video Background:

Full-screen background video, absolutely positioned, covering the entire viewport (object-cover)
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260403_050628_c4e32401-fab4-4a27-b7a8-6e9291cd5959.mp4
Autoplay, loop, muted, playsInline
NO dark overlay, NO gradient overlay, NO semi-transparent layer on top of the video. The video plays raw with no dimming whatsoever.
Typography (CRITICAL - must be applied globally):

Import the Google Font Inter via a <link> tag in index.html:

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
Set the body font-family in CSS to: 'Inter', sans-serif
Apply -webkit-font-smoothing: antialiased and -moz-osx-font-smoothing: grayscale on the body
Also extend the Tailwind config to set fontFamily: { sans: ['Inter', 'sans-serif'] } so all Tailwind font-sans usage picks up Inter automatically
Navbar:

Wrapped in horizontal page padding: px-6 md:px-12 lg:px-16 with pt-6 top padding
The navbar bar itself uses the .liquid-glass class and has rounded-xl, px-4 py-2, flex layout with items-center justify-between
Left: Logo text "VEX" - text-2xl font-semibold tracking-tight
Center (hidden on mobile, visible md+): Links "Story", "Investing", "Building", "Advisory" - text-sm, gap-8, hover transitions to gray-300
Right: "Start a Chat" button - bg-white text-black px-6 py-2 rounded-lg text-sm font-medium, hover to gray-100
Hero Content (Bottom of viewport):

Container: same horizontal padding as navbar, flex column filling remaining height, content pushed to bottom with flex-1 flex flex-col justify-end, bottom padding pb-12 lg:pb-16
On large screens: 2-column grid (lg:grid lg:grid-cols-2 lg:items-end)
Left Column - Main content:

Heading: "Shaping tomorrow\nwith vision and action." (literal line break between "tomorrow" and "with")

Responsive sizes: text-4xl md:text-5xl lg:text-6xl xl:text-7xl
font-normal, mb-4
Inline style: letterSpacing: '-0.04em'
Character-by-character entrance animation: Each character starts at opacity: 0 and translateX(-18px), then transitions to opacity: 1 and translateX(0). Each character gets a staggered delay calculated as: (lineIndex * lineLength * charDelay) + (charIndex * charDelay) where charDelay = 30ms. The whole animation starts after 200ms initial delay. Each character transition is 500ms.
Spaces render as \u00A0 (non-breaking space)
Subheading: "We back visionaries and craft ventures that define what comes next."

text-base md:text-lg text-gray-300 mb-5
Fade-in animation: starts at 800ms delay, 1000ms duration
Buttons row: flex-wrap with gap-4

"Start a Chat" - bg-white text-black px-8 py-3 rounded-lg font-medium
"Explore Now" - liquid-glass border border-white/20 text-white px-8 py-3 rounded-lg font-medium, hover transitions to white bg + black text
Fade-in animation: starts at 1200ms delay, 1000ms duration
Right Column - Tag:

Aligned to bottom-right on large screens (flex items-end justify-start lg:justify-end)
Glass card: liquid-glass border border-white/20 px-6 py-3 rounded-xl
Text: "Investing. Building. Advisory." - text-lg md:text-xl lg:text-2xl font-light
Fade-in animation: starts at 1400ms delay, 1000ms duration
Liquid Glass CSS (place in global CSS):


.liquid-glass {
  background: rgba(0, 0, 0, 0.4);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.1) 80%, rgba(255,255,255,0.3) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
FadeIn component: A wrapper that starts with opacity: 0 and transitions to opacity: 1 after a configurable delay (ms) using a setTimeout + React state. Transition duration is also configurable. Uses inline transitionDuration style and Tailwind's transition-opacity class.

AnimatedHeading component: Splits text by \n into lines, then each line into individual characters. Each character is an inline-block <span> with CSS transitions on opacity and transform (translateX). Animation triggers via React state after the initial delay.

Color scheme: Black background, white text, gray-300 for secondary text, white/20 for borders. No purple, no indigo.

Stack: React + TypeScript, Tailwind CSS, Vite. No extra UI libraries needed. Icons from lucide-react if needed (none currently used in the hero).
```

---

## 8. SkyElite Private Jets

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `skyelite-hero`

```
Create a premium private jet landing page hero section with the following specifications:

Video Background:
Use this exact CloudFront video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_091828_e240eb17-6edc-4129-ad9d-98678e3fd238.mp4
Video should autoplay, be muted, loop continuously, and include playsInline attribute
Video covers entire viewport (100vh) using object-cover

Navigation Bar:
Brand name "SkyElite" on the left (text-2xl, font-semibold, text-gray-900)
Desktop menu items (hidden on mobile, visible md:flex): Start, Story, Rates, Benefits, FAQ
Navigation links in gray-900 with hover:text-gray-700 transition
Mobile hamburger menu button using Lucide React icons (Menu/X)
Mobile menu appears as dropdown with white/95 opacity background, backdrop blur, rounded corners, shadow
Max width 7xl, centered with px-8 py-6

Hero Content (centered, -mt-80 to pull up):
Small uppercase label: "PRIVATE JETS" (text-sm, font-semibold, gray-600, tracking-wider, mb-4)
Large two-line heading with overlapping effect:
Line 1: "Premium." (text-6xl md:text-7xl lg:text-8xl, font-normal, text-gray-500, leading-none, tracking-tighter)
Line 2: "Accessible." (same size, color: #202A36, negative margin-top: -12px for overlap)
Subtitle: "Your dedication deserves recognition." (text-lg md:text-xl, gray-600, mb-6, max-w-2xl)
Two call-to-action buttons (gap-4, centered):
"Discover" button: px-4 py-2, rounded-full, bg-gray-300, text-gray-800, font-medium, hover:bg-gray-400
"Book Now" button: px-4 py-2, rounded-full, white text, bg-color #202A36, hover color #1a2229 with smooth transitions

Typography:
Use Inter font (import from Google Fonts: 400, 500, 600, 700 weights)
Apply to entire body via CSS

Technical Setup:
React with TypeScript
Tailwind CSS for styling
Lucide React for icons
useState hook for mobile menu toggle
Full screen height container (h-screen)
Responsive breakpoints: mobile-first, md, lg
All transitions use transition-colors class

Layout Structure:
Outer container: min-h-screen, bg-gray-50
Hero section: relative, h-screen, overflow-hidden
Content wrapper: relative, h-full, flex flex-col
Main content area: flex-1, flex items-center justify-center

Make it clean, modern, and premium-looking with smooth interactions.
```

---

## 9. Modern Agency

- **Category**: Agency
- **Type**: hero
- **Page Type**: landing
- **ID**: `modern-agency`

```
Build a React + Vite + Tailwind CSS landing page for "Axion Studio" - a design agency site. Use the `shaders` package (npm: `shaders`) for the hero background, `lucide-react` for icons. The page has 3 sections. Match every detail exactly:

---

## SECTION 1: HERO (Full viewport height)

**Background:** Light gray `#EFEFEF` with a full-screen animated shader overlay (positioned absolute, inset-0, z-10, pointer-events-none). The shader stack uses components from `shaders/react`:
- `Swirl` - colorA: `#ffffff`, colorB: `#f0f0f0`, detail: 1.7
- `ChromaFlow` - baseColor: `#ffffff`, downColor/leftColor/rightColor/upColor: `#ff5f03`, momentum: 13, radius: 3.5
- `FlutedGlass` - aberration: 0.61, angle: 31, frequency: 8, highlight: 0.12, highlightSoftness: 0, lightAngle: -90, refraction: 4, shape: "rounded", softness: 1, speed: 0.15
- `FilmGrain` - strength: 0.05

**Navigation (z-20, relative):** A pill-shaped white navbar (`bg-white rounded-full`) with 5px padding, inside a max-w-[1440px] container with p-2 sm:p-3.

- LEFT: Dark circle logo (w-9 h-9 sm:w-10 sm:h-10, bg-gray-900, rounded-full) with white text "AX" (10px/11px, font-bold, tracking-tight). Next to it (hidden on mobile, shown md+): nav links "Projects", "Studio", "Journal", "Connect" - 14px, text-gray-900, hover:text-gray-500, transition-colors duration-300, gap-6.

- RIGHT (hidden on mobile, shown md+): 
  - Text "Taking on projects for Q1 2026" (13px, text-gray-600, hidden below lg)
  - Clock icon (lucide, size 14) + live London time "{HH:MM} in London" (13px, text-gray-600)
  - CTA button: bg-gray-900, text-white, 13px font-medium, rounded-full, pl-5 pr-2 py-2. Text "Book a strategy call" with a HOVER TEXT ROLL animation: the text is duplicated inside a flex-col container with overflow-hidden h-[20px], on group-hover it translates -50% vertically (duration-500, ease cubic-bezier(0.25,0.1,0.25,1)). Arrow icon in a white circle (w-6 h-6) that rotates -45deg on hover (same easing).

- MOBILE: A "Menu"/"Close" toggle button (md:hidden), bg-gray-900, rounded-full, with Menu/X icons from lucide-react.

**Mobile Menu Overlay:** Fixed inset-0, z-50. Black/60 backdrop. A white bottom sheet (rounded-2xl, mx-3 mb-3) that slides up (translate-y-full to translate-y-0, duration-500, ease cubic-bezier(0.32,0.72,0,1)). Contains: time badge, nav links (28px/32px font-medium), and a "Start a project" button with arrow.

**Hero Content (z-20):** Positioned at the bottom of the viewport using flexbox (flex-1 spacer above). Max-w-[1440px], px-5 sm:px-8 lg:px-12, pb-14 sm:pb-16 lg:pb-20.

- Small label: "Axion Studio" (13px/14px, text-gray-900, tracking-wide, mb-5 sm:mb-8)
- Headline h1: "We craft digital experiences / for brands ready to dominate / their category online." - clamp(1.75rem,7vw,4.2rem) on mobile, clamp(2.5rem,5vw,4.2rem) on sm+. font-medium, leading-[1.08], tracking-[-0.03em], text-gray-900. Line breaks hidden on mobile (uses `<br className="hidden sm:block" />` with `<span className="sm:hidden"> </span>` fallback spaces).
- CTA row (mt-8 sm:mt-12, flex-col sm:flex-row, gap-4 sm:gap-5):
  - Orange button: bg-[#F26522], hover:bg-[#e05a1a], text-white, 13px/14px, rounded-full, pl-5 sm:pl-6 pr-2 py-2. Same text-roll hover animation for "Start a project". White circle (w-7 h-7 sm:w-8 sm:h-8) with orange ArrowRight that rotates -45deg on hover.
  - Partner badge: White pill with subtle shadow (0_2px_8px_rgba(0,0,0,0.08)), hover shadow (0_4px_16px_rgba(0,0,0,0.12)), rounded-[4px]. Contains an inline SVG icon (the starburst/compass shape below, w-5 h-5 sm:w-6 sm:h-6, fill-current text-[#E8704E]), text "Certified Partner" (13px/14px font-medium), and a dark badge "Featured" (10px/11px, bg-gray-900, text-white, px-1.5 sm:px-2 py-0.5, rounded).

**SVG Icon for partner badge:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="m19.6 66.5 19.7-11 .3-1-.3-.5h-1l-3.3-.2-11.2-.3L14 53l-9.5-.5-2.4-.5L0 49l.2-1.5 2-1.3 2.9.2 6.3.5 9.5.6 6.9.4L38 49.1h1.6l.2-.7-.5-.4-.4-.4L29 41l-10.6-7-5.6-4.1-3-2-1.5-2-.6-4.2 2.7-3 3.7.3.9.2 3.7 2.9 8 6.1L37 36l1.5 1.2.6-.4.1-.3-.7-1.1L33 25l-6-10.4-2.7-4.3-.7-2.6c-.3-1-.4-2-.4-3l3-4.2L28 0l4.2.6L33.8 2l2.6 6 4.1 9.3L47 29.9l2 3.8 1 3.4.3 1h.7v-.5l.5-7.2 1-8.7 1-11.2.3-3.2 1.6-3.8 3-2L61 2.6l2 2.9-.3 1.8-1.1 7.7L59 27.1l-1.5 8.2h.9l1-1.1 4.1-5.4 6.9-8.6 3-3.5L77 13l2.3-1.8h4.3l3.1 4.7-1.4 4.9-4.4 5.6-3.7 4.7-5.3 7.1-3.2 5.7.3.4h.7l12-2.6 6.4-1.1 7.6-1.3 3.5 1.6.4 1.6-1.4 3.4-8.2 2-9.6 2-14.3 3.3-.2.1.2.3 6.4.6 2.8.2h6.8l12.6 1 3.3 2 1.9 2.7-.3 2-5.1 2.6-6.8-1.6-16-3.8-5.4-1.3h-.8v.4l4.6 4.5 8.3 7.5L89 80.1l.5 2.4-1.3 2-1.4-.2-9.2-7-3.6-3-8-6.8h-.5v.7l1.8 2.7 9.8 14.7.5 4.5-.7 1.4-2.6 1-2.7-.6-5.8-8-6-9-4.7-8.2-.5.4-2.9 30.2-1.3 1.5-3 1.2-2.5-2-1.4-3 1.4-6.2 1.6-8 1.3-6.4 1.2-7.9.7-2.6v-.2H49L43 72l-9 12.3-7.2 7.6-1.7.7-3-1.5.3-2.8L24 86l10-12.8 6-7.9 4-4.6-.1-.5h-.3L17.2 77.4l-4.7.6-2-2 .2-3 1-1 8-5.5Z"/></svg>
```

---

## SECTION 2: ABOUT (White background)

`bg-white`, pt-16 sm:pt-20 lg:pt-32, pb-12 sm:pb-16 lg:pb-24, overflow-hidden. Max-w-[1440px] container.

**Badge row:** px-5 sm:px-8 lg:px-12, flex items-center gap-3, mb-6 sm:mb-8.
- Numbered circle: w-6 h-6 sm:w-7 sm:h-7, rounded-full, bg-gray-900, text-white, 11px/12px font-semibold. Shows "1".
- Pill label: "Introducing Axion" - 12px/13px, font-medium, border border-gray-200, rounded-full, px-3 sm:px-4 py-1 sm:py-1.5.

**Heading h2:** "Strategy-led creatives, delivering / results in digital and beyond." - clamp(1.5rem,4vw,3.2rem), font-medium, leading-[1.12], tracking-[-0.02em], text-gray-900, mb-12 sm:mb-16 lg:mb-28.

**Content area (responsive):**

- MOBILE/TABLET (lg:hidden): Stacked - paragraph + button, then images.
  - Paragraph: "Through research, creative thinking and iteration we help growing brands realize their digital full potential." - 15px/17px, leading-[1.6], font-medium, text-gray-900.
  - Button: "About our studio" - orange (#F26522), same text-roll animation, white arrow circle rotates -45deg.
  - Two images: flex-col sm:flex-row, gap-4 sm:gap-5. First: sm:w-[45%] aspect-[438/346]. Second: sm:w-[55%] aspect-[900/600]. Both rounded-xl sm:rounded-2xl, object-cover.

- DESKTOP (hidden lg:grid): `grid-cols-[26%_1fr_48%] items-end gap-6 xl:gap-8`.
  - Left column (self-end): Small image, aspect-[438/346], rounded-2xl.
  - Center column (self-start, flex justify-end): Paragraph (16px/18px, leading-[1.65], whitespace-nowrap, with `<br/>` between lines) + orange button.
  - Right column (self-end): Large image, aspect-[3/2], rounded-2xl.

**Image URLs:**
- Small image: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090123_74be96d4-9c1b-40cf-932a-96f4f4babed3.png&w=1280&q=85`
- Large image: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090133_c157d30b-a99a-4477-bec1-a446149ec3f2.png&w=1280&q=85`

---

## SECTION 3: CASE STUDIES (Light gray background)

`bg-[#F5F5F5]`, pt-16 sm:pt-20 lg:pt-28, pb-16 sm:pb-20 lg:pb-28. Max-w-[1440px] container.

**Badge row:** Same pattern as Section 2, but number is "2", label is "Featured client work", border-gray-300.

**Heading h2:** "Our projects" - same clamp sizing as hero headline (clamp(1.75rem,7vw,4.2rem) / clamp(2.5rem,5vw,4.2rem)), font-medium, leading-[1.08], tracking-[-0.03em], mb-10 sm:mb-14 lg:mb-16.

**Cards Grid:** `grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6 lg:gap-7`, px-5 sm:px-8 lg:px-12.

**Card 1 (Narrativ):**
- Video container: aspect-[329/246], rounded-2xl, overflow-hidden, bg-[#1a1d2e], group, cursor-pointer.
- Video: `src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260516_122702_390f5305-8719-41d5-ae80-d23ab3796c28.mp4"`, autoPlay, muted, loop, playsInline, w-full h-full object-cover.
- Hover button (absolute bottom-4 left-4): A white circle (h-9 w-9) that expands to w-[148px] on group-hover (transition-all duration-300 ease-in-out). Contains "Learn more" text (13px, font-medium, opacity-0 to opacity-100 on hover with delay-100) and a link/chain SVG icon (14x14, -rotate-45 to rotate-0 on hover). The SVG is the lucide "link" icon drawn manually with two arc paths.
- Description: "Winner of Site of the Month 2025 - an interactive 3D showcase driving record engagement" - 13px/14px, text-gray-600, mt-4, leading-relaxed.
- Title: "Narrativ" - 14px/15px, font-semibold, text-gray-900, mt-1.

**Card 2 (Luminar):**
- Video container: aspect-square, rounded-2xl, overflow-hidden, bg-[#6b6b6b], group, cursor-pointer.
- Video: `src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260516_123323_f909c2b8-ff6c-4edf-882b-8ebcdbe389b5.mp4"`, autoPlay, muted, loop, playsInline, w-full h-full object-cover.
- Hover button (absolute bottom-4 left-4): A DARK circle (bg-gray-900, h-9 w-9) that expands to w-[168px] on group-hover. Contains "View case study" text (13px, font-medium, text-white) and a white ArrowRight icon (size 14) that transitions from -rotate-45 to rotate-0 on hover.
- Description: "Transforming a dated platform into a conversion-focused brand experience" - 13px/14px, text-gray-600, mt-4, leading-relaxed.
- Title: "Luminar" - 14px/15px, font-semibold, text-gray-900, mt-1.

---

## GLOBAL STYLES (index.css):

Standard Tailwind directives plus two utility classes (not actively used in current layout but defined):
- `.liquid-glass`: rgba(255,255,255,0.01) bg, backdrop-filter blur(4px), inset box-shadow, pseudo-element gradient border using mask-composite.
- `.liquid-glass-strong`: Same but blur(50px), no pseudo-element.

---

## TECHNICAL DETAILS:
- **Framework:** React 18 + TypeScript + Vite
- **Styling:** Tailwind CSS 3.4 (default config, no custom theme extensions)
- **Packages:** `shaders` (for Shader, ChromaFlow, FilmGrain, FlutedGlass, Swirl from `shaders/react`), `lucide-react` (ArrowRight, Clock, Menu, X)
- **Font:** System default (no custom font loaded)
- **All animations use:** `duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]` unless noted otherwise
- **Max content width:** 1440px, centered with mx-auto
- **Responsive breakpoints:** Default Tailwind (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)
- **Live clock:** Updates every second, shows London timezone in HH:MM format
```

---

## 10. Aethera Studio

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `aethera-hero`

```
Prompt: Cinematic Hero Section with Looping Video Background

Create a fullscreen single-page hero section using React + Vite + Tailwind CSS + TypeScript with the following specifications:

Fonts:
Display text (headings, logo): Instrument Serif
Body text (navigation, descriptions): Inter
Import both fonts in /src/styles/fonts.css

Video Background:
URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_083109_283f3553-e28f-428b-a723-d639c617eb2b.mp4
Position: top: '300px' with inset: 'auto 0 0 0'
Implement custom fade-in/fade-out loop logic using React useEffect and useRef:
Use requestAnimationFrame to continuously monitor currentTime and duration
Fade in over 0.5s at the start (opacity 0 to 1)
Fade out over 0.5s before the end (opacity 1 to 0)
On ended event: set opacity to 0, wait 100ms, reset currentTime = 0, then play() again
This creates a seamless manual loop with smooth fade transitions
Add gradient overlays: absolute inset-0 bg-gradient-to-b from-background via-transparent to-background positioned over the video

Navigation Bar:
Logo: "Aethera®" (with registered trademark symbol as superscript)
Logo styling: text-3xl, tracking-tight, Instrument Serif, color #000000
Menu items: Home (color #000000), Studio, About, Journal, Reach Us (all others #6F6F6F)
Menu items: text-sm with transition-colors
CTA button: "Begin Journey", rounded-full, px-6 py-2.5, text-sm, black background (#000000), white text, hover scale 1.03
Layout: flex justify-between, px-8 py-6, max-w-7xl mx-auto

Hero Section:
Positioning: paddingTop: 'calc(8rem - 75px)', pb-40
Layout: centered (flex flex-col items-center justify-center text-center), px-6
Headline:
Text: "Beyond silence, we build the eternal."
Styling: text-5xl sm:text-7xl md:text-8xl, max-w-7xl, font-normal
Font: Instrument Serif
Line height: 0.95
Letter spacing: -2.46px
Color: #000000 for main text, #6F6F6F for italic emphasized words ("silence," and "the eternal.")
Animation: animate-fade-rise

Description:
Text: "Building platforms for brilliant minds, fearless makers, and thoughtful souls. Through the noise, we craft digital havens for deep work and pure flows."
Styling: text-base sm:text-lg, max-w-2xl, mt-8, leading-relaxed
Color: #6F6F6F
Animation: animate-fade-rise-delay

Hero CTA Button:
Text: "Begin Journey"
Styling: rounded-full, px-14 py-5, text-base, mt-12
Colors: black background (#000000), white text (#FFFFFF)
Hover: scale 1.03
Animation: animate-fade-rise-delay-2

Colors:
Background: white (#FFFFFF)
Headlines/logos/buttons: black (#000000)
Descriptions/menu items: gray (#6F6F6F)
Button text: white (#FFFFFF)

Animations (in /src/styles/theme.css):
fade-rise: opacity 0 to 1, translateY 20px to 0, duration 0.8s, ease-out
fade-rise-delay: same as fade-rise but with 0.2s delay
fade-rise-delay-2: same as fade-rise but with 0.4s delay

Layout Structure:
Container: relative min-h-screen w-full overflow-hidden
Background video layer (z-0)
Gradient overlay on video
Navigation bar (z-10)
Hero section (z-10)
All elements should be responsive and maintain the glassmorphic aesthetic with the specified padding, positioning, and smooth animations.
```

---

## 11. Asme

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `asme-hero`

```
Build a single-page hero section with a full-screen looping background video, liquid glass UI elements, and a dark cinematic aesthetic. Use React, TypeScript, Tailwind CSS, and Lucide React icons. Here are the exact specifications:

Background Video:

Full-screen muted autoplaying video covering the entire viewport, positioned absolutely with object-cover
Video source URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_115001_bcdaa3b4-03de-47e7-ad63-ae3e392c32d4.mp4
The video is shifted down by 17% (translate-y-[17%]) so the top portion of the video is cropped -- the interesting content is in the lower portion of the frame
The video loops seamlessly with a custom JavaScript fade system (no CSS transitions): 500ms requestAnimationFrame-based fade-in on load/loop start, 500ms fade-out when 0.55 seconds remain before the video ends. A fadingOutRef boolean prevents re-triggering the fade-out from repeated timeUpdate events. On ended, opacity is set to 0, then after 100ms the video resets to currentTime = 0, plays, and fades back in. Each new fade cancels any running animation frame to prevent competing animations. Fades resume from the current opacity rather than snapping.
The outer container is min-h-screen bg-black with overflow-hidden

Font:

Import Google Font "Instrument Serif" (both regular and italic) via CSS @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap')
The heading uses fontFamily: "'Instrument Serif', serif" applied via inline style

Liquid Glass CSS (.liquid-glass class):

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity
backdrop-filter: blur(4px) and -webkit-backdrop-filter: blur(4px)
border: none
box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1)
position: relative; overflow: hidden
A ::before pseudo-element creates the glass border effect:
position: absolute; inset: 0; border-radius: inherit; padding: 1.4px
background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)
Mask trick for border-only rendering: -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); -webkit-mask-composite: xor; mask-composite: exclude
pointer-events: none

Layout (all inside one full-screen flex column):

Navigation bar (relative z-20, padding pl-6 pr-6 py-6):
Inner container: rounded-full px-6 py-3 flex items-center justify-between max-w-5xl mx-auto
Left side: Logo area with a Globe icon (size 24) and text "Asme" in white, font-semibold text-lg, with gap-2
Next to the logo (with gap-8): three nav links ("Features", "Pricing", "About") -- hidden on mobile, shown on md: -- styled text-white/80 hover:text-white transition-colors text-sm font-medium
Right side (gap-4): "Sign Up" as plain white text button, "Login" as a liquid-glass rounded-full px-6 py-2 button

Hero content area (relative z-10 flex-1 flex flex-col items-center justify-center px-6 py-12 text-center -translate-y-[20%]):
Heading: "Built for the curious" -- text-5xl md:text-6xl lg:text-7xl text-white mb-8 tracking-tight whitespace-nowrap with Instrument Serif font
Below the heading, a max-w-xl w-full space-y-4 container:
Email input bar: liquid-glass rounded-full pl-6 pr-2 py-2 flex items-center gap-3. Inside: a transparent email input (placeholder: "Enter your email", text-white placeholder:text-white/40 text-base) and a white circular submit button (bg-white rounded-full p-3 text-black) containing an ArrowRight icon (size 20)
Subtitle text: text-white text-sm leading-relaxed px-4 -- "Stay updated with the latest news and insights. Subscribe to our newsletter today and never miss out on exciting updates."
Manifesto button: centered, liquid-glass rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors

Social icons footer (relative z-10 flex justify-center gap-4 pb-12):
Three circular icon buttons, each liquid-glass rounded-full p-4 text-white/80 hover:text-white hover:bg-white/5 transition-all
Icons: Instagram, Twitter, Globe (all size 20) from lucide-react
Each has an aria-label

Tech stack: Vite + React 18 + TypeScript, Tailwind CSS 3, lucide-react for all icons. Default Tailwind config with no extensions. No other UI libraries.
```

---

## 12. Innovation

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: landing
- **ID**: `innovation-landing`

```
RECREATION PROMPT

Build a single-page landing site using React + TypeScript + Vite + Tailwind CSS + framer-motion + lucide-react. The entire page has a bg-black background. The font loaded via Google Fonts is Instrument Serif (italic and regular). Import it in index.css:


@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');
LIQUID GLASS CSS (in index.css, inside @layer components)
Create a reusable .liquid-glass class used on every glass element:


.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.45) 0%,
    rgba(255, 255, 255, 0.15) 20%,
    rgba(255, 255, 255, 0) 40%,
    rgba(255, 255, 255, 0) 60%,
    rgba(255, 255, 255, 0.15) 80%,
    rgba(255, 255, 255, 0.45) 100%
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
SECTION 1 -- HERO (full-viewport, in Index.tsx)
Full-screen (min-h-screen) container with overflow-hidden relative flex flex-col.

Background video: absolute, covers the entire viewport (absolute inset-0 w-full h-full object-cover object-bottom). URL:


https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_074625_a81f018a-956b-43fb-9aee-4d1508e30e6a.mp4
Attributes: muted, autoPlay, playsInline, preload="auto". Starts at opacity: 0.

Video fade logic (vanilla JS via refs, no CSS transitions):

On canplay: play the video, then animate opacity from 0 to 1 over 500ms using requestAnimationFrame.
On timeupdate: when remaining time <= 0.55s, animate opacity from current to 0 over 500ms.
On ended: set opacity to 0, wait 100ms, reset currentTime to 0, play again, fade back to 1 over 500ms.
This creates a seamless loop with smooth crossfade to black between plays.
Navbar (relative z-20, px-6 py-6):

A liquid-glass rounded-full pill, max-w-5xl mx-auto, px-6 py-3, flex between left/right.
Left: Globe icon (24px, white) + "Asme" text (white, font-semibold, text-lg). Hidden on mobile: nav links "Features", "Pricing", "About" (text-white/80 hover:text-white text-sm font-medium, gap-8 ml-8).
Right: "Sign Up" text button (white, text-sm, font-medium) + "Login" button (liquid-glass rounded-full px-6 py-2, white text-sm font-medium).
Hero content (relative z-10, flex-1 flex flex-col items-center justify-center, px-6 py-12 text-center, -translate-y-[20%]):

Heading: text-7xl md:text-8xl lg:text-9xl, white, tracking-tight whitespace-nowrap, font-family 'Instrument Serif', serif. Text: Know it then <em className="italic">all</em>.
Email input: max-w-xl w-full. A liquid-glass rounded-full pill with pl-6 pr-2 py-2 flex items-center gap-3. Inside: transparent <input> with placeholder "Enter your email" (text-white placeholder:text-white/40). A white circular submit button (bg-white rounded-full p-3 text-black) containing ArrowRight icon (20px).
Subtitle: text-white text-sm leading-relaxed px-4. Text: "Stay updated with the latest news and insights. Subscribe to our newsletter today and never miss out on exciting updates."
Manifesto button: liquid-glass rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors.
Social icons footer (relative z-10, flex justify-center gap-4 pb-12):

Three liquid-glass rounded-full p-4 buttons for Instagram, Twitter, Globe icons (20px). text-white/80 hover:text-white hover:bg-white/5 transition-all.
SECTION 2 -- ABOUT SECTION (separate component AboutSection.tsx)
Uses framer-motion useInView (ref, { once: true, margin: "-100px" }).
bg-black pt-32 md:pt-44 pb-10 md:pb-14 px-6 overflow-hidden.
Subtle radial gradient overlay: bg-[radial-gradient(ellipse_at_top,_rgba(255,255,255,0.03)_0%,_transparent_70%)].
Label: "About Us" -- text-white/40 text-sm tracking-widest uppercase. Animates: opacity: 0, y: 20 -> opacity: 1, y: 0, duration 0.6.
Heading: text-4xl md:text-6xl lg:text-7xl text-white leading-[1.1] tracking-tight. Animates: opacity: 0, y: 40 -> opacity: 1, y: 0, duration 0.8, delay 0.1. Text structure:
Pioneering then ideas (Instrument Serif italic, text-white/60) for
Line break (hidden on mobile)
minds that then create, build, and inspire. (all Instrument Serif italic, text-white/60)
SECTION 3 -- FEATURED VIDEO (separate component FeaturedVideoSection.tsx)
bg-black pt-6 md:pt-10 pb-20 md:pb-32 px-6 overflow-hidden. Max-w-6xl.
A rounded-3xl overflow-hidden aspect-video container that animates opacity: 0, y: 60 -> opacity: 1, y: 0, duration 0.9.
Video: w-full h-full object-cover, muted, autoPlay, loop, playsInline, preload="auto". URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260402_054547_9875cfc5-155a-4229-8ec8-b7ba7125cbf8.mp4
Gradient overlay on video: bg-gradient-to-t from-black/60 via-transparent to-transparent.
Bottom overlay content (absolute bottom-0 left-0 right-0 p-6 md:p-10):
Flex row on desktop, column on mobile.
Left: a liquid-glass rounded-2xl p-6 md:p-8 max-w-md card. Label "Our Approach" (text-white/50 text-xs tracking-widest uppercase mb-3). Body text (text-white text-sm md:text-base leading-relaxed): "We believe in the power of curiosity-driven exploration. Every project starts with a question, and every answer opens a new door to innovation."
Right: "Explore more" button (liquid-glass rounded-full px-8 py-3, white text-sm font-medium) with whileHover={{ scale: 1.05 }} and whileTap={{ scale: 0.95 }}.
SECTION 4 -- PHILOSOPHY / INNOVATION x VISION (separate component PhilosophySection.tsx)
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.
Heading: text-5xl md:text-7xl lg:text-8xl text-white tracking-tight mb-16 md:mb-24. Animates opacity: 0, y: 40 -> opacity: 1, y: 0, duration 0.8. Text: Innovation then x in Instrument Serif italic text-white/40, then Vision.
Two-column grid (grid-cols-1 md:grid-cols-2 gap-8 md:gap-12):
Left: Video in rounded-3xl overflow-hidden aspect-[4/3]. Animates from opacity: 0, x: -40. URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4
muted, autoPlay, loop, playsInline, preload="auto".
Right: Animates from opacity: 0, x: 40. Two text blocks separated by a w-full h-px bg-white/10 divider.
Block 1: Label "Choose your space" (text-white/40 text-xs tracking-widest uppercase mb-4). Body (text-white/70 text-base md:text-lg leading-relaxed): "Every meaningful breakthrough begins at the intersection of disciplined strategy and remarkable creative vision. We operate at that crossroads, turning bold thinking into tangible outcomes that move people and reshape industries."
Block 2: Label "Shape the future". Body: "We believe that the best work emerges when curiosity meets conviction. Our process is designed to uncover hidden opportunities and translate them into experiences that resonate long after the first impression."
SECTION 5 -- SERVICES / WHAT WE DO (separate component ServicesSection.tsx)
bg-black py-28 md:py-40 px-6 overflow-hidden. Max-w-6xl.
Subtle radial gradient: bg-[radial-gradient(ellipse_at_center,_rgba(255,255,255,0.02)_0%,_transparent_60%)].
Header row: flex between "What we do" (text-3xl md:text-5xl text-white tracking-tight) and "Our services" label (text-white/40 text-sm, hidden on mobile). Animates opacity: 0, y: 30 -> visible, duration 0.7.
Two-card grid (grid-cols-1 md:grid-cols-2 gap-6 md:gap-8):
Each card: liquid-glass rounded-3xl overflow-hidden with group class. Animates opacity: 0, y: 50 -> visible, duration 0.8, staggered by 0.15s.
Card video area: aspect-video, object-cover, transition-transform duration-700 group-hover:scale-105. Gradient overlay: bg-gradient-to-t from-black/40 to-transparent.
Card body (p-6 md:p-8): tag label (uppercase, tracking-widest, text-white/40 text-xs), ArrowUpRight icon in a liquid-glass rounded-full p-2 circle, title (text-white text-xl md:text-2xl mb-3 tracking-tight), description (text-white/50 text-sm leading-relaxed).
Card 1: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4
Tag: "Strategy". Title: "Research & Insight". Description: "We dig deep into data, culture, and human behavior to surface the insights that drive meaningful, lasting change."
Card 2: Video URL:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260324_151826_c7218672-6e92-402c-9e45-f1e0f454bdc4.mp4
Tag: "Craft". Title: "Design & Execution". Description: "From concept to launch, we obsess over every detail to deliver experiences that feel effortless and look extraordinary."

```

---

## 13. Orbis NFT

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: landing
- **ID**: `orbis-nft-landing`

```
Create an NFT landing page called "Orbis.Nft" with 4 sections, using a dark space theme. The page uses video backgrounds served from CloudFront, a liquid glass UI effect, and a specific color/font system. Recreate it exactly as described below.

FONTS (Google Fonts)

Anton - Used for all headings and navigation text (aliased as font-grotesk in Tailwind)

Condiment - A cursive script used for accent/overlay text (aliased as font-condiment in Tailwind)

System monospace font (font-mono) - Used for body/description paragraphs

Load via Google Fonts in index.html:

https://fonts.googleapis.com/css2?family=Anton&family=Condiment&display=swap


COLOR SYSTEM (Tailwind config)

Background: #010828 (deep dark navy blue)

cream: #EFF4FF (off-white, used for all text)

neon: #6FFF00 (bright green, used for accent cursive text and underline bars)

LIQUID GLASS CSS EFFECT

Applied via a .liquid-glass class. This is used on the navbar, social icon buttons, NFT cards, and card overlays:

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}


TEXTURE OVERLAY

A full-screen fixed texture overlay sits on top of everything (z-50, pointer-events-none). It uses a /texture.png image with mix-blend-mode: lighten at opacity: 0.6, covering the entire viewport with background-size: cover.

SECTION 1: HERO (Full viewport)

Background: Full-bleed looping muted autoplaying video covering the entire section with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_045634_e1c98c76-1265-4f5c-882a-4276f2080894.mp4

Container: max-w-[1831px] centered with responsive horizontal padding

Section has rounded-b-[32px] bottom corners, clipping the video

Header:

Left: "Orbis.Nft" logo text in Anton, 16px, uppercase

Center: Navigation bar with liquid-glass effect, rounded-[28px], px-[52px] py-[24px]. Contains 5 links: Homepage, Gallery, Buy NFT, FAQ, Contact. Each link is Anton 13px uppercase. Links have hover:text-neon transition. Nav is hidden on mobile (hidden lg:block).

Hero Content:

Large heading in Anton font, responsive sizing: 40px mobile / 60px sm / 75px md / 90px lg. Uppercase. leading-[1.05] mobile, leading-[1] tablet+. Max width 780px on desktop, offset with lg:ml-32.

Text reads:

Beyond earth
and ( its ) familiar boundaries


Overlaid cursive accent text "Nft collection" in Condiment font (24px-48px responsive), positioned absolute to the right side of the heading, slightly rotated (-rotate-1), in neon green (text-neon), with mix-blend-exclusion and opacity-90.

Social Icons (Desktop):

3 square buttons (56x56px) stacked vertically in top-right corner, each with liquid-glass and rounded-[1rem]. Icons: Mail, Twitter, Github from lucide-react (20x20px). hover:bg-white/10 transition.

Social Icons (Mobile):

Same 3 buttons but centered horizontally below the heading, shown only below lg breakpoint.

SECTION 2: ABOUT / INTRO (Full viewport)

Background: Full-bleed looping muted autoplaying video with object-cover

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_151551_992053d1-3d3e-4b8c-abac-45f22158f411.mp4

Container: Same max-w-[1831px] centered, with generous vertical padding (64px-96px responsive)

Top Row (flex row on desktop, column on mobile):

Left: Heading in Anton, responsive 32px-60px, uppercase:

Hello!
I'm orbis


With an overlaid "Orbis" in Condiment cursive, neon green, mix-blend-exclusion, 36px-68px responsive, positioned absolute at bottom-right of heading, slightly rotated.

Right: Short paragraph in monospace 14px-16px, uppercase, cream color, max-width 266px: "A digital object fixed beyond time and place. An exploration of distance, form, and silence in space"

Bottom Row (flex row, space-between):

Two columns (left and right), each containing 2 identical paragraphs. Same monospace text as above but at opacity-10 (nearly invisible, decorative). Right column hidden below lg. On mobile, text uses text-[#010828] (dark) so it's effectively invisible against the video.

SECTION 3: NFT COLLECTION GRID

Background: Solid #010828 (no video)

Container: Same max-w-[1831px] centered

Header Row:

Left: Heading in Anton, 32px-60px responsive, uppercase:

Collection of
  [indented] Space objects


Where "Space" is in Condiment cursive neon green, and "objects" is in Anton. The second line is indented with ml-12 / ml-24 / ml-32 responsive.

Right: A "SEE ALL CREATORS" button. "SEE" is large (32px-60px), "ALL" and "CREATORS" are stacked smaller (20px-36px) next to it. Below the text is a neon green bar (bg-neon, height 6px-10px responsive, full width of button).

NFT Card Grid:

3-column grid on desktop (lg:grid-cols-3), 2 on tablet, 1 on mobile. Gap 24px.

Each card: liquid-glass container with rounded-[32px], padding 18px, hover:bg-white/10 transition.

Inside each card: a square video container (pb-[100%] aspect ratio trick) with rounded-[24px] overflow hidden.

Video URLs:

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_053923_22c0a6a5-313c-474c-85ff-3b50d25e944a.mp4 (Score: 8.7/10)

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_054411_511c1b7a-fb2f-42ef-bf6c-32c0b1a06e79.mp4 (Score: 9/10)

https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_055427_ac7035b5-9f3b-4289-86fc-941b2432317d.mp4 (Score: 8.2/10)

Each card has an overlay bar at the bottom: a liquid-glass bar with rounded-[20px], px-5 py-4, showing "RARITY SCORE:" label (11px, cream/70% opacity) and score value (16px). On the right side of the bar is a circular purple gradient button (48x48px, bg-gradient-to-br from-[#b724ff] to-[#7c3aed]) with a right-arrow chevron SVG inside, with shadow-lg shadow-purple-500/50 and hover:scale-110 transition.

SECTION 4: CTA / FINAL SECTION

Background: Full-width video (NOT object-cover, instead w-full h-auto block so it displays at native aspect ratio)

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_055729_72d66327-b59e-4ae9-bb70-de6ccb5ecdb0.mp4

Text Content (positioned absolute over the video):

Right-aligned block, offset with lg:pr-[20%] lg:pl-[15%]

Small "Go beyond" text in Condiment cursive, neon green, mix-blend-exclusion, positioned absolute at top-left of the heading block. Sizes: 17px-68px responsive.

Heading in Anton, responsive 16px-60px, uppercase:

JOIN US.
REVEAL WHAT'S HIDDEN.
DEFINE WHAT'S NEXT.
FOLLOW THE SIGNAL.


"JOIN US." has extra bottom margin (mb-4 to mb-12 responsive) before the remaining lines.

Social Icons (Bottom-left, absolute positioned):

Positioned at left-[8%], bottom-[12%] to bottom-[20%] with responsive breakpoints.

A vertical liquid-glass container with rounded-[0.5rem] to rounded-[1.25rem] responsive, containing 3 stacked icon buttons (Mail, Twitter, Github).

Buttons have responsive widths using viewport units and rem values (e.g., w-[14vw] sm:w-[14.375rem] md:w-[10.78125rem] lg:w-[16.77rem]) and similar responsive heights.

Buttons are separated by border-b border-white/10 dividers (except the last one).

KEY TECHNICAL DETAILS

Framework: React + TypeScript + Vite + Tailwind CSS

Icons: lucide-react (Mail, Twitter, Github)

No additional packages needed beyond what Vite + React + Tailwind provides

All videos: autoPlay loop muted playsInline attributes

Responsive: Mobile-first with sm:, md:, lg: breakpoints throughout

Max content width: 1831px across all sections

All text is uppercase except the Condiment cursive accents which are normal-case
```

---

## 14. Portfolio Cosmic

- **Category**: Portfolio
- **Type**: hero
- **Page Type**: landing
- **ID**: `portfolio-cosmic-hero`

```
Prompt to recreate this landing page:

Build a single-page dark portfolio landing page using React + Vite + Tailwind CSS + TypeScript + GSAP + Framer Motion + hls.js.

---

## Global Design System

### Fonts
Google Fonts import: Inter (300–700) and Instrument Serif (italic, 400).
- --font-body: 'Inter', sans-serif → Tailwind font-body
- --font-display: 'Instrument Serif', serif → Tailwind font-display

### CSS Custom Properties (HSL, no hsl() wrapper — Tailwind adds it)
--bg: 0 0% 4%;
--surface: 0 0% 8%;
--text: 0 0% 96%;
--muted: 0 0% 53%;
--stroke: 0 0% 12%;
--accent: 0 0% 96%;

### Tailwind Custom Colors
bg: "hsl(var(--bg))",
surface: "hsl(var(--surface))",
"text-primary": "hsl(var(--text))",
muted: "hsl(var(--muted))",
stroke: "hsl(var(--stroke))",

### Accent Gradient
linear-gradient(90deg, #89AACC 0%, #4E85BF 100%) — used on logo ring, hover borders, progress bars. CSS utility class .accent-gradient.

### Custom Animations (in index.css)
- @keyframes scroll-down — translateY(-100%) → translateY(200%), 1.5s ease-in-out infinite
- @keyframes role-fade-in — opacity 0 + translateY(8px) → opacity 1 + translateY(0), 0.4s ease-out
- @keyframes gradient-shift — background-position 0% 50% → 100% 50% → 0% 50%, 6s ease infinite (for animated gradient borders)

### Forced dark theme — no light mode toggle. body gets bg-bg text-text-primary.

---

## Page Structure (Index.tsx)

{isLoading && <LoadingScreen onComplete={() => setIsLoading(false)} />}

---

## Section 1: Loading Screen

Full-screen overlay (fixed inset-0 z-[9999] bg-bg). Uses requestAnimationFrame counter from 000→100 over 2700ms.

- Top-left: "Portfolio" label — text-xs text-muted uppercase tracking-[0.3em]. Animates y:-20→0, opacity 0→1.
- Center: Rotating words ["Design", "Create", "Inspire"] cycling every 900ms. AnimatePresence mode="wait" with y:20→0→-20 transitions. text-4xl md:text-6xl lg:text-7xl font-display italic text-text-primary/80.
- Bottom-right: Counter display — text-6xl md:text-8xl lg:text-9xl font-display text-text-primary tabular-nums. Shows String(count).padStart(3, "0").
- Bottom progress bar: h-[3px] bg-stroke/50, inner div with .accent-gradient, scaleX(count/100) transform, box-shadow: 0 0 8px rgba(137, 170, 204, 0.35).
- On complete (count reaches 100): 400ms delay then calls onComplete.

---

## Section 2: Hero

Full-viewport section with background HLS video and centered content.

### Background Video
- HLS source: https://stream.mux.com/Aa02T7oM1wH5Mk5EEVDYhbZ1ChcdhRsS2m1NYyx4Ua1g.m3u8
- Uses hls.js — if Hls.isSupported(), create HLS instance; else if native HLS support, set video.src directly.
- Video: autoPlay muted loop playsInline, absolutely positioned and centered with min-w-full min-h-full object-cover -translate-x-1/2 -translate-y-1/2.
- Dark overlay: bg-black/20
- Bottom fade: h-48 bg-gradient-to-t from-bg to-transparent

### Navbar (fixed, floats at top center)
fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 md:pt-6 px-4.

Inner pill: inline-flex items-center rounded-full backdrop-blur-md border border-white/10 bg-surface px-2 py-2. Gets shadow-md shadow-black/10 when scrollY > 100.

Contents (left to right):
1. Logo: 9×9 circle with accent gradient border (reverses direction on hover). Inner bg-bg circle with "JA" in font-display italic text-[13px]. Scales 110% on hover.
2. Divider: w-px h-5 bg-stroke mx-1 (hidden on mobile)
3. Nav links: ["Home", "Work", "Resume"] — text-xs sm:text-sm rounded-full px-3 sm:px-4 py-1.5 sm:py-2. Active: text-text-primary bg-stroke/50. Inactive: text-muted hover:text-text-primary hover:bg-stroke/50.
4. Divider
5. "Say hi" button: Same size as nav links. On hover, shows accent gradient border behind (using absolute span with inset: -2px). Inner content wrapped in bg-surface rounded-full backdrop-blur-md. Includes "↗" arrow.

### Hero Content (centered, z-10)
- Eyebrow: text-xs text-muted uppercase tracking-[0.3em] mb-8 — "COLLECTION '26". Class blur-in.
- Name: text-6xl md:text-8xl lg:text-9xl font-display italic leading-[0.9] tracking-tight text-text-primary mb-6 — "Michael Smith". Class name-reveal.
- Role line: "A {role} lives in Chicago." — roles cycle every 2s through ["Creative", "Fullstack", "Founder", "Scholar"]. Role word uses font-display italic text-text-primary animate-role-fade-in inline-block with key={roleIndex} for re-triggering animation.
- Description: text-sm md:text-base text-muted max-w-md mb-12 — "Designing seamless digital interactions by focusing on the unique nuances which bring systems to life."
- CTA Buttons (inline-flex gap-4):
  - "See Works": Solid button. Default: bg-text-primary text-bg. Hover: bg-bg text-text-primary with accent gradient border ring.
  - "Reach out...": Outlined button. Default: border-2 border-stroke bg-bg text-text-primary. Hover: border-transparent with accent gradient border ring.
  - Both: rounded-full text-sm px-7 py-3.5 hover:scale-105.

### GSAP Entrance
Timeline with ease: "power3.out":
- .name-reveal: opacity 0→1, y 50→0, duration 1.2s, delay 0.1s
- .blur-in: opacity 0→1, filter blur(10px)→blur(0px), y 20→0, duration 1s, stagger 0.1, delay 0.3s

### Scroll Indicator
Bottom-center, text-xs text-muted uppercase tracking-[0.2em] "SCROLL" label above a w-px h-10 bg-stroke line with animated highlight using .animate-scroll-down.

---

## Section 3: Selected Works

bg-bg py-12 md:py-16. Inner: max-w-[1200px] mx-auto px-6 md:px-10 lg:px-16.

### Header
Framer Motion whileInView — opacity 0→1, y 30→0, duration 1s, ease [0.25,0.1,0.25,1], viewport once margin "-100px".
- Eyebrow: w-8 h-px bg-stroke + "Selected Work" text-xs text-muted uppercase tracking-[0.3em]
- Heading: "Featured *projects*" — italic word in font-display italic
- Subtext: "A selection of projects I've worked on, from concept to launch."
- "View all work" button (desktop only, hidden md:inline-flex) — rounded-full with gradient hover border ring + right arrow

### Bento Grid
grid grid-cols-1 md:grid-cols-12 gap-5 md:gap-6. Column spans alternate: 7/5/5/7.

4 project cards with titles: Automotive Motion, Urban Architecture, Human Perspective, Brand Identity.

Each card: bg-surface border border-stroke rounded-3xl with aspect ratios. Contains:
- Background image with object-cover group-hover:scale-105
- Halftone overlay: radial-gradient(circle, #000 1px, transparent 1px) at 4×4px, opacity-20 mix-blend-multiply
- Hover: bg-bg/70 opacity-0→1 + backdrop-blur-lg
- Hover label: pill with animated gradient border, white bg, "View — *Title*" (title in font-display italic)

---

## Section 4: Journal

bg-bg py-16 md:py-24. Same header pattern (eyebrow + "Recent *thoughts*" + subtext + "View all" button).

4 journal entries displayed as horizontal pills (rounded-[40px] sm:rounded-full) with titles, images, read times, and dates.

Each entry: flex items-center gap-6 p-4 bg-surface/30 hover:bg-surface border border-stroke.

---

## Section 5: Explorations (Parallax Gallery)

min-h-[300vh] section for scroll-driven parallax.

### Layer 1: Pinned Center (z-10)
h-screen div pinned with GSAP ScrollTrigger.create({ pin: contentRef, pinSpacing: false }).
- Eyebrow: "Explorations"
- Heading: "Visual *playground*"
- Subtext + Dribbble button

### Layer 2: Parallax Columns (z-20, absolute)
grid grid-cols-2 gap-12 md:gap-40 inside max-w-[1400px].

6 items split into 2 columns with GSAP scroll-driven parallax movement.
Cards: aspect-square max-w-[320px], with rotation and lightbox on click.

---

## Section 6: Stats

bg-bg py-16 md:py-24. 3-column grid with stats: 20+ Years Experience, 95+ Projects Done, 200% Satisfied Clients.

---

## Section 7: Contact / Footer

bg-bg pt-16 md:pt-20 pb-8 md:pb-12 overflow-hidden.

### Background Video
Same HLS source as hero, but flipped vertically (scale-y-[-1]). Heavier overlay: bg-black/60.

### GSAP Marquee
"BUILDING THE FUTURE • " repeated 10×. GSAP xPercent: -50, duration 40, ease "none", repeat -1.

### CTA
Email button: mailto:hello@michaelsmith.com with gradient hover border ring.

### Footer Bar
Social links [Twitter, LinkedIn, Dribbble, GitHub] + Green pulsing dot + "Available for projects"

---

## Dependencies
gsap, framer-motion, hls.js, react-router-dom, tailwindcss-animate

Add smooth scroll nav and page transitions.
```

---

## 15. Securify Data Security

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `securify-hero`

```
Build a full-screen hero section for a data-security SaaS landing page called "securify" using React + TypeScript + Tailwind CSS, with a looping fullscreen background video, a floating pill-shaped navbar, and large staggered typography.

Fonts & Global Styles

Load Google font "Readex Pro" weights 300, 400, 500, 600, 700.
Set body font-family: 'Readex Pro', system-ui, -apple-system, sans-serif;, background #000, color #fff, antialiased.
Make html, body, #root height 100%.
Add a .hero-title class with letter-spacing: -0.04em; line-height: 0.95;.
Section container

A <section> with classes: relative h-screen w-full overflow-hidden bg-black.
Background video

<video> with className="absolute inset-0 w-full h-full object-cover", autoPlay loop muted playsInline, and src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_063509_7d167302-4fd4-480b-8260-18ab572333d4.mp4".
Navbar (absolute, z-20, px-6 md:px-10 pt-6, top-0 left-0 right-0)

A <nav> with flex items-center justify-between gap-4.
Left pill: flex items-center gap-2 bg-neutral-900/90 backdrop-blur rounded-full pl-4 pr-6 py-3 containing:
A custom white SVG logo (viewBox 0 0 256 256, class h-5 w-5) with path: M 128 192 L 128 256 L 64.5 256 L 32 223 L 0 192 L 0 128 L 64 128 Z M 256 192 L 256 256 L 192.5 256 L 160 223 L 128 192 L 128 128 L 192 128 Z M 128 64 L 128 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 Z M 256 64 L 256 128 L 192.5 128 L 160 95 L 128 64 L 128 0 L 192 0 Z filled #ffffff.
Brand text "securify" (text-white text-sm font-normal tracking-tight).
Center pill (hidden on mobile): hidden md:flex items-center gap-1 bg-neutral-900/90 backdrop-blur rounded-full px-3 py-2 with four anchor links: "platform", "solutions", "company", "support" — each text-neutral-300 hover:text-white transition-colors text-sm px-5 py-2 rounded-full.
Right button: "get started" — bg-white text-black text-sm font-normal rounded-full px-6 py-3 hover:bg-neutral-200 transition-colors.
Foreground content wrapper: relative h-full w-full (rendered after Navbar, above the video).

Three giant staggered headline words (each an <h1> with class hero-title absolute text-white font-medium text-[14vw] md:text-[13vw]):

"protect" — left-4 md:left-10 top-[18%]
"your" — right-4 md:right-10 top-[38%]
"data" — left-[18%] md:left-[28%] top-[58%]
All lowercase.

Description paragraph (absolute, left-6 md:left-10 top-[46%], max-w-[240px] text-[15px] leading-snug text-white/90):

"we can guarding your data with utmost care, empowering you with privacy everywhere"

Stat block — top-right (absolute right-6 md:right-24 top-[14%]):

Row: flex items-center gap-3 justify-end — a diagonal divider (hidden md:block h-px w-24 bg-white/40 rotate-[20deg]) then number "+65k" (text-4xl md:text-5xl font-medium tracking-tight).
Sublabel: "startups use" (text-xs md:text-sm text-white/70 mt-1 text-right).
Bottom gradient overlay: pointer-events-none absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-b from-transparent to-black.

Stat block — bottom-left (absolute left-6 md:left-20 bottom-20 md:bottom-24):

Row: number "+1.5b" then divider hidden md:block h-px w-24 bg-white/40 rotate-[-20deg].
Sublabel: "gb data was protected" (text-xs md:text-sm text-white/70 mt-1).
Stat block — bottom-right (absolute right-6 md:right-20 bottom-16 md:bottom-20):

Row: diagonal divider rotate-[-20deg] then "+300k".
Sublabel: "downloads" (right-aligned, text-white/70).
Notes

All text is lowercase.
Navbar pills use bg-neutral-900/90 backdrop-blur.
Only transitions: hover:text-white on nav links, hover:bg-neutral-200 on the button.
No purple/indigo anywhere; palette is pure black, white, neutral-900, and white opacity variants (white/40, white/70, white/90).
Responsive: mobile hides nav links and diagonal dividers; typography scales via vw units.
```

---

## 16. Portal

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `portal-hero`

```
PROMPT:

Build a full-viewport cinematic movie/streaming hero section using React, Tailwind CSS, and Lucide React icons. Use the Inter font from Google Fonts. The entire page is a single full-height hero -- no scrolling, no additional sections.

BACKGROUND VIDEO:

A full-screen background video plays on loop, muted, autoplaying, covering the entire viewport with object-cover. The video is fixed-positioned behind everything at z-index 0.

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260406_094145_4a271a6c-3869-4f1c-8aa7-aeb0cb227994.mp4

BOTTOM BLUR OVERLAY (no gradient darkening):

Over the video, there is a single fixed, full-screen overlay div that applies a strong backdrop-blur-xl. This div uses a CSS mask so the blur only appears at the bottom and fades to transparent toward the middle of the screen. There is NO dark gradient overlay -- only blur.

The mask: mask-image: linear-gradient(to top, black 0%, transparent 45%) (with the -webkit- prefix too).

This overlay is pointer-events-none and sits at z-index 1.

FONT:

Import Inter from Google Fonts (weights 300-700). Set font-family: 'Inter', sans-serif on the body.

LIQUID GLASS EFFECT (used on multiple buttons):

Create a reusable .liquid-glass CSS class with these exact properties:

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity
backdrop-filter: blur(4px) (with -webkit- prefix)
border: none
box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1)
position: relative; overflow: hidden
A ::before pseudo-element that creates a thin glowing border effect:
position: absolute; inset: 0; border-radius: inherit; padding: 1.4px
background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)
Uses -webkit-mask with linear-gradient(#fff 0 0) content-box and linear-gradient(#fff 0 0) combined with -webkit-mask-composite: xor and mask-composite: exclude to create a border-only gradient stroke
pointer-events: none
BLUR-FADE-UP ANIMATION (used on every element with staggered delays):

Create a @keyframes blurFadeUp animation:

From: opacity: 0; filter: blur(20px); transform: translateY(40px)
To: opacity: 1; filter: blur(0); transform: translateY(0)
The .animate-blur-fade-up class applies this as animation: blurFadeUp 1s ease-out forwards with initial opacity: 0. Each element on the page gets a staggered animationDelay via inline style.

NAVBAR (z-index 50, relative positioned):

A horizontal navbar with justify-between, padding px-4 sm:px-6 md:px-12 py-4 md:py-6.

Left: A text logo (e.g. your brand name like "CINEMATIC" or similar) styled as h-8 md:h-10, with blur-fade-up animation at delay 0ms.

Center (desktop only, hidden below lg): Navigation links -- "Movies", "TV Series", "Editor's Pick", "Interviews", "User Reviews" -- each as an anchor with text-sm, hover:text-gray-300 transition-colors, and staggered blur-fade-up delays from 100ms to 300ms (50ms increments).

Right: Two buttons visible on sm and up:

A "Search" button -- rounded-full liquid-glass pill with the text "Search" and a Lucide Search icon (size 18), padding px-4 md:px-6 py-2, blur-fade-up at 350ms.
A user/profile circle button -- w-10 h-10 rounded-full liquid-glass with a Lucide User icon (size 18), blur-fade-up at 400ms.
A hamburger menu button visible only below lg -- w-10 h-10 rounded-full liquid-glass with animated icon transition between Lucide Menu and X icons. The transition uses rotate-180, opacity, and scale-50 with duration-500 ease-out. Blur-fade-up at 350ms.
MOBILE MENU (below lg breakpoint):

An absolutely positioned dropdown below the navbar (top-[72px]), z-index 40. It slides in with translate-y-0 opacity-100 when open, -translate-y-4 opacity-0 pointer-events-none when closed, duration-500 ease-out.

Background: bg-gray-900/95 backdrop-blur-lg with border-t border-b border-gray-800 shadow-2xl.
Contains the same 5 nav links, each in a column with py-3 px-3 rounded-lg, hover:bg-gray-800/50, and staggered slide-in animations (translate-x based, 50ms delay increments).
Below sm, also shows Search and Profile buttons in a bordered section at the bottom.
HERO CONTENT (bottom of viewport):

A flex container that grows to fill remaining space and aligns content to the bottom (flex-1 flex flex-col justify-end), with padding px-4 sm:px-6 md:px-12 pb-8 md:pb-16, z-index 10.

Inside, a flex-col md:flex-row items-end gap-8 layout:

Left side (flex-1):

Metadata row -- a horizontal flex-wrap row with gap-3 sm:gap-6 mb-6 md:mb-8 text-xs sm:text-sm, blur-fade-up at 300ms:

Star icon (size 16, fill-white, responsive to sm:w-5 sm:h-5) + "8.7/10 IMDB" (font-medium)
Clock icon (size 16) + "132 min"
Calendar icon (size 16) + "April, 2025"
Title -- text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-normal, letter-spacing -0.04em, mb-4 md:mb-6, blur-fade-up at 400ms. Text: "Step Through. Work Smarter."

Description -- text-base sm:text-lg md:text-xl text-gray-400 mb-6 md:mb-12 max-w-2xl, blur-fade-up at 500ms. Text: "A voyage through forgotten realms, where past and future intertwine."

CTA buttons -- flex-wrap row with gap-3 sm:gap-4:

"Watch Now" -- bg-white text-black rounded-full font-medium, px-6 sm:px-8 py-2.5 sm:py-3, with a Lucide Play icon (size 18, fill-black), hover:bg-gray-200, blur-fade-up at 600ms.
"Learn More" -- rounded-full font-medium liquid-glass, same padding, blur-fade-up at 700ms.
Right side (navigation arrows):

A row of two pill buttons (md:w-auto, aligned right on desktop, left on mobile):

"Previous" button -- rounded-full liquid-glass, px-4 sm:px-6 py-2.5 sm:py-3, with Lucide ChevronLeft icon, blur-fade-up at 800ms.
"Next" button -- same styling with Lucide ChevronRight icon, blur-fade-up at 900ms.
COLOR PALETTE:

Background: pure black (bg-black)
Text: white, with text-gray-400 for the subtitle
All interactive glass elements use the .liquid-glass class (nearly transparent white with blur)
The only solid-colored element is the "Watch Now" button (white background, black text)
STAGGER TIMING SUMMARY:

Logo: 0ms
Nav links: 100ms, 150ms, 200ms, 250ms, 300ms
Search button: 350ms
User button: 400ms
Metadata row: 300ms
Title: 400ms
Description: 500ms
Watch Now: 600ms
Learn More: 700ms
Previous: 800ms
Next: 900ms
RESPONSIVE BREAKPOINTS:

Below sm (< 640px): Smaller text, tighter padding, Search/User buttons hidden (available in mobile menu)
Below lg (< 1024px): Nav links hidden, hamburger menu shown
md and up: Side-by-side layout for hero content and navigation arrows
lg and up: Full desktop navbar with all links visible
```

---

## 17. Max Reed Portfolio

- **Category**: Features
- **Type**: features
- **Page Type**: hero
- **ID**: `max-reed-portfolio`

```
Build a full-viewport dark personal portfolio Features section using React + TypeScript + Tailwind CSS + lucide-react.

**Layout & Structure:**
- Full screen dark background `#0a0a0a`, white text, Inter font with antialiased smoothing
- Top header row: left side has a heading "Hi, I'm Max Reed!" (size `text-[28px] sm:text-3xl md:text-4xl lg:text-[44px]`, leading `1.15`, font-normal, tracking-tight) followed by a paragraph "A London-based independent creator shaping sharp visual systems, web-ready products, and story-first campaigns. With a decade of craft behind me, I help ideas move with focus and intention." (text-sm md:text-[15px], leading-[1.6], text-white/60, max-w-3xl). Header container has `max-w-3xl`.
- Right side of header: a liquid-glass rounded-full button "Let's Team Up Today" (px-5 sm:px-6, py-2.5 sm:py-3)
- Overall section padding: `px-4 sm:px-6 md:px-10 lg:px-14 py-6 sm:py-8 md:py-10`, full screen `lg:h-screen`

**Grid (3 columns on lg, 2 on md, 1 on mobile, gap-4 md:gap-5):**

**Column 1 - Background card (rounded-2xl, bg-black):**
- Background video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260507_150203_44a5bd32-516a-47ce-a077-8acbf9aa8991.mp4` (autoPlay loop muted playsInline, absolute inset-0 object-cover)
- Top: centered "BACKGROUND" section label (uppercase, tracking-[0.22em], text-[11px], text-white/70) with Sparkle icons on each side (h-3 w-3, strokeWidth 1.5)
- Bottom: career timeline as a 4-col grid `[auto_auto_1fr_auto]`:
  - 2023-Now · Freelance Creative · Solo Studio
  - 2020-2023 · Head of Brand Design · Rove Studio
  - 2017-2020 · Visual Stylist · Ember Works
  - Separator between year and role is a Sparkle icon (h-3 w-3, text-white/60)

**Column 2 (stacked rows, md:grid-rows-[auto_1fr]):**

Top - Client Voice card (rounded-2xl, bg-[#324444], p-5 md:p-6, with noise-overlay):
- Left-aligned "CLIENT VOICE" label with Sparkle icons (justify-start)
- Quote: "Max reshaped our image with a degree of finesse and vision that surpassed what we'd hoped for. The process felt graceful, and the outcomes speak for themselves." (text-[13px] sm:text-[13.5px], leading-[1.6], text-white/85)
- Attribution: **Elena Brooks**, Creative Director — Halcyon

Bottom - 10M+ card (rounded-2xl, bg-black):
- Background video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260507_154543_d5b83fc1-9cea-44f3-b5e8-8f325935211a.mp4`
- Centered huge text "10M+" (text-5xl sm:text-6xl md:text-7xl lg:text-[88px], font-light, tracking-tight, drop-shadow)
- Bottom caption "Raised for startups" (centered, text-white/85)

**Column 3 (stacked):**

Top - Daily Software card (rounded-2xl, bg-black):
- Background video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260507_153148_d7a3e1dd-e5d0-4ce6-8306-00d7522ecc44.mp4`
- Top: "DAILY SOFTWARE" section label
- Bottom: two scrolling marquee rows of liquid-glass icon tiles (h-14 w-14 md:h-16 md:w-16, rounded-xl). Row 1 scrolls left with icons [Figma, Framer, Palette, PenTool, Layers, Type, Aperture, Chrome]. Row 2 scrolls right with icons [Camera, Brush, Box, Wand2, Figma, Framer, Type, Layers]. Each row duplicated for seamless loop. Mask fade on both edges with `[mask-image:linear-gradient(to_right,transparent,black_8%,black_92%,transparent)]`.

Bottom - Reach Me card (rounded-2xl, bg-[#324444], p-5 md:p-6, noise-overlay):
- "REACH ME" section label
- Email: hi@maxreed.com
- Phone: +44 207 81 63
- Top-right ArrowUpRight icon button (h-9 w-9 rounded-full)

**Custom CSS in index.css:**

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

@keyframes marquee-left { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@keyframes marquee-right { from { transform: translateX(-50%); } to { transform: translateX(0); } }
.animate-marquee-left { animation: marquee-left 22s linear infinite; }
.animate-marquee-right { animation: marquee-right 26s linear infinite; }

.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.55;
  mix-blend-mode: soft-light;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix type='matrix' values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
  background-size: 240px 240px;
}
```

Font: Inter (system fallback). Icons from lucide-react: ArrowUpRight, Sparkle, Figma, Framer, Palette, PenTool, Layers, Type, Aperture, Chrome, Camera, Brush, Box, Wand2. All icons use strokeWidth 1.5.
```

---

## 18. Mindloop Landing

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: landing
- **ID**: `mindloop-landing`

```
Build a dark monochrome landing page called Mindloop — a newsletter/content platform. Use React + Vite + TypeScript + Tailwind CSS + shadcn/ui + Framer Motion. Fonts: Inter (sans) and Instrument Serif (serif, used for italic accent words). The entire theme is pure black (#000) background with white foreground — no colors or gradients beyond monochrome. Install hls.js and framer-motion.

Design System (index.css)
All CSS variables in HSL (no hsl() wrapper in the variable, just the values):

--background: 0 0% 0%
--foreground: 0 0% 100%
--card: 0 0% 5%
--card-foreground: 0 0% 100%
--primary: 0 0% 100%
--primary-foreground: 0 0% 0%
--secondary: 0 0% 12%
--secondary-foreground: 0 0% 85%
--muted: 0 0% 15%
--muted-foreground: 0 0% 65%
--accent: 170 15% 45%
--accent-foreground: 0 0% 100%
--border: 0 0% 20%
--input: 0 0% 18%
--ring: 0 0% 40%
--hero-subtitle: 210 17% 95%
Liquid Glass Effect (global CSS class .liquid-glass)

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
Animation Pattern
All sections use a reusable fadeUp helper with staggered delays:

const fadeUp = (delay: number) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-100px" },
  transition: { duration: 0.6, delay, ease: "easeOut" },
});

Page Structure (top to bottom)
1. Navbar (fixed, transparent)
Left: Logo (concentric circles icon — outer w-7 h-7 with border-2 border-foreground/60, inner w-3 h-3 with border border-foreground/60) + "Mindloop" bold text.
Center-left: Nav links ["Home", "How It Works", "Philosophy", "Use Cases"] separated by • dots. Links are text-muted-foreground hover:text-foreground.
Right: 3 social icons (Instagram, Linkedin, Twitter from lucide-react) in liquid-glass circular buttons (w-10 h-10 rounded-full).
No background — fully transparent, fixed top-0 z-50, padding px-8 md:px-28 py-4.

2. Hero Section (full viewport height)
Background: autoplaying looping muted MP4 video covering the entire section.
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260325_120549_0cd82c36-56b3-4dd9-b190-069cfc3a623f.mp4
Bottom gradient: h-64 bg-gradient-to-t from-background to-transparent for smooth fade to black.
Content (centered, z-10, pt-28 md:pt-32):
Avatar row: 3 overlapping circular avatars (-space-x-2, w-8 h-8 rounded-full border-2 border-background) + "7,000+ people already subscribed" in text-muted-foreground text-sm.
Heading: text-5xl md:text-7xl lg:text-8xl font-medium tracking-[-2px] — "Get Inspired with Us" where "Inspired" is font-serif italic font-normal.
Subtitle: text-lg in hsl(var(--hero-subtitle)) color — "Join our feed for meaningful updates, news around technology and a shared journey toward depth and direction."
Email form: liquid-glass rounded-full p-2 max-w-lg container with email input and a white bg-foreground text-background rounded-full px-8 py-3 "SUBSCRIBE" button with whileHover scale 1.03 and whileTap scale 0.98.

3. "Search has changed" Section
Top padding pt-52 md:pt-64, bottom padding pb-6 md:pb-9.
Heading: text-5xl md:text-7xl lg:text-8xl — "Search has changed. Have you?" with "changed." in serif italic.
Subtitle: text-muted-foreground text-lg max-w-2xl mx-auto mb-24.
3 platform cards (grid md:grid-cols-3 gap-12 md:gap-8 mb-20): Each card has a 200x200 icon image centered, platform name (font-semibold text-base), and description (text-muted-foreground text-sm).
ChatGPT icon: local asset icon-chatgpt.png
Perplexity icon: local asset icon-perplexity.png
Google AI icon: local asset icon-google.png
Bottom tagline: "If you don't answer the questions, someone else will." in text-muted-foreground text-sm text-center.

4. Mission Section
Padding pt-0 pb-32 md:pb-44.
Video: Large 800x800 looping autoplaying muted video centered.
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260325_132944_a0d124bb-eaa1-4082-aa30-2310efb42b4b.mp4
Scroll-driven word-by-word reveal using useScroll and useTransform from framer-motion:
Paragraph 1 (text-2xl md:text-4xl lg:text-5xl font-medium tracking-[-1px]): "We're building a space where curiosity meets clarity — where readers find depth, writers find reach, and every newsletter becomes a conversation worth having." Words "curiosity", "meets", "clarity" are highlighted in --foreground, rest in --hero-subtitle.
Paragraph 2 (text-xl md:text-2xl lg:text-3xl font-medium mt-10): "A platform where content, community, and insight flow together — with less noise, less friction, and more meaning for everyone involved."
Each word transitions opacity from 0.15 to 1 based on scroll progress.

5. Solution Section
Padding py-32 md:py-44, border-t border-border/30.
Label: "SOLUTION" in text-xs tracking-[3px] uppercase text-muted-foreground.
Heading: text-4xl md:text-6xl — "The platform for meaningful content" (serif italic on "meaningful").
Video: Rounded rounded-2xl, aspect-[3/1] object-cover.
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260325_125119_8e5ae31c-0021-4396-bc08-f7aebeb877a2.mp4
4-column feature grid (md:grid-cols-4 gap-8): Curated Feed, Writer Tools, Community, Distribution — each with title (font-semibold text-base) and description (text-muted-foreground text-sm).

6. CTA Section
Padding py-32 md:py-44, border-t border-border/30, overflow-hidden.
Background video (HLS via hls.js): absolute inset-0 object-cover z-0.
HLS URL: https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8
Uses Hls.isSupported() check with fallback to native HLS for Safari.
Overlay: absolute inset-0 bg-background/45 z-[1].
Content (z-10, centered):
Concentric circles logo icon (w-10 h-10 outer, w-5 h-5 inner).
Heading: "Start Your Journey" (serif italic).
Subtitle in text-muted-foreground.
Two buttons: "Subscribe Now" (bg-foreground text-background rounded-lg px-8 py-3.5) and "Start Writing" (liquid-glass rounded-lg).

7. Footer
Simple py-12 px-8 md:px-28 footer.
Left: "© 2026 Mindloop. All rights reserved." in text-muted-foreground text-sm.
Right: Privacy, Terms, Contact links in text-muted-foreground text-sm hover:text-foreground.

Key Dependencies
framer-motion for all animations
hls.js for the CTA background video streaming
@fontsource/inter (400, 500, 600, 700)
@fontsource/instrument-serif (400, 400-italic)
lucide-react for icons
tailwindcss-animate plugin

Assets Needed
3 avatar images (avatar-1.png, avatar-2.png, avatar-3.png)
3 platform icons (icon-chatgpt.png, icon-perplexity.png, icon-google.png)
```

---

## 19. RIVR

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `rivr-hero`

```
Build a Hero section for a DeFi dashboard named RIVR showcasing a sleek, glassmorphism aesthetic. Please mimic these exact specifications to ensure a premium UI.

Dependencies: 
- Use `lucide-react` for icons.
- Use `motion` (imported from `'motion/react'`) for animations.

1. Global Styles (`src/index.css`)
Import the custom 'Helvetica Regular' font, set the Tailwind theme properly, and reset the body. Exact CSS to include:
@import "tailwindcss";

@font-face {
    font-family: "Helvetica Regular";
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot");
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot?#iefix")format("embedded-opentype"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff2")format("woff2"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff")format("woff"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.ttf")format("truetype"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.svg#Helvetica Regular")format("svg");
}

@theme {
  --font-helvetica: "Helvetica Regular", ui-sans-serif, system-ui, sans-serif;
}

:root {
  font-family: var(--font-helvetica);
}

body {
  margin: 0;
  overflow-x: hidden;
  background-color: #f0f0f0;
}

2. App Structure (`src/App.tsx`)
Create a single `<main className="min-h-screen bg-[#f0f0f0]">` instance that returns the `<Hero />` component.

3. Hero Component (`src/components/Hero.tsx`)
Outer wrapper: `<div className="w-full h-screen flex items-center justify-center p-3 md:p-5 bg-[#f0f0f0]">`.
Inner container: `<section className="relative w-full max-w-[1536px] h-full rounded-[1.5rem] md:rounded-[3rem] overflow-hidden shadow-none flex flex-col items-center bg-white/10 group">`
Inside the `<section>`:
- The Video Background: 
  A `<video>` element with `autoPlay muted loop playsInline`. 
  Classes: `absolute inset-0 w-full h-full object-cover object-[65%] lg:object-center z-0`. 
  Source URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260428_193507_4286c423-2fd9-4efd-92bd-91a939453fc1.mp4` (Must use exactly this URL).
- The Content Layer:
  A `<div className="relative z-10 w-full h-full flex flex-col items-center">`.
  Inside it, place: `<Navbar />`, the text container, `<BottomLeftCard />`, and `<BottomRightCorner />`.
- Text Container:
  `<div className="w-full flex flex-col items-center pt-8 px-6 text-center max-w-4xl">`. Inside it:
  - `<HeroBadge />`
  - A `<motion.h1>` with class: `text-4xl sm:text-5xl md:text-6xl lg:text-[80px] font-normal text-[#5E6470] mb-2 tracking-tight leading-[1.05]`. Text: "Fluid Asset Streams". Animation: initial={{ opacity: 0, scale: 0.98 }}, animate={{ opacity: 1, scale: 1 }}, transition={{ duration: 0.8, delay: 0.2 }}.
  - A `<motion.p>` with class: `text-sm sm:text-base md:text-lg text-[#5E6470] opacity-80 leading-relaxed max-w-xl font-normal`. Text: "Access Smart Vaults, stake RIVR, NFTs, transform rigid holdings into liquid cash instantly.". Animation: initial={{ opacity: 0 }}, animate={{ opacity: 1 }}, transition={{ duration: 0.8, delay: 0.4 }}.

4. Navbar Component (`src/components/Navbar.tsx`)
Wrapper: `<nav className="flex items-center justify-between py-6 px-6 md:px-10 w-full relative z-10">`.
- Left Side (hidden spacer for centering): `<div className="flex-1 hidden md:block" />`
- Center Menu: `<ul className="hidden md:flex items-center gap-8 text-[rgb(45,45,45)] font-normal text-sm">`. Include items: Ecosystem, Economics (hasDropdown), Developers, Governance (hasDropdown). List items need: `cursor-pointer hover:opacity-70 transition-opacity flex items-center gap-1 group`. Append a `ChevronRight` icon (classes: `w-4 h-4 transition-transform group-hover:translate-x-0.5`) if hasDropdown is true.
- Mobile Logo: `<div className="md:hidden"><span className="font-regular tracking-tighter text-xl text-[rgba(30,50,90,0.9)]">RIVR</span></div>`
- Right Button: `<div className="flex-1 flex justify-end">` wrapping a `<motion.button>` (whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}). 
  Button classes: `flex items-center bg-[rgba(30,50,90,0.8)] text-white rounded-full pl-2 pr-4 md:pr-6 py-1.5 md:py-2 gap-2 md:gap-3 hover:bg-[rgba(30,50,90,1)] transition-colors group`. Inside button: Add an icon wrapper `<div className="bg-white/20 p-1 md:p-1.5 rounded-full flex items-center justify-center">` containing `ArrowUpRight` (w-4 h-4 md:w-5 md:h-5 text-white), and a text node "Book Demo" (`text-xs md:text-sm font-normal`).

5. HeroBadge Component (`src/components/HeroBadge.tsx`)
Returns a `<motion.div>` (initial opacity 0, y 20; animate opacity 1, y 0; transition duration 0.6, ease "easeOut").
Classes: `flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 backdrop-blur-md border border-white/20 mx-auto mb-3 w-fit`.
Contents: `<Sparkles className="w-4 h-4 text-[rgba(30,50,90,0.8)]" />` and text `<span className="text-[14px] font-normal text-[rgba(30,50,90,0.9)]">Fluid Staking</span>`.

6. BottomLeftCard Component (`src/components/BottomLeftCard.tsx`)
Returns a `<motion.div>` (initial x: -20, opacity: 0; animate x: 0, opacity: 1; transition: duration 0.8, delay 0.2).
Position/Styling: `absolute bottom-28 right-4 left-auto md:left-6 md:right-auto md:bottom-6 lg:bottom-10 lg:left-10 p-3 md:p-4 lg:p-5 rounded-[1.2rem] md:rounded-[1.5rem] lg:rounded-[2.2rem] bg-white/30 backdrop-blur-xl flex flex-col gap-2 lg:gap-3 min-w-[140px] md:min-w-[150px] lg:min-w-[180px] w-fit`.
- Top text block: column with "5.2K" (classes: `text-2xl md:text-3xl font-normal text-[rgba(30,50,90,0.9)] tracking-tight`) and "Active Yielders" (classes: `text-[10px] md:text-[12px] font-normal text-[rgba(30,50,90,0.6)] uppercase tracking-wider`).
- Join Discord `<motion.button>` (hover/tap scale 1.02/0.98). Classes: `flex items-center bg-white rounded-full pl-1.5 pr-5 py-1.5 gap-2 hover:bg-white/90 transition-colors self-start group`. Inside: wrap `ArrowUpRight` in `<div className="bg-[rgba(30,50,90,0.1)] p-1 rounded-full ...">` (using `text-[rgba(30,50,90,0.9)]` for icon) and append "Join Discord" text (`text-[14px] font-normal text-[rgba(30,50,90,0.9)]`).

7. BottomRightCorner Component (`src/components/BottomRightCorner.tsx`)
This requires a complex faux-cutout layout. Use a `<motion.div>` (initial y: 20, opacity: 0; animate y: 0, opacity: 1; duration: 0.8, delay: 0.4).
Classes: `absolute bottom-0 right-0 p-3 pt-5 pl-8 sm:p-4 sm:pt-6 sm:pl-10 md:p-6 md:pt-8 md:pl-14 bg-[#f0f0f0] rounded-tl-[1.5rem] sm:rounded-tl-[2rem] md:rounded-tl-[3.5rem] flex items-center gap-3 sm:gap-4 md:gap-6`.
CRITICAL corner masks to include inside this container:
- Top intersection mask: `<div className="absolute -top-[1.5rem] sm:-top-[2rem] md:-top-[3.5rem] right-0 w-[1.5rem] sm:w-[2rem] md:w-[3.5rem] h-[1.5rem] sm:h-[2rem] md:h-[3.5rem] pointer-events-none"><svg width="100%" height="100%" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M56 56V0C56 30.9279 30.9279 56 0 56H56Z" fill="#f0f0f0"/></svg></div>`
- Left intersection mask: `<div className="absolute bottom-0 -left-[1.5rem] sm:-left-[2rem] md:-left-[3.5rem] w-[1.5rem] sm:w-[2rem] md:w-[3.5rem] h-[1.5rem] sm:h-[2rem] md:h-[3.5rem] pointer-events-none"><svg width="100%" height="100%" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M56 56H0C30.9279 56 56 30.9279 56 0V56Z" fill="#f0f0f0"/></svg></div>`
Content: 
- Circle Icon: A div with `bg-[rgba(30,50,90,0.05)] w-10 h-10 md:w-14 md:h-14 rounded-full flex items-center justify-center border border-[rgba(30,50,90,0.1)]` using `ArrowUpRight` (`text-[rgba(30,50,90,0.8)]`).
- Info column containing title "Documentation" (`text-[16px] md:text-[20px] font-normal text-[rgba(30,50,90,0.95)]`). Below it, a line containing text "Library" and a `ChevronRight` icon wrapped in `<div className="flex items-center gap-1 text-[rgba(30,50,90,0.6)] cursor-pointer hover:text-[rgba(30,50,90,0.8)] transition-colors"><span className="text-[12px] md:text-[15px] font-normal">...`
```

---

## 20. AI Designer Portfolio

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `vortex-studio-hero`

```
Create a single-page landing page for a creative design studio called "Viktor Oddy" using React, TypeScript, Vite, and Tailwind CSS. Use lucide-react for icons. The page has a white background throughout and uses two custom fonts: "PP Neue Montreal" (body text, loaded from Webflow CDN) and "PP Mondwest" (serif accent font, loaded from a local /PPMondwest-Regular.woff2 file). The body default font is PP Neue Montreal with system fallbacks.

The page consists of these sections in order:

1. HERO SECTION (centered, narrow column max-w-[440px], px-6, pt-12 md:pt-16)

Logo text: "Viktor Oddy" in PP Mondwest serif font, text-[32px] md:text-[40px] lg:text-[44px], font-semibold, color #051A24, tracking-tight, mb-4. Fades in with staggered animation (delay 0.1s).
Tagline: "The creative studio of Viktor Oddy" in monospace font (font-mono), text-xs md:text-sm, color #051A24, mb-2. Animation delay 0.2s.
Main Heading: Two lines: "Build the next wave," and "the bold way." where "next wave" and "bold way." are in PP Mondwest serif. Text is text-[32px] md:text-[40px] lg:text-[44px], leading-[1.1], color #0D212C, tracking-tight, whitespace-nowrap. Animation delay 0.3s.
Description: Three paragraphs in a flex-col gap-6 container, text-sm md:text-base, color #051A24, leading-relaxed, mt-5 md:mt-6. Animation delay 0.4s.
Paragraph 1: "I spent seven years at Apple crafting products used by over a billion people. I founded Vortex Studio to bring that same level of thinking to innovators shaping what comes next."
Paragraph 2: "The studio is deliberately small. I guide the creative vision on every project, backed by a veteran design crew that moves fast without cutting corners."
Paragraph 3: "Projects start at $5,000 per month."
Two buttons in flex-col sm:flex-row, gap-3 md:gap-4, mt-5 md:mt-6. Animation delay 0.5s:
"Start a chat" (primary: bg-[#051A24], text white, rounded-full, px-7 py-3, with a complex multi-layered box-shadow including an inset highlight)
"View projects" (secondary: bg-white, text #051A24, no border, with subtle shadow)
2. INFINITE MARQUEE (full width, mt-16 md:mt-20, mb-16)

Horizontally scrolling image strip. Uses 8 GIF images duplicated (total 16) in a flex row with animate-marquee CSS animation (translateX(0) to translateX(-50%), 30s linear infinite on desktop, 10s on mobile). Images are h-[280px] md:h-[500px], object-cover, mx-3, rounded-2xl, shadow-lg.

Image URLs (all from motionsites.ai):

https://motionsites.ai/assets/hero-space-voyage-preview-eECLH3Yc.gif
https://motionsites.ai/assets/hero-portfolio-cosmic-preview-BpvWJ3Nc.gif
https://motionsites.ai/assets/hero-velorah-preview-CJNTtbpd.gif
https://motionsites.ai/assets/hero-asme-preview-B_nGDnTP.gif
https://motionsites.ai/assets/hero-transform-data-preview-Cx5OU29N.gif
https://motionsites.ai/assets/hero-aethera-preview-DknSlcTa.gif
https://motionsites.ai/assets/hero-orbit-web3-preview-BXt4OttD.gif
https://motionsites.ai/assets/hero-nexora-preview-cx5HmUgo.gif
3. TESTIMONIAL QUOTE SECTION (py-12, px-6, max-w-2xl, centered)

A quote icon (lucide-react Quote, w-6 h-6, text-slate-900). Animation delay 0.1s.
Large quote text: 'I left Apple to build the studio I always wanted to work with' where "Apple" is in PP Mondwest serif. Text sizing: text-[32px] md:text-[40px] lg:text-[44px], leading-[1.1], color #0D212C, tracking-tight. Animation delay 0.2s.
Author: "Viktor Oddy" in italic, text-sm, color #273C46. Animation delay 0.3s.
Three company logo names displayed as text: "Apple" (80px wide, 24px font), "IDEO" (83px wide, 24px font), "Polygon" (110px wide, 24px font). Font-medium, text-slate-900. Animation delay 0.4s.
Below logos: A parallax image (scrolls with a parallax effect based on viewport position, max offset 200px). The image URL is: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260330_103804_7aa5494f-4d5b-432e-9dc7-20715275f143.png&w=1280&q=85. Alt text "Chris Halaska". w-full max-w-xs rounded-2xl shadow-lg. Animation delay 0.5s. The parallax uses IntersectionObserver + scroll listener with requestAnimationFrame.
4. PRICING SECTION (full width, py-12, px-6)

Two cards in a grid (grid-cols-1 md:grid-cols-2, gap-8), aligned right on desktop (md:justify-end, md:max-w-4xl). Each card has rounded-[40px], pl-10 pr-10 md:pr-24 pt-3 pb-10.

Card 1 (Dark): bg-[#051A24], inset shadow. Text color #F6FCFF / #E0EBF0. Animation delay 0.1s.

Title: "Monthly Partnership" (text-[22px], font-medium)
Description: "A dedicated creative design team. / You work directly with Viktor."
Price: "$5,000" (text-2xl, color #F6FCFF), "Monthly" below
Two buttons: "Start a chat" (primary) + "How it works" (secondary), both linking to https://halaskastudio.com/./book
Card 2 (Light): bg-white, shadow-[0_4px_16px_rgba(0,0,0,0.08)]. Animation delay 0.2s.

Title: "Custom Project" (text-[22px], font-medium)
Description: "Fixed scope, fixed timeline. / Same team, same standards."
Price: "$5,000" (text-2xl, color #0D212C), "Minimum" below
One button: "Start a chat" (tertiary variant: white bg with combined shadow)
5. TESTIMONIAL CAROUSEL (full width, py-20)

Header row (md:max-w-4xl, md:ml-auto): Title "What builders say" (where "builders" is in PP Mondwest serif, same large heading size) on left. On the right: 5 filled black star icons (lucide-react Star, w-5 h-5, fill-black) + "Clutch 5/5" text.
Auto-scrolling carousel (3s interval, pauses on hover) with prev/next circular buttons (w-12 h-12 rounded-full, border border-[#0D212C]/20, lucide ChevronLeft/ChevronRight).
Cards are 427.5px wide on desktop (full width minus 48px on mobile), gap-6, with exit animation (opacity fade + scale down). Each card: bg-white, rounded-[32px] md:rounded-[40px], shadow-[0_4px_16px_rgba(0,0,0,0.08)], px-6 md:pl-10 md:pr-24 py-8.
Card content: SVG quote mark icon (custom path), quote text (text-base, color #0D212C, leading-relaxed), author row with circular avatar (w-12 h-12), name (font-semibold, text-sm), role/company with arrow prefix.
Testimonials array uses Pexels avatar images. The testimonials are tripled for infinite scroll effect. Transform uses cubic-bezier(0.4, 0, 0.2, 1) with 0.8s transition.
5 testimonials:

Marcus Anderson, CEO, Data.storage - "With very little guidance team delivered designs that were consistently spot on..."
alexwu, Founder, Nexgate - "Viktor led the creation of our best fundraising deck to date!..."
James Mitchell, VP Product, LaunchPad - "Working with Viktor transformed our product vision..."
Rachel Foster, Co-founder, Nexus Labs - "The design quality exceeded our expectations..."
David Zhang, Head of Design, Paradigm Labs - "Incredible work from start to finish..."
6. PROJECTS SECTION (max-w-[1200px], px-6, py-12)

Vertical stack of 3 project items (gap-16 md:gap-20). Each has:

Text block offset left (ml-20 md:ml-28): Project name in PP Mondwest serif (text-2xl md:text-3xl, font-semibold, color #051A24) + description (text-sm md:text-base, color #051A24/70)
Full-width image below (rounded-2xl, shadow-lg, object-cover)
Each item independently triggers fade-in animation via IntersectionObserver.
Projects:

"evr" - "From idea to millions raised for a web3 AI product" - https://motionsites.ai/assets/hero-evr-ventures-preview-DZxeVFEX.gif
"Automation Machines" - "Streamlining industrial automation processes" - https://motionsites.ai/assets/hero-automation-machines-preview-DlTveRIN.gif
"xPortfolio" - "Modern portfolio management platform" - https://motionsites.ai/assets/hero-xportfolio-preview-D4A8maiC.gif
7. PARTNER SECTION (full width, py-12, px-6)

Large white container (max-w-7xl, py-48, rounded-[40px], subtle shadow). On mouse hover, GIF thumbnails (from the marquee images array) spawn at cursor position with random rotation (-10 to +10 deg), fade out over 1000ms with scale-down, spawning every 80ms minimum. Uses requestAnimationFrame-style cleanup.

Centered heading: "Partner with us" in PP Mondwest serif, text-[48px] md:text-[64px] lg:text-[80px], color #0D212C, mb-12.
CTA button: Dark pill with circular avatar image (Pexels photo 415829, w-10 h-10 rounded-full) + "Start chat with Viktor". Same primary button shadow style.
8. FOOTER (full width, py-12, px-6, max-w-[1200px])

Flex row (md:flex-row). Left side: "Start a chat" primary button. Right side: ArrowUpRight icon (lucide-react), then two columns of links:

Column 1: Services, Work, About (anchor links)
Column 2: x.com, LinkedIn (external links, target _blank)
All links: text-base, color #051A24, hover:opacity-70 transition.

9. COPYRIGHT BAR (max-w-[1200px], px-6, py-4)

Flex row justify-between: "Vortex Studio Limited" on left, "Austin, USA" on right. Text-sm, color #051A24.

10. FIXED BOTTOM NAV (z-50, centered)

Floating pill fixed to bottom (bottom-6, centered via left-1/2 -translate-x-1/2). White bg, rounded-full, px-8 py-2, complex layered shadow. Contains: "V" letter in PP Mondwest serif (text-2xl, font-semibold, color #051A24) + "Start a chat" primary button.

ANIMATIONS:

All sections use a custom useInViewAnimation hook (IntersectionObserver with threshold 0.1, triggers once). Elements get class animate-fade-in-up when in view (otherwise opacity-0). The animation is defined in CSS:


@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}
Each element within a section has staggered animationDelay values (0.1s, 0.2s, 0.3s, etc.).

COLOR PALETTE:

Primary dark: #051A24
Secondary dark: #0D212C
Light text on dark: #F6FCFF, #E0EBF0
Body text: #051A24
Muted text: #273C46
Background: white throughout
BUTTON SHADOWS (critical for the design feel):

Primary: 0_1px_2px_0_rgba(5,26,36,0.1), 0_4px_4px_0_rgba(5,26,36,0.09), 0_9px_6px_0_rgba(5,26,36,0.05), 0_17px_7px_0_rgba(5,26,36,0.01), 0_26px_7px_0_rgba(5,26,36,0), inset_0_2px_8px_0_rgba(255,255,255,0.5)
Secondary: 0_0_0_0.5px_rgba(0,0,0,0.05), 0_4px_30px_rgba(0,0,0,0.08)
FONTS (CSS):


@font-face {
  font-family: 'PP Neue Montreal';
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9bb43e36419997ecfe_PPNeueMontreal-Book.otf') format('opentype');
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: 'PP Neue Montreal';
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9b39c5673e51a86f5a_PPNeueMontreal-Medium.otf') format('opentype');
  font-weight: 500;
  font-display: swap;
}
@font-face {
  font-family: 'PP Mondwest';
  src: url('/PPMondwest-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
FILE STRUCTURE:

src/App.tsx - Main layout with hero, marquee, and section composition
src/components/Button.tsx - Reusable button (primary/secondary/tertiary variants)
src/components/TestimonialSection.tsx - Quote with parallax image
src/components/PricingSection.tsx - Two pricing cards
src/components/TestimonialCarousel.tsx - Auto-scrolling testimonial cards
src/components/ProjectsSection.tsx - Project showcase items
src/components/PartnerSection.tsx - Interactive mouse-trail CTA section
src/components/Footer.tsx - Footer with links
src/components/CopyrightBar.tsx - Copyright line
src/components/BottomNav.tsx - Fixed floating bottom nav
src/hooks/useInViewAnimation.ts - IntersectionObserver scroll-trigger hook
src/index.css - Font faces, marquee animation, fade-in-up animation
```

---

## 21. CodeNest Coding Platform

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `codenest-hero`

```
Create a high-end, dark-themed hero section for a coding education platform called 'CodeNest' using React and Tailwind CSS. The design must be responsive and follow these precise specifications:

1. Background & Layout:

Background: Implement a full-screen background video using the HLS stream: https://stream.mux.com/tLkHO1qZoaaQOUeVWo8hEBeGQfySP02EPS02BmnNFyXys.m3u8. Use hls.js and set enableWorker: false to ensure stability in sandboxed environments.

Overlays: Set the video to 60% opacity. Add a dark linear gradient from the left (#070b0a to transparent) and a bottom-up gradient for readability.

Grid System: Add three thin vertical grid lines (white/10 opacity) at the 25%, 50%, and 75% marks across the screen (visible on desktop).

Central Glow: Place a large horizontal SVG ellipse glow in the center-top area with a cyan/dark green hue, using a 25px Gaussian blur filter.

2. The Liquid Glass Card:

Component: Create a 200x200px floating card positioned above the main headline, shifted exactly 50px upwards using translate-y-[-50px].

CSS Styling (Liquid Glass):

background: rgba(255, 255, 255, 0.01) with background-blend-mode: luminosity.

backdrop-filter: blur(4px).

box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1).

Border Effect: A ::before pseudo-element with inset: 0, padding: 1.4px, and a 180-degree white linear gradient. Use -webkit-mask-composite: xor and mask-composite: exclude to create a sharp, high-end border frame.

Content: '[ 2025 ]' tag (14px), 'Taught by Industry Professionals' headline (18px, using Instrument Serif italic for 'Industry'), and a small description (11px).

3. Hero Content & Typography:

Eyebrow: 'Career-Ready Curriculum' in Plus Jakarta Sans, bold, 11px, color #5ed29c.

Main Headline: 'LAUNCH YOUR CODING CAREER.' in Inter Extra Bold, uppercase, tracking-tight. Scale from 40px (mobile) to 72px (desktop). The final period must be green (#5ed29c).

Description: 'Master in-demand coding skills...' in Inter, 14px, 70% white opacity, max-width 512px.

Primary CTA: 'Get Started' button with an ArrowRight icon. Rounded-full, background #5ed29c, text #070b0a, uppercase, bold.

4. Global Navigation:

Header: Sticky/Absolute header with a white minimalist logo.

Desktop Menu: Links for 'PROJECTS', 'BLOG', 'ABOUT', 'RESUME' in Inter, 16px. Hover state: #5ed29c.

Mobile Menu: A functional hamburger menu that toggles a full-screen dark overlay.

5. Required Imports:

Fonts: Inter, Plus Jakarta Sans, and Instrument Serif (italic).

Icons: lucide-react (ArrowRight, Menu, X).

Library: hls.js for video streaming.
```

---

## 22. Power AI

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `power-ai-hero`

```
Create a full-screen dark hero section with a looping background video, navbar, headline, subtitle, CTA button, and a logo marquee at the bottom. Here are the exact specifications:

Theme & Colors (index.css CSS variables):
Background: 260 87% 3% (deep dark blue-purple)
Foreground: 40 6% 95% (off-white)
Hero sub text: 40 6% 82%
Body font: Geist Sans (via @fontsource/geist-sans)
Headline font: General Sans (loaded from Fontshare: https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap)

Background Video (Index page wrapper):
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_065045_c44942da-53c6-4804-b734-f9e07fc22e08.mp4
Positioned absolute inset-0 w-full h-full object-cover behind all content
Starts with opacity: 0
Custom JS-controlled fade loop: 0.5s fade-in at start, 0.5s fade-out at end, using requestAnimationFrame. On ended, opacity resets to 0, waits 100ms, then replays from 0
No gradient overlays on the video
The wrapper div has overflow-hidden, the hero content sits in a relative z-10 div above

Blurred overlay shape (centered behind content):
w-[984px] h-[527px] opacity-90 bg-gray-950 blur-[82px]
Absolutely positioned at top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
pointer-events-none
The hero section has overflow-visible so the blur is not clipped

Navbar:
Full width, py-5 px-8, flex row with justify-between
Left: logo image (src/assets/logo.png, height 32px)
Center: nav items — "Features" (with ChevronDown), "Solutions", "Plans", "Learning" (with ChevronDown). Each is a button with text-foreground/90 and hover transition
Right: "Sign Up" button using heroSecondary variant, rounded-full px-4 py-2
Below navbar: a 1px divider line with gradient from-transparent via-foreground/20 to-transparent, offset mt-[3px]

Hero content (vertically centered in remaining space via flex-1):
Headline: "Power AI" at text-[220px], font-normal, leading-[1.02], tracking-[-0.024em], font-family General Sans
"Power " is plain text-foreground
"AI" uses bg-clip-text text-transparent with backgroundImage: linear-gradient(to left, #6366f1, #a855f7, #fcd34d) (indigo → purple → amber)
Subtitle: "The most powerful AI ever deployed / in talent acquisition" — text-hero-sub, text-lg, leading-8, max-w-md, mt-[9px], opacity-80
CTA: "Schedule a Consult" button, heroSecondary variant, px-[29px] py-[24px], mt-[25px]

Logo marquee (pinned to bottom of hero, pb-10):
Container: max-w-5xl mx-auto
Left side: static text "Relied on by brands / across the globe" in text-foreground/50 text-sm
Right side: infinite scrolling marquee with logos: Vortex, Nimbus, Prysma, Cirrus, Kynder, Halcyn (duplicated for seamless loop)
Each logo: a liquid-glass 24x24 rounded-lg icon showing the first letter, plus the name in text-base font-semibold text-foreground
Marquee animation: translateX(0%) → translateX(-50%), 20s linear infinite
gap-16 between logos, gap-12 between text and marquee

Liquid glass utility class (in index.css):
.liquid-glass { background: rgba(255, 255, 255, 0.01); background-blend-mode: luminosity; backdrop-filter: blur(4px); border: none; box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1); position: relative; overflow: hidden; }
.liquid-glass::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.4px; background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%); -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; }

Section structure: min-h-screen flex flex-col — navbar at top, content centered via flex-1 flex items-center justify-center, marquee at bottom.
```

---

## 23. Bloom AI

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `bloom-ai-hero`

```
Create a full-screen hero landing page for "Bloom" — an AI-powered plant/floral design platform. The design uses a liquid glass morphism aesthetic over a looping video background.

Background
Full-screen autoplaying, looping, muted video background: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260315_073750_51473149-4350-4920-ae24-c8214286f323.mp4
Video covers entire viewport with object-cover, sits at z-0. All content floats above at z-10.

Fonts
Display/Body: Poppins (Google Fonts) — used for headings and body text
Serif accent: Source Serif 4 (Google Fonts) — used only for italic/emphasis text inside headings (e.g., <em>, <i>, .italic inside h1-h3)
Headings use font-weight: 500

Color Palette
Strict grayscale only — all CSS variables are 0 0% X% HSL values
Text is text-white, text-white/80, text-white/60, text-white/50 for hierarchy
No colored accents whatsoever

Liquid Glass CSS (two tiers)
Define under @layer components:

.liquid-glass (light)
background: rgba(255,255,255,0.01);
background-blend-mode: luminosity;
backdrop-filter: blur(4px);
border: none;
box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
position: relative; overflow: hidden;
::before pseudo-element: gradient border using linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, transparent 40%, transparent 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%) with padding: 1.4px, masked via -webkit-mask-composite: xor; mask-composite: exclude;

.liquid-glass-strong (heavy, for CTA/panels)
Same structure but backdrop-filter: blur(50px), box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15), and ::before uses 0.5/0.2 alpha instead of 0.45/0.15.

Layout — Two-Panel Split
Flex row, min-h-screen. Left panel w-[52%], right panel w-[48%] (hidden on mobile lg:flex).

Left Panel
Has a liquid-glass-strong overlay (absolute inset-4 lg:inset-6 rounded-3xl)
Nav: Logo image (/logo.png, 32×32) + "bloom" text (semibold, 2xl, tracking-tighter, white) on left. "Menu" button with Menu icon on right, liquid-glass pill.
Hero center (flex-1, centered):
Logo image again (80×80)
h1: "Innovating the / spirit of bloom AI" — text-6xl lg:text-7xl, tracking-[-0.05em], white. The italic part uses font-serif text-white/80
CTA button: "Explore Now" with Download icon in a w-7 h-7 rounded-full bg-white/15 circle. Button is liquid-glass-strong, rounded-full, hover:scale-105 active:scale-95
Three pills: "Artistic Gallery", "AI Generation", "3D Structures" — liquid-glass, rounded-full, text-xs text-white/80
Bottom quote:
"VISIONARY DESIGN" label (text-xs tracking-widest uppercase text-white/50)
Quote: "We imagined a realm with no ending." — mixed font-display/font-serif italic spans
Author: "MARCUS AURELIO" with horizontal lines on each side

Right Panel (desktop only)
Top bar: Social icons (Twitter, LinkedIn, Instagram) in a liquid-glass pill with ArrowRight. Account button with Sparkles icon button, both liquid-glass.
Community card: Small liquid-glass card (w-56), "Enter our ecosystem" title + description
Bottom feature section (mt-auto): Outer liquid-glass container with rounded-[2.5rem]
Two side-by-side cards: "Processing" (Wand2 icon) and "Growth Archive" (BookOpen icon), each liquid-glass rounded-3xl
Bottom card: flower image thumbnail (from @/assets/hero-flowers.png, 96×64), "Advanced Plant Sculpting" title + description, and a "+" button. All liquid-glass.

Icons
All from lucide-react: Sparkles, Download, Wand2, BookOpen, ArrowRight, Twitter, Linkedin, Instagram, Menu

Key Details
All interactive elements: hover:scale-105 transition-transform
Social icon links: text-white hover:text-white/80 transition-colors
Icon containers: w-8 h-8 rounded-full bg-white/10 flex items-center justify-center
No border classes anywhere — glass effect handles all borders via ::before
border-radius token: --radius: 1rem
```

---

## 24. Luminex

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `luminex-hero`

```
Create a modern React landing page with a full-screen HLS video background, glassmorphic navigation header, and hero content positioned in the bottom-left corner.
```

---

## 25. Sentinel AI

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `sentinel-ai-hero`

```
Create a full-screen dark hero landing page for a security company called "SENTINEL AI" using React, Vite, TypeScript, Tailwind CSS, shadcn/ui, and an embedded Spline 3D scene as the background. The tech stack uses @splinetool/react-spline and @splinetool/runtime for the 3D embed. Here is every detail:

FONT:
Google Fonts "Sora" with weights 300, 400, 500, 600, 700. Load it in index.html:


<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet">
Set font-sora as the body font via Tailwind config: fontFamily: { sora: ["Sora", "sans-serif"] } and apply font-sora antialiased on body.

COLOR THEME (all HSL CSS custom properties, dark only, no light mode):

--background: 0 0% 10% (dark charcoal)
--foreground: 0 0% 96% (near-white)
--primary: 119 99% 46% (vivid green)
--primary-foreground: 0 0% 4% (near-black)
--secondary: 0 0% 18%
--secondary-foreground: 0 0% 96%
--muted: 0 0% 16%
--muted-foreground: 0 0% 60%
--accent: 119 99% 46% (same vivid green as primary)
--accent-foreground: 0 0% 4%
--destructive: 0 84% 60%
--border: 0 0% 20%
--input: 0 0% 20%
--ring: 119 99% 46%
--radius: 0.5rem
--nav-button: 0 0% 18%
--hero-bg: 0 0% 8% (the darkest background, nearly black)
Map these in Tailwind config using hsl(var(--variable)) pattern. Add custom color tokens: nav-button and hero-bg.

CUSTOM ANIMATIONS (Tailwind config keyframes + animation):

fade-up keyframe:

0%: opacity: 0, transform: translateY(20px), filter: blur(4px)
100%: opacity: 1, transform: translateY(0), filter: blur(0)
Animation: fade-up 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards
fade-in keyframe:

0%: opacity: 0
100%: opacity: 1
Animation: fade-in 0.5s ease-out forwards
NAVBAR (fixed, transparent, floating over the Spline scene):

fixed top-0 left-0 right-0 z-50, horizontal flex, justify-between, padding px-8 lg:px-16 py-5
Left: Logo text "SENTINEL" -- text-foreground text-xl font-semibold tracking-tight
Center: Nav links array: ["Services", "About Us", "Projects", "Team", "Contacts"] -- each is text-sm text-muted-foreground hover:text-foreground transition-colors uppercase tracking-widest. Links use href={#section-name}. Hidden on mobile (hidden md:flex), with gap-8.
Right: "Get Quote" button using shadcn Button with a custom navCta variant: text-foreground bg-nav-button hover:bg-nav-button/80 active:scale-[0.97] transition-all. Size lg, with classes hidden md:inline-flex rounded-lg uppercase text-xs tracking-widest px-6.
HERO SECTION (full-screen, content at bottom-left):

Structure:

Outer <section>: relative min-h-screen flex items-end bg-hero-bg overflow-hidden
Spline 3D Background (absolute, full-size): Lazy-loaded via React.lazy(() => import("@splinetool/react-spline")) wrapped in <Suspense> with a fallback <div className="absolute inset-0 bg-hero-bg" />. The Spline component uses scene="https://prod.spline.design/Slk6b8kz3LRlKiyk/scene.splinecode" and className="w-full h-full". Placed inside <div className="absolute inset-0">.
Dark overlay: <div className="absolute inset-0 bg-black/30 z-[1] pointer-events-none" />
Content container: relative z-10 pointer-events-none w-full max-w-[90%] sm:max-w-md lg:max-w-2xl px-6 md:px-10 pb-10 md:pb-10 pt-32
Content elements (all with staggered animate-fade-up, starting opacity-0):

Heading (delay 0.2s): <h1> with text "SENTINEL" in white + " AI" in primary green. Classes: text-[clamp(3rem,8vw,6rem)] font-bold leading-[1.05] tracking-[-0.05em] text-foreground mb-2 md:mb-4 uppercase. The "AI" part is wrapped in <span className="text-primary">.

Subheading (delay 0.4s): <p> -- "We implement security correctly." -- text-foreground/80 text-[clamp(1.125rem,2.5vw,1.875rem)] font-light mb-3 md:mb-6

Description (delay 0.55s): <p> -- "Enterprise security systems built in days. AI-powered surveillance deployed with zero-trust architecture. Smart access control set up for your entire facility. All of it done right, not just fast." -- text-muted-foreground text-[clamp(0.875rem,1.5vw,1.25rem)] font-light mb-4 md:mb-8

Two CTA buttons (delay 0.7s): Wrapped in flex flex-wrap gap-3 font-bold. Both are plain <button> elements (not shadcn Button) with pointer-events-auto (to re-enable clicks since parent is pointer-events-none):

"Book a Call": bg-primary text-primary-foreground px-6 py-3 md:px-8 md:py-4 text-sm rounded-sm cursor-pointer hover:brightness-110 transition-all active:scale-[0.97]
"Our Work": bg-white text-background px-6 py-3 md:px-8 md:py-4 text-sm rounded-sm cursor-pointer hover:brightness-90 transition-all active:scale-[0.97]
Trust line (delay 0.85s): <p> -- "Trusted security partner. Columbus, OH. 12 systems deployed." -- text-muted-foreground/60 text-xs font-light mt-4 md:mt-6

All animated elements use style={{ animationDelay: "Xs" }} for the stagger, combined with the opacity-0 animate-fade-up classes.

PAGE WRAPPER (Index.tsx):
Simple wrapper: <div className="bg-hero-bg min-h-screen"> containing <Navbar /> and <HeroSection />.

KEY DEPENDENCIES:

@splinetool/react-spline and @splinetool/runtime for the 3D Spline embed
tailwindcss-animate plugin
shadcn/ui Button component with custom variants (navCta, hero, heroOutline)
class-variance-authority for button variants
IMPORTANT NOTES:

The Spline scene URL is https://prod.spline.design/Slk6b8kz3LRlKiyk/scene.splinecode -- this is the exact 3D scene used
The entire content area has pointer-events-none so clicks pass through to the Spline scene, but buttons re-enable with pointer-events-auto
Responsive fluid typography uses clamp() for the heading, subheading, and description
The content is anchored to the bottom-left of the viewport (flex items-end on the section + padding-bottom on the content)
No hamburger menu on mobile -- the nav links and CTA simply hide (hidden md:flex / hidden md:inline-flex)
```

---

## 26. DesignPro Academy

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `designpro-hero`

```
Create a full-screen hero section for a product design education platform called "DesignPro" with the following exact specifications:

Background:

Full-screen looping video background using this exact CloudFront URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_105406_16f4600d-7a92-4292-b96e-b19156c7830a.mp4

Video should autoplay, loop, be muted, and play inline

Background color: black (#000000)

Navigation Bar:

Logo: Circular design with a white border (2px), containing a smaller filled white circle inside, followed by "DesignPro" text

Navigation links in a rounded pill container with gray-700 border: Home, About Us, Courses, Instructors, Testimonials, Blog, Contact us (with arrow icon)

All nav links: white/80 opacity, hover to full white

Font size: text-sm

Mobile: Show hamburger menu icon on screens smaller than lg

Max width: 7xl container with proper padding

Content Layout:

Top Section (below nav):

Two-column layout on large screens, stacked on mobile

Left column: "We deliver transformative programs that empower emerging product designers with cutting-edge expertise and vision to thrive globally."

Right column (right-aligned on lg+): "8000+ Talented Designers Launched !"

Both paragraphs: white/80 opacity, text-sm on mobile, text-base on desktop

Hero Section (center):

Small uppercase text above heading: "Seats for Next Program Opening Soon" (white/80 opacity, text-xs on mobile, text-sm on desktop, tight tracking)

Main heading with these exact specifications:

Line 1: "Become" in white, font-medium

Line 2: "Product Leader." with animated shiny gradient effect

Font sizes: text-5xl (mobile) scaling up to text-9xl (xl screens)

Line height: 0.85

Letter spacing: tracking-tighter

ShinyText Component:

Use framer-motion for animation

Base color: #64CEFB (light blue)

Shine color: #ffffff (white)

Animation speed: 3 seconds

Gradient spread: 100 degrees

Gradient should sweep across text continuously from left to right

Use CSS gradient with backgroundClip: text and transparent text fill

CTA Button:

Text: "Apply for Next Enrollment" with arrow icon (from lucide-react)

Black background, hover: gray-900

Rounded-full shape

Padding: px-6 md:px-8, py-3 md:py-4

Arrow should translate right on hover

Group hover animation on arrow icon

Typography:

Font family: Inter (sans-serif)

All text colors: white/80 opacity for body text, full white for headings and hover states

Technical Stack:

React + TypeScript

Vite

Tailwind CSS

Framer Motion for animations

Lucide React for icons

Responsive Breakpoints:

Mobile-first design

sm: 640px

md: 768px

lg: 1024px

xl: 1280px

Key CSS Details:

Container max-width: max-w-7xl with centered margins

Section height: h-screen

Video: absolute positioning, inset-0, object-cover

Content: relative z-10 positioning to appear above video

Smooth transitions on all interactive elements

Create the complete implementation including the ShinyText component with proper framer-motion animation logic.
```

---

## 27. Nexora Automation

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `nexora-hero`

```
Create a SaaS landing page hero section with the following exact specifications:

Page Layout

The entire page is h-screen flex flex-col bg-background overflow-hidden — the Navbar + Hero fill exactly 100vh with no scroll.
The page uses two Google Fonts imported via CSS: Instrument Serif (display/headings, including italic) and Inter (body text).
Fonts & Design Tokens (index.css)

Import fonts:

@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap');
CSS variables (:root):

--background: 0 0% 100% (white)
--foreground: 210 14% 17% (dark charcoal)
--primary: 210 14% 17% / --primary-foreground: 0 0% 100%
--secondary: 0 0% 96% / --secondary-foreground: 0 0% 9%
--muted: 0 0% 96% / --muted-foreground: 184 5% 55%
--accent: 239 84% 67% (indigo/blue) / --accent-foreground: 0 0% 100%
--border: 0 0% 90%
--ring: 239 84% 67%
--radius: 0.5rem
--font-display: 'Instrument Serif', serif
--font-body: 'Inter', sans-serif
--shadow-dashboard: 0 25px 80px -12px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.06)
Tailwind config extends fontFamily with display and body mapped to the CSS vars. All colors use hsl(var(--token)) pattern.

Navbar

flex items-center justify-between px-6 md:px-12 lg:px-20 py-5 font-body
Left: Logo text ✦ Nexora — text-xl font-semibold tracking-tight text-foreground
Right (hidden on mobile): Nav links "Home", "Pricing", "About", "Contact" — text-sm text-muted-foreground hover:text-foreground with gap-8
CTA button: rounded-full px-5 text-sm font-medium using primary styling
Hero Section




Background Video: Fullscreen muted autoplay loop video, absolute inset-0 w-full h-full object-cover z-0
Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260319_015952_e1deeb12-8fb7-4071-a42a-60779fc64ab6.mp4
All content wrapped in relative z-10 flex flex-col items-center w-full
1. Badge (top)

Framer Motion: fade up from y:10, duration 0.5s
inline-flex items-center gap-1.5 rounded-full border border-border bg-background px-4 py-1.5 text-sm text-muted-foreground font-body
Text: "Now with GPT-5 support ✨"
mb-6
2. Headline

Framer Motion: fade up from y:16, duration 0.6s, delay 0.1s
text-center font-display text-5xl md:text-6xl lg:text-[5rem] leading-[0.95] tracking-tight text-foreground max-w-xl
Content: The Future of Smarter Automation — the word "Smarter" renders in Instrument Serif italic
3. Subheadline

Framer Motion: fade up from y:16, duration 0.6s, delay 0.2s
mt-4 text-center text-base md:text-lg text-muted-foreground max-w-[650px] leading-relaxed font-body
Text: "Automate your busywork with intelligent agents that learn, adapt, and execute—so your team can focus on what matters most."
4. CTA Buttons

Framer Motion: fade up from y:16, duration 0.6s, delay 0.3s
mt-5 flex items-center gap-3
Primary button: rounded-full px-6 py-5 text-sm font-medium font-body — text "Book a demo"
Play button: ghost variant, h-11 w-11 rounded-full border-0 bg-background shadow-[0_2px_12px_rgba(0,0,0,0.08)] hover:bg-background/80 with a Play icon (lucide) h-4 w-4 fill-foreground
5. Dashboard Preview (custom coded, NOT an image)

Framer Motion: fade up from y:30, duration 0.8s, delay 0.5s
Container: mt-8 w-full max-w-5xl
Frosted glass wrapper: rounded-2xl overflow-hidden p-3 md:p-4 with inline styles:
background: rgba(255, 255, 255, 0.4)
border: 1px solid rgba(255, 255, 255, 0.5)
boxShadow: var(--shadow-dashboard)
Dashboard internals (all coded in React, text-[11px], select-none pointer-events-none):

Top bar: Logo "N" in rounded box + "Nexora" + chevron | Search bar with ⌘K shortcut | "Move Money" + bell + avatar "JB"
Sidebar (w-40): Items — Home (active), Tasks (badge "10"), Transactions, Payments (chevron), Cards, Capital, Accounts (chevron). Section "Workflows": Trake rutes, Payments, Notifications, Settings
Main content (bg-secondary/30):
Greeting: "Welcome, Jane" — text-sm font-semibold
Action buttons row: Send (primary/accent), Request, Transfer, Deposit, Pay Bill, Create Invoice — rounded-full pill buttons text-[10px], + "Customize" text
Two equal-width cards (flex-1 basis-0) side by side:
Balance card: "Mercury Balance" with checkmark, amount $8,450,190.32 (cents in text-xs text-muted-foreground), stats (Last 30 Days, +$1.8M green, -$900K red), SVG area chart (h-20) with smooth cubic Bézier curve, linear gradient fill from accent at 15% opacity to transparent, stroke in accent color strokeWidth="1.5"
Accounts card: Header "Accounts" with + and ⋮ icons. Three rows (py-3, no dividers, text-xs, justify-between): Credit $98,125.50, Treasury $6,750,200.00, Operations $1,592,864.82
Transactions table: "Recent Transactions" heading, table with columns Date/Description/Amount/Status. 4 rows: AWS -$5,200 Pending (amber), Client Payment +$125,000 Completed (green), Payroll -$85,450 Completed, Office Supplies -$1,200 Completed
Dependencies

framer-motion for all animations
lucide-react for all icons
shadcn/ui Button component
Tailwind CSS with tailwindcss-animate plugin
Key Design Decisions

The dashboard overflows toward the bottom of the viewport and is clipped by overflow-hidden on the parent
No dark mode — light only
All colors use semantic Tailwind tokens, never raw color values in components
The SVG chart uses a hand-crafted cubic Bézier path, not a charting library
```

---

## 28. Transform Data

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `transform-data-hero`

```
HERO SECTION CREATION PROMPT

Create a modern hero section with a looping video background and the following specifications:

Video Background:

URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260329_050842_be71947f-f16e-4a14-810c-06e83d23ddb5.mp4

Size: 115% width and height

Position: Centered horizontally, anchored to top with object-top focal point

Custom JavaScript fade system (NO CSS transitions):

250ms requestAnimationFrame-based fade-in on load/loop start

250ms fade-out when 0.55 seconds remain before video end

fadingOutRef boolean prevents re-triggering fade-out from repeated timeUpdate events

On ended: opacity set to 0, 100ms delay, reset to currentTime = 0, play, fade back in

Each new fade cancels running animation frames to prevent competing animations

Fades resume from current opacity (no snapping)

Fonts Required:

Schibsted Grotesk (weights: 400, 500, 600, 700)

Inter (weights: 400, 500, 600, 700)

Noto Sans (weights: 400, 500, 600, 700)

Fustat (weights: 400, 500, 600, 700)

Navigation Bar:

Logo: "Logoipsum" (Schibsted Grotesk SemiBold, 24px, -1.44px tracking)

Menu items (Schibsted Grotesk Medium, 16px, -0.2px tracking):

Platform

Features (with dropdown chevron icon)

Projects

Community

Contact

Right side buttons:

"Sign Up" (transparent background, 82px width)

"Log In" (black background, white text, 101px width)

Padding: 120px horizontal, 16px vertical

Hero Content (moved up 50px with -mt-[50px]):

Badge Component:

Dark badge with star icon + "New" text

Light background with text: "Discover what's possible"

Font: Inter Regular, 14px

Rounded corners with subtle shadow

Main Headline:

Text: "Transform Data Quickly"

Font: Fustat Bold, 80px, -4.8px tracking, line-height: none

Color: Black, center-aligned

Subtitle:

Text: "Upload your information and get powerful insights right away. Work smarter and achieve goals effortlessly."

Font: Fustat Medium, 20px, -0.4px tracking

Color: #505050

Max-width: 736px, width: 542px

Search Input Box:

Backdrop blur with dark transparent background (rgba(0,0,0,0.24))

Dimensions: 728px max-width, 200px height, rounded 18px

Top row: Credit info

Left: "60/450 credits" with green "Upgrade" button

Right: AI icon + "Powered by GPT-4o"

Font: Schibsted Grotesk Medium, 12px, white text

Main input area:

White background, rounded 12px, shadow

Placeholder: "Type question..." (16px, rgba(0,0,0,0.6))

Black circular submit button with up arrow icon (36px size)

Bottom row:

Left: Three action buttons (gray backgrounds, rounded 6px):

"Attach" with paperclip icon

"Voice" with microphone icon

"Prompts" with search icon

Right: Character counter "0/3,000" (12px, gray)

Icons (SVG paths from imported file):

Chevron down arrow

Up arrow

Star icon

AI sparkle icon

Attach/paperclip icon

Voice/microphone icon

Search icon

Spacing:

Gap between navigation and hero: 60px

Gap between header and search box: 44px

Gap within header elements: 34px (badge to title, title to subtitle)

Hero content moved up: 50px negative margin

Horizontal padding: 120px

Color Scheme:

Black text: #000000

Gray text: #505050

Light gray backgrounds: #f8f8f8

Green upgrade button: rgba(90,225,76,0.89)

Dark badge: #0e1311

White: #ffffff

Transparent overlay: rgba(0,0,0,0.24)

Component Structure:

VideoBackground component with custom fade logic

Navigation bar (fixed spacing, horizontal layout)

Hero content container (centered, max-width constraints)

Nested components for badge, header, and search input

All elements positioned over full-screen video background
```

---

## 29. Glow Features

- **Category**: Features Section
- **Type**: features
- **Page Type**: hero
- **ID**: `glow-features`

```
Create a React web application using Vite and Tailwind CSS v4 that perfectly replicates a dark-themed glowing feature card section.

**Libraries Required:**
- React 19, Vite, Tailwind CSS v4
- `lucide-react` for icons
- `motion/react` (Framer Motion) for animations

**Global Page Layout:**
- Set the main wrapper to `min-h-screen bg-[#0A0A0B] flex flex-col items-center justify-center p-6 md:p-12 font-sans`.
- Create a CSS grid to hold the cards: `grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-3 lg:gap-3 w-full max-w-[936px]`.

**The Feature Card Component Requirements:**
- Build a reusable `<FeatureCard />` component taking `title`, `description`, `icon`, `gradient`, and `delay` props.
- Wrap the entire card in a `<motion.div>`.
- Card size restrictions wrapper: `relative flex flex-col justify-start items-start w-full max-w-[260px] md:max-w-[300px] group mx-auto`.
- **Glow Background (Crucial):** Create an absolute positioned `div` behind the card content with `w-full h-[260px] md:h-[300px] opacity-60 rounded-[40px] pointer-events-none`. Apply inline styles: `background: gradient` and `filter: "blur(45px)"`.
- **Foreground Card with Gradient Border (Crucial):** On top of the glow, create a relative container with `self-stretch h-[260px] md:h-[300px] rounded-[40px] z-10 overflow-hidden`.
- Apply an 8px solid transparent border to this foreground card.
- Use the background-clip technique strictly for the border gradient via inline styles:
  `background: linear-gradient(#1A1A1C, #1A1A1C) padding-box, ${gradient} border-box;`
- Content Inner Layout: Inside the foreground, use `w-full h-full p-7 flex flex-col justify-between`.
- Icons should have `size={32}` and `strokeWidth={2.5}`, wrapped in a `text-white/90` div.
- Titles: `text-white font-medium text-xl mb-3 tracking-tight`.
- Descriptions: `text-gray-400 text-[14px] leading-[1.6] font-normal selection:bg-white/20`.

**Animations (Framer Motion):**
- The main `<motion.div>` wrapper should animate as follows:
  - Initial state: `{ opacity: 0, y: 30 }`
  - Animate state: `{ opacity: 1, y: 0 }`
  - Transition: `{ duration: 0.8, ease: "easeOut", delay }`

**Data for the 3 Cards:**
Instantiate three of these cards inside the main grid with the following exact data:

1. **Card 1 ("Hardware"):** 
   - Icon: `<Monitor />` from lucide-react. 
   - Delay: `0.1`
   - Description: "My entire desktop setup is built for power. It is silent, durable, and holds my focus."
   - Gradient: `linear-gradient(137deg, #FF3D77 0%, #FFB1CE 45%, #FF9D3C 100%)`

2. **Card 2 ("Studio"):** 
   - Icon: `<Palette />` from lucide-react. 
   - Delay: `0.2`
   - Description: "Studio is where I define every single pixel. It is the hub for each canvas I deliver."
   - Gradient: `linear-gradient(137deg, #FFFFFF 0%, #7DD3FC 45%, #06B6D4 100%)`

3. **Card 3 ("Motion"):** 
   - Icon: `<Zap />` from lucide-react. 
   - Delay: `0.3`
   - Description: "I use Motion to build lively prototypes, bridging the gap between views and code."
   - Gradient: `linear-gradient(137deg, #4361EE 0%, #E0AEFF 45%, #F72585 100%)`
```

---

## 30. Lumina

- **Category**: Footer Section
- **Type**: footer
- **Page Type**: hero
- **ID**: `lumina-footer`

```
Create a React frontend using Tailwind CSS v4, the `motion/react` library for animations, and `lucide-react` for icons. I want to build a page with an immersive video background and a highly stylized "liquid glass" footer.

Please follow these exact specifications:

1. Global CSS & Fonts (`index.css`):
Add the following exact `@font-face` to the CSS file and set it as the root Tailwind `--font-sans`:
@font-face {
    font-family: "Helvetica Regular";
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot");
    src: url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.eot?#iefix")format("embedded-opentype"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff2")format("woff2"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.woff")format("woff"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.ttf")format("truetype"),
    url("https://db.onlinewebfonts.com/t/a64ff11d2c24584c767f6257e880dc65.svg#Helvetica Regular")format("svg");
}

2. The "Liquid Glass" CSS:
Add this exact custom CSS for the liquid glass effect bordering:
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

3. Main App Structure (`App.tsx`):
- Wrap the page in a `<main>` with `relative w-full min-h-[115vh] overflow-x-hidden flex flex-col items-center font-sans selection:bg-white/20 selection:text-white`.
- Add a `<video>` element fixed to the background (`fixed inset-0 w-full h-full object-cover z-[0]`) that auto-plays, loops, and is muted.
- The `src` for the video must be exactly this CloudFront URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260429_114316_1c7889ad-2885-410e-b493-98119fee0ddb.mp4`

4. Content Wrapper:
On top of the video (`z-10`), add a `max-w-7xl` container that holds an upper CTA (you can use a placeholder for the CTA) and pushes the footer to the bottom.

5. The Footer (`motion.footer`):
- Start it with these exact Framer Motion props: `initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, delay: 0.4, ease: "easeOut" }}`
- Give it the classes: `liquid-glass w-full rounded-3xl p-6 md:p-10 text-white/70 mt-32 md:mt-64`.

6. Footer Layout - Top Grid:
- A 12-column grid (`grid-cols-1 md:grid-cols-12 gap-10 md:gap-12 mb-10`).
- First column (md:col-span-5): 
  - An SVG Logo `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 256 256" fill="currentColor"><path d="M 4.688 136 C 68.373 136 120 187.627 120 251.312 C 120 252.883 119.967 254.445 119.905 256 L 0 256 L 0 136.096 C 1.555 136.034 3.117 136 4.688 136 Z M 251.312 136 C 252.883 136 254.445 136.034 256 136.096 L 256 256 L 136.095 256 C 136.032 254.438 136.001 252.875 136 251.312 C 136 187.627 187.627 136 251.312 136 Z M 119.905 0 C 119.967 1.555 120 3.117 120 4.688 C 120 68.373 68.373 120 4.687 120 C 3.117 120 1.555 119.967 0 119.905 L 0 0 Z M 256 119.905 C 254.445 119.967 252.883 120 251.312 120 C 187.627 120 136 68.373 136 4.687 C 136 3.117 136.033 1.555 136.095 0 L 256 0 Z" /></svg>` along with the text "LUMINA" (text-xl font-medium).
  - A description below it: "Lumina provides premium clarity on global events and cosmic wonders - shared with all for free." (`text-sm leading-relaxed max-w-sm`).

7. Footer Layout - Links Section (md:col-span-7):
Make a 3-column grid containing these lists:
- Discover: Labs & Workshops, Deep Dive Series, Global Circle, Resource Vault, Future Roadmap
- The Mission: Origin Story, The Collective, Newsroom Hub, Join the Team
- Concierge: Get in Touch, Legal Privacy, User Agreement, Report Concern
(Headers should be `text-sm uppercase tracking-wider text-white font-medium mb-4` and links `text-xs space-y-2 hover:text-white transition-colors`).

8. Footer Layout - Bottom Bar:
- Create a bottom border (`pt-6 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-6 md:gap-4`).
- Left side: `<p className="text-[10px] uppercase tracking-widest opacity-50">Curated by @GotInGeorgiG</p>`
- Right side: A label `<span className="text-[10px] uppercase tracking-widest opacity-50">Join the Journey:</span>` alongside a horizontal flex row of `lucide-react` icons (sizes 16): Music2, Facebook, Twitter, Youtube, and Instagram. Wrap each in an `<a>` with `opacity-70 hover:opacity-100 transition-colors hover:text-white`.
```

---

## 31. USD Halo

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: landing
- **ID**: `halo-usd-landing`

```
Build a premium, fintech-style landing page for a stablecoin product called "Halo / USD Halo" using React + TypeScript + Vite + Tailwind CSS, with lucide-react for icons. No other UI libraries. Background color of the page is #F5F5F5.

Global Setup
Use TT Norms Pro as the primary font, loaded via @font-face from /fonts/tt-norms-pro-regular.woff2 (weight 400) and /fonts/tt-norms-pro-semibold.woff2 (weight 600), with font-display: swap. Apply it to html, body, and inherit on *.
Tailwind base + components + utilities at the top of src/index.css.
Page wrapper: flex flex-col bg-[#F5F5F5]. The first section (Navbar + Hero) is wrapped in a h-screen flex flex-col overflow-hidden container.
Inner content max width across sections: max-w-[88rem] mx-auto.
Custom Logo Icon
Create an SVG component LogoIcon using currentColor, viewBox 0 0 256 256, with this path (a stylized "halo" mark made of two interlocking rounded squares):


M 128.005 191.173 C 128.448 156.208 156.93 128 192 128 L 192 64 L 128 64 C 128 99.346 99.346 128 64 128 L 64 192 L 128 192 Z M 192 256 L 64 256 C 28.654 256 0 227.346 0 192 L 0 64 L 64 64 L 64 0 L 192 0 C 227.346 0 256 28.654 256 64 L 256 192 L 192 192 Z
1. Navbar (absolute, transparent over hero)
nav is absolute top-0 left-0 right-0 z-20 px-6 py-5.
Inner row: flex items-center justify-between.
Left: LogoIcon (w-7 h-7, black) + word "Halo" (text-2xl font-medium tracking-tight text-black).
Center (hidden below md): links Network · Ecosystem · Rewards · Help · News, gap-8, text-base text-gray-700 hover:text-black font-medium transition-colors duration-200.
Right: black pill button "Open Wallet" — bg-black text-white text-base font-medium px-7 py-2.5 rounded-full hover:bg-gray-800 transition-colors duration-200.
2. Hero Section
Outer: flex-1 px-6 pt-20 pb-6 flex items-end.
Inner card: relative w-full rounded-2xl overflow-hidden, inline style height: calc(100vh - 96px).
Background video (autoplay, muted, loop, playsInline, object-cover absolute inset-0 w-full h-full): 
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_161253_c72b1869-400f-45ed-ac0c-52f68c2ed5bd.mp4

Content overlay: relative z-10 flex flex-col items-start justify-start h-full p-12 pt-36.
h1: "Your Wealth\nWorks" (with <br/>) — text-black text-5xl md:text-6xl font-medium leading-tight max-w-xl mb-4, inline letterSpacing: '-0.04em'.
p: "An automated, reward-powered digital dollar built for native passive earnings and effortless connection into DeFi." — text-black/70 text-base md:text-lg max-w-md mb-8 leading-relaxed, inline fontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif".
Pill button "Join us" with arrow circle: inline-flex items-center gap-3 bg-black text-white text-base md:text-lg font-medium pl-8 pr-2 py-2 rounded-full hover:bg-gray-800. Trailing arrow inside bg-white rounded-full p-2, using ArrowRight w-5 h-5 text-black from lucide-react.
Followed by the Brand Marquee below.
Brand Marquee (inside hero, below button)
Container: mt-24 w-full max-w-md overflow-hidden.
Inject scoped <style> with keyframes marquee translating 0 → -50%, applied to .marquee-track { display:flex; width:max-content; animation: marquee 22s linear infinite; }.
Render the brand list twice (so it loops seamlessly).
Each item: mx-7 shrink-0 text-black/60 whitespace-nowrap with these inline styles:
Stripe — Georgia serif, weight 700, letterSpacing -0.02em, fontSize 15px
Coinbase — Arial sans, weight 900, letterSpacing 0.08em, fontSize 13px, uppercase
Uniswap — Trebuchet MS, weight 600, letterSpacing 0.01em, fontSize 15px, italic
Aave — Courier New monospace, weight 700, letterSpacing 0.12em, fontSize 13px, uppercase
Compound — Palatino, Book Antiqua, weight 400, letterSpacing -0.01em, fontSize 16px
MakerDAO — Impact, Arial Narrow, weight 400, letterSpacing 0.04em, fontSize 14px
Chainlink — Verdana, weight 700, letterSpacing -0.03em, fontSize 13px
3. Info Section ("Meet USD Halo.")
section bg-[#F5F5F5] px-6 py-24.
Row 1: 2-col grid (grid-cols-1 md:grid-cols-2 gap-12 mb-16 items-start).
Left: h2 "Meet USD Halo." — text-black text-4xl md:text-5xl font-medium leading-tight mb-8, letterSpacing -0.03em. Below it, black pill "Discover it" button with white arrow circle (same pattern as "Join us" but text-base).
Right: paragraph "USD Halo is a reward-earning dollar coin that lets your savings grow while remaining tied to the U.S. dollar." — text-black/70 text-2xl md:text-3xl leading-relaxed.
Row 2 — 4-col card grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4):
Card 1 (spans 2 cols on lg): rounded-2xl with background image: 
https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260423_164207_f243351d-ed59-48ec-83a0-a5e996bdbe3c.png&w=1280&q=85

 backgroundSize: cover; backgroundPosition: center. Inside: p-7 min-h-80 flex flex-col justify-between. Title (top): "Savings that bloom" — text-black text-2xl font-medium leading-snug letterSpacing -0.02em. Body (bottom): "Gain steady returns as your dollar tokens are routed into top-performing DeFi strategies." — text-black/70 text-base max-w-xs.
Card 2: solid #2B2644, rounded-2xl, p-7, min-h-80, flex-col-justify-between. White heading "Always fluid,\nalways pegged." text-2xl font-medium, body "Keep fully dollar-anchored with on-demand access to funds — no lockups or waits." text-white/60 text-base.
Card 3: same #2B2644 styling. Heading "Fully\nautomated". Body "Skip the task of tuning positions yourself. USD Halo runs in the background for you."
4. Backed By Section (marquee row)
section bg-[#F5F5F5] px-6 with inner max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 items-center.
Left col (1/4): text-black/70 text-base leading-relaxed — "Funded by premier partners\nand forward-thinking leaders."
Right col (3/4): infinite marquee (same pattern as hero marquee but 30s linear infinite, class .backers-track, keyframes backers-marquee). Items use mx-10 shrink-0 text-black/50 whitespace-nowrap with these inline styles:
Fundamental Labs — Times New Roman serif, 400, ls 0.02em, 14px
KUCOIN — Arial Black, 900, ls 0.08em, 16px
NGC — Impact, 700, ls 0.05em, 18px
NxGen — Georgia, 600, ls -0.02em, 17px
Matter Labs — Helvetica, 700, ls -0.01em, 15px
DEXTools — Verdana, 700, ls 0.06em, 14px, uppercase
NGRAVE — Courier New, 700, ls 0.18em, 14px
Polychain — Palatino, 500, ls 0.03em, 15px
Render brands twice for the loop.
5. Use Cases Section
section bg-[#F5F5F5] px-6 py-24. Inner: 2-col grid grid-cols-1 md:grid-cols-2 gap-8 items-start.
Left column (md:pr-12 md:pt-2):
Eyebrow: "USD Halo in Practice" — text-black/60 text-sm mb-2.
h2 "Use modes" — text-5xl md:text-6xl font-medium leading-none mb-6, ls -0.04em.
Paragraph: "USD Halo powers a wide range of modes for builders, companies and treasuries wanting safe and rewarding stablecoin integrations plus more" — text-black/60 text-base leading-relaxed max-w-sm.
Right column: large relative rounded-3xl overflow-hidden min-h-[720px] with background video (autoplay/muted/loop/playsInline, object-cover absolute inset-0): 
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_183428_ab5e672a-f608-4dcb-b319-f3e040f02e2d.mp4

Overlay content relative z-10 p-10 md:p-12:
h3 "Commerce" — text-4xl md:text-5xl font-medium leading-tight mb-5, ls -0.03em.
Paragraph: "Lift customer retention by offering USD Halo, a trusted dollar-backed stablecoin with strong yields, letting your patrons earn with zero effort on your platform." — text-black/70 text-base max-w-md mb-8.
Inline-flex link "Know more" with leading circular icon: w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center group-hover:bg-white transition-colors containing ArrowRight w-4 h-4 text-black.
Animations & Interactions
Two CSS keyframe marquees (22s for hero brands, 30s for backers), both translating 0 → -50% on a duplicated track for seamless looping.
All buttons use transition-colors duration-200 with hover state hover:bg-gray-800 (or hover:bg-white for the white circle).
Nav links transition on hover from text-gray-700 to text-black.
Videos autoplay muted with playsInline for mobile compatibility.
Composition
App renders, in order:

h-screen overflow-hidden wrapper containing Navbar (absolute) + HeroSection.
InfoSection
BackedBySection
UseCasesSection
All section backgrounds are #F5F5F5. All headings use negative letter-spacing for the tight, modern fintech feel. Use font-medium (600) as the heaviest weight throughout.
```

---

## 32. Taskly

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `taskly-hero`

```
System Prompt: High-Fidelity "Liquid Glass" Hero Section

Core Layout: Create a 1600px max-width landing page hero section. The background should be pure white with a subtle, layered gradient glow in the top-left (using blurred ellipses in light blue #60B1FF and #319AFF). The design must be fully responsive, transitioning from a single-column mobile view to a dual-column desktop layout.

Typography:

Headlines & Brand: Use Fustat (Bold).
Body & UI: Use Inter (Normal/Medium).
Hero Headline: "Work smarter, achieve faster" (75px, 1.05 line-height, -2px tracking).

The "Strong Liquid Glass" Navbar:

Position: Sticky at top-[30px], centered, w-fit.
Visuals: backdrop-blur-[50px], background rgba(255,255,255,0.3), rounded-[16px].
Fidelity Details:
Outer Stroke: 1px solid rgba(0,0,0,0.1).
Inner Highlight Shadow: inset 0px 4px 4px 0px rgba(255,255,255,0.25).
Items: Logo "Taskly" (Fustat), Nav links (Home, Features, Company, Pricing), and a glassy "SignUp" button with an arrow icon.

The Glassy Orb (Hero Right):

Source URL: https://future.co/images/homepage/glassy-orb/orb-purple.webm
Blending Mode: Must use mix-blend-screen to filter the black background.
Scaling: scale-125 to make it massive and bleed slightly off-center.
Exact Color Grade (CSS Filter): hue-rotate(-55deg) saturate(250%) brightness(1.2) contrast(1.1). This transforms the purple asset into a vibrant, high-end "Electric Brand Blue" that matches the primary CTA.

Hero Content (Hero Left):

Social Proof: A "Rated 4.9/5 by 2700+ customers" badge with five orange #FF801E stars.
Subheadline: "Effortlessly manage your projects, collaborate with your team, and achieve your goals with our intuitive task management tool." (18px, Inter, -1px tracking).
Primary CTA: "Get Started Now" button.
Color: rgba(0,132,255,0.8) with backdrop-blur-[2px].
Details: rounded-[16px], white text, inner highlight shadow inset 0px 4px 4px 0px rgba(255,255,255,0.35), and a white circular arrow icon.
Animation: Scale 1.02 on hover with a smooth transition.

Footer Logos: Include a "Trusted by Top-tier product companies" section at the bottom with 5 grayscale SVG logos (e.g., placeholder logos for tech companies) spaced at gap-[100px].

Key Technical Specs for the Developer:

Video Tag: autoPlay loop muted playsInline.
Container: Use a relative wrapper for the background glow and a z-10 main container for the content.
Smoothing: Apply -webkit-font-smoothing: antialiased for the sharpest typography.
```

---

## 33. Stellar AI

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `stellar-ai-hero`

```
Create a "Stellar.ai" landing page hero section using React, Tailwind CSS, and Lucide React icons. Use the Inter font (imported from Google Fonts). The page has a white background (bg-white), max-width max-w-7xl, and is centered with mx-auto.

Font: Import Inter (weights 400, 500, 600, 700) from Google Fonts. Set font-family: 'Inter', sans-serif on the body.

Custom CSS animations (in index.css):

@keyframes fadeInUp -- from opacity: 0; transform: translateY(30px) to opacity: 1; transform: translateY(0). Class .animate-fade-in-up uses this with 0.6s ease-out forwards.
@keyframes fadeInOverlay -- from opacity: 0 to opacity: 1. Class .animate-fade-in-overlay uses this with 0.4s ease-out forwards.
@keyframes fadeInDialog -- from opacity: 0 to opacity: 1. Class .animate-slide-up-overlay uses this with 0.5s ease-out forwards and has transform: translate(-50%, -50%).
Every major section uses .animate-fade-in-up with staggered animationDelay inline styles (starting at 0.1s and incrementing by 0.1s). Each element starts with opacity: 0 inline so the animation fills it to visible.

Tailwind config: Default config with no custom theme extensions. Uses standard content paths.

NAVIGATION (animationDelay: 0.1s):
px-6 py-4 flex items-center justify-between max-w-7xl mx-auto
Left: Lucide Star icon (w-5 h-5, fill-black) + "Stellar.ai" text (text-lg font-semibold)
Center (hidden on mobile, hidden md:flex items-center gap-8): "Solutions" with ChevronDown, "For Teams" with ChevronDown, "About Us", "Learn Hub" -- all text-sm text-gray-700 hover:text-black
Right: "Login" link (text-sm text-gray-700) + "Get started free" button (bg-black text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors)

HERO SECTION (px-6 pt-24 pb-32 max-w-7xl mx-auto text-center):
Reviews Badge (delay: 0.2s): inline-flex items-center gap-2 mb-8. Contains a bordered square (w-6 h-6 border border-gray-300 rounded) with a filled Star icon inside, plus "4.9 rating from 18.3K+ users" (text-sm font-medium text-black).

Main Heading (delay: 0.3s): text-6xl md:text-7xl lg:text-[80px] font-normal leading-[1.1] tracking-tight mb-5. First line: "Work Smarter. Move Faster." Second line: "AI Powers You Up." with gradient text (bg-gradient-to-r from-black via-gray-500 to-gray-400 bg-clip-text text-transparent).

Subheading (delay: 0.4s): text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto. Text: "Intelligent automation syncs with the tools you love to streamline tasks, boost output, and save time."

CTA Button (delay: 0.5s): bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors mb-12. Text: "Begin Free Trial".

Tab Bar (delay: 0.6s): Centered bg-gray-100 rounded-lg p-1 container.
Mobile (md:hidden): 2x2 grid with 4 buttons: Analyse (BarChart3), Train (BookOpen), Testing (Users), Deploy (Rocket). Active: bg-white text-black shadow-sm. Inactive: text-gray-600.
Desktop (hidden md:flex): Same 4 buttons in row with vertical dividers (w-px h-5 bg-gray-300).
Tabs auto-cycle every 4s using setInterval. State: useState('analyse').

Video + Overlay Section (delay: 0.7s):
Container: relative rounded-3xl overflow-hidden h-[400px] md:h-[500px]
Video: src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260319_165750_358b1e72-c921-48b7-aaac-f200994f32fb.mp4", autoPlay, loop, muted, playsInline, w-full h-full object-cover.

4 Conditional Overlays per tab with animate-fade-in-overlay outer and animate-slide-up-overlay inner card:
a. Analyse: "Set Up Your AI Workspace" wizard with purple progress bar at 25%, 4 steps
b. Train: "AI Model Training" with orange progress at 67%, 4 metrics
c. Testing: "Test Suite Results" with green success, 127/127 tests
d. Deploy: "Deploy to Production" with 4 checklist items, Deploy Now button

Company Logos (delay: 0.8s): mt-24 flex with INTERSCOPE, SPOTIFY, Nexera (dot grid), M3 (serif italic), LAURA COLE (LC circle), vertex (dots)
```

---

## 34. Datacore Booking

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `datacore-booking-hero`

```
Create a responsive, full-screen hero section for a web application using React and Tailwind CSS.

Design System & Assets:

Fonts: Load and use 'Manrope' (for UI/Nav), 'Cabin' (for buttons/tags), 'Instrument Serif' (for headlines), and 'Inter' (for body text).

Primary Color: Purple #7b39fc
Secondary/Dark Color: Dark Purple #2b2344
Background: Use a full-screen, absolute-positioned HTML5 video background. The video should autoplay, loop, mute, and play inline. Ensure it covers the viewport (min-h-screen, object-cover) without an overlay (keep it opaque).

Video URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260210_031346_d87182fb-b0af-4273-84d1-c6fd17d6bf0f.mp4

1. Navbar Component (Top Overlay)

Layout: Full width, transparent background, z-20 relative positioning.
Padding: px-6 (mobile) to px-[120px] (desktop), py-[16px].

Logo (Left): Use this specific SVG path filled with white:
Path: M1.04356 6.35771L13.6437 0.666504... (Future logo shape).

Navigation Links (Center-Left, Desktop Only):
Items: "Home", "Services" (with a ChevronDown icon), "Reviews", "Contact us".
Style: Manrope font, Medium weight, 14px size, White.
Hover effect: opacity-80.

Action Buttons (Right, Desktop Only):
Sign In: White background, thin gray border (#d4d4d4), rounded 8px, Black text (#171717), Manrope Semibold 14px.
Get Started: Primary Purple background (#7b39fc), rounded 8px, White text (#fafafa), Manrope Semibold 14px, subtle shadow.

Mobile: Hide links/buttons and show a White Menu icon (hamburger) that toggles a full-screen black overlay menu.

2. Hero Content (Centered)

Container: Centered vertically and horizontally (flex-col items-center text-center), z-10 relative, top margin mt-32.

Tagline Pill:
Style: Glassmorphism effect (bg-[rgba(85,80,110,0.4)], backdrop-blur, border rgba(164,132,215,0.5)).
Shape: Rounded 10px, Height 38px.
Content: A small inner badge (#7b39fc bg, rounded 6px) saying "New" followed by text "Say Hello to Datacore v3.2".
Font: Cabin, Medium, 14px, White.

Headline:
Text: "Book your perfect stay instantly and hassle-free".
Typography: Instrument Serif font, White.
Size: 5xl (mobile) to 96px (desktop).
Styling: Line-height 1.1. The word "and" should be italicized with specific spacing.

Subtext:
Text: "Discover handpicked hotels, resorts, and stays across your favorite destinations. Enjoy exclusive deals, fast booking, and 24/7 support."
Typography: Inter font, Normal weight, 18px.
Color: White with 70% opacity (text-white/70).
Width: Max width 662px.

Call to Action Buttons (Row):
Button 1: "Book a Free Demo" — Primary Purple (#7b39fc), rounded 10px, Cabin Medium 16px, White.
Button 2: "Get Started Now" — Dark Purple (#2b2344), rounded 10px, Cabin Medium 16px, Off-white (#f6f7f9).
Hover effects: Slightly lighten backgrounds on hover.
```

---

## 35. SAAS Software

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `convix-software-hero`

```
Build a fully responsive, full-viewport hero section for a PR-agency SaaS called "Convix Software" with these exact specs:

Page Frame
Outer wrapper: min-h-screen w-full bg-[#ededed] p-3 sm:p-4, font-family Inter
Hero container (clips everything inside): relative w-full h-[calc(100vh-24px)] sm:h-[calc(100vh-32px)] overflow-hidden bg-[#d9d9d9] rounded-2xl sm:rounded-3xl
Background Video
URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260424_064411_9e9d7f84-9277-41f4-ab10-59172d89e6be.mp4
Absolutely positioned, inset-0 w-full h-full object-cover pointer-events-none
Attributes: autoPlay, loop, muted, playsInline, preload="auto", disableRemotePlayback, webkit-playsinline="true", x5-playsinline="true"
Poster fallback: https://images.unsplash.com/photo-1557683316-973673baf926?w=1600&q=60
Above the video: absolute inset-0 bg-white/10 overlay
Foreground content wrapper: relative z-10
Fonts (/src/styles/fonts.css)
Import from Google Fonts:

Inter weights 400, 500, 600, 700
Instrument Serif regular + italic
Navbar (floating pill, responsive with hamburger)
Wrapper: flex justify-center pt-4 sm:pt-6 px-3 sm:px-4
Pill: bg-white rounded-full shadow-sm border border-neutral-200 pl-2 pr-2 py-2 w-full max-w-[760px] relative
Logo (left, shrink-0): orange #ef4d23 8-petal flower SVG — 8 circles at radius 10 around center (16,16) plus center circle, all r=3.5, viewBox 32×32, rendered w-7 h-7 sm:w-8 sm:h-8
Desktop links (hidden md:flex, gap-6, 14px): "Home" (with 1.5px black dot), "Features", "About", "Pages" (#ef4d23 + ChevronDown 3.5)
Right cluster (ml-auto): ShoppingCart icon (hidden on mobile), then orange #ef4d23 rounded-full button "Get early access" (desktop) / "Early access" (mobile) with white/20 inner circle holding ChevronRight
Mobile-only Menu (lucide) hamburger button (md:hidden)
When open: dropdown panel absolute top-full left-2 right-2 mt-2 bg-white rounded-2xl shadow-lg border border-neutral-200 p-3 z-20 listing the same nav items vertically
useState open toggles the menu
Hero Content (centered)
flex flex-col items-center px-4 pt-10 sm:pt-16 pb-8 sm:pb-12 text-center
Badge: inline-flex items-center gap-2 bg-white rounded-full px-4 py-1.5 shadow-sm, 13px — orange dot + "Convix Software"
Headline <h1> with inline style fontSize: clamp(36px, 8vw, 72px); lineHeight: 1.05; fontWeight: 500; letterSpacing: -0.02em, mt-5 sm:mt-6 max-w-4xl:
"Shaping " + <span style={{fontFamily:"'Instrument Serif', serif", fontStyle:"italic", fontWeight:400}}>Agencies</span> + <br> + "of tomorrow"
Subtitle <p> mt-4 sm:mt-6 text-neutral-700 px-2, fontSize: clamp(13px, 3.5vw, 16px): "The All-In-One Software Powering the Future of PR Agencies"
CTA button mt-6 sm:mt-8 inline-flex items-center gap-3 bg-[#0b0f1a] text-white rounded-full pl-6 sm:pl-7 pr-2 py-2 sm:py-2.5, 14px: "Get Started" + w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-white/15 containing ChevronRight (4×4)
Dashboard Preview
Wrapper: bg-[#f5f2ee] rounded-3xl p-4 sm:p-6 w-full max-w-[880px] mx-auto
Grid: grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4
Outer container around it: px-3 sm:px-4
Card 1 — Clicks (white, rounded-2xl, p-5)
Header: orange "Clicks" + neutral "This Month" (13px)
Big number "6,896" (28px, weight 600) + red pill bg-red-50 text-red-600 rounded-full px-2 py-0.5 with TrendingDown icon "-3,382 (33%)" (11px)
Small caption "Compared to yesterday"
Centered "Month Target achieved" label
Gauge at 92% in #ef4d23, with end labels "389K" / "425K"
Toggle pill bottom: bg-neutral-100 rounded-full p-1 flex — "Impressions" active (white card + shadow) / "Clicks" inactive
Card 2 — Form (white, rounded-2xl, p-5, flex flex-col gap-3)
Two label+dropdown groups (label 12px neutral-700, button bordered rounded-lg px-3 py-2 with ChevronDown):
"Show figures for" → "This month"
"Compare period by" → "Month-to-date (MTD)"
Two label+input groups with # prefix:
"Ste targets (This month)" → 10
"Ste targets (This year)" → 100
Footer: orange #ef4d23 "Save" button (rounded-lg px-5 py-2), underlined "Cancel", X icon pushed to right (ml-auto)
Card 3 — Video Starts (white, rounded-2xl, p-5)
Header: orange "Video Starts" + "today"
Big "0" + neutral pill with TrendingUp + "0"
"Compared to yesterday"
Gauge at 68% in #9ca3af (no end labels)
Toggle pill: "Video Clicks" active / "Video Starts"
Gauge Component (reusable)
Props: value, color="#ef4d23", showLabels, min, max
SVG viewBox 0 0 200 120, max-width 260px
40 tick marks spanning a 180° arc (start at angle π, sweep to 2π); active count = round(value/100 * 40)
Each tick: <line> from radius (r-10) to r=80 around center (100,100), strokeWidth=2.5, strokeLinecap="round", active uses color, inactive #d4d4d8
Center text: <text x=100 y=105 textAnchor="middle">{value}%</text>, fontSize 22, fontWeight 600
If showLabels: small flex row below SVG, 11px neutral-500, justify-between, showing min and max
Colors
Primary orange: #ef4d23
Dark CTA: #0b0f1a
Page bg: #ededed; hero bg: #d9d9d9; dashboard tray: #f5f2ee
Icons (lucide-react)
ChevronDown, ChevronRight, ShoppingCart, Menu, TrendingDown, TrendingUp, X

File Structure
src/app/App.tsx
src/app/components/Navbar.tsx
src/app/components/DashboardPreview.tsx
src/app/components/Gauge.tsx
src/styles/fonts.css
Behavior
No custom animations; only the native looping muted background video
Entire hero (video + content + dashboard) is clipped together by the rounded container, so the dashboard cards bleed off the bottom edge
Fully responsive: navbar collapses to hamburger under md, headline/CTA scale via clamp(), dashboard grid steps from 1 → 2 → 3 columns
```

---

## 36. Neuralyn

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `neuralyn-hero`

```
Create a dark landing page for "Neuralyn" — an analytics dashboard SaaS. Use React + Vite + Tailwind CSS + TypeScript + Framer Motion + shadcn/ui.

Fonts
Inter (400, 500, 600, 700) for body/UI via @fontsource/inter
Instrument Serif (400, 400-italic) for the italic accent word via @fontsource/instrument-serif

Color Theme (all HSL, dark mode by default in :root)
Background: 0 0% 0% (pure black)
Foreground: 0 0% 100% (pure white)
Muted foreground: 0 0% 65%
Card: 0 0% 5%
Border: 0 0% 20%
Hero subtitle: 210 17% 95%

Page Structure
Section 1: Hero (full viewport height, overflow-hidden)

Navbar — horizontal, padded px-8 md:px-28 py-4:

Left: Logo image + "Neuralyn" text (text-xl font-bold tracking-tight) + nav links (Home, Services with ChevronDown icon, Reviews, Contact us) — links hidden on mobile, gap-1 between links, gap-12 md:gap-20 between logo and links
Right: "Sign In" button — solid white background (bg-foreground), black text (text-background), rounded-lg text-sm font-semibold, hover opacity transition

Hero Content — centered column, mt-16 md:mt-20 px-4:

Tag pill: A "liquid glass" styled pill (liquid-glass class) with inner "New" badge (white bg, black text, rounded-md text-sm font-medium px-2 py-0.5) + "Say Hello to Corewave v3.2" in text-sm font-medium text-muted-foreground. Pill has px-3 py-2 rounded-lg mb-6.
Title: text-5xl md:text-7xl, tracking-[-2px], font-medium, leading-tight md:leading-[1.15] mb-3. Text: "Your Insights." / "One Clear Overview." — the word "Overview" is in Instrument Serif italic (font-serif italic font-normal)
Subtitle: text-lg font-normal leading-6 opacity-90 mb-8, color uses CSS variable --hero-subtitle. Text: "Neuralyn helps teams track metrics, goals, and progress with precision." with a <br/> after "goals,"
CTA Button: "Get Started for Free" — solid white (bg-foreground text-background), rounded-full px-8 py-3.5 text-base font-medium, whileHover: scale 1.03, whileTap: scale 0.98

Dashboard + Video Area — full viewport width using w-screen with marginLeft: calc(-50vw + 50%) trick, aspect-ratio: 16/9, positioned relative:

Background video: <video>, absolutely positioned inset-0 w-full h-full object-cover. URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4
Dashboard image: Absolutely positioned, centered, max-w-5xl w-[90%] rounded-2xl, mixBlendMode: "luminosity". Has parallax scroll (y: 0→-250).
Bottom gradient fade: Absolutely positioned at bottom of section, h-40, gradient from background to transparent, z-30, pointer-events-none.

Parallax Scroll Effects (Framer Motion useScroll({ target: sectionRef, offset: ["start start", "end start"] }) + useTransform):

Hero text content group: y: [0, -200] and opacity: [1, 0] (fades over first 50% of scroll)
Dashboard image: y: [0, -250]

Entrance Animations: Staggered initial={{ opacity: 0, y }} / animate={{ opacity: 1, y: 0 }}:

Tag pill: y: 10, duration 0.5s, delay 0
Title: y: 20, duration 0.6s, delay 0.1
Subtitle: y: 20, duration 0.6s, delay 0.2
CTA: y: 20, duration 0.6s, delay 0.3
Dashboard area: y: 40, duration 0.8s, delay 0.4

Liquid Glass CSS

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

Section 2: Testimonial (min-h-screen, centered, py-24 md:py-32 px-8 md:px-28)

Quote symbol image (w-14 h-10 object-contain)
Testimonial text (text-4xl md:text-5xl font-medium leading-[1.2], wrapped in flex flex-wrap): "Neuralyn revolutionized how we handle financial insights using smart analytics. We are now driving better outcomes quicker than we ever imagined! Neuralyn revolutionized how we handle financial insights using smart analytics."
Scroll-driven word reveal: Each word is a <motion.span> with mr-[0.3em]. Uses useScroll({ target: containerRef, offset: ["start end", "end center"] }). Each word maps to a sequential range [i/total, (i+1)/total] → opacity: [0.2, 1] and color: ["hsl(0 0% 35%)", "hsl(0 0% 100%)"].
Closing " quotation mark in text-muted-foreground ml-2
Author row (flex items-center gap-4): Avatar image (w-14 h-14 rounded-full border-[3px] border-foreground object-cover) + name "Brooklyn Simmons" (text-base font-semibold leading-7 text-foreground) + role "Product Manager" (text-sm font-normal leading-5 text-muted-foreground)
Layout: max-w-3xl mx-auto, content left-aligned (items-start), gap-10 between elements

Assets needed:
logo.png — small logo icon
hero-dashboard.png — dashboard screenshot
quote-symbol.png — decorative quote mark
testimonial-avatar.png — circular headshot
```

---

## 37. Digitwist AI Builder

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `digitwist-hero`

```
Create a dark mode hero section for an AI website builder with the following exact specifications:

## Technical Setup

### Required Packages
Install these packages:
- `motion` (version 12.23.24 or later) - for animations
- `hls.js` (version 1.6.15 or later) - for video streaming
- `lucide-react` (version 0.487.0 or later) - for icons

### Fonts
Import these Google Fonts:
```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Instrument+Serif:ital@0;1&display=swap');
```

## Layout Structure

### Navbar Component
Create a fixed, transparent navbar with:

**Position & Styling:**
- Fixed to top, full width, z-index 50
- Background: fully transparent (bg-transparent)
- Padding: px-6 py-4
- Flexbox layout: items-center justify-between

**Left Section:**
- Sunburst icon (24x24px SVG) in white color

**Center Section** (hidden on mobile, visible md:flex):
- Navigation links: "Products" (with ChevronDown icon), "Customer Stories", "Resources", "Pricing"
- Font: Instrument Sans, text-sm, font-medium
- Color: text-white/80, hover:text-white
- Gap: gap-8

**Right Section:**
- "Book A Demo" link (hidden on small screens, sm:block)
- "Get Started" button: white background, black text, rounded-full, px-5 py-2.5, font-semibold

### Hero Section Component

**Container:**
- Relative positioning, full width, min-h-screen
- Background color: #000000 (pure black)
- Text color: white
- Overflow hidden

**Background Video Layer:**
- Video URL: https://stream.mux.com/T6oQJQ02cQ6N01TR6iHwZkKFkbepS34dkkIc9iukgy400g.m3u8
- Video implementation using HLS.js with Safari fallback
- Video properties: muted, loop, playsInline
- Object-fit: cover, opacity: 60%
- Poster image fallback: https://images.unsplash.com/photo-1647356191320-d7a1f80ca777?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhYnN0cmFjdCUyMGRhcmslMjB0ZWNobm9sb2d5JTIwbmV1cmFsJTIwbmV0d29ya3xlbnwxfHx8fDE3Njg5NzIyNTV8MA&ixlib=rb-4.1.0&q=80&w=1080

**Video Overlay:**
- Black overlay: bg-black/60 with backdrop-blur-[2px]

**Decorative Gradients:**
- Top-left gradient: position top-[-20%] left-[20%], size 600x600px, bg-blue-900/20, blur-[120px], mix-blend-screen
- Bottom-right gradient: position bottom-[-10%] right-[20%], size 500x500px, bg-indigo-900/20, blur-[120px], mix-blend-screen

**Content Container:**
- Max-width: 5xl (max-w-5xl)
- Center aligned (mx-auto, items-center, text-center)
- Z-index: 10, top margin: mt-20
- Vertical spacing: space-y-12

**Pre-headline:**
- Text: "Design at the speed of thought"
- Font: Instrument Serif
- Size: text-3xl (mobile), sm:text-5xl, lg:text-[48px]
- Line height: leading-[1.1]
- Color: white
- Animation: Motion fade up (opacity 0→1, y 20→0, duration 0.6s)

**Main Headline:**
- Text: "Build Faster"
- Font: Instrument Sans, font-semibold
- Size: text-6xl (mobile), sm:text-8xl, lg:text-[136px]
- Line height: leading-[0.9], letter spacing: tracking-tighter
- Gradient: bg-gradient-to-b from-white via-white to-[#b4c0ff]
- Text effect: bg-clip-text text-transparent
- Animation: Motion scale (opacity 0→1, scale 0.9→1, delay 0.2s, duration 0.6s)

**Subheadline:**
- Text: "Create fully functional, SEO-optimized websites in seconds with our advanced AI engine."
- Font: Instrument Sans
- Size: text-lg (mobile), sm:text-[20px]
- Line height: leading-[1.65]
- Color: white, opacity-70
- Max width: max-w-xl
- Animation: Motion fade (opacity 0→0.7, delay 0.4s, duration 0.6s)

**CTA Buttons:**

Primary Button:
- Style: White pill-shaped with blue arrow
- Layout: pl-6 pr-2 py-2, rounded-full
- Background: white
- Text: "Start Building Free" (font-medium, text-lg, Instrument Sans, color #0a0400)
- Arrow container: 40x40px circle, bg-[#3054ff], hover:bg-[#2040e0]
- Icon: ArrowRight (lucide-react), white, 20x20px
- Hover effect: shadow-[0_0_20px_rgba(255,255,255,0.3)], scale-105

Secondary Button:
- Text: "See Examples"
- Style: text link with arrow
- Color: text-white/70, hover:text-white
- Background: backdrop-blur-sm, hover:bg-white/5
- Padding: px-4 py-2, rounded-lg
- Icon: ArrowRight with group-hover:translate-x-1 transition

Button Container:
- Layout: flex-col (mobile), sm:flex-row
- Gap: gap-6, items centered
- Animation: Motion fade up (opacity 0→1, y 20→0, delay 0.6s, duration 0.5s)

## HLS.js Video Implementation
```tsx
import { useEffect, useRef } from "react";
import Hls from "hls.js";

const videoRef = useRef<HTMLVideoElement>(null);
const videoSrc = "https://stream.mux.com/T6oQJQ02cQ6N01TR6iHwZkKFkbepS34dkkIc9iukgy400g.m3u8";

useEffect(() => {
  const video = videoRef.current;
  if (!video) return;

  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      video.play().catch((e) => console.log("Auto-play prevented:", e));
    });
    return () => {
      hls.destroy();
    };
  } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
    video.src = videoSrc;
    video.addEventListener("loadedmetadata", () => {
      video.play().catch((e) => console.log("Auto-play prevented:", e));
    });
  }
}, []);
```

## Motion Animations
Import: `import { motion } from "motion/react"`

- Pre-headline: initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
- Main headline: initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2, duration: 0.6 }}
- Subheadline: initial={{ opacity: 0 }} animate={{ opacity: 0.7 }} transition={{ delay: 0.4, duration: 0.6 }}
- Buttons: initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6, duration: 0.5 }}

## Color Palette
- Background: #000000
- Primary text: white
- Secondary text: white/80, white/70
- Primary button background: white
- Primary button text: #0a0400
- Primary button accent: #3054ff, hover #2040e0
- Gradient end color: #b4c0ff
- Decorative gradients: blue-900/20, indigo-900/20
```

---

## 38. Dot

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `dot-hero`

```
Build a React landing page exactly as specified below. Use React 19, Tailwind CSS v4, and motion/react for animations.
1. Fonts & Global CSS Setup:
In index.html, import these Google Fonts:
Instrument Serif (weights 400, italic 400)
Inter (weights 100 to 900)
In src/index.css, import this custom font for the Nokia text:
@import url('https://db.onlinewebfonts.com/c/440b53b1a1c65037f944ff19259d8014?family=Nokia+Cellphone+FC+Small');
Configure the Tailwind theme variables in index.css:
--font-instrument: "Instrument Serif", serif;
--font-serif: "Instrument Serif", serif;
--font-sans: "Inter", sans-serif;
--font-nokia: "Nokia Cellphone FC Small", monospace;
Create a @utility font-instrument { font-family: "Instrument Serif", serif; }
Set the root font-family to var(--font-sans) and apply anti-aliasing.
2. Component Structure:
Create one main App.tsx file containing 4 components: TypingMessages, Navbar, Hero, and App.
3. Navbar Component:
Container: Fixed to the top top-6, centered horizontally left-1/2 -translate-x-1/2, width 95% w-[95%] max-w-5xl. z-50, pointer-events-none.
Nav Tag: pointer-events-auto, backdrop blur, rounded full pill shape, transparent background with border border-black/10. Flex between items.
Logo: Text "dot." using font-instrument text-[28px] tracking-tight text-[#1a1a1a].
Links: "Philosophy", "Trust", "Access", "Tribe". Hidden on mobile, flex on desktop (gap-10). font-sans text-[14px] text-[#1a1a1a] with hover opacity fading.
CTA Button ("Link up"):
Background #0871E7, rounded full, white text font-sans text-[14px].
Shadow: shadow-[inset_0_-4px_4px_rgba(255,255,255,0.39)] outline-1 outline-[#0871E7] -outline-offset-1.
Add a subtle top glint effect using an absolutely positioned rectangle inside the button: w-[80%] h-4 left-[10%] top-[1px] bg-gradient-to-b from-[#DEF0FC] to-transparent rounded-[12px]. Make it scale wider on group hover (group-hover:scale-x-105).
4. Hero Component:
Container: min-h-screen bg-[#F3F4ED] pt-24 md:pt-32 flex column centered.
Video Background: Absolute positioning inset-0 z-0. Use an HTML5 <video> set to autoplay, loop, muted, playsInline, scaling with object-cover.
Video Source: EXACTLY https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260427_054418_a6d194f0-ac86-4df9-abe5-ded73e596d7c.mp4. Add an overlaid empty div with bg-white/5 for a slight tint.
Hero Text Container: Relative z-20, pointer-events-none, text-centered layout.
Main Headline: "Short notes. <br /> Daily calm."
Animate using motion.div (from opacity: 0, scale: 0.95 to opacity: 1, scale: 1 over 1.5s with ease [0.16, 1, 0.3, 1]).
Style: font-instrument text-[38px] md:text-[56px] lg:text-[72px] leading-[0.85] tracking-tight text-[#1a1a1a] mb-6.
Sub-headline: "Linked with a single anonymous peer. One message every day. A quiet rhythm in the digital noise."
Animate using motion.div (from opacity: 0, y: 20 to opacity: 1, y: 0 over 1.2s, delay: 0.3, ease [0.16, 1, 0.3, 1]).
Style: font-sans text-[16px] md:text-[18px] text-[#1a1a1a]/70 leading-relaxed font-normal max-w-xl mx-auto.
Include the TypingMessages component inside the hero to overlap on the phone screen in the video.
5. TypingMessages Component:
Logic: Cycle through an array of messages: ["Are you here?", "Yes, I am.", "Speak soon."].
Typing speed: 100ms. Deleting speed: 50ms. Pause before deleting: 2000ms.
Positioning: Absolute position it to sit perfectly on the phone screen inside the video:
absolute left-[48.5%] md:left-[47.5%] lg:left-[48.5%] -translate-x-1/2 bottom-[32%] z-30 w-[110px] sm:w-[130px] flex justify-start text-left.
Text Style: font-nokia text-[#2A3616] text-[10px] sm:text-[14px] leading-tight break-words min-h-[1.5em].
Cursor: Add a blinking Framer Motion cursor motion.span (w-1.5 h-3 bg-[#2A3616] ml-1 align-middle) animating opacity from 0 to 1 to 0 over 0.8s, repeating infinitely, linearly.

```

---

## 39. Email Marketing

- **Category**: Email Marketing
- **Type**: hero
- **Page Type**: hero
- **ID**: `design-rocket-email-hero`

```
Prompt: Recreate "Design Rocket Certificates" Email-Style Landing Page
Build a single-page React + TypeScript + Vite + Tailwind CSS project that renders an email-style marketing page for a "Design Rocket Certificates" AI leadership course, built in collaboration with Microsoft. Use lucide-react for icons. No other UI libraries.

Global setup
index.html

Title: Newsletter Design Build Out
Preconnect to fonts.googleapis.com and fonts.gstatic.com
Load Google Fonts: Instrument Serif (ital 0,1) and Inter (weights 400, 500, 600, 700)
src/index.css


@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --font-display: 'Instrument Serif', serif;
  --font-body: 'Inter', sans-serif;
}

body {
  font-family: var(--font-body);
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}
Headings use inline style={{ fontFamily: "'Instrument Serif', serif" }}. Body copy uses Inter (default).

Page shell
Outer page: min-h-screen bg-[#050505] py-10 px-4 font-sans
Email container: max-w-[640px] mx-auto shadow-2xl overflow-hidden ring-1 ring-white/5
Content card: bg-[#111111] text-[#F2F2F2]
Shared components
Step — numbered row

Wrapper: flex items-start gap-5 mb-6 last:mb-0
Number badge: flex-shrink-0 w-7 h-7 rounded-md bg-[#DCFF00] flex items-center justify-center text-[#0A0A0A] font-bold text-xs mt-1 showing {number}.
Text: text-[17px] leading-[1.55] text-[#E8E8E8]
Divider

py-8 flex justify-center containing h-px w-24 bg-white/20
PrimaryButton (lime CTA, with arrow)

inline-flex items-center gap-3 bg-[#DCFF00] text-[#0A0A0A] font-bold rounded-lg px-6 py-3 hover:bg-[#c9ea00] hover:-translate-y-0.5 transition-all duration-200
Contains the label and a lucide-react ArrowRight icon w-5 h-5 strokeWidth={2.5}
SolidButton (white pill)

inline-block bg-white text-[#0A0A0A] font-bold rounded-lg px-8 py-3 hover:bg-[#E8E8E8] hover:-translate-y-0.5 transition-all duration-200
Section 1 — Hero (video background)
Wrapper: relative w-full overflow-hidden with inline style={{ aspectRatio: '640 / 820' }}
Background video (absolutely filling container, object-cover, autoplay muted loop playsInline): https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260419_064822_f120e48a-d545-45dd-a02d-facb07829888.mp4
Overlay gradient (absolute inset-0): linear-gradient(to bottom, rgba(17,17,17,0) 45%, rgba(17,17,17,0.45) 68%, rgba(17,17,17,0.9) 88%, rgba(17,17,17,1) 100%)
Foreground stack: relative z-10 h-full flex flex-col items-center text-center px-6 pt-12 pb-10
Top brand block (white):
"Design Rocket" — Instrument Serif, text-[28px] leading-[0.95] tracking-tight
"CERTIFICATES" — text-[13px] tracking-[0.22em] font-medium mt-1
Spacer mt-40, then "NOW AVAILABLE" — text-white text-[13px] tracking-[0.28em] font-semibold
flex-1 spacer pushing headline to bottom
Headline (Instrument Serif): text-white text-[58px] leading-[1.02] tracking-tight max-w-[560px]
Text: Learn to lead AI
and unlock new value
CTA pill (note: uses #D8F90A not the card lime):
mt-10 inline-flex items-center gap-3 bg-[#D8F90A] text-[#1E1E1E] font-semibold rounded-full px-8 py-4 hover:bg-[#c9ea00] hover:-translate-y-0.5 transition-all duration-200
Label "Enroll Now" + ArrowRight w-5 h-5 strokeWidth={2.5}
Section 2 — Intro copy + CTA
Container px-[78px] pb-8 pt-4, centered paragraph text-[18px] leading-[1.55]:
Built in collaboration with Microsoft, this certificate course gives you the toolkit to lead AI transformation across your organization. Learn to spot opportunities, launch AI pilots, and scale adoption grounded in responsible practices and proven frameworks.

flex justify-center pb-14 with <PrimaryButton label="Get Started" />
<Divider />
Section 3 — "Transform how you lead with AI"
Heading container px-9 pb-8, Instrument Serif text-center text-[46px] leading-[1.05] tracking-tight: Transform how you lead with AI
Video card px-[42px] pb-10:
Anchor: block overflow-hidden rounded-[14px] group
Video: autoplay/muted/loop/playsInline, w-full h-[370px] object-cover rounded-[14px] transition-transform duration-700 group-hover:scale-[1.03]
Src: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260419_065931_e3ca7b53-d32e-4ad5-81de-dc9d6fcfda6d.mp4
Steps list container px-[76px] pb-10, inner max-w-[489px] mx-auto, rendering four <Step>s:
Learn how to spot AI opportunities that boost productivity across roles and deliver visible results.
Build structures that support your team so AI efficiencies multiply across the organization.
Gain the skills to drive culture change like securing buy-in and reducing resistance.
Get frameworks to deliver AI pilots that prove impact fast and build credibility with measurable results.
flex justify-center pb-14 with <SolidButton label="Enroll Now" />
<Divider />
Section 4 — "Build your AI transformation roadmap"
Heading container pb-7 px-9, Instrument Serif text-center text-[46px] leading-[1.05] tracking-tight:
Build your AI
transformation roadmap
Video card px-[42px] pb-10 (same classes as Section 3) with src:
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260417_110451_9f82b157-dc92-4a9f-a341-c25594ec20e1.mp4
Paragraph container px-[78px] pb-8, centered text-[18px] leading-[1.55]:
You'll finish this hands-on course with a personal AI Transformation Plan: your playbook for pilot proposals, data strategy and governance. Use it to help secure buy-in, guide rollout, and scale adoption responsibly.

flex justify-center pb-14 with <SolidButton label="Learn More" />
Section 5 — Lime CTA card
Outer px-14 pb-12
Card: bg-[#D8F90A] rounded-[10px] px-8 py-12 text-center
Heading (Instrument Serif): text-[#1E1E1E] text-[52px] leading-[1.02] tracking-tight mb-3
Ready to lead AI
at work?
Subtext: text-[#1E1E1E] text-[18px] leading-[1.5] mb-8 px-4 — Enroll now and be the leader your team has been waiting for.
Centered <PrimaryButton label="Enroll Now" />
Footer
bg-[#080808] text-white pt-12 px-10 text-center border-t border-white/5
Wordmark link text-[30px] font-bold tracking-tight text-white hover:text-[#DCFF00] transition-colors → "Design Rocket" (wrapped in pb-8 flex justify-center)
Disclaimer paragraph text-[12px] text-[#83837D] leading-[1.5] pb-8:
Microsoft is a collaborator on this specific course. Microsoft does not endorse
Design Rocket generally or other Design Rocket products.

Divider: flex justify-center pb-8 with inner h-px w-24 bg-white/20
Social icon row flex justify-center gap-5 pb-5 — six circular buttons mapping [Facebook, Twitter, Instagram, Youtube, Linkedin, Music2] from lucide-react. Each:
w-10 h-10 rounded-full border border-white/20 flex items-center justify-center hover:bg-white hover:text-[#1E1E1E] hover:border-white transition-colors, icon w-[18px] h-[18px]
Unsubscribe note text-[10px] text-[#83837D] pb-4 leading-[1.6]:
If you no longer want to receive updates on Design Rocket Certificates,
you can unsubscribe at any time by clicking "unsubscribe" below.

Link row text-[12px] pb-3 space-x-2: Support | Privacy | Terms | Unsubscribe (pipes text-[#8F8E88], links hover:underline)
Copyright anchor text-[12px] text-white/80 hover:text-white inline-block:
©2026 Design Rocket, 660 4th Street #443, San Francisco, CA 94107 USA
Trailing pb-10 spacer
Animation / interaction summary
All buttons: hover:-translate-y-0.5 transition-all duration-200 plus background-color change on hover.
Video cards: wrapper overflow-hidden rounded-[14px] group; video scales on hover via transition-transform duration-700 group-hover:scale-[1.03].
Footer wordmark and social icons: smooth color transitions via transition-colors.
Videos auto-play muted, loop, and playsInline for mobile autoplay.
Color palette
Page bg #050505, card bg #111111, footer bg #080808
Text #F2F2F2, secondary #E8E8E8, muted #83837D, divider #8F8E88
Lime primary #DCFF00, lime variant #D8F90A, lime hover #c9ea00
Dark text on lime #0A0A0A / #1E1E1E
Fonts
Display: Instrument Serif (all large headings, wordmark in hero)
Body / UI: Inter

```

---

## 40. Duolingo Styleguide

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `duolingo-styleguide-hero`

```
Fonts
Primary font: 'Nunito' from Google Fonts (weights: 400, 500, 600, 700, 800, 900)
Display/heading font: 'Feather Bold' from https://db.onlinewebfonts.com/c/14936bb7a4b6575fd2eee80a3ab52cc2?family=Feather+Bold
Font stack fallback: 'Nunito', 'DIN Round Pro', -apple-system, BlinkMacSystemFont, sans-serif
Color Variables (CSS custom properties)

--green: rgb(88, 204, 2)
--green-hover: rgb(75, 178, 0)
--green-shadow: #61B800
--dark-blue: rgb(16, 15, 62)
--blue: rgb(28, 176, 246)
--gray-text: rgb(75, 75, 75)
--gray-light: rgb(119, 119, 119)
--border-color: rgb(229, 229, 229)
--nav-text: rgb(175, 175, 175)
--footer-green: #4EC604
--red: #FF4B4B
--orange: #FF9600
--golden: #FFC800
Structure & Layout
Fixed Navbar (64px height, white background, bottom border)
Left side: Duolingo logo image (https://d35aaqx5ub95lt.cloudfront.net/images/splash/f92d5f2f7d56636846861c458c0d0b6c.svg, 140x33px), followed by a 1px vertical divider (24px tall), then "STYLE GUIDE" label (11px, uppercase, letter-spacing 1.5px, gray)
Right side: Horizontal nav links - "Colors", "Type", "Buttons", "Cards", "Components" (13px, bold, uppercase, 0.5px letter-spacing, gray, with green hover/active states and subtle green background on hover)
Max-width: 1440px, centered
Hero Section (centered, green-to-white gradient background)
Headline: "duolingo design" in Feather Bold font, 52px, green color (#58CC02), lowercase
Description: "A comprehensive visual reference for the Duolingo design system covering colors, typography, button variants, cards, and UI components." -- 17px, gray-light color, max-width 520px, 1.5 line-height
Two buttons below: Primary "GET STARTED" button (green, white text, 12px border-radius, 4px green box-shadow for 3D effect, uppercase bold) and Secondary "I ALREADY HAVE AN ACCOUNT" button (transparent with 2px gray border, blue text, 4px gray box-shadow for 3D effect)
Both buttons: 48px height, 24px horizontal padding, 15px font-size, 700 weight, uppercase
Buttons have active state: box-shadow removed, translateY(4px)
Padding: 56px top, 40px sides, 40px bottom
Main Grid (2-column grid, no gap, max-width 1440px)
Each panel has 36px vertical and 40px horizontal padding, bottom border and right border (border-color). Even panels have no right border.

Each panel has a section label: 11px, 800 weight, uppercase, 2px letter-spacing, gray (nav-text), with a 1px line extending to the right via ::after pseudo-element.

Panels in order (left-to-right, top-to-bottom):

Panel 1: Color Palette (light)
Grid of 12 color swatches, grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)), 12px gap. Each swatch:

Square (aspect-ratio: 1), 12px border-radius, 1px border rgba(0,0,0,0.06)
Hover: scale(1.05) with box-shadow 0 8px 24px rgba(0,0,0,0.12)
Below swatch: name (12px, bold, gray-text) and hex value (10px, gray-light, semi-bold)
Colors in order:

Green -- rgb(88, 204, 2) -- #58CC02
Green Hover -- rgb(75, 178, 0) -- #4BB200
Blue -- rgb(28, 176, 246) -- #1CB0F6
Dark Blue -- rgb(16, 15, 62) -- #100F3E
Red -- #FF4B4B
Orange -- #FF9600
Golden -- #FFC800
Footer Green -- #4EC604
Gray Text -- rgb(75, 75, 75) -- #4B4B4B
Gray Light -- rgb(119, 119, 119) -- #777777
Nav Text -- rgb(175, 175, 175) -- #AFAFAF
Border -- rgb(229, 229, 229) -- #E5E5E5
Panel 2: Typography (light)
Vertical stack with 20px gap. Each row is a flex row (baseline-aligned, 20px gap) with a meta column (80px wide, right-aligned) showing size in blue (11px bold) and weight label below (10px, nav-text color), then the sample text.

Rows:

48px / Feather Bold -- "Display" -- green color, Feather Bold font
32px / Bold 700 -- "Heading One" -- gray-text color
28px / Feather Bold -- "heading two" (lowercase) -- green color, Feather Bold font
18px / Medium 500 -- "Body text for paragraphs and descriptions with comfortable reading line-height." -- gray-light color, 1.6 line-height
14px / Bold 700 -- "CAPTION LABEL" -- uppercase, nav-text color, 0.5px letter-spacing
12px / Semi 600 -- "Small utility text for metadata and hints" -- gray-light color
Panel 3: Button Variants (light)
Vertical stack with 16px gap. Each row has an 80px label (10px, bold, uppercase, 1px letter-spacing, nav-text) then buttons with 12px gap, flex-wrap.

Rows:

"Primary" -- 3 buttons: "GET STARTED" (green bg, white text, 4px green shadow), "SMALL" (same but 36px height, 13px font, 16px padding, 10px radius, 3px shadow), "DISABLED" (same as primary but opacity 0.45, pointer-events none)
"Secondary" -- 3 buttons: "LEARN MORE" (transparent, 2px #CFCFCF border, blue text, 4px #CFCFCF shadow), "SMALL" (same sizing as small primary), "DISABLED" (opacity 0.45)
"Danger" -- 2 buttons: "DELETE" (#FF4B4B bg, white text, 4px #CC3C3C shadow), "REMOVE" (small variant)
"Ghost" -- 1 button: "VIEW ALL" (no bg/border/shadow, green text, green bg on hover at 0.08 opacity)
Panel 4: Dark Theme Buttons (dark-blue background)
Section label and ::after line use white at 35% and 10% opacity respectively.

Two rows:

"GET STARTED" primary + "TRY 1 WEEK FREE" (white bg, dark-blue text, 4px #88879F shadow, hover bg #c8f040)
Small variants of both
Panel 5: Cards (light)
2-column grid, 16px gap. Each card: white bg, 2px border (border-color), 16px border-radius. Hover: translateY(-4px), box-shadow 0 12px 32px rgba(0,0,0,0.08).

Card 1:

Image: https://images.pexels.com/photos/4145354/pexels-photo-4145354.jpeg?auto=compress&cs=tinysrgb&w=400&h=200&fit=crop (120px height, cover)
Tag: "NEW" (green text, green bg at 10% opacity, 11px, 800 weight, uppercase, 6px radius, 3px/8px padding)
Title: "Spanish for Beginners" (16px, bold, gray-text)
Description: "Start your language journey with interactive lessons designed to build fluency." (13px, gray-light, 1.5 line-height)
Footer (12px top border, 12px/16px padding): left "12 UNITS" (12px bold uppercase nav-text), right "START" (12px bold uppercase blue, hover opacity 0.7)
Card 2:

Image: https://images.pexels.com/photos/267669/pexels-photo-267669.jpeg?auto=compress&cs=tinysrgb&w=400&h=200&fit=crop
Tag: "POPULAR" (blue text, blue bg at 10% opacity)
Title: "French Conversations"
Description: "Practice real-world dialogue and improve pronunciation with native speakers."
Footer: "8 UNITS" / "CONTINUE"
Panel 6: Dark Theme Cards (dark-blue background)
2-column grid, same structure but no images. Cards have bg rgba(255,255,255,0.06), border rgba(255,255,255,0.08). Titles are white, descriptions are white at 50% opacity, footer border is white at 8% opacity, footer text is white at 30% opacity.

Card 1:

Tag: "SUPER" (golden #FFC800 text, golden bg at 15% opacity)
Title: "Unlimited Hearts"
Desc: "Keep learning without interruption with Super Duolingo benefits."
Footer: "PREMIUM" / "UPGRADE"
Card 2:

Tag: "PRO" (orange #FF9600 text, orange bg at 15% opacity)
Title: "Mastery Quizzes"
Desc: "Challenge yourself with advanced assessments to test your skill level."
Footer: "ADVANCED" / "TRY NOW"
Panel 7: Components (light)
Vertical stack with 20px gap. Each group has a label (10px bold uppercase, 1px letter-spacing, nav-text).

Badges: Flex row, 8px gap. Pill-shaped badges (4px/10px padding, 20px radius, 12px bold uppercase):

"COMPLETED" (green text, green bg 12%)
"IN PROGRESS" (blue text, blue bg 12%)
"FAILED" (red text, red bg 12%)
"STREAK" (orange text, orange bg 12%)
"PREMIUM" (golden-brown #b8920f text, golden bg 15%)
Input + Button: Flex row, 12px gap. Input (flex:1, 48px height, 16px padding, 2px border border-color, 12px radius, 15px font, 600 weight, focus border turns blue, placeholder is nav-text color 500 weight) + Primary "SUBSCRIBE" button.

Toggle: Flex row with two toggle switches. Each toggle is 48x28px. Track is border-color bg, 14px radius. Thumb is 22x22px white circle, 3px from edges, with 1px 3px rgba(0,0,0,0.15) shadow. Checked state: track turns green, thumb translates 20px right. Labels "Sound effects" and "Animations" (14px, 600 weight). First toggle is checked by default.

Progress: 3 progress bars in a column, 10px gap. Each row: flex, 12px gap, bar (flex:1, 12px height, border-color bg, 6px radius, overflow hidden), fill (6px radius, 0.6s ease width transition), value (12px bold, 32px wide, right-aligned).

85% green fill
60% blue fill
35% orange fill
Tooltips & Streak: Flex row, 16px gap, center-aligned.

Tooltip trigger: "Hover me" (13px, bold, green text, green bg 8%, 8px/16px padding, 8px radius). On hover shows tooltip bubble above (dark-blue bg, white 12px 600-weight text, 6px/12px padding, 8px radius, 5px triangle arrow pointing down via ::after border trick).
Streak counter: Inline-flex, 6px gap, 6px/14px padding, orange bg 10%, 20px radius. Fire emoji (18px) + "42" (16px, 800 weight, orange).
Panel 8: Dark Theme Components (dark-blue background)
Labels use white at 30% opacity.

Language Pills: Flex row, 8px gap. Each pill: inline-flex, 6px gap, 6px/12px padding, 2px border, 12px radius, cursor pointer, hover turns border green with subtle green bg.

"Spanish" (ACTIVE -- green border, green bg 8%, white text) with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/59a90a2cedd48b751a8fd22014768fd7.svg
"French" (inactive -- white border 12%, white text 70%) with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/482fda142ee4abd728ebf4ccce5d3307.svg
"German" with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/c71db846ffab7e0a74bc6971e34ad82e.svg
"Japanese" with flag https://d35aaqx5ub95lt.cloudfront.net/vendor/edea4fa18ff3e7d8c0282de3f102aaed.svg
Flag images: 24x18px, object-fit contain. Pill text: 13px, bold.
Avatar Group: Flex row with overlapping circular avatars (36px, 50% radius, 2px white border, -8px margin-left except first). Images:

https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=80&h=80&fit=crop
https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=80&h=80&fit=crop
https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress&cs=tinysrgb&w=80&h=80&fit=crop
Count badge "+5" (same 36px circle, #f0f0f0 bg, 11px 800 weight, gray-light)
Text next to group: "8 learners active" (13px, 600 weight, white 50% opacity)
Progress (Dark): 2 bars, track bg is white 8%, values are white 60%:

72% golden fill
45% green fill
Badges (Dark):

"MASTERED" (green bg 15%, #7ADB2E text)
"REVIEW" (blue bg 15%, #4DC4F8 text)
"CROWN" (golden bg 15%, #FFC800 text)
Responsive Breakpoints
900px and below:

Grid becomes single column, no right borders
Hero h1: 36px
Nav links hidden
Cards grid becomes single column
Hero buttons stack vertically, max-width 280px
600px and below:

Hero padding: 40px 20px 32px
Hero h1: 28px
Panel padding: 28px 20px
Color grid: 3 columns
Type meta column: hidden
Display type: 32px
Button labels: hidden
Input row: column direction

```

---

## 41. Price Calculator

- **Category**: SaaS
- **Type**: pricing
- **Page Type**: hero
- **ID**: `price-calculator`

```
Recreate Project Estimation Calculator Section

Create a full-width dark calculator section with id calculator-section. Background: bg-background, padding py-16 md:py-28 px-4 md:px-16, max-width max-w-7xl centered.

Header: Centered. Small mono uppercase tracking-widest label "Try project estimation calculator" in text-muted-foreground. Below it, an h2: "Get premium website within your budget" — text-3xl md:text-4xl lg:text-5xl font-normal.

Layout: 2-column grid (grid-cols-1 lg:grid-cols-2), rounded-2xl overflow-hidden, no gap.

LEFT COLUMN (Calculator Form): Background #0D0D0D, padding p-8 lg:p-12, sections divided by divide-y divide-[#1E1E1E].

4 sections separated by horizontal dividers:

Service Type (radio buttons): h3 "What kind of service do you need?" — 3 options: "Only Design" (design), "Only Development" (development), "Design + Development" (both, default). Custom radio circles: w-5 h-5 rounded-full border-2, active = border-[#FF5656] with inner w-2 h-2 rounded-full bg-[#FF5656].

Number of Pages (slider): h3 with current value in #FF5656. Shadcn <Slider> min=1, max=30, step=1, default=5. Labels "1" and "30" below.

Add-ons (checkboxes): Two checkboxes with price labels on the right in #FF5656:

"I will need help with content" → +$50/pages

"I want to optimize my website for SEO" → +$50/pages Custom checkboxes: w-5 h-5 border-2 rounded, checked = border-[#FF5656] bg-[#FF5656] with white SVG checkmark.

Timeline (radio buttons): h3 "How fast do you need this?" — 3 options with prices:

"Within 7 Days" → +$100/pages

"Within 14 Days" → +$25/pages

"Regular Speed (Based on discussion)" → no extra cost (default)

RIGHT COLUMN (Cost Estimation): Padding p-8 lg:p-12, border border-white/10 rounded-r-2xl, min-height 717.98px.

h3 "Estimated Cost" + description paragraph.

3 stacked cards (rounded-2xl p-6 space-y-3):

Agency card: bg-muted/50. Title "Typical Agency charges minimum". Large price text-4xl font-bold. Subtitle: "+ Too much extra time & additional cost".

Freelancer card: bg-muted/50. Title "Regular Freelancer charges minimum". Large price text-4xl font-bold. Subtitle: "+ Too much headache & back-and-forth".

Your price card: bg-gradient-to-r from-pink-500 to-orange-500 text-white. Title "With Webfluin Studio". Price text-5xl font-bold. Subtitle: "Save your money, time & headache".

PRICING LOGIC:

calculatePrice():
  Base prices by service:
    design: base=399, perPage=100
    development: base=199, perPage=100
    both: base=499, perPage=200
  
  total = max(base, base + (pages - 1) * perPage)
  if needContent: total += pages * 50
  if needSEO: total += pages * 50
  if rush: total += pages * 100
  if fast: total += pages * 25

calculateAgencyCost():
  perPage = (both ? 1000 : 400)
  return 8000 + (pages - 1) * perPage

calculateFreelancerCost():
  perPage = (both ? 500 : 200)
  return 3000 + (pages - 1) * perPage

All prices displayed with .toLocaleString() and $ prefix.

State: serviceType (design|development|both, default both), pages (number, default 5), needContent (bool), needSEO (bool), timeline (regular|fast|rush, default regular).

Dependencies: Shadcn Slider component, useToast hook.
```

---

## 42. Digital Epoch

- **Category**: Hero Section
- **Type**: hero
- **Page Type**: hero
- **ID**: `digital-epoch-hero`

```
Build a modern, high-performance landing page section using React, TypeScript, Tailwind CSS v4, and Motion. The application should match the following exact specifications:
1. Dependencies & Setup
Libraries: Install lucide-react, motion, clsx, and tailwind-merge.
Fonts & CSS: In index.css, import the Inter and Outfit fonts from Google Fonts: @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;500;600&display=swap');
Configure the Tailwind theme in your CSS to use Inter as --font-sans and Outfit as --font-display.
The global body background should be #f9fafb.
2. Main Hero Container & Video Background
Create a hero section container with these exact classes: relative w-full max-w-[1400px] mx-auto rounded-[48px] bg-white border border-slate-200/50 shadow-[0_40px_100px_-20px_rgba(0,0,0,0.03)] overflow-hidden h-[600px] flex flex-col.
Inside, add an absolutely positioned underlying layer (absolute inset-0 pointer-events-none z-0 overflow-hidden select-none) for the background video.
The video tag must point to exactly this URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260505_101331_74f9b798-3f00-4e86-8a01-377aa16ffeaa.mp4. It must include autoPlay, loop, muted, and playsInline attributes, with the classes: w-full h-full object-cover scale-105 transition-transform duration-1000. No overlays.
3. Hero Text Content
Create a content wrapper positioned relative (z-20 flex-1 px-8 md:px-16 pt-12 md:pt-16 flex flex-col items-start).
Use motion.div from motion/react to animate the text layer in (fade in, slide up slightly).
Headline: "Foundation of the<br />new digital epoch". Should use the font-display font, sizes text-[42px] md:text-[56px], medium weight, tight tracking, color #0a1b33.
Subheadline: "Designing products, powering ecosystems and laying the foundation of a decentralized web for enterprises, builders and communities alike." Should use font-sans, sizes text-[14px] md:text-[15px], color #64748b.
Contact Button: Text "Contact Us", using a dark background (bg-[#0a152d]), white text, rounded-full, with hover scale animations via motion.button.
4. Floating Bottom Navbar
Create an absolutely positioned navbar wrapper at the bottom center of the hero: absolute bottom-10 left-1/2 -translate-x-1/2 z-30.
The nav element should use motion.nav to fade in and slide up (delayed after the text). It must have the classes: flex items-center bg-white/90 backdrop-blur-2xl px-1.5 py-1.5 rounded-full shadow-[0_12px_40px_rgba(0,0,0,0.08)] border border-slate-200/40.
Nav Elements:
A small circular logo placeholder on the left (w-9 h-9 bg-white border-slate-100 shadow-sm) containing the star character "✦".
Two standard text buttons: "Products" and "Docs" (text-[12px] font-semibold text-slate-500 hover:text-[#0a1b33]).
A "Get in touch" button on the right containing the text and a small ChevronRight (from lucide-react). Styled identically to the marquee cards: bg-white px-5 py-2 rounded-full text-[12px] font-semibold text-[#0a1b33] border border-slate-200/60 shadow-sm hover:border-slate-300 transition-all.
5. Seamless Marquee Logo Scroller Component
Below the hero container (mt-10), add a custom highly-performant Marquee Scroller component.
The scroller must use a pure CSS @keyframes animation (transform: translateX(0) to translateX(-50%)) for infinite scrolling, pausing on hover. It needs a left/right masking gradient (maskImage linear-gradient fading to transparent on the edges). No title or description text above the scroller.
The Logos List: Supply an array of 8 objects with src URLs from svgl.app, alt names, and hex gradient objects:
Procure (procure.svg, blue gradient)
Shopify (shopify.svg, yellow gradient)
Blender (blender.svg, blue gradient)
Figma (figma.svg, purple gradient)
Spotify (spotify.svg, pink/red gradient)
Lottielab (lottielab.svg, yellow/green)
Google Cloud (google-cloud.svg, light blue)
Bing (bing.svg, cyan/teal)
Render the list twice inline to ensure a seamless loop.
Card Design: Make each logo's container card exactly match the "Get in touch" navbar button's styling. The container classes must be exactly: group relative h-24 w-40 shrink-0 flex items-center justify-center rounded-full bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 transition-all overflow-hidden.
Inside the card, add an absolute div using the specific gradient colors, scaled at 1.5 and 0 opacity, which drops to scale 1 and opacity 100 on group-hover.
The image tag should invert/turn black on hover (group-hover:brightness-0 group-hover:invert).
```

---

## 43. Kresna Footer

- **Category**: Footer Section
- **Type**: footer
- **Page Type**: hero
- **ID**: `kresna-footer`

```
Build a single-file HTML footer component called Kresna — a sales-automation SaaS brand. The deliverable is one self-contained .html file with inline <style> and inline <script>. Render it inside a <section class="footer-section"> on a white page (body { background: #ffffff; padding: 48px 24px; }).
Fonts
Load from Google Fonts in the <head>:

DM Sans — weights 400, 500, 600, 700 (body, nav links, buttons, headings, watermark)
Caveat — weights 500, 600, 700 (handwritten accents: "Stay in touch!", "Feeling lucky?", column titles "Navigation"/"Company")

Default body font: 'DM Sans', sans-serif. Body color #2d3148.
Use *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }.
Layout structure
A .footer-wrapper with max-width: 1150px, centered, CSS grid grid-template-columns: 350px 1fr, gap: 16px, align-items: stretch. Two cards side by side:
Left card — .footer-left (video background)

Position relative, min-height: 340px, border-radius: 28px, padding: 32px, overflow: hidden
Box shadow: 0 12px 40px rgba(21, 76, 189, 0.25)
Fallback background: #1e4fc0
Flex column, justify-content: space-between
Contains, in order:

A <video class="footer-left-video" autoplay muted loop playsinline preload="auto"> with <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260503_104800_bc43ae09-f494-43e3-97d7-2f8c1692cfd7.mp4" type="video/mp4" />. Style: position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; pointer-events: none;. No overlays, no tints, no noise texture.
.footer-logo — flex row, gap: 10px, position: relative; z-index: 1. Contains:

.footer-logo-mark — a 32×32 rounded square (border-radius: 8px), background: rgba(255,255,255,0.15), border: 1.5px solid rgba(255,255,255,0.85), centered bold "K" letter inside (DM Sans, 16px, weight 700, white, letter-spacing: -0.02em)
<span class="footer-logo-name">Kresna</span> — DM Sans, 22px, weight 700, white, letter-spacing: -0.02em


.footer-tagline-container — margin-top: auto; margin-bottom: 28px, z-index: 1. Contains .footer-tagline (19px, weight 400, white, line-height: 1.45) with text:



     Smarter sales automation,<br>
     <span>powered by AI.</span>
 The inner `<span>` uses `color: rgba(255, 255, 255, 0.65)`.
4. .footer-social-row — flex row, justify-content: space-between, align-items: center, gap: 12px, z-index: 1. Contains:
- .footer-social-label — Caveat, 17px, weight 600, color rgba(255,255,255,0.9), letter-spacing: 0.3px, text: "Stay in touch!"
- .footer-social-icons — flex row, gap: 7px. Four .social-icon divs, each 36×36, border-radius: 9px, background: #0e1014, centered 15×15 white SVG, box shadow 0 6px 18px rgba(0,0,0,0.35), 0 2px 6px rgba(0,0,0,0.2). Hover: background: #000, transform: translateY(-2px), deeper shadow, transition: background 0.2s, transform 0.15s, box-shadow 0.2s. Icons in order: Discord, X (Twitter), LinkedIn, GitHub — use the official brand path d= strings for each in a <svg viewBox="0 0 24 24">.
Right card — .footer-right (light gray)

background: #f0f1f5, border-radius: 28px, padding: 40px, overflow: visible, box-shadow: 0 4px 20px rgba(0,0,0,0.04)
Flex column, justify-content: space-between, position relative
Contains:

Floating "Feeling lucky?" badge — .footer-lucky-graphic
Absolutely positioned, top: -36px; right: 40px, z-index: 10, flex column, align-items: flex-start, gap: 6px. Overflows above the top edge of the card.

.lucky-cube — 96×96, border-radius: 22px, transform: rotate(-10deg), gradient linear-gradient(135deg, #5b9ffb 0%, #1e5dd7 55%, #1448be 100%), layered shadows:

  inset 3px 3px 8px rgba(255,255,255,0.35),
  inset -3px -3px 12px rgba(0,0,0,0.18),
  8px 14px 28px rgba(20,72,200,0.35)
Inside, a <span class="lucky-cube-mark">K</span>: DM Sans, 42px, weight 700, white, letter-spacing: -0.04em, transform: rotate(10deg) (counter-rotates the cube), text-shadow: 0 3px 6px rgba(0,0,0,0.25), line-height: 1.

.lucky-text-row — flex row, gap: 6px, align-items: center, transform: rotate(-4deg), margin-top: 4px. Contains:

.lucky-arrow — 22×22 inline SVG, color: #9ca3af. SVG content: a curved hand-drawn arrow:



html    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 20 C 6 14, 10 9, 18 5" />
      <path d="M18 5 L 12 5" />
      <path d="M18 5 L 18 11" />
    </svg>
SVG paths: `stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round`.

.lucky-text — Caveat, 20px, weight 600, color #9ca3af, white-space: nowrap, text: "Feeling lucky?"

Top — .footer-right-top with .footer-nav-cols
Flex row, gap: 72px, padding-top: 8px. Two .footer-col columns:

Column titles (.footer-col-title): Caveat, 24px, weight 600, italic, color #9ca3af, margin-bottom: 18px
Links (.footer-col a): block, DM Sans, 14px, weight 600, color #111827, margin-bottom: 14px, no underline, hover color #1f65d6, transition: color 0.2s

Column 1 — title "Navigation", links: How it works, Features, Pricing, Testimonials, FAQ
Column 2 — title "Company", links: Blog, About, Terms and Condition, Privacy Policy
Bottom — .footer-bottom
Flex row, align-items: flex-end, justify-content: space-between, margin-top: 48px. Contains:

.footer-copyright — DM Sans, 12.5px, weight 500, color #9ca3af, text: "© 2025 Kresna. All rights reserved."
.footer-cta-mini — flex column, gap: 14px, contains:

<h4> — 15px, weight 400, color #6b7280, line-height: 1.45, with text:



    AI moves fast.<br><strong>Stay ahead with Kresna.</strong>
The `<strong>` is block-level, 19px, weight 700, color `#111827`.

.footer-subscribe-row — flex row, width: 310px, background: #fff, border: 1px solid #e5e7eb, border-radius: 12px, padding: 5px, box-shadow: 0 2px 10px rgba(0,0,0,0.04). Contains:

<input type="email" placeholder="Enter email address"> — flex 1, padding: 11px 14px, transparent, no border, DM Sans 13.5px, color #111827, placeholder #9ca3af
<button type="button">Subscribe</button> — padding: 11px 22px, background: #111214, white text, DM Sans 13.5px weight 600, border-radius: 8px, shadow 0 6px 20px rgba(0,0,0,0.28), 0 2px 8px rgba(0,0,0,0.15). Hover: background: #000, deeper shadow, transform: translateY(-1px), transition: background 0.2s, box-shadow 0.2s, transform 0.15s.



Watermark — .footer-watermark (sits outside .footer-wrapper but inside the section)
A massive faded "Kresna" wordmark that scales fluidly to the full footer wrapper width with the visible glyph edges flush against the container edges.
CSS:
css.footer-watermark {
  max-width: 1150px;
  margin: -60px auto 0;
  pointer-events: none;
  user-select: none;
  position: relative;
  z-index: 0;
  line-height: 0;
}
.footer-watermark svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}
.footer-watermark text {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  letter-spacing: -0.03em;
  fill: rgba(0, 0, 0, 0.04);
}
HTML:
html<div class="footer-watermark" aria-hidden="true">
  <svg id="watermarkSvg" viewBox="62 95 876 175" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
    <text id="watermarkText" x="500" y="240" text-anchor="middle" font-size="320">Kresna</text>
  </svg>
</div>
Inline JS at the end of the section measures the rendered text bounding box with getBBox() and updates the SVG viewBox so the visible glyph edges sit flush against the container — runs after document.fonts.ready and on resize:
html<script>
  function fitWatermark() {
    const svg = document.getElementById('watermarkSvg');
    const text = document.getElementById('watermarkText');
    if (!svg || !text) return;
    try {
      const bbox = text.getBBox();
      svg.setAttribute('viewBox',
        `${bbox.x} ${bbox.y} ${bbox.width} ${bbox.height}`);
    } catch (e) {}
  }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitWatermark);
  } else {
    window.addEventListener('load', fitWatermark);
  }
  window.addEventListener('resize', fitWatermark);
</script>
Responsive breakpoints
@media (max-width: 860px):

.footer-wrapper becomes grid-template-columns: 1fr
.footer-left min-height: auto, gap: 40px

@media (max-width: 560px):

.footer-right padding: 24px
.footer-nav-cols gap: 40px
.footer-bottom flex-direction: column, align-items: flex-start, gap: 24px
.footer-subscribe-row width: 100%
.footer-lucky-graphic right: 12px, top: -28px
.lucky-cube width: 72px, height: 72px
.lucky-cube-mark scaled proportionally if needed

Animations / transitions
No keyframe animations. All motion is hover-driven via CSS transition:

Social icons: background, transform, box-shadow on hover
Subscribe button: background, box-shadow, lift on hover
Nav links: color shift on hover

The video on the left card autoplays, loops, muted, plays inline (no controls).
Final markup order inside <section class="footer-section">
<section class="footer-section">
  <div class="footer-wrapper">
    <div class="footer-left"> [video, logo, tagline, social row] </div>
    <div class="footer-right"> [floating lucky badge, nav cols, bottom row] </div>
  </div>
  <div class="footer-watermark"> [SVG] </div>
  <script> [fitWatermark] </script>
</section>
```

---

## 44. Vize Footer

- **Category**: Footer Section
- **Type**: footer
- **Page Type**: hero
- **ID**: `vize-footer`

```
Build a highly polished, responsive Footer component for a React application using Vite, Tailwind CSS, `lucide-react` for icons, and `motion/react` for animations. 

The design relies on a premium "layered card" aesthetic, precise typography, and a massive background-blended text element utilizing advanced, handcrafted SVG filters.

### 1. Dependencies
Ensure the project has:
`npm install lucide-react motion`

### 2. Global CSS (`src/index.css`)
Use the exact following CSS to define the Inter font, the Tailwind layer, and advanced `glass-card` and `liquid-glass` utilities:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import "tailwindcss";

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}

@layer utilities {
  .glass-card {
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
  }

  .text-glass {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .liquid-glass {
    background: rgba(255, 255, 255, 0.01);
    background-blend-mode: luminosity;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    border: none;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
  }

  .liquid-glass::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1.4px;
    background: linear-gradient(180deg,
      rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
      rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
      rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
  }
}

body {
  @apply bg-[#F9F9FB] text-[#141414] font-sans antialiased;
}
3. Application Layout (src/App.tsx)
Render the layout wrapper mimicking a full-screen application view exactly like this:
code
Tsx
import Footer from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen md:h-screen bg-[#F0F1F3] flex flex-col items-center justify-start md:justify-center overflow-y-auto md:overflow-hidden pt-8 md:pt-0 p-4">
      <Footer />
    </div>
  );
}
4. The Footer Component (src/components/Footer.tsx)
Create this file and structure it strictly with the following inner components and specific Tailwind dimensions/hex codes:
Component 1: LogoIcon
Render a square icon box.
Classes: w-8 h-8 bg-[#31A8FF] rounded-[8px] flex items-center justify-center
SVG Code: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M4 20C4 20 4 14 10 10C16 6 20 4 20 4C20 4 18 8 14 14C10 20 4 20 4 20Z" fill="white" /> <path d="M4 20L10 14" stroke="white" strokeWidth="2" strokeLinecap="round" /> </svg>
Component 2: FooterCard
A massive layered card layout holding the footer directories.
Wrappers:
Main Container: w-full max-w-6xl mx-auto
Outer Gray Body: bg-[#E9EBEE] rounded-[48px] border border-slate-200 shadow-sm overflow-hidden
Inner White Box: bg-white rounded-[40px] m-2 shadow-sm
Content Grid Space (Inside White Box): p-8 md:p-10 lg:p-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12
Grid Columns Layout:
Brand Info (lg:col-span-2 space-y-8):
A row (flex items-center gap-2.5) with <LogoIcon /> and <span className="text-[26px] font-bold tracking-tight text-[#0F172A]">vize</span>
Description: <p className="text-[#64748B] leading-relaxed text-[16px] font-normal max-w-[320px]">Premium strategic solutions designed to elevate your brand presence through advanced marketing.</p>
Socials Group: Map an array of Linkedin, Twitter, Instagram (imported from lucide-react). Make them buttons with classes: w-[44px] h-[44px] flex items-center justify-center rounded-xl border border-slate-100 bg-white shadow-[0_1px_2px_rgba(0,0,0,0.05)] hover:bg-slate-50 transition-all active:scale-95 group. Inside each put the Icon component with className="w-5 h-5 text-slate-800".
Product Column (space-y-6): Header <h4 className="text-[14px] font-medium text-[#94A3B8]">Product</h4>. Links (href="#" target): Features, Solutions, Pricing, Updates. Styling for links: text-[15px] font-medium text-[#1E293B] hover:text-[#31A8FF] transition-colors. Keep in a <ul> with space-y-4.
Science Column (space-y-6): Header Science. Links: Approach, Identity, Research, Metrics. Same link styling.
Company Column (space-y-6): Header Company. Links: About Us, Partners, Careers. Same link styling.
Bottom Legal Bar (Inside Gray Outer Wrap, OUTSIDE of White Box):
Container: px-6 sm:px-12 md:px-16 lg:px-20 py-5 flex flex-col md:flex-row justify-between items-center gap-6 text-[15px]
Left side: <p className="text-[#64748B] font-medium">© 2025 Vize. All rights reserved.</p>
Right side: Flex row (gap-8 text-[#64748B] font-medium items-center) featuring:
<a href="#" className="hover:text-[#1E293B] transition-colors">Legal Center</a>
Vertical Separator: <div className="w-[1px] h-4 bg-slate-300" />
<a href="#" className="hover:text-[#1E293B] transition-colors">User Agreement</a>
Component 3: GlassText
This must be perfectly implemented to work. It uses an absolute hidden SVG defining a filter, paired with Framer Motion.
Container: relative w-full flex items-center justify-center select-none pt-0.
Invisible SVG: <svg className="absolute w-0 h-0" aria-hidden="true" focusable="false">
Filter setup within SVG:
code
Xml
<defs>
  <filter id="glass-effect" x="-50%" y="-50%" width="200%" height="200%">
    <feDropShadow dx="0" dy="4" stdDeviation="6" floodColor="#000000" floodOpacity="0.25" result="outer-shadow"/>
    <feComponentTransfer in="SourceAlpha" result="alpha"><feFuncA type="linear" slope="1" /></feComponentTransfer>
    <feOffset in="alpha" dx="0" dy="4" result="offset-white" />
    <feGaussianBlur in="offset-white" stdDeviation="4" result="blur-white" />
    <feComposite in="alpha" in2="blur-white" operator="out" result="inner-white-mask" />
    <feFlood floodColor="#ffffff" floodOpacity="0.25" result="white-fill" />
    <feComposite in="white-fill" in2="inner-white-mask" operator="in" result="inner-white-final" />
    <feGaussianBlur in="alpha" stdDeviation="6" result="blur-black" />
    <feComposite in="alpha" in2="blur-black" operator="out" result="inner-black-mask" />
    <feFlood floodColor="#000000" floodOpacity="0.25" result="black-fill" />
    <feComposite in="black-fill" in2="inner-black-mask" operator="in" result="inner-black-final" />
    <feMerge>
      <feMergeNode in="outer-shadow" />
      <feMergeNode in="SourceGraphic" />
      <feMergeNode in="inner-white-final" />
      <feMergeNode in="inner-black-final" />
    </feMerge>
  </filter>
</defs>
Motion Element placed underneath the SVG code:
<motion.div initial={{ opacity: 0, scale: 0.98 }} whileInView={{ opacity: 1, scale: 1 }} transition={{ duration: 1.8, ease: [0.16, 1, 0.3, 1] }} className="relative">
Text Element logic: <h1 className="text-[min(25vw,400px)] font-bold tracking-normal leading-none select-none text-white px-4" style={{ filter: 'url(#glass-effect)' }}>vize</h1>
Final Default Export for Footer.tsx
code
Tsx
export default function Footer() {
  return (
    <footer className="w-full flex flex-col items-center gap-0">
      <FooterCard />
      <GlassText />
    </footer>
  );
}
```

---

## 45. HAUL!

- **Category**: Footer Section
- **Type**: footer
- **Page Type**: hero
- **ID**: `haul-footer`

```
Build a React functional component using Tailwind CSS, `motion/react` for animations, and `lucide-react` for icons.

**1. Typography & Setup:**
- Import the "Inter" font from Google Fonts (weights 400, 500, 600, 700) and set it as the default sans-serif font in the Tailwind config/CSS.
- The overall background of the page should be `#f8f9fa`.

**2. Top Spacer Section (View Below):**
- Create a section at the top of the page. Height should be `50vh` (on mobile/lg) and `30vh` (on md screens).
- Background color: `#FDFDFD`.
- Center a text element that says "View Below". The text should be `text-gray-300`, small font, bold, uppercase, with wide `tracking-[0.5em]`.
- Animate this text with Framer Motion to fade in from `opacity: 0` to `opacity: 1`.

**3. Main Parallax Container:**
- Below the spacer, create a main full-viewport-height (`h-screen`) section.
- Set its background image to: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260430_115327_3f256636-9e63-4885-8d0b-09317dc2b0a5.png&w=1280&q=85`
- Make sure the background covers the container (`bg-cover bg-center`) and set `overflow-hidden` with `relative` positioning.
- Set up a Framer Motion `useScroll` target on this container. Map the `scrollYProgress` from `[0, 1]` to `[-50, 150]` using `useTransform`. Apply this transformed y-value to the foreground truck image layer (described below).

**4. The Top-Aligned Footer Card:**
- Position a container `absolute top-0 w-full` inside the main parallax section. Give it top padding (`pt-12` mobile/lg, `pt-24` tablet).
- Inside, create a card constrained to `max-w-7xl mx-auto`.
- Card Styling: `bg-white/95`, `backdrop-blur-sm`, `shadow-xl`, rounded corners (`rounded-2xl` mobile, `rounded-3xl` desktop), `overflow-hidden`.
- Animation: The card should slide down and fade in (`initial={{ opacity: 0, y: -20 }}`, `animate={{ opacity: 1, y: 0 }}`, duration 0.8s easeOut).
- **Footer Content (Top Half):**
  - Use a flex row layout (flex-col on mobile, flex-row on md+) with spread space.
  - **Logo Area**: Include an orange square (`bg-orange-500`, 40x40px mobile, 48x48px desktop, rounded-lg, shadow-inner, p-2). Inside the square, place an SVG with viewBox "0 0 256 256" and this exact white path: `d="M 228 0 C 172.772 0 128 44.772 128 100 L 128 0 L 0 0 L 0 28 C 0 83.228 44.772 128 100 128 L 0 128 L 0 256 L 28 256 C 83.228 256 128 211.228 128 156 L 128 256 L 256 256 L 256 228 C 256 172.772 211.228 128 156 128 L 256 128 L 256 0 Z"`. Next to the logo block, add the text "HAUL!" (`text-gray-900`, 2xl/3xl, font-bold, tracking-tighter).
  - **Links Area**: Display 3 columns of links using flex. Layout: `Company` (Founding, Platform, Testify), `Mobile` (Get Apple App, Get Google App), `Contracts` (Private Data, User Consent). Section headers should be uppercase, tracking-widest, text-sm, bold. Link items should be gray-500, font-medium, and hover to `orange-600` with transition.
- **Footer Content (Bottom Bar):**
  - Add a top border (`border-gray-100`) and use a solid white background (`bg-white`).
  - Layout: flex, space between, aligning text to the left and social icons to the right. 
  - Text: "© 2026 HAUL! All Rights Reserved" (text-sm, gray-500, medium).
  - **Social Icons**: Map through an array of icons imported from `lucide-react`: Facebook, Twitter, Instagram, Linkedin (w-5 h-5). Wrap them in `a` tags shaped as 40x40px circles with `border-gray-100`. On hover, they should turn `bg-orange-500` with white text and an `orange-500` border (transition all duration-300).

**5. Background Truck Parallax Layer:**
- Add a `motion.div` placed absolutely at the bottom of the container (`absolute inset-x-0 bottom-0 h-full`).
- Add standard pointer-events-none and z-20.
- Ensure the `y` axis style is tied to the `useTransform` created in step 3 so it scrolls at a different speed than the background.
- Inside, place an image with `src="https://roof-wish-40038865.figma.site/_components/v2/f31fd17907ce60745d45e83a61d44fd3810d5f25/truck_1.8c4bff83.png"`.
- Image styling: `w-full h-full object-contain object-bottom origin-bottom`. Add scale responsive classes (`scale-[1.5]` mobile, `scale-110` sm, `scale-[2.0]` md, `scale-105` lg) to ensure the truck fits properly on various screen widths.
```

---

## 46. Axion About

- **Category**: About
- **Type**: about
- **Page Type**: hero
- **ID**: `axion-about`

```
Build a single React component for an "About" section using Tailwind CSS. Use `lucide-react` for the ArrowRight icon. System font stack only (no custom fonts). Match every detail exactly:

---

### Outer wrapper

`<section>` with `bg-white pt-16 sm:pt-20 lg:pt-32 pb-12 sm:pb-16 lg:pb-24 overflow-hidden`. Inner container: `max-w-[1440px] mx-auto`.

---

### Badge row

`px-5 sm:px-8 lg:px-12 flex items-center gap-3 mb-6 sm:mb-8`.

- **Numbered circle:** `w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-gray-900 text-white flex items-center justify-center text-[11px] sm:text-[12px] font-semibold`. Displays "1".
- **Pill label:** Text "Introducing Axion". `text-[12px] sm:text-[13px] font-medium rounded-full px-3 sm:px-4 py-1 sm:py-1.5`. No border, no background.

---

### Heading

`<h2>` with `px-5 sm:px-8 lg:px-12 text-[clamp(1.5rem,4vw,3.2rem)] font-medium leading-[1.12] tracking-[-0.02em] text-gray-900 mb-12 sm:mb-16 lg:mb-28`.

Text: "Strategy-led creatives, delivering / results in digital and beyond." - the `/` represents a line break that is `<br className="hidden sm:block" />` with a `<span className="sm:hidden"> </span>` fallback space before it (so on mobile it reads as one flowing line, on sm+ it breaks into two lines).

---

### Content area - MOBILE / TABLET layout (lg:hidden)

Wrapper: `lg:hidden px-5 sm:px-8`.

1. **Paragraph:** "Through research, creative thinking and iteration we help growing brands realize their digital full potential." - `text-[15px] sm:text-[17px] leading-[1.6] font-medium text-gray-900 mb-6`.

2. **CTA button** (inside a `mb-8` wrapper): Orange button (`bg-[#F26522] hover:bg-[#e05a1a]`) with text "About our studio", `text-white text-[13px] sm:text-[14px] font-medium rounded-full pl-5 sm:pl-6 pr-2 py-2 flex items-center gap-3`. Contains:
   - **Text-roll hover animation:** The button text is inside `overflow-hidden h-[20px]` > `flex flex-col` container. The text is duplicated (two identical `h-[20px] flex items-center` spans). On `group-hover`, the flex-col translates `-translate-y-1/2` with `transition-transform duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]`.
   - **Arrow circle:** White circle `bg-white w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center`. Contains `ArrowRight` from lucide-react (size 14), `text-[#F26522]`, starts at `-rotate-45`, on `group-hover` rotates to `rotate-0` (same duration-500 easing). The entire button has `className="group"`.

3. **Images:** `flex flex-col sm:flex-row gap-4 sm:gap-5`.
   - First: `sm:w-[45%]`, `<img>` with `w-full aspect-[438/346] rounded-xl sm:rounded-2xl object-cover`.
   - Second: `sm:w-[55%]`, `<img>` with `w-full aspect-[900/600] rounded-xl sm:rounded-2xl object-cover`.

---

### Content area - DESKTOP layout (hidden lg:grid)

Wrapper: `hidden lg:grid grid-cols-[26%_1fr_48%] items-end gap-6 xl:gap-8 px-5 sm:px-8 lg:px-12`.

- **Left column** (`self-end`): Small image, `w-full aspect-[438/346] rounded-2xl object-cover`.
- **Center column** (`self-start flex flex-col justify-end`):
  - Paragraph: `text-[16px] xl:text-[18px] leading-[1.65] font-medium text-gray-900 whitespace-nowrap mb-6`. Text with explicit `<br/>` tags: "Through research, creative thinking`<br/>`and iteration we help growing brands`<br/>`realize their digital full potential."
  - Same orange CTA button as mobile (identical text-roll animation).
- **Right column** (`self-end`): Large image, `w-full aspect-[3/2] rounded-2xl object-cover`.

---

### Image URLs

- **Small image:** `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090123_74be96d4-9c1b-40cf-932a-96f4f4babed3.png&w=1280&q=85`
- **Large image:** `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260516_090133_c157d30b-a99a-4477-bec1-a446149ec3f2.png&w=1280&q=85`

---

### Technical details

- **Framework:** React 18 + TypeScript + Tailwind CSS 3.4 (default config, no custom theme extensions)
- **Icons:** `ArrowRight` from `lucide-react`
- **Font:** System default (no custom font loaded)
- **All hover animations:** `duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]`
- **Max content width:** 1440px, centered with `mx-auto`
- **Responsive breakpoints:** Default Tailwind (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)

---
```

---

## 47. 404 Planet

- **Category**: 404
- **Type**: 404
- **Page Type**: hero
- **ID**: `404-planet`

```
Build a full-page 404 error page for a hosting company called "NEXOVA". The entire page is a single viewport-height layout with a looping background video, a navigation bar, a centered hero/404 section, and a multi-column footer. Use React + Tailwind CSS + Lucide React icons. No other UI libraries.

---

**FONT**

Load "Helvetica Now Var" via this stylesheet in `index.html`:
```
<link href="https://db.onlinewebfonts.com/c/e66905e07608167a84e6ad52f638c3c6?family=Helvetica+Now+Var" rel="stylesheet">
```
Apply it globally on the root container via inline style:
```
fontFamily: '"Helvetica Now Var", Helvetica, Arial, sans-serif'
```

---

**BACKGROUND VIDEO**

A `<video>` element with `autoPlay muted loop playsInline`, positioned `absolute inset-0 w-full h-full object-cover` behind all content. The video source URL is:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260613_180732_a54afbf6-b30d-470e-861f-669871f09f67.mp4
```
This is a cinematic dark-blue Earth-from-space shot.

---

**LAYOUT STRUCTURE**

The root is `relative min-h-screen flex flex-col`. Inside it:
1. The background `<video>` (absolute, behind everything)
2. A content wrapper `relative z-10 flex flex-col min-h-screen` containing nav, hero, and footer

---

**NAVIGATION BAR**

- Flex row, `items-center justify-between`, padding `px-6 md:px-12 lg:px-16 py-5`
- **Logo (left):** A custom SVG icon (4 quarter-circle leaf shapes forming a circle, white fill, `w-8 h-8`) next to the text "NEXOVA" in `text-white text-xl font-bold tracking-wider`. The exact SVG path is:
  ```
  M480 240a240 240 0 0 0-240 240 240 240 0 0 0 240-240Z
  M240 0A240 240 0 0 0 0 240 240 240 0 0 0 240 0Z
  M480 240A240 240 0 0 0 240 0a240 240 0 0 0 240 240Z
  M240 480A240 240 0 0 0 0 240a240 240 0 0 0 240 240Z
  ```
  viewBox `0 0 480 480`
- **Desktop nav links (center):** Hidden below `lg`. Links: Domain, Servers, Cloud, Managed, Email, Privacy. Styled `text-white/80 hover:text-white text-sm tracking-wide` with 200ms color transition, `gap-8`.
- **Login button (right):** Hidden below `lg`. Gradient button `bg-gradient-to-r from-emerald-400 to-cyan-500`, white text, `text-sm font-semibold px-6 py-2.5 rounded-full`. Text "LOG IN" with a Lucide `ArrowRight` icon (w-4 h-4) beside it.
- **Mobile hamburger:** Visible below `lg` breakpoint. A button with `z-[60]` showing Lucide `Menu` / `X` icons that cross-fade with rotation: the active icon is `opacity-100 rotate-0 scale-100`, the inactive is `opacity-0 rotate-90 scale-75` (or `-rotate-90`), all with `transition-all duration-300`.

---

**MOBILE MENU**

Uses two state variables: `mobileMenuOpen` (controls mount) and `menuVisible` (controls animation). When opening, `mobileMenuOpen` is set true, then `menuVisible` becomes true via `useEffect`. When closing, `menuVisible` is set false first, then after a 500ms timeout `mobileMenuOpen` is set false.

- **Backdrop:** Fixed overlay `inset-0 z-40 bg-black/40 backdrop-blur-md`, fades in/out with 400ms opacity transition. Clicking it closes the menu.
- **Menu panel:** Absolutely positioned `left-0 right-0 top-[68px] z-50`. Contains a backdrop-only blur layer (`backdrop-blur-xl`, no background color, `rounded-b-2xl`) and content on top (`relative z-10`).
- **Menu items:** Each nav link is centered, `text-lg sm:text-xl font-light tracking-[0.08em]`, `text-white/80 hover:text-white`. They stagger-animate in: each link has a `transitionDelay` of `350 + (index * 50)ms` when appearing (0ms when disappearing), transitioning opacity 0->1 and translateY 12px->0 over 400ms with `ease-out`.
- **Login button:** Same gradient style as desktop, appears last in the stagger sequence with delay `350 + (linkCount * 50)ms`.

---

**HERO / 404 SECTION**

Centered vertically and horizontally in the remaining space: `flex-1 flex flex-col items-center justify-center text-center px-4 sm:px-6 py-12 sm:py-16 md:py-0`.

1. **Subtitle lines (two h1 tags):**
   - "This page seems to have" and "slipped beyond our reach :/"
   - Both: `text-white/80 text-lg xs:text-2xl sm:text-3xl md:text-5xl font-light leading-snug tracking-tight`
   - First line: `mb-1 sm:mb-2`, second line: `mb-8 sm:mb-12`

2. **Giant "404" text:**
   - Wrapped in a `relative mb-8 sm:mb-12 w-full flex justify-center overflow-visible` div
   - The `<span>`: `text-[80px] xs:text-[100px] sm:text-[140px] md:text-[200px] lg:text-[260px] font-black text-white leading-none tracking-tighter select-none`
   - Has class `four-oh-four` which applies this CSS glow:
     ```css
     .four-oh-four {
       text-shadow: 0 0 80px rgba(255,255,255,0.3), 0 0 160px rgba(255,255,255,0.1);
     }
     ```

3. **"Return to Main Page" button:**
   - An `<a>` tag with class `liquid-glass` (glassmorphism effect) + `text-white text-[10px] xs:text-xs sm:text-sm tracking-[0.15em] sm:tracking-[0.2em] font-medium px-6 sm:px-8 py-3 sm:py-3.5 rounded-full uppercase`
   - The `liquid-glass` CSS class:
     ```css
     .liquid-glass {
       background: rgba(255, 255, 255, 0.01);
       background-blend-mode: luminosity;
       backdrop-filter: blur(4px);
       -webkit-backdrop-filter: blur(4px);
       border: none;
       box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
       position: relative;
       overflow: hidden;
     }
     .liquid-glass::before {
       content: '';
       position: absolute;
       inset: 0;
       border-radius: inherit;
       padding: 1.4px;
       background: linear-gradient(180deg,
         rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
         rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
         rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
       -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
       -webkit-mask-composite: xor;
       mask-composite: exclude;
       pointer-events: none;
     }
     ```

---

**FOOTER**

Positioned at the bottom: `relative z-10 px-4 sm:px-6 md:px-12 lg:px-16 pb-8 sm:pb-10 pt-10 sm:pt-16`.

Grid: `grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6 sm:gap-8 lg:gap-6`.

**4 link columns** (iterated from data):
- SERVERS: Web Servers, VPS Servers, Cloud Servers, Managed Instances, Bare Metal
- DOMAINS: Find Domain, Move Domains, DNS Manager, Domain Costs
- HELP US: Open a Ticket, FAQs, Docs, Tutorials, Forum
- ABOUT: Our Story, Leadership Team, Press Room, We Hire, Alliance, Blog

Each column title: `text-white text-[10px] sm:text-xs font-bold tracking-[0.15em] mb-3 sm:mb-4`. Links: `text-white/50 hover:text-white/80 text-[10px] sm:text-xs` with 200ms transition, in a `space-y-2 sm:space-y-2.5` list.

**Newsletter + Social column** (`col-span-2 lg:col-span-2`):
- Heading "JOIN FOR EXCLUSIVE DEALS" (same title style)
- Email input + "SEND IT" button side by side in a flex row, `max-w-sm`. Input: white bg, `rounded-l-md`, placeholder "Type your email to sign up". Button: same emerald-to-cyan gradient, `rounded-r-md`, `font-bold tracking-wider`.
- Heading "CONNECT" with `mt-5 sm:mt-6 mb-3`
- 6 social icons (Lucide: Facebook, Twitter, Dribbble, Youtube, Linkedin, Instagram), each `w-4 h-4`, `text-white/50 hover:text-white`, `gap-3`.

---

**RESPONSIVE BREAKPOINTS**
- `xs` is not a default Tailwind breakpoint -- if used, it needs to be added, or replaced with `sm`. The design uses mobile-first sizing that scales up at `sm` (640px), `md` (768px), and `lg` (1024px).
- Mobile: 2-col footer grid, hamburger menu, smaller text sizes
- Tablet (md): 4-col footer grid so newsletter sits beside the last link column
- Desktop (lg): 6-col footer grid, full horizontal nav, login button visible
```

---

## 48. Liquid Glass CTA

- **Category**: CTA
- **Type**: cta
- **Page Type**: hero
- **ID**: `liquid-glass-cta`

```
Build a "CTA + Footer" section component for a React + Vite + Tailwind CSS project. This is a cinematic full-width call-to-action section with an HLS video background, centered text, two CTA buttons, and a minimal footer bar at the bottom. Black background, white text, liquid glassmorphism effects.

---

### FONTS (import in index.css or HTML head)

```
https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&display=swap
```

- Headings: `Instrument Serif` italic -- Tailwind class `font-heading`
- Body: `Barlow` -- Tailwind class `font-body`

Add to `tailwind.config.ts` under `theme.extend.fontFamily`:
```js
heading: ["'Instrument Serif'", "serif"],
body: ["'Barlow'", "sans-serif"],
```

Base styles in `index.css`:
```css
body {
  font-family: 'Barlow', sans-serif;
  background: #000;
  color: #fff;
}
h1, h2, h3 {
  font-family: 'Instrument Serif', serif;
}
```

---

### LIQUID GLASS CSS (add to index.css inside `@layer components`)

```css
@layer components {
  .liquid-glass-strong {
    background: rgba(255, 255, 255, 0.01);
    background-blend-mode: luminosity;
    backdrop-filter: blur(50px);
    -webkit-backdrop-filter: blur(50px);
    border: none;
    box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.05),
      inset 0 1px 1px rgba(255, 255, 255, 0.15);
    position: relative;
    overflow: hidden;
  }

  .liquid-glass-strong::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1.4px;
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.5) 0%,
      rgba(255, 255, 255, 0.2) 20%,
      rgba(255, 255, 255, 0) 40%,
      rgba(255, 255, 255, 0) 60%,
      rgba(255, 255, 255, 0.2) 80%,
      rgba(255, 255, 255, 0.5) 100%
    );
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
  }
}
```

The `::before` pseudo-element uses a mask-composite trick to render a thin glowing gradient border that fades out in the middle of each side.

---

### DEPENDENCIES

```
npm install lucide-react hls.js
```

- `ArrowUpRight` icon from `lucide-react`
- `hls.js` for streaming the Mux HLS video

---

### HLS VIDEO URL (Mux)

```
https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8
```

This is an HLS stream that requires `hls.js` to play in non-Safari browsers. Safari supports HLS natively via `<video>`.

---

### EXACT COMPONENT CODE

```tsx
import { useEffect, useRef } from "react";
import { ArrowUpRight } from "lucide-react";
import Hls from "hls.js";

const CtaFooter = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const src = "https://stream.mux.com/8wrHPCX2dC3msyYU9ObwqNdm00u3ViXvOSHUMRYSEe5Q.m3u8";

    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(video);
      return () => hls.destroy();
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = src;
    }
  }, []);

  return (
    <section className="relative py-32 px-6 md:px-16 lg:px-24 text-center overflow-hidden">
      {/* Background HLS Video */}
      <video
        ref={videoRef}
        autoPlay
        loop
        muted
        playsInline
        className="absolute inset-0 w-full h-full object-cover z-0"
      />

      {/* Top fade */}
      <div
        className="absolute top-0 left-0 right-0 z-[1] pointer-events-none"
        style={{ height: '200px', background: 'linear-gradient(to bottom, black, transparent)' }}
      />
      {/* Bottom fade */}
      <div
        className="absolute bottom-0 left-0 right-0 z-[1] pointer-events-none"
        style={{ height: '200px', background: 'linear-gradient(to top, black, transparent)' }}
      />

      {/* Content */}
      <div className="relative z-10">
        <h2 className="text-5xl md:text-6xl lg:text-7xl font-heading italic text-white tracking-tight leading-[0.85] max-w-3xl mx-auto mb-4">
          Your next website starts here.
        </h2>
        <p className="text-white/60 font-body font-light text-sm md:text-base max-w-xl mx-auto mb-8">
          Book a free strategy call. See what AI&#8209;powered design can do. No commitment, no pressure. Just possibilities.
        </p>
        <div className="flex items-center justify-center gap-6">
          <button className="liquid-glass-strong rounded-full px-6 py-3 text-sm font-medium text-white flex items-center gap-2 hover:bg-white/10 transition-all font-body">
            Book a Call
            <ArrowUpRight className="h-5 w-5" />
          </button>
          <button className="bg-white text-black rounded-full px-6 py-3 text-sm font-medium flex items-center gap-2 hover:bg-white/90 transition-colors font-body">
            View Pricing
            <ArrowUpRight className="h-4 w-4" />
          </button>
        </div>

        {/* Footer */}
        <div className="mt-32 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/40 font-body font-light text-xs">
            &copy; 2026 Studio. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            {["Privacy", "Terms", "Contact"].map((link) => (
              <a key={link} href="#" className="text-white/40 hover:text-white/70 font-body font-light text-xs transition-colors">
                {link}
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default CtaFooter;
```

---

### SECTION STRUCTURE BREAKDOWN

```
<section>  (relative, py-32, px-6 md:px-16 lg:px-24, text-center, overflow-hidden)
  |
  +-- <video>  (absolute inset-0, full cover, z-0, autoPlay loop muted playsInline)
  |
  +-- Top gradient fade  (absolute top-0, 200px tall, black->transparent, z-[1])
  +-- Bottom gradient fade  (absolute bottom-0, 200px tall, transparent<-black, z-[1])
  |
  +-- Content wrapper  (relative z-10)
       |
       +-- <h2> heading
       +-- <p> subtext
       +-- Button row (flex, centered, gap-6)
       |    +-- "Book a Call" (liquid-glass-strong, rounded-full)
       |    +-- "View Pricing" (bg-white text-black, rounded-full)
       |
       +-- Footer bar (mt-32, border-t border-white/10)
            +-- Copyright (left)
            +-- Links: Privacy, Terms, Contact (right)
```

---

### HLS VIDEO SETUP PATTERN

The `useEffect` hook initializes `hls.js` for non-Safari browsers and falls back to native HLS for Safari:

1. Check `Hls.isSupported()` -- if true, create an `Hls` instance, load the `.m3u8` source, attach to the `<video>` element
2. If not supported but the browser can play `application/vnd.apple.mpegurl` (Safari), set `video.src` directly
3. Cleanup: `hls.destroy()` on unmount

The `<video>` element uses `autoPlay loop muted playsInline` -- all four attributes are required for autoplay to work across browsers (especially mobile).

---

### VIDEO OVERLAY FADE PATTERN

Two absolutely positioned `<div>` elements create black gradient fades at the top and bottom edges, making the video blend seamlessly into the surrounding black background:

- **Top fade**: `height: 200px`, `background: linear-gradient(to bottom, black, transparent)`, `z-[1]`, `pointer-events-none`
- **Bottom fade**: `height: 200px`, `background: linear-gradient(to top, black, transparent)`, `z-[1]`, `pointer-events-none`

Content sits at `z-10` above both the video and the fades.

---

### RESPONSIVE BEHAVIOR

| Breakpoint | Heading size | Padding | Footer layout |
|---|---|---|---|
| Mobile (default) | `text-5xl` | `px-6` | Stacked column (`flex-col`) |
| Tablet (`md:`) | `text-6xl` | `px-16` | Horizontal row (`md:flex-row`) |
| Desktop (`lg:`) | `text-7xl` | `px-24` | Horizontal row |

- Button row always horizontal (`flex items-center justify-center gap-6`), buttons stack naturally if viewport is very narrow
- Footer: `flex-col md:flex-row` -- copyright and links stack on mobile, sit side-by-side on tablet+
- Subtext constrained to `max-w-xl mx-auto`
- Heading constrained to `max-w-3xl mx-auto`

---

### TYPOGRAPHY DETAILS

| Element | Classes |
|---|---|
| Heading | `text-5xl md:text-6xl lg:text-7xl font-heading italic text-white tracking-tight leading-[0.85] max-w-3xl mx-auto mb-4` |
| Subtext | `text-white/60 font-body font-light text-sm md:text-base max-w-xl mx-auto mb-8` |
| Glass button text | `text-sm font-medium text-white font-body` |
| Solid button text | `text-sm font-medium` (inherits `text-black` from `bg-white text-black`) |
| Copyright | `text-white/40 font-body font-light text-xs` |
| Footer links | `text-white/40 hover:text-white/70 font-body font-light text-xs transition-colors` |

---

### BUTTON DETAILS

**Primary CTA ("Book a Call"):**
`liquid-glass-strong rounded-full px-6 py-3 text-sm font-medium text-white flex items-center gap-2 hover:bg-white/10 transition-all font-body`
- Glass background with gradient border via `::before`
- `ArrowUpRight` icon at `h-5 w-5`

**Secondary CTA ("View Pricing"):**
`bg-white text-black rounded-full px-6 py-3 text-sm font-medium flex items-center gap-2 hover:bg-white/90 transition-colors font-body`
- Solid white background, black text
- `ArrowUpRight` icon at `h-4 w-4` (slightly smaller than the primary)

---

### EXACT TEXT CONTENT

**Heading**: "Your next website starts here."
**Subtext**: "Book a free strategy call. See what AI-powered design can do. No commitment, no pressure. Just possibilities."
**Button 1**: "Book a Call"
**Button 2**: "View Pricing"
**Copyright**: "(c) 2026 Studio. All rights reserved."
**Footer links**: "Privacy", "Terms", "Contact"

---

### PARENT CONTEXT

This section sits on a `bg-black` parent container as the last section of the page. The top gradient fade blends the video into the section above (which also has a black background). The footer bar is part of this same component -- there is no separate footer component.
```

---

## 49. LaunchEx About

- **Category**: About
- **Type**: about
- **Page Type**: hero
- **ID**: `launchex-about`

```
--

**Prompt to recreate the About section:**

> Build a full-viewport "About the Founders" section using React with Tailwind CSS and lucide-react for icons. This is a single `<section>` with the following exact specifications:
>
> **Section container:**
> - `id="about"`
> - Background color: `#F0F5F7`
> - `min-height: 100vh`
> - Position relative
> - Padding: `py-20 sm:py-28 px-6 sm:px-10`
> - Uses `flex flex-col justify-center` to vertically center content
>
> **Inner wrapper:**
> - `max-w-7xl mx-auto`
>
> **Top row -- heading + description (side by side on desktop):**
> - A flex container: `flex flex-col lg:flex-row items-start justify-between gap-10 lg:gap-20`
> - All text color: `#154359`
>
> **Left side -- Section heading:**
> - `<h2>` with text `About` on line 1, `the founders` on line 2 (separated by `<br />`)
> - Uses custom font class `.font-firs` (font-family: `'TT Firs Neue', 'Inter', system-ui, sans-serif`)
> - Font sizes: `text-[36px] sm:text-[48px] lg:text-[54px]`
> - `font-semibold uppercase tracking-tight leading-[0.95]`
>
> **Right side -- Description block:**
> - `flex flex-col max-w-xl`
> - Text container: `text-[17px] sm:text-[18px] leading-[1.5]`, color `#154359`
> - Paragraph 1: `"Launchex.Hub is a platform that is part of a portfolio of companies Launchex, for sourcing and showcasing groundbreaking innovations."`
> - Paragraph 2: `"Launchex.Hub's mission is to offer every local-language innovator the chance to reshape our world with their pioneering creation."` -- with `mt-4` spacing
> - Below paragraphs, an external link:
>   - `<a>` tag pointing to `https://base.launchex.vc/`, opens in new tab (`target="_blank" rel="noreferrer"`)
>   - `group inline-flex items-center gap-4 mt-6 text-[14px] font-medium`, color `#154359`
>   - Text: `"Launchex.Hub website"`
>   - Next to it, an icon button: `flex items-center justify-center w-8 h-8 border`, border color `#154359`, with `transition-transform group-hover:-translate-y-0.5`
>   - The icon button uses a chamfered clip-path: `polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px)`
>   - Inside the button: `<ArrowUpRight>` from lucide-react, `w-3.5 h-3.5`, `strokeWidth={2}`
>
> **Stats cards grid (below the heading row):**
> - `mt-14 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5`
> - Contains 3 stat cards with this exact data:
>   1. value: `"7+ years"`, text: `"Launchex has served the market, guiding ventures and their journeys"`, image: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260514_154203_6c6f94dc-a07e-4ba5-8688-106f01ccd2c8.png&w=1280&q=85`, offset: false
>   2. value: `"15000+"`, text: `"innovation ventures moved through the Launchex pipeline"`, image: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260514_154151_45c62c60-3bcc-4f21-8f9d-03722ebb5df8.png&w=1280&q=85`, offset: true
>   3. value: `"120+"`, text: `"accelerator sessions delivered by Launchex across Eastern Europe"`, image: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260514_152238_24ec8db4-d728-4739-bb30-e985533e9637.png&w=1280&q=85`, offset: false
>
> **Each stat card:**
> - Outer wrapper: `relative w-full h-[280px] sm:h-[340px]`
> - The 2nd card (index 1, offset: true) gets `lg:mt-24` to create a staggered effect
> - Outer wrapper has `backgroundColor: 'rgba(255, 255, 255, 0.8)'` and `padding: '1.5px'` (acts as a thin white border)
> - Each card uses a unique polygon clip-path for chamfered/angular corners:
>   - Card 1: `polygon(64px 0, calc(100% - 14px) 0, calc(100% - 4px) 4px, 100% 14px, 100% calc(100% - 14px), calc(100% - 4px) calc(100% - 4px), calc(100% - 14px) 100%, 14px 100%, 4px calc(100% - 4px), 0 calc(100% - 14px), 0 64px)` -- large chamfer on top-left
>   - Card 2: `polygon(0 14px, 4px 4px, 14px 0, calc(100% - 64px) 0, 100% 64px, 100% calc(100% - 14px), calc(100% - 4px) calc(100% - 4px), calc(100% - 14px) 100%, 64px 100%, 0 calc(100% - 64px))` -- large chamfer on top-right and bottom-left
>   - Card 3: `polygon(0 14px, 4px 4px, 14px 0, calc(100% - 64px) 0, 100% 64px, 100% calc(100% - 64px), calc(100% - 64px) 100%, 14px 100%, 4px calc(100% - 4px), 0 calc(100% - 14px))` -- large chamfer on top-right, bottom-right
> - The same clip-path is applied to both the outer div and the inner image div (creating an inset border effect)
> - Inner div: `relative w-full h-full overflow-hidden bg-cover bg-center`, with the card's image as `backgroundImage`, `mixBlendMode: 'Normal'`
>
> **Text overlay inside each card:**
> - Positioned absolutely with different placements per card:
>   - Card 1: `left-6 right-6 bottom-6`
>   - Card 2: `left-6 bottom-20`
>   - Card 3: `left-6 right-28 bottom-6`
> - All have `max-w-[66%]`
> - The stat value uses `.font-firs font-semibold uppercase leading-none text-[36px] sm:text-[52px]`
> - Value text has a gradient fill: `linear-gradient(294deg, #185B7B 20%, #4BBDF0)` applied via `background`, `WebkitBackgroundClip: 'text'`, `backgroundClip: 'text'`, `color: 'transparent'`
> - Description text: `mt-3 text-[14px] leading-[1.4]`, color `#154359`
>
> **Bottom fade overlay:**
> - `pointer-events-none absolute inset-x-0 bottom-0 h-40 sm:h-56 z-10`
> - Background: `linear-gradient(to bottom, rgba(240, 245, 247, 0) 0%, rgba(240, 245, 247, 0.7) 60%, #F0F5F7 100%)` -- fades to the same background color
>
> **Fonts required in CSS:**
> ```css
> html, body {
>   font-family: 'Inter', system-ui, -apple-system, sans-serif;
>   -webkit-font-smoothing: antialiased;
> }
> .font-firs {
>   font-family: 'TT Firs Neue', 'Inter', system-ui, sans-serif;
> }
> ```
>
> **Color palette used:**
> - Section background: `#F0F5F7`
> - All text: `#154359` (dark teal/navy)
> - Card outer background/border: `rgba(255, 255, 255, 0.8)`
> - Stat value gradient: `#185B7B` to `#4BBDF0` at 294deg
> - Link icon border: `#154359`
> - Bottom gradient: fades to `#F0F5F7`
>
> **Key design details:**
> - The stat cards use CSS `clip-path` polygons (not border-radius) for angular/chamfered corner shapes -- each card has a different polygon creating visual variety
> - The 1.5px padding on the outer wrapper + white background creates the appearance of a thin white border inside the clip-path
> - The 2nd card is offset downward by `lg:mt-24` to create a staggered/masonry feel on desktop
> - Background images are loaded via inline `backgroundImage` style, not `<img>` tags
> - The external link arrow icon sits inside a small chamfered square button using clip-path
> - Responsive: cards stack 1-column on mobile, 2-column on `md:`, 3-column on `lg:`
> - No animations beyond the hover lift on the external link icon button (`group-hover:-translate-y-0.5`)

---
```

---

## 50. Creative Studio

- **Category**: Agency
- **Type**: hero
- **Page Type**: hero
- **ID**: `creative-studio`

```
Build a full-screen hero section using React, Tailwind CSS, Framer Motion, and Lucide React icons. Use the Inter font. The page is fully mobile-responsive. Here are the exact specifications:

---

**BACKGROUND:**
- A full-screen autoplaying, looping, muted video covering the entire viewport as a background.
- Video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260517_222138_3e3205be-3364-417b-a64a-bfe087acbec4.mp4`
- The video is positioned absolute, inset-0, with `object-cover` to fill the viewport.

---

**COLOR:**
- Accent color: `#5E0ED7` (deep purple). Used for the logo dot, the "+" symbols in stats, and the CTA link text.
- All body text is black (#000).

---

**FONT:**
- Font family: `'Inter', sans-serif` applied to the root container.
- All text is uppercase with wide letter-spacing (`tracking-widest` or `tracking-wide`).
- Font weights: 600 (semibold) throughout.

---

**LAYOUT (flex column, min-h-screen):**
The page is a flex column with three vertical sections:
1. **Nav** (top, fixed height)
2. **Stats row** (flex-1, vertically centered, right-aligned)
3. **Bottom content** (pinned to bottom with padding)

---

**NAVIGATION BAR:**
- Horizontal flex, items centered, justified between. Padding: `px-5 sm:px-8 md:px-12 pt-5 md:pt-6`.
- **Left:** A circular logo — 32px round div with 2px border in accent color, containing a 10px solid circle in accent color.
- **Center (hidden on mobile, visible md+):** Four nav links: "Story", "Expertise", "Studios", "Feedback". Text: 14px, font-semibold, tracking-widest, uppercase, black.
- **Right:** A 36px round black button with three horizontal white lines (hamburger icon — three `span` elements, each `w-4 h-0.5 bg-white` with `gap-1`). This opens the mobile menu on click.

---

**MOBILE MENU OVERLAY:**
- Triggered by hamburger click. Fixed, full-screen, z-50, white background.
- Top row: same logo (left) and a 36px round black close button with an X icon (right).
- Below: vertical list of the 4 nav links at `text-3xl`, font-semibold, tracking-widest, uppercase, with `gap-8` and `mt-16`.
- Bottom (mt-auto): "Work With Us" CTA in accent color with ArrowUpRight icon, `text-xl`.

---

**STATS ROW (middle section):**
- Container: `flex-1 flex items-center justify-end`, with same horizontal padding. `py-8 md:py-0`.
- Three stat items in a horizontal row with `gap-5 sm:gap-8 md:gap-10`, each right-aligned:
  - **+300** / CRAFTED BRANDS
  - **+200** / DIGITAL PRODUCTS
  - **+100** / VENTURES FUNDED
- Number styling: `fontSize: clamp(1.5rem, 5vw, 3.5rem)`, weight 600. The "+" is rendered separately in accent color at 0.5em size. The number is black.
- Label: `text-[10px] sm:text-xs md:text-sm`, font-semibold, tracking-widest, uppercase, black, `whitespace-pre-line leading-tight` (each label has a line break between the two words).

---

**BOTTOM SECTION:**
- Padding: `px-5 sm:px-8 md:px-12 pb-8 md:pb-12`. Flex column with `gap-6 md:gap-12`.

**Row A (tagline + CTA):**
- Flex row, items-center, justify-between, gap-4.
- **Left:** Small uppercase tagline paragraph: "Shaping Bold / Visions Into Power / For Your Tribe" (with `<br />` line breaks). Text: `text-[10px] sm:text-xs md:text-sm`, font-semibold, tracking-widest, max-width `130px sm:160px md:max-w-xs`.
- **Right:** CTA link "Work With Us" with ArrowUpRight icon. Text: `text-base sm:text-xl md:text-2xl`, accent color, weight 600, `whitespace-nowrap`. Icon: 18px on mobile, 22px on sm+.

**Row B (description + main heading):**
- Flex row, `items-end`, justify-between, `gap-3 sm:gap-4`.
- **Left:** A fixed-width container (`w-[120px] sm:w-[180px] md:w-[280px]`, shrink-0) containing a paragraph: "Creative Studios Built Around Elevating Your Vision Into Striking Reality". Text: `text-[9px] sm:text-xs md:text-sm`, font-semibold, tracking-widest, uppercase, `text-left md:text-right`.
- **Right:** The main heading — three words stacked vertically: "Fearless", "Vision", "Delivered". Each word in its own `overflow-hidden` wrapper. Text: `fontSize: clamp(2rem, 9vw, 9rem)`, `lineHeight: 0.88`, weight 600, uppercase, black, text-right.

---

**ANIMATIONS (Framer Motion):**

All animations fire on page load (initial -> animate).

1. **fadeDown variant** (nav elements):
   - From: `{ opacity: 0, y: -20 }`
   - To: `{ opacity: 1, y: 0 }`
   - Each element has a custom stagger index. Delay: `index * 0.1s`. Duration: 0.5s. Ease: `[0.22, 1, 0.36, 1]`.
   - Applied to: logo (custom=0), each nav link (custom=1-4), hamburger (custom=5).

2. **fadeUp variant** (stats + bottom content):
   - From: `{ opacity: 0, y: 32 }`
   - To: `{ opacity: 1, y: 0 }`
   - Delay: `index * 0.12s`. Duration: 0.6s. Ease: `[0.22, 1, 0.36, 1]`.
   - Applied to: each stat card (custom=2,3,4), tagline paragraph (custom=5), CTA link (custom=6), description block (custom=7).

3. **Heading slide-up** (main heading words):
   - Each word slides up from `y: "110%"` to `y: 0` within its overflow-hidden parent (clip reveal effect).
   - Delay: `0.4 + wordIndex * 0.14` (so 0.4s, 0.54s, 0.68s). Duration: 0.7s. Ease: `[0.22, 1, 0.36, 1]`.

---

**RESPONSIVE BREAKPOINTS:**
- Mobile-first. Three tiers: default (mobile), `sm:` (640px), `md:` (768px).
- Nav links hidden on mobile, shown md+.
- Spacing, font sizes, and widths scale up at each breakpoint.
- Mobile menu provides full navigation on small screens.

---

**DEPENDENCIES:**
- React 18
- Tailwind CSS 3
- framer-motion
- lucide-react (ArrowUpRight, X icons)
```

---

## 51. AI Image Generator UI

- **Category**: AI
- **Type**: hero
- **Page Type**: hero
- **ID**: `ai-image-generator-ui`

```
Build a "Core Features" marketing section as a single centered component with three gradient cards. Use the Inter font family (weights 400, 500, 600) loaded from Google Fonts: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap`.

**Page shell:**
- Body: white background `#ffffff`, 80px top/bottom + 20px left/right padding, flex centered, Inter font.
- Global reset: `* { box-sizing: border-box; margin: 0; padding: 0; }`.

**Container (`.c1-container`):** max-width 1100px, full width, text-align center.

**Header block:**
- Badge (`.c1-badge`): text "Core Features", 0.75rem, weight 600, uppercase, letter-spacing 1px, gradient text using `linear-gradient(90deg, #F5C344, #F28482, #B567C2)` with `-webkit-background-clip: text` and transparent fill. 16px bottom margin.
- Title (`.c1-title`): "Built for Speed & Quality", font-size 2.75rem, weight 500, color `#0f172a`, letter-spacing -0.02em, 12px bottom margin.
- Subtitle (`.c1-subtitle`): "Everything you need to go" + `<br>` + "from idea to image", 1.125rem, color `#64748b`, line-height 1.5, 50px bottom margin.

**Grid (`.c1-grid`):** 3 equal columns, 24px gap. Breakpoints: 2 columns under 900px, 1 column under 600px (title scales to 2.25rem).

**Card base (`.c1-card`):** 20px border-radius, height 340px, flex column justify-end, relative, overflow hidden, text-align left, background `#F4F8F9`, shadow `0 10px 30px -10px rgba(0,0,0,0.1)`. Titles inside (`h3`): 1.05rem, weight 600, color `#1e293b`, padding 24px, z-index 2.

**Card 1 — Smart Prompt Suggestions (`.c1-card-1`):**
- Background: `radial-gradient(circle at 50% 0%, #FFB347 0%, #F9ED96 30%, #F4F8F9 60%, #F4F8F9 100%)`.
- Prompt box (white, 12px radius, 16px padding, 0.8rem text, color `#475569`, line-height 1.6, shadow `0 8px 20px rgba(0,0,0,0.04)`), absolutely positioned top:30px/left:24px/right:24px. Text: "A bright, high-resolution 3D illustration of a **cheerful cartoon** of a **girl character** **centred against a** smooth blue background" — bold phrases have class `.c1-blur-text` with gradient `linear-gradient(90deg, #FFB347, #E5A1F5)` as clipped text, weight 600.
- "Add more details" pill button: absolute top:180px/left:40px, white background, 1px solid black border, 5px 14px padding, 20px radius, 0.75rem text, weight 600, color `#1e293b`, shadow `0 4px 15px rgba(0,0,0,0.08)`, includes `✦` character styled `color: #a855f7; font-size: 1rem` with 6px gap.
- Cursor SVG arrow: absolute top:205px/left:110px, 24x24, fill `#0f172a`, white stroke 1px, drop-shadow `0 4px 6px rgba(0,0,0,0.2)`, z-index 10. Path: `M4 2L20 11L11 13L9 22L4 2Z`.
- Heading: "Smart Prompt Suggestions".

**Card 2 — API Access (`.c1-card-2`):**
- Background: `radial-gradient(circle at 50% 0%, #E5A1F5 0%, #F8ACA0 30%, #F4F8F9 60%, #F4F8F9 100%)`.
- `.c1-api-visual` absolutely positioned top:0/left:0/right:0/bottom:70px, flex centered, 24px horizontal padding.
- Image (`.c1-network-img`): width 100%, height 180px, object-fit contain, margin-top 20px. Source: `https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/viktor/network.svg`.
- Heading: "API Access".

**Card 3 — Project Library (`.c1-card-3`):**
- Background: `radial-gradient(circle at 50% 0%, #F9ED96 0%, #E5A1F5 30%, #F4F8F9 60%, #F4F8F9 100%)`.
- Mesh overlay (`.c1-mesh`): absolute inset 0, background image = two linear gradients of `rgba(255,255,255,0.8) 1px, transparent 1px` (horizontal and 90deg vertical), background-size 16px 16px, masked with `radial-gradient(circle at center top, black 0%, transparent 80%)` (include `-webkit-mask-image`).
- Folder image (`.c1-folder`): absolute top:50px, horizontally centered via `left:50%; transform:translateX(-50%)`, width 170px, drop-shadow `0 15px 25px rgba(0,0,0,0.08)`. Source: `https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/viktor/library%20icon.svg`.
- Search pill (`.c1-search`): absolute top:220px, centered, white background, 1px solid black, 6px 18px padding, 20px radius, 0.75rem text weight 500 color `#1e293b`, shadow `0 8px 20px rgba(0,0,0,0.06)`, white-space nowrap, 8px gap. Contains a 14x14 lucide-style search SVG (circle cx=11 cy=11 r=8, line 21,21→16.65,16.65, stroke `#64748b`, stroke-width 2, round caps/joins) followed by text "Search in library".
- Heading: "Project Library".

**Note:** No animations are defined in this component — it is purely static styling. No JavaScript behavior, no hover effects. Use Supabase if any data persistence is needed, though this section requires none.
```

---

## 52. Creative Portfolio

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `creative-portfolio`

```
626f6c742d63632d6167656e74Let me read all the relevant files to compile the full recreation prompt.
Here's the full recreation prompt:

---

## Prompt to Recreate This Hero Section

Build a full-screen hero section for a creative portfolio using React, Vite, Tailwind CSS, and the Figtree Google Font. The page has two components: a **Navbar** and a **Hero**. No additional packages beyond `lucide-react` (though it's not used here). The entire page is black background with white text.

---

### Setup

- **Font:** Figtree (400, 500, 600) from Google Fonts, loaded in `index.html`
- **Tailwind custom breakpoints (max-width based):**
  - `mobile`: max 809.98px
  - `md-tablet`: min 810px, max 1199.98px
- **CSS variable:** `--ease-spring: cubic-bezier(0.16, 1, 0.3, 1)`

---

### Video Background

Three full-screen looping videos (muted, autoPlay, playsInline, loop) stacked absolutely with crossfade switching. All three render simultaneously; only the active one has `opacity-100`, the others have `opacity-0` with `transition-opacity duration-[1200ms] ease-in-out`.

**Video URLs (CloudFront):**
1. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260629_030107_874273ea-684a-4e90-bb96-8fdfde48d53d.mp4`
2. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260629_032424_3c9c2a9d-807b-4482-80e6-dd6d9dfd4545.mp4`
3. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260627_094019_4214ea73-b963-46a4-8327-61489192de99.mp4`

**Preloading:** On mount, fetch all videos as blobs and create object URLs for instant playback. Fall back to original URL on failure.

A `bg-black/10` overlay sits above videos at `z-[1]`.

---

### Navbar (absolute positioned, z-10, on top of hero)

- **Layout:** Centered container, max-width 1340px, `py-9 px-[15px]`
- **Left side:** Navigation items formatted as `01 / Works`, `02 / Services`, `03 / About`, `04 / Contact`
  - Index number: `text-[8px] leading-3 tracking-[-0.08px] font-medium uppercase`
  - Label: `text-xs leading-4 tracking-[-0.12px] font-medium uppercase`
  - Each link has a `.nav-link-underline` effect (underline slides in from right on hover via `scaleX` transform)
- **Right side (aligned right):** Email `Davies@gmail.com` and live clock showing `CUP HH:MM:SS` (24h format, updates every second using `Intl.DateTimeFormat('en-GB')`)
- **Mobile:** Nav items hidden, replaced by a `Menu`/`Close` toggle button. Mobile panel uses CSS Grid `grid-rows-[0fr]`/`grid-rows-[1fr]` transition (420ms, spring ease) for smooth expand/collapse. Mobile nav links are large: `text-[28px] leading-8 tracking-[-0.84px]`

---

### Hero Content (z-[2], relative)

Container: `max-w-[1340px]`, full height, flex column, `justify-end items-end`, `gap-[150px]`, `pt-[190px] px-[15px]`

**Section 1 - Video Switcher + Availability (upper area):**
- Left column (`flex-[4]`): Three buttons labeled `01 / WATER WAVE`, `02 / GRIDWAVE`, `03 / LIGHT TUNNEL`. Active button is full opacity, inactive is `opacity-55` with `hover:opacity-75`. On click, sets `activeIndex` to crossfade videos. Each has a `.role-link` class that translates 4px right on hover.
- Right column (`flex-1`): Pulsing dot + "Available for work" text. Dot is 7px circle with glow shadow and infinite pulse animation (scale 1 to 1.45, opacity 1 to 0.45, 1.6s). On slide 1, dot is `#F598F2` pink with pink glow. On slides 2-3, dot is white with white glow.

**Section 2 - Name + CTA (bottom area, pb-[60px]):**
- Left column (`flex-[2]`): Giant name "Viktor." in `text-[200px] leading-[81%] tracking-[-6px] font-medium uppercase`. The period is accent-colored: pink `#F598F2` on slide 1, white on slides 2-3. Animate in with `revealUp` (translateY 80px to 0, 0.9s spring ease).
- Right column (`flex-1`, `pl-[50px]`): Paragraph text ("I craft bold brands and modern websites with purpose...") at `text-base leading-6 tracking-[-0.16px] font-medium`. Below it, a "start a project" button (lowercase) with white border. Button has a fill-up hover effect: `::before` pseudo-element with `#F598F2` background that translateY from 101% to 0 on hover, text turns black, border turns pink. Both animate in with `revealRight` (translateX 100px to 0, 0.9s spring ease), button delayed by 0.08s.

**Reveal animations** trigger once via IntersectionObserver at 0.35 threshold.

---

### Responsive Tablet (810px-1199px)
- Navbar: `py-[30px] px-[18px]`, nav gaps shrink to `gap-4`
- Hero name: `text-[129.6px] leading-[113.4px] tracking-[-7.7px]`
- Bottom section: gap 28px, pb 52px, left padding 24px

### Responsive Mobile (<810px)
- Navbar: `py-6 px-[18px]`, desktop nav hidden, hamburger menu shown
- Hero content: `justify-end items-start gap-[72px] pt-[140px] px-[18px]`
- Switcher + availability stack vertically with `gap-7`
- Bottom section: column layout, `gap-8 pb-11`
- Name: `text-[clamp(68px,21vw,80px)] leading-[96px] tracking-[-4.8px]`
- Paragraph: `max-w-[420px]`

---

### Custom CSS Animations

```css
@keyframes videoFadeIn { from { opacity: 0 } to { opacity: 1 } }
@keyframes revealUp { from { opacity: 0; transform: translateY(80px) } to { opacity: 1; transform: translateY(0) } }
@keyframes revealRight { from { opacity: 0; transform: translateX(100px) } to { opacity: 1; transform: translateX(0) } }
@keyframes dotPulse { 0%,100% { opacity:1; transform:scale(1) } 50% { opacity:0.45; transform:scale(1.45) } }
```

### Accessibility
- `prefers-reduced-motion: reduce` disables all animations
- Semantic landmarks: `<header>`, `<main>`, `<nav>`, `<section>`
- ARIA labels on navigation regions and status elements
- Videos are `aria-hidden="true"`
```

---

## 53. Stillmind

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `stillmind`

```
Create a fullscreen cinematic hero section for a mindfulness/focus app called "Lumora" using React, Tailwind CSS, and Lucide React icons.

## Font

Use **Instrument Serif** (Google Fonts, italic for the logo). Load it in index.html:
```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
```

Set `font-family: 'Instrument Serif', serif` on html/body. Use `system-ui, sans-serif` inline for body text (subtext, buttons, stats, video labels).

---

## Background Video Layer

Stack 4 fullscreen looping videos absolutely positioned. Only the active one has `opacity-100`; others have `opacity-0`. Transition opacity over 1000ms ease-in-out. Videos autoPlay, muted, loop, playsInline.

**Video URLs (in order):**
1. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260702_081127_0992a171-d3c6-4978-8213-0ec5df8b6d63.mp4`
2. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260702_092026_dd05b805-ea0f-40b2-8c52-332b88502592.mp4`
3. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260702_081042_df7202bf-bd80-4b2b-bbc6-1f09ba2870e9.mp4`
4. `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260702_080959_4cac5234-3573-464e-a5b7-76b94b8a7d61.mp4`

**Labels:** Golden Hour, Still Water, Deep Woods, Quiet Dawn

---

## Transparent PNG Overlay (z-index 1)

Place this image over the videos as an absolutely positioned overlay covering the full viewport:
```
https://soft-zoom-63098134.figma.site/_assets/v11/0b4a435b2df2747593c43d7a1c9b4578f7d8d90c.png
```

Apply a continuous "train-bob" animation: translateY oscillates between 0 and -6px over 3s ease-in-out infinite, with a constant scale(1.03) to prevent edges from showing during the motion.

---

## Liquid Glass Effect (CSS class `.liquid-glass`)

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
```

With a `::before` pseudo-element for a subtle gradient border:
```css
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

---

## Content Layer (z-index 2) - Flex Column Full Height

### Navigation (top)
- Left: "Lumora" in white, italic, text-xl (sm:text-2xl)
- Right (desktop md+): A `.liquid-glass` pill containing nav links ("How It Works", "Features", "Pricing", "Community") in white/90 text-sm with hover to white, plus a solid white "Get Started" button at the end
- Right (mobile): A `.liquid-glass` rounded hamburger button using Lucide `Menu`/`X` icons with a crossfade rotation animation (300ms). The Menu icon rotates out 90deg and scales to 75%; the X icon rotates in from -90deg

### Mobile Menu Overlay (fixed, z-50)
- Backdrop: `bg-black/60 backdrop-blur-sm`
- Centered fullscreen panel with staggered entrance (each link delays 50ms more: 100ms, 150ms, 200ms, 250ms, 300ms)
- Links: white text-3xl, translate-y-4 to 0 on open
- "Get Started" button at bottom with scale animation
- Cubic-bezier easing: `cubic-bezier(0.4,0,0.2,1)`, duration 500ms

### Hero Content (centered, below nav)
- **Badge**: `.liquid-glass` rounded-full pill with text "Over 10,000 minds already finding their clarity"
- **Heading**: "Clarity in an Endlessly / Noisy Universe" (line break after "Endlessly"). Sizes: text-4xl / sm:text-5xl / md:text-7xl / lg:text-[5.5rem], leading-[1.1], max-w-4xl
- **Subtext**: "Rise above the chaos of pings, infinite scrolling, and relentless demands. Discover how to protect your presence and create with intention." max-w-xl, leading-relaxed
- **Email Input**: `.liquid-glass` rounded-full pill containing a text input ("Your Best Email") and a solid white "Get Early Access" button. Max-width 320px on mobile, sm:max-w-sm
- **Video Switcher**: Row of 4 text buttons with labels. Active button has solid color + bottom border. Inactive buttons are 50% opacity with transparent border, hover to 80%

### Dark Mode for "Deep Woods" (3rd video, index 2)
When the 3rd video is active, all hero content (badge, heading, subtext, input, video switcher) transitions to dark color `#182C41` with 700ms duration. The navbar and bottom stats remain white always.

### Bottom Stats (pushed to bottom via flex-1 spacer)
- Row of stats separated by `|` dividers (hidden on mobile): "60+ Deep Sessions", "12,000+ Creators", "4.8 User Satisfaction", "Intentional-First Design"
- text-white/70, text-xs sm:text-sm, system-ui font

---

## Video Switching Logic
- Track `activeVideo` state (default 0) and `isTransitioning` boolean
- On click, if not already active and not mid-transition, set new active video and start a 1000ms cooldown (matching the CSS crossfade duration)
- During cooldown, ignore additional clicks

---

## Responsive Behavior
- Mobile: Smaller text sizes, tighter padding, hamburger nav, stats wrap naturally
- Tablet/Desktop: Larger heading, more padding, inline nav pill, stats with pipe separators

---

## Section Container
```html
<section className="relative w-full h-screen overflow-hidden bg-black">
```

Black background prevents flash before videos load. Everything is a single viewport-height section with no scroll.

---

That's the complete specification. The entire app lives in a single `App.tsx` component with the CSS in `index.css`.
```

---

## 54. Equilibrium

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `equilibrium`

```
Build a full-screen, single-page React + TypeScript + Vite + Tailwind CSS hero section with a "liquid glass" aesthetic on top of a looping background video. Use `lucide-react` for icons. No other UI libraries.

**Font & Global CSS (`src/index.css`):**
- Import Geist from Google Fonts: `https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap`
- Apply `Geist` globally via `* { font-family: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }`
- Include `@tailwind base; @tailwind components; @tailwind utilities;`
- Define a `.liquid-glass` class:
  - `background: rgba(255,255,255,0.01);`
  - `background-blend-mode: luminosity;`
  - `backdrop-filter: blur(4px);` plus `-webkit-backdrop-filter`
  - `border: none;`
  - `box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);`
  - `position: relative; overflow: hidden;`
- Add a `.liquid-glass::before` pseudo-element creating a gradient border via mask compositing:
  - `content:''; position:absolute; inset:0; border-radius:inherit; padding:1.4px;`
  - `background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);`
  - `-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); -webkit-mask-composite: xor; mask-composite: exclude; pointer-events:none;`

**Component (`src/App.tsx`):**
- Import from `lucide-react`: `ChevronDown`, `Infinity`, `Menu`, `X`. Import `useState` from React.
- Constant `BG_VIDEO = 'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_230229_7c9bc431-46cf-489a-948d-e8144d8eb5d4.mp4'`
- `navLinks` array: `{ label: 'Home', active: true }`, `{ label: 'Wellness', dropdown: true }`, `{ label: 'Routine' }`, `{ label: 'Our Team' }`.
- `menuOpen` state via `useState(false)`.

**Layout:**
- Root: `<div class="relative w-full h-screen overflow-hidden">`.
- Background `<video>` absolutely positioned, `w-full h-full object-cover`, `autoPlay muted loop playsInline`, `src={BG_VIDEO}`.

**Navbar** (`absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-5 sm:px-8 py-5`):
- Logo (left): flex with `gap-2 text-white font-medium text-base`. `<Infinity size={22} strokeWidth={1.5} />` followed by `<span>Equilibrium</span>`.
- Nav pill (center, `hidden md:flex`): `liquid-glass items-center gap-1 rounded-xl px-2 py-2`. Map `navLinks`. Each button: `flex items-center gap-0.5 px-3 py-1.5 rounded-md text-sm transition-colors`; active gets `bg-white/15 text-white`, others `text-white/70 hover:text-white`. Dropdown items render a `<ChevronDown size={13} class="mt-px" />`.
- CTAs (right, `hidden md:flex items-center gap-3`):
  - "Log in": `liquid-glass text-white text-sm font-medium px-4 py-2.5 rounded-full hover:bg-white/5 transition-colors`
  - "Begin Now": `bg-white text-black text-sm font-medium px-4 py-2.5 rounded-full hover:bg-white/90 transition-colors`
- Mobile toggle (`md:hidden`): `liquid-glass text-white p-2 rounded-lg`; shows `X` when open else `Menu` (size 18).

**Mobile menu** (when `menuOpen`): `absolute top-[72px] left-4 right-4 z-30 md:hidden liquid-glass rounded-2xl p-4 flex flex-col gap-1`. Same nav links as buttons `flex items-center justify-between w-full px-4 py-3 rounded-lg text-sm`. Bottom CTA row: `flex gap-2 mt-2 pt-3 border-t border-white/10` with two `flex-1` buttons ("Log in", "Begin Now") matching desktop styles.

**Hero content (bottom-left)** `absolute bottom-0 left-0 z-20 px-6 sm:px-12 pb-10 sm:pb-16 max-w-2xl`:
- `<h1>`: `text-white text-4xl sm:text-5xl lg:text-6xl font-medium leading-tight tracking-tight mb-4` — text: `Live Better, Feel Whole Every Day`.
- `<p>`: `text-white/60 text-sm leading-relaxed mb-7 max-w-md` — text: `Take charge of how you feel with a companion built for your journey—build routines, follow your growth, and unlock tailored insights for a steadier, more vibrant life each day.`
- Buttons row `flex flex-wrap items-center gap-3`:
  - "Start Today": `bg-white text-black text-sm sm:text-base font-medium px-6 sm:px-7 py-3 rounded-full hover:bg-white/90 transition-colors`
  - "Discover How": `liquid-glass text-white text-sm sm:text-base font-medium px-6 sm:px-7 py-3 rounded-full hover:bg-white/5 transition-colors`

**Animations/interactions:** all buttons use Tailwind `transition-colors`; liquid-glass effect uses `backdrop-filter: blur(4px)` plus the animated-looking gradient border pseudo. No additional keyframe animations. The background video itself provides motion.

**Dependencies:** `react`, `react-dom`, `lucide-react`, `tailwindcss`, `vite`, `@vitejs/plugin-react`, TypeScript. Tailwind configured with default content globs for `./index.html` and `./src/**/*.{ts,tsx}`.
```

---

## 55. Blog Showcase

- **Category**: Blog
- **Type**: Blog
- **Page Type**: hero
- **ID**: `blog-showcase`

```
Build a "Behind the Lens" photography blog section with the following exact specifications:

**Layout and Structure:**
- White background page, max-width 1200px, centered, 60px vertical padding, 20px horizontal padding
- Header with: a small grey "Blog" badge (bg #f4f4f4, 8px border-radius), a large heading "Behind the lens" (64px, Outfit font, weight 500, letter-spacing -2.5px), a subtitle paragraph and a "View all posts" button side by side
- Subtitle: "Thoughts, insights, and stories from my photography journey. Take a peek into my creative process and recent projects." (max-width 480px, #666 color, 18px, weight 500, opacity 0.8)
- "View all posts" button: black bg, white text, 40px border-radius pill shape, 14px font, weight 600, scales 1.02 on hover

**Featured Post (full-width card):**
- 2-column grid (1fr 1fr), 20px border-radius, 1px solid #f0f0f0 border, min-height 520px, bg #fcfcfc
- Left side: autoplaying looped muted video, object-fit cover, fills the entire area
- Right side: 60px padding, contains a black "Must Read" pill badge (12px font, 20px border-radius), title in Outfit font 48px weight 500 (letter-spacing -1.5px), description in #666 at 17px, and a footer with author name and colored category badge pushed to the bottom via margin-top auto
- Featured post data: title "Full-Frame vs. Crop Sensor: Which for Photography?", description "An honest look at the real-world differences between these camera systems to help you choose what's actually right for your photography needs.", author "By August Renner (c)", category "Gear" with color #7d1a4a
- Featured video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260507_155500_808e6fdd-761f-4acd-b3be-cb7e6e700def.mp4`

**Blog Grid (3 standard cards):**
- 3-column grid, 25px gap, below the featured post
- Each card: video with 16/10 aspect ratio, 20px border-radius, title below (Outfit 17px weight 600) with a colored category badge aligned right
- Card 1: "Finding Natural Light in Unexpected Places", category "Lighting" (#2c4c34), video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260506_030111_a9e15665-d379-4a7f-8116-695bbe452ad1.mp4`
- Card 2: "My Approach to Editing: Creating a Consistent Photography Style", category "Editing" (#a63e2d), video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_064122_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4`
- Card 3: "Pricing Your Photography: Strategies That Work", category "Business" (#1a2b8c), video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260507_154232_f8809bd2-a6c3-4a38-908d-2005e5b3cb3e.mp4`

**Hover Interactions (on all video containers):**
- Videos scale to 1.08 on hover with cubic-bezier(0.33, 1, 0.68, 1) over 0.5s
- A dark overlay (rgba(0,0,0,0.25)) fades in over 0.4s on hover
- A centered "+" icon inside a 70px circle (rgba(255,255,255,0.2) bg) scales from 0.7 to 1.0 on hover over 0.3s
- White "L-shaped" corner brackets (12px, 1.5px border) in all 4 corners of each video, 15px inset from edges

**Category Badges:**
- Pill shape (20px border-radius), white text, 11px font, weight 600, 4px 12px padding, capitalized, background color matches each post's assigned color

**Fonts:**
- Google Fonts: Inter (400, 500, 600) for body text, Outfit (500, 600, 700) for headings and titles

**Responsive:**
- At 1024px: featured post becomes single column, grid becomes 2 columns, featured content padding 40px
- At 768px: heading drops to 48px, header-bottom stacks vertically, grid becomes 1 column, featured title drops to 32px

**Data Source:**
- Store all blog post data (type, badge, title, description, author, category, category_color, image/video URL, display_order) in a Supabase `blog_posts` table
- Fetch and render dynamically, ordered by display_order ascending
- Enable RLS with public read access for anon and authenticated users

**Tech Stack:**
- React + TypeScript + Vite + Tailwind CSS (for base resets only, use custom CSS for the blog styles)
- Supabase JS client for data fetching
- All videos use autoPlay, loop, muted, playsInline attributes
```

---

## 56. SaaS Value

- **Category**: SaaS
- **Type**: hero
- **Page Type**: hero
- **ID**: `saas-value`

```
Build a full-viewport hero section for a SaaS landing page called "Questly" using React, TypeScript, Tailwind CSS 3, and Vite. Use `lucide-react` for all icons. No other UI libraries.

---

FONT

Use the font "Nimbus Sans TW01" loaded from this stylesheet in `index.html`:

```
https://db.onlinewebfonts.com/c/bb5de19d87c09a95216dc6ccd96e37c6?family=Nimbus+Sans+TW01
```

Set the font stack in both `tailwind.config.js` and `index.css`:

```
'Nimbus Sans TW01', 'Helvetica Neue', Helvetica, Arial, sans-serif
```

Enable `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` on `html`.

---

BACKGROUND IMAGE

The full hero section uses this image as a `background-image` (cover, centered):

```
https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260611_133301_d5f2a94a-b22e-4e4a-a6b6-eacdddf1f5b0.png&w=1280&q=85
```

Applied via inline `style={{ backgroundImage: url(...) }}` on the `

`. The section is `relative min-h-[100svh] overflow-hidden bg-cover bg-center flex flex-col`.

---

GRASS OVERLAY

An absolutely positioned grass PNG sits at the bottom of the section, full width, `z-10`, pointer-events-none, select-none:

```
https://res.cloudinary.com/dy5er7kv5/image/upload/q_auto/f_auto/v1781191264/grass_eam204.png
```

Classes: `pointer-events-none absolute bottom-0 left-0 z-10 w-full select-none`

---

LOGO (SVG Component)

A custom SVG logo component used in the navbar and dashboard sidebar. It uses `currentColor` for fill so it inherits text color. ViewBox: `0 0 256 256`. Path data:

```
M 144 256 L 27.598 256 L 144 139.598 Z M 256 207.5 L 200 256 L 200 56 L 0 56 L 48 0 L 256 0 Z M 0 204.402 L 0 112 L 92.402 112 Z
```

---

NAVBAR

- Positioned with `animate-fade-down relative z-20`
- Flex row: logo left, nav links center, CTA + hamburger right
- Horizontal padding: `px-5 sm:px-8 lg:px-10`, vertical: `py-4 sm:py-5`
- Logo: `text-gray-900`, icon sized `w-5 h-5 sm:w-6 sm:h-6`
- Desktop nav links (hidden below `md`): `text-[13px] text-gray-700`, hover `text-gray-900`, gap-8. Items: "Toolkit" (with `ChevronDown` icon `w-3.5 h-3.5`), "Plans", "News"
- CTA button: `bg-gray-900 text-white text-[13px] font-medium px-4 sm:px-5 py-2 rounded-full hover:bg-gray-800`
- Hamburger (md:hidden): `w-9 h-9 rounded-full text-gray-900 hover:bg-gray-900/10`, toggles `Menu`/`X` icons (`w-5 h-5`)
- Mobile dropdown (when open): `absolute left-4 right-4 top-full rounded-2xl bg-white/80 backdrop-blur-xl ring-1 ring-gray-200 px-5 py-3 animate-fade-up`. Links: `text-[15px] text-gray-700 hover:text-gray-900 border-b border-gray-200 last:border-b-0`

---

HERO CONTENT (centered, text-center)

Spacing between navbar and content uses a flex spacer: `flex-1 min-h-8 sm:min-h-12 lg:min-h-16 shrink-0`

Headline (h1)
- `text-gray-900 font-normal leading-[1.05] tracking-tight`
- Sizes: `text-[40px] min-[400px]:text-[44px] sm:text-6xl lg:text-7xl xl:text-[80px]`
- Two lines, each a `` with staggered `animate-fade-up`:
  - Line 1: "Get cited." (no delay)
  - Line 2: "Effortlessly." (`[animation-delay:100ms]`)

### Search Bar (form)
- `animate-fade-up [animation-delay:220ms] mt-5 sm:mt-6 w-full max-w-xl`
- Pill container: `flex items-center gap-3 rounded-full bg-white/60 backdrop-blur-md ring-1 ring-gray-200 pl-5 pr-1.5 py-1.5`
- Input: `flex-1 bg-transparent text-sm sm:text-base text-gray-900 placeholder-gray-500 outline-none py-2`, placeholder: "What makes content rank in AI search?"
- Submit button: `w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-gray-900 text-white hover:scale-105 active:scale-95 transition-transform shrink-0`, contains `ArrowUp` icon `w-4 h-4 sm:w-[18px] sm:h-[18px]`

### Description
- `animate-fade-up [animation-delay:340ms] mt-4 sm:mt-5 text-gray-600 text-sm sm:text-base lg:text-lg leading-relaxed max-w-md`
- Text: "Ship articles that answer actual customer questions -- and be seen on [Sparkles icon] ChatGPT"
- Line break `
` before the dash
- `Sparkles` icon: `inline w-4 h-4 -mt-1`

### CTA Buttons
- `animate-fade-up [animation-delay:460ms] mt-4 sm:mt-5 flex flex-wrap items-center justify-center gap-3`
- **Primary**: `bg-gray-900 text-white text-sm font-medium px-6 py-2.5 rounded-full hover:bg-gray-800 hover:shadow-lg transition-all` -- "Try It Free"
- **Secondary**: `text-gray-700 text-sm font-medium px-6 py-2.5 rounded-full ring-1 ring-gray-300 hover:bg-gray-100 transition-colors` -- "Talk to sales"

---

## DASHBOARD MOCKUP (below the hero content)

Another flex spacer (`flex-1 min-h-10 sm:min-h-12 lg:min-h-16 shrink-0`) separates the content from the dashboard.

### Container
- `animate-hero-rise [animation-delay:620ms] relative z-0 w-[92%] sm:w-[84%] lg:w-[72%] max-w-4xl mx-auto shrink-0 -mb-10 sm:-mb-20 lg:-mb-32`
- Uses a **ScaledDashboard** wrapper: a `ResizeObserver`-based component that renders the mockup at a fixed design width of **896px** and scales it down via CSS `transform: scale()` to fit its container, with `transformOrigin: 'top left'`. The outer div's height is set to `inner.offsetHeight * scale` to prevent layout overflow.

### Mockup Chrome
- Outer: `rounded-t-2xl overflow-hidden bg-[#1a1a1c] shadow-[0_-20px_80px_rgba(0,0,0,0.35)] ring-1 ring-white/10 text-left`
- **Title bar**: `bg-[#242427] border-b border-white/5 px-4 py-2.5`
  - Traffic lights: three spans `w-2.5 h-2.5 rounded-full` colored `#ff5f57`, `#febc2e`, `#28c840`
  - Icons (all `w-3.5 h-3.5 text-white/40`): `PanelLeft`, `ChevronLeft`, `ChevronRight` (text-white/25)
  - Center URL bar: `bg-[#1a1a1c] rounded-md px-6 py-1 text-[10px] text-white/60` with `Monitor` icon -- text "questly.ai"
  - Right icons: `RotateCw`, `Share`, `Plus`, `Copy`

### Sidebar (22% width)
- `border-r border-white/5 bg-[#1e1e21] px-3 py-3.5`
- Logo icon `w-4 h-4 text-white/70` + `Grid` icon `w-3.5 h-3.5 text-white/30`
- Workspace badge: `w-4 h-4 rounded bg-[#e8553f]` with "C" letter, label "CareNest" `text-[10px] text-white/80`
- Nav items: Compass/Uncover, Layers/Subjects, ListTodo/Inbox -- `text-[10px] text-white/60`
- Recent articles list with "Ready to Release" green dots `text-[#28c840]/70`

### Main Content Area
- Header: workspace icon (larger `w-9 h-9 rounded-lg bg-[#e8553f]`), "CareNest" `text-sm font-medium text-white`, subtitle `text-[10px] text-white/45`, and a "Generate" button with `Sparkles` icon
- **Stats grid** (4 columns): `grid-cols-4 divide-x divide-white/5 rounded-xl bg-white/[0.03] ring-1 ring-white/5`
  - RELEASED: 62 / Posts indexed
  - BREADTH: 12 / Subject groups
  - REMAINING: 412 / Ready to draft
  - MAX REACH: 3,156,200 / Searches a month
  - Values: `text-xl font-medium text-white`, labels: `text-[8px] tracking-wider text-white/35`
- **Subject cards** (3 columns): Elder Care, Mobility, Home Safety -- `rounded-lg bg-white/[0.03] ring-1 ring-white/5`
- **Drafting inbox** table: 5 rows with question, volume, difficulty, status columns. "Drafting" status colored `text-[#febc2e]/80`

---

## ANIMATIONS (defined in index.css)

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}

@keyframes fade-down {
  from { opacity: 0; transform: translateY(-16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes hero-rise {
  from { opacity: 0; transform: translateY(64px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.animate-fade-up { animation: fade-up 0.9s cubic-bezier(0.22, 1, 0.36, 1) both; }
.animate-fade-down { animation: fade-down 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
.animate-hero-rise { animation: hero-rise 1.1s cubic-bezier(0.22, 1, 0.36, 1) both; }
```

Staggered delays applied via inline `[animation-delay:Xms]` Tailwind arbitrary values. Respect `prefers-reduced-motion: reduce` by disabling all three animations.

---

RESPONSIVE BREAKPOINTS SUMMARY

| Element | Mobile (<640) | SM (640+) | MD (768+) | LG (1024+) | XL (1280+) |
|---|---|---|---|---|---|
| Headline | 40px / 44px@400 | 60px | -- | 70px | 80px |
| Nav links | Hidden (hamburger) | -- | Visible | -- | -- |
| Search bar width | full | -- | -- | -- | max-w-xl |
| Dashboard width | 92% | 84% | -- | 72% | -- |
| Dashboard bottom overlap | -mb-10 | -mb-20 | -- | -mb-32 | -- |

---

FILE STRUCTURE

```
src/
  App.tsx            -- renders <Hero />
  main.tsx           -- ReactDOM.createRoot
  index.css          -- Tailwind directives + custom keyframes
  components/
    Hero.tsx          -- main section with bg image, content, ScaledDashboard, grass overlay
    Navbar.tsx        -- top nav with mobile drawer
    Logo.tsx          -- SVG logo component
    DashboardMockup.tsx -- full browser-chrome dashboard mockup
```
```

---

## 57. IntelligentX

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `intelligentx`

```
Prompt:
Build a modern React landing page using Vite, Tailwind CSS, and motion/react for elegant animations. The application must feature a highly polished, aesthetic hero section and a glassmorphic navigation bar.
1. Typography & Global CSS (src/index.css)
Import the fonts "Inter" and "Outfit" from Google Fonts.
Set --font-sans to Inter and --font-display to Outfit.
Set --color-brand-green to #9fff00 and --color-bg-base strictly to #EDEEF5.
Ensure the body uses @apply bg-bg-base text-zinc-900 font-sans antialiased; to carry the #EDEEF5 background throughout the entire page.
2. Component Structure (src/App.tsx)
Import Navbar and Hero.
Return a div containing the <Navbar /> and <main><Hero /></main>.
Set the wrapper container classes to min-h-screen bg-bg-base selection:bg-brand-green selection:text-black.
3. Navbar Component (src/components/Navbar.tsx)
Give it fixed styling: fixed top-0 left-0 w-full z-50 py-6 md:py-10 bg-gradient-to-b from-[#f1f1f1]/80 to-transparent backdrop-blur-[2px].
Container layout: A 12-column grid (grid-cols-12 max-w-7xl mx-auto).
Left (Cols 1-3): A geometric flower/clover SVG icon (fill: #1a1a1a) beside the brand name "mėntality" using the display font.
Center (Cols 4-9): Desktop-only hidden nav links: "service", "patient resources", "about us", "education center". Styled small and lowercase.
Right (Cols 10-12): "find help" anchor link, a black rounded button reading "get started →", and an elegant animated hamburger toggle icon for mobile.
Include an AnimatePresence and motion.div drawer that slides down for mobile with the navigation links.
4. Hero Component (src/components/Hero.tsx)
Main styling: <section className="relative min-h-[110vh] sm:min-h-[140vh] w-full flex flex-col items-center justify-start overflow-hidden bg-bg-base">
Background Video Container:
Absolute wrapper: <div className="absolute top-[15vh] sm:top-[20vh] left-0 w-full h-[95vh] sm:h-[120vh] z-0 pointer-events-none">
The video itself should be <video autoPlay loop muted playsInline className="w-full h-full object-cover opacity-100" />
Exact CloudFront URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260603_132049_036591b8-6e92-4760-b94c-a7ea6eef315c.mp4
Gradient Mask: Below the video in the wrapper, add <div className="absolute top-0 left-0 w-full h-24 sm:h-32 bg-gradient-to-b from-bg-base to-transparent"></div> to smoothly blend the video into the #EDEEF5 background.
Hero Content Alignment: Use <div className="max-w-7xl w-full mx-auto px-8 md:px-16 lg:px-20 relative z-10 grid grid-cols-12 gap-x-4 md:gap-x-8">. Place the text in col-span-12 md:col-span-10 md:col-start-2.
Hero Header (motion.h1): Needs a slide-up fade (initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}).
Exact text formatting:
[#1a1a1a] Remix: Mentality offers
[#8e8e8e] information
(line break)
[#8e8e8e] and resources to help you manage
(line break)
[#8e8e8e] your [Eye Icon Puipl UI Element] mental wellbeing.
For the Eye Icon Element between "your" and "mental", create an inline pill-shaped visual: w-[16px] md:w-[42px] lg:w-[62px] border-[2px] border-[#1a1a1a] rounded-full inline-flex items-center justify-center containing a tiny solid black dot (w-2 h-2).
Search Pill Component:
Add a delayed slide-up animation (delay: 0.15) under the header text.
Make a custom capsule <div className="bg-white rounded-[6px] border border-black/[0.05] p-1 pl-4 flex items-center shadow-sm">.
Include an <input placeholder="Ask me anything..."> with transparent background so it looks integrated.
Trailing action button: <button className="bg-[#1a1a1a] text-white w-9 h-9 rounded-full relative"> containing an SVG chevron/arrow icon.
Architectural Edge Anchors:
Absolute middle right edge: Create a glassmorphic pill button for language switching (pl — en).
Absolute bottom left corner: Place "2024" in small neat text.
Absolute bottom right corner: Place "mental health tools" in small neat text.
Ensure there are no artificial margins/padding below the video to make sure the video takes exactly 100% of the Hero viewport, while allowing the #EDEEF5 background base to anchor the entire page cleanly.
```

---

## 58. Portal

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `portal`

```
Build a password manager landing page hero section using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React icons. Here is every specification:

---

### Fonts

- **Heading font:** "Helvetica Now Display Bold" -- load via this stylesheet in `index.html`:
  ```
  <link href="https://db.onlinewebfonts.com/c/04e6981992c0e2e7642af2074ebe3901?family=Helvetica+Now+Display+Bold" rel="stylesheet">
  ```
- **Body font:** "Inter" (weights 300-900) -- load via Google Fonts in `index.css`:
  ```
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
  ```

### CSS Variables (defined in `:root` in `index.css`)

```
--font-heading: 'Helvetica Now Display Bold', sans-serif;
--font-body: 'Inter', sans-serif;
--color-text: #192837;
--color-accent: #7342E2;
--color-login-bg: #F2F2EE;
```

Global reset: `* { box-sizing: border-box; }`, body uses `var(--font-body)`, `var(--color-text)`, margin/padding 0.

---

### Background

Full-viewport looping background video, absolutely positioned, covering the entire page with `object-cover`. URL:

```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260606_131516_eca35265-ea66-4fbd-8d52-22aae6e1a503.mp4
```

Attributes: `autoPlay`, `muted`, `loop`, `playsInline`. Classes: `absolute inset-0 z-0 w-full h-full object-cover`.

---

### Logo (inline SVG component)

A custom geometric SVG logo, 32x32, viewBox `0 0 256 256`, fill `#192837`:

```
M 64 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 L 128 64 L 128 64.5 L 161 32 L 192 0 L 256 0 L 256 64 L 192 128 L 128 128 L 128 192 L 96 223 L 63.5 256 L 0 256 L 0 192 Z M 256 192 L 224 223 L 191.5 256 L 128 256 L 128 192 L 192 128 L 256 128 Z
```

---

### Navbar

- Max-width `1280px`, centered with `margin: 0 auto`.
- Padding: `px-5 sm:px-8 py-4 sm:py-5`.
- `relative z-10`, flexbox with `justify-between`, `items-center`.
- **Left:** Logo component.
- **Center (desktop, hidden on mobile `md:flex`):** 5 nav links -- "Vault", "Plans", "Install", "News", "Help". Each is `text-sm font-medium`, color `var(--color-text)`, `transition-opacity hover:opacity-70`, gap-8.
- **Right (desktop, hidden on mobile `md:flex`):** Two pill buttons with `gap-3`:
  - "Start For Free": background `#7342E2`, white text, `text-sm font-semibold px-5 py-2.5 rounded-full`, hover shadow, active scale-95.
  - "Sign In": background `#F2F2EE`, text `var(--color-text)`, same sizing/rounding.
- **Mobile (`md:hidden`):** Hamburger button using Lucide `Menu` icon (24px). Toggles to `X` icon when open.

---

### Mobile Menu (slide-in sheet)

Uses Framer Motion `AnimatePresence`. Two layers:

1. **Backdrop:** Fixed overlay, `rgba(25,40,55,0.35)` background, `backdrop-blur(4px)`. Fades in/out over 0.3s. Clicking dismisses the menu.

2. **Sheet:** Fixed, right-aligned, `width: min(88vw, 360px)`, `height: 100dvh`, background `#CFC8C5`, box-shadow `-12px 0 48px rgba(25,40,55,0.18)`. Slides in from right with custom cubic bezier `[0.22, 1, 0.36, 1]` over 0.45s; exits with `[0.55, 0, 1, 0.45]` over 0.35s.

   Contents:
   - **Header:** Logo + circular close button (40x40, background `rgba(25,40,55,0.1)`, X icon 20px), with `whileTap={{ scale: 0.9 }}`.
   - **Divider:** 1px line, `rgba(25,40,55,0.12)`, margin `0 24px`.
   - **Nav links:** Each link staggers in from right (x: 24 to 0, delay `0.18 + i * 0.07`, duration 0.4s). Font size `1.1rem`, rounded-xl, hover `bg-black/10`.
   - **CTA buttons:** Same "Start For Free" (`#7342E2`) and "Sign In" (`#F2F2EE`) as desktop, full-width, `py-3.5 rounded-full`, font size `0.95rem`.

---

### Hero Content

- Centered container, max-width `1280px`, `relative z-10`.
- Padding top: `clamp(40px, 8vw, 72px)`, bottom `48px`.
- Inner content wrapper: max-width `660px`, centered.

**Heading (`<h1>`):**
- Font: `var(--font-heading)`.
- Size: `clamp(1.65rem, 5vw, 3rem)`.
- Line-height: `1.05`, letter-spacing: `-0.01em`.
- Color: `var(--color-text)`.
- Text-align: center.
- Two lines:
  - Line 1 (nowrap): `Lock` [Zap icon 24px] `Down Your` [LockKeyhole icon 24px] `Passwords`
  - Line 2: `with Ironclad Security` [Fingerprint icon 24px]
- All inline icons: color `#192837`, `display: inline`, `verticalAlign: middle`, `position: relative`, `top: -2px`, margin `0 4px` (Fingerprint has `marginLeft: 6px` only).
- Animates: fade-up from `y: 28`, `opacity: 0`, duration 0.6s, ease `[0.22, 1, 0.36, 1]`, delay `0 * 0.15`.

**Subtext (`<p>`):**
- Font: `var(--font-body)`.
- Size: `clamp(0.9rem, 2.5vw, 1.1rem)`.
- Color: `var(--color-text)` at `opacity: 0.8`.
- Max-width: `560px`, line-height `1.65`, text-align center.
- Copy: "Zero stress, total control. Unbreakable storage, one-tap access, and pro-grade tools for your non-stop world."
- Animates: same fade-up, delay `1 * 0.15`.

**CTA Button:**
- Pill button (`borderRadius: 50px`), background `#7342E2`, white text.
- Size: `clamp(0.9rem, 2vw, 1rem)`, padding `17px 24px`, min-width `210px`.
- Box-shadow: `0 4px 24px rgba(115,66,226,0.28)`.
- Flexbox with `justify-between`, gap `32px`.
- Label: "Get It Free" with `ArrowRightCircle` icon (20px) on right.
- Hover: `scale: 1.04, brightness(1.1)`. Tap: `scale: 0.96`.
- Animates: same fade-up, delay `2 * 0.15`.

---

### Animation System (Framer Motion variants)

All hero elements use a shared `fadeUp` variant:
```
hidden: { opacity: 0, y: 28 }
visible: (i) => ({ opacity: 1, y: 0, transition: { delay: i * 0.15, duration: 0.6, ease: [0.22, 1, 0.36, 1] } })
```

---

### Dependencies

- `react`, `react-dom` (v18)
- `framer-motion`
- `lucide-react` (icons: ArrowRightCircle, Zap, LockKeyhole, Fingerprint, Menu, X)
- Tailwind CSS 3 with default config, no custom theme extensions
- Vite + TypeScript
```

---

## 59. Radial Diagram

- **Category**: Testimonials
- **Type**: testimonials
- **Page Type**: hero
- **ID**: `radial-diagram`

```
Build an "Our Comprehensive Branding Approach" section as a React component using TypeScript, Tailwind CSS 3, and Framer Motion. The section sits on a dark background (`#0f0f0f`) with white text. Font is `'DM Sans', sans-serif` (loaded via Google Fonts: `https://fonts.googleapis.com/css?family=DM+Sans:500,400`). Here is the exact specification:

---

**Overall Section Container:**

- `<section>` with `overflow-x-hidden`, `bg-[#0f0f0f]`, `text-white`, inline style `fontFamily: "'DM Sans', sans-serif"`

- Inner wrapper: `mx-auto max-w-7xl px-6 py-24 sm:px-10 lg:px-16 lg:py-32`

- All animations use the easing curve `[0.22, 1, 0.36, 1]` and trigger once when scrolled into view using Framer Motion's `useInView` with `{ once: true, margin: "-60px" }`

---

**Header (top of section):**

- Flex row (`flex items-start gap-4`) with `mb-20`

- Two lines of text stacked vertically:

  - Line 1: "Our Comprehensive" in `text-[#6e6e6e]` (gray), `font-light`, size `clamp(2rem, 3.4vw, 2.6rem)`, `leading-[1.18]`, `tracking-[-0.01em]`. Animates from `opacity:0, y:20` to visible, duration `0.7s`.

  - Line 2: "Branding Approach" in `text-white`, same font styling. Same animation but with `delay: 0.1s`.

- A small square button to the right: `h-7 w-7`, `border border-white/20`, contains a plus icon (SVG: two perpendicular lines forming a +, `stroke="currentColor"`, `strokeWidth="1.3"`, viewBox `0 0 12 12`). Text color `text-white/70`, hover: `bg-white/10 text-white`. Animates scale from 0.8 to 1, opacity 0 to 1, delay `0.25s`.

---

**Content Row (below header):**

- `flex flex-col gap-12 lg:flex-row lg:items-start lg:gap-10`

- Left side: `flex min-w-0 flex-1 flex-col gap-8 sm:flex-row sm:items-start sm:gap-10` containing the portrait and testimonial

- Right side: the circle diagram

---

**Left: Glitch Portrait**

- Container: `relative shrink-0`, fixed size `width: 250px`, `height: 310px`

- Contains an `<img>` filling the container with `object-cover`, using this Pexels image: `https://images.pexels.com/photos/3778212/pexels-photo-3778212.jpeg?auto=compress&cs=tinysrgb&w=600`

- 10 small white glitch blocks (`bg-white`) absolutely positioned around the edges of the portrait (some overflow outside). Each block has a fixed pixel `width` and `height` and percentage-based `left`/`top`. They animate in with `scale: 0 -> 1`, `opacity: [0, 1, 0.9]`, staggered by `0.05s` starting at `delay: 0.5s`, duration `0.35s`.

- The exact glitch block positions (x%, y%, width px, height px):

  ```

  (2, -3, 22, 22), (12, -5, 14, 10), (28, -2, 10, 10),

  (82, 22, 8, 8), (-4, 75, 16, 12), (8, 82, 10, 10),

  (-2, 88, 18, 16), (56, 82, 12, 14), (70, 90, 10, 10),

  (42, 94, 8, 6)

  ```

- The entire portrait group animates from `opacity:0, y:24` to visible, duration `0.8s`, delay `0.2s`.

---

**Left: Testimonial Text (next to portrait)**

- Container: `min-w-0 max-w-[420px]`

- Opening curly quote character `\u201C` in `text-[#555]`, font `Georgia, 'Times New Roman', serif`, `fontSize: "3.2rem"`, `lineHeight: 0.7`. Animates in with `y:14`, delay `0.3s`.

- Quote paragraph: "We kept seeing the same pattern -- brands with potential lost between messy processes, scattered visuals, and forgettable websites. This studio exists to align it all into one clear, consistent story." Use `&mdash;` for the em-dash. Styled as `text-white/90`, size `clamp(1.05rem, 1.5vw, 1.28rem)`, `font-normal`, `leading-[1.58]`. Animates from `y:20`, delay `0.4s`.

- Attribution block `mt-10`:

  - Name: "Alex West" in `text-[1.15rem] font-medium tracking-[0.01em] text-white`

  - Title: "Founder & Creative Director" (`&amp;` in JSX) in `mt-1 text-[0.85rem] tracking-wide text-[#6e6e6e]`

  - Both animate together from `y:14`, delay `0.55s`.

---

**Right: Circle Diagram**

- Wrapper: `flex w-full max-w-[360px] shrink-0 items-center justify-center self-center sm:max-w-[400px] lg:max-w-[440px]`

- Inner container has `aspect-ratio: 1/1`, position relative, animates opacity 0->1, delay `0.4s`, duration `0.8s`.

- SVG with `viewBox="0 0 100 100"`, absolutely filling the container:

  - A circle centered at `(50, 50)` with radius `30`, `stroke="white"`, `strokeWidth="0.18"`, `opacity="0.45"`

  - 3 lines radiating from center `(50,50)` outward to radius `36` (30+6) at these angles:

    - "websites" at 215 degrees

    - "brands" at 335 degrees

    - "ui/ux design" at 110 degrees

  - Lines default: `strokeWidth: 0.18`, `opacity: 0.45`. On hover of corresponding label: `strokeWidth: 0.6`, `opacity: 1`. Transition duration `0.3s`.

- 3 text labels positioned at radius `46` (30+16) from center at the same angles, using `transform: translate(-50%, -50%)` for centering. Styled with `fontSize: clamp(1.25rem, 2.8vw, 2.4rem)`, `letterSpacing: -0.01em`, `text-white`, `whitespace-nowrap`.

  - Default `fontWeight: 300`, on hover of that label: `fontWeight: 700` (transition `0.25s`).

  - Each label animates in with `opacity:0, y:16` to visible, staggered by `0.15s` starting at delay `0.6s`, duration `0.7s`.

- Hover state is shared: hovering a label highlights both the label (bold) and its corresponding SVG line.

---

**Dependencies:** React 18, Framer Motion (v12+), Tailwind CSS 3. Uses `useState`, `useRef`, `useInView` from framer-motion, and `motion` components for all animations. No external animation libraries beyond Framer Motion.
```

---

## 60. Rocket CTA

- **Category**: CTA
- **Type**: cta
- **Page Type**: hero
- **ID**: `rocket-cta`

```
Build a pixel-faithful recreation of the landing CTA section. Use React 18 + Vite + TypeScript, TailwindCSS, `framer-motion`, `clsx` + `tailwind-merge` as `cn()`. Dark theme background (`#000000`), Inter font, Material Symbols Outlined for icons. Use the white-alpha "landing" palette in `tailwind.config.ts`:

```ts
landing: {
  surface: "rgba(255, 255, 255, 0.10)",
  "surface-hover": "rgba(255, 255, 255, 0.16)",
  border: "rgba(255, 255, 255, 0.10)",
  "border-strong": "rgba(255, 255, 255, 0.20)",
  text: "rgba(255, 255, 255, 0.80)",
  "text-muted": "rgba(255, 255, 255, 0.60)",
}
```

Add a global `.liquid-glass` utility (frosted translucent surface):
```css
.liquid-glass {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 10px 30px rgba(0,0,0,0.25);
}
```

Add keyframes in `index.css` for the inner Velorah hero animation:
```css
@keyframes fade-rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-rise          { animation: fade-rise .8s ease-out both; }
.animate-fade-rise-delay    { animation: fade-rise .8s ease-out .25s both; }
.animate-fade-rise-delay-2  { animation: fade-rise .8s ease-out .5s both; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { scrollbar-width: none; }
```

Load fonts in `index.html`: Inter (400/500/600), Instrument Serif (400 + italic), Material Symbols Outlined.

---

## Assets

- Foreground "grass / horizon" PNG that overlays the bottom of the section — load directly from this URL (no local asset):
  `https://res.cloudinary.com/dy5er7kv5/image/upload/q_auto/f_auto/v1780586778/cta-bg_mlwy5s.png`
- CloudFront video URL used **inside** the Velorah dashboard preview (exact):
  `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4`

---

## Helper components (must exist)

### `FadeUp` (`framer-motion`)
```tsx
<motion.div
  initial={{ opacity: 0, y: y ?? 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.3 }}
  transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
/>
```

### `MIcon` — Material Symbols Outlined span, supports `name`, `size`, `fill`, `weight`, `grade`, `opticalSize`, applied via `fontVariationSettings: "'FILL' x, 'wght' y, 'GRAD' z, 'opsz' s"`.

### `PrimaryButton` (landing primitive)
- White pill, black text, `rounded-full`, sizes `sm/md/lg` (default `lg`: `h-12 px-9 text-sm font-medium`).
- Class: `inline-flex items-center justify-center rounded-full bg-white/80 hover:bg-white text-black leading-none transition-colors`.
- Wraps children in an `AnimatedText` component that slides current text up and reveals duplicate from below on hover (200–300ms ease).
- Polymorphic via `as="a" | "button"`, default `a`.

### `ChatPanel` (left side of the dashboard mock)
- Vertical flex column inside `rounded-2xl border border-white/10`, background `rgba(8,8,10,0.6)` + `backdrop-filter: blur(24px)`.
- Header row: 28px circular `bg-white/5` with `MIcon name="auto_awesome" size={14}`, then two-line label: **"Vibe Design course"** (text-sm font-medium white) + **"Learn how to build website with AI"** (text-[11px] white/40).
- Messages scroll area (`scrollbar-hide`, `space-y-4`, px-4 py-5). Seed messages:
  1. assistant — "Welcome to the Vibe Design course! I'll guide you through building stunning websites with AI. What would you like to learn first?"
  2. user — "I want to learn how to build a hero section with a cinematic video background using AI."
  3. assistant — "Great choice! In this course, you'll learn how to create full-screen looping videos, liquid glass nav bars, email signups, and manifesto buttons — all with AI assistance. Let's dive in!"
- Message bubbles: `max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed`. User = `bg-white/15 text-white/90` (right-aligned). Assistant = `bg-white/5 text-white/70 border border-white/5` (left).
- Props: `initialScroll?: "top" | "bottom"` (CTA uses `"top"`), `animateMessagesIn?: boolean` (CTA passes `true`, each message wrapped in `FadeUp delay={i * 0.12} y={16}`).
- Input row: `.liquid-glass rounded-2xl` containing a 1-row autosize `<textarea>` (transparent, placeholder "Ask about the course...") + white square send button (`bg-white text-black rounded-xl p-2`) with `MIcon name="arrow_upward" size={16}`. Enter (no shift) sends. Pushing user msg also pushes a canned assistant reply.

### `VelorahHeroPreview` (right side of the dashboard mock)
```tsx
const VIDEO_SRC = "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4";
```
- Wrapper: `relative w-full h-full overflow-hidden rounded-2xl`, inline `backgroundColor: "hsl(201 100% 13%)"` (deep teal as the video-loading color).
- `<video autoPlay loop muted playsInline preload="auto">` absolutely positioned, `object-cover`, `z-0`.
- Nav row (`relative z-10 flex items-center justify-between px-3 sm:px-4 md:px-6 py-2 sm:py-3 md:py-4`):
  - Left brand: `Velorah®` with `font-family: 'Instrument Serif', serif`, `text-sm sm:text-base md:text-lg`, `tracking-tight`, `®` as `<sup className="text-[0.5em]">`.
  - Center (hidden < md): `Home` (white) · `Studio` · `About` · `Journal` · `Reach Us` — `text-[9px] lg:text-[10px] text-white/60` with `hover:text-white` on the inactive items.
  - Right: `.liquid-glass rounded-full px-2.5 sm:px-3 py-1 text-[9px] sm:text-[10px] text-white` reading **Begin Journey**.
- Hero block (`flex flex-col items-center text-center px-3 sm:px-4 pt-3 sm:pt-5 md:pt-7 pb-6`):
  - `<h1>` Instrument Serif, `font-normal leading-[0.95] tracking-[-0.03em]`, `text-lg sm:text-2xl md:text-3xl lg:text-4xl max-w-[90%]`, class `animate-fade-rise`. Content: `Where <em class="not-italic text-white/55">dreams</em> rise <em class="not-italic text-white/55">through the silence.</em>`
  - Paragraph `animate-fade-rise-delay text-white/60 text-[9px] sm:text-[11px] md:text-xs leading-relaxed max-w-[80%] sm:max-w-sm md:max-w-md mt-2 sm:mt-3 md:mt-4`: "We're designing tools for deep thinkers, bold creators, and quiet rebels. Amid the chaos, we build digital spaces for sharp focus and inspired work."
  - Pill button `animate-fade-rise-delay-2 liquid-glass rounded-full px-4 sm:px-5 md:px-6 py-1.5 sm:py-2 md:py-2.5 text-[9px] sm:text-[10px] text-white mt-3 sm:mt-4 md:mt-5` reading **Begin Journey**.

### `CtaDashboardMock`
Frame around ChatPanel + VelorahHeroPreview:
```tsx
<div className="liquid-glass w-full max-w-[1100px] aspect-[3/4] sm:aspect-[16/10] lg:aspect-[16/9] rounded-2xl mx-auto overflow-hidden p-2 sm:p-3">
  <div className="grid h-full grid-cols-1 sm:grid-cols-[minmax(220px,320px)_1fr] gap-2 sm:gap-3">
    <div className="min-h-0 hidden sm:block"><ChatPanel initialScroll="top" animateMessagesIn /></div>
    <div className="min-h-0"><VelorahHeroPreview /></div>
  </div>
</div>
```

---

## `CtaSection` — exact layout & behavior

```tsx
const sectionRef = useRef<HTMLElement>(null);
const isMobile = useIsMobile(); // tailwind md breakpoint hook
const { scrollYProgress } = useScroll({ target: sectionRef, offset: ["start end", "end start"] });
const dashboardY = useTransform(scrollYProgress, [0, 1], ["120px", "-120px"]);
const grassY     = useTransform(scrollYProgress, [0, 1], isMobile ? ["80px", "-40px"] : ["200px", "-200px"]);
```

Markup:
```tsx
<section
  ref={sectionRef}
  id="cta"
  className="relative w-full"
  style={{ background: "linear-gradient(to bottom, transparent 0%, #14191E 100%)" }}
>
  <div className="relative mx-auto max-w-[1080px] px-4 sm:px-6 pt-24 sm:pt-32 md:pt-40 pb-[440px] sm:pb-[520px] md:pb-[440px]">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-start">
      {/* Left column */}
      <div className="relative z-20 max-w-[400px]">
        <FadeUp delay={1}>
          <h2 className="text-3xl sm:text-4xl font-normal tracking-[-0.02em] leading-[1.05] text-foreground">
            Learn how can one go from 0 to $11.5k with AI in 60 days.
          </h2>
        </FadeUp>
        <FadeUp delay={0.1}>
          <p className="mt-6 text-landing-text text-base sm:text-lg leading-[1.5] max-w-[380px]">
            Learn to turn your ideas into stunning websites with AI — the same skills agencies charge $5,000 for. Join the UI Rocket training and start building like a pro today.
          </p>
        </FadeUp>
        <FadeUp delay={0.2} className="mt-10">
          <PrimaryButton as="button">Start for free</PrimaryButton>
        </FadeUp>
      </div>
    </div>
  </div>

  {/* Dashboard pinned to right edge, behind grass, parallax Y */}
  <motion.div
    style={{ y: dashboardY }}
    className="absolute top-[440px] sm:top-[460px] md:top-[500px] lg:top-20 left-4 right-4 sm:left-auto sm:-right-[8%] md:-right-[10%] lg:-right-[12%] z-10 sm:w-[85%] md:w-[80%] lg:w-[68%]"
  >
    <CtaDashboardMock />
  </motion.div>

  {/* Foreground grass — in front of dashboard, parallax Y */}
  <motion.img
    src="https://res.cloudinary.com/dy5er7kv5/image/upload/q_auto/f_auto/v1780586778/cta-bg_mlwy5s.png"
    alt=""
    aria-hidden
    style={{ y: grassY }}
    className="pointer-events-none select-none absolute left-0 right-0 bottom-[-40px] sm:bottom-[-80px] lg:bottom-[-140px] w-full z-30 object-cover"
  />
</section>
```

### Behavior summary
- Section fades from transparent → `#14191E` vertically.
- On scroll, the dashboard translates from `+120px` → `-120px` (parallax up). The grass image translates `+200px` → `-200px` desktop, `+80px` → `-40px` mobile, on top of the dashboard (`z-30` over `z-10`).
- Left column stays static, on top of the grass (`z-20` left text container would otherwise be covered — keep grass at `z-30` to overlap the dashboard while the heading visually sits left of it).
- Headline `Learn how can one go from 0 to $11.5k with AI in 60 days.` enters with a delayed FadeUp; paragraph + button stagger in afterward.
- Mobile (< sm): dashboard stacks below the heading (`top-[440px]`), chat panel hides (`hidden sm:block`), only the Velorah preview shows.
- Button is `PrimaryButton as="button"` reading **Start for free**; hover triggers the AnimatedText slide.

---

## Acceptance checklist
- [ ] Section bg: `transparent → #14191E` linear gradient bottom.
- [ ] Inter font globally; Instrument Serif used in Velorah brand + headline; Material Symbols Outlined for icons.
- [ ] Headline copy is exactly: `Learn how can one go from 0 to $11.5k with AI in 60 days.`
- [ ] Subtext copy is exactly the paragraph above; button label exactly `Start for free`.
- [ ] `CtaDashboardMock` uses `.liquid-glass` frame, aspect `3/4 → 16/10 → 16/9`, ChatPanel left (hidden on mobile) + Velorah right.
- [ ] Velorah `<video>` uses the exact CloudFront URL, `autoPlay loop muted playsInline preload="auto"`, fallback bg `hsl(201 100% 13%)`.
- [ ] Velorah inner copy/animation classes match (`animate-fade-rise`, `-delay`, `-delay-2`).
- [ ] `useScroll` + `useTransform` parallax: dashboard `120 → -120`, grass `200 → -200` (desktop) / `80 → -40` (mobile).
- [ ] Grass image loaded from Cloudinary URL (`https://res.cloudinary.com/dy5er7kv5/image/upload/q_auto/f_auto/v1780586778/cta-bg_mlwy5s.png`) sits at `z-30` over dashboard (`z-10`), pointer-events-none, full width.
- [ ] FadeUp entrance order: heading (delay 1) → paragraph (0.1) → button (0.2).
- [ ] PrimaryButton: white pill, black text, AnimatedText hover slide.
```

---

## 61. PROMPT

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `prompt-hero`

```
### Overview

Build a full-screen, scroll-driven fashion/archive landing page for a brand called "prmpt". The page has two main phases:

1. **Hero phase** (first 100vh of scroll): Full-viewport video background with overlaid UI (logo, nav, product info, custom cursor). A black panel slides up from below covering the video.
2. **Gallery phase** (continues scrolling): The black panel contains a scattered grid of product images that scale in/out as they enter/exit the viewport. At the end, a white overlay fades in with a "view" CTA button.

---

### Tech Stack

- **React 19** + **TypeScript**
- **Vite 6** with `@vitejs/plugin-react`
- **Tailwind CSS v4** via `@tailwindcss/vite` plugin
- **GSAP 3.15** + `@gsap/react` (ScrollTrigger)
- **Motion (Framer Motion) 12** (`motion/react`)
- **Font**: "Inter Tight" (Google Fonts, weight 500) -- loaded via `<link>` or import

---

### Asset URLs

**Videos (CloudFront):**
- LEFT video: `https://d8j0ntlcm91z4.cloudfront.net/user_39ca84eAE1ODL9hbR5VhoEj8tBf/hf_20260625_154433_532a85d3-dabf-4265-b8bd-19ac6af31842.mp4`
- RIGHT video: `https://d8j0ntlcm91z4.cloudfront.net/user_39ca84eAE1ODL9hbR5VhoEj8tBf/hf_20260625_154401_a664f076-b971-4557-8728-40ef9ea4c49b.mp4`

**Gallery Images (10 total, in order):**
1. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_104530_521b2f85-c0f3-4d0e-9704-b578315b4cb9.png&w=1920&q=85`
2. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103711_76ccdb8b-5043-4f47-9c54-4379713393ea.png&w=1920&q=85`
3. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103728_394f6a1b-85e2-4386-a4f6-408472a0a5b7.png&w=1920&q=85`
4. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103739_86743e0e-16a7-4bee-bf38-dd67985344dc.png&w=1920&q=85`
5. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103748_b2215dc8-a3a7-470d-b19a-5b87fa7d0c37.png&w=1920&q=85`
6. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103758_e919ce72-5c9d-4b87-9be6-d7647b34825c.png&w=1920&q=85`
7. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103808_013583d0-3386-4547-9832-37c7d8edb3ac.png&w=1920&q=85`
8. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103937_a0c49d0a-33eb-4ead-aea6-c1baf241acbc.png&w=1920&q=85`
9. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_103956_d18ed8fd-7b6f-4b86-91f9-20010fe38670.png&w=1920&q=85`
10. `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260629_104034_ba5a9963-87ff-4008-a545-6bd686c088b5.png&w=1920&q=85`

---

### SECTION 1: Hero (Video Background + Overlaid UI)

#### Root Container
- `id="scroll-spacer"`, `position: relative`, `user-select: none`, `background: white`
- Height is dynamically calculated (initially `500vh`, then overridden by GSAP to `vh + maxScroll + 2*vh`)
- Custom cursor hidden on desktop (`cursor: none`), default on touch devices

#### 1A. Custom Cursor (Desktop Only)
- Hidden on mobile/tablet (< 1024px)
- A `fixed`, `pointer-events-none`, `z-index: 50` div that follows `mousemove`
- Positioned via direct DOM manipulation (`style.left/top = clientX/clientY`)
- `transform: translate(-50%, -50%)` to center on pointer
- `mix-blend-mode: exclusion`
- Contains a 48x48 SVG: a circle with stroke (r=22.75, strokeWidth=2.5) containing a custom Japanese/decorative glyph path, all filled white

#### 1B. Logo (Top Left)
- `position: fixed`, `pointer-events-none`, `z-index: 20`
- `mix-blend-mode: exclusion`
- Responsive width: 124px (mobile < 640), 266px (tablet 640-1024), 355px (desktop)
- Position: `top: 16px, left: 16px` (mobile), `top: 32px, left: 32px` (desktop)
- Motion animation: fade in + slide up (`opacity: 0->1, y: 12->0`), duration 0.6s, ease `[0.25, 0.1, 0.25, 1]`, delay 0s
- SVG viewBox `0 0 355 110`, contains the "prmpt" wordmark + circled "R" mark, all paths filled white

#### 1C. Caption (Below Logo, Left Side)
- `position: fixed`, `pointer-events-none`, `z-index: 20`
- `mix-blend-mode: exclusion`
- Position: `left: 32px` (desktop), `left: 16px` (mobile)
- Top: 244px (desktop), 180px (tablet), 118px (mobile)
- Width: 692px (desktop), `calc(50vw - 48px)` (tablet), `calc(100vw - 32px)` (mobile)
- Font: Inter Tight, weight 500, size 12px, line-height 140%, letter-spacing -0.04em, color #FFFFFF
- Motion animation: same as logo but delay 0.3s
- Text content: "When switching between videos near the center, do not reset currentTime to 0 abruptly. Add a small dead zone: if cursor is within +/-50px of center, keep both videos at currentTime = 0 and show whichever was last active."

#### 1D. Header Navigation (Top Right)
- `position: fixed`, `z-index: 20`, `pointer-events-none`
- `mix-blend-mode: exclusion`
- Position: `top: 32px, right: 32px` (desktop), `top: 16px, right: 16px` (mobile)
- Width: 330px (desktop), auto (mobile)
- Height: 30px
- Flex row, justify-content: space-between, align-items: center
- Motion animation: same easing, delay 0.15s
- Contains:
  - "ABOUT" text (hidden on mobile): Inter Tight, 500, 15px, uppercase, white
  - A flex row with gap 50px (desktop) / 20px (mobile):
    - Hamburger SVG icon: viewBox `0 0 40 40`, two horizontal lines (`M0 14H40` and `M0 26H40`), stroke white, strokeWidth 2.5. Size: 30x30 (desktop), 24x24 (mobile)
    - "[ CART ]" text: Inter Tight, 500, 15px (desktop) / 13px (mobile), white

#### 1E. Product Info (Bottom Right)
- `id="outro-info"`, `position: fixed`, `pointer-events-none`, `z-index: 20`
- `mix-blend-mode: exclusion`
- **Desktop**: right: 32px, bottom: 80px, width: 330px, flex-column, align center
- **Mobile**: left: 0, right: 0, bottom: 48px, flex-column, align center
- Motion animation: opacity 0->1, delay 0.45s
- `data-outro-offset`: 166 (desktop), 132 (mobile) -- used by scroll animation
- Contains:
  - Top block (flex-column, align flex-start, width 100% desktop / 252px mobile, margin-bottom 32px desktop / 12px mobile):
    - Circle icon: relative div (30x30 desktop, 20x20 mobile) containing:
      - SVG circle (cx=20, cy=20, r=18.75, stroke white, strokeWidth 2.5 desktop / 2 mobile)
      - `<span id="circle-symbol">` centered inside, shows "8" initially, changes to random symbol from `['8', '$', '^^', '%', '/']` on scroll (throttled 80ms)
      - Font: Inter Tight, 500, 15px (desktop) / 10px (mobile), letter-spacing -0.04em, uppercase, white
    - Collection label: Inter Tight, 500, 30px (desktop) / 20px (mobile), line-height 100%, text-align center, letter-spacing -0.04em, uppercase, white. Content: `ARCHIVE COLLECTION` + line break + `"PROMPT"`
  - Price: Inter Tight, 500, 80px (desktop) / 60px (mobile), line-height 100%, text-align center, letter-spacing -0.04em, white. Content: `$97,33`

#### 1F. "View" Button (Bottom Right, Initially Hidden)
- `id="outro-buy"`, `position: fixed`, `pointer-events-none`, `z-index: 20`
- `mix-blend-mode: exclusion`
- **Desktop**: right: 32px, bottom: 32px, width: 330px, height: 174px
- **Mobile**: left: 16px, right: 16px, bottom: 60px, height: 100px
- `transform-origin: right bottom`, `transform: scale(0)` (starts hidden, scales to 1 via scroll)
- Background: #fff, border-radius: 1335px (pill shape)
- Flex center
- Text "view": Inter Tight, 500, 110px (desktop) / 72px (mobile), letter-spacing -0.04em, color #fff, `mix-blend-mode: exclusion`

#### 1G. Video Container
- `id="main-canvas"`, `pointer-events-none`
- **Desktop**: `position: fixed, inset: 0, width: 100%, height: 100%, z-index: 0`
- **Mobile**: `position: fixed, left: 0, top: 220px, width: 100vw, height: calc(100vh - 220px), z-index: 0`
- Opacity transition: 0 -> 1 when both videos loaded (`opacity 0.3s ease`)
- `overflow: hidden`
- Contains two `<video>` elements (muted, playsInline, preload="auto"), absolutely positioned to fill container, `object-fit: cover`
- Left video starts `display: none`, right starts `display: block`


**Desktop (non-touch):**
- Videos are NOT auto-played. They are scrubbed based on cursor X position via `requestAnimationFrame`.
- Dead zone: `Math.max(30, width * 0.05)` pixels from center
- If cursor is in dead zone, keep current video at `currentTime = 0`
- If cursor moves left of dead zone: show RIGHT video, scrub it based on distance from center-left-edge to left edge
- If cursor moves right of dead zone: show LEFT video, scrub it based on distance from center+deadzone to right edge
- `activeSideRef` tracks which side was last active, only changes when cursor exceeds dead zone
- Progress calculation: `(distance from dead zone edge) / (available range)` mapped to `0...video.duration`
CRITICAL: Only update currentTime when !video.seeking -- this prevents jittery playback by waiting for the browser to finish rendering the previous seek before requesting a new one.
#### 1H. Video Interaction Logic

**Mobile/Tablet (touch):**
- Videos auto-play alternately: left plays first, on `ended` event switches to right, on right `ended` switches back to left
- Respects `prefers-reduced-motion`

#### 1I. White Overlay
- `id="outro-overlay"`, `position: fixed, inset: 0`, `pointer-events-none`, `z-index: 12`
- Background: #fff, opacity: 0 (controlled by scroll)

#### 1J. Footer
- `id="outro-footer"`, `position: fixed`, `pointer-events-none`
- Left: 16px, bottom: 32px (desktop) / 24px (mobile)
- `mix-blend-mode: exclusion`, opacity: 0 (controlled by scroll)
- Flex row, gap: 80px (desktop) / space-between (mobile)
- Two spans: "PRMPT (R) 2026" and "PRIVACY POLICY"
- Font: Inter Tight, 500, 13px (desktop) / 11px (mobile), letter-spacing -0.02em, uppercase, white

---

### SECTION 2: Black Panel (Gallery)

#### Container
- `position: fixed, inset: 0`, background: black, `z-index: 10`
- Initially translated `translateY(100vh)` (off-screen below)
- Slides up to `translateY(0)` during first 100vh of scroll via GSAP ScrollTrigger (scrub: true, ease: none)

#### Inner Wrapper
- `width: 100%`, `padding-top: min(400px, 40vh)`

#### Grid Layout Algorithm
- Responsive columns: 2 (< 640px), 3 (640-1024px), 4 (>= 1024px)
- Each cell has `aspect-ratio: 2/3`
- Layout function `buildLayout(count, cols)` creates rows:
  - For each row `r`, compute primary column: `a = (r * 2 + (r % 2)) % cols`
  - Place one image at column `a`
  - Every 3rd row (`r % 3 === 0`), place a second image at `b = (a + 2) % cols` (or `(a+1)%cols` if same as a)
  - Empty cells get `-1` (rendered as empty spacer divs)

#### Card Behavior
- Each card has class `bp-card`, `will-change: transform`
- `transform: scale(0)` initially
- `transform-origin`: cards in left half of grid get `right bottom`, right half get `left bottom`
- Scale is computed per-frame in RAF based on card's vertical position:
  - **Enter**: `Math.min(1, (vh - top) / (vh * 0.6))` -- scales from 0 to 1 as it enters viewport
  - **Exit**: `Math.min(1, bottom / (vh * 0.4))` -- scales from 1 to 0 as it exits top
  - Final scale: `Math.min(enter, exit)`
  - If card is fully off-screen (bottom <= 0 or top >= vh): `scale(0)`

#### Scroll Phases (RAF-based, NOT scroll events)
- **Phase 1** (scrollY 0 to vh): Panel slides up. Cards are computed with panelOffset = `vh - scrollY`
- **Phase 2** (scrollY > vh): Panel is fixed at top. Inner wrapper translates up: `translateY(-(scrollY - vh))`. Cards recomputed with phase2 offset.
- **Outro** (scrollY > vh + maxScroll): White overlay fades in, product info slides up by `outroOffset` px, "view" button scales from 0 to 1, footer fades in. Progress: `(scrollY - vh - maxScroll) / (vh - 100)`

#### Spacer Height Calculation
- Set dynamically: `vh + maxScroll + 2 * vh` where `maxScroll = wrapScrollHeight - vh`

---

### CSS (index.css)

```css
@import "tailwindcss";

.bp-card {
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .bp-card {
    will-change: auto;
  }
}
```

---

### Responsive Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: >= 1024px

---

### Key Design Principles
- All text overlays use `mix-blend-mode: exclusion` to remain visible against both light and dark backgrounds
- No visible scroll bar interaction -- entirely RAF-driven position tracking
- `pointer-events-none` on all overlaid UI elements
- `user-select: none` on root container
- Videos hidden (`visibility: hidden`) once scroll passes first viewport height
- Circle symbol randomizes on scroll (throttled to 80ms)
- Entry animations staggered: logo (0s), nav (0.15s), caption (0.3s), product info (0.45s)
```

---

## 62. Guardnet Benefits

- **Category**: Benefits
- **Type**: features
- **Page Type**: hero
- **ID**: `guardnet-benefits`

```
Build a single React + TypeScript section using Tailwind CSS. No extra libraries. Fully mobile-responsive. Black background, white text.

## Global Prerequisites

- Font: `@import url(https://db.onlinewebfonts.com/c/e55e9079ee863276569c8a68d776ef04?family=Futura+Md+BT+Medium);`
- Body: `font-family: 'Futura Md BT Medium', system-ui, -apple-system, sans-serif; background-color: #000; color: #fff; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`
- Section sits inside a `w-full max-w-[1400px]` wrapper on a black page.

---

## BenefitsSection

Container: `relative w-full bg-black px-4 sm:px-6 md:px-10 py-12 sm:py-20`

### Section Heading

`text-white text-3xl sm:text-4xl md:text-5xl font-light text-center mb-12 sm:mb-24` with inline style `letterSpacing: '-0.04em'`

Text: **"Key Benefits"**

### Three-Column Card Grid

`grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4`

All three cards share: `relative h-[380px] sm:h-[460px] rounded-2xl bg-neutral-950 overflow-hidden`

---

#### Card 1: Text Card (Left)

Additional classes: `p-6 sm:p-8`

**Blue Blob:** `absolute top-1/2 -translate-y-1/2 -left-[420px] h-[460px] w-[460px] rounded-full bg-[#1e3a8a] blur-3xl opacity-40`

**Content wrapper:** `relative z-10 flex flex-col h-full`

**Heading:** `text-white text-xl sm:text-2xl font-light leading-tight`
Text (two lines with `<br />`):
```
Preemptive Risks
Scouting and Reactions
```

**Body paragraph:** `mt-12 sm:mt-20 text-[13px] sm:text-[14px] leading-relaxed text-white/70 font-light max-w-[280px]`
Text: **"Defense platforms constantly observe bandwidth streams, record files, and machine behaviors to uncover unusual patterns or outliers that could signal a defensive failure."**

---

#### Card 2: Video Card (Center)

Additional classes: `flex flex-col` (no padding on card itself)

**Top video region:** `relative w-full overflow-hidden` with inline style `height: '75%'`

- `<video>` element: `w-full h-full object-cover block`, attributes: `autoPlay loop muted playsInline`
- **Exact URL:** `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260421_072701_f6a01abb-eb30-4559-9d6e-774362defbc3.mp4`
- **Bottom fade overlay inside video wrapper:** `pointer-events-none absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-b from-transparent to-neutral-950`

**Bottom text region:** `flex-1 flex items-center justify-start p-6 sm:p-8`

**Heading:** `text-white text-xl sm:text-2xl font-light leading-tight text-left`
Text (two lines with `<br />`):
```
Know-how and Sectoral
Awareness
```

---

#### Card 3: Text Card (Right)

Additional classes: `p-6 sm:p-8`

**Blue Blob:** `absolute -top-28 -right-28 h-56 w-56 rounded-full bg-[#1e3a8a] blur-3xl opacity-40`

**Content wrapper:** `relative z-10 flex flex-col h-full`

**Heading:** `text-white text-xl sm:text-2xl font-light leading-tight`
Text (two lines with `<br />`):
```
Preemptive Risks
Scouting and Reactions
```

**Body paragraph:** `mt-auto text-[13px] sm:text-[14px] leading-relaxed text-white/70 font-light max-w-[320px]`
Text: **"Defense platforms constantly observe bandwidth streams, record files, and machine behaviors to uncover unusual patterns or outliers that could signal a defensive failure."**

Key difference from Card 1: the paragraph uses `mt-auto` to pin it to the **bottom** of the card, versus Card 1 which uses `mt-12 sm:mt-20` to place it in the **middle**.

---

## Color Palette Reference

| Token | Hex |
|---|---|
| Background | `#000000` (black) |
| Card surface | `neutral-950` (Tailwind) |
| Blob blue | `#1e3a8a` |
| Video fade target | `neutral-950` (matches card bg) |
| Body text | `white/70` |
| Heading text | `white` |

## Responsive Breakpoints

- Default (mobile): `< 640px` -- cards stack in a single column
- `sm:` at `640px` -- cards grow taller (460px), text/padding increases
- `md:` at `768px` -- switches to 3-column grid layout

## Interactions

- No hover states or JavaScript animations
- All motion comes from the looping background video in Card 2
- The bottom fade on the video blends seamlessly into the `neutral-950` card surface
```

---

## 63. AI Workflow Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `ai-workflow`

```
### Stack

- **Vite** + **React 18** + **TypeScript**
- **Tailwind CSS 3.4**
- **lucide-react** for icons (`LogIn`, `UserPlus`, `Play`, `Sparkles`, `Menu`, `X`)
- No Framer Motion -- all animations are CSS `transition-*` classes

---

### Fonts (loaded in `index.html`)

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
<link href="https://db.onlinewebfonts.com/c/6e47ef470dd19698c911332a9b4d1cf4?family=Neue+Haas+Grotesk+Text+Pro" rel="stylesheet" />
<link href="https://db.onlinewebfonts.com/c/dec0d9b4e22ca588dc20e1e2e09a59b5?family=Neue+Haas+Grotesk+Display+Pro+55+Roman" rel="stylesheet" />
```

Body/root font stack (in `index.css`):

```css
html, body, #root {
  height: 100%;
  margin: 0;
  font-family: 'Neue Haas Grotesk Display Pro 55 Roman', 'Neue Haas Grotesk Text Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
```

---

### Video URL (CloudFront)

```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_131941_d136af49-e243-493a-be14-6ff3f24e09e6.mp4
```

---

### Color Palette

| Token | Hex |
|-------|-----|
| Dark green (text, buttons) | `#1f2a1d` |
| Medium dark green | `#2d3a2a` |
| Button hover | `#2a3827` |
| Body text green | `#4b5b47` |
| Heading primary | `#336443` |
| Heading accent | `#85AB8B` |
| Bottom-left text | `#3d5638` |
| Bottom-left button bg | `#3d5638`, hover `#2d4228` |

---

### Architecture

Two files:

1. **`BoomerangVideoBg.tsx`** -- captures video frames into canvas, then plays them forward/backward in a seamless boomerang loop at 30fps (960px max capture width).
2. **`App.tsx`** -- the full hero section.

---

### `BoomerangVideoBg.tsx` (exact)

```tsx
import { useEffect, useRef, useState } from 'react';

type Props = {
  src: string;
  className?: string;
};

export default function BoomerangVideoBg({ src, className }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const displayCanvasRef = useRef<HTMLCanvasElement>(null);
  const [framesReady, setFramesReady] = useState(false);
  const framesRef = useRef<HTMLCanvasElement[]>([]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const frames: HTMLCanvasElement[] = [];
    let capturing = true;
    let lastTime = -1;
    const MAX_WIDTH = 960;

    const captureFrame = () => {
      if (!capturing || video.readyState < 2) return;
      if (video.currentTime === lastTime) return;
      lastTime = video.currentTime;

      const vw = video.videoWidth;
      const vh = video.videoHeight;
      if (!vw || !vh) return;

      const scale = Math.min(1, MAX_WIDTH / vw);
      const w = Math.round(vw * scale);
      const h = Math.round(vh * scale);

      const canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      ctx.drawImage(video, 0, 0, w, h);
      frames.push(canvas);
    };

    type VFCVideo = HTMLVideoElement & {
      requestVideoFrameCallback?: (cb: () => void) => number;
    };
    const vfcVideo = video as VFCVideo;
    const hasVFC = typeof vfcVideo.requestVideoFrameCallback === 'function';

    let rafId = 0;
    const rafLoop = () => {
      captureFrame();
      if (capturing) rafId = requestAnimationFrame(rafLoop);
    };

    const vfcLoop = () => {
      captureFrame();
      if (capturing && vfcVideo.requestVideoFrameCallback) {
        vfcVideo.requestVideoFrameCallback(vfcLoop);
      }
    };

    const onEnded = () => {
      capturing = false;
      if (frames.length > 0) {
        framesRef.current = frames;
        setFramesReady(true);
      }
    };

    const onLoaded = () => {
      video.play().catch(() => {});
      if (hasVFC) {
        vfcVideo.requestVideoFrameCallback!(vfcLoop);
      } else {
        rafId = requestAnimationFrame(rafLoop);
      }
    };

    video.addEventListener('loadedmetadata', onLoaded);
    video.addEventListener('ended', onEnded);
    if (video.readyState >= 1) onLoaded();

    return () => {
      capturing = false;
      cancelAnimationFrame(rafId);
      video.removeEventListener('loadedmetadata', onLoaded);
      video.removeEventListener('ended', onEnded);
    };
  }, [src]);

  useEffect(() => {
    if (!framesReady) return;
    const canvas = displayCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const frames = framesRef.current;
    if (frames.length === 0) return;

    const first = frames[0];
    canvas.width = first.width;
    canvas.height = first.height;

    let index = 0;
    let direction = 1;
    let last = performance.now();
    const interval = 1000 / 30;
    let rafId = 0;

    const render = (now: number) => {
      if (now - last >= interval) {
        last = now;
        ctx.drawImage(frames[index], 0, 0);
        index += direction;
        if (index >= frames.length - 1) {
          index = frames.length - 1;
          direction = -1;
        } else if (index <= 0) {
          index = 0;
          direction = 1;
        }
      }
      rafId = requestAnimationFrame(render);
    };
    rafId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(rafId);
  }, [framesReady]);

  return (
    <div className={className ?? 'absolute inset-0 w-full h-full'}>
      <video
        ref={videoRef}
        src={src}
        className="w-full h-full object-cover"
        style={{ display: framesReady ? 'none' : 'block' }}
        muted
        playsInline
        preload="auto"
        crossOrigin="anonymous"
      />
      <canvas
        ref={displayCanvasRef}
        className="w-full h-full object-cover"
        style={{ display: framesReady ? 'block' : 'none' }}
      />
    </div>
  );
}
```

---

### `App.tsx` (exact)

```tsx
import { useState, useEffect } from 'react';
import { LogIn, UserPlus, Play, Sparkles, Menu, X } from 'lucide-react';
import BoomerangVideoBg from './BoomerangVideoBg';

const BG_VIDEO =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_131941_d136af49-e243-493a-be14-6ff3f24e09e6.mp4';

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [menuOpen]);

  const navLinks = [
    { href: '#mission', label: 'Purpose' },
    { href: '#how', label: 'The Process' },
    { href: '#pricing', label: 'Tariffs' },
  ];

  return (
    <section className="relative w-full min-h-screen sm:h-screen overflow-hidden">
      <BoomerangVideoBg src={BG_VIDEO} className="absolute inset-0 w-full h-full" />
      <nav className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 sm:px-6 md:px-10 py-4 sm:py-6">
        <div className="flex items-center gap-2 text-[#2d3a2a]">
          <span className="text-lg sm:text-xl md:text-2xl font-semibold tracking-tight">
            LinkFlow<sup className="text-[10px] sm:text-xs font-medium">TM</sup>
          </span>
        </div>

        <div className="hidden lg:flex items-center gap-1 bg-white/70 backdrop-blur-md rounded-full pl-6 pr-1 py-1 shadow-sm border border-white/60">
          {navLinks.map((link, i) => (
            <a
              key={link.href}
              href={link.href}
              className={`text-sm px-3 py-2 transition-colors ${
                i === 0 ? 'font-semibold text-[#1f2a1d]' : 'font-medium text-[#4b5b47] hover:text-[#1f2a1d]'
              }`}
            >
              {link.label}
            </a>
          ))}
          <button className="ml-2 bg-[#1f2a1d] hover:bg-[#2a3827] text-white text-sm font-medium px-5 py-2.5 rounded-full transition-colors">
            Try it Live
          </button>
        </div>

        <div className="flex items-center gap-3 sm:gap-6 text-[#2d3a2a]">
          <a href="#signup" className="hidden sm:flex items-center gap-2 text-sm font-medium hover:opacity-80 transition-opacity">
            <UserPlus className="w-4 h-4" />
            Sign Me Up!
          </a>
          <a href="#login" className="hidden sm:flex items-center gap-2 text-sm font-medium hover:opacity-80 transition-opacity">
            <LogIn className="w-4 h-4" />
            Enter
          </a>
          <button
            onClick={() => setMenuOpen((v) => !v)}
            className="lg:hidden relative flex items-center justify-center w-10 h-10 rounded-full bg-white/70 backdrop-blur-md border border-white/60 text-[#1f2a1d] transition-all duration-300 hover:bg-white/90"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
          >
            <Menu
              className={`w-5 h-5 absolute transition-all duration-300 ${
                menuOpen ? 'opacity-0 rotate-90 scale-50' : 'opacity-100 rotate-0 scale-100'
              }`}
            />
            <X
              className={`w-5 h-5 absolute transition-all duration-300 ${
                menuOpen ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 -rotate-90 scale-50'
              }`}
            />
          </button>
        </div>
      </nav>

      {/* Mobile menu overlay */}
      <div
        className={`lg:hidden fixed inset-0 z-20 transition-opacity duration-300 ${
          menuOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setMenuOpen(false)}
      >
        <div className="absolute inset-0 bg-[#1f2a1d]/40 backdrop-blur-sm" />
      </div>

      {/* Mobile menu drawer */}
      <div
        className={`lg:hidden fixed top-0 right-0 bottom-0 z-20 w-[85%] max-w-sm bg-white/95 backdrop-blur-xl shadow-2xl transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          menuOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full pt-24 px-8 pb-8">
          <div className="flex flex-col gap-1">
            {navLinks.map((link, i) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setMenuOpen(false)}
                className={`text-2xl font-semibold text-[#1f2a1d] py-4 border-b border-[#1f2a1d]/10 transition-all duration-500 ${
                  menuOpen ? 'translate-x-0 opacity-100' : 'translate-x-8 opacity-0'
                }`}
                style={{ transitionDelay: menuOpen ? `${150 + i * 70}ms` : '0ms' }}
              >
                {link.label}
              </a>
            ))}
          </div>

          <div
            className={`mt-8 flex flex-col gap-4 transition-all duration-500 ${
              menuOpen ? 'translate-x-0 opacity-100' : 'translate-x-8 opacity-0'
            }`}
            style={{ transitionDelay: menuOpen ? '400ms' : '0ms' }}
          >
            <a href="#signup" className="flex items-center gap-2 text-sm font-medium text-[#2d3a2a] sm:hidden">
              <UserPlus className="w-4 h-4" />
              Sign Me Up!
            </a>
            <a href="#login" className="flex items-center gap-2 text-sm font-medium text-[#2d3a2a] sm:hidden">
              <LogIn className="w-4 h-4" />
              Enter
            </a>
            <button className="mt-2 bg-[#1f2a1d] hover:bg-[#2a3827] text-white text-sm font-semibold px-5 py-3 rounded-full transition-colors">
              Try it Live
            </button>
          </div>
        </div>
      </div>

      {/* Hero copy */}
      <div className="relative z-10 flex flex-col items-center text-center pt-24 sm:pt-28 md:pt-32 px-4 sm:px-6">
        <h1
          className="font-normal leading-[0.95] text-[#336443] text-[2rem] sm:text-4xl md:text-5xl lg:text-[4.75rem] xl:text-[5.25rem] max-w-5xl"
          style={{ fontFamily: '"Neue Haas Grotesk Display Pro 55 Roman", "Neue Haas Grotesk Text Pro", "Helvetica Neue", Helvetica, Arial, sans-serif', letterSpacing: '-0.035em' }}
        >
          Close the rift{' '}
          <span className="text-[#85AB8B]">
            linking
            <br className="hidden sm:block" /> signals and action
          </span>
        </h1>
        <p className="mt-6 sm:mt-8 text-[#4b5b47] text-sm sm:text-base md:text-lg leading-relaxed max-w-md px-2">
          Shape scattered signals into meaningful outcomes via AI-driven workflows.
        </p>
      </div>

      {/* Bottom-left CTA block */}
      <div className="absolute left-4 right-4 sm:right-auto sm:left-6 md:left-10 bottom-6 sm:bottom-8 md:bottom-10 z-10 max-w-sm">
        <div className="flex items-center gap-2 text-[#3d5638] sm:text-white/95 mb-3">
          <Sparkles className="w-4 h-4" />
          <span className="text-sm font-semibold sm:font-medium">
            FluxEngine<sup className="text-[10px]">TM</sup>
          </span>
        </div>
        <p className="text-[#3d5638]/90 sm:text-white/85 text-xs leading-relaxed mb-6 max-w-xs font-medium sm:font-normal">
          LinkFlow smoothly unites your company systems, streamlining data paths between services without having to write custom scripts.
        </p>
        <div className="flex items-center gap-4 flex-wrap">
          <button className="bg-[#3d5638] sm:bg-white hover:bg-[#2d4228] sm:hover:bg-white/90 text-white sm:text-[#1f2a1d] text-sm font-semibold px-5 sm:px-6 py-2.5 sm:py-3 rounded-full transition-colors shadow-sm">
            Try it Live
          </button>
          <button className="text-[#3d5638] sm:text-white text-sm font-semibold sm:font-medium hover:opacity-80 transition-opacity">
            Know More.
          </button>
        </div>
      </div>

      {/* Bottom-right video link */}
      <div className="hidden sm:flex absolute right-6 md:right-10 bottom-8 md:bottom-10 z-10 items-center gap-2 text-white/90 text-sm">
        <button className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/30 transition-colors">
          <Play className="w-3 h-3 fill-white text-white ml-0.5" />
        </button>
        <span className="font-medium">How we build?</span>
        <span className="text-white/60">1:35</span>
      </div>
    </section>
  );
}

export default App;
```

---

### Animation Details (all CSS, no Framer Motion)

| Element | Property | Values |
|---------|----------|--------|
| Hamburger Menu/X icon swap | `transition-all duration-300` | Open: Menu gets `opacity-0 rotate-90 scale-50`, X gets `opacity-100 rotate-0 scale-100`. Closed: reverse. |
| Mobile overlay backdrop | `transition-opacity duration-300` | Open: `opacity-100 pointer-events-auto`. Closed: `opacity-0 pointer-events-none`. |
| Mobile drawer slide | `transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]` | Open: `translate-x-0`. Closed: `translate-x-full`. |
| Mobile nav links stagger | `transition-all duration-500` | Open: `translate-x-0 opacity-100`, delay per item: `150ms + i * 70ms`. Closed: `translate-x-8 opacity-0`, delay `0ms`. |
| Mobile CTA group | `transition-all duration-500` | Open: `translate-x-0 opacity-100`, delay `400ms`. Closed: `translate-x-8 opacity-0`, delay `0ms`. |
| Nav buttons | `transition-colors` | Default Tailwind duration (150ms). |
| Opacity links | `transition-opacity` | `hover:opacity-80`. |

---

### Key Layout/Spacing Notes

- Root section: `relative w-full min-h-screen sm:h-screen overflow-hidden`
- Navbar padding: `px-4 sm:px-6 md:px-10 py-4 sm:py-6`
- Desktop pill nav: `bg-white/70 backdrop-blur-md rounded-full pl-6 pr-1 py-1 shadow-sm border border-white/60`
- Hero heading: `pt-24 sm:pt-28 md:pt-32`, font sizes `text-[2rem] sm:text-4xl md:text-5xl lg:text-[4.75rem] xl:text-[5.25rem]`, `leading-[0.95]`, `letterSpacing: '-0.035em'`
- Bottom-left block: `absolute left-4 right-4 sm:right-auto sm:left-6 md:left-10 bottom-6 sm:bottom-8 md:bottom-10`
- Bottom-right video: `absolute right-6 md:right-10 bottom-8 md:bottom-10`

---

### Dependencies (package.json)

```json
{
  "dependencies": {
    "lucide-react": "^0.344.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.5.3",
    "vite": "^5.4.2"
  }
}
```
```

---

## 64. NexaCore Results

- **Category**: Features
- **Type**: features
- **Page Type**: hero
- **ID**: `nexacore-results`

```
Build a single React + TypeScript + Tailwind CSS v3 component called `PrecisionSection`. No external icon libraries — all icons are inline SVG or `<img>` tags. No `useState`, no animations, no hover states. Two separate layouts: a desktop staircase (absolutely-positioned pillars) and a mobile alternating-flow layout. The `sm:` breakpoint controls visibility between them.

---

## Global font

Register **"Mazzard H"** in `index.css` and apply it globally:

```css
@font-face {
  font-family: 'Mazzard H';
  font-weight: 400;
  font-style: normal;
  src: url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.woff2') format('woff2'),
       url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.woff') format('woff'),
       url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.ttf') format('truetype');
}
@font-face {
  font-family: 'Mazzard H';
  font-weight: 500;
  font-style: normal;
  src: url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.woff2') format('woff2'),
       url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.woff') format('woff'),
       url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.ttf') format('truetype');
}

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html, body, * { font-family: 'Mazzard H', sans-serif; }
}
```

---

## File: `src/components/PrecisionSection.tsx`

### Constants (top of file, before the component)

```ts
const LOGO_ICON =
  'https://cdn.prod.website-files.com/6720dd1ab6df0da205830ab1/6870f623cf3df417ce45df05_icon%20logo%20eternacloud.png';

const LINE_GRADIENT =
  'linear-gradient(rgb(28, 78, 255), rgb(254, 136, 27) 0%, rgb(172, 36, 255) 25%, rgb(247, 159, 255) 50%, rgb(255, 214, 0) 66%, rgb(254, 136, 27) 84%, rgba(254, 136, 27, 0) 102%)';

const PILLARS = [
  { label: 'Scopes',     items: ['conditions', 'capacity', 'specs', 'timelines'],     leftVw: 2.8,  bottomVw: 7     },
  { label: 'Integrates', items: ['civil', 'mechanical', 'electrical', 'controls'],     leftVw: 22.4, bottomVw: 9.08  },
  { label: 'Certifies',  items: ['redundancy', 'testing', 'compliance', 'sign-offs'], leftVw: 41.2, bottomVw: 11.16 },
  { label: 'Activates',  items: ['cutover', 'runbooks', 'handoff', 'SLAs'],           leftVw: 61.1, bottomVw: 13.24 },
];
```

---

### Section element

Inline styles only (no Tailwind on the `<section>` itself):

```
background-image: url("https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260418_125638_553b96dc-a1fd-4b2b-81a9-ed7daa80006e.png&w=1280&q=85")
background-size: cover
background-position: center
background-repeat: no-repeat
width: 100%
display: flex
flex-direction: column
align-items: center
text-align: center
padding: clamp(48px, 8vw, 120px) clamp(16px, 4vw, 60px) clamp(48px, 5.56vw, 80px)
gap: clamp(32px, 4vw, 56px)
```

---

### Block 1 — Header

Wrapper `<div>` — inline: `display: flex`, `flex-direction: column`, `align-items: center`, `gap: 36px`

#### Badge pill `<div>`

Inline:
```
background-color: rgb(249, 249, 249)
display: flex
align-items: center
gap: 8px
font-size: clamp(14px, 1.1vw, 18px)
font-weight: 500
border-radius: 36px
padding: clamp(8px, 0.9vw, 14px) clamp(12px, 1.25vw, 20px)
color: rgb(26, 11, 84)
white-space: nowrap
```

Contains this inline SVG (`width: 19`, `height: 18`, `flex-shrink: 0`, `viewBox="0 0 17 16"`, `fill="none"`):

```xml
<g clipPath="url(#prec-clip)">
  <circle cx="8.5" cy="8" r="7" stroke="#c86fff" fill="none" />
  <path d="M9.5 11.5V10.5H7.5V11.5H9.5ZM7.5 14.5C7.5 15.0523 7.94772 15.5 8.5 15.5C9.05228 15.5 9.5 15.0523 9.5 14.5H7.5ZM8.5 11.5H7.5V14.5H8.5H9.5V11.5H8.5Z" fill="rgb(200, 111, 255)" />
  <path d="M12 7H11V9H12V7ZM15 9C15.5523 9 16 8.55228 16 8C16 7.44772 15.5523 7 15 7V9ZM12 8V9H15V8V7L12 7V8Z" fill="rgb(200, 111, 255)" />
  <path d="M5 9H6V7H5V9ZM2 7C1.44772 7 1 7.44772 1 8C1 8.55228 1.44772 9 2 9V7ZM5 8V7H2V8V9H5V8Z" fill="rgb(200, 111, 255)" />
  <path d="M7.5 4.5V5.5H9.5V4.5H7.5ZM9.5 1.5C9.5 0.947715 9.05228 0.5 8.5 0.5C7.94772 0.5 7.5 0.947715 7.5 1.5H9.5ZM8.5 4.5H9.5V1.5H8.5H7.5V4.5H8.5Z" fill="rgb(200, 111, 255)" />
</g>
<defs>
  <clipPath id="prec-clip">
    <rect width="16" height="16" fill="white" transform="translate(0.5)" />
  </clipPath>
</defs>
```

After the SVG: plain text **"Structured Delivery"**

#### Heading + subtext `<div>`

Inline: `display: flex`, `flex-direction: column`, `align-items: center`, `max-width: clamp(700px, 60vw, 900px)`, `gap: 22px`

`<h2>` — inline: `font-size: clamp(28px, 4vw, 56px)`, `font-weight: 500`, `color: rgb(26, 11, 84)`, `line-height: 1.15`, `margin: 0`

Inside the `<h2>`, two `<span>` elements:

**Span 1** — Tailwind class `sm:whitespace-nowrap`, inline `display: block`:
> **One integrated, end-to-end system.**

**Span 2** — inline only:
```
background-image: linear-gradient(90deg, rgb(43, 167, 255), rgb(202, 69, 255) 50%, rgb(254, 136, 27))
-webkit-background-clip: text
background-clip: text
-webkit-text-fill-color: transparent
color: transparent
padding-bottom: 0.3vw
display: block
```
> **Compounding operational value.**

`<p>` below heading — inline: `font-size: clamp(15px, 1.2vw, 20px)`, `color: rgb(169, 151, 206)`, `margin: 0`
> **"NexaCore teams capture, align, validate and deliver exactly what keeps your programs on track."**

---

### Block 2 — Pillars container `<div>`

Inline: `width: 100%`, `max-width: 82.292vw`, `margin: 0 auto`

Contains two children:

---

#### Desktop pillars — `hidden sm:block` (Tailwind)

Inline:
```
position: relative
width: 82.292vw
height: 31.94vw
color: rgb(26, 11, 84)
```

Map over `PILLARS`. Each pillar wrapper `<div>`:
```
position: absolute
bottom: `${pillar.bottomVw}vw`
left: `${pillar.leftVw}vw`
display: flex
flex-direction: column
align-items: center
justify-content: flex-start
```

**Chip `<div>`:**
```
display: flex
align-items: center
justify-content: center
background-image: linear-gradient(135deg, rgb(255, 255, 255), rgba(255, 255, 255, 0.6))
font-size: 18px
font-weight: 500
border-radius: 20px
padding-top: 0.972vw
padding-bottom: 0.972vw
padding-left: 1.736vw
padding-right: 1.736vw
white-space: nowrap
gap: 8px
```

Chip contents:
1. `<img src={LOGO_ICON} alt="" style={{ width: '1.111vw', height: 'auto', display: 'inline-block' }} />`
2. `{pillar.label}`

**Line + items wrapper `<div>`** (directly below chip):
```
position: relative
display: flex
flex-direction: column
align-items: center
justify-content: flex-end
```

**Items container** (absolutely positioned, overlays the line):
```
position: absolute
top: 0.56vw
left: 1.94vw
display: flex
flex-direction: column
gap: 4px
font-size: 16px
align-items: flex-start
justify-content: space-between
```

Each item `<div>`:
```
padding-top: 0.69vw
padding-bottom: 0.69vw
padding-left: 1.04vw
padding-right: 1.04vw
display: flex
align-items: flex-start
```
Text: the item string.

**Vertical gradient line `<div>`** (sibling of items container, rendered after it):
```
background-image: LINE_GRADIENT  (see constant above)
width: 1px
height: 14.24vw
```

---

#### Mobile pillars — Tailwind: `flex flex-col sm:hidden w-full`

Inline: `color: rgb(26, 11, 84)`, `gap: 0`

Map over `PILLARS` with index. `isRight = index % 2 !== 0` (index 1 and 3 are right-aligned).

**Pillar wrapper `<div>`:**
```
display: flex
flex-direction: column
align-items: isRight ? 'flex-end' : 'flex-start'
width: 100%
padding-bottom: 8px
```

**Chip `<div>`:**
```
display: inline-flex
align-items: center
background-image: linear-gradient(135deg, rgb(255, 255, 255), rgba(255, 255, 255, 0.6))
font-size: 15px
font-weight: 500
border-radius: 20px
padding: 10px 18px
white-space: nowrap
gap: 7px
```

Chip contents:
1. `<img src={LOGO_ICON} alt="" style={{ width: 16, height: 'auto' }} />`
2. `{pillar.label}`

**Line + items row `<div>`:**
```
display: flex
flex-direction: isRight ? 'row-reverse' : 'row'
align-items: stretch
width: 100%
```

**Vertical line `<div>`:**
```
width: 1px
flex-shrink: 0
background-image: LINE_GRADIENT
margin-left: isRight ? 0 : 22px
margin-right: isRight ? 22px : 0
min-height: 120px
```

**Items `<div>`:**
```
display: flex
flex-direction: column
gap: 0
padding-left: isRight ? 0 : 20px
padding-right: isRight ? 20px : 0
padding-top: 8px
padding-bottom: 8px
align-items: isRight ? 'flex-end' : 'flex-start'
```

Each item `<div>`:
```
font-size: 14px
color: rgb(100, 80, 160)
padding: 8px 0
```
Text: the item string.

---

## Pillar data reference

| Label | Items | Desktop left | Desktop bottom |
|---|---|---|---|
| Scopes | conditions, capacity, specs, timelines | 2.8vw | 7vw |
| Integrates | civil, mechanical, electrical, controls | 22.4vw | 9.08vw |
| Certifies | redundancy, testing, compliance, sign-offs | 41.2vw | 11.16vw |
| Activates | cutover, runbooks, handoff, SLAs | 61.1vw | 13.24vw |

---

**No animations. No hover states. No scroll effects. No JavaScript logic. Static render only. Desktop: 4 pillars arranged in a rising staircase via `position: absolute` with `bottom` and `left` in `vw` units. Mobile: single column, even-indexed pillars align left, odd-indexed align right, each with a vertical gradient line beside its items list.**
```

---

## 65. Tech-Forward

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `tech-forward`

```
Create a full-screen hero section landing page using React, Vite, and Framer Motion (`motion` package). Use plain CSS (no Tailwind). The font is Inter (weights 300, 400, 500, 600) from Google Fonts. The design is minimal black-and-white with a full-viewport background video.

**Stack:** React 19, Vite, `motion` (framer-motion), `lucide-react` (for the Plus icon).

**Layout:**
- Full viewport height (`min-height: 100vh`), white background, flex column with `justify-content: space-between`
- Fixed navbar at top (z-index 50, pointer-events none on the nav itself, auto on children)
- Absolutely positioned full-screen video behind everything (z-index 0)
- Footer content pinned to bottom (z-index 30) with a white gradient fade-up background

**Navbar (fixed, top):**
- Left side contains:
  1. Logo: custom SVG icon (two rotated rounded rectangles at -35deg, black fill) + brand text "NeuralKinetics" (hidden on mobile, shown on desktop 768px+)
  2. Menu button: black pill with white circle containing a Plus icon (lucide, size 12, strokeWidth 3) + "Menu" text (11px, white)
  3. Tags pill: light gray (#F4F4F6) rounded-full container with two text labels "Advanced Bionics" and "Cognitive AI" (hidden on mobile, shown on desktop)
- Right side contains:
  - A light gray pill with a black circle button (containing a 4-dot grid SVG icon) + label "Adaptive Systems" (hidden on mobile)

**Background Video:**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_215831_c6a8989c-d716-4d8d-8745-e972a2eec711.mp4`
- autoPlay, muted, playsInline, object-fit: cover
- On mobile: video wrapper is 80% width and 80% height (centered)
- On desktop (768px+): video wrapper is 100% width and 100% height

**Footer content (bottom, over gradient):**
- Background: `linear-gradient(to top, #ffffff 0%, rgba(255,255,255,0.8) 50%, transparent 100%)`
- On mobile: stacks vertically. On desktop: row layout, items aligned to bottom.
- Left block:
  1. Subtitle line: small black dot (8px circle) + "Best digital banking card 2026" (13px, 55% opacity black)
  2. Heading: "One Card, Zero / Limits. Worldwide." on two lines. Font-weight 300, clamp(2rem, 8vw, 4.5rem) on mobile, clamp(2.5rem, 5.5vw, 4.5rem) on desktop, letter-spacing -0.03em, line-height 1
  3. Two buttons: "See Features" (black pill, white text, 13px) and "How It Works" (transparent with dark border rgba(0,0,0,0.35), 13px)
- Right block: Three tag pills "Neuromorphic", "AGI", "Cybernetics" (white bg, light border rgba(0,0,0,0.12), 11px, rounded-full)

**Animations (using `motion` from 'motion/react'):**
- Navbar: slides down from y:-16, opacity 0 to visible. Duration 0.8s, ease [0.16, 1, 0.3, 1]
- Video: fades in from opacity 0 + scale 1.05 to opacity 1 + scale 1. Duration 1.8s
- Footer wrapper: slides up from y:20, delay 0.5s, duration 1s
- Subtitle: slides up from y:16, delay 0.6s, duration 0.8s
- Heading: slides up from y:20, delay 0.8s, duration 0.8s
- Buttons: slides up from y:16, delay 1.0s, duration 0.8s
- All use ease: [0.16, 1, 0.3, 1]

**Responsive (mobile-first, breakpoint at 768px):**
- Mobile: navbar padding 16px, smaller buttons (28px circles), brand text hidden, tags hidden, right label hidden, footer stacks vertically, video at 80% size
- Desktop (768px+): navbar padding 24px 32px, larger buttons (32px circles), all text/tags visible, footer is row layout, video fills 100%
```

---

## 66. Organic Odyssey

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `organic-odyssey`

```
Create a full-screen cinematic hero section using React, Tailwind CSS, and Framer Motion. Use Vite with TypeScript. The dependencies required are: `react`, `react-dom`, `framer-motion`, `lucide-react`, and `tailwindcss`.

**VIDEO BACKGROUND:**
- Full-screen looping background video, absolutely positioned to fill the viewport
- Video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260619_191346_9d19d66e-86a4-47f7-8dc6-712c1788c3b2.mp4`
- Properties: autoPlay, muted, loop, playsInline, object-cover, object-center
- Page background: `#010101`, full viewport height, overflow hidden

**FONTS (load via index.html link tags):**
- Garamond from: `https://db.onlinewebfonts.com/c/2bf40ab72ea4897a3fd9b6e48b233a19?family=Garamond`
- Geist from Google Fonts: weights 300, 400, 500
- Body font: `'Geist', -apple-system, BlinkMacSystemFont, sans-serif`
- Heading font class `.font-garamond`: `'Garamond', 'Times New Roman', serif`

**NAVIGATION:**
- Relative positioned, z-20, flexbox centered on desktop, space-between on mobile
- Brand name "Organic Visions" -- white, uppercase, letter-spacing 0.25em (mobile) / 0.3em (desktop), font-light
- Desktop nav links: "Wander", "Archive", "Story", "Connect" -- white/80, uppercase, 0.2em tracking, hover to white, 300ms transition
- Mobile: hamburger toggle using lucide-react `Menu` and `X` icons (size 22)

**MOBILE MENU (hamburger dropdown):**
- Fixed position, top-16, left-4, right-4, z-50, hidden on md+
- Uses `AnimatePresence` from framer-motion for mount/unmount animation
- Animation: fade in from y:-10 to y:0, duration 0.3s, ease 'easeOut'; reverse on exit
- Each link staggers in with opacity 0 to 1, y:-8 to 0, delay 0.05 + index*0.06
- Links: white/90, 0.25em tracking, uppercase, font-light, hover to white
- Custom glass class `.mobile-menu-glass`:
  ```css
  background: rgba(10, 10, 10, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  ```
- Rounded-2xl, py-8, gap-5, flex-col centered

**HERO CONTENT:**
- Relative z-10, flex-col centered, text-center
- Padding: px-5 (sm:px-8), pt-12 (sm:pt-16, md:pt-24)
- Heading: Two lines -- "WITNESS THE" and "HIDDEN REALM"
- Font: Garamond, sizes 4xl/6xl/8xl/9xl responsive, font-normal, white, line-height 1.08, tracking-tight, mb-6 (sm:mb-8)
- Each line uses a `StaggeredFade` component that splits text into individual characters and animates each with 0.07s stagger delay (opacity 0 to 1), triggered once when in view

**STAGGERED FADE COMPONENT:**
- Accepts `text` string prop
- Splits into individual `<motion.span>` characters
- Uses `useInView` hook (once: true) to trigger animation
- Variants: hidden = opacity 0; show = opacity 1, y:0, with delay `i * 0.07` per character

**SUBTITLE:**
- Framer Motion animated paragraph, initial opacity:0 y:20, animate opacity:1 y:0, duration 0.8s, delay 1.6s
- Text: "An odyssey through delicate living forms," (line break hidden on mobile, visible sm+) "revealed by lens and curiosity."
- White/70, font-light, leading-relaxed, max-w-xs (sm:max-w-md), mb-8 (sm:mb-10)
- Responsive sizes: text-sm / text-base / text-lg

**CTA BUTTON:**
- Framer Motion animated, initial opacity:0 y:20, animate opacity:1 y:0, duration 0.8s, delay 2.0s
- Text: "Begin the Experience"
- Uses `.liquid-glass` class, rounded-full, responsive padding px-7/px-10 py-3.5/py-4
- White/90, uppercase, tracking 0.18em/0.2em responsive

**LIQUID GLASS CSS (.liquid-glass):**
```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.liquid-glass:hover {
  background: rgba(255, 255, 255, 0.04);
  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.15);
}

.liquid-glass:active {
  transform: scale(0.98);
}
```

**GLOBAL CSS:**
- Reset: margin 0, padding 0, box-sizing border-box on all elements
- Body: antialiased font smoothing, white text, #010101 background
- Uses Tailwind directives: @tailwind base/components/utilities

**PAGE TITLE:** "Synthetic Nature"
```

---

## 67. Portfolio About

- **Category**: About
- **Type**: about
- **Page Type**: hero
- **ID**: `portfolio-about`

```
**Prompt:**

Create an "About Me" section using React, Tailwind CSS, and **framer-motion**. The site uses **Google Font "Kanit"** (weights 300-900) and a dark background `#0C0C0C`.

**Section layout:**
- Full-width section, `min-h-screen`, flexbox column, centered both axes
- Padding: `px-5 sm:px-8 md:px-10 py-20`
- Background: `#0C0C0C` (inherited from page)
- `position: relative` -- the section has 4 decorative floating images placed absolutely in the corners

**4 decorative corner images (absolute positioned, z-0):**

1. **Top-left** -- Moon icon
   - URL: `https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/moon_icon.11395d36.png`
   - Position: `top-[4%] left-[1%] sm:left-[2%] md:left-[4%]`
   - Size: `w-[120px] sm:w-[160px] md:w-[210px] h-auto`
   - Fade-in animation: `delay: 0.1`, slides from left (`x: -80, y: 0`), `duration: 0.9`

2. **Bottom-left** -- 3D object
   - URL: `https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/p59_1.4659672e.png`
   - Position: `bottom-[8%] left-[3%] sm:left-[6%] md:left-[10%]`
   - Size: `w-[100px] sm:w-[140px] md:w-[180px] h-auto`
   - Fade-in animation: `delay: 0.25`, slides from left (`x: -80, y: 0`), `duration: 0.9`

3. **Top-right** -- Lego icon
   - URL: `https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/lego_icon-1.703bb594.png`
   - Position: `top-[4%] right-[1%] sm:right-[2%] md:right-[4%]`
   - Size: `w-[120px] sm:w-[160px] md:w-[210px] h-auto`
   - Fade-in animation: `delay: 0.15`, slides from right (`x: 80, y: 0`), `duration: 0.9`

4. **Bottom-right** -- 3D group
   - URL: `https://shrug-person-78902957.figma.site/_components/v2/ebb2b8f25d8e24d5f0a5ca8af4c950de81aa2fd7/Group_134-1.2e04f3ce.png`
   - Position: `bottom-[8%] right-[3%] sm:right-[6%] md:right-[10%]`
   - Size: `w-[130px] sm:w-[170px] md:w-[220px] h-auto`
   - Fade-in animation: `delay: 0.3`, slides from right (`x: 80, y: 0`), `duration: 0.9`

**Center content (relative z-10, max-w-4xl, centered):**

Vertical layout with `gap-16 sm:gap-20 md:gap-24`, containing two groups:

**Group 1 -- Heading + Animated Text** (gap `10 sm:14 md:16`):

- **Heading "About me":**
  - `font-black uppercase leading-none tracking-tight text-center`
  - Font size: `clamp(3rem, 12vw, 160px)`
  - Uses a CSS class `hero-heading` which applies a gradient text fill:
    ```css
    .hero-heading {
      background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    ```
  - Fade-in: `delay: 0, y: 40`

- **Animated paragraph** (scroll-driven character-by-character reveal):
  - Text content: `"With more than five years of experience in design, i focus on branding, web design, and user experience, i truly enjoy working with businesses that aim to stand out and present their best image. Let's build something incredible together!"`
  - Styling: `text-[#D7E2EA] font-medium text-center leading-relaxed max-w-[560px]`
  - Font size: `clamp(1rem, 2vw, 1.35rem)`
  - **Animation behavior** (uses framer-motion `useScroll` + `useTransform`):
    - Each character is rendered as an individual `<span>` with `position: relative; display: inline-block`
    - An invisible duplicate holds the space; the visible character is absolutely positioned on top
    - Scroll tracking: `useScroll({ target: containerRef, offset: ['start 0.8', 'end 0.2'] })`
    - Per-character opacity: calculate `charProgress = index / totalChars`, then `start = max(0, charProgress - 0.1)` and `end = min(1, charProgress + 0.05)`. Map `scrollYProgress` from `[start, end]` to opacity `[0.2, 1]`
    - Spaces are rendered as `\u00A0` (non-breaking space)
    - Characters start dim (opacity 0.2) and brighten to full opacity (1) as the user scrolls through the section, creating a progressive text reveal from left to right

**Group 2 -- Contact Button:**
- Fade-in: `delay: 0.3, y: 20`
- Pill-shaped button (rounded-full), text "Contact Me"
- Responsive padding: `px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4`
- Text: `text-white font-medium uppercase tracking-widest`, size `text-xs sm:text-sm md:text-base`
- Background gradient: `linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%)`
- Box shadow: `0px 4px 4px rgba(181, 1, 167, 0.25), 4px 4px 12px #7721B1 inset`
- Outline: `2px solid #E3E3E3` with `outlineOffset: -3px`
- Hover: `opacity: 0.9`, Active: `opacity: 0.75`, transition 200ms
- Links to `#contact`

**FadeIn component (reusable, framer-motion):**
- Props: `delay`, `duration` (default 0.7), `x` (default 0), `y` (default 30), `className`, `style`, `as` (HTML element tag, default `div`)
- Uses `motion.create()` to make any HTML element animatable
- Variants: `hidden` state sets `opacity: 0` + the x/y offsets; `visible` animates to `opacity: 1, x: 0, y: 0`
- Easing: cubic bezier `[0.25, 0.1, 0.25, 1]`
- Viewport trigger: `{ once: true, margin: "50px", amount: 0 }`

**Font (loaded in HTML head):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
```

CSS base: `font-family: 'Kanit', sans-serif` on html/body.

---
```

---

## 68. NexaCore Control

- **Category**: Features
- **Type**: features
- **Page Type**: hero
- **ID**: `nexacore-control`

```
Build a single React + TypeScript + Tailwind CSS v3 component called `FreedomSection`. It uses `hls.js` for HLS video streaming and `useEffect` / `useRef` from React. No external icon libraries — all icons are inline SVG or `<img>` tags. Fully mobile-responsive. No hover states.

---

## Global font

Register **"Mazzard H"** in `index.css` and apply it globally:

```css
@font-face {
  font-family: 'Mazzard H';
  font-weight: 400;
  font-style: normal;
  src: url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.woff2') format('woff2'),
       url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.woff') format('woff'),
       url('https://db.onlinewebfonts.com/t/eb5b5ee332420add9a40ee988cb6ac37.ttf') format('truetype');
}
@font-face {
  font-family: 'Mazzard H';
  font-weight: 500;
  font-style: normal;
  src: url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.woff2') format('woff2'),
       url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.woff') format('woff'),
       url('https://db.onlinewebfonts.com/t/875fffdfa62169a0f131e90f37f1faf4.ttf') format('truetype');
}

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html, body, * { font-family: 'Mazzard H', sans-serif; }
}
```

---

## Dependencies

`hls.js` must be installed: `npm install hls.js`. It is imported as `import Hls from 'hls.js'`.

---

## File: `src/components/FreedomSection.tsx`

### Constants (top of file)

```ts
const HLS_SRC = 'https://stream.mux.com/bnYL6x5cAX6WiJv2pOKpITehZd3NVdXpj3ylJFpX5Lk.m3u8';

const CROSS_ICON = 'https://cdn.prod.website-files.com/6720dd1ab6df0da205830ab1/686cc0f520a992816d8b15dc_bullet-list-cross.svg';
const CHECK_ICON = 'https://cdn.prod.website-files.com/6720dd1ab6df0da205830ab1/686cc068490683bbb3377d04_bullet-list.svg';

const negatives = [
  'Reactive firefighting when foundational issues surface too late',
  'Bloated coordination overhead drains bandwidth from core teams',
  "Constant re-verification because source data can't be trusted",
  'Fragmented vendor relations produce mismatched deliverables',
  'Scattered specs and decisions buried across siloed systems',
];

const positives = [
  'Layered dependency maps eliminate costly surprises at every phase',
  'Streamlined team handoffs deliver production-ready outcomes fast',
  'Live validation loops keep requirements locked across all stages',
  'Unified vendor management through a single accountable contact',
  'Centralized context and clear records accelerate every decision',
];
```

---

### `HlsVideo` sub-component (defined above `FreedomSection`, not exported)

```ts
function HlsVideo() {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (Hls.isSupported()) {
      const hls = new Hls({
        startLevel: -1,
        capLevelToPlayerSize: false,
        maxMaxBufferLength: 60,
        enableWorker: true,
      });
      hls.loadSource(HLS_SRC);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        hls.currentLevel = hls.levels.length - 1;
        video.play().catch(() => {});
      });
      return () => hls.destroy();
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = HLS_SRC;
      video.play().catch(() => {});
    }
  }, []);

  return (
    <video
      ref={videoRef}
      autoPlay
      loop
      muted
      playsInline
      style={{
        width: '160%',
        height: '160%',
        objectFit: 'cover',
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      }}
    />
  );
}
```

The video is zoomed to `160% x 160%` and centered with `translate(-50%, -50%)` inside a circular clipping container, so it fills the circle with no letterboxing.

---

### `FreedomSection` component

**`<section>`** — Tailwind: `w-full flex flex-col items-center`

Inline:
```
background-color: #ffffff
padding: clamp(48px, 6vw, 80px) clamp(16px, 3vw, 40px)
gap: 36px
```

---

#### Block 1 — Header

Tailwind: `flex flex-col items-center gap-9 text-center`

**Badge pill:**

Tailwind: `flex items-center gap-2 text-lg font-medium rounded-full`

Inline: `background-color: rgb(249, 249, 249)`, `padding: 0.9vw 1.25vw`, `color: rgb(26, 11, 84)`

Contains this inline SVG (`width: 19px`, `height: 18px`, `flex-shrink: 0`, `viewBox="0 0 17 16"`, `fill="none"`, `xmlns="http://www.w3.org/2000/svg"`):

```xml
<g clipPath="url(#freedom-clip)">
  <path
    fillRule="evenodd"
    clipRule="evenodd"
    d="M8.50037 3.66955C7.53221 2.82462 6.41758 2.275 5.333 2.07887C4.11096 1.85888 2.84987 2.0826 1.96658 2.95885C1.10056 3.81944 0.866218 5.04172 1.06751 6.23193C1.24778 7.29835 1.7803 8.39907 2.60501 9.35959C2.41536 10.1071 2.46371 10.8946 2.7434 11.6137C3.02308 12.3327 3.52035 12.9481 4.16678 13.375C4.81321 13.802 5.57702 14.0195 6.35308 13.9976C7.12915 13.9758 7.87933 13.7157 8.50037 13.2531C9.12146 13.7161 9.87183 13.9765 10.6482 13.9985C11.4245 14.0205 12.1886 13.8029 12.8352 13.3758C13.4819 12.9487 13.9792 12.3331 14.2588 11.6137C14.5384 10.8943 14.5865 10.1065 14.3965 9.35884C15.2204 8.39832 15.753 7.29835 15.9325 6.23119C16.1338 5.04098 15.8994 3.81944 15.0334 2.9596C14.1501 2.0826 12.889 1.85888 11.667 2.07962C10.5824 2.275 9.46854 2.82537 8.50037 3.66955Z"
    fill="rgb(200, 111, 255)"
  />
</g>
<defs>
  <clipPath id="freedom-clip">
    <rect width="16" height="16" fill="white" transform="translate(0.5)" />
  </clipPath>
</defs>
```

After the SVG: plain text **"Control"**

**`<h2>`** — Tailwind: `font-medium`

Inline: `font-size: clamp(32px, 4vw, 56px)`, `color: rgb(26, 11, 84)`, `line-height: 1.15`, `margin: 0`

Structure:
```
Stop absorbing the chaos.<br />
<span gradient>Run with confidence.</span>
```

Gradient `<span>` inline styles:
```
background-image: linear-gradient(90deg, rgb(43,167,255), rgb(202,69,255) 50%, rgb(254,136,27))
-webkit-background-clip: text
background-clip: text
-webkit-text-fill-color: transparent
color: transparent
padding-bottom: 0.3vw
display: inline-block
```

---

#### Block 2 — Three-column grid

Tailwind: `w-full flex flex-col lg:grid`

Inline:
```
grid-template-columns: 26vw 1fr 26vw
column-gap: 36px
row-gap: 24px
align-items: start
padding: 0 clamp(0px, 2.92vw, 40px)
gap: 24px
```

On mobile (`flex flex-col`): stacks vertically. On `lg:` and above: renders as 3-column grid with `gridTemplateColumns: '26vw 1fr 26vw'`.

---

##### Left column — Negatives

Tailwind: `flex flex-col`

Inline: `gap: 12px`, `font-size: clamp(13px, 1.15vw, 17px)`, `color: rgb(131, 121, 158)`

Map over `negatives`. Each card `<div>` — Tailwind: `flex flex-col`

Inline:
```
gap: 12px
padding: clamp(12px, 0.97vw, 16px) clamp(14px, 1.25vw, 20px)
border-radius: 18px
background-color: rgb(255, 255, 255)
box-shadow: 0 3px 9.1px #3f4a7e0d, 0 1px 29px #3f4a7e1a
```

Contents:
1. `<img src={CROSS_ICON} alt="" aria-hidden style={{ width: 'clamp(16px, 1.25vw, 20px)', flexShrink: 0 }} />`
2. `<div>{text}</div>` — inherits parent `color: rgb(131, 121, 158)`

---

##### Center column — Video circle

Tailwind: `flex items-center justify-center order-first lg:order-none`

Inline: `align-self: center`

On mobile, `order-first` places the video above both card columns. On `lg:`, `lg:order-none` restores it to the middle.

Inside, a circular container:
```
position: relative
border-radius: 50%
overflow: hidden
width: clamp(200px, 22vw, 400px)
height: clamp(200px, 22vw, 400px)
flex-shrink: 0
```

Inside the circle: `<HlsVideo />` (described above — the `<video>` is absolutely positioned at 160% size, centered with translate -50% -50%).

---

##### Right column — Positives

Tailwind: `flex flex-col`

Inline: `gap: 12px`, `font-size: clamp(13px, 1.15vw, 17px)`

Map over `positives`. Each card `<div>` — Tailwind: `flex flex-col`

Inline: (same shadow/padding/border-radius as negatives)
```
gap: 12px
padding: clamp(12px, 0.97vw, 16px) clamp(14px, 1.25vw, 20px)
border-radius: 18px
background-color: rgb(255, 255, 255)
box-shadow: 0 3px 9.1px #3f4a7e0d, 0 1px 29px #3f4a7e1a
```

Contents:
1. `<img src={CHECK_ICON} alt="" aria-hidden style={{ width: 'clamp(16px, 1.25vw, 20px)', flexShrink: 0 }} />`
2. `<div style={{ color: 'rgb(26, 11, 84)' }}>{text}</div>`

---

## Layout summary

- **Mobile**: flex-col — video first (order-first), then left negatives, then right positives stacked vertically
- **Desktop (lg+)**: CSS grid — left negatives | center video circle | right positives
- Section background is pure white `#ffffff`
- No animations, no hover states, no scroll effects

```

---

## 69. Wellness Balance

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `wellness-balance`

```
Create a single-page hero landing for a wellness/supplements brand called "TerraElix" using React + Tailwind CSS + Lucide React icons. The page is a full-viewport hero with a background image, navbar, headline with word-by-word reveal animations, CTA section, and a 3-panel footer strip. It must be fully responsive (mobile, tablet, desktop).

---

## Fonts

Import from Google Fonts:
- **DM Sans** (weights 400, 500) -- used for brand name, nav links, headline, panel 1 text
- **Inter** (weights 400, 500) -- used for buttons, body text, panel 2/3 text

---

## Background

Full-screen background image covering the entire viewport:
```
url: https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_110248_b62f758d-f68c-4045-a7b4-91771d6d0a0f.png&w=1280&q=85
background-size: cover; background-position: center; background-repeat: no-repeat;
```

---

## Layout Structure

```
<div> (min-h-screen, flex flex-col, relative, overflow-hidden)
  <nav> -- navbar
  <section> -- hero content (flex-1, flex col, justify-center)
  <div> -- mobile/tablet product image (visible below lg)
  <div> -- 3-panel grid footer
  <img> -- desktop floating product image (absolute, hidden below lg)
</div>
```

---

## Navbar

- **Left:** Brand name "TerraElix" -- white, DM Sans 500, 30px, letter-spacing -0.05em
- **Center (desktop only, hidden on mobile):** Nav links "About", "Products", "Promotions", "Contact" -- DM Sans 500, 18px, text-white/90, gap 10 (lg)
- **Right:** Row of icon buttons + avatar + mobile menu toggle
  - Search icon (Lucide `Search`, size 20, strokeWidth 1.5)
  - Shopping bag icon (Lucide `ShoppingBag`, size 20, strokeWidth 1.5)
  - Return icon (Lucide `CornerUpLeft`, size 20, strokeWidth 1.5)
  - Round avatar image (w-8 h-8, lg:w-10 lg:h-10, rounded-full, object-cover):
    ```
    https://polo-pecan-73837341.figma.site/_assets/v11/ca8093996e970200cbcf8bde8744175e52da5a79.png
    ```
  - Hamburger menu button (md:hidden, Lucide `Menu` / `X` toggle)

- **Mobile overlay menu:** fixed inset-0 bg-black/90 z-30 with centered nav links (text-2xl, white)

Padding: px-5 sm:px-8 lg:px-10, py-4 lg:py-5

---

## Hero Headline

Font: DM Sans, weight 400, letter-spacing -0.05em

Responsive sizes:
- Base: 48px/50px line-height
- sm: 80px/72px
- md: 110px/95px
- lg: 130px/110px
- xl: 155px/125px

Text layout (3 lines):
```
Line 1: "The" (white) "Power" (white) "of" (white/45 -- dimmed)
Line 2: "Nature" (dimmed) "in" (dimmed) "Every" (white)
Line 3: "Capsule" (white) + inline image
```

Each word is wrapped in a container with overflow-hidden, and the inner span animates with `wordReveal` (translateY 100% + blur to visible). Staggered delays: 0.3s, 0.4s, 0.5s, 0.6s, 0.7s, 0.8s, 0.9s.

**Inline image** after "Capsule" (hidden on mobile, sm:inline-block, align-middle, ml-2 lg:ml-4):
```
https://polo-pecan-73837341.figma.site/_assets/v11/6a7de4fbe9c9e2315040607320a9ff5e93117bf4.png
height: clamp(60px, 10vw, 160px); width: auto;
```

---

## CTA Section

Below the headline, mt-8 sm:mt-12 lg:mt-[75px]. Flex row on sm+, column on mobile. Gap: 5 (mobile), 8 (sm), 50px (lg).

- **Button:** "Explore Now" + ArrowUpRight icon. bg-black text-white rounded-md. Sizes: w-full sm:w-[240px] md:w-[280px] lg:w-[310px], h-14 sm:h-16 lg:h-[72px]. Font: Inter 500, responsive text (base to 2xl), letter-spacing -0.03em.
- **Paragraph:** "Discover our new plant-based supplements for daily balance and clean energy." -- white, max-w-[310px], Inter 400, text-sm sm:text-base lg:text-lg, line-height 1.45, letter-spacing -0.03em.

---

## Mobile/Tablet Product Image (lg:hidden)

Visible below lg breakpoint. Oversized, bleeding off edges:
```
https://polo-pecan-73837341.figma.site/_assets/v11/50ad042b3cd48a2e120ea3ba17c8cfeaf3cc334c.png
w-[180%] sm:w-[151%] max-w-[1296px], object-contain, mx-auto, drop-shadow-2xl
margin-bottom: -180px sm:-220px (overlaps panels below)
```

---

## Bottom 3-Panel Grid

`grid grid-cols-1 md:grid-cols-[2fr_1fr_2fr]`, relative z-10.

### Panel 1 (bg-[#ECEDEC])
- Text: "Start your personalized path to natural balance" -- DM Sans 400, text-2xl sm:text-[28px] lg:text-[35px], leading-[1.1], letter-spacing -0.05em, max-w-[350px]
- Link: "Personal Assessment" -- underline, Inter 400, text-base lg:text-lg, letter-spacing -0.03em
- Decorative image (absolute right-0 bottom-0, h-full, mix-blend-multiply):
  ```
  https://polo-pecan-73837341.figma.site/_assets/v11/6736cbe6e26afa2cd7c04a91892a79f7640785b5.png
  ```

### Panel 2 (bg-[#FEFDF9]) -- Auto-rotating card carousel
4 cards cycling every 3500ms with fade/slide transition:
1. FlaskConical icon, bg-black circle: "Experience our newly enhanced natural formula"
2. Leaf icon, bg-emerald-800 circle: "Pure organic ingredients sourced sustainably"
3. Droplets icon, bg-cyan-800 circle: "Advanced bioavailability for maximum absorption"
4. Sun icon, bg-amber-700 circle: "Clinically tested for daily energy & vitality"

Each card: icon in a 40px (sm:48px) round colored circle + text (Inter 400, text-sm sm:text-base lg:text-lg, text-black/80, line-height 1.2, letter-spacing -0.03em).

Active card: opacity-100 translate-y-0. Inactive: opacity-0 translate-y-4 absolute.

Bottom dots: 4 thin bars (h-0.5, flex-1, rounded-full). Active: bg-black. Inactive: bg-black/20.

### Panel 3 (bg-black)
- Left: Product image (w-[120px] h-[82px] sm:w-[160px] h-[110px] lg:w-[208px] h-[142px]):
  ```
  https://polo-pecan-73837341.figma.site/_assets/v11/30e8f38d1f993c357a3be2721557fc899d5640fc.png
  ```
- Right: "+14K" (white, Inter 400, text-2xl sm:text-3xl lg:text-[35px], letter-spacing -0.05em) + "People have already optimized their wellness" (text-white/60, Inter 400, text-sm sm:text-base lg:text-lg, line-height 1.2)

---

## Desktop Floating Product (lg+ only)

Same image as mobile product, but absolutely positioned for desktop:
```
https://polo-pecan-73837341.figma.site/_assets/v11/50ad042b3cd48a2e120ea3ba17c8cfeaf3cc334c.png
position: absolute; z-0; hidden lg:block;
width: clamp(600px, 80vw, 1412px); height: auto;
bottom: -10%; right: clamp(-400px, -20vw, -100px);
```

---

## Animations (CSS keyframes)

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes wordReveal {
  from { opacity: 0; transform: translateY(100%); filter: blur(4px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0px); }
}
```

All use `cubic-bezier(0.16, 1, 0.3, 1)` easing with `both` fill mode.

**Classes and their animations:**
- `.animate-fade-up` -- fadeUp 0.8s
- `.animate-fade-in` -- fadeIn 0.7s
- `.animate-slide-left` -- slideInLeft 0.8s
- `.animate-slide-right` -- slideInRight 0.8s
- `.animate-scale-in` -- scaleIn 1s
- `.animate-word-reveal > span` -- wordReveal 0.7s

**Delay classes:** .delay-200 through .delay-1100 (increments of 0.1s)

**Animation assignments:**
- Navbar container: animate-fade-in
- Brand name: animate-slide-left delay-200
- Nav links: animate-fade-in delay-400
- Right icons: animate-slide-right delay-300
- CTA row: animate-fade-up delay-600
- Desktop product image: animate-scale-in delay-700
- Mobile product image: animate-scale-in delay-800
- Panel 1: animate-fade-up delay-900
- Panel 2: animate-fade-up delay-1000
- Panel 3: animate-fade-up delay-1100
- Inline capsule image: animate-scale-in delay-1000
```

---

## 70. Email Landing Page

- **Category**: Landing page
- **Type**: landing
- **Page Type**: landing
- **ID**: `email-landing-page`

```
Build a premium, AI-native email client landing page called "Aura" using **React 18 + TypeScript + Vite + Tailwind CSS + motion/react (framer motion) + lucide-react**. The aesthetic is dark (bg `#0c0c0c`), cinematic, glassy, with a looping fullscreen background video, a shiny gradient headline, a macOS-style menu bar, a realistic inbox mockup, and a custom "liquid-glass" card treatment.

## Stack / setup

- `package.json` dependencies: `react`, `react-dom`, `@supabase/supabase-js`, `motion` (v12+, import from `motion/react`), `lucide-react`.
- Tailwind config extends colors with `brand: '#3D81E3'` and fontFamily sans with `['Inter','system-ui','sans-serif']`.
- Font: Google Fonts Inter weights 400, 500, 600, 700, 800, 900. Import in `index.css` via `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');`.
- `html,body { font-family: 'Inter', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }`.
- Background color base `#0c0c0c`, text white, selection `bg-brand/30`.

## Global background video (fixed, behind everything)

Inside the root wrapper (`relative min-h-screen overflow-x-hidden bg-[#0c0c0c] text-white`), render a fixed full-screen video:

```
<div className="fixed inset-0 z-0 pointer-events-none">
  <video autoPlay loop muted playsInline
    className="w-full h-full object-cover pointer-events-none"
    src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_064122_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4" />
</div>
```

Also render two hidden-on-mobile fixed vertical guide lines at the 36rem container edges:
```
<div className="hidden md:block pointer-events-none fixed inset-y-0 left-1/2 -translate-x-[calc(50%+36rem)] w-px bg-white/10 z-[5]" />
<div className="hidden md:block pointer-events-none fixed inset-y-0 left-1/2 translate-x-[calc(-50%+36rem)] w-px bg-white/10 z-[5]" />
```

## Global SVG noise filters (two, both id `c3-noise`)

- One at root level (subtle grain, multiply blend) for the shiny headline.
- One inside the pricing section (fractal noise, overlay blend) for the watermark.

Root filter:
```
<filter id="c3-noise">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" />
  <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.35 0" />
  <feComposite in2="SourceGraphic" operator="in" result="noise" />
  <feBlend in="SourceGraphic" in2="noise" mode="multiply" />
</filter>
```

Pricing filter:
```
<filter id="c3-noise">
  <feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="2" stitchTiles="stitch" />
  <feComponentTransfer><feFuncA type="linear" slope="0.075" /></feComponentTransfer>
  <feComposite in2="SourceGraphic" operator="in" result="noise" />
  <feBlend in="SourceGraphic" in2="noise" mode="overlay" />
</filter>
```

## Shared primitives

**AppleLogo** — inline SVG Apple mark, `viewBox="0 0 384 512"`, `fill="currentColor"`, default `w-4 h-4`. Path:
`M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z`.

**LogoMark** — abstract 4-quadrant curve mark, `viewBox="0 0 256 256"`, default `w-8 h-8`, white fill. Path:
`M 0 128 C 70.692 128 128 185.308 128 256 L 64 256 C 64 220.654 35.346 192 0 192 Z M 256 192 C 220.654 192 192 220.654 192 256 L 128 256 C 128 185.308 185.308 128 256 128 Z M 128 0 C 128 70.692 70.692 128 0 128 L 0 64 C 35.346 64 64 35.346 64 0 Z M 192 0 C 192 35.346 220.654 64 256 64 L 256 128 C 185.308 128 128 70.692 128 0 Z`.

**AppleButton** — rounded-full white pill, Apple logo + "Download Aura" label + ChevronRight. Chevron translates `+1px` on group hover. Classes: `group inline-flex items-center justify-center gap-2 rounded-full bg-white text-black font-medium text-sm px-5 py-3 transition-all hover:bg-white/90 active:scale-[0.98]`. Accepts `label` and `full` props.

**SectionEyebrow** — `<span className="w-1.5 h-1.5 rounded-full bg-white" />` + label, optional tag pill with `px-2 py-0.5 rounded-full border border-white/10 text-white/50`.

**gradientStyle** used on the headline word "Revitalized":
```
backgroundImage: 'linear-gradient(to right, #091020 0%, #0B2551 12.5%, #A4F4FD 32.5%, #00d2ff 50%, #0B2551 67.5%, #091020 87.5%, #091020 100%)'
backgroundSize: '200% auto'
WebkitBackgroundClip: 'text' (+ backgroundClip text)
color: 'transparent'; WebkitTextFillColor: 'transparent'
filter: 'url(#c3-noise)'
```

Shiny animation (`.animate-shiny`): 6s linear infinite, keyframes shiny `{0%: background-position: -200% center; 100%: 200% center;}`.

## Liquid-glass utility (used across cards)

```
.liquid-glass {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative; overflow: hidden;
}
.liquid-glass::before {
  content: ''; position: absolute; inset: 0; border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  pointer-events: none;
}
```

## Section 1 — Navbar

Max-width `max-w-6xl mx-auto px-6`. Motion nav fades/slides down (opacity 0 -> 1, y -10 -> 0, 0.6s easeOut). Left: just the `LogoMark` (NO "Aura" word). Center (`hidden md:flex gap-8`): links `['Solutions','Pricing','Blog','Documentation','Careers']` each `text-white/70 text-sm font-medium hover:text-white` with staggered y animation (delay 0.1 + i*0.05). Right desktop: `<AppleButton />` default label "Download Aura". Mobile right: `w-10 h-10 rounded-full border border-white/10 bg-white/5` Menu icon button.

## Section 2 — Hero

Centered section, `pt-16 md:pt-28 pb-20 text-center flex flex-col items-center`.
Motion h1 (delay 0.3, 0.8s cubic-bezier(.22,1,.36,1)), classes `text-4xl md:text-7xl font-semibold tracking-tight leading-[0.9]`:
- Line 1: "Your email." (white)
- Line 2: "Revitalized" — apply `animate-shiny` and the `gradientStyle` inline.

Then motion paragraph (delay 0.5): `mt-8 text-white/60 max-w-md text-base leading-[1.5]`:
> "Aura is the premier inbox platform for the current era. It leverages powerful AI to organize, prioritize, and refine your messages into total clarity."

Then motion div (delay 0.7) with `<AppleButton />` and `text-xs text-white/40` "Download for Intel / Apple Silicon".

## Section 3 — macOS menu bar strip

Full-width bar `h-10 bg-black/40 backdrop-blur-md border-t border-b border-white/10`. Inside `max-w-6xl mx-auto px-6 h-full flex items-center justify-between text-xs`. Left: `AppleLogo w-3.5 h-3.5`, bold white "Aura", then menu items `['File','Edit','View','Go','Window','Help']` (progressive hiding: index>2 `hidden sm:inline`, index>3 `hidden md:inline`). Right: `Search w-3.5 h-3.5` + "Wed May 6 1:09 PM". Enters with delay 0.9.

## Section 4 — Inbox mockup

`max-w-6xl mx-auto px-6 py-16 md:py-24`. Outer container `relative rounded-2xl overflow-hidden border border-white/10 bg-[#0e1014]/90 backdrop-blur-2xl`. Motion enters from y:40 at delay 1.1.

Title bar: three traffic lights `#ff5f57`, `#febc2e`, `#28c840` (each `w-3 h-3 rounded-full`); center label "Aura — Inbox" `text-xs text-white/50`.

Body `grid grid-cols-12 h-[520px]`:

**Sidebar (col-span-3, border-r, bg-black/30, p-4):**
- White "Compose with Aura" button with `Sparkles` icon (`rounded-lg bg-white text-black text-xs font-semibold px-3 py-2`).
- Nav items (icon + label + optional count): Inbox (12, active), Starred (3), Sent, Drafts (2), Archive, Trash. Active uses `bg-white/10 text-white`, others `text-white/60 hover:bg-white/5`.
- Labels section: uppercase tracking "Labels" small title, then 4 color dots: Work `#00d2ff`, Personal `#A4F4FD`, Travel `#f59e0b`, Finance `#10b981`.

**Message list (col-span-4, border-r):**
- Search header: `Search` icon + placeholder "Search mail".
- 6 messages with name, subject, preview, time, unread/active flags:
  - Linear — "Weekly product digest" — "Your team shipped 23 issues this week..." — 9:41 AM — unread + active
  - Sophia Chen — "Re: Q3 roadmap review" — "Thanks for sending the deck over. I had a few thoughts..." — 8:12 AM — unread
  - Figma — "Marcus commented on your file" — "Love the new direction on the landing hero." — Yesterday
  - Stripe — "Payout of $12,480.00 sent" — "Your payout is on its way to your bank..." — Yesterday
  - Vercel — "Deployment ready for aura-web" — "Preview is live at aura-web-g3f.vercel.app" — Mon
  - GitHub — "[aura/core] PR #482 approved" — "david-lim approved your pull request." — Mon

**Reader (col-span-5):**
- Toolbar with Reply, Forward, Archive, Trash2 icon buttons (each `w-7 h-7 rounded-md hover:bg-white/5`) and a MoreHorizontal on the right.
- Header: "Weekly product digest"; sender avatar gradient bubble `w-7 h-7 rounded-full bg-gradient-to-br from-[#00d2ff] to-[#0B2551]` with "L"; "Linear" + "to me · 9:41 AM"; "Work" pill.
- Body:
  - Card with `Sparkles` icon (color `#A4F4FD`) labeled "Summary by Aura" and text "Your team closed 23 issues, merged 14 PRs, and shipped 2 features. Top contributor: Marcus. No action needed."
  - Paragraphs: "Hi team,", "Here is your weekly digest of everything happening across your projects. This was a strong week with significant progress on the Q3 roadmap.", "Twenty-three issues were closed, fourteen pull requests were merged, and two customer-facing features went out. The velocity trend continues to climb.", "Let me know if you would like a deeper breakdown by project or contributor.", "— The Linear team" (`text-white/50`).
  - Attachment pill with `Paperclip` icon: "digest-may-6.pdf".

## Section 5 — FeatureTriage

`max-w-6xl mx-auto px-6 py-20 md:py-28`, two-column grid `grid md:grid-cols-2 gap-10 md:gap-16 items-start`.

Left column motion (y 20 -> 0, 0.7s): `SectionEyebrow label="Triage" tag="AI-native"`, h2 `mt-5 text-3xl md:text-5xl font-semibold tracking-tight leading-[1.02]`: "Clear your inbox" <br/> "in a single pass.". Paragraph `mt-6 text-white/60 text-base leading-[1.6] max-w-md`: "Aura reads every message, understands intent, and routes the noise away from the signal. Focus on what moves your day forward — the rest handles itself." Chips row (`text-xs text-white/70 px-3 py-1.5 rounded-full border border-white/10 bg-white/[0.03]`): "Auto-categorize", "Snooze for later", "Silent newsletters", "One-tap unsubscribe".

Right column: `liquid-glass rounded-2xl p-5` card. Eyebrow text: "Today · 42 messages triaged". Four sub-cards (each `liquid-glass rounded-lg p-3`):
- Priority (4) `#ffffff` — items: "Sophia Chen — Q3 review", "David Lim — contract signoff"
- Follow-up (7) `#e5e5e5` — items: "Marcus — design review", "Figma — comment thread"
- Updates (18) `#a3a3a3` — items: "Vercel — deploy ready", "GitHub — PR #482 merged"
- Archived (13) `#525252` — items: "Stripe payout · Newsletter · Receipts"

## Section 6 — LogoCloud

`max-w-6xl mx-auto px-6 py-16 md:py-20`. Centered kicker `text-xs uppercase tracking-widest text-white/40`: "Trusted by the world's most thoughtful teams". Grid `mt-10 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-6`, each logo name as `text-sm font-semibold tracking-tight text-white/50 hover:text-white`. Names: Linear, Vercel, Figma, Stripe, Ramp, Notion, Loom, Arc. Each fades in with stagger 0.05.

## Section 7 — Testimonials

`max-w-6xl mx-auto px-6 py-20 md:py-28 border-t border-white/10`. 3-col grid of `liquid-glass rounded-2xl p-6` figures. Each: blockquote `text-sm text-white/80 leading-[1.6]` wrapped in quotes, `figcaption mt-6 pt-5 border-t border-white/10` with name `text-sm font-semibold`, role `text-xs text-white/50`, company uppercased `text-xs text-white font-semibold tracking-wide`.
- "Aura gave our leadership team four hours of their week back. It reads like email from the future." — Parker Wilf, Group Product Manager, MERCURY
- "The command palette alone has changed how I process messages. I can't imagine going back to a traditional client." — Andrew von Rosenbach, Senior Engineering Program Manager, COHERE
- "Triage that actually understands context. Our team stopped dreading Monday morning inboxes." — Mathies Christensen, Engineering Manager, LUNAR

## Section 8 — Pricing

Uses custom CSS classes (not Tailwind) for cinematic typography.

Outer `<section className="c3-pricing-section">` with its own `<svg>` defining the `c3-noise` pricing filter described earlier.

Watermark (giant hero headline as backdrop):
```
<div className="c3-watermark-container">
  <div className="c3-watermark-main">
    <span className="c3-watermark-line-1">Your email.</span>
    <span className="c3-watermark-line-2">Revitalized</span>
  </div>
</div>
```

State: `yearly` boolean toggle. Three plans:
- **Free** — "Free" — "For creators taking their first steps with Forma." — Up to 3 projects in the cloud / Image export up to 1080p / Basic editing tools / Free templates and icons / Access via web and mobile app.
- **Standard** — monthly "$9,99/m" yearly "$99,99/y" — "For freelancers and small teams who need more freedom and flexibility." — Up to 50 projects in the cloud / Export up to 4K / Advanced editing toolkit / Team collaboration (up to 5 members) / Access to premium template library.
- **Pro** (`c3-card-pro`) — monthly "$19,99/m" yearly "$199,99/y" — "For studios, agencies, and professional creators working with brands." — Unlimited projects / Export up to 8K + animations / AI-powered content generation tools / Unlimited team members / Brand customization.

Each card renders: `c3-tier-small` (tier), `c3-tier-large` (price), `c3-desc`, `c3-list` of checkmark rows (white circle `c3-check` with white SVG check), `c3-btn` "Choose Plan".

Below: `c3-toggle-wrap` with "Yearly" label and a pill toggle (white knob black when off; when `.active`, background `rgba(255,255,255,0.2)`, knob white, translated 24px).

Pricing CSS (key values, include exactly):
- `.c3-pricing-section { position: relative; padding: 40px 20px 80px; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; }`
- `.c3-watermark-container { position: relative; width: 100%; max-width: 1100px; text-align: center; margin-top: 40px; z-index: 2; }`
- `.c3-watermark-main { font-size: 9rem; font-weight: 800; line-height: 0.9; letter-spacing: -0.05em; filter: url(#c3-noise); display: flex; flex-direction: column; align-items: center; }`
- `.c3-watermark-line-1 { color: #fff; }`
- `.c3-watermark-line-2 { background: linear-gradient(to right, #091020 0%, #0B2551 25%, #A4F4FD 65%, #00d2ff 100%); -webkit-background-clip: text; background-clip: text; color: transparent; -webkit-text-fill-color: transparent; }`
- `.c3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; width: 100%; max-width: 1100px; margin-top: 60px; transform: translateX(20px); position: relative; z-index: 3; }`
- `.c3-card { background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.4)); backdrop-filter: blur(14px) brightness(0.91); border: 1px solid rgba(255,255,255,1); border-radius: 44px; padding: 50px 24px; min-height: 580px; display: flex; flex-direction: column; transition: all 0.6s cubic-bezier(.22,1,.36,1); overflow: hidden; position: relative; }`
- `.c3-card::before { content:''; position:absolute; inset:0; border-radius:inherit; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 50%); pointer-events:none; }`
- `.c3-card:hover { background: rgba(15,15,15,0.6); border-color: rgba(34,211,238,0.7); transform: translateY(-12px) scale(1.01); }`
- `.c3-card-pro { background: linear-gradient(135deg, rgba(0,0,0,0.85), rgba(0,0,0,0.55)); }`
- `.c3-tier-small { font-size: 1.1rem; font-weight: 400; color: rgba(255,255,255,0.6); }`
- `.c3-tier-large { font-size: 2.8rem; font-weight: 500; letter-spacing: -0.02em; color: #fff; margin-top: 8px; }`
- `.c3-desc { font-size: 0.88rem; color: rgba(255,255,255,0.45); min-height: 3.2em; margin-top: 16px; margin-bottom: 40px; line-height: 1.5; }`
- `.c3-list li { display:flex; align-items:flex-start; gap: 14px; font-size: 0.92rem; color: rgba(255,255,255,0.8); margin-bottom: 18px; line-height: 1.4; }`
- `.c3-check { width:28px; height:28px; border-radius:50%; background: rgba(255,255,255,0.15); display:inline-flex; align-items:center; justify-content:center; flex-shrink:0; }`
- `.c3-btn { background:#fff; color:#000; padding: 10px 32px; border-radius: 100px; font-weight:600; font-size: 0.88rem; margin-top:auto; border:none; cursor:pointer; align-self:center; transition: all 0.3s cubic-bezier(.22,1,.36,1); }`
- `.c3-btn:hover { background:#f5f5f5; transform:scale(1.02); box-shadow: 0 8px 24px rgba(255,255,255,0.15); }`
- `.c3-toggle-wrap { display:flex; align-items:center; justify-content:flex-end; gap:12px; width:100%; max-width:1100px; margin-top:32px; padding-right:20px; }`
- `.c3-toggle { width:52px; height:28px; background:#fff; border-radius:100px; position:relative; cursor:pointer; border:none; transition: background 0.3s cubic-bezier(.4,0,.2,1); padding:0; }`
- `.c3-toggle-knob { width:20px; height:20px; background:#000; border-radius:50%; position:absolute; top:4px; left:4px; transition: all 0.3s cubic-bezier(.4,0,.2,1); }`
- `.c3-toggle.active { background: rgba(255,255,255,0.2); }`
- `.c3-toggle.active .c3-toggle-knob { transform: translateX(24px); background:#fff; }`
- Media query `(max-width:1024px)`: `.c3-watermark-main { font-size: 3.5rem; filter:none; }`, `.c3-watermark-line-2 { background:none; -webkit-text-fill-color:#00d2ff; color:#00d2ff; }`, `.c3-grid` becomes horizontal scroll-snap flex (`display:flex; overflow-x:auto; scroll-snap-type:x mandatory; transform:none; width:100vw; padding:0 20px; gap:16px; scrollbar-width:none`), cards `flex: 0 0 320px; scroll-snap-align:center`, `.c3-grid::-webkit-scrollbar{display:none}`, `.c3-toggle-wrap { justify-content:center; padding-right:0; }`.

## Section 9 — FinalCTA

`max-w-6xl mx-auto px-6 py-20 md:py-32`. Motion `liquid-glass relative overflow-hidden rounded-3xl px-8 py-16 md:py-24 text-center`. Radial glow overlay: `radial-gradient(600px circle at 50% 0%, rgba(255,255,255,0.15), transparent 70%)` at opacity 0.3.
- h2 `text-4xl md:text-6xl font-semibold tracking-tight leading-[1.02]`: "Close the tabs." / "Open your day.".
- Paragraph `mt-6 text-white/60 max-w-md mx-auto text-sm leading-[1.6]`: "Join thousands of builders, founders, and operators who treat email like a tool — not an obligation."
- Buttons: `<AppleButton label="Download Aura" />` and `rounded-full border border-white/15 text-white text-sm font-medium px-5 py-3 hover:bg-white/5` "Talk to sales" + ChevronRight.


Reproduce exactly — fonts, gradient stops, noise filters, copy strings, animation delays, and the CloudFront video URL `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_064122_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4`.
```

---

## 71. Immersive Ocean

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `immersive-ocean`

```
Create a fullscreen hero landing page for a creative studio called "Foldcraft" using React, Tailwind CSS, and Lucide React icons. The page is a single viewport-height section with a looping background video, a responsive navbar, a mobile menu, and staggered-animated hero text.

**Video Background:**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_204221_5339e40b-e73d-4ab0-9c65-79c18c66fd50.mp4`
- Attributes: autoPlay, muted, loop, playsInline
- Styling: absolute positioned, full width/height, object-cover, object-position at 70% horizontal center
- The video sits behind all content (no z-index or z-0)

**Font:**
- Google Fonts: Geist (weights 300-700), loaded via `<link>` in index.html
- Tailwind config extends fontFamily with `geist: ['Geist', 'sans-serif']`
- Applied as `font-geist` on the root container
- Body CSS: `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale`

**Root Container:**
- `relative h-screen w-full overflow-hidden bg-black font-geist`

**Navbar (z-30):**
- Flex, space-between, padding: `px-6 py-5 md:px-12 lg:px-16`
- Left side: Logo text "Foldcraft" (`text-lg font-semibold tracking-tight text-white sm:text-xl`) followed by desktop nav links (hidden on mobile, flex on md+)
- Nav links: Home, Projects, Studio, Reach Us (`text-sm text-white/80 hover:text-white transition-colors`)
- Right side (desktop): "Let's Talk" button (`rounded-lg bg-white px-5 py-2 text-sm font-medium text-black hover:scale-105 transition-transform`)
- Right side (mobile): hamburger toggle button (40x40, z-50) with animated Menu/X icons from lucide-react. Menu rotates 90deg out and X rotates in with opacity and scale transitions (duration-300). Button has `active:scale-90`.

**Mobile Menu (z-20):**
- Absolute, `inset-x-0 top-0`, full-screen overlay with `bg-black/98 backdrop-blur-xl`
- Transition: `duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]` toggling between `h-screen opacity-100` and `h-0 opacity-0 pointer-events-none`
- Inner content: centered vertically (`flex h-full flex-col justify-center px-8`), with a delayed fade + translate animation (delay-100, translate-y-8)
- Links: Home, Projects, Studio, Reach Us (`text-3xl font-medium text-white/90 hover:text-white`)
- Button: "Let's Talk" (`mt-6 rounded-full bg-white px-8 py-3.5 text-base font-medium text-black hover:scale-105`)
- All links/button call `setMobileMenuOpen(false)` on click

**Hero Content (z-10):**
- Flex column, justify-between, fills remaining height: `h-[calc(100vh-80px)]`
- Padding: `px-6 pb-10 pt-12 sm:pb-12 sm:pt-16 md:px-12 md:pb-16 md:pt-20 lg:px-16`

**Top Section (max-w-3xl):**
- Badge: "Brand & Visual Storytelling" (`text-xs sm:text-sm text-white/90`), with `animate-[fadeSlideUp_0.8s_ease_0.2s_both]`, margin-bottom 4 (sm:6)
- Heading h1: "Shaping visual / narratives, / one pixel at a time." with `<br/>` line breaks
  - Sizing: `text-3xl sm:text-5xl md:text-6xl lg:text-7xl`
  - Style: `font-medium leading-[1.1] tracking-tight text-white`
  - Animation: `animate-[fadeSlideUp_0.8s_ease_0.4s_both]`

**Bottom Section:**
- Paragraph: "Turning vision into reality through craft, motion, and an endless pursuit of beauty."
  - Style: `text-sm sm:text-base md:text-lg leading-relaxed text-white/60 max-w-sm sm:max-w-lg mb-5 sm:mb-6`
  - Animation: `animate-[fadeSlideUp_0.8s_ease_0.7s_both]`
- CTA Button: "Explore Work" with ArrowRight icon (size 16)
  - Style: `rounded-lg bg-white px-5 py-2.5 sm:px-6 sm:py-3 text-sm font-medium text-black hover:scale-105 transition-transform inline-flex items-center gap-2`
  - Animation: `animate-[fadeSlideUp_0.8s_ease_0.9s_both]`

**CSS Animation (in index.css):**
```css
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**CSS Reset (in index.css):**
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
```

**Dependencies:** React, lucide-react (ArrowRight, Menu, X), Tailwind CSS, Google Fonts Geist.
```

---

## 72. Contact Cybernetic

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `contact-cybernetic`

```
Build a modern, interactive hero section using React, Tailwind CSS, and Framer Motion (motion/react). Ensure you follow these precise architecture and styling instructions:
1. Fonts & Global Animations
Import the Inter font from Google Fonts.
In your CSS setup, configure Tailwind to use it by default (--font-sans: 'Inter', ...).
Create a keyframe animation in CSS named blink for the typewriter cursor:
code
CSS
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.animate-blink { animation: blink 1s step-end infinite; }
2. General Page Structure
Wrap the entire application in a container div with the following classes: relative bg-white text-neutral-900 font-sans selection:bg-[#EAECE9] selection:text-[#1C2E1E] antialiased overflow-x-hidden flex flex-col lg:block lg:min-h-screen.
3. Background Video Component (with Native Scrubbing)
Container element: Add a div containing the background video with classes: order-last lg:order-none relative lg:absolute lg:inset-0 lg:z-0 overflow-hidden pointer-events-none w-full aspect-square md:aspect-video lg:aspect-auto lg:h-full bg-neutral-50 lg:bg-transparent.
Video element: Use <video> with muted, playsInline, preload="auto".
Video Source URL: https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260601_110537_3a579fa0-7bbc-4d94-9d25-0e816c7840f5.mp4
Classes: w-full h-full object-cover object-right lg:object-right-bottom.
Scrubbing/Playback Logic via useEffect hooks:
Desktop Mouse Scrubbing Hook: Listen to the window mousemove event. If window.innerWidth < 1024, ignore (disable scrubbing). Store the mouse 'previous X' coordinate to calculate the delta against 'current X'. Update the target scrub time based on (delta / window.innerWidth) * 0.8 * video.duration. Clamp the time between 0 and duration. Set video.currentTime = targetTime. Bind a seeked event listener to ensure smooth tracking frame to frame.
Mobile Autoplay Hook: Because scrubbing is disabled on mobile frames, trigger normal playback for screens < 1024 width: video.autoplay = true and video.play().
4. Interactive Navbar
Header wrapper: Wrap the Navbar in <header className="fixed top-0 inset-x-0 z-10 px-5 sm:px-8 py-4 sm:py-5 flex flex-row justify-between items-center bg-transparent">
Logo (Left side): Flex row with gap-3.
Text: Mainframe&reg; (using the ® symbol). Classes: text-[21px] sm:text-[26px] tracking-tight text-black font-medium select-none.
Icon block right beside it: An asterisk &#10033;. Classes: text-[25px] sm:text-[30px] text-black select-none tracking-[-0.02em] font-medium leading-none mb-1.
Desktop Nav Links (Center): Flex row, hidden md:flex, text-[23px] text-black. Links are "Labs", "Studio", "Openings", "Shop" separated by <span className="opacity-40">,&nbsp;</span> dividers. Hover states should use hover:opacity-60 transition-opacity.
Desktop CTA (Right): Hidden on mobile. A link reading "Get in touch" mapped with text-[23px] text-black underline underline-offset-2 hover:opacity-60 transition-opacity.
Mobile Menu Logic:
Hamburger <button> visible below md. Has three w-6 h-[2px] bg-black spans.
Hook it to a local state isMobileMenuOpen. When open, animate the burger into an 'X' (top bar rotate-45 translate-y-[7px], middle bar opacity-0, bottom bar -rotate-45 -translate-y-[7px]). All spans need transition-all duration-300.
Create a full screen Mobile Navigation Overlay div hidden on Desktop. Fixed inset-0 z-[9] with bg-white/95 backdrop-blur-sm. Apply opacity-100 pointer-events-auto when isMobileMenuOpen is true; otherwise, opacity-0 pointer-events-none.
5. Content Layout Container
Below the background video and relative to it, add a content grouping layer: <div className="relative z-10 flex flex-col order-first lg:order-none w-full bg-white lg:bg-transparent pb-8 lg:pb-0 lg:min-h-screen">
Inside that, the overarching layout engine: <main id="spade-hero" className="w-full max-w-7xl mx-auto px-6 py-12 flex-1 flex flex-col justify-center">
6. Typewriter Hook and Headline
Implement a custom useTypewriter(text, speed = 38, startDelay = 600) React hook. It uses setTimeout and setInterval to iteratively build a string slice by slice. It must return an object: { displayed: string, done: boolean }.
Run the hook with the string "we'd love to\nhear from you!".
Wrap the headline securely in a motion.div configured to drop-in (initial: opacity: 0, y: 20, animate: opacity: 1, y: 0, transition duration 0.6).
Render your hook text inside <h1 className="text-5xl md:text-6xl lg:text-[76px] font-normal tracking-tight text-black leading-[1.08] mb-8 select-none w-full whitespace-pre-wrap">.
While typing (!done), output a <span className="inline-block w-[2px] h-[1.1em] bg-black align-middle ml-[2px] animate-blink" /> cursor at the end of the displayed text string.
7. Secondary Description Text
Another motion.div (delay 0.1s from the headline).
Content: <p> tag that reads: Whether you have questions, feedback, <br /> drop us a message and we'll get back to you as soon as possible.
Classes: text-lg md:text-xl text-[#5A635A] leading-relaxed font-normal mb-14 max-w-2xl.
8. Interactive Multi-Select Service Pills
Using setServices track an array ["Brand", "Digital", "Campaign", "Other"].
The prompt Title: "What sort of service?" (text-2xl font-medium tracking-tight mb-2). Subtitle: "Select all that apply" (opacity-85 text-[#738273] mb-8).
Iterate over the options natively outputting motion.button wrapper tags allowing multiple selections inside a flex wrap container.
Pill active traits classes: bg-[#1C2E1E] text-white shadow-md shadow-emerald-950/5 transform. Show a check icon (lucide-react) dropping in using type: "spring", stiffness: 300, damping: 20.
Pill inactive traits classes: bg-white text-[#1C2E1E] border border-[#F1F3F1] hover:bg-[#F1F3F1]/55.
Contingent Feedback Status Banner: Underneath your service pills, write an <AnimatePresence mode="wait"> that tracks user state array length:
Empty: Show a generic placeholder indicating "Please click to select services above." at fifty percent opacity (opacity: 0.5, italic, text-xs).
Active Selection: Swap cleanly into a container <motion.div> that springs height gracefully (height: "auto"). Inside, display an acknowledgment banner reading "Ready to inquire about: [array.join(", ")]" combined with an arrow call-to-action button "Let's Go" (text-[#4D6D47] uppercase text-xs). Style the banner with bg-[#FAFBF9] border rounded-2xl.
```

---

## 73. Retro-Futurist

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `retro-futurist`

```
Build a full-screen hero landing page for a creative agency called "Mainframe" using React, TypeScript, Vite, and Tailwind CSS. Here is every detail:

---

FONTS

Load two fonts in `index.html` via these stylesheet links:
- Heading: `https://db.onlinewebfonts.com/c/5ac3fe7c6abd2f62067f266d89671492?family=HelveticaNowDisplay-Medium`
- Body: `https://db.onlinewebfonts.com/c/1aa3377e489837a26d019bba501e779d?family=HelveticaNowDisplayW01-Rg`

In `index.css`, define CSS variables:
```css
:root {
  --font-heading: 'HelveticaNowDisplay-Medium', 'Helvetica Neue', Arial, sans-serif;
  --font-body: 'HelveticaNowDisplayW01-Rg', 'Helvetica Neue', Arial, sans-serif;
}
body {
  font-family: var(--font-body);
}
```

The entire page uses `var(--font-body)` except the logo text which uses `var(--font-heading)`.

---

BACKGROUND VIDEO (mouse-scrub controlled)

- A full-screen `` element is `position: fixed; inset: 0; z-index: 0; object-fit: cover; object-position: 70% center;`.
- Video source URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260530_042513_df96a13b-6155-4f6e-8b93-c9dee66fba08.mp4`
- The video is `muted`, `playsInline`, `preload="auto"`. It does NOT autoplay.
- The video scrubs forward/backward based on horizontal mouse movement. Use a `mousemove` event listener on `window`. Track `prevX`, compute `delta = currentX - prevX`, convert to a time offset: `(delta / window.innerWidth)  SENSITIVITY  video.duration` where `SENSITIVITY = 0.8`. Clamp `targetTime` between 0 and `video.duration`. Use `video.currentTime` to seek, and an `onSeeked` handler to queue the next seek if `targetTime` has moved, preventing seek-flooding.

---

**NAVBAR (fixed, z-index: 10)**

- Fixed to top, full width. Padding: `px-5 sm:px-8 py-4 sm:py-5`. Flex row, `justify-between`, `items-center`.
- **Logo (left):** Flex row with `gap-3`. Text "Mainframe(R)" (use the registered trademark symbol) at `text-[21px] sm:text-[26px]`, `tracking-tight`, black, using `var(--font-heading)`. Beside it, a decorative asterisk character `✳︎` at `text-[25px] sm:text-[30px]`, black, `select-none`, `letter-spacing: -0.02em`.
- **Desktop nav links (center, hidden below md):** Flex row, `text-[23px]`, black. Links: "Labs", "Studio", "Openings", "Shop" separated by commas rendered as `, `. Each link has `hover:opacity-60 transition-opacity`.
- **Desktop CTA (right, hidden below md):** An anchor "Get in touch" at `text-[23px]`, black, `underline underline-offset-2`, `hover:opacity-60 transition-opacity`.
- **Mobile hamburger (visible below md):** A button with 3 horizontal bars (each `w-6 h-[2px] bg-black`), spaced with `gap-[5px]`. On toggle, the top bar rotates 45deg and translates down 7px, middle bar fades to opacity 0, bottom bar rotates -45deg and translates up 7px. All transitions are `duration-300`.
- **Mobile overlay (z-index: 9):** `fixed inset-0 bg-white/95 backdrop-blur-sm`, flex column, vertically centered, left-aligned with `px-8 gap-8`. Same links at `text-[32px] font-medium`, plus "Get in touch" underlined. Fades in/out with `opacity` and `pointerEvents` toggled. Hidden on md+.

---

**HERO SECTION (z-index: 1)**

- Full `h-screen`, flex column. On mobile: `justify-end pb-12`. On `md:`: `justify-center pb-0`. Horizontal padding: `px-5 sm:px-8 md:px-10`. `overflow-hidden`.
- Content container: `max-w-xl`, `relative z-10`.

**1. Blurred intro label:**
- `pointer-events-none`, `select-none`, `mb-5 sm:mb-6`.
- Font size: `clamp(18px, 4vw, 26px)`, `line-height: 1.3`, `font-weight: 400`, `color: #000`, `filter: blur(4px)`.
- Two lines of text:
  - Line 1: "Hey there, meet A.R.I.A,"
  - Line 2: "Mainframe's Adaptive Response Interface Agent"
- Separated by a `
`.

**2. Typewriter text:**
- Text: `"Glad you stopped in. Good taste tends to find us. Now, what are we building?"`
- Custom `useTypewriter` hook: takes `text`, `speed` (default 38ms per character), `startDelay` (default 600ms). After the delay, an interval reveals one character at a time. Returns `{ displayed, done }`.
- Rendered in a `

` tag, black, `mb-5 sm:mb-6`, font size `clamp(18px, 4vw, 26px)`, `line-height: 1.35`, `font-weight: 400`, `min-height: 54px`.
- While typing, show a blinking cursor: `inline-block w-[2px] h-[1.1em] bg-black align-middle ml-[2px]` with CSS animation `blink 1s step-end infinite` (`opacity: 1 at 0%/100%, 0 at 50%`). Cursor disappears when `done` is true.

**3. Action pill buttons:**
- Appear with a fade-in + slide-up animation (`opacity 0->1`, `translateY(8px)->0`, `transition: opacity 0.4s ease, transform 0.4s ease`). They become visible 400ms after page load, independent of the typewriter animation (do NOT wait for typing to finish).
- Container: `flex flex-wrap gap-y-1`.
- **4 white pill buttons:** Labels: "Pitch us an idea", "Come work here", "Send a brief hello", "See how we operate". Each is `inline-flex items-center justify-center bg-white text-black border border-black/10 rounded-full text-[13px] sm:text-[15px] px-4 sm:px-5 py-[0.3em] mx-[0.2em] mb-[0.4em] white-space: nowrap`. Hover: `bg-black text-white`, `transition-colors duration-200`.
- **1 outline pill button:** Text "Reach us: hello@mainframe.co" (email is underlined with `underline-offset-1`), followed by a small 12x12 copy icon (inline SVG of two overlapping rectangles). Styled: `text-white bg-transparent border border-white rounded-full`, same sizing as above, with `gap-2 sm:gap-3` between text and icon. Hover: `bg-white text-black`. On click, copies "hello@mainframe.co" to clipboard via `navigator.clipboard.writeText()`.

---

DEPENDENCIES

Only React, ReactDOM, Tailwind CSS, and Vite. No other UI libraries. Lucide-react is available but not used in this component.
```

---

## 74. Prosthetics Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `prosthetics-hero`

```
Build a React + TypeScript + Tailwind CSS single-page hero section using Vite. The entire page lives in `src/App.tsx`. No extra libraries beyond `react`, `react-dom`, `lucide-react`, and Tailwind.

**Background:**
- A fullscreen autoplaying, muted, looping, `playsInline` background `<video>` element absolutely positioned `inset-0 w-full h-full object-cover`.
- Video URL (exact): `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_215831_c6a8989c-d716-4d8d-8745-e972a2eec711.mp4`
- Root wrapper: `relative min-h-screen overflow-hidden bg-[#f0f0ee]`.
- Foreground content wrapper: `relative z-10 flex flex-col min-h-screen`.

**Logo (inline SVG component):**
- `width="18" height="18"`, `viewBox="0 0 256 256"`, `fill="none"`.
- Single path with `fill="rgb(84, 84, 84)"` and `d="M 160 88 L 194 34 L 216 0 L 256 0 L 256 40 L 221.5 93.5 L 200 128 L 256 128 L 256 256 L 96 256 L 96 168 L 64.246 220 L 40 256 L 0 256 L 0 216 L 34 162 L 56 128 L 0 128 L 0 0 L 160 0 Z"`.

**Navbar (centered, pill-style, two separate pills):**
- `<nav>` classes: `flex items-center justify-center pt-4 sm:pt-6 px-4 sm:px-8 gap-2 sm:gap-3`.
- Left circular logo container: `flex items-center justify-center rounded-full w-10 h-10 sm:w-11 sm:h-11 shrink-0`, inline style `backgroundColor: '#EDEDED'`, contains the Logo.
- Right pill container: `flex items-center gap-4 sm:gap-10 rounded-xl px-4 sm:px-8 py-2.5 sm:py-3`, inline style `backgroundColor: '#EDEDED'`.
- Nav links array: `['Story', 'Products', 'Help', 'Support']`. Each anchor: `text-[12px] sm:text-[14px] font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200`.

**Hero content (bottom-left aligned):**
- Outer: `flex-1 flex items-end pb-10 sm:pb-16 lg:pb-20 px-6 sm:px-12 md:px-20 lg:px-28`.
- Inner: `max-w-xs`. Four stacked elements, each with `mb-3`:

1. Badge link: `inline-flex items-center gap-1.5 text-[11.5px] font-medium text-blue-500 hover:text-blue-600 transition-colors mb-3 group`. Text: `Seen on Shark Tank in India` followed by an arrow `→` in a span with `inline-block transition-transform duration-200 group-hover:translate-x-0.5`.

2. Headline `<h1>`: `text-[1.5rem] sm:text-[1.75rem] leading-[1.15] font-medium text-gray-900 tracking-tight mb-3`. Text: `Simple, smart prosthetics made for people who keep fighting.`

3. Subtext `<p>`: `text-[13px] text-gray-400 font-normal mb-3`. Text: `Reclaim your movement now.`

4. CTA anchor: `inline-flex items-center gap-2 text-[13px] font-medium text-blue-500 border border-blue-400 rounded-full px-5 py-2.5 hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-200 group`. Text: `Try a free fitting` plus arrow `→` in span with `transition-transform duration-200 group-hover:translate-x-0.5`.

**Animations / micro-interactions:**
- Arrow spans translate right by `0.5` on group hover (`group-hover:translate-x-0.5`).
- CTA fills blue on hover (bg + text + border transitions, 200ms).
- Nav links shift from gray-700 to gray-900 on hover.

**Fonts:** Default Tailwind sans-serif system font stack (no custom font). All sizes are exact pixel/rem values above (`11.5px`, `12px`, `13px`, `14px`, `1.5rem`, `1.75rem`).

**Colors:** Page background `#f0f0ee`; pill backgrounds `#EDEDED`; accent `blue-500/600/400`; text `gray-900/700/400`.

Do not add any other sections, no Supabase wiring, no routing. Only the single hero page as described.
```

---

## 75. Coffee Rewards

- **Category**: Loyalty App
- **Type**: mobile
- **Page Type**: hero
- **ID**: `coffee-rewards`

```
Build a mobile coffee profile screen inside a phone mockup frame. Use vanilla HTML, CSS, and JS with Vite as the bundler. The design is dark/warm-toned, inspired by iOS profile screens with glassmorphic UI elements.

**Phone mockup:**
- 390x844px at zoom 0.78, black background, 44px border-radius, overflow hidden, strong drop shadow
- Internal `.screen` div with dark background (`#180a06`), vertical scroll, hidden scrollbar

**Hero section (top):**
- Full-width, 430px tall
- Contains a looping muted autoplay video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260707_003042_3d2380a6-1ce6-4407-a2e2-cfec46546407.mp4`
- Video covers the area with `object-fit: cover; object-position: center top`
- Bottom gradient overlay fading from transparent at 52% to the background color at 100%
- Top bar with two glass circle buttons (edit icon on left, X close SVG on right), positioned absolute top 18px

**Identity section (overlaps hero by -112px margin-top):**
- Centered name "Dasha" (28px, weight 500)
- Left and right laurel images flanking the name (local assets `/assets/images/laurel-left.png` and `laurel-right.png`), 73px tall, 0.6 opacity, positioned via `right: calc(50% + 66px)` / `left: calc(50% + 66px)`
- Subtitle "Plum Parfait Latte" below (15px, muted color `rgba(235, 220, 205, 0.55)`)

**Achievements pill (centered, 30px below identity):**
- Glass pill button, 54px tall, 225px wide, 27px border-radius
- Trophy icon (local `/assets/images/icon-trophy.png`, 18px) + text "12 achievements" (18px, weight 500)

**Stats grid (3 columns, 12px gap, 26px top padding, 16px horizontal padding):**
- Each card: semi-transparent background `rgba(255,255,255,0.06)`, 24px border-radius
- Card 1: coffee image `https://polo-pecan-73837341.figma.site/_assets/v11/a8ba62db54d1e331b7beb36d69308e9b92516b99.png` (84x84), number "154", label "drinks consumed"
- Card 2: sandwich image `https://polo-pecan-73837341.figma.site/_assets/v11/953600065119f54f64ab9edb076b3cbb289fcff8.png` (84x84), number "36", label "sandwiches eaten"
- Card 3: cafe image `https://polo-pecan-73837341.figma.site/_assets/v11/aef68e05f729a30ed177f74c2cece578c05bfdba.png` (84x84), number "12", label "cafes visited"
- Numbers: 25px, weight 500. Labels: 13px, color `#BAAA9A8C`

**Favorite card (12px below stats, 16px horizontal margin):**
- Same card background, 24px radius, 110px height, flex row with 16px gap
- Latte image `https://polo-pecan-73837341.figma.site/_assets/v11/976a811111808abc50be33c2483872dbdb6ad5a8.png` (108x108, object-fit contain)
- Text column: "Favorite" (13px, weight 500), "Latte" (19px, weight 500), "Ordered 73 times" (13px, color `#BAAA9A8C`)
- Shuffle button on right (glass circle, local icon `/assets/images/icon-shuffle.png` 19px)

**Partial next card:** Same card style but only 34px tall with flat bottom corners (teaser for scroll)

**Glass button system:**
- Shared `.glass` class: no border, `rgba(255,255,255,0.03)` background, subtle inset box-shadows for edge highlights, `backdrop-filter: blur(2px) saturate(1.3)`, scale-down on `:active`
- `.glass.circle`: 58x44px, 22px radius
- `.glass.pill`: 54px tall, pill-shaped

**Fonts:**
- Primary: "Neue Haas Unica" (loaded from local `/assets/fonts/neue-haas-unica/stylesheet.css`)
- Also load "Helvetica Now Display" from `/assets/fonts/helvetica-now/stylesheet.css`
- Fallbacks: -apple-system, SF Pro Display, Inter, Segoe UI, Roboto

**Page background (behind phone):**
- Multiple warm-toned radial gradients over `#070402`:
  - `radial-gradient(ellipse 65% 55% at 15% 52%, rgba(168, 78, 10, 0.22))`
  - `radial-gradient(ellipse 52% 48% at 83% 26%, rgba(122, 52, 8, 0.17))`
  - `radial-gradient(ellipse 44% 52% at 56% 92%, rgba(98, 36, 5, 0.14))`
  - `radial-gradient(ellipse 30% 30% at 72% 75%, rgba(60, 20, 5, 0.10))`

**Entry animations (respects prefers-reduced-motion):**
- Hero: `heroReveal` - opacity 0 + scale(1.01) to normal, 1.9s, cubic-bezier(0.16, 1, 0.3, 1)
- Top bar buttons: `dropIn` from translateY(-10px), 0.7s, staggered 0.35s/0.42s
- Laurels: `fadeIn` 0.8s, delay 0.5s
- Name: `fadeRise` from translateY(16px), 0.7s, delay 0.5s
- Subtitle: same, delay 0.58s
- Achievements: same, delay 0.66s
- Stat cards: staggered at 0.74s, 0.80s, 0.86s
- Favorite card: delay 0.94s
- Next card: fadeIn delay 1.02s
- All use cubic-bezier(0.16, 1, 0.3, 1) except simple fadeIn which uses ease-out

**JavaScript (liquid glass effect):**
- Generates a displacement map canvas for each `[data-liquid]` element based on its dimensions and border-radius
- Uses SDF (signed distance field) of a rounded rectangle to compute refraction vectors
- Creates SVG `<feDisplacementMap>` filters and applies them as `backdrop-filter: url(#id) blur(0.3px) saturate(1.3)`
- Falls back to standard blur if SVG filter not supported

**CSS variables:**
```
--bg: #180a06
--card: rgba(255, 255, 255, 0.06)
--text: #ede4d8
--muted: rgba(235, 220, 205, 0.55)
--radius-card: 24px
```

**Responsive:** At 440px viewport, phone scales to zoom 0.6. Body flex-wraps at 900px.
```

---

## 76. 3D Collectible Hero

- **Category**: 3D Website
- **Type**: 3D Website
- **Page Type**: hero
- **ID**: `3d-collectible-hero`

```
Build a single full-viewport hero section in React + TypeScript + Vite + Tailwind CSS, using `lucide-react` for icons. The component is a character-figurine carousel called "TOONHUB".

**Fonts (load in `index.html` head):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
```
Body font: `'Inter', sans-serif`. Display font (huge ghost text + bottom-right link): `'Anton', sans-serif`.

**Image data (4 items, exact URLs and colors):**
```ts
const IMAGES = [
  { src: 'https://fifth-gentle-45902158.figma.site/_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/1.02464a56.png', bg: '#F4845F', panel: '#F79B7F' },
  { src: 'https://fifth-gentle-45902158.figma.site/_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/2.b977faab.png', bg: '#6BBF7A', panel: '#85CC92' },
  { src: 'https://fifth-gentle-45902158.figma.site/_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/3.4df853b4.png', bg: '#E882B4', panel: '#ED9DC4' },
  { src: 'https://fifth-gentle-45902158.figma.site/_components/v2/4de492f6d9cf8244ad5293233e5c6f52407d42fc/4.4457fbce.png', bg: '#6EB5FF', panel: '#8DC4FF' },
];
```
Preload all 4 images on mount via `new Image()`.

**State & logic:**
- `activeIndex` (0–3), `isAnimating` boolean lock, `isMobile` (`window.innerWidth < 640`, updated on resize).
- `navigate('next' | 'prev')`: ignore if animating; set `isAnimating=true`; bump `activeIndex` `(prev+1)%4` or `(prev+3)%4`; release lock after `650ms`.
- Roles derived from activeIndex: `center=activeIndex`, `left=(activeIndex+3)%4`, `right=(activeIndex+1)%4`, `back=(activeIndex+2)%4`.

**Layout structure:**
Outer `<div>` has `backgroundColor: IMAGES[activeIndex].bg`, transition `background-color 650ms cubic-bezier(0.4,0,0.2,1)`, `fontFamily: 'Inter, sans-serif'`, `relative w-full overflow-hidden`. Inside, a `relative w-full` div with `height: 100vh; overflow: hidden`.

1. **Grain overlay** (`absolute inset-0 pointer-events-none`, zIndex 50): SVG fractalNoise data URI, `baseFrequency=0.9`, `numOctaves=4`, opacity 0.08 inside SVG, container `opacity: 0.4`, `backgroundSize: 200px 200px`, repeat.

2. **Giant ghost text "3D SHAPE"** (`absolute inset-x-0 flex items-center justify-center pointer-events-none select-none`, zIndex 2, `top: 18%`): font Anton, `fontSize: clamp(90px, 28vw, 380px)`, weight 900, color white, opacity 1, lineHeight 1, uppercase, letterSpacing `-0.02em`, whiteSpace nowrap.

3. **Top-left brand label "TOONHUB"** (`absolute top-6 left-4 sm:left-8`, zIndex 60): `text-xs font-semibold uppercase`, white, opacity 0.9, letterSpacing `0.18em`.

4. **Carousel** (`absolute inset-0`, zIndex 3): map all 4 IMAGES; each item is `position:absolute`, `aspectRatio: '0.6 / 1'`, with role-based styles below. Inside, an `<img>` `width:100%; height:100%; objectFit:contain; objectPosition:bottom center; draggable=false`.

   Per-role style:
   - **center**: `transform: translateX(-50%) scale(${isMobile?1.25:1.68})`, no blur, opacity 1, zIndex 20, `left:50%`, `height: isMobile?'60%':'92%'`, `bottom: isMobile?'22%':0`.
   - **left**: `translateX(-50%) scale(1)`, blur 2px, opacity 0.85, zIndex 10, `left: isMobile?'20%':'30%'`, `height: isMobile?'16%':'28%'`, `bottom: isMobile?'32%':'12%'`.
   - **right**: same as left but `left: isMobile?'80%':'70%'`.
   - **back**: `translateX(-50%) scale(1)`, blur 4px, opacity 1, zIndex 5, `left:50%`, `height: isMobile?'13%':'22%'`, `bottom: isMobile?'32%':'12%'`.

   Transition on each item: `transform 650ms cubic-bezier(0.4,0,0.2,1), filter 650ms ..., opacity 650ms ..., left 650ms ...`. `willChange: transform, filter, opacity`.

5. **Bottom-left text + nav buttons** (`absolute bottom-6 left-4 sm:bottom-20 sm:left-24`, zIndex 60, `maxWidth:320px`):
   - `<p>` "TOONHUB FIGURINES" — bold uppercase, tracking-widest, `mb-2 sm:mb-3 text-base sm:text-[22px]`, white, opacity 0.95, letterSpacing `0.02em`.
   - `<p>` (hidden on mobile, `hidden sm:block`): "The artwork is stunning, shipped fully prepared. The finish is a vision, the 3D craft is flawless. Many thanks! Wishing you the win. Order now." — `text-xs sm:text-sm`, white, opacity 0.85, lineHeight 1.6, `mb-4 sm:mb-5`.
   - Two circular buttons (`w-12 h-12 sm:w-16 sm:h-16`, transparent bg, 2px white border, white icon): `ArrowLeft` and `ArrowRight` from lucide-react, size 26, strokeWidth 2.25. On hover: scale 1.08 + bg `rgba(255,255,255,0.12)`. Transition `transform 150ms, background-color 150ms`. Click triggers `navigate('prev')` / `navigate('next')`.

6. **Bottom-right link "DISCOVER IT"** (`absolute bottom-6 right-4 sm:bottom-20 sm:right-10`, zIndex 60): `<a>` flex items-center, font Anton, `fontSize: clamp(20px, 4vw, 56px)`, weight 400, white, opacity 0.95→1 on hover (200ms), letterSpacing `-0.02em`, lineHeight 1, uppercase, no underline. Followed by `ArrowRight` (`w-5 h-5 sm:w-8 sm:h-8`, strokeWidth 2.25).

**Behavior summary:** clicking arrows rotates roles; background color, image positions, scales, blurs, and opacities all crossfade simultaneously over 650ms with `cubic-bezier(0.4,0,0.2,1)`. The character images sit at the bottom of the screen overlapping the giant "3D SHAPE" text behind them.
```

---

## 77. Celestial Renewal

- **Category**: Wellness
- **Type**: hero
- **Page Type**: hero
- **ID**: `celestial-renewal`

```
**Build a React + Vite + Tailwind CSS landing page with two full-screen sections for a luxury beauty/wellness brand called "Serene". Use TypeScript.**

---

### Fonts (loaded via Google Fonts in index.html)

Load these three font families from Google Fonts:
- **Dancing Script** (weights: 400, 500, 600, 700) -- used for the brand logo
- **Instrument Serif** (italic: 0, 1) -- used for the hero heading and the quote text
- **Inter** (weights: 300, 400, 500, 600, 700, 800, 900) -- used for body text, navbar links, and buttons

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
```

---

### Global CSS (index.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background: #0a0a0c;
  overflow-x: hidden;
}

.font-inter {
  font-family: 'Inter', sans-serif;
}

.font-instrument {
  font-family: 'Instrument Serif', serif;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.text-glow {
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.4), 0 0 80px rgba(255, 255, 255, 0.2), 0 0 120px rgba(255, 255, 255, 0.1);
}

.button-glow {
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.3), 0 0 40px rgba(255, 255, 255, 0.1);
}
```

---

### App Layout (App.tsx)

The wrapper div has `bg-[#0a0608]`. It renders `<Hero />` followed by `<QuoteSection />`.

---

### SECTION 1: Hero

A full-viewport (`h-screen`) section with:

1. **Background video** -- autoplays, muted, loops, playsInline, covers the full section with `object-cover`:
   ```
   https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260613_180732_a54afbf6-b30d-470e-861f-669871f09f67.mp4
   ```

2. **Dark overlay** -- `absolute inset-0 bg-black/20`

3. **Fixed Navbar** -- `fixed top-0 left-0 right-0 z-50`, flex row, space-between, `px-6 md:px-12 py-5`:
   - **Left**: Brand name "Serene" in Dancing Script cursive, white, `text-2xl md:text-3xl`
   - **Center (desktop only, hidden on mobile)**: Navigation links -- "About", "Services", "Journal", "Contact" -- `text-white/80 hover:text-white text-sm tracking-wide`, spaced `gap-12`
   - **Right (desktop)**: White pill button "Book a consultation"
   - **Right (mobile)**: Hamburger icon (3 lines, animated to X on open). Uses cubic-bezier(0.22,1,0.36,1) easing. On open: top line rotates 45deg + translates down 9px; middle line fades/scales to 0; bottom line rotates -45deg + translates up 9px.
   - **Mobile menu**: Slide-in panel from right, `w-[85%] max-w-[340px]`, `bg-[#0a0608]/95 backdrop-blur-xl border-l border-white/10`. Links stagger-animate in (opacity + translateX, 75ms delay between each, starting at 150ms). Button at bottom with 450ms delay.

4. **Center content** -- absolutely positioned, flex column, centered, with `-mt-[120px]` to shift up:
   - **Heading**: `font-instrument text-white text-[36px] md:text-7xl lg:text-[110px] leading-[0.9] tracking-tight text-center text-glow` -- text: "Gentle touch. Radiant presence."
   - **Subtext**: `text-white/70 text-sm md:text-base text-center mt-5 md:mt-7 max-w-xl` -- text: "Expert beauty and holistic wellness, delivered with warmth and intention."
   - **CTA Button**: White pill button "Begin your renewal", `mt-6 md:mt-9`

5. **Sound indicator (desktop only)** -- bottom-left corner (`bottom-8 left-8`), a 40px circle with `border border-white/20` containing a small horizontal bar, next to two lines of text: "Experience" / "with sound" in `text-white/60 text-xs`

**Button component**: `bg-white text-black px-8 py-3.5 rounded-full font-medium text-sm tracking-wide hover:bg-white/90 transition-all duration-300 button-glow`

---

### SECTION 2: Quote Section (with parallax scroll animations)

A full-viewport (`h-screen`) section with:

**Background**: CSS linear-gradient top to bottom:
```
#010A17 0% -> #0A4267 30% -> #20658E 60% -> #6BADC4 100%
```

**Animated layers (requestAnimationFrame-based parallax with lerp smoothing):**

The animation uses a `progress` value (0 to 1) based on how far the section has scrolled through the viewport:
```
progress = clamp(0, 1, (windowHeight - rect.top) / (windowHeight + rect.height))
```

1. **Rainbow image** -- full-width, positioned `absolute inset-x-0 top-0 z-30`. Parallax: moves vertically from +120px to -160px based on scroll progress. Lerp factor: 0.06.
   ```
   https://soft-zoom-63098134.figma.site/_assets/v11/8d520a7515d06cbfc403d0125e3d05b1a7ccd29c.png
   ```

2. **Left cloud** -- `absolute left-0 bottom-[10%] z-10`, hidden on mobile (`hidden sm:block`). Width: `w-[500px] md:w-[650px]`. Has `marginLeft: '-50%'` to let it overflow left. Slides in from -200px on X when in view (progress 0.12-0.92), slides back out when not. Also drifts up (cloudY = progress * -50). Opacity tied to X distance. Lerp factor: 0.04.
   ```
   https://soft-zoom-63098134.figma.site/_assets/v11/0d6dfd3f90b930f21726f2ed56a3320d79b7a797.png
   ```

3. **Right cloud** -- same image as left but `scale-x-[-1]` (flipped), `absolute right-0 bottom-[15%] z-10`. Has `marginRight: '-75%'`. Slides in from +200px. Same lerp/timing as left cloud.

4. **Quote content** -- centered, `z-20`, `max-w-4xl`:
   - **Quote text**: `font-instrument text-white text-xl sm:text-2xl md:text-4xl lg:text-[42px] leading-[1.45] md:leading-[1.5]` -- text: "Serene was founded on a belief in beauty that honors your nature. We pursue refined outcomes, considered approaches, and lasting vitality. We spend time learning what matters to you before deciding what serves you best. No rushing, no excess -- just support that lets you feel radiant." (wrapped in curly quotes)
   - **Attribution**: `mt-6 md:mt-8 text-white/80 text-sm md:text-base tracking-wide` -- text: "Dr. Mia Callahan -- Founder"

**Key animation implementation detail**: All transforms use `translate3d` for GPU acceleration with `will-change-transform`. Initial cloud state is `opacity: 0` and translated off-screen. The lerp function smoothly interpolates current values toward targets each frame: `current + (target - current) * factor`.

---

### Tailwind Config

Default Tailwind config with no extensions -- all custom styling handled via CSS utility classes in index.css.
```

---

## 78. Neo Museum

- **Category**: Website
- **Type**: hero
- **Page Type**: hero
- **ID**: `neo-museum`

```
Project Setup

Stack: React 19 + Vite 6 + Tailwind CSS 4 + Motion (Framer Motion) + Lucide React icons + TypeScript

package.json dependencies:
- `react`, `react-dom` ^19.0.1
- `vite` ^6.2.3
- `@tailwindcss/vite` ^4.1.14, `tailwindcss` ^4.1.14
- `motion` ^12.23.24
- `lucide-react` ^0.546.0
- `@vitejs/plugin-react` ^5.0.4
- `typescript` ~5.8.2

Fonts (loaded via Google Fonts in `index.css`):
- Sans: Inter (weights: 300, 400, 500, 600)
- Mono: JetBrains Mono (weights: 400, 500)

```css
/* index.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
@import "tailwindcss";

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, monospace;
}

@layer utilities {
  .text-mega {
    font-size: 21vw;
    line-height: 0.75;
    letter-spacing: -0.04em;
  }
}
```

Global styling: Background `#fcfcfc`, text `#111`, selection color `bg-black text-white`, `overflow-x-hidden`, `font-sans` (Inter).

---

DATA

```tsx
const chaptersData = [
  { name: "Age of Dinosaurs", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624247/01_udnber.png" },
  { name: "Fossils of Ancient Life", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624374/02_pmvxxl.png" },
  { name: "Reptiles of the Mesozoic", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624236/03_hcp3jc.png" },
  { name: "Marine Fossil Gallery", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624256/04_get63z.png" },
  { name: "Prehistoric Giants", image: "https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624251/05_kz1tyu.png" }
];
```

---

STATE

```tsx
const [showVideo, setShowVideo] = useState(false);
const [activeChapter, setActiveChapter] = useState(2); // starts at "Reptiles of the Mesozoic"
const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
```

- `showVideo` flips to `true` after a 2800ms delay (setTimeout)
- `activeChapter` auto-cycles every 3500ms via setInterval, wrapping `(prev + 1) % 5`

---

ANIMATION VARIANTS

```tsx
const fadeUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

const letterBlock = {
  initial: { y: 120, opacity: 0 },
  animate: { 
    y: 0, 
    opacity: 1, 
    transition: { duration: 1.2, ease: [0.16, 1, 0.3, 1] } 
  }
};
```

---

SECTION 1: HERO (full viewport height)

Container: `relative w-full min-h-screen flex flex-col overflow-hidden`

1A. HEADER (NHM Logo)

- `motion.header` with `staggerChildren: 0.1, delayChildren: 0.1`
- Padding: `pt-6 px-6 md:px-16`, `z-20`
- The "NHM" logo is a custom inline SVG with `viewBox="0 0 840 100"`, `fill-[#111]`, full width
- The SVG is wrapped in `motion.h1` with `variants` that animate from `scale: 1.03` to `scale: 1` with `staggerChildren: 0.06, delayChildren: 0.1`
- Each polygon of each letter uses the `letterBlock` variant (slides up from `y: 120`)
- Letter N (translate 0,0): Three polygons -- left vertical `0,0 14,0 14,100 0,100`, right vertical `200,0 214,0 214,100 200,100`, diagonal `0,0 33,0 214,100 181,100`
- Letter H (translate 280,0): Three polygons -- left vertical `0,0 14,0 14,100 0,100`, right vertical `200,0 214,0 214,100 200,100`, crossbar `14,43 200,43 200,57 14,57`
- Letter M (translate 560,0): Four polygons -- left vertical `0,0 14,0 14,100 0,100`, right vertical `266,0 280,0 280,100 266,100`, left diagonal `0,0 26,0 153,100 127,100`, right diagonal `254,0 280,0 153,100 127,100`

1B. SUB-NAV BAR

- Below the SVG logo, `flex justify-between items-start mt-8`
- Font: `text-[10px] md:text-[11px] font-mono tracking-[0.2em] uppercase`
- Uses `fadeUp` variant with `duration: 0.8, ease: "easeOut"`

Left column (15% width): Three lines -- "Natura" / "History" / "Museum"

Arrow separator (5% width, hidden on mobile): `ArrowRight` from lucide, size 14, strokeWidth 1, `text-gray-400`

Center column (flex-1 on mobile, 30% on desktop): "Exploring the story of life on earth through science, discovery and wonder." -- Split differently on desktop (3 lines) vs mobile (4 lines). `text-gray-800 leading-relaxed font-mono`

Arrow separator (5% width, hidden on mobile): Same as above

Right column (15% width, hidden on mobile): Nav links list -- Visit, Exhibitions, Discover, Learn, About. `text-gray-800`, `hover:text-black hover:underline`

Hamburger button (far right, z-60): Two horizontal lines (`w-8 h-[1.5px] bg-black`), `gap-[6px]`. Hover: first line shrinks to `w-6`, second expands to `w-10`. When open: first rotates 45deg + translateY, second rotates -45deg + translateY (forming an X). Transition: `duration-300`.

1C. MOBILE MENU OVERLAY

- `AnimatePresence` wrapping a `motion.div`
- Appears below the header, slides in from `y: -20`, `opacity: 0` to `y: 0, opacity: 1`
- `bg-[#fcfcfc] border-b border-gray-200 shadow-xl`, only visible on `md:hidden`
- Contains the same nav links as the desktop version, `text-sm font-mono tracking-[0.2em] uppercase`, `space-y-6`

1D. BACKGROUND VIDEO

- Appears after 2800ms delay (controlled by `showVideo` state)
- `absolute top-0 left-0 w-full h-full pointer-events-none z-0`
- Video: `autoPlay loop muted playsInline`, `w-full h-full object-cover`
- Video URL: `https://res.cloudinary.com/dsdxaxkiz/video/upload/v1779624998/magnific_use-img-2-as-the-exact-ba_Piu3X0W42C_wnrc8f.mp4`

1E. LEFT SIDEBAR CONTENT

- `motion.div` with `staggerChildren: 0.15, delayChildren: 0.6`
- Position: `px-10 md:px-16`, `mt-20 sm:mt-28 md:mt-32`, `w-[320px]`, `z-10`

Section indicator: `01` + horizontal line (`w-16 h-[1.5px] bg-black/20`), `text-xs font-mono`

Headline: "TIMELESS WONDERS" -- `text-[3.5rem] md:text-[5rem] font-normal tracking-tight leading-[1]`. Line break between "TIMELESS" and "WONDERS".

Description: "Step into the natural world and / discover the stories written / millions of years ago." -- `text-[13px] md:text-[14px] text-gray-700 w-[240px] leading-[1.6]`

CTA Button ("Explore Now"):
- Container: `bg-[#1a1a1a] px-6 py-3.5 border border-[#1a1a1a] rounded-md shadow-sm`
- Hover: slides up 0.5px, adds `shadow-[3px_3px_0px_rgba(17,17,17,0.5)]`
- Active: resets translate and shadow
- Has a sliding background panel: `bg-[#fcfcfc]` that slides from `-translate-x-[101%]` to `translate-x-0` on hover, `duration-700 ease-[cubic-bezier(0.16,1,0.3,1)]`
- Icon: Custom SVG leaf/plant shape (4 paths forming a stylized leaf), white by default, turns `#111` on hover with `scale-110 -rotate-12 -translate-y-1` transform
- Text: "Explore Now", `text-[15px] font-medium`, white turning to `#111` on hover

1F. RIGHT SIDEBAR (hidden on mobile)

- `motion.div` with `staggerChildren: 0.15, delayChildren: 0.9`
- Position: `w-[200px] mt-12 md:mt-20`, `hidden md:flex`

Specimen info: "Tyrannosaurus Rex" heading (`text-[10px] font-bold font-mono tracking-widest uppercase`), subtext "Late Cretaceous period / 68-66 million years ago" (`text-[12px] text-gray-600 leading-[1.6]`)

Stats: "Length" label + "12.3 m" value, "Height" label + "4.0 m" value. Labels: `text-[10px] font-mono tracking-widest uppercase text-gray-500`. Values: `text-[13px] font-medium`.

View Details button: Circle (`w-10 h-10 rounded-full border border-gray-400`) with `Plus` icon (size 16, strokeWidth 1.5), text "View Details" (`text-[10px] font-mono uppercase tracking-widest font-bold`). Hover: circle gets `border-black bg-[#111]`, icon turns white.

1G. BOTTOM-LEFT "SCROLL TO EXPLORE"

- `absolute bottom-10 left-[2.5rem] md:left-[4rem]`, `hidden md:flex`
- Fade up animation: `delay: 1.2`
- Circle (`w-12 h-12 rounded-full border border-gray-300`) containing two thin vertical lines (`w-[1px] h-[12px] bg-gray-600`, `gap-[4px]`) representing a pause icon
- Text: "Scroll to explore" -- `text-[10px] font-mono tracking-widest uppercase text-gray-500 font-semibold`

---

SECTION 2: "EXPLORE OUR WORLD"

Container: `relative w-full min-h-[75vh] md:min-h-screen bg-[#fcfcfc]`, flex column centered, `pt-24 md:pt-32 pb-0 z-20`

2A. SECTION LABEL

`[ 02 ] Explore Our World` -- `text-[10px] md:text-[11px] font-mono tracking-[0.2em]`, `mb-12`. "02" in `text-gray-500`, "Explore Our World" in `text-gray-900 font-bold uppercase`.

2B. MAIN HEADING

"Unearth the stories of our planet's past through fossils, minerals, and ancient wonders." -- `text-[2.2rem] md:text-[3.5rem] lg:text-[4.2rem] leading-[1.1] font-medium tracking-tight text-[#111]`, max-width 1000px, text-center. Line break on desktop after "past". Animates with `whileInView` from `y: 40, opacity: 0` to `y: 0, opacity: 1`, `once: true`, margin `-100px`.

2C. ACTION PILLS

Five pill buttons in a flex-wrap row, `gap-3 md:gap-4`, `mb-10 md:mb-24`. Staggered reveal animation (`staggerChildren: 0.1, delayChildren: 0.3`). Each pill: `rounded-full border border-gray-300 text-[11px] font-medium uppercase tracking-wider bg-white/50 backdrop-blur-sm text-gray-800`. Hover: `border-black bg-black text-white`. Icons from lucide (size 14, strokeWidth 2):

1. `Bone` + "Dinosaurs"
2. `Dna` + "Ancient Life"
3. `Gem` + "Minerals"
4. `Leaf` + "Fossils"
5. `BookOpen` + "Learn More"

2D. SPACER

`min-h-[220px] md:min-h-[450px]` -- provides room for the pterodactyl image from Section 3 to overlap upward.

2E. BOTTOM TEXT

Absolute positioned at bottom, `px-8 md:px-16 pb-8 md:pb-12`, `pointer-events-none`. Two text elements at `justify-between`:
- Left: "WE DON'T JUST TELL STORIES."
- Right: "PALEONTOLOGY (C) 2026"
- Both: `text-[10px] font-mono tracking-widest uppercase text-gray-500 font-medium`, hidden on mobile.

---

SECTION 3: "ANCIENT COLLECTION" (Dark Section)

Container: `relative w-full bg-[#0a0a0a] text-white flex flex-col z-30`

3A. PTERODACTYL IMAGE (Overlapping)

- Absolute positioned at top, centered horizontally (`left-1/2 -translate-x-1/2`)
- Width: `w-[160vw] md:w-[1100px]`
- Image URL: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779625001/ChatGPT_Image_May_23_2026_12_24_44_PM_1_lv1dne.png`
- Animates with `whileInView` from `y: "-65%", opacity: 0` to `y: "-78%", opacity: 1`, `duration: 1.4, ease: "easeOut"`, viewport margin `100px`
- `pointer-events-none z-0`, `mix-blend` not applied here

3B. HEADING AREA

- Padding: `px-8 md:px-16 pt-32 md:pt-48 mb-16`, `z-10`
- Two-column layout on xl (`flex-col xl:flex-row justify-between`)

Left -- Main heading: "Curated from millions of years of wonder [3 circle icons] & discovery." -- `text-[1.8rem] md:text-[3rem] lg:text-[3.8rem] xl:text-[4rem] leading-[1.15] font-medium tracking-tight text-white`. The three circle icons are inline (`inline-flex gap-2 md:gap-3 align-middle mx-2 md:mx-4 translate-y-[-4px]`), each `w-10 h-10 md:w-14 md:h-14 rounded-full border border-gray-600 bg-black text-gray-400`. Hover: `bg-white text-black border-white`. Icons: `Bone`, `Dna`, `Leaf` (size 22).

Right -- Tagline + pills:
- Tagline: "WE DON'T JUST DISPLAY FOSSILS / WE SHARE EARTH'S STORY" -- `text-[9px] md:text-[10px] font-mono tracking-widest text-gray-400 uppercase mb-6 leading-relaxed`
- Three pills: "Educational", "Authentic", "Inspiring" -- `px-5 py-2 rounded-full border border-gray-600 text-[9px] font-mono tracking-widest uppercase text-gray-300`. Hover: `bg-white text-black border-white`.

3C. TWO-COLUMN PANEL

Separated by `h-[1px] bg-gray-800` line. Flex row on desktop, column on mobile.

Left panel (35% width):
- `border-r border-gray-800` on desktop, `border-b` on mobile
- `min-h-[400px] md:min-h-[500px]`
- Top: `***` text (`text-gray-500 text-xl tracking-[0.3em]`)
- Center: Chapter image using `SandTransitionImage` component (SVG filter-based sand/dissolve transition). Image: `absolute inset-0 w-[80%] h-[80%] m-auto object-contain mix-blend-lighten`. Uses `AnimatePresence mode="wait"`.
- Bottom: Chapter counter `01 / 05` style, with animated number (`motion.div` slides vertically). `text-[10px] font-mono tracking-widest text-[#888] uppercase`. Counter numeral color `#888`, divider `text-[#333]`.

Right panel (65% width):
- Top bar: "Explore the past. Understand the present." + animated "Chapter 0X" label. `border-b border-gray-800 p-8 text-[10px] font-mono text-gray-400 tracking-widest`.
- Chapter list: 5 items, each `border-b border-gray-800/80 py-8`. Active: `text-white`, inactive: `text-[#444] hover:text-[#999]`. Chapter name: `text-2xl md:text-[2rem] font-medium tracking-tight`. Active item shows `ArrowUpRight` icon (size 22, strokeWidth 1, `text-gray-400`) that animates in/out.
- Clicking a chapter sets `activeChapter`.

3D. BOTTOM FOOTER

- `h-[1px] bg-gray-800` divider
- Text: "DIGGING INTO OUR PLANET'S PAST" -- `px-8 py-8 text-[10px] font-mono tracking-widest text-gray-500 uppercase bg-[#0a0a0a]`

---

SandTransitionImage COMPONENT

A custom component that creates a sand/particle dissolve effect using SVG filters:

```tsx
function SandTransitionImage({ src, alt, className }) {
  // Uses usePresence() from motion/react for AnimatePresence awareness
  // Unique filterId per instance via useRef
  // requestAnimationFrame loop over 900ms
  // Easing: entering = quartic ease-out (1 - Math.pow(1-t, 4)), exiting = cubic (Math.pow(t, 3))
  // SVG filter chain:
  //   1. feTurbulence: fractalNoise, baseFrequency 1.8, numOctaves 4
  //   2. feDisplacementMap: scale up to 150 based on progress
  //   3. feOffset: dy up to -80 (enter) or 120 (exit), dx up to -30/+30
  //   4. feGaussianBlur: up to 6px
  //   5. feColorMatrix: opacity fades (1 - progress * 1.2)
  // Image has crossOrigin="anonymous" and referrerPolicy="no-referrer"
}
```

---

ALL EXTERNAL ASSET URLs

Video:
- `https://res.cloudinary.com/dsdxaxkiz/video/upload/v1779624998/magnific_use-img-2-as-the-exact-ba_Piu3X0W42C_wnrc8f.mp4`

Images:
- Chapter 1: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624247/01_udnber.png`
- Chapter 2: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624374/02_pmvxxl.png`
- Chapter 3: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624236/03_hcp3jc.png`
- Chapter 4: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624256/04_get63z.png`
- Chapter 5: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779624251/05_kz1tyu.png`
- Pterodactyl: `https://res.cloudinary.com/dsdxaxkiz/image/upload/v1779625001/ChatGPT_Image_May_23_2026_12_24_44_PM_1_lv1dne.png`

(Note: these are Cloudinary URLs, not CloudFront. The project uses Cloudinary for all hosted media assets.)

---

KEY DESIGN DETAILS

- Color palette: `#fcfcfc` (off-white bg), `#111` / `#1a1a1a` (near-black), `#0a0a0a` (dark section bg). Gray scale via Tailwind: `gray-300` through `gray-800`.
- No purple/indigo anywhere. Strictly monochrome black/white/gray.
- Typography hierarchy: Large display headings (3.5-5rem), mono labels (10-11px), body text (13-14px).
- Spacing: 8px base system throughout.
- Transitions: Most hover transitions 300-700ms. Button slide effect uses `cubic-bezier(0.16, 1, 0.3, 1)`. Letter animations use same cubic bezier.
- The page is entirely a single `App.tsx` component plus the `SandTransitionImage` helper function in the same file.
```

---

## 79. Place Saver

- **Category**: Travel
- **Type**: mobile
- **Page Type**: hero
- **ID**: `place-saver`

```
**Build a single-page HTML showcase displaying two iOS device frames (370x790px each) side by side on a neutral `#F4F4F4` stage. The stage auto-scales to fit the viewport using JS. Both phones have a Dynamic Island, status bar (time "11:11", signal/wifi/battery icons in white SVG), and a home indicator bar. Animations are gated behind video `loadeddata` events + font loading, with a 5s safety timeout.**

---

### Fonts

1. **ITC Garamond Std Narrow** (self-hosted from Cloudinary):
   - Light (300): `https://res.cloudinary.com/dgupuutfn/raw/upload/v1783596334/ITCGaramondStd-LtNarrow_i2zcip.woff2` / `.woff` variant `ITCGaramondStd-LtNarrow_soc5vc.woff`
   - Book (400): `https://res.cloudinary.com/dgupuutfn/raw/upload/v1783596334/ITCGaramondStd-BkNarrow_xjfoc0.woff2` / `.woff` variant `ITCGaramondStd-BkNarrow_wfoxm1.woff`
   - Book Italic (400 italic): `https://res.cloudinary.com/dgupuutfn/raw/upload/v1783596334/ITCGaramondStd-BkNarrowIta_hiy9ld.woff2` / `.woff` variant `ITCGaramondStd-BkNarrowIta_rlarxo.woff`

2. **Google Fonts**: `Playfair Display` (400, 500, 600 + italic) and `Inter` (400, 500, 600, 700)

---

### Screen 1 -- "The place for all your places" (Light device frame)

**Background**: Dark (#02040c). Uses a native 470x1008 design scaled down to 370x790 via `transform: scale(0.787234)` with `transform-origin: top left`.

**Video background (hero)**:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260710_114906_ad7cee37-9e56-434f-99bc-92d5bdc4f9fe.mp4
```
- `autoplay loop muted playsinline`, `object-fit: cover`, `object-position: center 48%`, covers entire frame, z-index 0.

**Hero fade overlay**: Bottom 46% of the frame, gradient from `rgba(2,4,12,0)` to `rgba(2,4,12,.35)` at 46% to `rgba(2,4,12,.72)` at 100%. z-index 1.

**Logo** (centered, top 74px):
```
https://polo-pecan-73837341.figma.site/_assets/v11/b1ddc82509144261f1999a0c4d92be5ce6689c0f.png
```
- Width 118px, `filter: drop-shadow(0 0 7px rgba(190,215,255,.28))`. z-index 4.

**Title** (top 618px, centered, z-index 4):
- Font: ITC Garamond Std Narrow, weight 300, 66px, line-height 68px, letter-spacing 0.2px
- Text: `The place for all` then line break, then `your places` in italic (weight 400)
- Text shadow: `0 0 34px rgba(255,255,255,.22), 0 1px 2px rgba(0,0,0,.35)`
- The italic "your places" has an extra glow: `0 0 10px rgba(255,255,255,.6), 0 0 20px rgba(255,235,190,.5), 0 0 40px rgba(255,210,140,.32)`

**Subtitle** (top 787px, centered, z-index 4):
- Font: Inter, 16.5px, weight 400, line-height 26px, color `rgba(255,255,255,.52)`
- Text: "Save, Organize and Share\nyour favorite places"

**Button** (top 874px, left 32px, 406x55px, z-index 4):
- White background, border-radius 28px, box-shadow `0 6px 26px rgba(0,0,0,.28)`
- Apple logo SVG (18x21, fill #1a1a1a) + text "Continue with Apple"
- Font: Helvetica Neue, 18px, weight 500, -webkit-text-stroke 0.6px #1a1a1a

**Terms** (top 950px, centered, z-index 4):
- Font: 12px, weight 400, color `rgba(255,255,255,.42)`
- Text: "By continuing, you agree to **Terms of Use**" (bold text is `rgba(255,255,255,.82)`, weight 400)

---

### Screen 2 -- "Unlock Pro" (Dark device frame)

**Background**: Dark (#14151d).

**Video background**:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260710_115050_a1ba47d0-aedf-413c-9dea-14509599d3dd.mp4
```
- `autoplay loop muted playsinline`, positioned `left: 0; top: -30%`, 370x790px, `object-fit: cover`, z-index 0.

**Background fade** (full overlay, z-index 1):
```css
linear-gradient(to bottom,
  rgba(20,21,29,0) 0%, rgba(20,21,29,0) 40%,
  rgba(20,21,29,0.55) 55%, rgba(20,21,29,0.92) 66%,
  #14151d 74%, #14151d 100%);
```

**Heading** (left 28px, top 386px):
- Font: ITC Garamond Std Narrow, weight 500, 26px, line-height 1, color white
- Letter-spacing 0.2px, text-shadow `0 0 18px rgba(120,180,220,0.35)`
- Text: "Unlock Pro:"

**Divider** (left 28px, top 418px, 265x1px):
- `linear-gradient(to right, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.30) 70%, rgba(255,255,255,0) 100%)`

**Feature list** (left 28px, top 429px, width 314px):
Each row is 24px tall with a 22px-wide icon area + text (13.5px, weight 400, white, 4px left margin).

Icons are all SVG, 19x19 (or 20x20 for infinity), stroke #fff, stroke-width 1.7, no fill:

1. **Layers icon** (paths: `M12 2 2 7l10 5 10-5-10-5Z` / `M2 12l10 5 10-5` / `M2 17l10 5 10-5`) -- "Create private Guides"
2. **Phone icon** (rect 6,2.5 12x19 rx2.5 + line 10.5,18.5 to 13.5,18.5) -- "Import from social media"
3. **Infinity icon** (path: `M18.178 8c5.096 0 5.096 8 0 8-5.095 0-7.988-8-13.083-8-5.096 0-5.096 8 0 8 5.095 0 7.988-8 13.083-8z`) -- "Unlimited Guides"
4. **Sparkle icon** (path: `M12 3c.4 3.6 1.4 4.6 5 5-3.6.4-4.6 1.4-5 5-.4-3.6-1.4-4.6-5-5 3.6-.4 4.6-1.4 5-5Z`) -- "AI search"
5. **People icon** (circle cx8.5 cy8 r3 + path for body + second person outline) -- "Collaborate with friends"

**Pricing cards** (left 28px, top 561px, 314x123px):

- **Monthly card** (left 0, 144x123px, border-radius 14px):
  - Background image: `https://polo-pecan-73837341.figma.site/_assets/v11/ef4533e6536f2495088e56e0f98036b5ff15446d.png` (cover, centered)
  - Border: 1px solid `rgba(255,255,255,0.11)`
  - Inner padding: 14px 14px 15px 15px
  - "Monthly" label (13px, weight 400), "$20" price (19px, weight 500, margin-top 6px, letter-spacing 0.3px), "Billed Monthly" at bottom-left (12px)
  - All text white with `text-shadow: 0 1px 6px rgba(0,0,0,0.35)`

- **Yearly card** (left 154px, 160x123px, border-radius 14px):
  - Background: #1e212a, border: 1px solid `rgba(255,255,255,0.11)`
  - "Yearly" label + "Billed Yearly" in `rgba(255,255,255,0.50)`
  - "$200" price in `rgba(255,255,255,0.62)`
  - **Save badge** (left 15px, top 66px): inline-flex pill, padding 5px 8px, border-radius 11px, background #4d5057, text "Save $40.00" (10.5px, weight 600, color `rgba(255,255,255,0.65)`, letter-spacing 0.2px)

**Subscribe button** (left 28px, top 709px, 314x50px):
- White background, border-radius 26px
- "Subscribe" text: Helvetica Neue, 16px, weight 500, color #0c0c0e, -webkit-text-stroke 0.4px
- Right chevron SVG: 9x15, stroke #0c0c0e, stroke-width 2, path `M1.5 1.5 7 7.5 1.5 13.5`

---

### iOS Device Frame (reusable for both)

- Width: 370px, Height: 790px, Border-radius: 48px
- Light frame: background `#F2F2F7`; Dark frame: background `#000`
- Box-shadow: `0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.12)`
- Dynamic Island: 126x37px, border-radius 24px, black, centered at top 11px
- Status bar time: SF Pro weight 590, 17px, white
- Status bar icons: signal bars (4 rects), WiFi (3 arcs + dot), battery (rect + fill + nub) -- all white SVG
- Home indicator: 139x5px bar, border-radius 100px, `rgba(0,0,0,0.25)` on light / `rgba(255,255,255,0.7)` on dark

---

### Stage Layout

- Gap between phones: 70px
- Viewport padding: 40px
- Background: `#F4F4F4`
- Auto-scale JS: measures stage vs viewport, applies `transform: scale(min(1, fitRatio) * 0.95)` centered

---

### Entrance Animations

All paused until `.ze-ready` class is added to viewport (triggered when both videos fire `loadeddata` + fonts ready, or 5s timeout).

**Keyframes used:**
- `zeBgSettle`: scale 1.12 + opacity 0 to scale 1 + opacity 1 (1.7s, for backgrounds)
- `zeReveal`: translateY(26px) + scale(0.985) + blur(7px) + opacity 0 to normal (0.9s)
- `zeDrop`: translateY(-16px) + scale(0.90) + opacity 0 to normal (0.9s)
- `zeLine`: scaleX(0) to scaleX(1), transform-origin left (0.9s)
- `zePop`: translateY(8px) + scale(0.78) to bounce scale(1.07) to scale(1) (0.7s, spring easing)

**Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (expo-out). Save badge uses `cubic-bezier(0.34, 1.56, 0.64, 1)` (spring).

**Stagger (Screen 1):**
- Hero bg: 0s delay
- Logo (zeDrop): 0.45s
- Title (zeReveal): 0.62s
- Subtitle: 0.78s
- Button: 0.94s
- Terms: 1.06s

**Stagger (Screen 2):**
- Video bg (zeBgSettle): 0.12s delay
- Heading (zeReveal): 0.58s
- Divider (zeLine): 0.72s
- Row 1-5 (zeReveal): 0.80s, 0.88s, 0.96s, 1.04s, 1.12s
- Monthly card: 1.22s
- Yearly card: 1.30s
- Subscribe button: 1.42s
- Save badge (zePop): 1.55s

**Reduced motion:** All animations disabled via `@media (prefers-reduced-motion: reduce)`.

-
```

---

## 80. Nexto 404

- **Category**: 404
- **Type**: hero
- **Page Type**: hero
- **ID**: `404`

```
Build a 404 "Page Not Found" hero page as a single full-viewport (100vh, no scroll) React + Vite + Tailwind CSS application using the DM Sans font and Google Material Symbols Rounded icons. The page must match the following specification exactly:

---

## Fonts & External Resources

- **Google Font:** DM Sans (all weights, variable: `opsz 9..40, wght 100..1000`)
- **Google Material Symbols Rounded:** `opsz,wght,FILL,GRAD@24,400,1,0`
- **Logo image:** `https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/Tests/logoipsum-415.svg` (rendered with `filter: brightness(0)` to make it black, height 28px)
- **Background spaceship image:** `https://pub-e68758f43067417dba612b2371819aa1.r2.dev/viktor-components/alien-spaceship.png`

---

## Layout

The entire page is exactly `100vh` with `overflow: hidden` on html, body, and `#root`. No scrolling. The body uses `display: flex; flex-direction: column`. The `#root` div also uses `height: 100vh; display: flex; flex-direction: column; overflow: hidden`.

---

## Background

Body has a layered background:
1. The spaceship PNG centered at `center 40%`, sized with `background-size: contain`
2. A `linear-gradient(to top left, #F5F5F5, #F7F7F7)` covering the full page

Both are `background-attachment: fixed` and `no-repeat`.

---

## Color Variables (CSS custom properties)

```
--text-main: #1a1a1a
--text-secondary: #888888
--bg-page: #F5F5F5
--card-bg: #ffffff
```

---

## Navbar

- Max-width `1100px`, centered, padding `28px 40px`
- Has a dashed bottom border made with `background-image: linear-gradient(to right, rgba(0,0,0,0.08) 2px, transparent 2px); background-size: 6px 1px` on a `::after` pseudo-element
- **Left:** Logo (the SVG image + the text "nexto." in 20px bold, -0.3px letter-spacing, color #111, flex with 9px gap)
- **Center:** Nav links ("Our Team", "Solutions" with a dropdown arrow character, "Showcase", "News") - 14px, weight 400, opacity 0.65, hover to opacity 1, gap 36px
- **Right:** CTA button "Let's Connect" - dark gradient button (`linear-gradient(180deg, #2c2c2c 0%, #111111 100%)`), white text 13px weight 500, border-radius 40px, padding `5px 16px 5px 5px`. Has a white circular arrow icon (24px circle) on the LEFT side with a chevron SVG inside. Box-shadow `0 4px 15px rgba(0,0,0,0.15)`. On hover: translateY(-1px), stronger shadow, brightness(1.1).
- **Hamburger (mobile only):** 3 spans, 24px wide, 2px height, animates to X when active. Hidden on desktop, shown on mobile (`display: flex` at max-width 768px).

---

## Mobile Navigation

- Fixed full-screen overlay, slides in from right with `transform: translateX(100%)` -> `translateX(0)`, cubic-bezier(0.77, 0, 0.175, 1) transition
- On mobile: left-aligned, large links (38px, weight 800, letter-spacing -1.5px), each with bottom border, padding 24px 0
- Last link is the CTA button styled same as navbar but with 32px arrow circle

---

## Main Content Area

- `flex: 1`, centered both ways (`align-items: center; justify-content: center`), max-width 700px, padding `20px 20px 30px`
- **Lost text:** "Seems you've wandered off..." - 15px, color `--text-secondary`, weight 400, margin-bottom 12px
- **Title wrapper:** `position: relative; display: inline-block; margin-bottom: 14px`
  - **Cloud decoration:** Material Symbols "cloud" icon, positioned `top: -18px; left: -24px`, font-size 42px, with gradient text fill (`linear-gradient(to bottom, #F7B2FB 50%, #786EF1 80%, #5588FB 100%)` using `-webkit-background-clip: text; -webkit-text-fill-color: transparent`), white drop-shadow outline, `floatSlow` animation (5s, 0.3s delay)
  - **Heart decoration:** Material Symbols "favorite" icon, positioned `bottom: -15px; right: 20px`, font-size 32px, same gradient fill, white drop-shadow outline, `floatSlow` animation (4.5s, 1s delay)
  - **Title:** "Whoops! Nothing here yet" - `font-size: clamp(34px, 5vw, 52px)`, weight 500, letter-spacing -1.5px, line-height 1.08, color #0f0f0f
- **Subtext:** "Grab a 30-minute `chat` to explore your ideas, scope, and vision. We'll find common ground, sync and `define` a clear roadmap." - 14px, color `--text-secondary`, line-height 1.7, max-width 470px, margin-bottom 28px. The words "chat" and "define" are in highlighted tags (inline-flex, background #E0E2E7, 12.5px, weight 600, padding 2px 12px, border-radius 6px)

---

## Navigation Cards

- Flex column, gap 12px, max-width 460px, positioned at bottom with `margin-top: auto`
- **Card 1 "Main Page":** House SVG icon (path: `M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H5a1 1 0 01-1-1V9.5z` with door `M9 21V12h6v9` in white). Subtitle: "Back where it all begins..."
- **Card 2 "Showcase":** Circle-dot SVG icon (circle r=9 filled, inner circle r=3.5 white). Subtitle: "Where we walk the walk"
- Each card: white background, border-radius 18px, padding 18px 22px, flex between, 1px border rgba(0,0,0,0.05), shadow `0 2px 12px rgba(0,0,0,0.04)`. On hover: translateY(-3px), shadow `0 8px 28px rgba(0,0,0,0.08)`.
- Icon container: 48px circle, background #eaecf0, scales 1.05 on card hover
- Right chevron arrow (rsaquo character, 21px), translateX(6px) on hover
- Card title: 15px weight 600, subtitle: 12px color `--text-secondary`

---

## Animations

```css
@keyframes floatSlow {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(3deg); }
}
```

---

## Responsive Breakpoints

**768px and below:**
- Hide nav-links and desktop CTA button, show hamburger
- Background-size: 90%, position: center 45%
- Navbar padding: 20px
- Title: 30px, decorations smaller
- Cards: full width, gap 10px, smaller padding/icons

**480px and below:**
- Title: 26px
- Background-size: 100%
- Decorations even smaller

---
```

---

## 81. Pixel Grid Hover

- **Category**: Case Studies
- **Type**: blog
- **Page Type**: hero
- **ID**: `pixel-grid-hover`

```
Build a "Projects / Case Studies" section as a React + TypeScript component using Tailwind CSS 3 and Framer Motion. Font is `'DM Sans', sans-serif` (Google Fonts: `https://fonts.googleapis.com/css?family=DM+Sans:500,400`). White background, black text. Here is the exact specification:

---

**Section Container:**
- `<section>` with `relative bg-white text-black`, inline style `fontFamily: "'DM Sans', sans-serif"`
- All animations use easing `[0.22, 1, 0.36, 1]`
- Inject a `<style>` block for the marquee keyframe:
  ```css
  @keyframes marqueeProjects {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
  }
  .marquee-projects {
    animation: marqueeProjects 28s linear infinite;
  }
  .marquee-projects:hover {
    animation-play-state: paused;
  }
  ```

---

**Top Area (Header with floating squares):**
- Container: `relative px-6 pb-10 pt-32 sm:px-10 lg:px-16 lg:pt-40`
- Contains a `pointer-events-none absolute inset-0 overflow-hidden` layer with 8 parallax floating black squares. Each square uses `useScroll` (target: the section ref, offset `["start end", "end start"]`) and `useTransform` + `useSpring` for vertical parallax, plus a gentle infinite bob animation (`y: [0, -10, 0]`, duration `3s + index * 0.4s`, ease `easeInOut`, staggered delay `index * 0.3s`).
- Square positions (x%, y%, size px):
  ```
  (6, 20, 12), (12, 32, 8), (8, 44, 6), (88, 18, 10),
  (92, 30, 14), (85, 42, 7), (90, 52, 5), (14, 56, 5)
  ```
- Parallax formula: `useTransform(scrollYProgress, [0, 1], [0, -(80 + index * 30)])`, smoothed with `useSpring({ stiffness: 40, damping: 20 })`

**Header text** (centered, inside `relative mx-auto max-w-7xl text-center`):
- Animates from `opacity: 0, y: 24` to visible, duration `0.7s`, triggered by `useInView` with `{ once: true, margin: "-60px" }`
- Badge: "Projects" in `mb-5 inline-block bg-black px-4 py-1.5 text-[13px] font-medium tracking-wide text-white`
- Heading: `text-[clamp(1.8rem,3.2vw,2.8rem)] font-light leading-[1.25] tracking-tight`
  - "Insights from " in `text-black`, then "Our" in `text-black/40`
  - New line: "Case Studies" in `text-black/40`

---

**Case Study Cards (2x2 grid):**
- Container: `mx-auto max-w-7xl px-6 pb-16 sm:px-10 lg:px-16`, inner `grid gap-4 md:grid-cols-2`
- Each card animates from `opacity: 0, y: 30` to visible, staggered `delay: index * 0.1`, duration `0.7s`

**4 case studies data:**
```
1. id: "heartx", title: "HeartX", category: "Brand Strategy & Product Design", year: "2026"
   image: https://images.pexels.com/photos/7691249/pexels-photo-7691249.jpeg?auto=compress&cs=tinysrgb&w=800

2. id: "swave", title: "Swave\u00AE", category: "Web Design & Identity", year: "2025"
   image: https://images.pexels.com/photos/2559941/pexels-photo-2559941.jpeg?auto=compress&cs=tinysrgb&w=800

3. id: "eduspark", title: "EduSpark", category: "Brand Strategy & Web Design", year: "2023"
   image: https://images.pexels.com/photos/5428003/pexels-photo-5428003.jpeg?auto=compress&cs=tinysrgb&w=800

4. id: "greenergy", title: "Greenergy", category: "Brand Strategy & Web Design", year: "2022"
   image: https://images.pexels.com/photos/2800832/pexels-photo-2800832.jpeg?auto=compress&cs=tinysrgb&w=800
```

**Each card structure** (aspect ratio `4/3`, `group relative overflow-hidden`):

1. **Background image**: absolutely positioned, `h-full w-full object-cover`

2. **Pixel-block hover overlay**: A 12-column x 8-row grid of absolutely positioned `bg-black/80` blocks. Each block covers `100/12 %` width and `100/8 %` height. On hover they animate `scale: 0 -> 1, opacity: 0 -> 1` with a diagonal stagger: `delayIn = (row + col) * 0.018s`, `delayOut = ((8 - row) + (12 - col)) * 0.012s`. Duration `0.25s`. This creates a pixel-dissolve reveal effect on hover.

3. **Magnetic squares**: 5-6 small black squares per card, absolutely positioned. They react to the cursor via `useMotionValue` + `useTransform` + `useSpring`: when the card is hovered, each square shifts toward the pointer proportionally (`dist * 40`). Spring config: `{ stiffness: 80, damping: 18, mass: 0.6 }`. When pointer leaves, they spring back to center (pointer resets to `0.5, 0.5`).

   Square positions per card (x%, y%, size px):
   ```
   HeartX:    (5,30,16), (10,42,10), (3,52,7), (80,70,14), (85,82,9), (78,60,6)
   Swave:     (82,55,16), (88,68,10), (78,72,7), (85,42,6), (90,80,8)
   EduSpark:  (4,24,16), (10,36,10), (2,44,7), (78,78,14), (84,88,8)
   Greenergy: (82,26,14), (88,38,10), (78,44,7), (84,54,5), (90,60,8)
   ```

4. **Plus button** (top right): `absolute right-4 top-4`, `h-7 w-7 items-center justify-center border border-white/30 text-xs text-white`, "+" text, `zIndex: 10`

5. **Info plate** (bottom left): `absolute bottom-0 left-0 bg-white px-4 pb-3 pt-2.5`, `zIndex: 20`, `maxWidth: "70%"`
   - Title: `text-[clamp(1.4rem,2.2vw,2rem)] font-normal leading-tight text-black`
   - Below: flex row with category (`text-[12px] text-black/60`) and year (`text-[12px] font-medium text-black`), `mt-1.5 gap-4`

---

**Footer Area:**
- Container: `mx-auto max-w-7xl px-6 pb-6 sm:px-10 lg:px-16`
- Flex row on desktop (`md:flex-row md:items-end md:justify-between`), column on mobile

**Left side** (`max-w-md`):
- Plus button: `mb-4 flex h-7 w-7 items-center justify-center border border-black/20 text-xs text-black`, "+"
- Paragraph: "We partner with ambitious brands that are ready to move beyond fragmented visuals and shallow quick fixes -- turning their identity, website, and messaging into one focused engine for growth." in `text-[14px] leading-[1.7] text-black/60`
- CTA button (`mt-6`): A `<button>` with `group flex items-end`:
  - Main label: `inline-flex items-center gap-[10px] border border-black/20 bg-black px-3 py-2 text-base font-medium text-white`, hover `bg-black/85`. Text: "Let's work together"
  - Arrow badge: A small `h-6 w-6` black square with `mb-6`, containing a diagonal arrow SVG (white, 16x16, viewBox `0 0 24 24`, path: `M18.75 6V15.75C18.75 15.949 18.671 16.14 18.53 16.28C18.39 16.421 18.199 16.5 18 16.5C17.801 16.5 17.61 16.421 17.47 16.28C17.329 16.14 17.25 15.949 17.25 15.75V7.81L6.53 18.53C6.39 18.671 6.199 18.75 6 18.75C5.801 18.75 5.61 18.671 5.47 18.53C5.329 18.39 5.25 18.199 5.25 18C5.25 17.801 5.329 17.61 5.47 17.47L16.19 6.75H8.25C8.051 6.75 7.86 6.671 7.72 6.53C7.579 6.39 7.5 6.199 7.5 6C7.5 5.801 7.579 5.61 7.72 5.47C7.86 5.329 8.051 5.25 8.25 5.25H18C18.199 5.25 18.39 5.329 18.53 5.47C18.671 5.61 18.75 5.801 18.75 6Z`). On group hover, the badge shifts up: `mb-6 -> mb-9`, with `transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]`

**Right side** (`flex-1 overflow-hidden md:ml-12`, with `border-t border-black/10` on mobile, no border on desktop):
- An infinite horizontal marquee (`overflow-hidden py-5`)
- Inner track: `marquee-projects flex w-max` (uses the CSS keyframe above, 28s duration)
- Pauses on hover
- 8 logos, doubled (16 total) for seamless loop. Each item: `flex shrink-0 items-center gap-2.5 px-8`
  - An SVG icon (black, varying per logo)
  - Name text: `whitespace-nowrap text-sm font-medium tracking-wide text-black/80`

**8 marquee logos** (name, icon type):
```
("Codecraft_", code), ("ennLabs", dots), ("GlobalBank", circle-ring),
("45 Degrees\u00b0", arrow), ("AlphaWave", wave-circle), ("Biosynthesis", lines),
("Boltshift", bolt), ("Clandestine", plus)
```

**SVG icon definitions** (all black stroke or fill):
- **code**: 22x18, viewBox `0 0 22 18`, stroke, strokeWidth 2, round caps. Two polylines `6,4 1,9 6,14` and `16,4 21,9 16,14`, one line `13,2 to 9,16`
- **dots**: 20x20, viewBox `0 0 20 20`, filled. 9 circles at grid positions `[3,10,17] x [3,10,17]`, radius `2.2`
- **circle-ring**: 22x22, viewBox `0 0 22 22`, stroke, strokeWidth 2. Two circles at `(11,11)` with radii `9` and `4`
- **arrow**: 18x18, viewBox `0 0 18 18`, stroke, strokeWidth 2, round caps. Line `2,16 to 16,2`, polyline `7,2 16,2 16,11`
- **wave-circle**: 22x22, viewBox `0 0 22 22`, stroke, strokeWidth 1.5. Circle `(11,11)` r=9, path `M5 11Q8 7 11 11Q14 15 17 11`
- **lines**: 24x18, viewBox `0 0 24 18`, stroke, strokeWidth 2.2, round caps. Three horizontal lines: `(0,3 to 24,3)`, `(6,9 to 24,9)`, `(0,15 to 18,15)`
- **bolt**: 14x20, viewBox `0 0 14 20`, filled. Polygon `8,0 0,11 6,11 6,20 14,9 8,9`
- **plus**: 18x18, viewBox `0 0 18 18`, filled. Two rects: `(7.5, 0, 3, 18)` and `(0, 7.5, 18, 3)`

**Bottom spacer**: `<div className="h-12" />`

---

**Dependencies:** React 18, Framer Motion (v12+), Tailwind CSS 3. Uses `useRef`, `useState`, `useCallback`, `useScroll`, `useTransform`, `useSpring`, `useMotionValue`, `useInView`, and `motion` from framer-motion. No other libraries.
```

---

## 82. Wellness Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `wellness-hero`

```
Build a full-screen hero section landing page for "Aurai" - an always-on AI wellness companion. The page is a single viewport-height section with a looping background video and overlaid content.

## Video Background

- Full-screen `<video>` element with `autoPlay`, `loop`, `muted`, `playsInline` attributes
- Video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260618_174853_aac61aa2-0f3f-4cf1-bc78-7f657dd11164.mp4`
- Video covers entire viewport with `object-cover`
- Focal point positioning:
  - Mobile (default): `object-position: 80% center`
  - Tablet (md breakpoint): `object-position: right center`
  - Desktop (lg breakpoint): `object-position: center center`

## Fonts

- **Askan Light** loaded from: `https://db.onlinewebfonts.com/c/304a6edcec9f8858eeaafc2ac18243f4?family=Askan+Light` - used for the brand name and heading
- **Inter** (weights 300, 400, 500, 600) from Google Fonts - used as the body/UI font
- Tailwind config extends fontFamily with `askan: ['"Askan Light"', 'serif']` and `inter: ['Inter', 'sans-serif']`

## Layout Structure

The content is layered on top of the video using `absolute inset-0 z-10` with a flex column layout. Padding: `px-4 sm:px-10 lg:px-12 py-4 sm:py-8`.

## Navigation (Top)

A `<nav>` with `flex items-center justify-between`:

**Left nav pill (glassmorphism):**
- `bg-black/20 backdrop-blur-md rounded-2xl border border-white/10`
- Padding: `px-4 py-2.5 sm:px-6 sm:py-4`
- Contains:
  - A custom SVG logo (4-petal pinwheel shape, `w-5 h-5 sm:w-7 sm:h-7`, white)
  - Brand text "Aurai" in `font-askan text-white text-base sm:text-xl tracking-wide`
  - Hamburger menu icon (lucide-react `Menu`/`X`) with left margin: `ml-4 sm:ml-32 md:ml-64 lg:ml-96`

**Right button (desktop only):**
- `hidden sm:block bg-white text-gray-900 font-medium text-sm px-6 py-3 rounded-full`
- Text: "Join the list"

## Mobile Menu (shown on toggle)

- `sm:hidden`, positioned `absolute top-[4.5rem] left-4 right-4`
- `bg-black/30 backdrop-blur-xl rounded-2xl p-5 border border-white/10`
- Contains links: "Story", "Benefits", "Connect" (white text) and a full-width "Join the list" button

## Main Content (Bottom-aligned)

On mobile: a spacer `flex-1 sm:hidden` pushes content to the bottom.

The content container: `flex flex-col sm:flex-1 sm:flex-row sm:items-end pb-4 sm:pb-12 lg:pb-16 sm:mt-auto`

**Left column:**

1. **Heading:** `font-askan text-white text-[2rem] sm:text-[3.5rem] md:text-[4.5rem] lg:text-[5.5rem] leading-[1.05] tracking-tight max-w-[700px]`
   - Text: "Your calm is always within."

2. **Subtitle:** `text-white/70 text-xs sm:text-base md:text-lg max-w-[520px] leading-relaxed`
   - Text: "Aurai is your always-on wellness companion. Built by leading therapists, it brings you the care and clarity right when you need it."

3. **Email form:** A rounded pill input with inline submit button
   - Container: `bg-black/30 backdrop-blur-md rounded-full border border-white/10`
   - Input: transparent background, white text, placeholder "Your email address", `px-4 sm:px-6 py-3 sm:py-4 text-sm`
   - Submit button (absolute right-1.5): `bg-white text-gray-900 text-xs sm:text-sm font-medium px-3 sm:px-6 py-2 sm:py-3 rounded-full`
   - Text: "Join the list"
   - On submit: shows alert with entered email

4. **Feature pills (mobile only):** `flex sm:hidden flex-wrap gap-2 mt-2`
   - Three pills with `bg-black/30 backdrop-blur-md text-white text-xs px-3 py-1.5 rounded-full border border-white/10`
   - Labels: "Smart Therapy", "Real-time Healing", "Insights into outcomes"

**Right column (desktop only):**
- `hidden sm:flex flex-col items-end gap-2 self-end`
- Same three feature pills as mobile but with `text-xs sm:text-sm px-4 py-2`

## Custom SVG Logo

A pinwheel/4-quadrant shape with this path:
```
M 228 0 C 172.772 0 128 44.772 128 100 L 128 0 L 0 0 L 0 28 C 0 83.228 44.772 128 100 128 L 0 128 L 0 256 L 28 256 C 83.228 256 128 211.228 128 156 L 128 256 L 256 256 L 256 228 C 256 172.772 211.228 128 156 128 L 256 128 L 256 0 Z
```
ViewBox: `0 0 256 256`, fill: `currentColor`

## Global CSS

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
```

## Key Design Principles

- No dark overlay on the video - content relies on glassmorphism pills and text contrast
- All interactive glass elements use `bg-black/20` or `bg-black/30` with `backdrop-blur-md` or `backdrop-blur-xl`
- Borders are `border-white/10` throughout
- White text with `/70` opacity for secondary text
- Rounded-full for buttons and inputs, rounded-2xl for containers
- Page title: "Aurai - Always-On Wellness Companion"
```

---

## 83. Beauty Categories

- **Category**: Categories
- **Type**: features
- **Page Type**: hero
- **ID**: `beauty-categories`

```
---

**Prompt to recreate the "Categories" section:**

> Build a "Categories" section in React + Tailwind CSS with the following exact specifications:
>
> **Section Container:**
> - Full-width `<section>` with `bg-white`, `text-white`, `min-h-screen`.
> - Flexbox column layout with `justify-center` to vertically center the grid content.
> - No horizontal or vertical padding on the section itself.
>
> **Grid Layout:**
> - A CSS grid: `grid-cols-1` on mobile, `md:grid-cols-3` on medium+.
> - The entire grid uses an IntersectionObserver-based reveal animation (threshold `0.1`): transitions from `opacity-0 translate-y-12` to `opacity-100 translate-y-0` over `duration-1000 ease-out`.
>
> **3 Category Cards with exact data:**
> 1. Name: `"face"` | Video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_203023_87a26602-2898-4acc-a396-c7a2b5ad84fd.mp4`
> 2. Name: `"beauty tools"` | Video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_203415_b86e3f19-2aec-46cd-9a86-b64c40118e38.mp4`
> 3. Name: `"body"` | Video: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_203051_85fee398-ea01-4aa0-972b-137a74213be5.mp4`
>
> **Card Layout (each card):**
> - `position: relative`, flexbox column with `justify-between`, `items-start`.
> - Padding: `p-6` mobile, `sm:p-8`, `md:p-12`.
> - Heights: `min-h-[400px]` mobile, `sm:min-h-[500px]`, `md:min-h-[750px]`.
> - `overflow-hidden`.
> - Each card has a staggered `transitionDelay` of `index * 150ms`.
> - Uses `group` for hover interactions.
>
> **Background Video:**
> - `<video>` element with attributes: `autoPlay`, `loop`, `muted`, `playsInline`.
> - Positioned absolutely: `absolute inset-0 w-full h-full object-cover`.
> - Hover effect: `scale-105` over `duration-700` via `transition-transform group-hover:scale-105`.
> - The `src` attribute is set directly from the video URL (no `<source>` tag).
>
> **Dark Overlay:**
> - A `<div>` absolutely positioned over the video: `absolute inset-0`.
> - Default: `bg-black/10`. On hover: `group-hover:bg-black/20`.
> - `transition-colors duration-500`.
>
> **Category Name (vertical text):**
> - `<h2>` tag, positioned above overlay: `relative z-10`.
> - Font sizes: `text-5xl` mobile, `sm:text-6xl`, `md:text-7xl`, `lg:text-8xl`. Weight: `font-medium`.
> - **Vertical text**: achieved with inline style `writingMode: 'vertical-lr'` combined with `transform: 'rotate(180deg)'` (this makes text read bottom-to-top).
> - Hover: `group-hover:-translate-y-2` over `duration-500`.
> - Text is lowercase (rendered as-is from the data: "face", "beauty tools", "body").
>
> **Shop Button:**
> - `<button>` with class `btn-primary` (see CSS below) plus `relative z-10 mt-auto px-8 py-3 bg-white text-black rounded-full text-sm`.
> - Text: `"shop {category name}"` in lowercase (e.g., "shop face", "shop beauty tools", "shop body").
> - `mt-auto` pushes the button to the bottom of the card.
>
> **Required CSS for `btn-primary` (in global stylesheet):**
> ```css
> .btn-primary {
>   position: relative;
>   overflow: hidden;
>   transition: transform 0.3s ease, box-shadow 0.3s ease;
> }
> .btn-primary::before {
>   content: '';
>   position: absolute;
>   inset: 0;
>   background: linear-gradient(120deg, transparent 0%, rgba(0, 0, 0, 0.05) 50%, transparent 100%);
>   transform: translateX(-100%);
>   transition: transform 0.5s ease;
> }
> .btn-primary:hover {
>   transform: translateY(-2px);
>   box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
> }
> .btn-primary:hover::before {
>   transform: translateX(100%);
> }
> .btn-primary:active {
>   transform: translateY(0);
>   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
> }
> ```
>
> **IntersectionObserver hook (`useInView`):**
> - Accepts a `threshold` parameter (default `0.15`), uses a ref.
> - Observes the element; once `isIntersecting` is true, sets `isVisible = true` and unobserves (one-shot animation).
> - Returns `{ ref, isVisible }`.
> - This section calls it with threshold `0.1`.

---
```

---

## 84. CozyPaws

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `cozypaws`

```
## Prompt to Recreate CozyPaws Hero Section

**Build a single-page "CozyPaws" pet store hero section using React, Tailwind CSS, and Lucide React icons. The layout is viewport-height (h-screen), no scroll, with three responsive breakpoints (mobile, tablet md, desktop lg+). Use Vite + TypeScript.**

---

### Fonts (Google Fonts)
- **Inter** (weights: 400, 500, 600) — body/UI text
- **DM Serif Display** (weight: 400) — hero heading only

Load via `<link>` in `index.html`:
```
https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap
```

Apply with CSS utility class `.font-serif-display { font-family: 'DM Serif Display', serif; }` and `body { font-family: 'Inter', sans-serif; }`

---

### Color Palette
- Background: `#EFFDF0` (light mint green)
- Primary dark green: `#1a3d1a`
- Hover green: `#2a5a2a`
- Orange accent: `#E86A10`
- Orange hover: `#d45e0d`

---

### Asset URLs (all external, do not download)

| Asset | URL |
|-------|-----|
| Logo SVG | `https://polo-pecan-73837341.figma.site/_assets/v11/0ae29d6d9628bede667f90d57bebe81b8f1ec2bf.svg` |
| Avatar | `https://polo-pecan-73837341.figma.site/_assets/v11/e62173d41f91350a59628e8a9a55ae078a886fb9.png?w=128` |
| Product card (Cat House) | `https://polo-pecan-73837341.figma.site/_assets/v11/3e5158dad63d392ade022e81890edc9f54d750bc.png` |
| Video card (TikTok/YouTube) | `https://polo-pecan-73837341.figma.site/_assets/v11/76be6ec3a93a703b15e9cc01e764a4e3f9d7d2c0.png` |
| Bottom left image | `https://polo-pecan-73837341.figma.site/_assets/v11/8d44b25186ef45a5789c74668fb781cea4e1ff49.png` |
| Bottom center image (tallest) | `https://polo-pecan-73837341.figma.site/_assets/v11/96745c4e72ad5c5208e53a885df797fd82cd854a.png?h=1024` |
| Bottom right image | `https://polo-pecan-73837341.figma.site/_assets/v11/81bd2e7a66b58f3d8f3ad78fd1ebf01af8dfdee1.png` |

---

### Header
- Full-width, `px-12` on desktop, `py-4`, relative z-30
- **Left:** Logo image (205x52px desktop, 130x33px mobile)
- **Center nav (hidden below md):** Links "Home" (text-gray-900), "Shop", "Delivery and payment", "Brands", "Blog" (text-gray-600), text-sm font-medium, gap-8
- **Right:** Search button (circle, border, hidden below sm), Favorites button (orange circle, white star icon, badge "4"), Cart button (circle, border, cart icon, badge "1"), Avatar (circle, 40x40)
- Badges: absolute -top-1 -right-1, 20x20, bg-orange, border-2 border-background, white text 10px bold

---

### Desktop Hero Layout (lg+)

**Text layer (z-5):** Centered, `px-12 pt-[5.4rem]`
- Heading: `font-serif-display`, color `#1a3d1a`, `text-[clamp(60px,7.5vw,110px)]`, `leading-[0.95]`, tracking-tight
- Text reads: "Everything" (line 1), "Your Pets Love" (line 2)
- Each word is an `inline-block` with staggered `animate-word-pop` animation

**Left product card:** Absolutely positioned `top-[50px] left-12`
- Width: `clamp(160px,14vw,260px)`
- Image: aspect-ratio 260/257, rounded-2xl, overflow-hidden
- Arrow button bottom-right corner (dark green circle, ArrowUpRight icon)
- Text below: "Cozy Cat House" in gray-700, "$49.99" in dark green bold
- Responsive font sizes via clamp

**Right video card:** Absolutely positioned `top-[50px] right-12`
- Width: `clamp(120px,10vw,177px)`
- Image: aspect-ratio 177/287, rounded-2xl
- Play button (dark green circle) centered near bottom
- Text below play button: "Watch Product Reviews on TikTok and YouTube"

**Bottom 3 images:** Absolutely positioned `bottom-0 left-0 right-0`, z-10, flex items-end, no gaps
- Left image: `flex-1`, max-height `min(70vh, 55vw)`
- Center image: `flex-[1.265]` (wider), max-height `min(85vh, 70vw)`
- Right image: `flex-1`, max-height `min(70vh, 55vw)`
- All images: `w-full h-auto block`

**Overlays on bottom images:**
- Left: "98K+" stat with avatar stack (avatar + green circle with Plus icon)
- Center: "Best Products for Your Pet" white heading + "Explore Products" orange pill button with ArrowRight icon
- Right: "4.6" rating with orange filled Star icon
- All positioned with `bottom: clamp(20px, 4vh, 50px)`

---

### Tablet Layout (md to lg) — Similar to desktop but smaller
- Heading: text-7xl
- Side cards at `top-[80px]`, left-4/right-4, smaller fixed widths (160px/120px)
- Bottom images: same 3-panel flex, maxHeight 60vh/75vh/60vh

---

### Mobile Layout (below md)
- Top section: centered title (36px), subtitle, "Explore Products" button
- Two cards side-by-side (flex, gap-3): product card (aspect-square) + video card (aspect-3/4)
- Stats row: "98K+" with avatars left, divider, "4.6" star right
- Bottom images: same 3-panel flex, no max-height constraint

---

### Animations (CSS keyframes, custom classes)

| Class | Keyframe | Duration | Easing |
|-------|----------|----------|--------|
| `.animate-fade-up` | 0→30px translateY, 0→1 opacity | 0.8s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-fade-in` | 0→1 opacity | 0.6s | ease-out |
| `.animate-slide-up` | 0→60px translateY | 0.9s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-slide-in-left` | -40px→0 translateX | 0.8s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-slide-in-right` | 40px→0 translateX | 0.8s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-text-reveal` | translateY(40px) skewY(3deg) blur(4px) → none | 1s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-word-pop` | translateY(60px) scale(0.7) rotate(-4deg) blur(8px) → bounce overshoot → settle | 0.9s | cubic-bezier(0.34, 1.56, 0.64, 1) |
| `.animate-scale-in` | scale(0.85)→1 | 0.7s | cubic-bezier(0.16, 1, 0.3, 1) |
| `.animate-photo-reveal` | translateY(80px) scale(1.02) → normal | 1.1s | cubic-bezier(0.16, 1, 0.3, 1) |

All use `animation-fill-mode: both`. `.animate-word-pop` starts with `opacity: 0`.

**Delay classes:** `.delay-100` through `.delay-1200` in 100ms increments.

---

### Stagger Order
1. Header fades in (100-300ms)
2. Hero heading words pop in (200-600ms stagger)
3. Side cards slide in (600-700ms)
4. Bottom photos reveal upward (600-900ms stagger, center first)
5. Overlay stats/buttons pop in (1000-1200ms)

---

### Key Technical Details
- Container: `h-screen flex flex-col overflow-hidden` (no scrolling)
- Header: `shrink-0`
- Hero section: `flex-1 flex flex-col overflow-hidden`
- All responsive layouts use show/hide (`hidden lg:flex`, etc.), not CSS-only media queries
- Extensive use of `clamp()` for fluid typography and spacing
- Lucide icons used: Search, ShoppingCart, Star, ArrowUpRight, Play, ArrowRight, Plus
```

---

## 85. Visual Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `visual-hero`

```
**Build a fullscreen hero section in a Vite + React + TypeScript + Tailwind CSS project. Use `gsap` and `lucide-react`. No other UI libraries.**

### Fonts (in `src/index.css`)
Import at the top of index.css BEFORE `
@tailwind
` directives:
```css
@import
 url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&display=swap');

@font
-face {
  font-family: 'Dirtyline';
  src: url('https://fonts.cdnfonts.com/s/15011/Dirtyline36DaysofType.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
```
Body font: `'Barlow', sans-serif`, background `#000`.

### Tailwind config (`tailwind.config.js`)
```js
theme: {
  extend: {
    fontFamily: {
      heading: ['Instrument Serif', 'serif'],
      body: ['Barlow', 'sans-serif'],
      dirtyline: ['Dirtyline', 'sans-serif'],
    },
    borderRadius: { DEFAULT: '9999px' },
  },
},
```

### CSS (append to `src/index.css`)
```css
.liquid-glass {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0)    40%,
    rgba(255,255,255,0)    60%,
    rgba(255,255,255,0.15) 80%,
    rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.liquid-glass-strong {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  border: none;
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);
  position: relative;
  overflow: hidden;
}
.liquid-glass-strong::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.5) 0%,
    rgba(255,255,255,0.2) 20%,
    rgba(255,255,255,0)   40%,
    rgba(255,255,255,0)   60%,
    rgba(255,255,255,0.2) 80%,
    rgba(255,255,255,0.5) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.hero-title {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: clamp(96px, 18vw, 280px);
  line-height: 0.92;
  letter-spacing: -0.02em;
  color: white;
  text-align: center;
}
```

### Component (`src/App.tsx`)

**Constants:**
- `NAV_LINKS = ['Gallery', 'Styles', 'API', 'Pricing', 'Blog']`
- `VIDEO_SRC = 'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_080827_a9e5ad52-b6ee-4e79-b393-d936f179cfd7.mp4'`

**LogoMark** — inline SVG, 44x26, viewBox `0 0 44 26`, three white rects at x=0/16/30, y=3, widths 14/12/14, height 20, rx=3.

**State/refs:**
- `mounted` (boolean, set true in a mount effect for fade-in).
- `videoRef` (HTMLVideoElement), `videoBgRef` (HTMLDivElement), `displayCanvasRef` (HTMLCanvasElement).
- `framesReady` boolean state, `framesRef` = `useRef<HTMLCanvasElement[]>([])`.

**Effect 1 — Frame capture (boomerang setup):**
- On mount, get `videoRef.current`. Set `capturing = true`, `lastTime = -1`, `MAX_WIDTH = 960`, `frames: HTMLCanvasElement[] = []`.
- `captureFrame()`: bail if `!capturing` or `readyState < 2` or `currentTime === lastTime`. Update `lastTime`. Scale = `min(1, 960/videoWidth)`. Create offscreen canvas at scaled w/h, `ctx.drawImage(video, 0, 0, w, h)`, push to frames.
- Use `requestVideoFrameCallback` when available, else `requestAnimationFrame` fallback.
- On `loadedmetadata`: call `http://video.play().catch(()=>{})` then start the capture loop.
- On `ended`: set `capturing = false`, store frames in `framesRef.current`, `setFramesReady(true)`.
- If `readyState >= 1`, invoke `onLoaded()` immediately.
- Cleanup: cancel raf + remove listeners.

**Effect 2 — Boomerang render:**
- When `framesReady` true, grab `displayCanvasRef`, set its `width/height` from `frames[0]`.
- Variables: `index = 0`, `direction = 1`, `last = http://performance.now()`, `interval = 1000/30`.
- In an `requestAnimationFrame(render)` loop: if `now - last >= interval`, draw `frames[index]`, advance `index += direction`. When `index >= frames.length - 1`, clamp and flip to `-1`. When `index <= 0`, clamp and flip to `+1`.
- Cleanup: cancelAnimationFrame.

**Effect 3 — Parallax mouse tracking (gsap):**
- `strength = 20`. Track `targetX/Y`, smoothly lerp `currentX/Y += (target - current) * 0.06` each frame.
- On `mousemove`: `targetX = ((clientX - cx)/cx) * strength` (same for Y).
- Each frame: `gsap.set(videoBgRef.current, { x: currentX, y: currentY })`.

**JSX structure:**
Root: `<div className="min-h-screen bg-black text-white font-body overflow-x-hidden">`

1. **Video background layer:** `<div ref={videoBgRef} className="fixed top-0 left-0 w-full h-full z-0 scale-[1.08] origin-center">` containing:
   - `<video>` with `src={VIDEO_SRC}`, `muted`, `playsInline`, `preload="auto"`, `crossOrigin="anonymous"`, `className="w-full h-full object-cover"`, `style={{ display: framesReady ? 'none' : 'block' }}`.
   - `<canvas ref={displayCanvasRef} className="w-full h-full object-cover" style={{ display: framesReady ? 'block' : 'none' }}>`.

2. **Hero title:** fixed div, `left-0 right-0 z-20 w-full px-4`, `style={{ top: '126px' }}`, fades in via `transition-all duration-1000` toggling `opacity-100 translate-y-0` vs `opacity-0 translate-y-6` based on `mounted`. Inside: `<h1 className="hero-title select-none">MicroVisuals</h1>`.

3. **Nav:** `<nav className="fixed top-5 left-1/2 -translate-x-1/2 z-50 whitespace-nowrap">` containing a `liquid-glass flex items-center gap-6 rounded px-4 py-2.5` pill:
   - `<LogoMark />`
   - `<div className="flex items-center gap-5">` of `NAV_LINKS` as `<a>` with classes `text-sm font-body font-light text-white/70 hover:text-white transition-colors duration-200`.
   - Right cluster `flex items-center gap-3 ml-4`: "Sign in" link (same style), then "Try it free" with `liquid-glass-strong text-sm font-body font-medium text-white rounded px-4 py-1.5 transition-all duration-200 hover:scale-[1.04] hover:shadow-[0_0_16px_2px_rgba(255,255,255,0.12)] active:scale-[0.97]`.

4. **Bottom row:** fixed, `bottom-12 left-0 right-0 px-10 flex items-end justify-between z-20`, fade-in with `transition-all duration-1000 delay-300`.
   - Left `<p>`: `text-sm font-body font-light text-white/75 max-w-[220px] leading-relaxed`, text: "Forma's AI understands context, composition, and style like a creative director would."
   - Center absolute `left-1/2 -translate-x-1/2 bottom-0 flex items-center gap-3` with two buttons:
     - Primary: `group relative bg-white text-black text-sm font-body font-medium rounded px-6 py-3 overflow-hidden active:scale-[0.97] transition-all duration-200 shadow-[0_0_0_0_rgba(255,255,255,0)] hover:shadow-[0_0_24px_4px_rgba(255,255,255,0.25)] hover:scale-[1.03]`. Contents: `<span className="relative z-10">Start generating</span>` + overlay `<span className="absolute inset-0 bg-gradient-to-b from-white to-white/85 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />`.
     - Secondary: `liquid-glass group text-white text-sm font-body font-medium rounded px-6 py-3 active:scale-[0.97] transition-all duration-200 hover:scale-[1.03] hover:shadow-[inset_0_1px_1px_rgba(255,255,255,0.2),0_0_20px_2px_rgba(255,255,255,0.07)]` — label "See templates".
   - Right `<p>`: same classes as left plus `text-right`, text: "Describe what you see in your head — get images that actually match."

### Notes
- Tailwind default border-radius is overridden to `9999px` (full pill) — every `rounded` in the markup produces pill corners.
- Do NOT use `video.currentTime` to reverse — the boomerang uses the captured `frames[]` array only.
- The video element stays mounted (hidden once `framesReady`) so the canvas keeps drawing snapshots.
```

---

## 86. FAQ CTA

- **Category**: CTA
- **Type**: cta
- **Page Type**: hero
- **ID**: `faq-cta`

```
**PROMPT:**

Build a React + TypeScript + Vite + Tailwind CSS page with a "CTA + FAQ + Footer" section using the **Inter** font. Use `lucide-react` for icons (`ChevronDown`, `ChevronUp`). No other UI libraries.

### Layout

A centered container `max-w-[1100px] w-full mx-auto px-5`, white body (`bg-white text-neutral-900`), applied font: `style={{ fontFamily: "'Inter', sans-serif" }}`. Main section has `py-20 max-[900px]:py-[60px]`.

Inside `<main>`, a two-column grid:
- `grid grid-cols-[1.6fr_1fr] gap-[30px] items-stretch max-[900px]:grid-cols-1 max-[900px]:gap-[60px]`

### Left column — Animated Gradient CTA card

A div with class `c5-animated-gradient rounded-[24px] py-20 px-10 text-white flex flex-col justify-center items-center text-center` and inline `boxShadow: '0 10px 30px rgba(0, 0, 0, 0.05)'`.

Contents:
- `<h2>` — "Ready to Transfer<br/>Without Borders?" with classes `font-normal leading-[1.1] mb-[15px]` and inline `fontSize: '3.5rem', letterSpacing: '-0.03em'`.
- `<p>` — "Send Money Worldwide at the Best Rates" with `text-[0.9rem] mb-[30px] font-normal opacity-85`.
- `<button>` — "Get Started Today", classes `bg-neutral-900 text-white font-semibold cursor-pointer border-none text-[0.95rem] transition-all duration-200 hover:-translate-y-0.5`, inline `padding: '14px 32px', borderRadius: '12px', boxShadow: '0 10px 20px rgba(0,0,0,0.3)'`. On hover, bump shadow to `0 14px 30px rgba(0,0,0,0.4)` via `onMouseEnter`/`onMouseLeave`.

### Animated Gradient CSS (put in `src/index.css` after the Tailwind directives)

Use CSS `@property` declarations so custom properties interpolate smoothly, five radial-gradient blobs that each drift across wide paths AND pulse in size. Fast, looping, respects `prefers-reduced-motion`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@property --c5-x1 { syntax: '<percentage>'; inherits: false; initial-value: 10%; }
@property --c5-y1 { syntax: '<percentage>'; inherits: false; initial-value: 10%; }
@property --c5-x2 { syntax: '<percentage>'; inherits: false; initial-value: 90%; }
@property --c5-y2 { syntax: '<percentage>'; inherits: false; initial-value: 10%; }
@property --c5-x3 { syntax: '<percentage>'; inherits: false; initial-value: 10%; }
@property --c5-y3 { syntax: '<percentage>'; inherits: false; initial-value: 90%; }
@property --c5-x4 { syntax: '<percentage>'; inherits: false; initial-value: 90%; }
@property --c5-y4 { syntax: '<percentage>'; inherits: false; initial-value: 90%; }
@property --c5-x5 { syntax: '<percentage>'; inherits: false; initial-value: 50%; }
@property --c5-y5 { syntax: '<percentage>'; inherits: false; initial-value: 50%; }
@property --c5-s1 { syntax: '<percentage>'; inherits: false; initial-value: 55%; }
@property --c5-s2 { syntax: '<percentage>'; inherits: false; initial-value: 55%; }
@property --c5-s3 { syntax: '<percentage>'; inherits: false; initial-value: 55%; }
@property --c5-s4 { syntax: '<percentage>'; inherits: false; initial-value: 55%; }
@property --c5-s5 { syntax: '<percentage>'; inherits: false; initial-value: 65%; }

.c5-animated-gradient {
  background-color: #ff8e53;
  background-image:
    radial-gradient(circle at var(--c5-x1) var(--c5-y1), #fff1aa 0px, transparent var(--c5-s1)),
    radial-gradient(circle at var(--c5-x2) var(--c5-y2), #ff4b2b 0px, transparent var(--c5-s2)),
    radial-gradient(circle at var(--c5-x3) var(--c5-y3), #8aff8a 0px, transparent var(--c5-s3)),
    radial-gradient(circle at var(--c5-x4) var(--c5-y4), #ffd000 0px, transparent var(--c5-s4)),
    radial-gradient(circle at var(--c5-x5) var(--c5-y5), #ff1493 0px, transparent var(--c5-s5));
  animation:
    c5-blob1 5s ease-in-out infinite,
    c5-blob2 6s ease-in-out infinite,
    c5-blob3 5.5s ease-in-out infinite,
    c5-blob4 6.5s ease-in-out infinite,
    c5-blob5 4s ease-in-out infinite,
    c5-size1 3.5s ease-in-out infinite,
    c5-size2 4.2s ease-in-out infinite,
    c5-size3 3.8s ease-in-out infinite,
    c5-size4 4.6s ease-in-out infinite,
    c5-size5 3s ease-in-out infinite;
}

@keyframes c5-blob1 {
  0%,100% { --c5-x1: 5%;  --c5-y1: 5%;  }
  25%     { --c5-x1: 45%; --c5-y1: 20%; }
  50%     { --c5-x1: 30%; --c5-y1: 55%; }
  75%     { --c5-x1: 0%;  --c5-y1: 30%; }
}
@keyframes c5-blob2 {
  0%,100% { --c5-x2: 95%; --c5-y2: 5%;  }
  33%     { --c5-x2: 55%; --c5-y2: 35%; }
  66%     { --c5-x2: 80%; --c5-y2: 65%; }
}
@keyframes c5-blob3 {
  0%,100% { --c5-x3: 5%;  --c5-y3: 95%; }
  40%     { --c5-x3: 45%; --c5-y3: 65%; }
  70%     { --c5-x3: 25%; --c5-y3: 100%; }
}
@keyframes c5-blob4 {
  0%,100% { --c5-x4: 95%; --c5-y4: 95%; }
  30%     { --c5-x4: 60%; --c5-y4: 70%; }
  60%     { --c5-x4: 100%; --c5-y4: 50%; }
}
@keyframes c5-blob5 {
  0%,100% { --c5-x5: 50%; --c5-y5: 50%; }
  25%     { --c5-x5: 70%; --c5-y5: 30%; }
  50%     { --c5-x5: 40%; --c5-y5: 70%; }
  75%     { --c5-x5: 30%; --c5-y5: 40%; }
}

@keyframes c5-size1 { 0%,100% { --c5-s1: 45%; } 50% { --c5-s1: 80%; } }
@keyframes c5-size2 { 0%,100% { --c5-s2: 45%; } 50% { --c5-s2: 85%; } }
@keyframes c5-size3 { 0%,100% { --c5-s3: 45%; } 50% { --c5-s3: 78%; } }
@keyframes c5-size4 { 0%,100% { --c5-s4: 45%; } 50% { --c5-s4: 82%; } }
@keyframes c5-size5 { 0%,100% { --c5-s5: 50%; } 50% { --c5-s5: 85%; } }

@media (prefers-reduced-motion: reduce) {
  .c5-animated-gradient { animation: none; }
}
```

### Right column — FAQ accordion

State: `const [activeIndex, setActiveIndex] = useState<number | null>(0);` with toggle function.

FAQ data array (in order):
1. Q: "What is the maximum amount I can send?" — A: "Transfer limits depend on your verification level and country. You can check your limits inside your account settings."
2. Q: "Does my recipient need an account?" — A: "No, your recipient doesn't need an account. Funds can be sent directly to their bank account or mobile wallet."
3. Q: "Is there a mobile app available?" — A: "Yes, our mobile app is available on both iOS and Android for easy transfers on the go."
4. Q: "Can I cancel a transfer?" — A: "Transfers can be cancelled if they have not yet been processed by the receiving bank. Check your transfer status for options."
5. Q: "What currencies are supported?" — A: "We support over 50 currencies worldwide. You can view the full list of supported currencies in our app or website."

Container: `flex flex-col justify-center gap-3`.

Each item: clickable div, `bg-white border rounded-[10px] py-[18px] px-5 cursor-pointer transition-all duration-200`, border color `#eaeaea` when active else `#f0f0f0` (+ `hover:border-[#eaeaea]`). Box shadow `0 4px 12px rgba(0,0,0,0.04)` when active, else `0 2px 8px rgba(0,0,0,0.02)`.

Row: `flex justify-between items-center font-normal text-[0.9rem] text-neutral-900`, question on left, `ChevronUp` (size 20) if active else `ChevronDown`.

When active, answer block below: `mt-3 text-[0.9rem] text-[#666] leading-[1.6]`.

### Footer

`<footer className="bg-[#fafafa] pt-20 pb-5 max-[900px]:pt-[60px]">`, container `max-w-[1100px] w-full mx-auto px-5`.

Grid: `grid grid-cols-[2fr_1fr_1fr_2fr] gap-10 mb-[50px] max-[900px]:grid-cols-2 max-[480px]:grid-cols-1`.

1. **Logo column**: `<img src="https://pub-f170a2592d2c4a1485466404c36807be.r2.dev/Tests/logoipsum-415.svg" className="h-6 mb-[15px]" style={{ filter: 'brightness(0)' }}/>` then `<p className="text-[0.85rem] text-[#888] leading-[1.6] max-w-[220px]">Reliable transfers that always reach their destination on time.</p>`.
2. **Navigation**: `<h4 className="font-semibold mb-5 text-[0.95rem] text-neutral-900">Navigation</h4>` + `<ul>` of `Features, Benefits, Testimonials, Pricing` — each `<li className="mb-3">` with `<a href="#" className="text-[#888] no-underline text-[0.85rem] transition-colors duration-200 hover:text-neutral-900">`.
3. **Pages**: same styling, items `Home, Contact, 404`.
4. **Newsletter**: heading "Newsletter", p: "Join our newsletter and get notified." (`text-[0.85rem] text-[#888] mb-[15px]`), then `flex gap-[10px]`:
   - Input: `type="email"`, placeholder "Enter your email...", classes `flex-grow border border-[#f0f0f0] bg-white outline-none transition-colors duration-200 focus:border-[#ccc] text-[0.9rem]`, inline `padding: '12px 16px', borderRadius: '10px', boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.02)'`.
   - Button "Subscribe": `bg-neutral-900 text-white border-none font-semibold cursor-pointer transition-all duration-200 hover:-translate-y-0.5 text-[0.9rem]`, inline `padding: '12px 28px', borderRadius: '10px', boxShadow: '0 12px 24px rgba(0,0,0,0.4)'`.

Bottom bar: `border-t border-[#f0f0f0] pt-[25px] pb-[10px] flex justify-between text-[0.85rem] text-[#888] max-[480px]:flex-col max-[480px]:gap-[15px] max-[480px]:items-center` containing "All rights reserved. © 2025" and "Designed by Peter Design".

### Font loading

Add to `index.html` `<head>`: Google Fonts Inter preconnect + stylesheet link:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Notes

- Gradient uses five colors: base `#ff8e53`, blobs `#fff1aa`, `#ff4b2b`, `#8aff8a`, `#ffd000`, `#ff1493`.
- Animation uses CSS `@property` for GPU-friendly custom-property interpolation — this is the modern standard for animated CSS gradients (no JS, no canvas).
- Blobs travel wide paths and pulse in radius; durations 3–6.5s, each offset for organic motion.
```

---

## 87. Vision Reveal

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `vision-reveal`

```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Creative Studio Showcase</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
* { font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }

html, body {
  margin: 0; padding: 0;
  background: #E4E4E4;
  color: #F4F1E8;
  overflow-x: hidden;
  scroll-behavior: smooth;
}

/* ===== SPLASH ===== */
.splash {
  position: fixed; inset: 0;
  width: 100vw; height: 100vh;
  z-index: 9999;
  pointer-events: none;
  overflow: hidden;
  animation: splashHide 0.3s ease forwards;
  animation-delay: 1.35s;
}
.splash-row { display: flex; width: 100%; height: 50%; }
.splash-box { width: 20%; height: 100%; background: #75C5DE; }
.splash-row-top .splash-box { animation: splashTop 1s cubic-bezier(0.96,-0.02,0.38,1.01) forwards; }
.splash-row-bottom .splash-box { animation: splashBottom 1s cubic-bezier(0.96,-0.02,0.38,1.01) forwards; }
.splash-box:nth-child(1) { animation-delay: 0s; }
.splash-box:nth-child(2) { animation-delay: 0.05s; }
.splash-box:nth-child(3) { animation-delay: 0.1s; }
.splash-box:nth-child(4) { animation-delay: 0.15s; }
.splash-box:nth-child(5) { animation-delay: 0.2s; }

@keyframes splashTop { from { transform: translateY(0%); } to { transform: translateY(-100%); } }
@keyframes splashBottom { from { transform: translateY(0%); } to { transform: translateY(100%); } }
@keyframes splashHide { to { opacity: 0; visibility: hidden; } }

/* ===== HERO IMAGE ENTRANCE ===== */
@keyframes heroImageIn {
  from { opacity: 0; transform: scale(1.5) rotate(3deg); }
  to { opacity: 1; transform: scale(1) rotate(0deg); }
}
.hero-image-animate {
  animation: heroImageIn 1.2s cubic-bezier(0.25,0.46,0.45,0.94) forwards;
  animation-delay: 1s;
  opacity: 0;
}

/* ===== WORD REVEAL ===== */
@keyframes wordReveal {
  from { opacity: 0; transform: translateY(10px); filter: blur(10px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.word-reveal {
  opacity: 0;
  display: inline-block;
  margin-right: 0.3em;
  animation: wordReveal 0.4s ease forwards;
}

/* ===== CTA ENTRANCE ===== */
@keyframes slideUpScale {
  from { opacity: 0; transform: translateY(60px) scale(0.4); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.cta-animate {
  opacity: 0;
  animation: slideUpScale 0.8s cubic-bezier(0.25,0.46,0.45,0.94) forwards;
  animation-delay: 1s;
}

/* ===== CTA BUTTON ===== */
.cta-btn { position: relative; overflow: hidden; display: flex; align-items: center; border: none; background: none; cursor: pointer; border-radius: 9999px; padding: 8px; gap: 12px; }
.cta-btn-bg {
  position: absolute; top: 5px; bottom: 5px; left: 8px;
  width: calc(100% - 8px - 8px - 48px - 12px);
  border-radius: 9999px; background: white; z-index: 0;
  transition: width 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
}
@media (min-width: 768px) { .cta-btn-bg { width: calc(100% - 8px - 8px - 54px - 12px); } }
.cta-btn:hover .cta-btn-bg { width: calc(100% - 16px); }
.cta-btn-text { position: relative; z-index: 1; color: #111111; font-weight: 500; font-size: 16px; padding: 12px 32px; white-space: nowrap; }
@media (min-width: 768px) { .cta-btn-text { font-size: 18px; padding: 16px 40px; } }
.cta-btn-circle {
  position: relative; z-index: 1; display: flex; align-items: center; justify-content: center;
  width: 48px; height: 48px; border-radius: 50%; background: #75C5DE; flex-shrink: 0;
  transition: transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
}
@media (min-width: 768px) { .cta-btn-circle { width: 54px; height: 54px; } }
.cta-btn:hover .cta-btn-circle { transform: translateX(-7px); }

/* ===== MENU CTA (smaller) ===== */
.menu-cta-btn { position: relative; overflow: hidden; display: flex; align-items: center; border: none; background: none; cursor: pointer; border-radius: 9999px; padding: 6px; gap: 8px; }
.menu-cta-bg {
  position: absolute; top: 5px; bottom: 5px; left: 8px;
  width: calc(100% - 8px - 8px - 38px - 8px);
  border-radius: 9999px; background: white; z-index: 0;
  transition: width 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
}
.menu-cta-btn:hover .menu-cta-bg { width: calc(100% - 12px); }
.menu-cta-text { position: relative; z-index: 1; color: #111111; font-weight: 500; font-size: 14px; padding: 8px 40px; white-space: nowrap; }
.menu-cta-circle {
  position: relative; z-index: 1; display: flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; border-radius: 50%; background: #75C5DE; flex-shrink: 0;
  transition: transform 0.3s ease;
}
.menu-cta-btn:hover .menu-cta-circle { transform: translateX(-4px); }

/* ===== CREATOR TEXT ===== */
@keyframes creatorSlideUp { from { transform: translateY(330px); } to { transform: translateY(0); } }
.creator-text-animate {
  transform: translateY(330px);
  animation: creatorSlideUp 1s cubic-bezier(0.16,1,0.3,1) forwards;
  animation-delay: 1.5s;
}

/* ===== NAVIGATION ===== */
.logo-wrapper {
  position: fixed; top: 30px; left: 0; width: 50%; z-index: 10;
  display: flex; justify-content: flex-start; align-items: center; mix-blend-mode: difference;
}
@media (min-width: 768px) { .logo-wrapper { top: 40px; } }
.logo-wrapper .inner { padding-left: 20px; }
@media (min-width: 768px) { .logo-wrapper .inner { padding-left: 40px; } }
.logo-wrapper img { width: 32px; height: 32px; }

.burger-wrapper {
  position: fixed; top: 16px; right: 0; width: 50%; z-index: 10;
  display: flex; justify-content: flex-end; align-items: center;
}
@media (min-width: 768px) { .burger-wrapper { top: 27px; } }
.burger-wrapper .inner { padding-right: 20px; }
@media (min-width: 768px) { .burger-wrapper .inner { padding-right: 40px; } }

.burger-btn {
  width: 59px; height: 59px; border-radius: 50%; border: none; cursor: pointer;
  display: flex; flex-direction: column; gap: 4px; align-items: center; justify-content: center;
  background: #F4F1E8; transition: background 0.4s ease;
}
.burger-btn:hover { background: #0B0B0B; }
.burger-btn .bar {
  display: block; width: 24px; height: 2px; background: #111111;
  transition: all 0.3s ease;
}
.burger-btn:hover .bar { background: #F4F1E8; }
.burger-btn.open { background: #0B0B0B; }
.burger-btn.open .bar { background: #F4F1E8; }
.burger-btn.open .bar:first-child { transform: rotate(45deg) translate(2px, 2px); }
.burger-btn.open .bar:last-child { transform: rotate(-45deg) translate(2px, -2px); }

/* ===== MENU PANEL ===== */
.menu-panel {
  position: fixed; z-index: 9;
  left: 8px; right: 8px;
  border-radius: 20px;
  background: rgba(17,17,17,0.95);
  backdrop-filter: blur(26px); -webkit-backdrop-filter: blur(26px);
  padding: 90px 32px 32px 32px;
  display: flex; flex-direction: column; justify-content: space-between;
  transition: top 0.5s cubic-bezier(0.25,0.46,0.45,0.94), opacity 0.4s ease;
  top: -600px; opacity: 0; pointer-events: none;
}
@media (min-width: 768px) {
  .menu-panel { left: auto; right: 7px; width: 420px; padding: 60px; }
}
.menu-panel.open { top: 0; opacity: 1; pointer-events: auto; }
@media (min-width: 768px) { .menu-panel.open { top: 7px; } }

.menu-panel nav { display: flex; flex-direction: column; gap: 8px; }
.menu-panel nav a {
  color: #F4F1E8; font-size: 36px; font-weight: 500; text-decoration: none;
  line-height: 130%; transition: opacity 0.3s ease;
}
@media (min-width: 768px) { .menu-panel nav a { font-size: 42px; } }
.menu-panel nav a:hover { opacity: 0.7; }

.menu-contact { display: flex; flex-direction: column; gap: 20px; margin-top: 32px; }
.menu-email { color: #9A9590; font-size: 18px; text-decoration: none; transition: color 0.3s ease; }
@media (min-width: 768px) { .menu-email { font-size: 20px; } }
.menu-email:hover { color: #F4F1E8; }
.menu-socials { display: flex; gap: 24px; }
.menu-socials a {
  color: #9A9590; font-size: 14px; text-decoration: underline;
  text-underline-offset: 2px; transition: color 0.3s ease;
}
.menu-socials a:hover { color: #F4F1E8; }

/* ===== HERO ===== */
.hero {
  position: relative; width: 100%; overflow: hidden;
  background: #E4E4E4; min-height: 100vh;
}
@media (min-width: 768px) { .hero { height: 100vh; min-height: 800px; } }

.hero-big-text {
  position: absolute; bottom: -30px; left: 0; right: 0; z-index: 2;
  pointer-events: none; width: 100%; text-align: center;
}
@media (min-width: 768px) { .hero-big-text { bottom: -40px; } }
.hero-big-text h2 {
  font-weight: 500; color: #F4F1E8; line-height: 80%;
  letter-spacing: -0.04em; white-space: nowrap;
  font-size: clamp(180px, 28vw, 560px);
}

.hero-base-img {
  position: absolute; top: 30vh; left: 0; right: 0; bottom: 0;
  background-size: cover; background-repeat: no-repeat;
  background-position: 60% center; z-index: 5;
}
@media (min-width: 768px) { .hero-base-img { top: 0; background-position: center; } }

.hero-reveal-img {
  position: absolute; top: 30vh; left: 0; right: 0; bottom: 0;
  background-size: cover; background-repeat: no-repeat;
  background-position: 60% center; z-index: 7; pointer-events: none;
}
@media (min-width: 768px) { .hero-reveal-img { top: 0; background-position: center; } }

.hero-content {
  position: relative; z-index: 8;
  display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start;
  width: 100%; max-width: 1600px; margin: 0 auto;
  padding: 110px 16px 24px 16px; pointer-events: none;
}
@media (min-width: 768px) {
  .hero-content {
    position: absolute; inset: 0;
    justify-content: space-between;
    padding: 160px 40px 100px 40px;
  }
}
.hero-content-inner { display: flex; flex-direction: column; align-items: flex-start; gap: 30px; width: 100%; pointer-events: auto; }

.hero-headline {
  font-size: 22px; font-weight: 500; line-height: 120%;
  letter-spacing: -0.02em; color: #111111; max-width: 447px;
}
@media (min-width: 768px) { .hero-headline { font-size: 28px; } }

/* ===== CANVAS (hidden) ===== */
#reveal-canvas { display: none; position: absolute; inset: 0; pointer-events: none; }

/* ===== REDUCED MOTION ===== */
@media (prefers-reduced-motion: reduce) {
  .splash { animation: splashHide 0.01s linear forwards; }
  .splash-box { animation: none !important; }
  .hero-image-animate, .word-reveal, .cta-animate, .creator-text-animate {
    animation: none !important; opacity: 1 !important;
    transform: none !important; filter: none !important; visibility: visible !important;
  }
}
</style>
</head>
<body>

<!-- SPLASH -->
<div class="splash" id="splash">
  <div class="splash-row splash-row-top">
    <div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div>
  </div>
  <div class="splash-row splash-row-bottom">
    <div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div><div class="splash-box"></div>
  </div>
</div>

<!-- LOGO -->
<div class="logo-wrapper">
  <div class="inner">
    <a href="/" aria-label="Home">
      <img src="https://framerusercontent.com/images/VMcS7YYTM5PXfXvlHc9u3hSCMM.svg" alt=""/>
    </a>
  </div>
</div>

<!-- BURGER -->
<div class="burger-wrapper">
  <div class="inner">
    <button class="burger-btn" id="burger-btn" aria-label="Open menu">
      <span class="bar"></span>
      <span class="bar"></span>
    </button>
  </div>
</div>

<!-- MENU PANEL -->
<div class="menu-panel" id="menu-panel">
  <nav>
    <a href="#work">Work</a>
    <a href="#about">About</a>
    <a href="#blog">Blog</a>
  </nav>
  <div class="menu-contact">
    <a href="mailto:studio@norakessler.com" class="menu-email">studio@norakessler.com</a>
    <div class="menu-socials">
      <a href="#">Pinterest</a>
      <a href="#">Behance</a>
      <a href="#">Letterboxd</a>
    </div>
  </div>
  <div style="margin-top:32px;">
    <button class="menu-cta-btn">
      <span class="menu-cta-bg"></span>
      <span class="menu-cta-text">Let's talk</span>
      <span class="menu-cta-circle">
        <svg width="14" height="14" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 13L13 5M13 5H6M13 5V12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
    </button>
  </div>
</div>

<!-- HERO -->
<main class="hero">
  <!-- Big text behind image -->
  <div class="hero-big-text creator-text-animate">
    <h2>Visuals</h2>
  </div>

  <!-- Base image -->
  <div class="hero-base-img hero-image-animate"
       style="background-image:url('https://soft-zoom-63098134.figma.site/_assets/v11/5c9f982199fde1d9b85a20e5396f0fa7bacaf9a3.png?w=2560');">
  </div>

  <!-- Reveal layer -->
  <canvas id="reveal-canvas"></canvas>
  <div class="hero-reveal-img" id="reveal-img"
       style="background-image:url('https://soft-zoom-63098134.figma.site/_assets/v11/6be2165e31648955b4e071f4cf2a50bc572b9bfd.png?w=1536');">
  </div>

  <!-- Content -->
  <div class="hero-content">
    <div class="hero-content-inner">
      <h1 class="hero-headline" id="headline"></h1>
      <button class="cta-btn cta-animate">
        <span class="cta-btn-bg"></span>
        <span class="cta-btn-text">Start a project now</span>
        <span class="cta-btn-circle">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 13L13 5M13 5H6M13 5V12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </button>
    </div>
  </div>
</main>

<script>
(function() {
  // Word reveal
  const headline = document.getElementById('headline');
  const text = "I build compelling visual stories & motion that make ideas shine.";
  const words = text.split(' ');
  words.forEach(function(word, i) {
    const span = document.createElement('span');
    span.className = 'word-reveal';
    span.textContent = word;
    span.style.animationDelay = (1 + i * 0.05) + 's';
    headline.appendChild(span);
  });

  // Burger menu toggle
  const burgerBtn = document.getElementById('burger-btn');
  const menuPanel = document.getElementById('menu-panel');
  let menuOpen = false;
  burgerBtn.addEventListener('click', function() {
    menuOpen = !menuOpen;
    if (menuOpen) {
      burgerBtn.classList.add('open');
      menuPanel.classList.add('open');
      burgerBtn.setAttribute('aria-label', 'Close menu');
    } else {
      burgerBtn.classList.remove('open');
      menuPanel.classList.remove('open');
      burgerBtn.setAttribute('aria-label', 'Open menu');
    }
  });
  // Close menu on nav link click
  menuPanel.querySelectorAll('nav a').forEach(function(a) {
    a.addEventListener('click', function() {
      menuOpen = false;
      burgerBtn.classList.remove('open');
      menuPanel.classList.remove('open');
    });
  });

  // Spotlight reveal
  const SPOTLIGHT_R = 260;
  const canvas = document.getElementById('reveal-canvas');
  const imgLayer = document.getElementById('reveal-img');
  const ctx = canvas.getContext('2d');

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const mouse = { x: -999, y: -999 };
  const smooth = { x: -999, y: -999 };

  window.addEventListener('mousemove', function(e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  function loop() {
    smooth.x += (mouse.x - smooth.x) * 0.1;
    smooth.y += (mouse.y - smooth.y) * 0.1;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var grad = ctx.createRadialGradient(smooth.x, smooth.y, 0, smooth.x, smooth.y, SPOTLIGHT_R);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.4, 'rgba(255,255,255,1)');
    grad.addColorStop(0.6, 'rgba(255,255,255,0.75)');
    grad.addColorStop(0.75, 'rgba(255,255,255,0.4)');
    grad.addColorStop(0.88, 'rgba(255,255,255,0.12)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');

    ctx.beginPath();
    ctx.arc(smooth.x, smooth.y, SPOTLIGHT_R, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    var dataUrl = canvas.toDataURL();
    imgLayer.style.webkitMaskImage = 'url(' + dataUrl + ')';
    imgLayer.style.maskImage = 'url(' + dataUrl + ')';
    imgLayer.style.webkitMaskSize = '100% 100%';
    imgLayer.style.maskSize = '100% 100%';

    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
```

---

## 88. Rocket Pricing

- **Category**: Pricing
- **Type**: pricing
- **Page Type**: hero
- **ID**: `rocket-pricing`

```
Build a `PricingSection` React component that matches the spec below exactly.

## Stack & global setup

- React 18 + Vite + TypeScript, TailwindCSS, `framer-motion`, `clsx` + `tailwind-merge` exposed as `cn()` from `@/lib/utils`.
- Dark theme. Page background `#000000`. Font: Inter (`font-inter`). Icons: Google **Material Symbols Outlined** (loaded globally).
- Tailwind config must include semantic HSL tokens plus:
  ```ts
  theme.extend.colors.landing = {
    surface: "rgba(255,255,255,0.10)",
    "surface-hover": "rgba(255,255,255,0.16)",
    border: "rgba(255,255,255,0.10)",
  }
  ```
- `--background` / `--foreground` HSL tokens drive `bg-background` (dark) and `text-foreground` (near-white).

## Helper components (reuse exact behavior)

### `MIcon`
Material Symbols span. Props: `name`, `size=20`, `weight=400`, `fill=0`, `grade=0`, `opticalSize=24`, `className`.
```tsx
<span
  className={cn("material-symbols-outlined select-none leading-none", className)}
  style={{
    fontSize: size,
    fontVariationSettings: `'FILL' ${fill}, 'wght' ${weight}, 'GRAD' ${grade}, 'opsz' ${opticalSize}`,
  }}
>{name}</span>
```

### `FadeUp`
`framer-motion` wrapper: `initial={{opacity:0, y:24}}`, `whileInView={{opacity:1, y:0}}`, `viewport={{once:true, amount:0.3}}`, `transition={{duration:0.6, delay, ease:[0.22,1,0.36,1]}}`. Props: `children`, `delay=0`, `className`.

### `SpotlightBorder`
1px gradient border that follows the cursor via CSS masks.
- Props: `children`, `className`, `radius="2xl"`, `size=520`, `intensity=0.5`.
- Wrapper sets CSS vars `--spot-x`, `--spot-y` (default `-9999px`) updated on `pointermove` relative to element.
- Two stacked layers using `-webkit-mask` + `mask` `linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)` with `mask-composite: exclude` to produce a 1px ring; the ring is painted with `radial-gradient(circle var(--size) at var(--spot-x) var(--spot-y), rgba(255,255,255, var(--intensity)), transparent 60%)`.
- Outer ring: `rounded-2xl border border-white/10`. Inner highlight ring: thinner, brighter on hover. Pointer events on inner content only.

### `PrimaryButton` / `SecondaryButton`
- Both: `inline-flex items-center justify-center rounded-full`, Inter, leading-none, hover text-up-from-below animation (`AnimatedText`).
- PrimaryButton: `bg-white/80 hover:bg-white text-black`. Size `sm` = `h-8 px-4 text-sm`.
- SecondaryButton: `bg-landing-surface hover:bg-landing-surface-hover border border-landing-border text-foreground backdrop-blur-[2.5px] font-medium`. Size `sm` = `h-8 px-4 text-sm`.

## Section structure — `PricingSection`

```tsx
<section id="pricing" className="relative w-full bg-background py-12 sm:py-16">
  <div className="mx-auto max-w-[1080px] px-4 sm:px-6">
    {/* HEADER */}
    <div className="mb-14 flex flex-col items-start gap-10 lg:flex-row lg:items-end lg:justify-between">
      <div className="max-w-2xl">
        <FadeUp>
          <span className="mb-6 inline-flex items-center gap-2 rounded-full bg-landing-surface border border-white/10 px-3 py-1 text-xs text-foreground/80 backdrop-blur">
            <span className="h-1.5 w-1.5 rounded-full bg-foreground/70" />
            Pricing
          </span>
        </FadeUp>
        <FadeUp delay={0.1}>
          <h2 className="text-3xl sm:text-4xl font-normal tracking-[-0.02em] leading-[1.05] text-foreground">
            Clear pricing plans
            <br className="hidden sm:block" /> that scale with you.
          </h2>
        </FadeUp>
      </div>
      <FadeUp delay={0.2}>
        <p className="max-w-sm text-sm sm:text-base text-foreground/60">
          One-time payment. Lifetime access. Pick the plan that fits how far
          you want to go.
        </p>
      </FadeUp>
    </div>

    {/* CARDS */}
    <div className="mx-auto grid max-w-3xl grid-cols-1 gap-6 md:grid-cols-2">
      {plans.map(p => <PricingCard key={p.name} plan={p} />)}
    </div>
  </div>
</section>
```

## Plans data (exact)

```ts
type Feature = { text: string; included: boolean };
type Plan = {
  name: string; price: string; originalPrice?: string; description: string;
  features: Feature[]; featured?: boolean; badge?: string; bg: string;
};

const plans: Plan[] = [
  {
    name: "Course",
    price: "159", originalPrice: "497",
    description: "Once. Lifetime. 68% off.",
    bg: "#161616",
    features: [
      { text: "All courses and videos", included: true },
      { text: "All modules. Lifetime access.", included: true },
      { text: "AI Builder", included: true },
      { text: "Unlimited Templates", included: false },
      { text: "Unlimited Motion Videos", included: false },
    ],
  },
  {
    name: "Course + Lovable Templates",
    price: "239", originalPrice: "697",
    description: "Once. Lifetime. Best deal.",
    bg: "#252525",
    features: [
      { text: "All courses and videos", included: true },
      { text: "All modules. Lifetime access.", included: true },
      { text: "AI Builder", included: true },
      { text: "Unlimited Templates", included: true },
      { text: "Unlimited Motion Videos", included: true },
    ],
    featured: true,
    badge: "Best Value",
  },
];
```

## `PricingCard`

```tsx
<SpotlightBorder radius="2xl" size={460} intensity={0.5}
  className="relative h-full p-2 sm:p-3">
  <div
    className="relative flex h-full flex-col rounded-2xl border border-white/10 p-7 sm:p-8"
    style={{ backgroundColor: plan.bg }}
  >
    {plan.badge && (
      <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full border border-white/15 bg-white px-3 py-1 text-xs font-medium text-black">
        {plan.badge}
      </div>
    )}

    <FadeUp delay={0}>
      <div className="text-[11px] uppercase tracking-[0.2em] text-foreground/60">
        {plan.name}
      </div>
    </FadeUp>
    <div className="mt-3 border-t border-white/10" />

    <FadeUp delay={0.1}>
      <div className="mt-10 flex items-baseline gap-2">
        <span className="text-[2.75rem] leading-none font-normal tracking-tight text-foreground">${plan.price}</span>
        {plan.originalPrice && (
          <span className="text-lg text-foreground/40 line-through">${plan.originalPrice}</span>
        )}
      </div>
    </FadeUp>

    <FadeUp delay={0.2}>
      <p className="mt-4 text-sm leading-relaxed text-foreground/60">{plan.description}</p>
    </FadeUp>

    <FadeUp delay={0.3}>
      <div className="mt-7">
        {plan.featured
          ? <PrimaryButton href="/auth?mode=signup" size="sm">Get Started</PrimaryButton>
          : <SecondaryButton href="/auth?mode=signup" size="sm">Get Started</SecondaryButton>}
      </div>
    </FadeUp>

    <FadeUp delay={0.4}>
      <ul className="mt-7 flex flex-1 flex-col gap-2">
        {plan.features.map((f, i) => (
          <li key={f.text}
            className={cn(
              "flex items-center gap-3 py-4 text-sm",
              i !== 0 && "border-t border-white/10",
              f.included ? "text-foreground/85" : "text-foreground/40"
            )}>
            <span className={cn(
              "flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full border",
              f.included ? "border-white/20 bg-white/[0.06]" : "border-white/10 bg-transparent"
            )}>
              {f.included
                ? <MIcon name="check" size={12} className="text-foreground" />
                : <MIcon name="close" size={12} className="text-foreground/50" />}
            </span>
            {f.text}
          </li>
        ))}
      </ul>
    </FadeUp>
  </div>
</SpotlightBorder>
```

## Acceptance checklist

- Section id `pricing`, `bg-background`, vertical padding `py-12 sm:py-16`, max width `1080px`.
- Header: pill ("Pricing" with dot), heading "Clear pricing plans / that scale with you." (line break ≥sm), right-aligned paragraph (max-w-sm) on `lg+`. All three with staggered `FadeUp` delays 0, 0.1, 0.2.
- Cards grid: `max-w-3xl mx-auto`, `gap-6`, 1 col → 2 cols at `md`.
- Card 1 bg `#161616`, card 2 bg `#252525` with "Best Value" pill (`-top-3`, white bg, black text), featured uses `PrimaryButton`, other uses `SecondaryButton`.
- `SpotlightBorder` 1px cursor-following ring on each card (size 460, intensity 0.5).
- Card content order: eyebrow (uppercase, `text-[11px] tracking-[0.2em]`), divider, price row (`$2.75rem` + line-through original `text-foreground/40`), description, button, feature list.
- Feature rows: `py-4`, divided by `border-t border-white/10` except first. Included = 20px circle `border-white/20 bg-white/[0.06]` with check; excluded = transparent circle with close, text `text-foreground/40`.
- Inner card `FadeUp` stagger: 0, 0.1, 0.2, 0.3, 0.4.
- Buttons link to `/auth?mode=signup`.
- All colors via HSL tokens / declared landing surface tokens; never hardcode hex outside the two card backgrounds and `#000000`.
```

---

## 89. Tech-Noir About

- **Category**: About
- **Type**: about
- **Page Type**: hero
- **ID**: `tech-noir-about`

```
---

## Prompt

Create a single full-page section with a solid `#FF0000` red background using React 19, TypeScript, Vite, Tailwind CSS v4 (`@tailwindcss/vite`), and `motion` (from `motion/react`).

### Fonts (index.css)

```css
@import url('https://fonts.googleapis.com/css2?family=Italiana&family=Manrope:wght@400;600&family=Marck+Script&display=swap');
@import "tailwindcss";

@theme {
  --font-manrope: "Manrope", sans-serif;
  --font-italiana: "Italiana", serif;
  --font-marck: "Marck Script", cursive;
}
```

### Section Container

```
<section className="relative min-h-screen w-full bg-[#FF0000] flex flex-col z-10">
```

---

### 1. Centered Content

**Outer wrapper:**
```
<div className="flex-1 flex flex-col items-center w-full pt-[100px] md:pt-[400px]">
```

**Inner container:**
```
<div className="flex flex-col items-center w-full px-8 text-center z-20 relative max-w-[900px] h-auto md:h-[620px] mx-auto">
```

**a) Logo SVG** -- white fill, 80x80, `mb-12`:
```tsx
<svg width="80" height="80" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path fillRule="evenodd" clipRule="evenodd" d="M60 120C26.8629 120 0 93.1371 0 60V0C22.5654 0 42.2213 12.4569 52.4662 30.8691C38.4788 34.2089 28.0787 46.7902 28.0787 61.8006V63.1443C28.0787 79.9648 41.7146 93.6006 58.5353 93.6006H59.8789L59.8785 61.8006C59.8785 79.3633 74.1159 93.6006 91.6787 93.6006L91.6787 61.8006C91.6787 44.2783 77.5071 30.0661 60 30.0008L60 0H62.5352C94.2722 0 120 25.7279 120 57.4648V60C120 93.1371 93.1371 120 60 120Z" fill="white"/>
</svg>
```

**b) Mission statement:**
```tsx
<p className="text-white text-[16px] h-[100px] w-full max-w-[400px] leading-[1.6] mb-[40px] uppercase tracking-wider mx-auto">
  We built this platform with a single purpose to eliminate operational chaos and restore balance to your daily business routine
</p>
```

**c) Cursive signature:**
```tsx
<div className="font-marck text-white text-[120px] leading-none mb-[32px]">
  S.P.D
</div>
```

**d) Two paragraphs** (Title Case, font-light):
```tsx
<div className="text-white leading-[1.6] mb-[100px] md:mb-24 w-full flex flex-col items-center font-light">
  <p className="mb-[24px] text-[16px] w-[400px] max-w-full text-center">
    I Was Exhausted By Software That Demanded More Effort Than It Actually Saved. That Is Why We Engineered An Autonomous Architecture That Operates Silently In The Background.
  </p>
  <p className="text-[16px] w-[400px] max-w-full text-center">
    Your Business Should Serve Your Life, Not Consume It. Let Our Algorithms Handle The Heavy Lifting, So You Can Focus On The Vision.
  </p>
</div>
```

---

### 2. Bottom Video with Red Gradient Blend

```tsx
<div className="relative w-full shrink-0">
  <div className="absolute top-0 left-0 w-full h-[100px] bg-gradient-to-b from-[#FF0000] to-transparent z-10 pointer-events-none" />
  <video autoPlay loop muted playsInline className="w-full h-auto block object-contain">
    <source
      src="https://res.cloudinary.com/daklr2whx/video/upload/v1778602552/track-video_2_s9lp53.mp4"
      type="video/mp4"
    />
  </video>
</div>
```

A 100px gradient overlay at the top of the video fades from `#FF0000` to transparent, seamlessly blending the red background into the video. The video uses `object-contain` -- native aspect ratio, full width, no cropping. `shrink-0` prevents flexbox from compressing it.

---

### Asset URL

| Asset | URL |
|---|---|
| Bottom video | `https://res.cloudinary.com/daklr2whx/video/upload/v1778602552/track-video_2_s9lp53.mp4` |

Hosted on **Cloudinary**.
```

---

## 90. Health Portal

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `health-portal`

```
Create a single-page dental clinic landing page using **React + Vite + TypeScript + Tailwind CSS**. No external UI libraries, no icon libraries. Everything lives in one `App.tsx` file. The page has 3 full-screen sections, a splash screen, and a fixed navbar.

---

### SETUP

**Font:** "Open Sauce One" loaded via these exact links in `index.html` `<head>`:
```html
<link href="https://db.onlinewebfonts.com/c/1cd1e7d71e048159076fd90b39846902?family=Open+Sauce+One" rel="stylesheet">
<link href="https://db.onlinewebfonts.com/c/42acf9aa4a6dc2f2886a3f682e337ead?family=Open+Sauce+One+Bold" rel="stylesheet">
```

**Title:** "Dental Health - Quality Healthcare"

**Global CSS (index.css):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html, body, #root {
    height: 100%;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: 'Open Sauce One', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}
```

**Tailwind config:** Default, no extensions. Content: `['./index.html', './src/**/*.{js,ts,jsx,tsx}']`.

---

### IMAGE URLS (use these EXACT URLs)

```ts
const HERO_IMAGE = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_113640_ccf3cf97-d447-425b-a134-d7b09fc743fc.png&w=1280&q=85';

const SECTION2_IMAGE = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_114219_414dfe80-f15c-4e25-bf52-b13721f4bd88.png&w=1280&q=85';

const SECTION3_IMG1 = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_115253_c19ab167-8dd5-48b4-967d-b9f0d9d6e8fb.png&w=1280&q=85';

const SECTION3_IMG2 = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_115237_fc519057-6e87-4abf-999a-9610b8b085b4.png&w=1280&q=85';

const SECTION3_BG = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_114355_752ba9e6-0942-4abb-9047-5d9bb16632e9.png&w=1280&q=85';
```

---

### DATA CONSTANTS

```ts
const featureBars = ['Advanced Dentistry', 'High Quality Equipment', 'Friendly Staff'];

const services = [
  { name: 'Dental\nVeneers', num: '01', active: true },
  { name: 'Dental\nCrowns', num: '02', active: false },
  { name: 'Teeth\nWhitening', num: '03', active: false },
  { name: 'Dental\nImplants', num: null, active: false },
];
```

---

### CORE TECHNICAL CONCEPT: "MASKED CARDS"

Sections 1 and 2 use a single large background image shared across multiple cards. Each card shows a different "window" into the same image, creating a cohesive mosaic effect. Implementation:

**`useMaskPositions` hook:**
- Takes a ref to the section container and a ref to an array of card elements.
- Uses `ResizeObserver` on the section container.
- For each card, computes `{ x, y, sw, sh }` where x/y is the card's top-left offset relative to the section, sw/sh is the section's width/height.

**`useImageWidth` hook:**
- Loads the image in a `new Image()` object.
- Calculates: `renderWidth = img.naturalWidth * (sectionHeight / img.naturalHeight)`.
- Returns how wide the image would be if scaled to fill the section height.

**`MaskedCard` component:**
- Props: `bgImage`, `position` (from useMaskPositions), `imageWidth` (from useImageWidth), `focalX` (0-1 float), `className`, `children`, `cardRef`, `style`.
- Calculates `overflow = imageWidth > position.sw ? imageWidth - position.sw : 0`, then `focalOffset = overflow * focalX`.
- Applies inline style:
  ```
  backgroundImage: url(bgImage)
  backgroundSize: auto [position.sh]px
  backgroundPosition: -[position.x + focalOffset]px -[position.y]px
  backgroundRepeat: no-repeat
  ```
- `focalX` values: Section 1 mobile=0.7, desktop=0.8. Section 2 mobile=0.65, desktop=0.8.

**`useIsMobile` hook:**
- Listens to `window.matchMedia('(max-width: 767px)')` change events.
- Returns boolean.

---

### ANIMATION: `useStaggeredReveal` hook

- Takes `count` (number of elements) and `threshold` (IntersectionObserver threshold, default 0.15).
- Returns `{ containerRef, getAnimStyle }`.
- `containerRef` is attached to the section; when it crosses the threshold, `visible` becomes true (fires once).
- `getAnimStyle(index)` returns:
  ```css
  opacity: visible ? 1 : 0
  transform: visible ? 'translateY(0)' : 'translateY(24px)'
  transition: opacity 0.6s cubic-bezier(0.16,1,0.3,1) [index*120]ms,
              transform 0.6s cubic-bezier(0.16,1,0.3,1) [index*120]ms
  ```

---

### SPLASH SCREEN

- Fixed overlay covering viewport, `z-[100]`, white background.
- Number counter displayed at **bottom-left** (`items-end justify-start`).
- Counter style: `text-7xl md:text-9xl font-bold tabular-nums p-6 md:p-10 leading-none`, black text.
- Counts from 0 to 100 over exactly 2000ms (20ms per step, 100 steps).
- After reaching 100: wait 200ms, then set `exiting=true` which triggers `opacity-0` with `transition-opacity duration-700`.
- After 900ms total from reaching 100, call `onComplete()` which removes splash from DOM.

---

### NAVBAR

**Container:** `fixed top-0 left-0 right-0 z-50`, `flex items-center justify-between`, `px-4 md:px-6 py-2 md:py-3`, `bg-white/80 backdrop-blur-md`.

**Logo (left side):**
- Two lines stacked: "Dental" and "Health"
- Wrapper: `flex flex-col`
- Text: `text-xl md:text-2xl font-extrabold uppercase tracking-tight leading-none`
- Second line has `-mt-1.5 md:-mt-2` for tight spacing
- Below logo text: "quality healthcare" in `text-[8px] md:text-[9px] font-medium leading-none mt-1.5 md:mt-2`

**Desktop nav (hidden on mobile with `hidden md:block`):**
- "Menu" button: `px-6 py-3 bg-white rounded-full border border-black text-sm font-semibold`, hover: `hover:bg-black hover:text-white transition-colors duration-200`
- "Dental Emergency" text: `text-sm font-semibold text-black`

**Mobile hamburger (visible only on mobile with `md:hidden`):**
- Container: `w-10 h-10 flex items-center justify-center`, `relative`
- 3 spans, each: `absolute h-0.5 w-6 bg-black rounded-full`
- Transition: `transition-all duration-300 ease-[cubic-bezier(0.76,0,0.24,1)]`
- Closed state: top span `-translate-y-2`, middle `opacity-100 scale-x-100`, bottom `translate-y-2`
- Open state: top `rotate-45 translate-y-0`, middle `opacity-0 scale-x-0`, bottom `-rotate-45 translate-y-0`

**Mobile menu overlay (`md:hidden`):**
- Outer: `fixed inset-0 z-40`, pointer-events toggled based on open state
- Backdrop: `absolute inset-0 bg-black/20 backdrop-blur-sm`, fades opacity. Clicking closes menu.
- Panel: `absolute top-0 right-0 h-full w-[85%] max-w-sm bg-white shadow-2xl`, slides with `translate-x-0` (open) / `translate-x-full` (closed), `duration-500 ease-[cubic-bezier(0.76,0,0.24,1)]`
- Content: `flex flex-col justify-center h-full px-8 gap-1`
- Nav links: ['Home', 'Services', 'About', 'Gallery', 'Contact']
  - Each: `text-4xl font-bold text-black hover:text-neutral-500`
  - Staggered entrance: `opacity-0 translate-x-8` -> `opacity-100 translate-x-0`, `transitionDelay: ${100 + i * 60}ms` when open
  - `transition-all duration-500 ease-[cubic-bezier(0.76,0,0.24,1)]`
- Bottom section: `mt-8 pt-8 border-t border-neutral-200`, delayed 450ms
  - "Dental Emergency" text: `text-sm font-semibold text-black mb-4`
  - Button: `w-full px-6 py-4 bg-black rounded-full text-white text-sm font-semibold hover:bg-neutral-800 transition-colors duration-200`, text "Book Appointment"
- When open: `document.body.style.overflow = 'hidden'`. Cleanup on unmount.

---

### SECTION 1 - HERO

**Container:** `<section>`, `h-screen w-full overflow-hidden flex flex-col`, `pt-24 md:pt-24 px-3 md:px-5 pb-1.5 md:pb-2 gap-1.5 md:gap-2`

Attach both `section1Ref` and `s1Reveal.containerRef` to this element.

Uses `HERO_IMAGE` as shared background via MaskedCard technique.

**3 Feature Bars** (mapped from `featureBars` array):
- Each is a `MaskedCard` with: `w-full h-14 md:h-20 shrink-0 rounded-xl md:rounded-2xl overflow-hidden relative`
- Animated with `s1Reveal.getAnimStyle(i)` for i=0,1,2
- Content: `<span>` centered vertically and horizontally (`flex items-center justify-center h-full`), `text-black text-lg md:text-3xl font-bold text-center`, `relative z-10`

**Main Hero Card** (4th card, index 3):
- `MaskedCard`: `w-full flex-1 min-h-0 rounded-xl md:rounded-2xl overflow-hidden relative`
- Animated with `s1Reveal.getAnimStyle(3)`
- **Top-left text:** `absolute top-4 left-4 md:top-7 md:left-7`, `text-black text-xs md:text-sm font-semibold leading-4 md:leading-5 max-w-[200px] md:max-w-[300px] z-10`
  - Content: "We wish to provide professional dental services" `<br/>` "that match the current technologies"
- **Bottom-left block:** `absolute bottom-5 left-3 md:bottom-8 md:left-4 z-10`
  - Label: `block text-black text-xs md:text-sm font-semibold mb-1 md:mb-2`, text "Trusted Dentist in West New York"
  - Heading: `<h1>` with `text-black text-[clamp(3rem,11vw,11rem)] font-bold leading-[0.79] tracking-tight`, content: "Dental" `<br/>` "Care"
- **Bottom-right text:** `absolute bottom-6 right-4 md:bottom-10 md:right-8`, `text-white text-xs md:text-sm font-semibold z-10`, content: "Free Consultation"

---

### SECTION 2 - SMILE GALLERY

**Container:** `<section>`, `min-h-screen md:h-screen w-full overflow-hidden flex flex-col`, `pt-1.5 md:pt-2 px-3 md:px-5 pb-1.5 md:pb-2 gap-1.5 md:gap-2`

Attach both `section2Ref` and `s2Reveal.containerRef` to this element.

Uses `SECTION2_IMAGE` as shared background via MaskedCard technique.

**Grid container:** `flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 grid-rows-[auto_auto_auto_auto] md:grid-rows-[1fr_1fr_0.8fr] gap-1.5 md:gap-2`

**Card 0 - Top Left ("Smile Gallery"):**
- `MaskedCard`: `rounded-xl md:rounded-2xl overflow-hidden relative min-h-[160px] md:min-h-0`
- Animated: `s2Reveal.getAnimStyle(0)`
- Heading: `absolute top-4 left-5 md:top-6 md:left-7`, `text-white md:text-black text-2xl md:text-3xl font-bold z-10`, text "Smile Gallery"
- Subtitle: `absolute bottom-4 left-5 md:bottom-6 md:left-7`, `text-white md:text-black text-xs md:text-sm font-semibold z-10`, text "Our cosmetic dental work"

**Card 1 - Top Right (spans 2 rows on desktop):**
- `MaskedCard`: `md:row-span-2 rounded-xl md:rounded-2xl overflow-hidden relative min-h-[200px] md:min-h-0`
- Animated: `s2Reveal.getAnimStyle(1)`
- Text: `absolute bottom-16 left-5 md:bottom-20 md:left-7`, `text-white text-xs md:text-sm font-semibold leading-4 md:leading-5 z-10`, content: "If you want a gorgeous smile," `<br/>` "call us to ask about a smile makeover."
- Button: `absolute bottom-4 right-4 md:bottom-6 md:right-6`, `px-5 py-3 md:px-8 md:py-5 bg-white rounded-full text-black text-base md:text-xl font-bold z-10 hover:scale-105 transition-transform`, text "Call Us"

**Card 2 - Bottom Left ("Smile makeover"):**
- `MaskedCard`: `rounded-xl md:rounded-2xl overflow-hidden relative min-h-[160px] md:min-h-0`
- Animated: `s2Reveal.getAnimStyle(2)`
- Heading: `absolute top-4 left-5 md:top-6 md:left-7`, `text-white md:text-black text-[clamp(3rem,7vw,6rem)] font-bold leading-[0.9] z-10`, content: "Smile" `<br/>` "makeover"

**Card 3 - Bottom Full Width (Services):**
- `MaskedCard`: `col-span-1 md:col-span-2 rounded-xl md:rounded-2xl overflow-hidden relative min-h-[200px] md:min-h-0`
- Animated: `s2Reveal.getAnimStyle(3)`
- Inner container: `absolute inset-0 z-10 flex flex-wrap md:flex-nowrap gap-1.5 md:gap-2 p-2 md:p-3`
- 4 service sub-cards mapped from `services` array:
  - Container: `flex-1 min-w-[calc(50%-4px)] md:min-w-0 rounded-xl md:rounded-2xl p-3 md:p-5 flex flex-col justify-between`
  - Active: `bg-white/90 backdrop-blur-md`
  - Inactive: `bg-white/20 backdrop-blur-xl`
  - Service name: `<h3>` with `text-xl md:text-4xl font-bold leading-[1.05] whitespace-pre-line`, color: active=`text-black`, inactive=`text-white`
  - Number badge (if `svc.num` exists): `self-end w-8 h-8 md:w-12 md:h-12 rounded-full border flex items-center justify-center text-xs md:text-sm font-semibold`
    - Active: `border-black text-black`
    - Inactive: `border-white text-white`

---

### SECTION 3 - IMPLANT DENTISTRY

**Container:** `<section>`, `min-h-screen md:h-screen w-full overflow-hidden flex flex-col`, `pt-1.5 md:pt-2 px-3 md:px-5 pb-1.5 md:pb-2 gap-1.5 md:gap-2`

Attach `s3Reveal.containerRef` to this element.

Does NOT use MaskedCard technique. Uses regular `<img>` tags and solid backgrounds.

**Grid:** `flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 gap-1.5 md:gap-2`

#### LEFT COLUMN: `flex flex-col gap-1.5 md:gap-2`

**1. Heading Card:**
- `<div>`: `rounded-xl md:rounded-2xl bg-stone-50 p-5 md:p-7 flex flex-col justify-between flex-[1.2] min-h-[180px] md:min-h-0`
- Animated: `s3Reveal.getAnimStyle(0)`
- Heading: `<h2>` with `text-[clamp(3rem,7vw,6.5rem)] font-bold leading-[0.95] text-black`, content: "Implant" `<br/>` "Dentistry"
- Subtitle: `<p>` with `text-xs md:text-sm font-semibold text-black`, text "Restore Missing Teeth"

**2. Two Image Cards (side by side):**
- Wrapper: `<div>` with `flex gap-1.5 md:gap-2 flex-1 min-h-[140px] md:min-h-0`
- Animated: `s3Reveal.getAnimStyle(1)`
- Left image: `<div className="flex-1 rounded-xl md:rounded-2xl overflow-hidden"><img src={SECTION3_IMG1} alt="Dental implant procedure" className="w-full h-full object-cover" /></div>`
- Right image: `<div className="flex-1 rounded-xl md:rounded-2xl overflow-hidden"><img src={SECTION3_IMG2} alt="Dental restoration" className="w-full h-full object-cover" /></div>`

**3. Consultation Card:**
- `<div>`: `rounded-xl md:rounded-2xl bg-zinc-200 p-5 md:p-7 flex items-end justify-between flex-[0.8] min-h-[160px] md:min-h-0`
- Animated: `s3Reveal.getAnimStyle(2)`
- Left content block:
  - Label: `<p>` with `text-xs md:text-sm font-semibold text-black mb-2 md:mb-3`, text "Consultation"
  - Heading: `<h3>` with `text-xl md:text-3xl font-bold text-black leading-6 md:leading-8`, content: "Dental" `<br/>` "Restoration" `<br/>` "Services"
- Button: `px-5 py-3 md:px-8 md:py-5 bg-white rounded-full text-black text-base md:text-xl font-bold hover:scale-105 transition-transform`, text "Book Online"

#### RIGHT COLUMN: Single tall image card

- `<div>`: `rounded-xl md:rounded-2xl overflow-hidden relative min-h-[350px] md:min-h-0`
- Animated: `s3Reveal.getAnimStyle(3)`
- Background image: `<img src={SECTION3_BG} alt="Smiling patient" className="w-full h-full object-cover" />`
- **Overlay container:** `absolute bottom-3 left-3 right-3 md:bottom-5 md:left-5 md:right-5 flex gap-1.5 md:gap-2`

**Overlay Card 1 (white, left):**
- `flex-1 bg-white rounded-xl md:rounded-2xl p-3 md:p-5 flex flex-col justify-between h-36 md:h-52`
- Heading: `<h4>` with `text-lg md:text-2xl font-bold text-black leading-5 md:leading-7`, content: "The Process" `<br/>` "of Installing" `<br/>` "Implants"
- Arrow icon: `self-end w-9 h-9 md:w-12 md:h-12 rounded-full border border-black flex items-center justify-center`
  - SVG: `width="14" height="14" viewBox="0 0 14 14" fill="none"`, class `rotate-[-45deg]`
  - Path: `d="M1 7h12m0 0L8 2m5 5L8 12"` with `stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"`

**Overlay Card 2 (glass, right):**
- `flex-1 bg-white/20 backdrop-blur-xl rounded-xl md:rounded-2xl p-3 md:p-5 flex flex-col justify-between h-36 md:h-52`
- Heading: `<h4>` with `text-lg md:text-2xl font-bold text-white leading-5 md:leading-7`, content: "Caring" `<br/>` "for Dental" `<br/>` "Implants"
- Arrow icon: `self-end w-9 h-9 md:w-12 md:h-12 rounded-full border border-white flex items-center justify-center`
  - Same SVG as above but with added class `text-white`

---

### OUTER WRAPPER

The entire app is wrapped in `<div className="bg-white">` containing:
1. `{showSplash && <SplashScreen />}` (conditionally rendered)
2. `<Navbar />`
3. Section 1
4. Section 2
5. Section 3

---

### KEY DESIGN RULES

- **Spacing between sections:** Only `pb-1.5 md:pb-2` on each section and `pt-1.5 md:pt-2` on sections 2 and 3 -- virtually seamless.
- **Border radius:** All cards use `rounded-xl md:rounded-2xl` with `overflow-hidden`.
- **Color palette:** Strictly black, white, and translucent white (`bg-white/20`, `bg-white/90`) with `backdrop-blur-md` or `backdrop-blur-xl`.
- **Background fills:** `bg-stone-50` and `bg-zinc-200` for Section 3 solid cards.
- **Typography:** Heavy bold/extrabold, `clamp()` for responsive headings, extremely tight leading (0.79, 0.9, 0.95, 1.05).
- **Interactions:** `hover:scale-105 transition-transform` on CTA buttons.
- **Responsive:** Single `md:` (768px) breakpoint. Stacked on mobile, grid on desktop.
- **No external packages** beyond React and Tailwind.
```

---

## 91. Orbis Hello

- **Category**: About
- **Type**: about
- **Page Type**: hero
- **ID**: `orbis-hello`

```
---

> **Setup requirements before building the section:**
>
> **Google Fonts** -- Load these in `index.html` `<head>`:
> ```html
> <link rel="preconnect" href="https://fonts.googleapis.com" />
> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
> <link href="https://fonts.googleapis.com/css2?family=Anton&family=Condiment&display=swap" rel="stylesheet" />
> ```
>
> **Tailwind config** -- Extend `theme` with these exact custom values:
> ```js
> fontFamily: {
>   grotesk: ['Anton', 'sans-serif'],
>   condiment: ['Condiment', 'cursive'],
> },
> colors: {
>   cream: '#EFF4FF',
>   neon: '#6FFF00',
> }
> ```
> `font-grotesk` maps to **Anton** (a tall, condensed display font). `font-condiment` maps to **Condiment** (a flowing cursive/script font).
>
> **No additional CSS classes or animations are used in this section.** No keyframes, no transitions, no hover states. It is a static layout.
>
> ---
>
> **Build the following section as a React component using Tailwind CSS:**
>
> A `<section>` tag with classes `relative overflow-hidden min-h-screen`. No background color -- the background is a fullscreen video.
>
> **Background video:** An absolutely positioned `<video>` element covering the entire section. Classes: `absolute inset-0 w-full h-full object-cover`. Attributes: `autoPlay`, `loop`, `muted`, `playsInline`. The `<source>` element points to:
> ```
> https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260331_151551_992053d1-3d3e-4b8c-abac-45f22158f411.mp4
> ```
> with `type="video/mp4"`.
>
> **Content wrapper:** A `<div>` sitting on top of the video with classes: `relative max-w-[1831px] mx-auto px-4 sm:px-6 md:px-8 py-16 sm:py-20 md:py-24 z-10`.
>
> Inside the content wrapper are **two rows**:
>
> ---
>
> **ROW 1 (top):** A `<div>` with classes `flex flex-col lg:flex-row justify-between items-start gap-8 lg:gap-12 mb-12 sm:mb-16 md:mb-20`. Contains two children:
>
> **Child A -- The heading:** An `<h2>` with classes `font-grotesk text-[32px] sm:text-[48px] md:text-[60px] font-normal uppercase leading-[1.05] sm:leading-[1] md:leading-[1] text-cream relative`. The text content is:
> ```
> Hello!<br />
> I'm orbis
> ```
> (Literally "Hello!" on line 1, "I'm orbis" on line 2, separated by a `<br />`. All rendered uppercase by Tailwind so it displays as "HELLO!" and "I'M ORBIS".)
>
> **Inside the `<h2>`**, after the text, there is an absolutely positioned `<span>` with the word **"Orbis"**. This span has classes: `font-condiment text-[36px] sm:text-[52px] md:text-[68px] font-normal normal-case text-neon mix-blend-exclusion leading-[0.79] tracking-[0.03em] absolute right-[-8px] bottom-[-20px] sm:bottom-[-30px] md:bottom-[-40px] -rotate-1 opacity-90`.
>
> Key details of this span:
> - `normal-case` overrides the parent's uppercase, so it renders as "Orbis" (capital O, lowercase rbis) in the Condiment cursive font.
> - `text-neon` = `#6FFF00` (bright green).
> - `mix-blend-exclusion` makes the green text interact with the video background.
> - `absolute right-[-8px] bottom-[-20px]` (responsive: `sm:bottom-[-30px] md:bottom-[-40px]`) positions it hanging below and slightly right of the parent heading, overlapping the word "orbis" above it.
> - `-rotate-1` gives it a slight counter-clockwise tilt (-1 degree).
> - `leading-[0.79]` is a very tight line-height. `tracking-[0.03em]` adds subtle letter spacing.
> - `opacity-90` makes it 90% opaque.
>
> **Child B -- The paragraph:** A `<p>` with classes `font-mono text-[14px] sm:text-[15px] md:text-[16px] uppercase text-cream max-w-[266px] leading-relaxed`. The text is:
> > "A digital object fixed beyond time and place. An exploration of distance, form, and silence in space"
>
> (`font-mono` uses the browser's default monospace font. `leading-relaxed` = 1.625 line-height.)
>
> ---
>
> **ROW 2 (bottom):** A `<div>` with classes `flex justify-between items-start`. Contains two children:
>
> **Child A -- Left text column** (always visible): A `<div>` with classes `flex flex-col gap-5 max-w-[335px]`. Contains **two identical `<p>` tags**, each with classes `font-mono text-[14px] sm:text-[15px] md:text-[16px] uppercase lg:text-cream text-[#010828] opacity-10 leading-relaxed`. Both contain the same text:
> > "A digital object fixed beyond time and place. An exploration of distance, form, and silence in space"
>
> Key detail: The color is `text-[#010828]` (near-invisible dark navy matching the page background) by default, switching to `lg:text-cream` (`#EFF4FF`) on large screens. Combined with `opacity-10`, this text is extremely faint/ghostly -- almost invisible, serving as a subtle texture element rather than readable content.
>
> **Child B -- Right text column** (desktop only): A `<div>` with classes `hidden lg:flex flex-col gap-5 max-w-[335px]`. Contains **two identical `<p>` tags** with the exact same classes and text as Child A. This column is hidden on mobile/tablet and only appears on `lg:` (1024px+) screens.
>
> ---
>
> **There are no animations, transitions, hover effects, scroll effects, or JavaScript interactions in this section.** It is purely a static layout with a looping background video. The only "motion" comes from the autoplaying video itself.

---
```

---

## 92. Digital Experiences

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `digital-experiences`

```
## Prompt

Build a single-page React + Vite + TypeScript + Tailwind CSS site with exactly two full-screen sections (Hero and Capabilities). The page is a dark, cinematic web design agency landing page with "liquid glass" morphism UI elements and smooth blur/fade animations using Framer Motion.

---

### Fonts (Google Fonts)

Load via `<link>` in `index.html`:
- **Instrument Serif** (italic) -- used for all headings (`font-heading`)
- **Barlow** (weights 300, 400, 500, 600) -- used for body text (`font-body`)

Tailwind config extends `fontFamily`:
```js
heading: ["'Instrument Serif'", 'serif'],
body: ["'Barlow'", 'sans-serif'],
```

Base CSS: `html, body { background: #000; color: #fff; font-family: 'Barlow', sans-serif; }`

---

### Liquid Glass CSS (in index.css)

Two variants defined as plain CSS classes:

**`.liquid-glass`** (subtle):
- `background: rgba(255, 255, 255, 0.01)` with `background-blend-mode: luminosity`
- `backdrop-filter: blur(4px)` / `-webkit-backdrop-filter: blur(4px)`
- No border; `box-shadow: inset 0 1px 1px rgba(255,255,255,0.1)`
- `position: relative; overflow: hidden`
- `::before` pseudo-element creates a gradient stroke border:
- `position: absolute; inset: 0; border-radius: inherit; padding: 1.4px`
- `background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)`
- Masked with `-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); -webkit-mask-composite: xor; mask-composite: exclude;`
- `pointer-events: none`

**`.liquid-glass-strong`** (bolder):
- Same structure but `backdrop-filter: blur(50px)`
- `box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15)`
- `::before` gradient uses 0.5 alpha at edges, 0.2 at 20%/80%

---

### FadingVideo Component

A reusable `<video>` component accepting `src` (string or string[]), `className`, and `style`. It:
1. Starts with `opacity: 0`
2. On `loadeddata`, fades in over 500ms using `requestAnimationFrame`
3. On `timeupdate`, when remaining time <= 0.55s, fades out over 550ms
4. On `ended`, if single source: resets `currentTime` to 0, replays, fades back in. If array: advances to next index (cycling).
5. Video is `autoPlay`, `muted`, `playsInline`, `preload="auto"`

---

### BlurText Component

A word-by-word staggered blur-in animation component using Framer Motion:
- Splits `text` prop by spaces
- Each word is a `motion.span` with `display: inline-block`, `marginRight: 0.28em`
- Triggers on IntersectionObserver (threshold 0.1)
- Each word animates: `filter` from `blur(10px)` to `blur(0px)`, `opacity` 0 to 1, `y` from 50 to 0
- Duration 0.7s per word, stagger delay of 100ms per word index
- Container uses `display: flex; flexWrap: wrap; justifyContent: center; rowGap: 0.1em`

---

### Section 1: Hero

- Full viewport height (`h-screen`), `overflow-hidden`, `bg-black`
- **Background video**: Single `<FadingVideo>` with:
- `src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260619_191346_9d19d66e-86a4-47f7-8dc6-712c1788c3b2.mp4"`
- Positioned: `absolute left-1/2 top-0 -translate-x-1/2 object-cover object-top z-0`
- Inline style: `width: 120%; height: 120%`

- **Content** (`relative z-10, flex flex-col h-full`):

**Navbar** (fixed, `top-4 left-0 right-0 z-50`, flex between, `px-8 lg:px-16`):
- Left: `liquid-glass` circle (h-12 w-12 rounded-full) with italic "a" in `font-heading text-2xl`
- Center (hidden on mobile, `md:flex`): `liquid-glass rounded-full px-1.5 py-1.5` pill containing links ["Work", "Studio", "Services", "Journal", "Contact"] as `px-3 py-2 text-sm font-medium text-white/90 font-body` + a white CTA button "Start a Project" with ArrowUpRight icon
- Right: empty `h-12 w-12` spacer div

**Main content** (centered, `flex-1 flex flex-col items-center justify-center pt-24 px-4 text-center`):
- **Badge** (motion.div, delay 0.4): `liquid-glass rounded-full` pill with a white "New" badge inside + text "Booking Q3 2026 engagements -- limited capacity"
- **Headline** (mt-6, max-w-3xl): `<BlurText>` with text "Crafted Digital Experiences Built to Outlast Trends", classes: `text-6xl md:text-7xl lg:text-[5.5rem] font-heading italic text-white leading-[0.8] tracking-[-4px]`
- **Subtext** (motion.p, delay 0.8, mt-4): "We are a small studio of designers and engineers shaping brand-defining websites for ambitious companies. Precise typography, cinematic motion, and code you can be proud of." -- `text-sm md:text-base text-white max-w-2xl font-body font-light leading-tight`
- **CTA buttons** (motion.div, delay 1.1, mt-6, flex gap-6): "Start a Project" in `liquid-glass-strong rounded-full px-5 py-2.5` with ArrowUpRight + "Watch Showreel" plain text with Play icon
- **Stats cards** (motion.div, delay 1.3, mt-8, flex gap-4): Two `liquid-glass p-5 w-[220px] rounded-[1.25rem]` cards:
- Card 1: ClockIcon, "6 Weeks", "Average End-to-End Launch Time"
- Card 2: GlobeIcon, "140+", "Brands Shipped Across Four Continents"
- Numbers: `text-4xl font-heading italic tracking-[-1px] leading-none mt-4`

**Bottom trust bar** (motion.div, delay 1.4, flex-col items-center gap-4 pb-8):
- `liquid-glass rounded-full` pill: "Trusted by founders, operators, and creative directors worldwide"
- Logo names in a flex row (gap-12 md:gap-16): ["Aeon", "Vela", "Apex", "Orbit", "Zeno"] each as `font-heading italic text-2xl md:text-3xl tracking-tight`

- **All motion elements** use shared initial/animate: `{ filter: 'blur(10px)', opacity: 0, y: 20 }` -> `{ filter: 'blur(0px)', opacity: 1, y: 0 }`, duration 0.8s, easeOut

---

### Section 2: Capabilities

- `min-h-screen`, `overflow-hidden`, `bg-black`, relative
- **Background video**: `<FadingVideo>` with:
- `src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_093722_ccfc7ebf-182f-419f-8a62-2dc02db7dd9d.mp4"`
- `absolute inset-0 w-full h-full object-cover z-0`

- **Content** (`relative z-10 px-8 md:px-16 lg:px-20 pt-24 pb-10 flex flex-col min-h-screen`):
- **Header** (mb-auto):
- Label: `text-sm font-body text-white/80 mb-6` -- "// Capabilities"
- Heading: `font-heading italic text-6xl md:text-7xl lg:text-[6rem] leading-[0.9] tracking-[-3px]` -- "Studio craft,\nend to end"

- **Cards grid** (mt-16, `grid grid-cols-1 md:grid-cols-3 gap-6`), three cards:
1. **Design** -- Icon: ImageIcon (filled image icon), Tags: ["Brand Systems", "Art Direction", "Visual Identity", "Motion"], Body: "We shape identities and interfaces that feel unmistakably yours -- typographic systems, component libraries, and art-directed pages that scale without losing soul."
2. **Engineering** -- Icon: MovieIcon (film/clapboard), Tags: ["React", "Next.js", "Headless CMS", "Edge-Ready"], Body: "Production-grade front-ends built on modern stacks. Performant, accessible, and instrumented -- with code your team will enjoy extending long after launch."
3. **Growth** -- Icon: LightbulbIcon, Tags: ["SEO", "Analytics", "A/B Testing", "Retention"], Body: "Launch is the starting line. We partner with your team on conversion, content, and iteration loops that turn a beautiful site into a compounding asset."

- Each card: `liquid-glass rounded-[1.25rem] p-6 min-h-[360px] flex flex-col`
- Top row: icon in a nested `liquid-glass h-11 w-11 rounded-[0.75rem]` square + tags (flex-wrap, gap-1.5) right-aligned, each tag is `liquid-glass rounded-full px-3 py-1 text-[11px] text-white/90 font-body whitespace-nowrap`
- Spacer: `flex-1`
- Bottom: title in `font-heading italic text-3xl md:text-4xl tracking-[-1px] leading-none` + body in `text-sm text-white/90 font-body font-light leading-snug max-w-[32ch]`

---

### Custom SVG Icons (no external icon library needed for these)

- **ArrowUpRight**: 24x24, stroke, paths "M7 17L17 7" and "M7 7h10v10"
- **Play**: 24x24, filled polygon "6 4 20 12 6 20 6 4"
- **ClockIcon**: 24x24, stroke (1.5), circle r=9 + "M12 7v5l3 2"
- **GlobeIcon**: 24x24, stroke (1.5), circle r=9 + horizontal line + two arc paths
- **ImageIcon**: 24x24, filled Material-style image icon
- **MovieIcon**: 24x24, filled Material-style movie icon
- **LightbulbIcon**: 24x24, filled Material-style bulb icon

---

### Dependencies

- react, react-dom
- framer-motion
- tailwindcss, postcss, autoprefixer
- vite, @vitejs/plugin-react
- typescript

---

### Key Design Principles

- Everything is on a pure black (#000) background
- All text is white; subtle text uses `white/80` or `white/90`
- Liquid glass elements have near-invisible fills with gradient-stroke borders via CSS masks
- Videos cover sections as atmospheric backgrounds, fading in/out smoothly
- Typography: heading font is always italic with very tight tracking (negative), body font is light weight
- Responsive: nav links hidden on mobile, grid collapses to single column, text sizes scale with breakpoints
- Animations: staggered blur-in on load for hero content, intersection-triggered for BlurText
```

---

## 93. Stark Minimal Footer

- **Category**: Footer
- **Type**: footer
- **Page Type**: hero
- **ID**: `stark-minimal-footer`

```
---

Build a **Site Footer** for an aerospace company called "EngineTech." This is a black-background footer with an animated dotted top border, a four-column nav grid with a large heading, an oversized wordmark brand row, and a legal line.

---

## ROOT CONTAINER (`.site-footer`)

- Position relative, z-index 100, overflow hidden.
- Background: `#000000`. Color: `#ffffff`.

---

## ANIMATED DOTS STRIP (`.footer-dots`)

A decorative band at the very top of the footer with horizontally drifting dots.

- Position relative, height 120px, overflow hidden, background `#000000`.
- Has `aria-hidden="true"`.

**Inside (`.footer-dots__line`):**

- Position absolute, `left: 0; top: 50%`. Width **200%**, height 70px.
- Opacity 0.75. `transform: translateY(-50%)`.
- Background-image (three layered radial-gradient dot patterns):
  - `radial-gradient(circle, rgb(255 255 255 / 0.55) 1.5px, transparent 2px)`
  - `radial-gradient(circle, rgb(255 255 255 / 0.35) 1px, transparent 1.5px)`
  - `radial-gradient(circle, rgb(255 255 255 / 0.45) 1.2px, transparent 1.8px)`
- Background-position: `0 8px, 24px 22px, 48px 14px`.
- Background-size: `72px 38px, 110px 44px, 160px 52px`.
- Animation: `footerDotsMove 18s linear infinite`.

**Keyframes:**

```
@keyframes footerDotsMove {
  from { transform: translate3d(0, -50%, 0); }
  to   { transform: translate3d(-50%, -50%, 0); }
}
```

---

## FOOTER INNER (`.site-footer__inner`)

- Width: `min(100% - 96px, var(--hero-max-width))` where `--hero-max-width: 1820px`. Margin `0 auto`.
- Padding: `clamp(34px, 4vw, 66px) 0 clamp(18px, 2vw, 34px)`.

---

## TOP GRID (`.site-footer__top`)

- Display grid. Columns: `minmax(320px, 1.25fr) repeat(3, minmax(150px, 0.42fr))`.
- Gap: `clamp(28px, 4vw, 76px)`. Min-height: `clamp(220px, 24vw, 330px)`.

### H2 (first cell)

- Text: "Proven Advanced Propulsion Technology".
- Max-width 680px, margin 0, color `#ffffff`, `font-size: clamp(34px, 3.5vw, 62px)`, weight 220, letter-spacing 0, line-height 1.06.

### Nav columns (three `.site-footer__nav` elements)

Each nav is `display: flex; flex-direction: column; align-items: flex-start; gap: clamp(14px, 1.35vw, 22px)`.

Each link `<a>`:
- Color `rgb(255 255 255 / 0.88)`, font-size 16px, weight 650, line-height 1.1.
- Transition: `color 180ms ease, transform 180ms ease`.
- Hover: color `#ffffff`, `transform: translateX(3px)`.

**Nav 1 (`aria-label="Footer navigation"`):**
- Company → `#company`
- Technology → `#technology`
- Solutions → `#solutions`
- Our Edge → `#our-edge`
- Investors → `#investors`

**Nav 2 (`aria-label="Company links"`):**
- Our Team → `#our-team`
- News → `#news`
- Careers → `#careers`
- Contact Us → `#contact`

**Nav 3 (`aria-label="Social links"`):**
- LinkedIn → `https://www.linkedin.com` (`target="_blank" rel="noreferrer"`)
- Follow Us on X → `https://x.com` (`target="_blank" rel="noreferrer"`)

---

## BRAND ROW (`.site-footer__brand-row`)

- Width 100%. Margin-top: `clamp(18px, 3vw, 46px)`.

**Brand link (`.site-footer__brand`):**

- Anchor `href="/"`, `aria-label="EngineTech home"`.
- Display flex, align-items center, width 100%, color `#ffffff`.

**Brand mark (`.site-footer__mark`):**

- Position relative, `flex: 0 0 clamp(58px, 6.1vw, 118px)`, `aspect-ratio: 1`.
- Margin-right `clamp(14px, 1.6vw, 28px)`. Overflow hidden, border-radius 50%.
- Background `#ffffff`.
- `::before` pseudo: absolute `inset: -18%`, background `#000000`, with `clip-path: polygon(0 20%, 100% 8%, 100% 19%, 0 31%, 0 43%, 100% 31%, 100% 42%, 0 54%, 0 66%, 100% 54%, 100% 65%, 0 77%)`. This creates a zig-zag wave pattern inside the white circle.
- Has `aria-hidden="true"`.

**Brand wordmark (second `<span>`):**

- Text: "EngineTech".
- Display block, `flex: 1 1 auto`, min-width 0.
- `font-size: clamp(58px, 11.1vw, 214px)`. Weight 760. `letter-spacing: -0.055em`. Line-height 0.78.
- `white-space: nowrap`.

---

## LEGAL LINE (`.site-footer__legal`)

- Flex row, wrap allowed, justify-content flex-start, gap `8px 18px`.
- Margin-top: `clamp(14px, 1.4vw, 24px)`.
- Color `rgb(255 255 255 / 0.52)`, font-size 9px, line-height 1.35.

Contents:
- `<p>`: "© 2026 EngineTech. All rights reserved." (margin 0)
- `<a href="#privacy">`: "Privacy Policy" (color inherit, hover `#ffffff`)
- `<a href="#terms">`: "Terms of Use" (same styling)

---

## RESPONSIVE BREAKPOINTS

**At 980px:**

- `.site-footer__inner` width: `min(100% - 48px, var(--hero-max-width))`.
- Top grid: `grid-template-columns: 1fr 1fr` (two columns).
- H2 spans full width: `grid-column: 1 / -1`.

**At 560px:**

- `.site-footer__inner` width: `min(100% - 32px, var(--hero-max-width))`.
- Top grid: single column (`grid-template-columns: 1fr`). Min-height auto.
- Nav links font-size 15px.
- Brand mark flex-basis: `clamp(38px, 12vw, 58px)`.
- Brand wordmark font-size: `clamp(45px, 18vw, 84px)`.

---

## GLOBAL STYLES

**CSS custom property used:** `--hero-max-width: 1820px`.

**Font stack:** `"Geist", "Inter", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` with `-webkit-font-smoothing: antialiased` and `text-rendering: geometricPrecision`.

**Anchor reset:** `a { color: inherit; text-decoration: none; }`.

**Color palette:** No purple or violet. Pure black `#000000` background, pure white `#ffffff` text, with `rgb(255 255 255 / 0.88)` for nav links, `rgb(255 255 255 / 0.55)` / `0.45` / `0.35` for the dot pattern, and `rgb(255 255 255 / 0.52)` for legal text.
```

---

## 94. Nike Hover

- **Category**: Features
- **Type**: features
- **Page Type**: hero
- **ID**: `nike-hover`

```
Create a single full-viewport (`h-[100dvh]`) Nike-branded section in React + Tailwind CSS + GSAP. It must be **fully mobile responsive**. The app requires `react-player` and `gsap` installed via npm.

---

### 1. Dependencies to Install
Install `react-player` and `gsap`.

### 2. Globals & Configuration (`src/index.css`)
Replace `index.css` with this exact Tailwind v4 and Google Fonts configuration:
```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap');
@import "tailwindcss";

@theme {
  --font-sans: "Manrope", sans-serif;
  --font-serif: "Instrument Serif", serif;
}
```

### 3. SpotlightReveal Component (`src/components/SpotlightReveal.tsx`)

An interactive cursor-following SVG spotlight mask. The user's mouse reveals a hidden video layer underneath a static image overlay. On mobile/touch devices, falls back to touch tracking.

```tsx
import { useEffect, useRef } from 'react';

interface SpotlightRevealProps {
  imageSrc: string;
  videoSrc: string;
  isPlaying?: boolean;
  baseRadius?: number;
}

export default function SpotlightReveal({
  imageSrc,
  videoSrc,
  isPlaying = true,
  baseRadius = 420,
}: SpotlightRevealProps) {
  const NUM_TRAILS = 6;
  const videoRef = useRef<HTMLVideoElement>(null);
  const pointsRef = useRef(
    Array.from({ length: NUM_TRAILS }, () => ({ x: -1000, y: -1000 }))
  );

  useEffect(() => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.play().catch(() => {});
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying]);

  useEffect(() => {
    let targetX = window.innerWidth / 2,
      targetY = window.innerHeight / 2;
    const handleMouseMove = (e: MouseEvent) => {
      targetX = e.clientX;
      targetY = e.clientY;
    };
    window.addEventListener('mousemove', handleMouseMove);

    let animationFrameId: number;
    const animate = () => {
      const points = pointsRef.current;
      points[0].x += (targetX - points[0].x) * 0.2;
      points[0].y += (targetY - points[0].y) * 0.2;
      for (let i = 1; i < points.length; i++) {
        points[i].x += (points[i - 1].x - points[i].x) * 0.35;
        points[i].y += (points[i - 1].y - points[i].y) * 0.35;
      }
      for (let i = 0; i < points.length; i++) {
        const circle = document.getElementById(`trail-${i}`);
        if (circle) {
          circle.setAttribute('cx', points[i].x.toString());
          circle.setAttribute('cy', points[i].y.toString());
        }
      }
      animationFrameId = requestAnimationFrame(animate);
    };
    animate();
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="absolute inset-0 w-full h-full z-0 bg-black pointer-events-none overflow-hidden flex items-center justify-center">
      <div className="absolute inset-0 w-full h-full flex items-center justify-center overflow-hidden pointer-events-none">
        <video
          ref={videoRef}
          src={videoSrc}
          className="absolute inset-0 w-full h-full object-cover"
          muted
          loop
          playsInline
        />
      </div>
      <svg
        className="absolute inset-0 w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <radialGradient id="holeGradient">
            <stop offset="0%" stopColor="black" stopOpacity="1" />
            <stop offset="60%" stopColor="black" stopOpacity="0.8" />
            <stop offset="100%" stopColor="black" stopOpacity="0" />
          </radialGradient>
          <mask
            id="spotlight-mask"
            maskContentUnits="userSpaceOnUse"
            x="0"
            y="0"
            width="100%"
            height="100%"
          >
            <rect width="100%" height="100%" fill="white" />
            {Array.from({ length: NUM_TRAILS })
              .reverse()
              .map((_, reversedIndex) => {
                const i = NUM_TRAILS - 1 - reversedIndex;
                return (
                  <circle
                    key={`trail-${i}`}
                    id={`trail-${i}`}
                    cx="-1000"
                    cy="-1000"
                    r={baseRadius - i * 35}
                    fill="url(#holeGradient)"
                    opacity={1 - i * 0.15}
                  />
                );
              })}
          </mask>
        </defs>
        <image
          href={imageSrc}
          width="100%"
          height="100%"
          preserveAspectRatio="xMidYMid slice"
          mask="url(#spotlight-mask)"
        />
      </svg>
    </div>
  );
}
```

**How it works:**
- A `<video>` plays fullscreen behind everything.
- An SVG `<image>` is overlaid on top, masked by a radial gradient mask.
- 6 trail circles follow the cursor with easing (leader at 0.2 lerp, followers at 0.35 lerp). Where the circles are, the mask cuts a hole revealing the video underneath.
- `baseRadius` controls the spotlight size (default 420 for section 1, 520 for this section 2).
- `isPlaying` toggles video play/pause via hover zones defined in the parent.

---

### 4. Section 2 Layout (`src/App.tsx`)

**Exact assets:**
- **Image overlay (static):** `https://github.com/dsMagnatov/Acreage-landing-assets/blob/main/02604201313.png?raw=true`
- **Video (revealed on hover):** `https://pikaso.cdnpk.net/private/production/4024859125/d070ae9c-55df-47aa-acbe-4ee66337855c-0.mp4?token=exp=1777075200~hmac=4202c1d0ec90137eb6dffa8e0db93ed7569a68b2016165d8b1b567f888869ff5`
- **SpotlightReveal baseRadius:** `520`

**Section container:**
```tsx
<section
  className="relative z-10 w-full h-[100dvh] overflow-hidden bg-black text-white"
  style={{ boxShadow: '0 -20px 50px rgba(0,0,0,0.5)' }}
>
```
- Full viewport height, black background, white text, top inset shadow for depth when scrolling.

**Element 1 -- SpotlightReveal background:**
```tsx
<SpotlightReveal
  imageSrc="https://github.com/dsMagnatov/Acreage-landing-assets/blob/main/02604201313.png?raw=true"
  videoSrc="https://pikaso.cdnpk.net/private/production/4024859125/d070ae9c-55df-47aa-acbe-4ee66337855c-0.mp4?token=exp=1777075200~hmac=4202c1d0ec90137eb6dffa8e0db93ed7569a68b2016165d8b1b567f888869ff5"
  isPlaying={isSecondVideoPlaying}
  baseRadius={520}
/>
```

**Element 2 -- Two invisible hover trigger zones (toggle video play/pause):**
```tsx
{/* Right-side hover zone */}
<div
  className="absolute right-[calc(8%+100px)] bottom-[12%] w-[calc(50%-50px)] h-[calc(50%+230px)] z-30"
  onMouseEnter={() => setIsSecondVideoPlaying(true)}
  onMouseLeave={() => setIsSecondVideoPlaying(false)}
/>
{/* Left-side hover zone */}
<div
  className="absolute left-[calc(8%+200px)] top-[calc(20%+190px)] w-[calc(15%+250px)] h-[calc(22.5%+130px)] -translate-y-full z-30"
  onMouseEnter={() => setIsSecondVideoPlaying(true)}
  onMouseLeave={() => setIsSecondVideoPlaying(false)}
/>
```
These are transparent interactive areas that trigger the video. Make them responsive: on mobile, simplify to a single full-width touch zone or auto-play the video.

**Element 3 -- Stats card (top-left area):**
Positioned `absolute left-[calc(8%+200px)] top-[20%] z-20`. Width `320px`. Glassmorphism card with:
- `background: rgba(0, 0, 0, 0.16)`, `backdrop-filter: blur(80px)`, `border: 1px solid rgba(255,255,255,0.1)`, `border-radius: 2px (rounded-sm)`.
- Padding: `px-8 py-6`.

Card contents:
1. **Big stat:** `78%` in `font-serif italic`, color `#DA3A16`, size `72px`, `leading-[80px]`, `tracking-tight`.
2. **Inline SVG chart** next to the stat (inside a `w-[11px]` wrapper, but the SVG itself is `width: 160px, height: 80px`). The chart is a wavy line in `#DA3A16` with a drop shadow filter in the same orange-red color. Exact SVG path:
```svg
<svg style="width:160px;height:80px" viewBox="0 0 289 138" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g filter="url(#filter0_d_878_28499)">
    <path d="M22.5 48.7306C39.7833 48.7306 49.34 54.94 63.1667 69.2965C76.9933 83.653 86.55 110.5 103.833 110.5C121.117 110.5 130.673 84.2876 144.5 59.2856C158.327 34.2837 167.883 19.5573 185.167 19.5573C202.45 19.5573 208.55 57.6673 225.833 57.6673C243.117 57.6673 249.217 19.5 266.5 19.5" stroke="#DA3A16" stroke-width="2"/>
  </g>
  <defs>
    <filter id="filter0_d_878_28499" x="0" y="0" width="289" height="138" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feFlood flood-opacity="0" result="BackgroundImageFix"/>
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
      <feOffset dy="4"/>
      <feGaussianBlur stdDeviation="11.25"/>
      <feComposite in2="hardAlpha" operator="out"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.854902 0 0 0 0 0.227451 0 0 0 0 0.0862745 0 0 0 1 0"/>
      <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_878_28499"/>
      <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_878_28499" result="shape"/>
    </filter>
  </defs>
</svg>
```
3. **Title:** `"NEXT-GEN CUSHIONING ARCHITECTURE"` -- `font-serif`, white, `text-[15px]`, `tracking-[0.02em]`, uppercase, `mb-2`, `leading-tight`.
4. **Subtitle:** `"Impact Absorption & Energy Return Dynamics"` -- `font-serif`, `text-white/60`, `text-[13px]`.

On mobile: reposition this card to `left-4 top-[15%]` or `top-auto bottom-[55%]`, reduce width to `w-[280px]`, scale the stat to `text-[48px]`.

**Element 4 -- Hero headline (bottom-left):**
Positioned `absolute left-[8%] bottom-[12%] z-20`, `max-w-[500px]`.

```html
<h2 class="text-[44px] leading-[1.05] tracking-tight flex flex-col">
  <span class="font-sans font-medium">Bringing Aerospace-</span>
  <span class="font-sans font-medium">Grade Infrastructure</span>
  <span class="font-serif font-normal pt-1">
    <span class="not-italic">Directly To Your </span>
    <span class="italic">Everyday</span>
  </span>
  <span class="font-serif italic font-normal">Urban Exploration</span>
</h2>
```

- Lines 1-2 use `font-sans` (Manrope) `font-medium`.
- Lines 3-4 use `font-serif` (Instrument Serif). Line 3 mixes non-italic "Directly To Your" with italic "Everyday". Line 4 is fully italic.
- On mobile: reduce to `text-[24px] sm:text-[32px] md:text-[44px]`, position `left-4 bottom-[8%]`, `max-w-[90%]`.

**Element 5 -- Nike branded CTA block (bottom-right):**
Positioned `absolute right-[calc(8%+100px)] bottom-[12%] z-20`, stacked vertically with `flex flex-col items-center`.

Two stacked boxes, each `w-[180px]`:
1. **Top box (white):** `bg-white`, `py-[6px]`, centered text: `"THE SCIENCE OF IMPACT CONTROL"` in `text-black font-serif text-[10px] uppercase font-bold tracking-[0.08em] leading-[16px]`.
2. **Bottom box (Nike red):** `bg-[#DA3A16]`, `h-[100px]`, centered Nike swoosh SVG in white, `width="86"`. Exact swoosh path:
```svg
<svg width="86" viewBox="135.5 361.38 420.32 149.8" fill="white" xmlns="http://www.w3.org/2000/svg">
  <path d="m181.86 511.11c-12.524-0.49755-22.77-3.9244-30.782-10.289-1.529-1.2159-5.1725-4.8616-6.3949-6.3992-3.2489-4.0853-5.4578-8.0611-6.931-12.472-4.5334-13.579-2.2002-31.397 6.6737-50.953 7.5979-16.742 19.322-33.347 39.776-56.344 3.013-3.384 11.986-13.281 12.043-13.281 0.0216 0-0.46749 0.84706-1.083 1.8786-5.3183 8.9082-9.8689 19.401-12.348 28.485-3.9823 14.576-3.502 27.085 1.4068 36.784 3.3862 6.6822 9.1913 12.47 15.719 15.67 11.428 5.5993 28.159 6.0625 48.592 1.3554 1.4068-0.32599 71.116-18.831 154.91-41.123 83.794-22.294 152.36-40.52 152.37-40.505 0.0237 0.0193-194.68 83.333-295.75 126.56-16.007 6.8431-20.287 8.5715-27.812 11.214-19.236 6.7551-36.467 9.9783-50.396 9.4251z"/>
</svg>
```

On mobile: reposition to `right-4 bottom-[8%]`, reduce width to `w-[140px]`, reduce box height to `h-[80px]`.

---

### 5. Color Palette
| Token | Value | Usage |
|---|---|---|
| Background | `#000000` | Section bg |
| Nike Red/Orange | `#DA3A16` | Stat text, chart stroke, chart glow shadow, Nike logo box |
| Text primary | `#FFFFFF` | Headlines, card title |
| Text muted | `rgba(255,255,255,0.6)` | Card subtitle (`text-white/60`) |
| Card bg | `rgba(0,0,0,0.16)` | Glassmorphism card |
| Card border | `rgba(255,255,255,0.1)` | Card border |
| CTA top box | `#FFFFFF` bg / `#000000` text | Label box |

### 6. Typography Rules
| Element | Font | Weight | Size | Style |
|---|---|---|---|---|
| Headline lines 1-2 | Manrope (`font-sans`) | 500 (medium) | 44px | Normal |
| Headline lines 3-4 | Instrument Serif (`font-serif`) | 400 (normal) | 44px | Italic (mixed on line 3) |
| Stat number | Instrument Serif | 400 | 72px | Italic |
| Card title | Instrument Serif | 400 | 15px | Normal, uppercase |
| Card subtitle | Instrument Serif | 400 | 13px | Normal |
| CTA label | Instrument Serif | 700 (bold) | 10px | Normal, uppercase |

### 7. Mobile Responsive Requirements

Implement these breakpoints:
- **< 640px (mobile):** Stack elements vertically. Stats card moves to top-center with reduced dimensions. Headline drops to `text-[24px]` at `left-4 bottom-[30%]`. Nike CTA block moves to center-bottom. Hover zones become a single full-area touch zone. Consider auto-playing the video on mobile since there's no hover. Reduce `baseRadius` to `280` on mobile.
- **640px-1024px (tablet):** Stats card shifts to `left-[5%] top-[18%]`, headline to `text-[32px]`. CTA block to `right-[5%]`.
- **> 1024px (desktop):** Use the exact desktop positions described above unchanged.

### 8. State Management
```tsx
const [isSecondVideoPlaying, setIsSecondVideoPlaying] = useState(false);
```
Controlled by the invisible hover zones. On mobile, default to `true` (auto-play) or use `onTouchStart`/`onTouchEnd`.

---
```

---

## 95. Audio Showcase

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `audio-showcase`

```
Build a full-screen hero section for a fictional vinyl record label called **"quietpress"** using React, TypeScript, Tailwind CSS, and Vite. The page is a single viewport-height hero with no scrolling. Use **lucide-react** for icons. No other UI libraries.

---

### Font

Load **Helvetica Regular** via this stylesheet in `index.html`:
```
https://db.onlinewebfonts.com/c/a64ff11d2c24584c767f6257e880dc65?family=Helvetica+Regular
```
Set the base font in CSS:
```css
html { font-family: 'Helvetica Regular', Helvetica, Arial, sans-serif; }
```

---

### Background: Boomerang Video Loop

Use this CloudFront video as the background:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260611_183632_c311af08-e4b7-458f-81e7-79847a49b3d3.mp4
```

Create a `BoomerangVideoBg` component that:
1. Plays the video once (muted, playsInline, crossOrigin="anonymous"), capturing every frame into off-screen canvases (max width 960px, scaled proportionally).
2. Uses `requestVideoFrameCallback` when available, falling back to `requestAnimationFrame`.
3. When the video ends, hides the `<video>` element and renders a `<canvas>` that plays the captured frames in a ping-pong (boomerang) loop at 30fps -- forward then backward, endlessly.
4. The container is `absolute inset-0 z-0` with `scale-[1.08] origin-center overflow-hidden` to slightly zoom the video and hide edges.

---

### Liquid Glass CSS Effect

Create a reusable `.liquid-glass` CSS class:
```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

---

### Fade-Up Entrance Animation

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: none; }
}
.animate-fade-up {
  animation: fade-up 0.7s cubic-bezier(0.22, 1, 0.36, 1) backwards;
}
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.25s; }
.delay-3 { animation-delay: 0.4s; }
.delay-4 { animation-delay: 0.55s; }
.delay-5 { animation-delay: 0.75s; }
@media (prefers-reduced-motion: reduce) {
  .animate-fade-up { animation: none; }
}
```

**CRITICAL:** Use `animation-fill-mode: backwards` (not `both` or `forwards`). Using `both` or `forwards` leaves a `transform` on the element after the animation ends, which breaks `backdrop-filter` on any child using `.liquid-glass`. `backwards` applies the "from" state before the animation starts but fully releases all properties when it finishes, so the glass blur works correctly.

---

### Header (absolute, top, z-20)

- **Logo (left):** A custom SVG icon (a quarter-circle shape with a centered dot, white fill, 20x20px) next to the text "quietpress" in `text-base tracking-tight text-white`.
  - SVG path: `M 256 256 L 128 256 C 198.692 256 256 198.692 256 128 C 256 57.308 198.692 0 128 0 C 57.308 0 0 57.308 0 128 C 0 198.692 57.308 256 128 256 L 0 256 L 0 0 L 256 0 Z M 128 104 C 141.255 104 152 114.745 152 128 C 152 141.255 141.255 152 128 152 C 114.745 152 104 141.255 104 128 C 104 114.745 114.745 104 128 104 Z` (viewBox `0 0 256 256`)

- **Nav links (center, hidden on mobile):** "Anthology", "Talents", "Sound diary", "Playback salon" -- `text-sm text-white/90 hover:text-white`, gap-8.

- **Right side:**
  - **Cart button:** White pill shape (`rounded-xl bg-white p-1 pr-3 sm:pr-4`). Contains a blue-700 icon square (`h-7 w-7 rounded-lg bg-blue-700`) with a `ShoppingCart` icon (size 14, strokeWidth 2), then text "Cart (0)" (hidden on mobile, showing just "(0)" on small screens). Has `hover:scale-105 active:scale-95`.
  - **Mobile menu toggle:** `liquid-glass` square button (`h-9 w-9 rounded-xl`), shows `Menu` or `X` icon (size 18). Hidden on `md:` and above.

- **Mobile nav dropdown** (shown when menu is open): `liquid-glass mx-4 rounded-2xl p-2`, each link is `rounded-xl px-4 py-3 text-sm text-white/90 hover:bg-white/10`.

---

### Hero Content (centered, z-10)

Padding: `pt-28 sm:pt-36 md:pt-44`, `px-4 sm:px-6`.

1. **Tag badge** (animate-fade-up delay-1): `liquid-glass rounded-lg px-4 py-1.5 text-xs sm:text-sm text-white` with inline style `background: rgba(255, 255, 255, 0.16)`. Text: "Press 04 . Vernal woods". Bottom margin `mb-5 sm:mb-6`.

2. **Headline** (animate-fade-up delay-2): `max-w-3xl text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-[1.1] text-white`. Two lines:
   ```
   records cut for the
   calm listener.
   ```

3. **Subtext** (animate-fade-up delay-3): `mt-5 sm:mt-6 max-w-md text-sm sm:text-base md:text-lg leading-relaxed text-white/90`. Text: "Drone, roots, and nature-captured sound on wax LPs. Every disc cut just once, snag it or miss."

4. **Two buttons** (animate-fade-up delay-4, `mt-8`, stack vertically on mobile, row on `sm:`):
   - **Primary:** `rounded-xl bg-white px-7 py-2.5 text-sm text-gray-900 hover:scale-105 active:scale-95`. Label: "Browse the shelves"
   - **Secondary:** `liquid-glass rounded-xl px-7 py-2.5 text-sm text-white hover:scale-105 active:scale-95`. Label: "Newest arrivals"

---

### Now Playing Widget (bottom-right, z-20)

Positioned `absolute bottom-4 right-4 sm:bottom-6 sm:right-6 md:bottom-8 md:right-10`. Max width `270px` on mobile, `w-72` on sm+. Has `animate-fade-up delay-5`.

- **Track card:** `rounded-2xl bg-white p-2.5 pr-4 shadow-lg`. Contains:
  - Blue icon square (`h-11 w-11 rounded-xl bg-blue-700`) with `BarChart3` icon (size 20, strokeWidth 2.5).
  - Track info: "Helia Marsh -- Fern Light" (truncated, `text-sm text-gray-900`).
  - Progress bar: `h-1 rounded-full bg-gray-200` with `w-[30%] bg-blue-700` fill.
  - Times: "0:33" and "-1:21" in `text-[10px] text-gray-500`.

- **Controls row** (gap-2):
  - "Prev" and "Next" buttons: `flex-1 rounded-2xl bg-white py-2 text-sm text-gray-900 shadow-lg hover:scale-105 active:scale-95`.
  - Heart button (center): `h-10 w-10 rounded-full bg-white shadow-lg hover:scale-110 active:scale-95`. Uses `Heart` icon (size 16) in `text-blue-700`, filled when liked (`fill-blue-700`). Toggles on click.

---

### Key Technical Notes
- The outer wrapper is `relative h-screen w-full overflow-hidden`.
- All interactive elements use `transition-transform duration-200`.
- The accent color throughout is Tailwind's `blue-700`.
- No Supabase or backend needed -- this is purely a static hero.
```

---

## 96. Animated Cards

- **Category**: Component
- **Type**: carousel
- **Page Type**: hero
- **ID**: `animated-cards`

```
Create a high-performance, interactive 3D horizontal cylinder carousel showing premium animated bank cards.
Core Features & Interactions:
Use React (useState, useEffect, useRef), Tailwind CSS v4, and standard requestAnimationFrame for a smooth 60fps render loop. No external animation libraries needed.
The scene should behave like a continuous circular scroll/carousel, updating a continuous progress variable.
Add interactive 3D parallax tilt to the cards that smoothly responds to mouse cursor movement (mousemove), using inertia damping to lag slightly behind the cursor.
The cards should have real volumetric 3D thickness (achieved by stacking multiple div layers close together, simulating 3D depth).
The carousel math should push cards to the sides (using smoothstep interpolation) and hide them gracefully using perspective formulas as they move completely off-screen.
Each card must have a front and back face. The front face includes an autoplaying video background, a silver metallic chip (SVG), an embedded JWT logo top-right, and intersecting circles bottom-right. The back face should blur the same video background, have a dark magnetic stripe across the top, and feature the cardholder name, number, and CVV in JetBrains Mono.
Visual Styling:
Use a pure black background (#000000).
The application relies exclusively on the interactive 3D card layout (no text layers over the background).
Make sure the scene's wrapper uses CSS perspective: 1350px; and standard transformStyle: preserve-3d.
Please use the exact code below for src/App.tsx and src/index.css to build this exactly as requested.

import React, { useState, useEffect, useRef } from 'react';

const CARD_VIDEOS = [
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260506_030111_a9e15665-d379-4a7f-8116-695bbe452ad1.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260429_171347_f640c30d-ec21-426a-98bc-77e07c2c60cb.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260503_104800_bc43ae09-f494-43e3-97d7-2f8c1692cfd7.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_161253_c72b1869-400f-45ed-ac0c-52f68c2ed5bd.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_115655_b4d9cd77-feed-43cd-a198-af78ebdf1f7a.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260324_024928_1efd0b0d-6c02-45a8-8847-1030900c4f63.mp4',
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260324_024928_1efd0b0d-6c02-45a8-8847-1030900c4f63.mp4'
];

// Nine beautiful premium solid colors to clearly track the cards
const CARD_COLORS = [
  '#FF3B30', // Apple Red
  '#FF9500', // Apple Orange
  '#FFCC00', // Apple Yellow
  '#34C759', // Apple Green
  '#007AFF', // Apple Blue
  '#5856D6', // Apple Purple
  '#FF2D55', // Apple Pink
  '#AF52DE', // Apple Violet
  '#00C7BE', // Apple Teal
];

// Different card details for each of the cards
const CARD_DETAILS = [
  { number: '4232 8908 1121 4892', name: 'ZACHARY MERCER', cvv: '382' },
  { number: '4154 7831 9904 5124', name: 'SOPHIA MARTINEZ', cvv: '109' },
  { number: '5457 4120 7733 9035', name: 'BENJAMIN CARTER', cvv: '764' },
  { number: '4441 5567 1223 2468', name: 'EMILY MORRISON', cvv: '491' },
  { number: '5375 8891 2234 7713', name: 'JACKSON REID', cvv: '255' },
];


export default function App() {
  const cardCount = 5;
  const cardsRefs = useRef<(HTMLDivElement | null)[]>([]);
  const frameId = useRef<number>(0);
  
  // Continuous scroll progress
  const progress = useRef<number>(0);

  // Track mouse coordinates for interactive 3D parallax tilt with inertia damping
  const mouse = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });

  // Responsive state containing card dimensions
  const [metrics, setMetrics] = useState({
    cardW: 336,
    cardH: 211, // 1.59 standard credit card ratio
  });

  // Typography metrics to prevent collisions beautifully across all viewports
  const [fontMetrics, setFontMetrics] = useState({
    titleFontSize: '1.5rem',
    sigFontSize: '2.5rem',
    descFontSize: '14px',
    titleGap: '40px',
    pl: '0px'
  });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Screen-space cursor offset relative to window center, clamped to [-1.0, 1.0] range
      const rx = (e.clientX - window.innerWidth / 2) / (window.innerWidth / 2);
      const ry = (e.clientY - window.innerHeight / 2) / (window.innerHeight / 2);
      mouse.current.targetX = Math.max(-1, Math.min(1, rx));
      mouse.current.targetY = Math.max(-1, Math.min(1, ry));
    };

    const handleMouseLeave = () => {
      // Return gently to center orientation when mouse focus is lost or moves away
      mouse.current.targetX = 0;
      mouse.current.targetY = 0;
    };

    window.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  useEffect(() => {
    const handleResize = () => {
      const w = window.innerWidth;
      const h = window.innerHeight;

      // 1. Calculate Card Metrics (shrink cards if height is small to save vertical space)
      let cardW = Math.round(w * 0.16 + 130);
      
      const heightFactor = Math.min(1.0, Math.max(0.65, h / 850));
      cardW = Math.round(cardW * heightFactor);
      
      cardW = Math.min(336, Math.max(150, cardW));
      const cardH = Math.round(cardW / 1.5925); // Standard credit card ratio

      setMetrics({ cardW, cardH });

      // 2. Calculate Typography Metrics (shrink font sizes aggressively if height or width is small)
      const isMobile = w < 640;
      
      let titleSize = '';
      let sigSize = '';
      let descSize = '';
      let titleGap = '40px'; 
      let plVal = '0px';

      if (isMobile) {
        // Mobile style: centered, text size increased by 30% for high legibility
        titleSize = 'clamp(1.8rem, 5.2vw + 0.4rem, 2.2rem)';
        sigSize = 'clamp(2.86rem, 7.8vw + 0.6rem, 3.5rem)';
        descSize = 'clamp(0.72rem, 1.4vw + 0.35rem, 0.95rem)';
        titleGap = '24px';
        plVal = '0px';
      } else {
        // Desktop / Tablet style: aligned bottom-left
        // Scale factor depends on width and height to shrink before hitting cards
        const scale = Math.min(1.0, Math.max(0.48, (w * 0.45 + h * 0.55) / 1300));
        
        titleSize = `${Math.max(1.15, 3.5 * scale).toFixed(3)}rem`;
        sigSize = `${Math.max(1.5, 4.5 * scale).toFixed(3)}rem`;
        descSize = `${Math.max(11, 16 * scale).toFixed(1)}px`;
        titleGap = `${Math.max(16, Math.round(40 * scale))}px`;
        plVal = `${Math.min(6, Math.max(2.8, 3.5 * scale + 2.2)).toFixed(2)}rem`;
      }

      setFontMetrics({
        titleFontSize: titleSize,
        sigFontSize: sigSize,
        descFontSize: descSize,
        titleGap,
        pl: plVal
      });
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Compute positions, rotations, and visual rules at 60fps
  const renderLoop = () => {
    // Upward flow speed of continuous transition - decreased speed by more than half for slower, premium, and calmer transitions
    progress.current += 0.0016; 

    // Smoothly interpolate current mouse variables towards their target positions (damping/inertia logic)
    mouse.current.x += (mouse.current.targetX - mouse.current.x) * 0.08;
    mouse.current.y += (mouse.current.targetY - mouse.current.y) * 0.08;

    const cards = cardsRefs.current;
    const h = window.innerHeight;
    const { cardH } = metrics;

    const continuousProgress = progress.current;
    const roundedIndex = Math.round(continuousProgress);
    const diffFromRound = continuousProgress - roundedIndex; // ranges between [-0.5, 0.5]
    
    // Custom non-linear magnetic step logic
    // It creates a gorgeous brief "dwell/pause" at front center before accelerating to the next card
    const easedDiff = Math.sign(diffFromRound) * Math.pow(Math.abs(diffFromRound) * 2, 4.2) / 2;
    const virtualActiveIndex = roundedIndex + easedDiff;

    for (let i = 0; i < cardCount; i++) {
      const card = cards[i];
      if (!card) continue;

      // Solve circular wrapping to get closest representation in [-cardCount/2, cardCount/2]
      let offset = i - virtualActiveIndex;
      const halfCount = cardCount / 2;
      while (offset > halfCount) offset -= cardCount;
      while (offset < -halfCount) offset += cardCount;

      const absOffset = Math.abs(offset);
      const sign = Math.sign(offset);

      // Allow cards to render completely off-screen smoothly up to offset 3.0. This prevents any clipping or sudden pop-outs.
      if (absOffset > 3.0) {
        card.style.visibility = 'hidden';
        continue;
      } else {
        card.style.visibility = 'visible';
      }

      // Spacing gap between center card and adjacent cards
      const gap = 36;
      const peekAmount = -55; // Push the card's edge 55px past the screen boundary to hide a premium portion of it!
      const D = 1350; // Perspective distance

      let y = 0;
      let z = 0;
      let rot = 0;

      if (absOffset <= 1) {
        // Smoothstep interpolation from 0 to 1 (Center card to first adjacent card)
        const t = absOffset;
        const easedT = t * t * (3 - 2 * t);

        // Y moves from 0 to (cardH + gap)
        const targetY = cardH + gap;
        y = -sign * (easedT * targetY);

        // Z moves from 400 (center) to 220 (adjacent)
        z = 400 + easedT * (220 - 400);

        // Rotation moves from 0 to 132 degrees (beautiful tilted back face)
        rot = easedT * 132;
      } else if (absOffset <= 2) {
        // Smoothstep interpolation from 1 to 2 (Adjacent card to peeking screen-edge card)
        const t = absOffset - 1;
        const easedT = t * t * (3 - 2 * t);

        const yStart = cardH + gap;
        const zStart = 220;
        const rotStart = 132;

        const zEnd = -60;
        const rotEnd = 175;

        // Perspective-aware formula for exact edge alignment at the screen boundary (peekAmount = 26px inside)
        const sEnd = D / (D - zEnd);
        const yEnd = (h / 2 - peekAmount) / sEnd - (cardH / 2);

        const currentY = yStart + easedT * (yEnd - yStart);
        y = -sign * currentY;

        z = zStart + easedT * (zEnd - zStart);
        rot = rotStart + easedT * (rotEnd - rotStart);
      } else {
        // Smoothstep interpolation from 2 to 3 (Peeking card to completely off-screen card)
        const t = Math.min(absOffset - 2, 1);
        const easedT = t * t * (3 - 2 * t);

        const zStart = -60;
        const rotStart = 175;

        const zEnd3 = -250;
        const rotEnd3 = 195;

        const sEnd2 = D / (D - zStart);
        const yEnd2 = (h / 2 - peekAmount) / sEnd2 - (cardH / 2);

        // Calculate yEnd3 dynamically so that the card's edge is completely 100px past the screen boundary
        const sEnd3 = D / (D - zEnd3);
        const yEnd3 = (h / 2 + 100) / sEnd3 + (cardH / 2);

        const currentY = yEnd2 + easedT * (yEnd3 - yEnd2);
        y = -sign * currentY;

        z = zStart + easedT * (zEnd3 - zStart);
        rot = rotStart + easedT * (rotEnd3 - rotStart);
      }

      const localCardRotation = -sign * rot;

      // Determine how close this card is to the exact center (1.0 = center, 0.0 = adjacent/offscreen)
      const centerFactor = Math.max(0, 1 - absOffset);

      // Vertical tilt (around X-axis) and horizontal tilt (around Y-axis) driven by mouse coordinates
      const maxTiltY = 15; // Max angle tilt left-to-right (degrees)
      const maxTiltX = 12; // Max angle tilt up-and-down (degrees)

      const activeTiltX = -mouse.current.y * maxTiltX * centerFactor;
      const activeTiltY = mouse.current.x * maxTiltY * centerFactor;

      const totalRotX = localCardRotation + activeTiltX;
      const totalRotY = activeTiltY;

      // Depth z-index layer
      card.style.zIndex = Math.round(z).toString();
      card.style.opacity = '1';

      // Inject translation matrix with the premium -3deg tilt combined with dynamic mouse-interactive 3D tilt
      card.style.transform = `translateY(${y.toFixed(2)}px) translateZ(${z.toFixed(2)}px) rotateX(${totalRotX.toFixed(2)}deg) rotateY(${totalRotY.toFixed(2)}deg) rotateZ(-3deg)`;
    }
  };

  useEffect(() => {
    const tick = () => {
      renderLoop();
      frameId.current = requestAnimationFrame(tick);
    };

    frameId.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameId.current);
  }, [metrics]);

  // Slices for 3D volumetric depth with 30% reduced thickness
  // Span from -1.47px to 1.47px creates an extremely premium real 3D volume feel
  const thicknessLayers = [-1.47, -0.73, 0, 0.73, 1.47];

  return (
    <div className="absolute inset-0 bg-[#000000] text-white flex items-center justify-center overflow-hidden select-none">
      
      {/* 3D perspective camera space */}
      <div
        className="relative w-full h-full flex items-center justify-center pointer-events-none"
        style={{
          perspective: '1350px',
        }}
      >
        {/* Dynamic 3D coordinate viewport */}
        <div
          className="absolute"
          style={{
            width: `${metrics.cardW}px`,
            height: `${metrics.cardH}px`,
            transformStyle: 'preserve-3d',
          }}
        >
          {Array.from({ length: cardCount }).map((_, i) => (
            <div
              key={i}
              ref={(el) => { cardsRefs.current[i] = el; }}
              className="absolute inset-0"
              style={{
                width: `${metrics.cardW}px`,
                height: `${metrics.cardH}px`,
                transformStyle: 'preserve-3d',
                backfaceVisibility: 'visible',
              }}
            >
              {/* Build physical 3D volumetric thickness by dense parallel layering */}
              {thicknessLayers.map((zOffset, layerIdx) => {
                const isFrontFace = layerIdx === thicknessLayers.length - 1;
                const isBackFace = layerIdx === 0;

                const videoSrc = CARD_VIDEOS[i % CARD_VIDEOS.length];
                const baseBgColor = '#0f0f0f';

                // Middle structural slice
                if (!isFrontFace && !isBackFace) {
                  return (
                    <div
                      key={layerIdx}
                      className="absolute inset-0 rounded-[16px] border border-[#808080] pointer-events-none overflow-hidden"
                      style={{
                        backgroundColor: '#808080',
                        transform: `translateZ(${zOffset}px)`,
                      }}
                    />
                  );
                }

                // Front face slice
                if (isFrontFace) {
                  const frontBorderStyle = "border border-white/15";
                  return (
                    <div
                      key={layerIdx}
                      className={`absolute inset-0 rounded-[16px] ${frontBorderStyle} pointer-events-none overflow-hidden`}
                      style={{
                        backgroundColor: baseBgColor,
                        transform: `translateZ(${zOffset}px)`,
                        backfaceVisibility: 'hidden',
                        boxShadow: 'inset 0 1px 1px rgba(255,255,255,0.15)',
                      }}
                    >
                      <video
                        src={videoSrc}
                        autoPlay
                        loop
                        muted
                        playsInline
                        className="absolute inset-0 w-full h-full object-cover rounded-[16px]"
                      />

                      <div className="absolute inset-0 p-5 sm:p-6 text-white h-full w-full font-sans z-10 bg-black/15">
                        {/* Golden/Silver Metallic Contact Chip - positioned mid-left (vertically centered on the card) with custom user vectors */}
                        <div className="absolute left-5 sm:left-6 top-1/2 -translate-y-1/2">
                          <svg
                            className="w-6 h-6 sm:w-[29px] sm:h-[29px]"
                            viewBox="0 0 60 60"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              fillRule="evenodd"
                              clipRule="evenodd"
                              d="M20 8H40V14C40.0016 14.5299 40.2128 15.0377 40.5875 15.4125C40.9623 15.7872 41.4701 15.9984 42 16H59V24H42C41.4701 24.0016 40.9623 24.2128 40.5875 24.5875C40.2128 24.9623 40.0016 25.4701 40 26V52H20V8ZM18 8H8.00039C4.47435 8 1.56576 10.6083 1.08 14H18V8ZM1 16V24V26V34V36V44H18V36H1V34H18V26H1V24H18V16H1ZM1.08 46C1.56576 49.3917 4.47435 52 8.00039 52H18V46H1.08ZM42 14V8H52.0004C55.5264 8 58.4342 10.6084 58.92 14H42ZM59 26H42V34H59V26ZM59 36H42V44H59V36ZM52.0004 52H42V46H58.92C58.4342 49.3916 55.5264 52 52.0004 52Z"
                              fill={`url(#paint0_linear_1032_4_${i})`}
                            />
                            <path
                              fillRule="evenodd"
                              clipRule="evenodd"
                              d="M1.02453 14.4146C1.00608 14.609 0.998061 14.8045 1.00039 15C1.00039 14.8028 1.00854 14.6076 1.02453 14.4146ZM1.00039 45C0.998061 45.1955 1.00608 45.391 1.02453 45.5854C1.00854 45.3924 1.00039 45.1972 1.00039 45ZM59.0004 15C59.0026 14.8176 58.9955 14.6353 58.9794 14.4538C58.9933 14.634 59.0004 14.8162 59.0004 15ZM59.0004 45C59.0004 45.1838 58.9933 45.366 58.9794 45.5462C58.9955 45.3647 59.0026 45.1824 59.0004 45Z"
                              fill="#B7B7B7"
                            />
                            <defs>
                              <linearGradient
                                id={`paint0_linear_1032_4_${i}`}
                                x1="30"
                                y1="8"
                                x2="30"
                                y2="52"
                                gradientUnits="userSpaceOnUse"
                              >
                                <stop stopColor="white" />
                                <stop offset="1" stopColor="#999999" />
                              </linearGradient>
                            </defs>
                          </svg>
                        </div>

                        {/* JWT Brand Logo - positioned at top-right */}
                        <div className="absolute right-5 sm:right-6 top-5 sm:top-6 opacity-95">
                          <svg
                            className="w-[84px] xs:w-[101px] sm:w-[120px] h-auto"
                            viewBox="0 0 341 49"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              d="M8.75294 47.68C6.10761 47.68 4.10227 47.04 2.73694 45.76C1.41427 44.48 0.582275 42.7733 0.240941 40.64C-0.100392 38.464 -0.0790588 36.0747 0.304941 33.472C0.731608 30.8267 1.37161 28.1813 2.22494 25.536C3.07827 22.848 3.99561 20.3307 4.97694 17.984C6.00094 15.5947 6.93961 13.5893 7.79294 11.968C8.26227 11.072 8.88094 10.56 9.64894 10.432C10.4169 10.2613 11.1423 10.368 11.8249 10.752C12.5503 11.136 13.0623 11.6907 13.3609 12.416C13.7023 13.1413 13.6383 13.9307 13.1689 14.784C11.2916 18.368 9.79828 21.7813 8.68894 25.024C7.57961 28.2667 6.85427 31.1467 6.51294 33.664C6.21427 36.1387 6.23561 38.1013 6.57694 39.552C6.96094 40.96 7.68628 41.664 8.75294 41.664C9.73428 41.664 10.8009 41.3013 11.9529 40.576C13.1049 39.8507 14.3423 38.5493 15.6649 36.672C17.0303 34.6667 18.3529 32.064 19.6329 28.864C20.9556 25.6213 22.1289 21.8667 23.1529 17.6C23.4089 16.6187 23.8783 15.9573 24.5609 15.616C25.2863 15.2747 26.0329 15.2107 26.8009 15.424C27.5689 15.6373 28.1876 16.064 28.6569 16.704C29.1263 17.3013 29.2543 18.0693 29.0409 19.008C27.9316 23.616 27.3769 27.5627 27.3769 30.848C27.4196 34.1333 27.7609 36.5227 28.4009 38.016C28.8703 39.0827 29.4249 39.8507 30.0649 40.32C30.7476 40.7893 31.4943 41.024 32.3049 41.024C33.1156 41.024 33.9689 40.7253 34.8649 40.128C35.8036 39.488 36.7209 38.4 37.6169 36.864C38.5556 35.328 39.3876 33.216 40.1129 30.528C37.6809 28.48 35.6756 25.7707 34.0969 22.4C32.5183 19.0293 31.7289 15.168 31.7289 10.816C31.7289 8.93867 31.9423 7.21067 32.3689 5.632C32.7956 4.05333 33.5209 2.79467 34.5449 1.856C35.5689 0.874666 36.9769 0.383999 38.7689 0.383999C40.9449 0.383999 42.7156 1.17333 44.0809 2.752C45.4463 4.288 46.4489 6.37867 47.0889 9.024C47.7289 11.6267 48.0063 14.5493 47.9209 17.792C47.8783 21.0347 47.5369 24.3413 46.8969 27.712C47.5369 28.0107 48.2196 28.2453 48.9449 28.416C49.7129 28.5867 50.4809 28.672 51.2489 28.672C52.9983 28.672 54.7903 28.416 56.6249 27.904C58.5023 27.3493 60.1023 26.6453 61.4249 25.792C62.2783 25.2373 63.0676 25.088 63.7929 25.344C64.5183 25.5573 65.0943 26.0053 65.521 26.688C65.9476 27.328 66.1183 28.0533 66.0329 28.864C65.9903 29.632 65.5636 30.272 64.7529 30.784C62.8756 32.0213 60.7423 33.0027 58.3529 33.728C56.0063 34.4533 53.6383 34.816 51.2489 34.816C49.2863 34.816 47.3449 34.4533 45.4249 33.728C44.1876 37.7387 42.5023 40.96 40.3689 43.392C38.2356 45.824 35.5476 47.04 32.3049 47.04C30.2569 47.04 28.3583 46.4427 26.6089 45.248C24.9023 44.0107 23.6223 42.4107 22.7689 40.448C22.5983 40.064 22.4276 39.6587 22.2569 39.232C22.1289 38.8053 22.0223 38.4 21.9369 38.016C21.7236 38.4 21.4889 38.7627 21.2329 39.104C21.0196 39.4453 20.7849 39.7867 20.5289 40.128C18.9503 42.3467 17.1796 44.16 15.2169 45.568C13.2969 46.976 11.1423 47.68 8.75294 47.68ZM41.5849 23.104C42.0116 19.9893 42.1183 17.3653 41.9049 15.232C41.6916 13.0987 41.3503 11.392 40.8809 10.112C40.4116 8.78933 39.9423 7.85067 39.4729 7.296C39.0463 6.69867 38.8116 6.4 38.7689 6.4C38.7689 6.4 38.6836 6.42133 38.5129 6.464C38.3849 6.464 38.2356 6.76267 38.0649 7.36C37.9369 7.91467 37.8729 9.06667 37.8729 10.816C37.8729 12.992 38.1929 15.168 38.8329 17.344C39.4729 19.4773 40.3903 21.3973 41.5849 23.104Z"
439:                               fill="white"
440:                             />
441:                             <path
442:                               d="M91.5429 48.768C89.5376 48.768 87.9163 48.3627 86.6789 47.552C85.4843 46.784 84.6096 45.76 84.0549 44.48C83.5003 43.1573 83.2016 41.7493 83.1589 40.256C81.3243 42.4747 79.2763 44.224 77.0149 45.504C74.7963 46.7413 72.4709 47.36 70.0389 47.36C68.1189 47.36 66.3056 46.912 64.5989 46.016C62.8923 45.0773 61.5056 43.6907 60.4389 41.856C59.4149 39.9787 58.9029 37.6107 58.9029 34.752C58.9029 31.7653 59.5216 28.8427 60.7589 25.984C62.0389 23.0827 63.7669 20.48 65.9429 18.176C68.1616 15.8293 70.6789 13.9733 73.4949 12.608C76.3536 11.2 79.3403 10.496 82.4549 10.496C84.5029 10.496 86.5296 10.752 88.5349 11.264C90.5403 11.776 92.2896 12.5227 93.7829 13.504C94.6363 14.0587 95.1056 14.72 95.1909 15.488C95.2763 16.256 95.0843 16.9813 94.6149 17.664C94.1883 18.304 93.6123 18.752 92.8869 19.008C92.1616 19.264 91.3936 19.136 90.5829 18.624C89.7723 18.112 88.5563 17.6427 86.9349 17.216C85.3563 16.7467 83.8629 16.512 82.4549 16.512C80.0229 16.512 77.7616 17.0667 75.6709 18.176C73.5803 19.2853 71.7243 20.736 70.1029 22.528C68.5243 24.32 67.2869 26.2827 66.3909 28.416C65.4949 30.5493 65.0469 32.6613 65.0469 34.752C65.0469 35.8187 65.1749 36.864 65.4309 37.888C65.7296 38.8693 66.2416 39.7013 66.9669 40.384C67.6923 41.024 68.7163 41.344 70.0389 41.344C71.3189 41.344 72.7483 40.9173 74.3269 40.064C75.9483 39.168 77.4843 37.76 78.9349 35.84C79.8309 34.6453 80.7696 33.216 81.7509 31.552C82.7323 29.8453 83.6283 28.16 84.4389 26.496C85.2923 24.7893 85.9749 23.3387 86.4869 22.144C86.8283 21.2907 87.3403 20.736 88.0229 20.48C88.7483 20.224 89.4736 20.224 90.1989 20.48C90.9243 20.6933 91.5003 21.0987 91.9269 21.696C92.3536 22.2933 92.4816 23.04 92.3109 23.936L89.4949 37.632C89.1963 39.1253 89.1963 40.2347 89.4949 40.96C89.7936 41.6853 90.1776 42.176 90.6469 42.432C91.1163 42.6453 91.4149 42.752 91.5429 42.752C92.2256 42.752 93.1003 42.432 94.1669 41.792C95.2336 41.1093 96.5563 39.8507 98.1349 38.016C99.4576 36.5227 100.823 34.7733 102.231 32.768C103.682 30.72 105.068 28.6293 106.391 26.496C107.756 24.32 108.972 22.272 110.039 20.352C111.148 18.3893 112.023 16.768 112.663 15.488C113.09 14.592 113.687 14.0587 114.455 13.888C115.223 13.7173 115.948 13.824 116.631 14.208C117.356 14.5493 117.868 15.0827 118.167 15.808C118.508 16.4907 118.466 17.28 118.039 18.176C117.356 19.584 116.439 21.2907 115.287 23.296C114.178 25.3013 112.919 27.4347 111.511 29.696C110.146 31.9147 108.695 34.0907 107.159 36.224C105.666 38.3573 104.194 40.2773 102.743 41.984C101.036 43.9467 99.2869 45.568 97.4949 46.848C95.7456 48.128 93.7616 48.768 91.5429 48.768Z"
443:                               fill="white"
444:                             />
445:                             <path
446:                               d="M118.45 48.448C115.549 48.448 113.351 47.6373 111.858 46.016C110.407 44.352 109.533 42.0267 109.234 39.04C108.978 36.0533 109.17 32.5547 109.81 28.544C110.493 24.5333 111.517 20.16 112.882 15.424C113.181 14.4427 113.693 13.8027 114.418 13.504C115.143 13.1627 115.89 13.12 116.658 13.376C117.426 13.632 118.023 14.08 118.45 14.72C118.919 15.36 119.026 16.1493 118.77 17.088C117.191 22.464 116.146 26.8373 115.634 30.208C115.165 33.536 115.037 36.096 115.25 37.888C115.463 39.6373 115.869 40.832 116.466 41.472C117.106 42.112 117.767 42.432 118.45 42.432C119.303 42.432 120.413 41.9413 121.778 40.96C123.143 39.936 124.594 38.5067 126.13 36.672C127.666 34.8373 129.138 32.7253 130.546 30.336C129.778 27.904 129.394 25.152 129.394 22.08C129.394 20.2027 129.501 18.176 129.714 16C129.97 13.7813 130.397 11.6907 130.994 9.728C131.634 7.76533 132.509 6.18667 133.618 4.992C134.77 3.79733 136.242 3.264 138.034 3.392C139.485 3.52 140.573 4.032 141.298 4.928C142.066 5.824 142.535 6.95467 142.706 8.32C142.919 9.68533 142.941 11.1573 142.77 12.736C142.599 14.272 142.343 15.808 142.002 17.344C141.661 18.8373 141.319 20.16 140.978 21.312C139.954 24.8107 138.781 28.032 137.458 30.976C138.61 33.024 140.061 34.432 141.81 35.2C143.559 35.968 145.33 36.2453 147.122 36.032C148.914 35.776 150.45 35.2427 151.73 34.432C152.583 33.8773 153.373 33.728 154.098 33.984C154.823 34.1973 155.399 34.6453 155.826 35.328C156.295 35.968 156.487 36.6933 156.402 37.504C156.317 38.272 155.869 38.912 155.058 39.424C152.967 40.7893 150.642 41.6427 148.082 41.984C145.565 42.3253 143.09 42.0907 140.658 41.28C138.226 40.4693 136.093 39.04 134.258 36.992C132.039 40.576 129.586 43.392 126.898 45.44C124.253 47.4453 121.437 48.448 118.45 48.448ZM135.666 18.112C136.391 15.5947 136.882 13.7173 137.138 12.48C137.394 11.2427 137.522 10.432 137.522 10.048C137.522 9.62133 137.522 9.408 137.522 9.408C137.522 9.408 137.394 9.68533 137.138 10.24C136.882 10.752 136.605 11.648 136.306 12.928C136.007 14.1653 135.794 15.8933 135.666 18.112Z"
447:                               fill="white"
448:                             />
449:                             <path
450:                               d="M164.834 48.512C161.762 48.512 159.117 47.808 156.898 46.4C154.68 44.9493 152.973 43.008 151.778 40.576C150.584 38.1013 149.986 35.328 149.986 32.256C149.986 29.2267 150.562 26.3893 151.714 23.744C152.866 21.056 154.36 18.7093 156.194 16.704C158.072 14.656 160.056 13.0773 162.146 11.968C164.28 10.816 166.306 10.24 168.226 10.24C169.762 10.24 171.17 10.5387 172.45 11.136C173.73 11.7333 174.754 12.5867 175.522 13.696C176.333 14.8053 176.738 16.1493 176.738 17.728C176.738 20.0747 176.034 22.1227 174.626 23.872C173.261 25.5787 171.384 27.4773 168.994 29.568C167.202 31.1467 165.325 32.64 163.362 34.048C161.4 35.456 159.352 36.8427 157.218 38.208C158.584 41.0667 161.122 42.496 164.834 42.496C165.858 42.496 166.946 42.3467 168.098 42.048C169.25 41.7067 170.552 41.024 172.002 40C173.453 38.976 175.16 37.376 177.122 35.2C177.762 34.4747 178.466 34.1333 179.234 34.176C180.045 34.2187 180.749 34.5173 181.346 35.072C181.944 35.584 182.285 36.2453 182.37 37.056C182.498 37.824 182.242 38.5707 181.602 39.296C178.445 42.7947 175.458 45.2053 172.642 46.528C169.869 47.8507 167.266 48.512 164.834 48.512ZM156.13 31.744C157.752 30.6773 159.309 29.6107 160.802 28.544C162.296 27.4347 163.704 26.2827 165.026 25.088C167.245 23.1253 168.738 21.504 169.506 20.224C170.317 18.9013 170.722 18.0693 170.722 17.728C170.722 17.5573 170.594 17.28 170.338 16.896C170.082 16.4693 169.378 16.256 168.226 16.256C167.16 16.256 165.944 16.6613 164.578 17.472C163.256 18.24 161.954 19.328 160.674 20.736C159.437 22.144 158.392 23.7867 157.538 25.664C156.685 27.5413 156.216 29.568 156.13 31.744Z"
451:                               fill="white"
452:                             />
453:                             <path
454:                               d="M201.487 13.248C204.773 13.248 207.717 13.9733 210.319 15.424C212.922 16.8747 214.949 18.9013 216.399 21.504C217.893 24.1067 218.639 27.1147 218.639 30.528C218.639 33.9413 217.893 36.9707 216.399 39.616C214.949 42.2187 212.922 44.2453 210.319 45.696C207.717 47.1467 204.773 47.872 201.487 47.872C198.97 47.872 196.666 47.3813 194.575 46.4C192.485 45.4187 190.757 43.9893 189.391 42.112V47.488H183.503V0H189.647V18.688C191.013 16.896 192.719 15.552 194.767 14.656C196.815 13.7173 199.055 13.248 201.487 13.248ZM200.975 42.496C203.151 42.496 205.093 42.0053 206.799 41.024C208.549 40 209.914 38.592 210.895 36.8C211.919 34.9653 212.431 32.8747 212.431 30.528C212.431 28.1813 211.919 26.112 210.895 24.32C209.914 22.4853 208.549 21.0773 206.799 20.096C205.093 19.1147 203.151 18.624 200.975 18.624C198.842 18.624 196.901 19.1147 195.151 20.096C193.402 21.0773 192.037 22.4853 191.055 24.32C190.074 26.112 189.583 28.1813 189.583 30.528C189.583 32.8747 190.074 34.9653 191.055 36.8C192.037 38.592 193.402 40 195.151 41.024C196.901 42.0053 198.842 42.496 200.975 42.496Z"
455:                               fill="white"
456:                             />
457:                             <path
458:                               d="M256.568 13.568V47.488H250.68V42.112C249.315 43.9893 247.587 45.4187 245.496 46.4C243.406 47.3813 241.102 47.872 238.584 47.872C235.299 47.872 232.355 47.1467 229.752 45.696C227.15 44.2453 225.102 42.2187 223.608 39.616C222.158 36.9707 221.432 33.9413 221.432 30.528C221.432 27.1147 222.158 24.1067 223.608 21.504C225.102 18.9013 227.15 16.8747 229.752 15.424C232.355 13.9733 235.299 13.248 238.584 13.248C241.016 13.248 243.256 13.7173 245.304 14.656C247.352 15.552 249.059 16.896 250.424 18.688V13.568H256.568ZM239.096 42.496C241.23 42.496 243.171 42.0053 244.92 41.024C246.67 40 248.035 38.592 249.016 36.8C249.998 34.9653 250.488 32.8747 250.488 30.528C250.488 28.1813 249.998 26.112 249.016 24.32C248.035 22.4853 246.67 21.0773 244.92 20.096C243.171 19.1147 241.23 18.624 239.096 18.624C236.92 18.624 234.958 19.1147 233.208 20.096C231.502 21.0773 230.136 22.4853 229.112 24.32C228.131 26.112 227.64 28.1813 227.64 30.528C227.64 32.8747 228.131 34.9653 229.112 36.8C230.136 38.592 231.502 40 233.208 41.024C234.958 42.0053 236.92 42.496 239.096 42.496Z"
459:                               fill="white"
460:                             />
461:                             <path
462:                               d="M283.745 13.248C288.055 13.248 291.468 14.5067 293.985 17.024C296.545 19.4987 297.825 23.1467 297.825 27.968V47.488H291.681V28.672C291.681 25.3867 290.892 22.912 289.313 21.248C287.735 19.584 285.473 18.752 282.529 18.752C279.201 18.752 276.577 19.7333 274.657 21.696C272.737 23.616 271.777 26.3893 271.777 30.016V47.488H265.633V13.568H271.521V18.688C272.759 16.9387 274.423 15.5947 276.513 14.656C278.647 13.7173 281.057 13.248 283.745 13.248ZM319.82 31.68L312.78 38.208V47.488H306.636V0H312.78V30.464L331.276 13.568H338.7L324.428 27.584L340.108 47.488H332.556L319.82 31.68Z"
463:                               fill="white"
464:                             />
465:                           </svg>
466:                         </div>
467: 
468:                         {/* Double intersecting circle Brand Logo - bottom right corner */}
469:                         <div className="absolute right-5 sm:right-6 bottom-5 sm:bottom-6 flex -space-x-3 items-center opacity-90">
470:                           <div className="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-white/20 backdrop-blur-[1px] border border-white/10" />
471:                           <div className="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-white/35 backdrop-blur-[1px] border border-white/10" />
472:                         </div>
473:                       </div>
474:                     </div>
475:                   );
476:                 }
477: 
478:                 // Back face slice
479:                 if (isBackFace) {
480:                   const backBorderStyle = "border border-white/15";
481:                   const details = CARD_DETAILS[i % CARD_DETAILS.length];
482:                   return (
483:                     <div
484:                       key={layerIdx}
485:                       className={`absolute inset-0 rounded-[16px] ${backBorderStyle} pointer-events-none overflow-hidden`}
486:                       style={{
487:                         backgroundColor: baseBgColor,
488:                         transform: `translateZ(${zOffset}px) rotateX(180deg)`,
489:                         backfaceVisibility: 'hidden',
490:                         boxShadow: 'inset 0 1px 1px rgba(255,255,255,0.15)',
491:                       }}
492:                     >
493:                       {/* Render Video with premium 16px blur on the back face of the card */}
494:                       <div className="absolute inset-0 pointer-events-none" style={{ filter: 'blur(16px)', transform: 'scale(1.15)' }}>
495:                         <video
496:                           src={videoSrc}
497:                           autoPlay
498:                           loop
499:                           muted
500:                           playsInline
501:                           className="absolute inset-0 w-full h-full object-cover"
502:                         />
503:                       </div>
504: 
505:                       {/* Premium Real Magnetic stripe */}
506:                       <div className="absolute left-0 right-0 top-4 sm:top-5 h-7 sm:h-9 bg-black/85 backdrop-blur-md z-10" />
507: 
508:                       {/* Card holder info and details on the bottom-left */}
509:                       <div 
510:                         className="absolute left-4 sm:left-6 bottom-4 sm:bottom-5 z-20 flex flex-col gap-0.5 sm:gap-1 text-left"
511:                         style={{ fontFamily: '"JetBrains Mono", monospace' }}
512:                       >
513:                         {/* Card Number */}
514:                         <div className="font-mono text-[10px] sm:text-[12px] font-medium tracking-[0.14em] text-white select-none">
515:                           {details.number}
516:                         </div>
517:                         {/* Owner & CVV */}
518:                         <div className="font-mono text-[7px] sm:text-[9px] font-medium text-white/70 tracking-wide flex items-center gap-2 select-none">
519:                           <span className="uppercase">{details.name}</span>
520:                           <span className="text-white/40 font-light">•</span>
521:                           <span>CVV: {details.cvv}</span>
522:                         </div>
523:                       </div>
524:                     </div>
525:                   );
526:                 }
527: 
528:                 return null;
529:               })}
530:             </div>
531:           ))}
532:         </div>
533:       </div>
534:     </div>
535:   );
536: }
```

---

## 97. Arceage Stats

- **Category**: Stats
- **Type**: stats
- **Page Type**: hero
- **ID**: `arceage-stats`

```
Create a React + Tailwind CSS v4 + Motion (framer-motion successor) stats section component. Use Vite as the bundler. The section should be fully mobile responsive.

### Fonts

Import from Google Fonts in your global CSS:
```
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Instrument+Serif:ital@0;1&display=swap');
```

Define two Tailwind v4 theme fonts:
- `--font-sans: "Barlow", ui-sans-serif, system-ui, sans-serif;` (used as the primary UI font via `font-sans`)
- `--font-dm-serif: "Instrument Serif", serif;` (used as the accent/poetic font via `font-dm-serif`)

The page wrapper uses `bg-black font-sans text-white`.

### Dependencies

- `react` v19
- `motion` (npm package "motion", imported as `motion/react` -- provides `motion`, `useInView`, `animate`)
- `tailwindcss` v4 with `@tailwindcss/vite` plugin
- Vite v6+

### Section Layout

The section is a `<section>` with:
- `id="stats"`
- Classes: `bg-black text-white py-8 md:py-24 px-6 md:px-12 lg:px-[120px] w-full border-t border-white/10 overflow-hidden`
- Inner wrapper: `w-full max-w-[1440px] mx-auto`
- Content is a two-column flexbox: `flex flex-col lg:flex-row gap-16 lg:gap-[160px] items-stretch`

### Left Column (flex-1, flex flex-col justify-start)

The entire left column is wrapped in a `motion.div` with staggered reveal animation:
- `initial="hidden"`, `whileInView="visible"`, `viewport={{ once: true, margin: "-100px" }}`
- Variants: hidden = `{ opacity: 0 }`, visible = `{ opacity: 1, transition: { staggerChildren: 0.06 } }`

**Heading (h2):**
- Classes: `text-[clamp(1.5rem,4vw,3.5rem)] font-medium tracking-tight mb-6 leading-[1.1] w-[590px] max-w-full`
- Content uses a custom `<Typewriter>` component (described below):
  - `<Typewriter text="Powering Harvests" delay={0} speed={0.012} />` followed by `<br />`
  - `<Typewriter text="that " delay={0.25} speed={0.012} />` then a `<span className="font-dm-serif italic font-normal">` wrapping `<Typewriter text="Maximize Your Yield" delay={0.35} speed={0.012} />`
- The phrase "Maximize Your Yield" renders in Instrument Serif italic as the accent font.

**Subtitle (p):**
- Classes: `text-base md:text-lg text-white/40 leading-relaxed font-light max-w-lg whitespace-normal mb-16`
- Content: `<Typewriter text="For over a decade, the region's most demanding agricultural operations have relied on our modern machinery and skilled crews to secure their crops efficiently and reduce loss." delay={0.1} speed={0.012} />`

**Stats Grid:**
- Wrapped in `motion.div` with stagger variants: hidden = `{ opacity: 0 }`, visible = `{ opacity: 1, transition: { staggerChildren: 0.06, delayChildren: 0.1 } }`
- Classes: `grid grid-cols-2 md:grid-cols-[max-content_max-content] gap-8 md:gap-x-16 lg:gap-x-24`
- 5 stat items, each wrapped in `motion.div` with variants: hidden = `{ opacity: 0, y: 20 }`, visible = `{ opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } }`
- Each stat item (`flex flex-col`):
  - **Number:** `text-4xl md:text-5xl lg:text-[56px] font-dm-serif tracking-tight mb-3` (uses Instrument Serif)
  - **Label:** `text-[10px] md:text-xs font-semibold text-white/40 uppercase tracking-wider`

The 5 stats with their AnimatedCounter props:
1. `value={500} suffix="K+"` / Label: "Acres Harvested Annually"
2. `value={99.8} decimals={1} suffix="%"` / Label: "Crop Recovery Rate"
3. `value={50} suffix="+"` / Label: "Modern Combines Deployed"
4. `value={15} suffix="+"` / Label: "Crop Varieties Supported"
5. `value={24} suffix="/7"` / Label: "Uptime During Season"

### AnimatedCounter Component

A helper component that animates from 0 to a target value on scroll into view:
- Props: `value: number`, `suffix?: string` (default ""), `prefix?: string` (default ""), `decimals?: number` (default 0)
- Uses `useRef<HTMLSpanElement>`, `useInView(ref, { once: true, margin: "-50px" })` from `motion/react`
- On `inView`, calls `animate(0, value, { duration: 1.5, ease: "easeOut", onUpdate(val) { ref.current.textContent = prefix + val.toFixed(decimals) + suffix } })`
- Returns `<span ref={ref}>{prefix}0{suffix}</span>` as initial render

### Typewriter Component

A reusable character-by-character reveal animation triggered on scroll:
- Props: `text: string`, `delay?: number` (default 0), `speed?: number` (default 0.015), `className?: string` (default "")
- Uses `useRef`, `useInView(ref, { once: true, margin: "-10px" })` from `motion/react`
- Renders a `motion.span` with `initial="hidden"` and `animate={inView ? "visible" : "hidden"}`
- Parent variants: hidden = `{ opacity: 1 }`, visible = `{ opacity: 1, transition: { staggerChildren: speed, delayChildren: delay } }`
- Splits text into individual characters, each wrapped in `motion.span` with variants: hidden = `{ opacity: 0 }`, visible = `{ opacity: 1 }`

### Right Column: Logo-Masked Video

- Wrapper: `flex justify-center lg:justify-end items-center shrink-0 lg:w-1/2`
- Inner `motion.div`:
  - `initial={{ opacity: 0, scale: 0.9 }}`
  - `whileInView={{ opacity: 1, scale: 1.2 }}`
  - `viewport={{ once: true, margin: "-100px" }}`
  - `transition={{ duration: 0.8, delay: 0, ease: "easeOut" }}`
  - Classes: `w-full max-w-[500px] lg:max-w-none lg:w-[120%] aspect-square origin-center`
  - Uses CSS `mask-image` (both `-webkit-mask-image` and `mask-image`) with an inline SVG data URI of a triangular/mountain-like logo shape. The exact SVG path data:
    ```
    m53.54,45.42c2.19-3.79,7.67-3.79,9.86,0l4.54,7.87c1.17,2.02,1.17,4.51,0,6.54l-8.15,13.81c-1.68,2.91.42,6.55,3.78,6.55h17.81c3.45,0,5.61-3.74,3.89-6.73l-28.76-49.81c-2.95-5.12-10.34-5.12-13.29,0l-28.46,49.3c-1.86,3.22.46,7.24,4.18,7.24h10.23c2.55,0,4.91-1.36,6.19-3.57l18.18-31.19Z
    ```
  - SVG viewBox: `0 0 100 100`
  - Mask properties: `maskSize: 'contain'`, `maskRepeat: 'no-repeat'`, `maskPosition: 'center'`
  - Full inline style object:
    ```js
    {
      WebkitMaskImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='m53.54,45.42c2.19-3.79,7.67-3.79,9.86,0l4.54,7.87c1.17,2.02,1.17,4.51,0,6.54l-8.15,13.81c-1.68,2.91.42,6.55,3.78,6.55h17.81c3.45,0,5.61-3.74,3.89-6.73l-28.76-49.81c-2.95-5.12-10.34-5.12-13.29,0l-28.46,49.3c-1.86,3.22.46,7.24,4.18,7.24h10.23c2.55,0,4.91-1.36,6.19-3.57l18.18-31.19Z'/%3E%3C/svg%3E")`,
      WebkitMaskSize: 'contain',
      WebkitMaskRepeat: 'no-repeat',
      WebkitMaskPosition: 'center',
      maskImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='m53.54,45.42c2.19-3.79,7.67-3.79,9.86,0l4.54,7.87c1.17,2.02,1.17,4.51,0,6.54l-8.15,13.81c-1.68,2.91.42,6.55,3.78,6.55h17.81c3.45,0,5.61-3.74,3.89-6.73l-28.76-49.81c-2.95-5.12-10.34-5.12-13.29,0l-28.46,49.3c-1.86,3.22.46,7.24,4.18,7.24h10.23c2.55,0,4.91-1.36,6.19-3.57l18.18-31.19Z'/%3E%3C/svg%3E")`,
      maskSize: 'contain',
      maskRepeat: 'no-repeat',
      maskPosition: 'center',
    }
    ```

- Inside the masked div, a `<video>` element:
  - Attributes: `autoPlay`, `loop`, `muted`, `playsInline`
  - Classes: `w-full h-full object-cover`
  - Source: `https://app-uploads.krea.ai/wan-videos/7f348c17-c3aa-40c9-9d5b-a2bed9a72c2e.mp4` (type `video/mp4`)

### Mobile Responsiveness Summary

- Section padding: `py-8 px-6` on mobile, `md:py-24 md:px-12`, `lg:px-[120px]`
- Layout stacks vertically on mobile (`flex-col`), goes side-by-side at `lg:` (`flex-row`)
- Heading uses fluid typography: `clamp(1.5rem, 4vw, 3.5rem)`
- Stats grid: 2 columns on mobile (`grid-cols-2`), auto-sized on `md:` (`grid-cols-[max-content_max-content]`)
- Stat numbers: `text-4xl` on mobile, `md:text-5xl`, `lg:text-[56px]`
- Video mask: `max-w-[500px]` on mobile, full width at `lg:` with `lg:w-[120%]`

---
```

---

## 98. Neon Logic

- **Category**: Landing Page
- **Type**: hero
- **Page Type**: hero
- **ID**: `neon-logic`

```
Build a single-page landing site for "SynapseX" -- a futuristic neural-AI interface product. The entire site uses a black background with white text and full-viewport video backgrounds. The primary font is "Space Mono" (monospace) for all text. Use React + TypeScript + Vite + Tailwind CSS + Framer Motion.

### Fonts & External Assets

- **Primary font:** "Space Mono" (all weights: 400, 700, italic) from Google Fonts
- **Display font (background watermark only):** "Anton SC" from Google Fonts
- **Icons:** Bootstrap Icons CDN (`https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css`) -- used only for the Apple icon (`bi bi-apple`) in the download button
- **All Tailwind `fontFamily` keys** (`sans`, `serif`, `mono`) are overridden to `"Space Mono", monospace`

### Video URLs (CloudFront -- use exactly these)

1. **Hero (mouse-scrubbed, NOT autoplay):**
   `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_083515_290e5a10-0b95-41af-a5e2-32b6389baa4d.mp4`

2. **Second Section (autoplay, muted, loop):**
   `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_092455_089c54f8-3b03-4966-9df1-e9746063d0ef.mp4`

3. **Metrics Section (autoplay, muted, loop):**
   `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_095810_ecea3dd2-fc5e-4e41-8696-4219290b6589.mp4`

4. **Technology Section (autoplay, muted, loop):**
   `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_095750_32a52ce0-2005-45c9-9093-41f03fde9530.mp4`

5. **Footer (autoplay, muted, loop):**
   `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_080203_fd7f4f85-3a86-4837-8192-85e7bfe68e75.mp4`

### Dependencies

```json
"framer-motion": "^12.40.0",
"lucide-react": "^0.344.0",
"react": "^18.3.1",
"react-dom": "^18.3.1"
```

### Global CSS (`index.css`)

- Import Space Mono from Google Fonts
- Import Bootstrap Icons CSS
- Tailwind directives (`@tailwind base/components/utilities`)
- CSS variables: all `--font-*` set to `"Space Mono", monospace`
- Global reset: `* { margin: 0; padding: 0; box-sizing: border-box; }`
- `html, body`: `background: #000; color: #fff; overflow-x: hidden; overflow-y: auto; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`
- Lenis smooth scroll utility classes (`.lenis.lenis-smooth`, `.lenis.lenis-stopped`, `.lenis.lenis-scrolling iframe`)

### Custom Text Animation Components

#### 1. `ScrambleIn` -- entrance reveal animation
- Props: `text: string`, `delay: number` (ms before start), `triggered: boolean`
- Character set: `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~|}{[]:;?><`
- On trigger (after delay): runs interval every 25ms, revealing characters left-to-right at 0.5 chars/frame
- Characters not yet revealed show random chars (up to 3 ahead of the reveal cursor); characters beyond that are empty
- Spaces always show as spaces
- Before triggered: renders `&nbsp;`

#### 2. `ScrambleText` -- hover-driven scramble
- Props: `text: string`, `isHovered: boolean`, `className?: string`
- On hover: scrambles all chars with random chars, then reveals left-to-right at 4 frames/char, interval 25ms
- On unhover: immediately resets to original text

### Custom SVG Logo (`SynapseXLogo`)

A 4-fold rotationally symmetric abstract shape rendered in an SVG with `viewBox="-50 -50 100 100"`. Each quadrant is the same path rotated 0/90/180/270 degrees:

```
M 1.5,23 L 1.5,33 C 1.5,38.5 6,43 11.5,43 L 16.5,43 C 22,43 26.5,38.5 26.5,33 Q 28,28 33,26.5 C 38.5,26.5 43,22 43,16.5 L 43,11.5 C 43,6 38.5,1.5 33,1.5 L 23,1.5 Q 12,12 1.5,23 Z
```

### Animated Hamburger (`SquashHamburger`)

- 3 horizontal bars (absolute positioned spans)
- Desktop: container 18x12px, bar height 1.5px
- Mobile: container 15x10px, bar height 1.2px
- On open: top bar rotates 45deg + translates down to center; middle bar fades/scales out; bottom bar rotates -45deg + translates up to center
- Spring animation: stiffness 300, damping 20

---

### Page Sections (in order)

---

#### SECTION 1: Hero (full viewport height)

- **Background:** Video #1, `object-cover`, paused on load. Controlled by mouse-scrub: horizontal mouse movement across viewport scrubs the video timeline forward/backward. Sensitivity factor: `0.8`. Uses `seeked` event to chain seeks without dropping frames.
- **Entrance animation:** After 800ms delay, `entranceComplete` state becomes true -- all hero content fades in (opacity 0 -> 1, duration 1s).
- **Dot grid overlay:** `radial-gradient(#ffffff 1px, transparent 1px)` with 24x24px grid, opacity 0.05, pointer-events-none
- **Large background watermark text:** The word "TRANSCENDENCE" in "Anton SC" font, centered vertically (offset +50px from center), `clamp(120px, 30vw, 521px)` font size, uppercase, letter-spacing -4px. Opacity 0.10. Color achieved via `radial-gradient(circle, rgba(142,127,148,0) 0%, #8E7F94 70%)` as `background-clip: text` with transparent fill.
- **Layout:** Flexbox column, padding `px-4 sm:px-6 md:px-8 pt-20 sm:pt-24 pb-8 sm:pb-12`. Content is pushed to the bottom using `flex-1` spacer.
- **Bottom row:** `flex-col gap-6 md:flex-row md:items-end md:justify-between`
  - **Left column** (`flex flex-col gap-4`):
    - **h1** "Brain" / "And Body" (two lines via `<br>`): `text-white font-light leading-[0.95] tracking-[-0.03em] text-[clamp(40px,10vw,100px)]`. Each line uses `ScrambleIn` with delays 200ms and 500ms.
    - **Description paragraph** (motion.p): fade-up animation (y:25->0, opacity 0->1, duration 0.9s, cubic-bezier ease `[0.215, 0.610, 0.355, 1.000]`, delay 0.2s). Text: "Built at the intersection of neuroscience and artificial intelligence. SynapseX continuously maps neural pathways, cognitive load, and physiological states into a single adaptive intelligence layer." Style: `max-w-sm text-[13px] sm:text-[15px] text-white/60 leading-relaxed`
  - **Right h1** "One" / "Network": Same styling as left h1 but with `text-left md:text-right`. ScrambleIn delays: 700ms and 1000ms.

---

#### NAVBAR (fixed, z-50)

- Fixed to top, height 80px (h-20), transparent background, full width
- Fades in with `entranceComplete` (opacity 0->1, duration 0.8s)

**Desktop (hidden below `sm`):**
- Left group: two pills side by side with gap-2
  - **Logo pill:** h-12, px-5, `bg-white/15 backdrop-blur-md rounded-[14px]`. Contains SynapseXLogo (18x18px white) + "SynapseX" text (16px font-medium tracking-tight white). WhileHover: scale 1.02 + bg rgba(255,255,255,0.22). WhileTap: scale 0.98. Hides on `sm` when menu open (`hidden md:flex`), shows normally otherwise.
  - **Expanding menu pill:** Animates width from 48px (closed) to 290px (open) with spring (stiffness 350, damping 28). h-12, `rounded-[14px]`, `bg-white/15 backdrop-blur-md`. Contains:
    - Hamburger button: when closed = 48x48px rounded-[14px]; when open = 36x36px rounded-[11px] with `bg-white/10 hover:bg-white/20 ml-1.5`
    - Nav links (fade in when open, offset x:15->0): "About" and "Metrics" with ScrambleText on hover. 16px font-normal text-white/85 hover:text-white. Smooth-scroll to `window.innerHeight` and `window.innerHeight * 2` respectively.
- Right: **Download button** -- `h-12 px-6 bg-white rounded-full`, black text. Apple icon + "Download" with ScrambleText on hover. WhileHover: scale 1.03 + bg #e2e2e6. WhileTap: scale 0.97.

**Mobile (visible below `sm`):**
- Scaled-down version: h-9 pills, rounded-[10px], smaller text (13px), logo pill animates to width 0 when menu open (spring stiffness 350, damping 28). Menu capsule expands to 100% width when open. Download button: h-9 px-3.5 rounded-full.

---

#### SECTION 2: Cinematic Text (full viewport height)

- **Background:** Video #2, autoplay muted loop, object-cover
- **Top gradient overlay:** 180px height, linear-gradient from `#010103` to transparent, z-10
- **Content:** Centered large paragraph in a `max-w-5xl` container with 3D perspective (400px)
  - Framer Motion: `rotateX(24deg) translateY(${yScaleValue}px) translateZ(15px)` where `yScaleValue` transforms from 60 to -120 based on smooth scroll progress (spring: stiffness 15, damping 32, mass 1.8). Opacity fades in from 0 to 1 between scroll progress 0.3-0.5.
  - Text: "A neural-AI interface built on the architecture of the human nervous system. SynapseX translates synaptic activity into computational intelligence. Every signal becomes measurable, structured, and visible. It continuously reconstructs internal state as a dynamic neural map. Biological noise is filtered into actionable cognitive patterns."
  - Style: `font-sans font-normal text-[22px] sm:text-[30px] md:text-[36px] lg:text-[42px] text-white leading-[1.35] tracking-[-0.02em] select-none px-6 sm:px-12 text-center`

---

#### SECTION 3: Metrics (min-h-screen)

- **Background:** Video #3, autoplay muted loop, object-cover
- **Layout:** Centered content, `pt-32 pb-32 px-6`, max-w-6xl
- **Subtitle:** "Performance Metrics" -- `text-white/40 text-[13px] sm:text-[14px] tracking-[0.2em] uppercase mb-20 text-center`. Fades in on scroll (whileInView, duration 1.2s, once, amount 0.3).
- **Metrics grid:** 3 columns on md, 1 on mobile, gap-16 md:gap-8. Each metric fades up (y:30->0, opacity, duration 0.8s, staggered 0.15s delay per item):
  - "2.4ms" -- Synaptic Latency
  - "99.7%" -- Signal Accuracy
  - "140B" -- Neural Parameters
  - Value: `text-white text-[clamp(48px,10vw,96px)] font-light tracking-[-0.04em] leading-none`
  - Label: `text-white/40 text-[13px] sm:text-[15px] mt-4 tracking-wide`

---

#### SECTION 4: Technology / Adaptive Intelligence (full viewport height)

- **Background:** Video #4, autoplay muted loop, object-cover
- **Layout:** Flexbox column, `px-8 sm:px-12 md:px-16 py-12 sm:py-16`
- **Top area:** flex-col md:flex-row md:justify-between md:items-start gap-6
  - **Left heading:** "Adaptive / Intelligence" (two lines), `text-white font-light text-[clamp(36px,8vw,72px)] leading-[0.95] tracking-[-0.03em]`. Fades up (y:40->0, duration 1.0s, whileInView once amount 0.3).
  - **Right paragraph:** "The system learns your neural baseline within 72 hours. From there, every cognitive state is mapped, predicted, and optimized in real time." `text-white/50 text-[13px] sm:text-[15px] leading-relaxed max-w-xs md:text-right md:pt-2`. Fades up (y:20->0, duration 1.0s, delay 0.2s).
- **Spacer** (`flex-1`)
- **Bottom grid:** 2 cols on mobile, 4 cols on md, gap-8 md:gap-6. Fades in on scroll (duration 1.0s, delay 0.3s). Each item staggered (y:20->0, duration 0.7s, delay i*0.1):
  1. "Cortical Mapping" -- "Real-time spatial reconstruction of active neural regions."
  2. "Signal Isolation" -- "Separates cognitive intent from biological noise."
  3. "State Prediction" -- "Anticipates cognitive transitions before they occur."
  4. "Loop Feedback" -- "Closed-loop adjustment based on outcome correlation."
  - Title: `text-white text-[14px] sm:text-[16px] font-normal mb-2`
  - Desc: `text-white/40 text-[12px] sm:text-[14px] leading-relaxed`

---

#### SECTION 5: Architecture (min-h-screen, pure black background, no video)

- Centered content, max-w-3xl, `px-6 py-32`
- **Heading block** (fades up y:30->0, duration 1.0s, whileInView once amount 0.4):
  - Subtitle: "Architecture" -- `text-white/40 text-[13px] sm:text-[14px] tracking-[0.2em] uppercase mb-8`
  - Heading: "Three layers. Zero friction." -- `text-white font-light text-[clamp(28px,6vw,56px)] leading-[1.15] tracking-[-0.02em] mb-10`
  - Description: "Sensor layer captures raw bioelectric signals. Processing layer isolates intent. Interface layer delivers structured output to any connected system." -- `text-white/45 text-[15px] sm:text-[17px] leading-relaxed max-w-xl mx-auto`
- **Layer cards** (fade in, duration 1.2s, delay 0.4s, whileInView once amount 0.4): 3 stacked cards, `mt-20 flex-col items-center gap-4`. Each card: `max-w-md h-[72px] border border-white/10 rounded-lg flex items-center justify-between px-6`
  - Left: "Layer 1/2/3" -- `text-white/30 text-[12px] tracking-[0.15em] uppercase`
  - Right: "Capture" / "Process" / "Interface" -- `text-white text-[16px] sm:text-[18px] font-light`

---

#### FOOTER

- Black background, overflow hidden
- Two-column layout (stacked on mobile): `flex-col md:flex-row min-h-[400px]`
- **Left:** Video #5, `object-cover`, fills half width (h-[300px] on mobile, auto height on md)
- **Right:** Flex column justify-between, `p-10 sm:p-16`
  - Top: SynapseXLogo (18x18px, text-white/70) + "SynapseX" text (15px font-medium text-white/70 tracking-tight), mb-8. Below: "The next evolution of human-machine interaction. Built for those who refuse to be limited by biology alone." `text-white/40 text-[14px] sm:text-[15px] leading-relaxed max-w-sm`
  - Bottom: "(c) 2026 SynapseX Labs. All rights reserved." `text-white/25 text-[12px] mt-12`

---

### Key Technical Details

- The entire app wrapper has inline style: `fontFamily: '"Space Mono", monospace'`
- All `h-screen` elements also have `h-[100dvh]` for mobile viewport compatibility
- The hero video is NOT autoplay -- it starts paused at time 0 and is scrubbed by horizontal mouse movement (delta-based, not absolute position). The seek logic chains via `seeked` event to avoid frame-dropping.
- Framer Motion `useScroll` tracks the second section with offset `["start end", "end start"]`, piped through `useSpring` (stiffness 15, damping 32, mass 1.8) then `useTransform` and `useMotionTemplate` for the 3D text rotation effect.
- No external state management, no routing, no database -- pure single-page React app.

---
```

---

## 99. Wanderful Hero

- **Category**: Travel
- **Type**: hero
- **Page Type**: hero
- **ID**: `wanderful-hero`

```
Build a full-viewport cinematic hero section for a travel brand called "Wanderful" using React + TypeScript + Vite + Tailwind CSS. Use GSAP for animation and `lucide-react` for icons.

**Fonts (load via Google Fonts in `src/index.css`):**
```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');
```
Also load a custom display font:
```css
@font-face {
  font-family: 'Dirtyline';
  src: url('https://fonts.cdnfonts.com/s/15011/Dirtyline36DaysofType.woff') format('woff');
  font-weight: normal; font-style: normal; font-display: swap;
}
```
Body font: `Barlow`. Hero headings: `Inter`. Body background: `#000`.

**Video background (fixed, full screen, z-0):**
- Use this exact CloudFront URL as the `<video>` src:
  `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260510_060007_60275ce7-030c-4668-a160-8f364ec537d3.mp4`
- Attributes: `autoPlay muted loop playsInline`, `object-cover`, wrapper scaled `scale-[1.08]` with `origin-center`.
- On `onLoadedMetadata`, set `playbackRate = 1.25`.
- Add GSAP-driven mouse parallax: listen to `mousemove`, compute `targetX/Y = ((clientX - cx)/cx) * 20`, lerp `currentX/Y += (target - current) * 0.06` inside `requestAnimationFrame`, and apply via `gsap.set(videoBg, { x, y })`.

**Liquid-glass utility (add to `index.css`):**
```css
.liquid-glass {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%,
    rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%,
    rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

**Header (fixed top, z-50, `px-10 py-8`, flex justify-between items-center):**
- Left: wordmark `Wanderful` followed by `<sup>TM</sup>`, `text-[17px] font-semibold tracking-tight`.
- Center: `<nav>` using `.liquid-glass rounded-full px-2 py-2 flex items-center gap-1`. Links: `JOURNEY`, `BENEFITS`, `JOURNAL`, `GUIDEBOOK`. Each link: `text-[11px] font-medium tracking-[0.12em] text-white/90 hover:text-white px-4 py-1.5 rounded-full transition-colors duration-200`.
- Right: "GET ROAMING" anchor with same `.liquid-glass rounded-full px-5 py-2.5 text-[11px] font-medium tracking-[0.12em] text-white/90 hover:text-white`.

**Hero headline (fixed, `top: 120px`, centered, z-20):**
Two lines, both centered, `Inter` 400, `font-size: clamp(40px, 5.4vw, 72px)`, `line-height: 1.1`, `letter-spacing: -0.02em`:
- Line 1 (white): `Venture without edges.`
- Line 2 (`rgba(255,255,255,0.55)`): `Uncover with keen instinct.`

Fade-in on mount: `opacity 0 → 100` and `translate-y-6 → 0` with `transition-all duration-1000`.

**Bottom block (fixed `bottom-14`, z-20, flex-col items-center gap-6), fade-in with `delay-300`:**
1. Paragraph, `max-w-[620px] text-[15px] leading-relaxed` centered:
   - White: "Our smart itineraries shape around you — your rhythm, your vibe, your hunger for adventure."
   - `text-white/55`: " Each getaway is tailored, seamless, and wholly yours."
2. Button: white bg, black text, `text-[15px] font-medium rounded-full px-8 py-3.5`, hover `scale-[1.03]` + `shadow-[0_0_32px_4px_rgba(255,255,255,0.2)]`, active `scale-[0.97]`. Label: `Plan my escape today`.
3. Row: `Lock` icon from lucide-react (`size={13} strokeWidth={1.5}`) + `text-[11px] font-medium tracking-[0.14em] text-white/70`, text: `SECURE BY DESIGN. ZERO DATA LEAKS.`

**Root container:** `min-h-screen bg-black text-white overflow-x-hidden` with inline `fontFamily: "'Inter', sans-serif"`.

Dependencies: `gsap`, `lucide-react`, `react`, `react-dom`, tailwind configured with content globs `./index.html` and `./src/**/*.{js,ts,jsx,tsx}`.
```

---

## 100. Cybersecurity Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `cybersecurity-hero`

```
Build a **single-page React + TypeScript (Vite)** landing hero for a product called **"Xero"** that recreates the following section exactly. Use the **Inter** Google Font (weights 300, 400, 500, 600, 700, 800). Do not use Tailwind utility classes for the hero — write plain CSS in a global stylesheet. No purple/indigo branding outside the specified pink-magenta gradient arc.

## Layout & Structure

Render three top-level blocks centered on a black page (`#0a0a0f`), each constrained to `max-width: 1600px`, in this vertical order:

1. **`<nav>`** — sticky-style top bar (not actually sticky, just at top)
2. **`<section class="hero-card">`** — the rounded dark hero card with the animated icon pipeline
3. **`<div class="brands">`** — a row of 5 monochrome brand logos

The body uses `display: flex; flex-direction: column; align-items: center; padding: 14px;` and `font-family: 'Inter', sans-serif;`.

### CSS Variables (on `:root`)
```
--bg: #0a0a0f;
--surface: #111118;
--text: #f0f0f5;
--text-muted: #8888a8;
--accent: #c8a0e0;
--accent-pink: #b04090;
--border: rgba(255, 255, 255, 0.08);
```

## NAVBAR

- Grid layout: `grid-template-columns: 1fr auto 1fr; padding: 12px 24px; margin-bottom: 14px;`
- **Left**: `<span class="nav-logo">Xero</span>` — `font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em;`
- **Center**: `<ul class="nav-links">` with three `<a>` items: **Method**, **Pricing**, **Docs**. Color `--text-muted`, `font-size: 0.85rem`, gap 32px, hover transitions to `--text` over 0.2s.
- **Right**: `<div class="nav-actions">` containing two pill buttons:
  - `.btn-login` — `rgba(255,255,255,0.06)` bg, 1px border `--border`, white text, padding `7px 18px`, `border-radius: 999px`, `font-size: 0.82rem`, `font-weight: 500`. Hover: bg `rgba(255,255,255,0.12)`.
  - `.btn-signup` — solid white bg, black `#0a0a0f` text, same dimensions, `font-weight: 600`. Hover: `opacity: 0.88`.
- The `.nav-menu` wrapper uses `display: contents` on desktop so the `ul` and actions become direct grid children.

### Mobile (≤ 768px)
- Nav becomes flex with space-between.
- A `.menu-toggle` hamburger appears: 24×14 button with two 2px-tall white spans. When `.active`, span 1 rotates `translateY(6px) rotate(45deg)` and span 2 rotates `translateY(-6px) rotate(-45deg)` to form an X.
- `.nav-menu.active` slides in from `right: -100%` to `right: 0` over 0.4s `cubic-bezier(0.4, 0, 0.2, 1)` as a full-screen `var(--bg)` overlay with column-stacked links and full-width buttons.
- Toggling sets `document.body.style.overflow = 'hidden'`.

## HERO CARD

Outer `.hero-card` styles:
- `width: 100%; max-width: 1600px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.07); overflow: hidden; position: relative; background: #0d0b12; padding: 80px 40px 70px; min-height: 640px;`
- `display: flex; flex-direction: column; align-items: center; text-align: center;`

### `::before` Gradient Arc (the signature visual)
A radial gradient positioned at `50% -70%` with **many manually-tuned stops** producing a smooth dark→pink→white arc near the top:
```
background:
  radial-gradient(circle at 50% -70%,
    transparent 60%,
    rgba(176,48,136,0.03) 63%,
    rgba(176,48,136,0.08) 65%,
    rgba(176,48,136,0.16) 67%,
    rgba(176,48,136,0.28) 69%,
    rgba(176,48,136,0.40) 71%,
    rgba(176,48,136,0.52) 73%,
    rgba(176,48,136,0.64) 75%,
    rgba(176,48,136,0.74) 77%,
    rgba(176,48,136,0.82) 79%,
    rgba(210,70,175,0.92) 85%,
    rgba(240,110,210,0.88) 87%,
    rgba(255,205,250,0.92) 91%,
    rgba(255,240,255,0.98) 93%,
    #ffffff 95%),
  radial-gradient(circle at 50% 35%, rgba(120,40,180,0.08) 0%, transparent 50%);
z-index: 0; pointer-events: none;
```

### `.hero-grid` Overlay
A separate absolutely-positioned div with crosshatch grid:
```
background-image:
  linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
background-size: 40px 40px;
mask-image: radial-gradient(circle at 50% -70%, transparent 60%, black 78%);
```
This makes the grid only visible inside the arc area.

## ICON PIPELINE (the animated centerpiece)

Container `.icon-pipeline`: `position: relative; display: flex; align-items: center; justify-content: center; max-width: 700px; margin-bottom: 52px; z-index: 1;`

Children in this exact order:

1. **`<svg class="beam-svg">`** — absolutely-positioned over the whole pipeline (`overflow: visible`), containing:
   - A `<filter id="glow">` with `feGaussianBlur stdDeviation="2"` then `feComposite ... operator="over"`.
   - A `<linearGradient id="beam-gradient" gradientUnits="userSpaceOnUse">` with stops:
     - `0%` `#b04090` opacity 0
     - `20%` `#b04090` opacity 0.8
     - `50%` `#fff` opacity 1
     - `80%` `#c8a0e0` opacity 0.8
     - `100%` `#c8a0e0` opacity 0
   - Two `<path>` elements both stroked with `url(#beam-gradient)`:
     - Glow path: `stroke-width="2"`, `filter="url(#glow)"`, `opacity: 0.6`.
     - Core path: `stroke-width="0.8"`.

2. **Left node** `.icon-node.node-light-right` (id `node-stack`) — Lucide-style **layers** SVG (3 stacked diamonds): `<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>`.

3. **`.pipeline-line`** — `width: 160px; height: 1px;` linear gradient `90deg, rgba(255,255,255,0.15), rgba(255,255,255,0.07)`.

4. **Center wrapper** with `position: relative;` containing:
   - **`.splash`** — 100×100 absolutely centered, `border-radius: 50%`, `background: radial-gradient(circle, rgba(255,77,200,0.6) 0%, transparent 70%)`, initial `opacity: 0; transform: scale(0.4); z-index: 2;`
   - **`.icon-node-center`** (id `node-x`) — 64×64 round, `background: #1e1e2c`, neumorphic shadow (see below), containing the **Xero "X" logoipsum** SVG (`viewBox="0 0 40 40"`) — the multi-cut path provided in the source.

5. **`.pipeline-line.right`** — same 160×1 line, gradient reversed.

6. **Right node** `.icon-node.node-light-left` (id `node-shield`) — Lucide-style **shield-check** SVG: `<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>`.

### Side Node Styling
`.icon-node`: 46×46 round, `background: #1a1a24`, `cursor: pointer`, `z-index: 3`, with **neumorphic** shadow stack:
```
box-shadow:
  6px 6px 12px rgba(0,0,0,0.4),
  -4px -4px 10px rgba(255,255,255,0.03),
  inset 1px 1px 1px rgba(255,255,255,0.05),
  inset 4px 4px 8px rgba(0,0,0,0.4);
```
Plus an `::after` dotted outer ring at `inset: -7px` (`border: 1px dotted #1a1a24`).
Hover: `translateY(-1px)` and stronger shadows. Active: inset-only shadows.
Inner SVG: 20×20, stroke `rgba(255,255,255,0.7)`, `stroke-width: 1.5`, fill none, round caps.

### Center Node Styling
`.icon-node-center`: 64×64, `background: #1e1e2c`, similar but stronger neumorphic shadow:
```
8px 8px 16px rgba(0,0,0,0.5),
-6px -6px 14px rgba(255,255,255,0.04),
inset 1px 1px 2px rgba(255,255,255,0.06),
inset 6px 6px 12px rgba(0,0,0,0.5);
```
Inner Xero SVG: 28×28, `fill: white`.

### Side-Light Glows
- `.node-light-right::before` — half-circle radial glow on the right side: `radial-gradient(circle at right, rgba(200,200,200,0.45) 0%, transparent 70%)`, `opacity: 0` default, `opacity: 1` when `.active` (300ms transition).
- `.node-light-left::before` — same but on left, color `rgba(200,100,255,0.5)`.

### Splash Keyframe
```
@keyframes splash-anim {
  0%   { transform: scale(0.4); opacity: 0.8; }
  40%  { opacity: 0.6; }
  100% { transform: scale(1.4); opacity: 0; }
}
```
Triggered by adding `.animate` (0.8s ease-out forwards).

## BEAM ANIMATION (JavaScript / requestAnimationFrame)

Implement a state machine with four phases. On mount and on every window `resize`, recompute the SVG path:

```
const pRect = pipeline.getBoundingClientRect();
const sRect = nodeStack.getBoundingClientRect();
const xRect = nodeX.getBoundingClientRect();
const shRect = nodeShield.getBoundingClientRect();
const startX = sRect.left + sRect.width/2 - pRect.left;
const startY = sRect.top  + sRect.height/2 - pRect.top;
// midX/midY from nodeX, endX/endY from nodeShield
const d = `M ${startX},${startY} L ${midX},${midY} L ${endX},${endY}`;
```
Set this `d` on **both** beam paths.

The gradient is animated by mutating `x1` / `x2` of `#beam-gradient` (in `userSpaceOnUse`) so the bright window slides along. Use `halfWidth = 5` (percentage units), `center = percentage * 100`:
```
gradient.x1 = (center - 5) + '%'
gradient.x2 = (center + 5) + '%'
y1 = y2 = '0%'
```

State machine in a `requestAnimationFrame` loop, tracking `lastStateChange` timestamp:

| State | Duration | Behavior |
|---|---|---|
| **`p1`** | 800 ms | `percentage` interpolates `0 → 0.5`. While `p < 0.4`, add `.active` to `node-stack`; remove after. At end: switch to `splash`, hide both beam paths (`opacity: 0`), add `.animate` to splash. |
| **`splash`** | 800 ms | Wait. After elapsed: switch to `p2`, remove `.animate`, restore `opacity: 1` on both beam paths. |
| **`p2`** | 800 ms | `percentage` interpolates `0.5 → 1.0`. While `p > 0.6`, add `.active` to `node-shield`. At end: remove `.active`, switch to `idle`. |
| **`idle`** | 1000 ms | Wait, then loop back to `p1`. |

Total cycle ≈ 3.4 seconds, infinite.

## HERO TEXT

`.hero-content` `max-width: 620px; z-index: 1;`

```html
<h1 class="hero-heading">
  The simple way
  <strong>encryption your data</strong>
</h1>
<p class="hero-sub">
  Fully managed data encrypting service and annotation<br>
  platform for teams of all industries.
</p>
<a href="#" class="btn-cta">Get Started</a>
```

- `.hero-heading`: `font-size: clamp(2.4rem, 5.5vw, 4rem); font-weight: 300; line-height: 1.1; letter-spacing: -0.02em;`
- `.hero-heading strong`: `display: block; font-weight: 400; margin-top: 4px;` with `background: linear-gradient(to right, #ffffff, #a98597); -webkit-background-clip: text; -webkit-text-fill-color: transparent;`
- `.hero-sub`: 0.9rem, `rgba(255,255,255,0.4)`, `max-width: 440px`, `margin: 0 auto 36px`.
- `.btn-cta`: white pill, black text, `padding: 12px 32px; border-radius: 999px; font-weight: 600;`. Hover: `opacity: 0.9; translateY(-1px)`.

## BRANDS ROW

`.brands`: flex row, `gap: 64px; padding: 32px 24px 10px; flex-wrap: wrap; justify-content: center;`

Five `.brand-item` blocks (each: flex, gap 10, color `rgba(255,255,255,0.35)`, font-size 1.1rem, font-weight 500, white-space nowrap, with a 22×22 SVG):

1. **Expedia** — `<circle cx=12 cy=12 r=10 fill=current /><path fill="var(--bg)" d="M8 9h8v2H8zm0 4h6v2H8z"/>` then text `Expedia`.
2. **asana** — three filled circles: `(12,7,r=4)`, `(5,16,r=3.5)`, `(19,16,r=3.5)`, text `asana`.
3. **zenefits** — three stroked horizontal polylines (lengths 16/8/16) at y=8/12/16, text `zenefits`.
4. **HubSpot** — small filled circle `(15.5,8.5,r=2.5)`, stroked circle `(8.5,8.5,r=2)`, paths connecting them; text `HubSp<span class="hubspot-dot"></span>t` where `.hubspot-dot` is a 6×6 round superscript dot.
5. **loom** — circle `(12,12,r=9)` plus vertical/horizontal/diagonal stroke lines forming a globe-with-X, text `loom`.

## Responsive Breakpoints

- `≤ 860px`: pipeline `gap: 0; margin-bottom: 40px;` `.pipeline-line { width: 80px }`.
- `≤ 768px`: enable mobile hamburger menu, `.icon-node` shrinks to 38×38, `.icon-node-center` to 52×52, `.hero-card { padding: 60px 20px 60px; min-height: auto }`, `.brands { gap: 32px }`.
- `≤ 480px`: `.hero-card { border-radius: 16px }`, `.brands { gap: 24px }`.

## Z-Index Stack (critical for splash/beam layering)

- `0` — gradient arc + grid overlay
- `1` — pipeline container, hero text
- `2` — beam SVG, splash
- `3` — all icon nodes
- `4` — node side-light glows
- `1000-1001` — mobile nav overlay and toggle

Implement all of the above exactly. Use `useRef` for the pipeline, the three nodes, both beam paths, the gradient, and the splash. Use one `useEffect` to set up the resize listener and the `requestAnimationFrame` loop, and clean both up on unmount.
```

---

## 101. Aurora Onboard

- **Category**: Signup
- **Type**: hero
- **Page Type**: hero
- **ID**: `aurora-onboard`

```
Please build a modern, two-column registration interface called "Aurora Sign Up". Use React, Tailwind CSS (v4), `motion/react` (for animations), and `lucide-react` (for icons). The app should be contained entirely in `App.tsx` and `index.css`.

### 1. Global Setup & CSS (`index.css`)
- Import the "Inter" font from Google Fonts (weights 300, 400, 500, 600, 700).
- Extend the Tailwind theme with `--font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;` and a custom color: `--color-brand-gray: #1A1A1A`.
- Apply base styles to the `body`: `@apply font-sans bg-black text-white antialiased;`.

### 2. Main Layout (`App.tsx` container)
- The `<main>` element should have: `flex min-h-screen w-full bg-black selection:bg-white/30 p-2 transition-all duration-500`. 
- On `lg` breakpoints: `lg:h-screen lg:overflow-hidden lg:p-4`.
- Split this container into a Left Column (Hero) and a Right Column (Form).

### 3. Left Column (Hero & Background Video)
- Width on large screens should be exactly `w-[52%]`. It should be hidden on mobile/tablet and only visible `lg:flex`.
- Styles: `relative flex-col items-center justify-end pb-32 px-12 rounded-3xl overflow-hidden shadow-2xl h-full`.
- **Background Video**: Add an absolutely positioned `<video>` tag (`inset-0`, `w-full`, `h-full`, `object-cover`). It must have `autoPlay`, `muted`, `loop`, and `playsInline`. 
- **CRITICAL**: The `<source>` MUST be exactly `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260506_081238_406ed0e3-5d83-436e-a512-0bbff7ec5b95.mp4` (`type="video/mp4"`).
- **CRITICAL**: Do NOT add any dark overlay, gradient, or tint mask over the video. Let it play purely without overlays.
- **Hero Content Container**: Place content over the video (`z-10 w-full max-w-xs space-y-8`).
- **Animations**: Use `motion.div` for a staggered reveal. The container should transition `opacity: 0` to `1` with `staggerChildren: 0.15` and `delayChildren: 0.2`. Every child element inside should fade in and slide up (`y: 10` to `y: 0`, duration `0.5`).
- **Brand/Logo**: A flex row with the `Circle` icon from Lucide (fill-white text-white) and the text "Aurora" (`text-xl font-semibold tracking-tight`).
- **Heading Block**: "Join Aurora" (`text-4xl font-medium tracking-tight whitespace-nowrap`). Below it, a description: "Follow these 3 quick phases to activate your space." (`text-white/60 text-sm leading-relaxed px-4`).
- **Steps**: Render a custom `<StepItem>` component three times. 
  1: "Register your identity" (active state)
  2: "Configure your studio"
  3: "Finalize your profile"

### 4. Right Column (Sign Up Form)
- A container with `flex-1 flex flex-col items-center justify-center py-12 lg:py-6 px-4 sm:px-12 lg:px-16 xl:px-24 overflow-y-auto lg:overflow-hidden`.
- **Animation**: Wrap the interior content in a `motion.div` that fades in (`opacity: 0` to `1`, `duration: 0.8`, `ease: "easeOut"`). Inner width `w-full max-w-xl`, spacing `space-y-8 lg:space-y-6 sm:space-y-10`.
- **Header**: "Create New Profile" (`text-3xl font-medium tracking-tight`). Subtitle: "Input your basic details to begin the journey." (`text-white/40 text-sm`).
- **Social Buttons**: A 2-column grid (`grid grid-cols-2 gap-4`). Render Google (`Chrome` icon) and Github (`Github` icon) using a `<SocialButton>` component.
- **Divider**: A horizontal line (`border-white/10`) with the text "Or" in the center (`bg-black px-4 text-xs font-medium text-white/40 uppercase tracking-widest`).
- **Form Layout**: 
  - First Name and Last Name in a 2-column grid.
  - Email (full width).
  - Password (full width) with a custom `lucide-react` `Eye` toggle icon in the absolute right of the input, and a tiny helper text "Requires at least 8 symbols."
  - **Submit Button**: "Create Account" (`w-full h-14 bg-white text-black font-semibold rounded-xl hover:bg-white/90 active:scale-[0.98] mt-4`).
  - **Footer Link**: "Member of the team? Log in".

### 5. Reusable Components to Create
Create these exact functional components at the bottom of the file:
1. **`<StepItem>`**: Takes `number`, `text`, and an optional `active` boolean.
   - If active: Apply `bg-white text-black border border-white`. The number circle is `bg-black text-white`.
   - If inactive: Apply `bg-brand-gray text-white border-none`. The number circle is `bg-white/10 text-white/40`.
2. **`<SocialButton>`**: Takes `icon` and `label`. Button has `bg-black border border-white/10 rounded-xl hover:bg-white/5`.
3. **`<InputGroup>`**: Takes `label`, `placeholder`, and `type`. The label is `text-sm font-medium text-white`. The input is `bg-brand-gray border-none rounded-xl h-11 px-4 text-white placeholder:text-white/20 focus:ring-2 focus:ring-white/20`.

Ensure the final code uses `export default function App()` at the top.
```

---

## 102. Network Hero

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `network-hero`

```
Create a single-page React + Vite landing page for "Marketeam" -- a marketing talent platform. Use Inter (400, 500, 600, 700) and Urbanist (600, 700) from Google Fonts. The page is a full-viewport hero with a header, left content area, right animated circles visualization, and a bottom logo ticker strip.

---

### Background

Full-page background image covering the entire viewport:
```
https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_111401_56af5012-2263-45d3-849a-8688084d7c2a.png&w=1280&q=85
```
Applied as `background: url(...) center center / cover no-repeat` on the root `.app` container.

---

### Header

- Flexbox row, `justify-content: space-between`, padding `24px 64px`, max-width `1920px`, centered.
- **Left side**: Logo image + nav links
  - Logo: `<img>` with height 32px from: `https://polo-pecan-73837341.figma.site/_assets/v11/17ae538989a509947a8de3892c644664895e69b1.png`
  - Nav links: "Your Team", "Solutions", "Blog", "Pricing" -- color `#000000`, 15px, font-weight 400, with underline animation on hover (scaleX from 0 to 1, transform-origin left, 0.3s ease).
- **Right side**: "Log In" link + "Join Now" button
  - Log In: color `#ffffff`, 15px, weight 500, same underline hover as nav but white.
  - Join Now: pill button (border-radius 50px), black bg (`#000000`), white text, padding `12px 26px`, 15px, weight 500. On hover a `#A068FF` fill slides in from left using `::after` with `translateX(-100%)` to `translateX(0)`, cubic-bezier(0.22, 1, 0.36, 1), 0.4s. Button uses `overflow: hidden`.
  - The button is wrapped in a `.btn-border-wrap` div that has a rotating conic-gradient border using `::before` with `inset: -3px`, `padding: 3px`, mask technique for border-only effect. The gradient is: `conic-gradient(from var(--border-angle), #A068FF, #070319, #A068FF, #070319, #A068FF)`. It rotates via CSS `@property --border-angle` from `0deg` to `360deg` in 3s linear infinite.

---

### Hero Left

- `flex: 0 1 600px`, `padding-top: 40px`
- **Heading**: Typewriter effect, font Urbanist, 64px, weight 600, line-height 64px, letter-spacing -1.5px. Text: "Unlock Top Marketing Talent You Thought Was Out of Reach -- Now Just One Click Away!". The first 67 characters are colored `#000000`, the rest `#ffffff`. A blinking purple cursor (`#A068FF`) appears during typing. Typing speed: 35ms per character, starts after 400ms delay.
- **"Start Project" button**: Same pill style as Join Now but slightly larger (padding `14px 28px`, 16px), bg `#060218`. Has a right-arrow chevron SVG icon (18x18). Hover fill slides from right (`translateX(100%)` to `translateX(0)`). Also wrapped in `.btn-border-wrap` with the same rotating gradient border. Appears after typing finishes (animation-delay 3.2s).
- **Cursor element**: A purple cursor icon (SVG: pointer arrow filled `#A068FF`) + "David" label (pill badge, bg `#A068FF`, white text, 16px, weight 500, padding `8px 16px`, border-radius 20px). Positioned `margin-left: 290px`, `margin-top: 40px`. Appears with animation-delay 3.6s.

---

### Hero Right -- Circles Visualization

- Container: `720x720px`, centered.
- 4 concentric circles (orbits), each rotating slowly:
  - Orbit 1 (innermost): 353px diameter, spins left (counterclockwise) 30s
  - Orbit 2: 501px diameter, spins right 40s
  - Orbit 3: 649px diameter, spins right 50s
  - Orbit 4 (outermost): 797px diameter, spins left 60s
- Each circle has a 1px gradient border: `linear-gradient(180deg, rgba(217, 161, 255, 0) 0%, rgba(217, 161, 255, 1) 43%, rgba(217, 161, 255, 0) 100%)` applied via the mask technique.
- **Center circle (orbit-1)**: Displays an animated count-up number "20k+" (Urbanist 64px, weight 500) and "Specialists" label (Urbanist 16px, weight 600). Counter-rotates to stay upright.
- **Avatars** placed on orbits using `transform: translate(-50%, -50%) rotate(Xdeg) translate(radius) rotate(-Xdeg)`:
  - Avatar images (58px default, some 78px/88px) from these URLs:
    - `https://polo-pecan-73837341.figma.site/_assets/v11/aa51718fb3af3637e6d666b6543fc27a175fada6.png` (orbit 1, at 270deg, 177px radius, square with border-radius 20px, purple glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/ca755f7f93c1126fb8bdbf99ab364a33aa9ab272.png` (orbit 2, at 60deg, 251px, round, yellow glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/dc01064c7093dcc32674876ee3cf5e41c4a485c6.png` (orbit 2, at 180deg, 251px, 78px, pink glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/d5470a58b02388336141575048720f19a50de832.png` (orbit 2, at 300deg, 251px, square border-radius 20px, blue glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/018736aa5d0275c4ce56cfebaf2ae3007d81ca1e.png` (orbit 3, at 130deg, 325px, 88px, pink glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/c76d8a0b99676de31c014344bfaf75bad090758d.png` (orbit 4, at 30deg, 399px, purple glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/7b1b5f039de7b54cc9913e96c1923c3b15a157fa.png` (orbit 4, at 95deg, 399px, 88px, square border-radius 24px, orange glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/9ae171d8895199349755c43fbff00e122221a027.png` (orbit 4, at 220deg, 399px, 88px, square border-radius 24px, pink glow)
    - `https://polo-pecan-73837341.figma.site/_assets/v11/926c9eb7b4bc1df846fa0e39f0b0dc3fefd80671.png` (orbit 4, at 320deg, 399px, purple glow)
  - Each avatar has a staggered fly-in animation (scale 0.3 + rotate -180deg + blur -> normal), delays from 0.6s to 2.3s.

---

### Logo Ticker (Bottom)

- Horizontal infinitely scrolling strip of partner logos, `gap: 64px`, 20s animation.
- Fade masks on left/right edges (linear-gradient mask).
- 5 unique SVG logos repeated 4x for seamless loop:
  - `https://polo-pecan-73837341.figma.site/_assets/v11/1e7b0e6fcc016cd28aec5c68990118b8c54c35a5.svg`
  - `https://polo-pecan-73837341.figma.site/_assets/v11/3eac03c183db2ae080d910159211c14843398b61.svg`
  - `https://polo-pecan-73837341.figma.site/_assets/v11/17705a4c0023a0e5a99154dfb10582adbbf4260b.svg`
  - `https://polo-pecan-73837341.figma.site/_assets/v11/0e5f442b09dc5c248e3e60d40a65505fb1887228.svg`
  - `https://polo-pecan-73837341.figma.site/_assets/v11/63f99030ceb459e3c9ab9e429cfa2353491d3816.svg`
- Each logo: `width: 137px`, `height: 40px`, `object-fit: contain`.

---

### Entrance Animations

- Header: fade-down (translateY -20px to 0, 0.8s)
- Hero left: fade-up (translateY 40px to 0, 1s)
- Hero right circles: scale-in (scale 0.85 to 1 + opacity, 1.2s, delay 0.3s)
- Logos section: fade-up, delay 0.6s
- All using `cubic-bezier(0.22, 1, 0.36, 1)` easing.

---

### Responsive Breakpoints

- **1280px**: circles scale 0.85
- **1024px**: stack layout (flex-direction column), heading 48px, circles scale 0.7, nav gap shrinks
- **768px**: hide nav, heading 36px, circles scale 0.5
- **480px**: heading 28px, circles scale 0.4, smaller buttons/logos

---

### Key Colors

- Primary accent: `#A068FF`
- Background dark: `#060218` / `#070319`
- Text dark: `#000000`
- Text light: `#ffffff`
- Body bg fallback: `#0a0a0a`

---

### Technical Details

- React (useState, useEffect, useRef), Vite build
- Custom `useCountUp` hook: animates 0 to 20 over 2s with easeOutCubic, starts after 1.2s delay
- `TypewriterHeading` component: types char by char at configurable speed
- CSS `@property --border-angle` for the animated border gradient
- No external animation libraries -- pure CSS animations + JS for typewriter/counter
```

---

## 103. Build With Us

- **Category**: Contact us
- **Type**: hero
- **Page Type**: hero
- **ID**: `build-with-us`

```
Build a single-page React + TypeScript + Vite + Tailwind site that is a full-screen video-background landing page with a contact form. Use `lucide-react` for icons.

**Layout & Sizing**
- Root: `min-h-screen` white background with padding `p-3 sm:p-4 md:p-6`.
- Inside the root, one large rounded card with `rounded-2xl sm:rounded-3xl`, `overflow-hidden`. Heights: `min-h-[calc(100vh-24px)] sm:min-h-[calc(100vh-32px)] md:min-h-[calc(100vh-48px)] lg:h-[calc(100vh-48px)]`. On desktop it locks to viewport; on tablet/mobile it expands to content.
- Background video fills the card (`absolute inset-0 w-full h-full object-cover`). The video element has `autoPlay muted loop playsInline`. Use this exact URL:
  ```
  https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260602_150901_c45b90ec-18d7-42ff-90e2-b95d7109e330.mp4
  ```
- Content layer: `relative z-10 flex flex-col` with the same min-height ladder as the card and `lg:h-full`, padding `p-4 sm:p-6 md:p-8`, `gap-6`.

**Fonts**
- Import from Google Fonts in `index.css`: `Inter` (weights 300–700) and `Instrument Serif` (italic + regular).
- Set `* { font-family: 'Inter', sans-serif; }` globally.
- Use `Instrument Serif` italic for one accent word inline (see headline below).

**Navbar (top)**
- Pill bar with `bg-white/60 backdrop-blur-md rounded-2xl shadow-sm`, padding `pl-3 sm:pl-4 pr-2 py-2`, `w-full sm:w-auto`, `flex items-center gap-3 sm:gap-6`.
- Logo: 32x32 inline SVG (`viewBox="0 0 256 256"`) with two black filled paths forming a stylized "M":
  `M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z`.
- Links (hidden on mobile, shown `sm:flex`): `Our story`, `Expertise`, `Our work`, `Journal` — class `text-gray-800 text-sm font-medium hover:opacity-60 transition-opacity whitespace-nowrap`.
- CTA button on the right: black pill `bg-black text-white text-sm font-medium px-4 sm:px-5 py-2 rounded-xl hover:bg-gray-800` with label `Start a project`. On mobile it floats right with `ml-auto`.

**Spacer**
- A `<div className="flex-1 min-h-[2rem]" />` between nav and the bottom row.

**Bottom row (headline + form)**
- Container: `flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6`.

**Headline (left)**
- `<p>` with white text, `text-3xl sm:text-4xl xl:text-5xl font-medium leading-tight drop-shadow-lg lg:max-w-lg xl:max-w-2xl shrink-0`.
- Content (with `<br />`):
  `We craft bold ideas` / `and ship them as *products*`
- The word `products` is wrapped in a `<span>` with inline style: `fontFamily: "'Instrument Serif', serif"`, `fontStyle: 'italic'`, `fontWeight: 400`.

**Contact form card (right)**
- Outer: `w-full lg:w-[min(480px,45%)] shrink-0`.
- Card: `bg-white rounded-2xl sm:rounded-3xl shadow-2xl overflow-hidden`, inner padding `p-4 sm:p-6`, `flex flex-col gap-4`.

1. **Heading:** `Say hello! 👋` — `text-xl sm:text-2xl font-semibold text-black tracking-tight`.

2. **Email + socials row** (always horizontal): `flex flex-row items-center justify-between gap-3 bg-gray-50 rounded-2xl px-4 py-2.5`.
   - Left: small grey label `Drop us a line`, then mailto link `hello@forma.co` in `text-blue-600 font-semibold hover:underline truncate`.
   - Right: four 32x32 rounded-xl buttons (`w-8 h-8 rounded-xl flex items-center justify-center hover:opacity-80 transition-opacity`) using lucide icons size 13:
     - Twitter — `bg-gray-100 text-gray-800`
     - Circle — `bg-pink-100 text-pink-500`
     - Instagram — `bg-orange-100 text-orange-400`
     - Linkedin — `bg-blue-100 text-blue-600`
   - Extract this into a small `SocialBtn` helper component.

3. **OR divider:** horizontal lines on either side of the word `OR` (`text-gray-400 font-medium text-sm`, lines `flex-1 h-px bg-gray-200`).

4. **Form** (`flex flex-col gap-4`):
   - Label `Tell us about your vision` (`text-sm font-medium text-black`).
   - Name + Email inputs side by side on `sm:` (`flex flex-col sm:flex-row gap-2`), placeholders `Full name` and `Email`. Input style: `flex-1 min-w-0 text-sm px-3 py-2.5 rounded-xl border border-gray-200 bg-transparent placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition`.
   - Textarea, 4 rows, placeholder `What are you looking to build or improve...`, same input style plus `resize-none`.
   - Service tags section: label `I need help with...`. Tags wrap (`flex flex-wrap gap-1.5`). Each tag is a button `text-xs font-medium px-3 py-2 rounded-lg border transition-all`. Inactive: `bg-white text-gray-700 border-gray-200 hover:border-gray-400`. Active (selected): `bg-gray-100 text-black border-black`. Multi-select toggle via state.
     - Services list (exact order): `Website`, `Mobile App`, `Web App`, `E-Commerce`, `Visual Identity`, `3D & Motion`, `Digital Marketing`, `Growth & Consulting`, `Other`.
   - Submit button: `w-full bg-black text-white text-sm font-semibold py-3 rounded-2xl hover:bg-gray-800 transition-colors disabled:opacity-60`. Label: `Send my message` (or `Sending...` while submitting).

5. **Submit behavior:** On submit, set `sending=true`, await a 1-second fake delay (`new Promise(r => setTimeout(r, 1000))`), then show a success state in place of the form: centered column with `py-6 gap-3`, a 48x48 green check pill (`w-12 h-12 rounded-full bg-green-50 flex items-center justify-center text-xl` containing `✓`), heading `You're all set!` (`text-base font-semibold text-gray-900`), and subtext `Expect a reply within 24 hours.` (`text-sm text-gray-500`).

**State (useState)**
- `selected: string[]` (toggled service chips)
- `name`, `email`, `message`: strings
- `sending`, `sent`: booleans

**Transitions/animations**
- All interactive elements use Tailwind `transition-*` utilities (opacity, colors, all).
- No external animation library; rely on Tailwind hover/focus transitions and `backdrop-blur-md` on the navbar.

**Constants at the top of the file**
- `VIDEO_URL` (the CloudFront URL above) and `SERVICES` array.

**Files**
- `src/App.tsx` — entire component plus `SocialBtn` helper.
- `src/index.css` — Google Fonts import + Tailwind directives + global `* { font-family: 'Inter', sans-serif; }`.
- Standard Vite + Tailwind config (`tailwind.config.js` scanning `./index.html` and `./src/**/*.{ts,tsx}`).
```

---

## 104. Impact Ventures

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `impact-ventures`

```
Create a fullscreen hero landing page section for a design agency called "Atelier" using React, Tailwind CSS, and Lucide React icons. The section must be fully mobile responsive with an animated hamburger mobile menu. Here are the exact specifications:

**Fonts (Google Fonts):**
- "Instrument Serif" (regular + italic) for headings and mobile menu links
- "Inter" (weights 300, 400, 500, 600) as the sans-serif body font

Load them in index.html:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
```

**Tailwind Config** - extend fontFamily:
```js
fontFamily: {
  'instrument-serif': ['"Instrument Serif"', 'serif'],
  sans: ['Inter', 'system-ui', 'sans-serif'],
}
```

**Background:**
A fullscreen looping autoplay muted video covering the entire viewport with `object-cover`. Video URL:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_204103_f607742e-09da-4cf5-bb06-4e67b0a531de.mp4
```

**Layout:** The entire section is `w-full h-screen overflow-hidden` with the video absolutely positioned behind a `relative z-10` content layer that is `flex flex-col h-full`.

**Navbar:**
- Horizontal flex bar with padding `px-6 md:px-12 lg:px-16 py-5 md:py-6`
- Left side: Logo text "Atelier" (white, font-semibold, text-lg, tracking-tight, font-sans) followed by desktop nav links (hidden on mobile, shown md+): "Projects", "Expertise", "Studio", "Insights" - styled as `text-white/80 hover:text-white text-sm font-light transition-colors duration-200`
- Right side: "Reach Out" text link (hidden mobile) + "Let's Talk" button (white bg, black text, rounded-full, px-5 py-2, hidden mobile) + hamburger button (shown only on mobile, md:hidden)
- Hamburger: 3 lines (2px height, white, rounded-full) with the middle line shorter (w-4 vs w-6). On open, top/bottom lines rotate 45/-45 degrees and translate, middle fades out. Uses `cubic-bezier(0.76,0,0.24,1)` easing with 500ms duration.

**Mobile Menu Overlay (fixed inset-0 z-50, md:hidden):**
- Backdrop: `bg-black/90 backdrop-blur-xl` fading in with 700ms transition
- Content fades in with same 700ms cubic-bezier easing
- Header: matches navbar layout with logo + close button (X formed by rotated lines)
- Nav links: Stacked vertically, centered, `text-4xl sm:text-5xl font-instrument-serif`, white text, each with `border-b border-white/10`, `py-4`. On open they animate in with staggered delays (150ms + index*80ms), translating from `translate-y-8` to `translate-y-0`. Hover shifts text right with `hover:pl-4`
- Items: "Projects", "Expertise", "Studio", "Insights", "Reach Out"
- Footer: Full-width "Let's Talk" button (white bg, black text, rounded-full, py-4) with 550ms delay fade-in

**Hero Content (centered below navbar):**
- Container: `flex-1 flex flex-col items-center justify-start pt-4 sm:pt-6 md:pt-8 lg:pt-10 px-6 text-center`
- Heading (h1): `font-instrument-serif text-white text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl leading-[1.1] max-w-5xl`
  - Text content (with line breaks):
    ```
    UX <italic>and</italic> APP
    DESIGN <italic>for</italic> BOLD
    VENTURES
    ```
  - The italic words "and" and "for" use `italic font-instrument-serif` spans
- Subtext (p): `mt-4 md:mt-5 text-white/70 text-sm md:text-base font-light max-w-md leading-relaxed`
  - "We shape digital products that define brands" + line break (hidden sm:block) + "and unlock exponential growth."
- Buttons row: `mt-5 md:mt-6 flex flex-col sm:flex-row items-center gap-4`
  - Primary: "See Cases" with ArrowRight icon (lucide-react), white bg, black text, rounded-full, px-7 py-3, text-sm font-medium. On hover the arrow translates 0.5 right.
  - Secondary: "Watch Reel" with Play icon (lucide-react), transparent with `border border-white/40`, white text, rounded-full, px-7 py-3. On hover: `bg-white/10 border-white/60`

**Global CSS (index.css):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}
```

**Dependencies:** React, lucide-react (for ArrowRight and Play icons), Tailwind CSS. No other UI libraries.
```

---

## 105. Halo Use Case

- **Category**: Use Case
- **Type**: features
- **Page Type**: hero
- **ID**: `halo-use-case`

```
**Prompt:**

Build a "Use Cases" section for a fintech stablecoin landing page using **React + TypeScript + Tailwind CSS** with **lucide-react** for icons (use `ArrowRight`). Make it fully mobile responsive.

---

### Font Setup

The page uses **"TT Norms Pro"** loaded via a stylesheet link in `index.html`:

```html
<link href="https://db.onlinewebfonts.com/c/49bf5d043a27b890a040cf393277e2b2?family=TT+Norms+Pro+Regular" rel="stylesheet">
```

Add this `<link>` inside the `<head>` of your `index.html`.

Then in `index.css`, apply it globally:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: 'TT Norms Pro Regular', ui-sans-serif, system-ui, sans-serif;
  }
  body {
    font-family: 'TT Norms Pro Regular', ui-sans-serif, system-ui, sans-serif;
  }
  * {
    font-family: inherit;
  }
}
```

No local font files are needed. The font is served from the external stylesheet URL above.

---

### Section Component: `UseCasesSection`

**Outer wrapper:** `<section>` with classes `bg-[#F5F5F5] px-6 py-24`.

**Inner container:** `<div>` with classes `max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-start`.

---

#### LEFT COLUMN (text-only intro)

Wrapper `<div>` with classes `md:pr-12 md:pt-2`.

Contains three elements stacked vertically:

1. **Eyebrow label:**
   - Element: `<p>`
   - Text: **"USD Halo in Practice"**
   - Classes: `text-black/60 text-sm font-normal mb-2`

2. **Section heading:**
   - Element: `<h2>`
   - Text: **"Use modes"**
   - Classes: `text-black text-5xl md:text-6xl font-medium leading-none mb-6`
   - Inline style: `{ letterSpacing: '-0.04em' }`

3. **Description paragraph:**
   - Element: `<p>`
   - Text: **"USD Halo powers a wide range of modes for builders, companies and treasuries wanting safe and rewarding stablecoin integrations plus more"**
   - Classes: `text-black/60 text-base leading-relaxed max-w-sm`

---

#### RIGHT COLUMN (large video background card)

Wrapper `<div>` with classes `relative rounded-3xl overflow-hidden min-h-[720px]`.

**Background video** (fills entire card as ambient background):
- Element: `<video>`
- Classes: `absolute inset-0 w-full h-full object-cover`
- Attributes: `autoPlay`, `muted`, `loop`, `playsInline`
- `src` URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_183428_ab5e672a-f608-4dcb-b319-f3e040f02e2d.mp4`

**Content overlay** (sits above video):
- Wrapper `<div>` with classes `relative z-10 p-10 md:p-12`

Contains three elements:

1. **Card heading:**
   - Element: `<h3>`
   - Text: **"Commerce"**
   - Classes: `text-black text-4xl md:text-5xl font-medium leading-tight mb-5`
   - Inline style: `{ letterSpacing: '-0.03em' }`

2. **Card description:**
   - Element: `<p>`
   - Text: **"Lift customer retention by offering USD Halo, a trusted dollar-backed stablecoin with strong yields, letting your patrons earn with zero effort on your platform."**
   - Classes: `text-black/70 text-base leading-relaxed max-w-md mb-8`

3. **"Know more" button:**
   - Element: `<button>`
   - Classes: `inline-flex items-center gap-3 text-black text-base font-medium group`
   - Contains (in this exact order):
     - **Icon circle first:** `<span>` with classes `w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center group-hover:bg-white transition-colors`, containing `<ArrowRight className="w-4 h-4 text-black" />` from lucide-react.
     - **Text label second:** the plain text **"Know more"** (placed after the span, so icon is on the left).

---

### Key Design Specifications

- **Page background:** `#F5F5F5` (light warm gray).
- **Video card:** Video fills the entire rounded card via `object-cover` and loops silently. There is **no gradient overlay, no dark scrim, no blur layer** -- text sits directly on the video.
- **Card corner radius:** `rounded-3xl` (24px).
- **Card minimum height:** `min-h-[720px]`.
- **Typography system:**
  - All text uses inherited "TT Norms Pro Regular" from the web font link.
  - Headings: `font-medium` with tight negative letter-spacing (`-0.04em` for section title, `-0.03em` for card title).
  - Body text: default weight (400), `text-base` size.
  - Color hierarchy: `text-black` for headings, `text-black/70` for card body text, `text-black/60` for muted/secondary text.
- **"Know more" button:** Frosted-glass circle icon (`bg-white/80 backdrop-blur`) transitions to solid white on hover via Tailwind `group`/`group-hover`. Icon circle comes before text label.
- **Layout:** Two-column grid on `md:` breakpoint. Stacks to single column on mobile. Left column has `md:pr-12` and `md:pt-2` for breathing room.
- **Spacing:** `gap-8` between columns. Section padding `py-24` vertical, `px-6` horizontal.

---

### Complete JSX Reference

```tsx
import { ArrowRight } from 'lucide-react';

function UseCasesSection() {
  return (
    <section className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        {/* Left column */}
        <div className="md:pr-12 md:pt-2">
          <p className="text-black/60 text-sm font-normal mb-2">USD Halo in Practice</p>
          <h2 className="text-black text-5xl md:text-6xl font-medium leading-none mb-6" style={{ letterSpacing: '-0.04em' }}>
            Use modes
          </h2>
          <p className="text-black/60 text-base leading-relaxed max-w-sm">
            USD Halo powers a wide range of modes for builders, companies and treasuries wanting safe and rewarding stablecoin integrations plus more
          </p>
        </div>

        {/* Right column -- big card with bg video */}
        <div className="relative rounded-3xl overflow-hidden min-h-[720px]">
          <video
            className="absolute inset-0 w-full h-full object-cover"
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_183428_ab5e672a-f608-4dcb-b319-f3e040f02e2d.mp4"
            autoPlay
            muted
            loop
            playsInline
          />
          <div className="relative z-10 p-10 md:p-12">
            <h3 className="text-black text-4xl md:text-5xl font-medium leading-tight mb-5" style={{ letterSpacing: '-0.03em' }}>
              Commerce
            </h3>
            <p className="text-black/70 text-base leading-relaxed max-w-md mb-8">
              Lift customer retention by offering USD Halo, a trusted dollar-backed stablecoin with strong yields, letting your patrons earn with zero effort on your platform.
            </p>
            <button className="inline-flex items-center gap-3 text-black text-base font-medium group">
              <span className="w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center group-hover:bg-white transition-colors">
                <ArrowRight className="w-4 h-4 text-black" />
              </span>
              Know more
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---
```

---

## 106. Daisy Wild

- **Category**: Product
- **Type**: features
- **Page Type**: hero
- **ID**: `daisy-wild`

```
Build a standalone React + TypeScript + Tailwind CSS section component. This is a fragrance product showcase split into two halves: a looping video on the LEFT and a lime-green product panel on the RIGHT. On mobile it stacks vertically with the product panel ABOVE the video (achieved via `flex-col-reverse`). Every value below is exact.

## Tech Stack
- React 18 + TypeScript
- Tailwind CSS 3 (default config, default breakpoints: `sm:640px`, `md:768px`)
- Vite
- No extra packages. No icon libraries needed.

## Constants

```ts
const TEXT_COLOR = '#000000';
const BG_LIME = '#BDE84F';
const EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';
```

## Animation Helper

```ts
function anim(visible: boolean, delay: number, opts: { y?: number; x?: number; duration?: number } = {}) {
  const { y = 20, x = 0, duration = 1600 } = opts;
  const translateFrom = y !== 0 ? `translateY(${y}px)` : x !== 0 ? `translateX(${x}px)` : 'none';
  return {
    style: {
      opacity: visible ? 1 : 0,
      transform: visible ? 'translate(0,0)' : translateFrom,
      transition: `opacity ${duration}ms ${EASE} ${delay}ms, transform ${duration}ms ${EASE} ${delay}ms`,
    } as React.CSSProperties,
  };
}
```

## Product Data

```ts
const WILD_PRODUCT = {
  name: 'Eau So Extra',
  size: '100 ml / 3.3 oz',
  image: 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260511_151621_4fba6892-ed21-4c2e-8cb3-0bd2ec2abefa.png&w=1280&q=85',
  notes: [
    { label: 'Top', ingredient: 'BANANA BLOSSOM ACCORD' },
    { label: 'Heart', ingredient: 'CHOCOLATE DAISY ACCORD' },
    { label: 'Base', ingredient: 'VETIVER OIL' },
  ],
};
```

## Video URL (exact, verbatim)

```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_151818_65bb22c5-33ae-4e23-85ea-0a3dd89957c2.mp4
```

---

## Component: `ProductPanel`

This is a reusable component shared with Section 2. For this section it is called with `noteStyle="bold"`.

### Props

```ts
{
  bg: string;
  product: { name: string; size: string; image: string };
  notes: { label: string; ingredient: string }[];
  visible: boolean;
  noteStyle?: 'normal' | 'bold';   // defaults to 'normal'
}
```

### Outer wrapper
```jsx
<div
  className="relative flex flex-col px-6 md:px-8 pt-6 md:pt-8 pb-8 md:pb-10"
  style={{ backgroundColor: bg, minHeight: '100%' }}
>
```

### 1. Top labels row
```jsx
<div
  className="flex items-start justify-between mb-auto"
  {...anim(visible, 0, { y: 12, duration: 1400 })}
>
  <span className="text-xs font-normal" style={{ color: TEXT_COLOR }}>
    {noteStyle === 'bold' ? 'Daisy wild' : 'Daisy love'}
  </span>
  <span className="text-xs font-normal" style={{ color: TEXT_COLOR }}>
    {noteStyle === 'bold' ? 'Playful' : 'Sweet'}
  </span>
</div>
```

For this section (`noteStyle="bold"`), the labels read **"Daisy wild"** on the left and **"Playful"** on the right.

### 2. Product image block
```jsx
<div
  className="flex flex-col items-center py-8"
  style={{ flex: 1, justifyContent: 'center', ...anim(visible, 300, { y: 40, duration: 1800 }).style }}
>
```

#### Image container
```jsx
<div
  className="overflow-hidden"
  style={{
    width: 'clamp(140px, 40%, 220px)',
    aspectRatio: '220/340',
    backgroundColor: '#D9D9D9',
    borderRadius: '2px',
    flexShrink: 0,
  }}
>
  <img
    src={product.image}
    alt={product.name}
    style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
  />
</div>
```

#### Caption (below image)
```jsx
<div className="text-center mt-4" {...anim(visible, 600, { y: 10, duration: 1400 })}>
  <p className="text-sm font-normal" style={{ color: TEXT_COLOR }}>{product.name}</p>
  <p className="text-xs font-normal mt-1" style={{ color: TEXT_COLOR }}>{product.size}</p>
</div>
```

### 3. Bottom row — notes + button

```jsx
<div className="flex items-end justify-between gap-4 flex-wrap">
```

#### Notes column (left side)
```jsx
<div className="flex flex-col gap-0.5" {...anim(visible, 900, { y: 16, duration: 1400 })}>
```
For each note, render `<div key={note.ingredient}>` with two `<p>`:
- Label: `<p className="text-xs leading-snug" style={{ color: TEXT_COLOR, fontWeight: noteStyle === 'bold' ? 700 : 400 }}>{note.label}</p>`
- Ingredient: `<p className="text-xs font-bold tracking-widest uppercase leading-snug" style={{ color: TEXT_COLOR }}>{note.ingredient}</p>`

For this section (`noteStyle="bold"`), the note LABELS ("Top", "Heart", "Base") render at `fontWeight: 700`. The ingredient lines are always `font-bold` regardless.

#### SHOP NOW button (right side)
```jsx
<button
  className="text-xs font-bold tracking-widest uppercase border px-6 py-3 relative group shrink-0"
  style={{
    color: TEXT_COLOR,
    borderColor: TEXT_COLOR,
    backgroundColor: 'transparent',
    ...anim(visible, 1150, { y: 16, duration: 1400 }).style,
  }}
>
  <span className="relative z-10 group-hover:text-black transition-colors duration-500">SHOP NOW</span>
  <span
    className="absolute inset-0 origin-left scale-x-0 group-hover:scale-x-100 transition-transform duration-500 ease-out"
    style={{ backgroundColor: '#ffffff' }}
  />
</button>
```

Button: `1px` solid border colored `#000000`. On hover, a white fill scales from the left over 500ms. Text stays above (`z-10`).

---

## Component: `WildScentSection`

### Visibility trigger
```ts
const ref = useRef<HTMLDivElement>(null);
const [visible, setVisible] = useState(false);

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => { if (entry.isIntersecting) setVisible(true); },
    { threshold: 0.15 }
  );
  if (ref.current) observer.observe(ref.current);
  return () => observer.disconnect();
}, []);
```

One-shot: once 15% visible, `visible` becomes `true` permanently, triggering all staggered animations.

### Layout structure

```jsx
<section ref={ref} className="relative w-full">
  <div className="flex flex-col-reverse md:grid md:min-h-screen" style={{ gridTemplateColumns: '1fr 1fr' }}>
```

**Critical difference from Section 2:** This uses `flex-col-reverse` (not `flex-col`). The DOM order is: video divs first, then ProductPanel. But on mobile, `flex-col-reverse` visually flips them so the product panel appears ABOVE the video.

### Three children inside (in DOM order):

#### Child 1: Desktop video panel (left half on desktop, hidden below `md`)
```jsx
<div className="hidden md:block relative overflow-hidden" style={{ backgroundColor: '#111', minHeight: '100%' }}>
  <video autoPlay muted loop playsInline className="absolute inset-0 w-full h-full object-cover">
    <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_151818_65bb22c5-33ae-4e23-85ea-0a3dd89957c2.mp4" type="video/mp4" />
  </video>
</div>
```

#### Child 2: Mobile video strip (hidden at `md` and above)
```jsx
<div className="md:hidden relative overflow-hidden" style={{ height: '75vw', backgroundColor: '#111' }}>
  <video autoPlay muted loop playsInline className="absolute inset-0 w-full h-full object-cover">
    <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_151818_65bb22c5-33ae-4e23-85ea-0a3dd89957c2.mp4" type="video/mp4" />
  </video>
</div>
```

#### Child 3: ProductPanel (right half on desktop, visually on top on mobile)
```jsx
<ProductPanel
  bg={BG_LIME}
  product={WILD_PRODUCT}
  notes={WILD_PRODUCT.notes}
  visible={visible}
  noteStyle="bold"
/>
```

Called with `noteStyle="bold"`, which changes:
- Top labels: `"Daisy wild"` / `"Playful"` (instead of `"Daisy love"` / `"Sweet"`)
- Note labels: `fontWeight: 700` (instead of `400`)

---

## Responsive Behavior

| Viewport | Layout | Visual order (top to bottom / left to right) |
|---|---|---|
| < 768px | `flex flex-col-reverse` | Product panel (lime, full width) then video strip (`height: 75vw`, full width) |
| >= 768px | `grid 1fr 1fr`, `min-h-screen` | Video (left half) then Product panel (right half, lime) |

The `flex-col-reverse` trick: DOM order is [video-desktop, video-mobile, panel]. On mobile, `flex-col-reverse` reverses visual order to [panel, video-mobile, video-desktop(hidden)]. On desktop, `md:grid` overrides flex, and the grid places them left-to-right in DOM order: video left, panel right.

## Animation Stagger Timeline

All triggered when 15% of the section scrolls into view. Easing: `cubic-bezier(0.22, 1, 0.36, 1)`.

| Element | Delay | Duration | Direction | Distance |
|---|---|---|---|---|
| Top labels ("Daisy wild" / "Playful") | 0ms | 1400ms | translateY | 12px |
| Product image block | 300ms | 1800ms | translateY | 40px |
| Caption (name + size) | 600ms | 1400ms | translateY | 10px |
| Notes column | 900ms | 1400ms | translateY | 16px |
| SHOP NOW button | 1150ms | 1400ms | translateY | 16px |

Each element starts at `opacity: 0` + translated down, then transitions to `opacity: 1` + `translate(0,0)`.

## Colors Used

- `#BDE84F` — product panel background (lime green)
- `#000000` — all text, button border
- `#D9D9D9` — image placeholder background
- `#111` — video panel background (while loading)
- `#ffffff` — button hover fill

## Fonts
No custom or Google Fonts. Tailwind default sans-serif system stack for all text.

## SVGs / Icons
None in this section.

## Key Differences from Section 2 (ScentFinder)

| Aspect | Section 2 (ScentFinder) | Section 3 (WildScent) |
|---|---|---|
| Background color | `#4BB3ED` (sky blue) | `#BDE84F` (lime green) |
| Panel position (desktop) | LEFT half | RIGHT half |
| Video position (desktop) | RIGHT half | LEFT half |
| Flex direction (mobile) | `flex-col` (panel on top, video below) | `flex-col-reverse` (panel on top via reversal, video below) |
| Top labels | "Daisy love" / "Sweet" | "Daisy wild" / "Playful" |
| Note label weight | `fontWeight: 400` (normal) | `fontWeight: 700` (bold) |
| `noteStyle` prop | `'normal'` (default) | `'bold'` |
| Product name | Eau So Sweet | Eau So Extra |
| Product size | 100 ml / 3.3 oz | 100 ml / 3.3 oz |
| Video URL | `...151802_1bbf9a81...` | `...151818_65bb22c5...` |
| Notes content | Fruity top / WHITE RASPBERRIES, Floral heart / DAISY TREE PETALS, Feminine base / SUGAR MUSKS | Top / BANANA BLOSSOM ACCORD, Heart / CHOCOLATE DAISY ACCORD, Base / VETIVER OIL |
```

---

## 107. Cognitra Feature

- **Category**: Feature
- **Type**: features
- **Page Type**: hero
- **ID**: `cognitra-feature`

```
---

**Prompt:**

Create a full-viewport section (100vh) that sits over a fixed background video. The section has no background color of its own -- it is fully transparent so the fixed video behind it shows through.

**Background video (fixed, behind everything):**
A `<video>` element fixed to the viewport (`position: fixed; top: 0; left: 0; width: 100%; height: 100vh; object-fit: cover; z-index: 0`), using this source:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260514_135830_bb6491d1-9b66-4aec-9722-13b4dfe3fb46.mp4
```
It should `autoPlay`, be `muted`, `loop`, and `playsInline`.

**Section layout:**
- `position: relative; z-index: 1`
- `display: flex; flex-direction: column; justify-content: center` (centers content vertically)
- `height: 100vh`
- Padding: `70px 32px 32px 32px`

**Content block** (inside the section):
- A wrapper `div` with `display: flex; flex-direction: column; align-items: flex-start; max-width: 720px`
- **Heading (`<h2>`):**
  - Text: `"WE BUILD END-TO-END AI AUTOMATION SYSTEMS."`
  - Each word is wrapped in an individual `<span>` element, displayed using `display: flex; flex-wrap: wrap; gap: 0.25em`
  - Each word animates in with a staggered fade-up animation: starts at `opacity: 0, y: 32px`, animates to `opacity: 1, y: 0` using Framer Motion `whileInView` with `viewport: { once: true, amount: 0.2 }`
  - Stagger: first word at `delay: 0.15`, each subsequent word adds `0.08s` (so word 2 = 0.23, word 3 = 0.31, etc.)
  - Animation easing: `[0.22, 1, 0.36, 1]`, duration: `0.7s`
  - Typography: `font-size: clamp(26px, 3vw, 42px); font-weight: 700; line-height: 1.08; letter-spacing: -0.01em; text-transform: uppercase; color: #fff; margin: 0`

- **Subtext (`<p>`):**
  - Text: `"We provide all-in-one AI automation services in one place."`
  - `margin-top: 24px; font-size: 14px; line-height: 1.65; color: rgba(255,255,255,0.85); max-width: 260px`
  - Same fade-up animation as the words but with `delay: 0.9` and default `y: 24px`

**Font:**
```css
@import url('https://db.onlinewebfonts.com/c/e66905e07608167a84e6ad52f638c3c6?family=Helvetica+Now+Var');
* { font-family: 'Helvetica Now Var', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
```

**FadeUp component (reusable, Framer Motion):**
```tsx
import { motion } from 'framer-motion';
import { CSSProperties, ReactNode } from 'react';

type FadeUpProps = {
  children: ReactNode;
  delay?: number;
  duration?: number;
  y?: number;
  className?: string;
  style?: CSSProperties;
  as?: 'div' | 'section' | 'span' | 'h1' | 'h2' | 'h3' | 'p' | 'nav';
  once?: boolean;
};

export function FadeUp({
  children, delay = 0, duration = 0.7, y = 24,
  className, style, as = 'div', once = true,
}: FadeUpProps) {
  const Tag = motion[as];
  return (
    <Tag
      className={className}
      style={style}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once, amount: 0.2 }}
      transition={{ duration, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </Tag>
  );
}
```

**Mobile responsive (max-width: 900px):**
- Section padding changes to `90px 18px 32px 18px`

**Tech stack:** React 18, TypeScript, Vite, Tailwind CSS 3, Framer Motion 12.

---
```

---

## 108. No-Code Waitlist

- **Category**: Waitlist
- **Type**: hero
- **Page Type**: hero
- **ID**: `no-code-waitlist`

```
Build a full-screen dark hero section landing page in React + Vite + Tailwind CSS v4 + Motion (framer-motion) + Lucide React icons + hls.js. The page should be a single screen (100vh, no scroll) with a black background, a fullscreen background video, a glassmorphism navbar, and a centered hero with an email capture CTA.
>
> **Dependencies:** `react`, `react-dom`, `motion`, `hls.js`, `lucide-react`, `tailwindcss` v4 with `@tailwindcss/vite`, `@vitejs/plugin-react`
>
> **Fonts:** Import Google Fonts:
> - `Inter` (weights 300, 400, 500, 600) -- used as the base sans-serif font
> - `Instrument Serif` (regular and italic) -- used for the hero heading
>
> **CSS (`index.css`):**
> - Import both Google Font URLs, then `@import "tailwindcss";`
> - Set `@theme { --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif; }`
> - `:root` variables: `--background: #000000; --foreground: #ffffff;`
> - `body`: background-color var(--background), color var(--foreground), font-family var(--font-sans), `-webkit-font-smoothing: antialiased`, `letter-spacing: -0.01em`
> - `.liquid-glass` class: `background: rgba(255,255,255,0.01)`, `background-blend-mode: luminosity`, `backdrop-filter: blur(4px)`, `-webkit-backdrop-filter: blur(4px)`, `border: none`, `box-shadow: inset 0 1px 1px rgba(255,255,255,0.1)`, `position: relative`, `overflow: hidden`. It has a `::before` pseudo-element for a gradient border effect: `padding: 1.4px`, `background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)`, masked with `-webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)` and `-webkit-mask-composite: xor; mask-composite: exclude;`
> - `.glass-pill` class: `background: rgba(255,255,255,0.04)`, `backdrop-filter: blur(16px) saturate(180%)`, `border-radius: 9999px`, `box-shadow: none !important`
>
> **Background Video component:**
> - Renders an absolutely positioned `<div>` covering the full parent (`absolute inset-0 overflow-hidden pointer-events-none`)
> - Contains a `<video>` element: `autoPlay`, `muted`, `loop`, `playsInline`, classes `w-full h-full object-cover opacity-100`
> - Video source URL: `https://stream.mux.com/kimF2ha9zLrX64H00UgLGPflCzNtl1T0215MlAmeOztv8.m3u8` (this is an HLS stream from Mux, NOT CloudFront)
> - Uses `hls.js`: if the browser natively supports HLS (`video.canPlayType("application/vnd.apple.mpegurl")`), set `video.src` directly; otherwise instantiate `new Hls()`, `loadSource`, `attachMedia`
>
> **Navbar component:**
> - Animates in with `motion.nav`: `initial={{ y: -20, opacity: 0 }}`, `animate={{ y: 0, opacity: 1 }}`
> - Classes: `relative z-20 px-6 py-6 w-full`
> - Inner container: `liquid-glass rounded-full px-6 py-3 flex items-center justify-between max-w-5xl mx-auto`
> - Left side (`flex items-center gap-8`):
>   - Logo: `Globe` icon from lucide-react (w-6 h-6 text-white) + "Asme" text (`text-white font-semibold text-lg`), in a `flex items-center gap-2` wrapper
>   - Nav links: "Features", "Pricing", "About" -- hidden on mobile (`hidden md:flex`), `items-center gap-8 text-white/80 text-sm font-medium`, each link has `hover:text-white transition-colors duration-300`
> - Right side (`flex items-center gap-4`):
>   - "Sign Up" plain text button: `text-white hover:text-white/80 transition-colors text-sm font-medium cursor-pointer`
>   - "Login" glassmorphism button: `liquid-glass rounded-full px-6 py-2 text-sm font-medium text-white hover:opacity-90 transition-opacity cursor-pointer`
>
> **Hero component:**
> - `<section>` with `relative flex-1 flex flex-col items-center justify-center px-6`
> - Content wrapper: `relative z-10 text-center max-w-5xl mx-auto flex flex-col items-center justify-center w-full gap-12`
> - **Tagline** (motion.p): text "BUILD A NO-CODE AI APP IN MINUTES", `text-white/80 text-[10px] md:text-[11px] font-medium tracking-[0.2em] uppercase mb-4`, animates `initial={{ opacity: 0, y: 10 }}`, `animate={{ opacity: 1, y: 0 }}`, `transition={{ delay: 0.1 }}`
> - **Heading** (motion.h1): text "A new way to think and create with computers" (with `<br className="hidden md:block" />` after "create"), `fontFamily: "'Instrument Serif', serif"` set via inline style, classes `text-4xl md:text-[64px] font-medium tracking-[-0.01em] leading-[1.1] mb-6 bg-gradient-to-b from-white via-white/95 to-white/70 bg-clip-text text-transparent max-w-4xl`, animates `initial={{ opacity: 0, y: 20 }}`, `animate={{ opacity: 1, y: 0 }}`, `transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}`
> - **CTA area** (motion.div): `min-h-[50px] mt-2`, animates with `delay: 0.4`. Uses `AnimatePresence mode="wait"` to toggle between:
>   - **Button state**: "Get early access" -- `px-10 py-3 text-[14px] font-medium border border-white/10 rounded-full hover:border-white/30 hover:bg-white/[0.02] transition-all duration-300 text-white/90 backdrop-blur-sm cursor-pointer`. On click, switches to email form.
>   - **Email form state**: a `<form>` with `flex items-center gap-2 pl-5 pr-1.5 py-1.5 text-[14px] font-medium border border-white/20 rounded-full bg-white/[0.02] backdrop-blur-sm w-full max-w-[320px] focus-within:border-white/40 transition-colors duration-300`. Contains an email `<input>` (transparent background, white text, `placeholder-white/45`, `autoFocus`) and a submit button with either `ArrowRight` icon (default) or `Check` icon (after submit). Both states animate scale 0.95 to 1 with 0.2s duration.
>   - **Typewriter placeholder**: when the email form opens, the placeholder text "Enter Your Email Here For Early Access" types in character by character at 60ms intervals. After submission, it types "You Will Receive Notifications By Email" instead. After 4 seconds, it resets back to the button state.
> - **"Play Video Demo"** link below (motion.div with `delay: 0.8` fade-in): `text-white/80 hover:text-white/40 transition-colors duration-300 text-[13px] font-medium tracking-wide`
>
> **App root layout:**
> - `<main>` with `relative bg-black h-screen w-screen flex flex-col overflow-hidden selection:bg-white selection:text-black shrink-0`
> - Render order: `BackgroundVideo`, `Navbar`, `Hero`
> - Text selection is styled white bg with black text

---

Key clarification: The video URL is **not** from CloudFront. It is an HLS stream hosted on **Mux**: `https://stream.mux.com/kimF2ha9zLrX64H00UgLGPflCzNtl1T0215MlAmeOztv8.m3u8`. The `.m3u8` format requires hls.js for non-Safari browsers.
```

---

## 109. VaultShield

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `vaultshield`

```
Create a fullscreen hero section for a password manager app called "VaultShield" using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React icons.

---

## Fonts

- **Heading font:** `Helvetica Now Display Bold` loaded from `https://db.onlinewebfonts.com/c/04e6981992c0e2e7642af2074ebe3901?family=Helvetica+Now+Display+Bold` (add as a `<link>` in `index.html`)
- **Body font:** `Inter` (weights 300-900) loaded from Google Fonts: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap` (imported in CSS)

## CSS Variables

```css
:root {
  --font-heading: 'Helvetica Now Display Bold', sans-serif;
  --font-body: 'Inter', sans-serif;
  --color-text: #192837;
  --color-accent: #7342E2;
  --color-login-bg: #F2F2EE;
}
```

## Background Video

Full-screen background video covering the entire viewport (`absolute inset-0, object-cover`):

```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260518_003132_8b7edcb6-c64d-4a52-a9ca-879942e122ad.mp4
```

Attributes: `autoPlay`, `muted`, `loop`, `playsInline`

## Layout Structure

1. **Container:** `relative w-full min-h-screen`, font-family from `--font-body`, color from `--color-text`
2. **Navbar:** max-width 1280px, centered, z-10, `px-5 sm:px-8 py-4 sm:py-5`, flex with items centered and space-between
3. **Hero content:** max-width 1280px centered container with `paddingTop: clamp(40px, 8vw, 72px)`, content block capped at `max-width: 560px`

## Logo (SVG)

Custom SVG logo, 32x32, fill `#192837`, geometric angular shape:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" overflow="visible" viewBox="0 0 256 256">
  <path d="M 64 128 L 64.5 128 L 32 95 L 0 64 L 0 0 L 64 0 L 128 64 L 128 64.5 L 161 32 L 192 0 L 256 0 L 256 64 L 192 128 L 128 128 L 128 192 L 96 223 L 63.5 256 L 0 256 L 0 192 Z M 256 192 L 224 223 L 191.5 256 L 128 256 L 128 192 L 192 128 L 256 128 Z" fill="#192837"/>
</svg>
```

## Navbar Elements

- **Left:** Logo
- **Center (desktop only, `hidden md:flex`):** 5 links — `['Vault', 'Plans', 'Install', 'News', 'Help']`, text-sm font-medium, opacity hover effect
- **Right (desktop only):**
  - "Start For Free" button — `background: #7342E2`, white text, rounded-full, `px-5 py-2.5`
  - "Sign In" button — `background: #F2F2EE`, dark text, rounded-full, `px-5 py-2.5`
- **Mobile:** Hamburger icon (Menu/X from lucide-react), opens a right-side slide-in sheet

## Mobile Menu Sheet (AnimatePresence + Framer Motion)

- **Backdrop:** fixed inset-0, `rgba(25,40,55,0.35)` background with `blur(4px)` backdrop-filter
- **Sheet:** fixed right-0 top-0, width `min(88vw, 360px)`, height `100dvh`, background `#CFC8C5`, box-shadow `-12px 0 48px rgba(25,40,55,0.18)`
- **Sheet animation:** slides from `x: '100%'` to `x: 0`, ease `[0.22, 1, 0.36, 1]`, duration 0.45s
- **Sheet content:** Logo + close button header, 1px divider, staggered nav links (delay `0.18 + i * 0.07`), bottom CTA buttons matching desktop style

## Hero Heading

- Font: `var(--font-heading)`
- Size: `clamp(1.65rem, 5vw, 3rem)`
- Line-height: `1.05`
- Letter-spacing: `-0.01em`
- Color: `#192837`
- Margin-bottom: `24px`
- Contains inline Lucide icons (Zap, LockKeyhole, Fingerprint) at 24px, color `#192837`, vertically aligned middle, positioned `top: -2px`
- Text: "Lock Down Your Passwords with Ironclad Security"
  - Zap icon before "Lock"
  - LockKeyhole icon between "Passwords" and "with"
  - Fingerprint icon after "Security"

## Hero Subtext

- Font: `var(--font-body)`
- Size: `clamp(0.9rem, 2.5vw, 1.1rem)`
- Line-height: `1.65`
- Opacity: `0.8`
- Max-width: `560px`
- Text: "Zero stress, total control. VaultShield keeps you covered with unbreakable storage, one-tap access, and pro-grade tools for your non-stop world."

## CTA Button

- Background: `#7342E2`
- Color: white
- Border-radius: `50px`
- Padding: `17px 24px`
- Font: `var(--font-body)`, font-weight semibold
- Size: `clamp(0.9rem, 2vw, 1rem)`
- Box-shadow: `0 4px 24px rgba(115,66,226,0.28)`
- Min-width: `210px`
- Flex with space-between, gap `32px`
- Text: "Get It Free" with ArrowRightCircle icon (20px) on the right
- Hover: `scale(1.04)` + `brightness(1.1)`
- Tap: `scale(0.96)`

## Animations (Framer Motion)

**fadeUp variant** applied to heading (delay 0), subtext (delay 0.15s), and CTA button (delay 0.30s):

```js
hidden: { opacity: 0, y: 28 }
visible: { opacity: 1, y: 0, transition: { delay: i * 0.15, duration: 0.6, ease: [0.22, 1, 0.36, 1] } }
```

## Dependencies

- `react`, `react-dom`
- `framer-motion`
- `lucide-react` (icons: ArrowRightCircle, Zap, LockKeyhole, Fingerprint, Menu, X)
- Tailwind CSS

---

That is every detail needed to reproduce the hero section exactly as built.
```

---

## 110. Subscription Agency

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `subscription-agency`

```
**Create a single-page landing hero section for a creative agency called "Alwayzz" with a React + Vite + Tailwind CSS setup. Use custom CSS (not Tailwind utilities) for all styling. The design should be minimal, clean, black-and-white, with tight negative letter-spacing throughout.**

---

### Fonts (loaded via Google Fonts in index.html)

```
Inter: weights 400, 500, 600, 700
Source Serif 4: weights 400, 600 (both normal and italic)
```

Preconnect to `fonts.googleapis.com` and `fonts.gstatic.com`.

---

### CSS Variables

```css
--bg: #ffffff;
--text: #0a0a0a;
--muted: #6b6b6b;
--button-bg: #0a0a0a;
--button-text: #ffffff;
--border-soft: rgba(0, 0, 0, 0.08);
--green: #17c964;
```

---

### Components

**1. Navbar (fixed top, z-index 100)**
- Padding: `19px 36px`, max-width `1200px` centered.
- Left: Logo text "Alwayzz" in `Source Serif 4`, 30px, weight 600, **italic**, letter-spacing `-0.08em`, with a registered trademark symbol in Inter 14px weight 600.
- Right: "Menu" pill button (black bg, white text, rounded-full, 14px weight 500, Inter) with a `ChevronUp` icon (16px) from lucide-react.
- Full-screen drawer overlay on click: white bg, fade transition 0.4s. Nav links centered vertically at 48px weight 500, letter-spacing `-0.04em`. Links: Projects, Plans, Team, FAQs, Get in Touch. Footer with copyright.

**2. Hero Section**
- Min-height: `850px`, padding: `160px 36px`, centered flex column.
- **Background image** (via `::before` pseudo-element, covers full section):
  ```
  https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260626_041422_4a459e05-abce-4150-9fb7-4ededc423cd1.png&w=1280&q=85
  ```
  Background-size: cover, background-position: center.

- **Curved line animations** (decorative):
  - 20 lines on left side, 20 on right side, absolutely positioned.
  - Each line is a tall rectangle with one-sided border-radius (80%) and `2.5px solid #FCFAF8` border.
  - Left lines: no left border, radius on right. Right lines: no right border, radius on left.
  - Staggered `animationDelay: i * 0.25s`, widths from 60px increasing by 10px per line.
  - Animation: `line-pulse` 5s ease-in-out infinite (fade in to 0.9 opacity, then back to 0 with slight scale).
  - On mobile (<810px): hide side lines, show top horizontal lines instead (same animation, horizontal orientation with bottom border-radius).

- **Ticker row** (max-width 500px, height 36px):
  - Horizontal marquee scrolling left over 30s, linear, infinite.
  - Items: "Brand Identity", "App Development", "Visual Design", "Creative Video", "Iconography"
  - Each item: 13px, weight 500, color `var(--muted)`, padding `6px 14px`, rounded-full, background `rgb(251, 251, 251)`.
  - Marquee has edge fade mask: `linear-gradient(90deg, transparent 0%, black 12%, black 88%, transparent 100%)`.
  - 4x duplicated rows for seamless loop.

- **Title**:
  ```
  Premium creative <span class="serif italic">alwayzz</span><sup style registered mark> on demand.
  ```
  - Max-width: 550px, font-size: 82px, line-height: 1.03, letter-spacing: `-0.07em`, weight 600, centered.
  - The word "alwayzz" uses `Source Serif 4`, italic, weight 600, letter-spacing `-0.08em`.
  - The registered mark: Inter, 24px, weight 600, vertical-align super.

- **Subtitle**:
  ```
  A flexible design partnership for founders, brands, and agencies who want top craft delivered on their timeline.
  ```
  - Max-width: 476px, 17px, line-height 1.45, weight 400, color `var(--muted)`, centered.

- **CTA row** (flex, gap 16px, centered):
  - **Primary button** "View Plans": height 56px, padding `18px 30px`, rounded-full, black bg, white text, 15px weight 600 Inter. Hover: translateY(-1px) + box-shadow `0 4px 20px rgba(0,0,0,0.12)`.
  - **Book button** "Chat for 15 minutes": white bg, `4px solid rgb(248,248,248)` border, rounded-full, padding `8px 24px 8px 8px`. Contains:
    - Avatar image (40px circle): `https://framerusercontent.com/images/hfneFL6CHBi5BnNvCeOaqU9HqE4.png`
    - Text stack: primary "Chat for 15 minutes" (14px, weight 600, black) and secondary "Pick a slot" (12px, weight 500, `rgb(152,152,152)`) with a green dot (`rgb(29, 204, 93)`, 8px circle).

- **Progressive blur** at bottom: absolute, full width, height 178px, gradient from transparent to `rgba(255,255,255,0.4)` at 40% to solid white.

**3. TrustedBy Section**
- Padding: 36px, max-width 1200px centered.
- Left: label "Partnered with top-tier companies globally" (max-width 163px, 14px, weight 500, muted color).
- Right: horizontal marquee (30s) of company names styled as text logos (16px, weight 600, black, each with distinct font-family):
  - Airbnb (Cedarville Cursive, 700), Shopify (system-ui, 800), Notion (Georgia, 500), Linear (Inter, 600), Webflow (Inter, 700), Figma (system-ui, 600), Slack (Georgia, 700), Stripe (system-ui, 800), Vercel (Inter, 600), Framer (Source Serif 4, 600).
- Same edge-fade marquee mask as ticker.

---

### Responsive Breakpoints

- **< 1200px**: Hero padding `140px 32px`, title clamp(60px, 8vw, 72px), navbar padding 32px, drawer links 40px.
- **< 810px**: Hero min-height 760px, padding `120px 24px 96px`. Background image rotated 90deg to fill portrait viewport. Side curved lines hidden, top horizontal lines shown. Title clamp(44px, 13vw, 52px). CTA buttons stack vertically full-width (max 320px). Trusted section stacks vertically. Drawer links 32px. Navbar padding 20px.

---

### Key Animation Keyframes

```css
@keyframes marquee-left {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

@keyframes line-pulse {
  0% { opacity: 0; transform: scale(1); }
  15% { opacity: 0.9; }
  70% { opacity: 0.4; }
  100% { opacity: 0; transform: scale(0.85); }
}
```

---

### CloudFront Video/Image URL

The hero background image URL (exact):
```
https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260626_041422_4a459e05-abce-4150-9fb7-4ededc423cd1.png&w=1280&q=85
```

The book button avatar URL (exact):
```
https://framerusercontent.com/images/hfneFL6CHBi5BnNvCeOaqU9HqE4.png
```
]
```

---

## 111. Wellbeing OS

- **Category**: Hero
- **Type**: hero
- **Page Type**: hero
- **ID**: `wellbeing-os`

```
Create a fullscreen hero section for a SaaS product called "flowpath" using React, Tailwind CSS, and Lucide React icons. The section should be a single `<section>` filling the viewport (`h-screen w-full overflow-hidden`).

**Background:**
- A looping, muted, autoplaying `<video>` element covering the full section with `object-cover`. Video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260703_053131_1ec3dd1c-d627-44fb-ab20-6e1fce41b0d5.mp4`
- A subtle dark overlay on top of the video: `bg-black/10`

**Font:**
- Use "Helvetica Now Text" as the primary font, loaded from: `https://db.onlinewebfonts.com/c/08e020de1811ec4489f82d1247a42c09?family=Helvetica+Now+Text`
- Fallback stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Applied globally via `* { font-family: ... }` in CSS

**Navigation (top, not fixed/sticky):**
- Full-width with responsive horizontal padding (`px-5 sm:px-6 md:px-12 lg:px-16`) and vertical padding (`py-4 sm:py-5`)
- Logo: An inline SVG diamond shape (28x28) with two overlapping diamond paths at 0.9 and 0.5 opacity, followed by the text "flowpath" in white, `text-lg sm:text-xl font-medium tracking-tight`
- Desktop nav (hidden on mobile): horizontal flex with items "Product" (dropdown: Connections, Workflows, Insights), "Solutions" (dropdown: Guides, Use cases, API reference), "About" (dropdown: Our story, Open roles, Reach us), "Plans" (no dropdown)
- Nav buttons: `text-white/90 hover:text-white text-sm font-medium`, with a `ChevronDown` icon (3.5x3.5) that rotates 180 degrees when dropdown is open
- Dropdowns open on hover (onMouseEnter/onMouseLeave), positioned `absolute top-full left-0`, using a custom `.liquid-glass` class, `rounded-xl py-3 px-2 min-w-[160px] shadow-xl`. Dropdown items: `text-white/80 hover:text-white text-sm rounded-lg hover:bg-white/5`
- Desktop CTA: "Log in" link (`text-white/90 hover:text-white text-sm font-medium`) and "Try it free" button using `.liquid-glass rounded-full px-5 py-2 text-white text-sm font-medium`
- Mobile menu button: animated toggle between `Menu` and `X` icons with rotation/scale/opacity transitions (duration-300)
- Mobile menu: absolutely positioned below nav, slides in with `cubic-bezier(0.16,1,0.3,1)` easing over 400ms. Background: `bg-[#2C221C]/95 backdrop-blur-xl rounded-2xl p-6`. Shows all nav items with sub-items indented, plus a bordered footer with Log in and Try it free

**Hero Content (below nav, top-aligned, not vertically centered):**
- Container: `flex-1 flex items-start justify-center` with `pt-16 sm:pt-20 md:pt-24` for spacing from the nav
- Text wrapper: `text-center max-w-3xl`
- Heading `<h1>`: `text-white text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl leading-[1.05] tracking-[-0.02em]`
  - Content (with line breaks):
    ```
    Bridge the
    gaps. <span class="text-white/60">Ditch the</span>
    <span class="text-white/60">grindwork.</span>
    ```
- Subheading `<p>`: `text-white/80 text-sm sm:text-base md:text-lg leading-relaxed max-w-md mx-auto mt-6 sm:mt-8`
  - Text: "Flowpath unifies your complete wellness tools, so your crew spends less energy plugging gaps and more on real progress."
- Two CTA buttons side by side (`flex flex-wrap items-center justify-center gap-3 sm:gap-4 mt-6 sm:mt-8`):
  1. "Begin your journey" - solid white button: `px-5 sm:px-6 py-2.5 sm:py-3 bg-white text-gray-900 text-sm font-semibold rounded-full hover:bg-white/90`
  2. "See it live" - glass button: `px-5 sm:px-6 py-2.5 sm:py-3 liquid-glass rounded-full text-white text-sm font-semibold hover:bg-white/10`

**Custom CSS (`.liquid-glass` class):**
```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

**Additional CSS utilities:**
```css
@keyframes dropdown-in {
  from { opacity: 0; transform: translateY(-4px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-dropdown { animation: dropdown-in 0.2s ease-out; }
.duration-400 { transition-duration: 400ms; }
```

**Important notes:**
- Dropdown elements need `!absolute` (Tailwind important modifier) to override the `position: relative` from `.liquid-glass`
- The entire section is fully responsive with breakpoints at sm, md, lg, xl
- No external UI libraries beyond Lucide React for icons
- Tailwind config is default with no extensions
```

---

## 112. Wellness Companion

- **Category**: Wellness
- **Type**: mobile
- **Page Type**: hero
- **ID**: `wellness-companion`

```
Build a mobile wellness quiz screen inside a realistic phone frame mockup, centered on a white page. Use React with Tailwind CSS and Lucide React icons.

**Phone Frame:**
- Dimensions: 375px wide x 780px tall
- Border radius: 52px
- Background color: `#8a9aaa`
- Box shadow to simulate a real phone bezel: `inset 0 0 0 2px rgba(255,255,255,0.08), 0 0 0 1px rgba(0,0,0,0.6), 0 0 0 10px #1a1a1e, 0 0 0 11px rgba(255,255,255,0.06), 0 0 60px rgba(0,0,0,0.5)`
- A black pill-shaped Dynamic Island at the top center: 120px wide, 32px tall, fully rounded, z-index 50

**Background:**
- Full-bleed background image using this exact URL: `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260704_143500_a76b8e64-2c69-4683-80e7-2bb060a921d6.png&w=1280&q=85`
- Apply `blur(12px)` and `scale(1.1)` to the background image
- Semi-transparent overlay: `#8a9aaa` at 30% opacity on top

**Font:**
- Load "Helvetica Now Var" from: `https://db.onlinewebfonts.com/c/e66905e07608167a84e6ad52f638c3c6?family=Helvetica+Now+Var`
- Fallback stack: 'Helvetica Neue', Helvetica, Arial, sans-serif
- Apply globally to all elements

**Content Layout (flex column, padding: 56px top, 24px sides, 24px bottom):**

1. **Header Badge** (top, with 40px margin-bottom):
   - Liquid glass pill with Timer icon (12px, white/80) + text "Vitaforge Daily" (12px, white/90, medium weight)
   - Padding: 10px vertical, 12px horizontal

2. **Title Section** (32px margin-bottom):
   - Subtitle: "Choose all that apply" - white/60, 14px
   - Heading: "What aspects of your wellness would you like to boost?" - white, 28px, normal weight, tight leading and tracking

3. **Selection Grid** (2 columns, 12px gap, pushes to fill available space):
   - 4 cards: "Sleep quality", "Stress", "Weight", "Skin"
   - Each card: rounded-[32px], 100px height, padding 16px
   - Shows a number label (01, 02, etc.) in white/50, 11px, medium weight
   - Option text in white, 16px, medium weight
   - "Stress" (id:2) and "Skin" (id:4) are pre-selected
   - Cards are toggleable on click

4. **Voice Button** (centered, 24px vertical margin):
   - Yellow/gold radial glow behind: `radial-gradient(ellipse at center, rgba(220,200,80,0.5) 0%, rgba(180,160,40,0.2) 40%, transparent 70%)`
   - 64px circular liquid glass button with a waveform SVG icon (white strokes, strokeWidth 2, strokeLinecap round) showing 5 vertical bars of varying heights
   - "voice" label below in white/70, 12px

5. **Slide-to-Confirm Button** (bottom, inside 24px horizontal padding):
   - Full-width rounded-full track, 56px tall, liquid glass style
   - White circular thumb (44px) on the left with ArrowRight icon (gray-800)
   - "Done" text centered in white/60, 14px, medium weight
   - 3 ChevronRight icons on the right (14px) at white/40, white/50, white/60 opacity
   - Draggable thumb with pointer events: snaps back if not dragged past 85%, snaps to end if past 85%

**Liquid Glass Effect (CSS classes):**

`.liquid-glass`:
- Background: `rgba(255,255,255,0.01)` with luminosity blend mode
- Backdrop filter: `blur(4px)`
- Box shadow: `inset 0 1px 1px rgba(255,255,255,0.1)`
- `::before` pseudo-element for gradient border: `linear-gradient(180deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%, rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%)` with 1.4px padding and mask-composite exclude technique

`.liquid-glass-selected`:
- Same as above but background: `rgba(255,255,255,0.12)`, blur 8px, stronger box shadow (`inset 0 1px 2px rgba(255,255,255,0.2)`), and brighter gradient border (0.6 alpha at edges, 0.25 at 20%/80%)

**Animations:**
- Staggered fade-up animation on all elements
- Keyframes: from `opacity:0, translateY(16px)` to `opacity:1, translateY(0)`
- Duration: 0.5s, easing: `cubic-bezier(0.22, 1, 0.36, 1)`, fill: forwards
- Delays: header 0.1s, title 0.25s, grid cards 0.4s/0.48s/0.56s/0.64s, voice 0.7s, slider 0.85s

**Dependencies:**
- React 18, Tailwind CSS 3, Lucide React, Vite, TypeScript
```

---

## 113. Travel Journal

- **Category**: Travel
- **Type**: mobile
- **Page Type**: hero
- **ID**: `travel-journal`

```
Create a mobile travel app UI mockup displayed inside a realistic iPhone-style phone frame, centered on a white webpage. Tech stack: React + TypeScript, Tailwind CSS, Lucide React icons, Vite. Font: Google Fonts "Inter" (weights 300-900).

---

**PAGE WRAPPER:**

Full viewport (`h-screen w-screen`), solid white background, flexbox centered, overflow hidden.

---

**PHONE FRAME:**

- Dimensions: 375px x 780px
- Background: `#0a0a0c`
- Border-radius: 52px
- Overflow: hidden
- Box-shadow (layered bezel effect):
  ```
  inset 0 0 0 2px rgba(255, 255, 255, 0.08),
  0 0 0 1px rgba(0, 0, 0, 0.6),
  0 0 0 10px #1a1a1e,
  0 0 0 11px rgba(255, 255, 255, 0.06),
  0 0 60px rgba(0, 0, 0, 0.5)
  ```

**Dynamic Island notch:** Absolute, top-0, centered horizontally, 120px wide, 28px tall, solid black, `rounded-b-2xl`, z-50.

---

**HEADER (absolute, top):**

- Z-index: 30
- `backdrop-filter: blur(12px)` with `background-color: rgba(10, 10, 12, 0.75)`
- Padding: `px-6 pt-14 pb-4`
- Left side: Button with "Asia" text (text-lg, font-semibold, white) + ChevronDown icon (size 18, text-white/70)
- Right side: Calendar icon button (size 22, text-white/70)

---

**SCROLLABLE CONTENT:**

- `overflow-y-auto` with hidden scrollbar
- Padding: `px-6 pt-28 pb-24`
- Vertical spacing: `space-y-4` (16px gap)

---

**DESTINATION CARDS (4 total):**

Each card:
- Full width, height 200px, rounded-2xl, overflow hidden, position relative
- Full-bleed background image (`absolute inset-0, object-cover`)
- Gradient overlay: `bg-gradient-to-t from-black/20 to-transparent`
- **Top-left:** liquid-glass pill (`rounded-full px-3 py-1`) with "{N} moments" text (text-white/90, text-xs, font-normal)
- **Top-right:** liquid-glass circle (w-8 h-8, rounded-full) with MoreHorizontal icon (size 16, text-white/80)
- **Bottom:** Destination name in 96px bold font, centered horizontally, clipped in an 80px tall container with `overflow: hidden`. Color: `rgba(255, 255, 255, 0.55)`, tracking-tight, leading-none, margin-top 2px

**Card data with exact image URLs:**

1. **Tokyo** - 23 moments
   `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260704_101902_e8f0f37b-18b7-4c14-bb5c-99f0724d2646.png&w=1280&q=85`

2. **Seoul** - 18 moments
   `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260704_101935_4b17f250-8ddb-4ff2-b63d-dfd3497d4428.png&w=1280&q=85`

3. **Bali** - 29 moments
   `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260704_101958_7116d6bf-fd6f-496f-b3cf-007688cd5123.png&w=1280&q=85`

4. **Rome** - 15 moments
   `https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260704_143008_72ee7299-04a8-474c-ae73-220d45b24a20.png&w=1280&q=85`

---

**FLOATING BOTTOM NAV BAR:**

- Absolute, bottom-6, centered horizontally, z-30
- liquid-glass pill (`rounded-full, flex, gap-6, px-6 py-2`)
- 3 nav items (flex-col, items-center, gap-0.5):
  - "Feed" + Home icon (size 20) -- inactive (`text-white/50`)
  - "Account" + User icon (size 20) -- inactive (`text-white/50`)
  - "Trips" + FileText icon (size 20) -- active (`text-white`)
- Label style: `text-[10px] font-medium`

---

**LIQUID-GLASS CSS:**

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

---

**STAGGERED ENTRANCE ANIMATION:**

Each card starts at `opacity: 0` and `transform: translateY(24px)`. On component mount, a `setTimeout` triggers a state change that transitions to `opacity: 1` and `translateY(0)`. Transition: `transition-all duration-700 ease-out`. Stagger delay: first card 150ms, each subsequent +120ms (150, 270, 390, 510ms). Implemented with React `useState` + `useEffect`.

---

**SCROLLBAR HIDING:**

```css
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
```

---

**GLOBAL:**

```css
* { font-family: 'Inter', sans-serif; }
```

Load in HTML head:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
```
```

---

## 114. Cross-Border

- **Category**: Transportation
- **Type**: mobile
- **Page Type**: hero
- **ID**: `cross-border`

```
Create a mobile-first logistics company landing page for "CARGOX GROUP" displayed inside an iPhone 15 Pro mockup frame. Use React, TypeScript, Tailwind CSS, and the `motion` library (motion/react) for animations. Use Vite as the build tool.

## Structure

The page is wrapped in a realistic iPhone 15 Pro mockup (aspect ratio 393:852) with:
- Dark frame (#1a1a1a) with 54px border-radius, 8px border (#2a2a2a), inset highlight (#3a3a3a)
- Dynamic Island (126x36px, centered at top, black, 20px border-radius, z-200)
- Home indicator at bottom (134x5px, white 30% opacity)
- Scrollable content area inside with hidden scrollbar and `container-type: size`

The body background is #111111. The scrollable container uses `container-type: size; container-name: phone;` for container queries.

## Fonts

- Import **Barlow Condensed 800** from Google Fonts
- Body font: Helvetica, Arial, sans-serif

## SECTION 1: Hero (full viewport height of the container using `100cqb`)

**Background:** Autoplaying, muted, looping video:
```
https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260620_185230_f7f71ef4-6655-469f-b9c6-efbdc1f7684a.mp4
```

**Navbar (absolute, top):**
- Left: "CARGOX" (white) / "GROUP" (yellow #ffda00) in Barlow Condensed 800, uppercase, clamp(22px, 6vw, 32px)
- Right: Hamburger menu icon (lucide-react Menu/X, 28px, white)
- Both slide in from left/right with 0.6s expo-out ease

**Mobile menu overlay:** Fixed, z-99, background #6682c2, centered nav items (Services, Industries, Company) in white 24px. AnimatePresence with scale + opacity transitions. Items stagger in from bottom.

**Hero content (bottom of section, z-10, padding 0 20px 24px):**
- Large headline in Barlow Condensed 800, uppercase, clamp(48px, 14vw, 72px), line-height 0.82:
  - "BEYOND" (white) - slides from x:-400
  - "BORDERS" (yellow #ffda00, text-align right) - slides from x:+400
  - "AND LIMITS" (white) - slides from x:-400
  - Staggered delays: 0s, 0.13s, 0.26s. Duration 0.85s, expo-out [0.16, 1, 0.3, 1]
- CTA Button: Custom SVG pill shape (fill #ffda00) with a circular end section containing a rotating arrow (white stroke, rotates from -135deg to -90deg on hover). Text "Get in touch" centered in the non-circle area. Font: Helvetica 20px, color #002a35. Hover: scale 1.08, y:-2. Tap: scale 0.97.

**Show hero content only after video `onCanPlay` fires** (fade in with AnimatePresence).

## SECTION 2: Info Card

**Background:** `linear-gradient(180deg, #C8C7B3 0%, #F0B172 50%, #EA7C58 100%)`
**Padding:** clamp(60px, 12vh, 120px) 20px

**Tagline** (scroll-triggered, slides from left):
- "LOGISTICS" in Barlow Condensed 800, white, clamp(44px, 13vw, 64px)
- "shaped by scale" / "powered by precision" in Helvetica, clamp(18px, 5vw, 26px), color #1a1a1a

**World Map:**
- Background map image: `https://polo-pecan-73837341.figma.site/_assets/v11/b6d561167283e799453232309bd13dd78b2d1afa.png`
- Aspect ratio 435/340, extends 20px beyond container edges
- SVG overlay (viewBox 0 0 299.037 142.509) at left:10%, top:18%, width:80% with 4 curved route paths in yellow (#FFDA00, 2.5 stroke):
  ```
  M128.161 74.6764C79.9989 130.001 71.9994 46.0005 20.9815 111.737
  M216.999 9.99985C260.499 12.4998 222.499 71.9998 291.999 58.9998
  M130.102 70.9998C144.499 -32.0002 183.852 70.2739 219.999 3.99985
  M14.4999 16.9998C111 20.9998 -53.0003 73.4998 21.4999 107
  ```
- Route lines animate with `pathLength` from 0 to 1, staggered
- Animated yellow arrow polygons (points="0,-4 8,0 0,4") using SVG `<animateMotion>` along each path, rotating automatically
- 5 stop dots at coordinates: [9.519,15.519], [289.519,59.518], [220.519,9.519], [125.518,78.519], [19.519,104.519] - each is a yellow circle r=9.519 with dark center r=3.389 (#002A35). They pop in with scale animation.
- 3 floating transport icons (white circle bg, 16% width, rounded-full, box-shadow):
  - Ship: `https://image-bottom-92901062.figma.site/_components/v2/142c6a6f3074dd8aee013fa440ff4ff369649d48/08d6a37375d428e07c59e24a8529de89bfee157e.08d6a373.png` at left:26%, top:28.9%
  - Car: `https://image-bottom-92901062.figma.site/_components/v2/142c6a6f3074dd8aee013fa440ff4ff369649d48/7d6f50a87e1427d9b4d1a9c9f1c064ff04b2b3f9.7d6f50a8.png` at left:70.8%, top:15.6%, rotate(9.73deg)
  - Plane: `https://image-bottom-92901062.figma.site/_components/v2/142c6a6f3074dd8aee013fa440ff4ff369649d48/0e0282ab1c70db03d437b0d01875ce45557d49f6.0e0282ab.png` at left:55.2%, top:52.1%, rotate(180deg) scaleY(-1)
  - Icons pop in (scale 0.5 -> 1), then continuously float up/down with infinite y animation

**Stats** (scroll-triggered, slide in from opposite sides):
- "3M+" white Barlow Condensed 800, clamp(50px, 14vw, 72px) + "tons of cargo / delivered / without delays" in #1a1a1a, clamp(14px, 3.8vw, 18px)
- "13+" same styling, indented left clamp(40px, 12vw, 90px) + "years of trusted / and reliable / operations"

## SECTION 3: Contact Us

**Background:** #0a1f2b
**Padding:** clamp(48px, 10vh, 96px) 20px clamp(32px, 6vh, 64px)

**Heading** (scroll-triggered fade+slide from bottom):
- "CONTACT " (white) + "US" (yellow #ffda00), Barlow Condensed 800, clamp(44px, 13vw, 64px)
- Subtitle: "Complete the form and our team will contact you soon." in #b0b8bc, clamp(14px, 3.8vw, 18px)

**Form fields** (scroll-triggered, stagger from bottom):
- 3 inputs (First Name, Last Name, E-mail): pill-shaped (40px radius), bg rgba(255,255,255,0.08), white text, clamp(14px, 3.5vw, 16px). On focus: bg brightens to 0.14, slight scale 1.01.
- "Send" button: pill, bg #FFDA00, color #0a1f2b, font-weight 700, clamp(16px, 4vw, 20px). Hover: scale 1.03, y:-2, bg #ffe84d. Tap: scale 0.97.

**Footer info:**
- Email: info@cargox-group.com
- Phone: +380 44 234-7890
- Color #b0b8bc, hover slides right 4px and turns white

**Social icons** (3 white circles 44x44, hover: scale 1.15, y:-3):
- Instagram, LinkedIn, Facebook (inline SVG icons, fill #0a1f2b)

**Scroll-to-top button** (right side): white 44x44 circle with up-arrow SVG, same hover animation.

**Copyright:** "(c) 2025. All rights reserved." in #6b7a80, clamp(12px, 3.2vw, 14px)

## Animation System

- Use `motion/react` (NOT framer-motion)
- Easing curves: EXPO_OUT = [0.16, 1, 0.3, 1], EASE_OUT = [0.25, 0.46, 0.45, 0.94]
- Scroll-triggered reveals using `useInView` from motion/react with `once: true` and margin: '0px 0px -40px 0px' or '0px 0px -60px 0px'
- All scroll animations fire only once
- Transport icons have infinite floating y-axis animation with varying durations (2.5-3.3s)
- Mobile menu uses AnimatePresence for enter/exit

## Dependencies

```json
{
  "motion": "^12.40.0",
  "lucide-react": "^0.344.0",
  "react": "^18.3.1",
  "react-dom": "^18.3.1"
}
```
```

---

