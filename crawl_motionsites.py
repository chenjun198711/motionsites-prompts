#!/usr/bin/env python3
"""
MotionSites.ai 提示词爬虫脚本
==============================
自动爬取 motionsites.ai 网站的所有提示词数据（Sites + Apps），
通过 Supabase Edge Function 获取完整提示词文本，
最终输出 JSON 和 Markdown 两种格式的报告。

特点:
  - 无需手动输入，直接运行即可
  - 自动从网站 JS 中提取最新的 API Key
  - 内置全部 241 个提示词的元数据（224 网站 + 17 应用）
  - 每 20 条自动保存一次，防止中途崩溃丢失数据
  - 支持断点续爬（跳过已获取的提示词）

用法:
    python3 crawl_motionsites.py

依赖:
    pip install requests

输出文件:
    - motionsites_all_prompts.json  (结构化 JSON 数据)
    - motionsites_all_prompts.md    (Markdown 汇总报告)
"""

import json
import time
import sys
import re
from pathlib import Path

import requests

# ============================================================
# 内置提示词元数据（从 motionsites.ai 页面提取）
# 格式: (id, title, category, type, is_free, platform)
# ============================================================
PROMPTS_METADATA = [
    # ===== Sites (网站类提示词) =====
    ("3d-story", "3D Story", "Landing Page", "hero", False, "website"),
    ("interactive-discovery", "Interactive Discovery", "Hero", "hero", True, "website"),
    ("urban-jungle-hero", "Urban Jungle", "Landing Page", "hero", False, "website"),
    ("3d-jack-portfolio-hero", "3D Portfolio", "Portfolio", "hero", True, "website"),
    ("shamoni-hero", "Shamoni", "Hero Section", "hero", False, "website"),
    ("solar-energy-hero", "Solar Energy Hero", "Hero", "hero", False, "website"),
    ("zenith-realty-landing", "Zenith Realty", "Landing Page", "landing-page", False, "website"),
    ("interactive-portfolio", "Interactive Portfolio", "Hero", "hero", False, "website"),
    ("asme-hero", "Asme", "Hero Section", "hero", True, "website"),
    ("jewelry-store", "Jewelry Store", "Ecommerce", "hero", False, "website"),
    ("dreamcore-landing", "Dreamcore Landing", "Landing Page", "hero", False, "website"),
    ("ai-driving-assistant", "AI Driving Assistant", "AI SaaS Website", "hero", False, "website"),
    ("bold-studio", "Bold Studio", "Hero", "hero", True, "website"),
    ("celestial-renewal", "Celestial Renewal", "Wellness", "hero", True, "website"),
    ("prisma-landing", "Prisma Creative Studio", "Landing Page", "landing-page", True, "website"),
    ("ai-meeting-notes", "AI Meeting Notes", "SaaS", "hero", False, "website"),
    ("product-studio", "Product Studio", "Agency Website", "hero", False, "website"),
    ("art-landing", "Art Landing", "Landing Page", "hero", False, "website"),
    ("sky-estate", "Sky Estate", "Real Estate", "hero", False, "website"),
    ("velorah-hero", "Velorah", "Agency", "", True, "website"),
    ("outdoor-apparel", "Outdoor Apparel", "Fashion", "hero", False, "website"),
    ("9", "Web3 EOS Hero", "Web3", "", False, "website"),
    ("oyla", "OYLA", "Ecommerce", "hero", False, "website"),
    ("aetheris-voyage-hero", "Aetheris Voyage", "Hero Section", "hero", True, "website"),
    ("pulse-3d", "Pulse 3D", "3D Website", "hero", False, "website"),
    ("codercrest-hero", "CoderCrest", "SaaS", "", False, "website"),
    ("future-state", "Future-State", "Landing Page", "hero", False, "website"),
    ("vex-ventures-hero", "VEX Ventures", "Hero Section", "hero", True, "website"),
    ("cleantech", "CleanTech", "Sustainability", "hero", False, "website"),
    ("skyelite-hero", "SkyElite Private Jets", "Landing Page", "hero", True, "website"),
    ("stillmind", "Stillmind", "Hero", "hero", True, "website"),
    ("reveal-hero", "Reveal Hero", "Hero", "hero", False, "website"),
    ("financial-suite", "Financial Suite", "Landing Page", "hero", False, "website"),
    ("modern-agency", "Modern Agency", "Agency", "hero", True, "website"),
    ("lead-funnel", "Lead Funnel", "Hero", "hero", False, "website"),
    ("liquid-glass-agency", "Liquid Glass Agency", "Landing Page", "landing-page", False, "website"),
    ("tech-forward", "Tech-Forward", "Hero", "hero", True, "website"),
    ("luxury-editorial-ecommerce-design", "Luxury Ecommerce Design", "Landing Page", "landing", False, "website"),
    ("vision-reveal", "Vision Reveal", "Hero", "hero", True, "website"),
    ("grow-ai-hero", "Grow AI Talent Platform", "SaaS", "", False, "website"),
    ("prompt-hero", "PROMPT", "Landing Page", "hero", True, "website"),
    ("aethera-hero", "Aethera Studio", "Hero Section", "hero", True, "website"),
    ("wellness-balance", "Wellness Balance", "Hero", "hero", True, "website"),
    ("5", "Glassmorphism Agency Hero", "Agency", "", False, "website"),
    ("bio-age-dashboard", "Bio-Age Dashboard", "Hero", "hero", False, "website"),
    ("14", "Logoisum Video Agency Hero", "Agency", "", False, "website"),
    ("integration-saas", "Integration SaaS", "Hero", "hero", False, "website"),
    ("innovation-landing", "Innovation", "Landing Page", "landing-page", True, "website"),
    ("cozypaws", "CozyPaws", "Hero", "hero", True, "website"),
    ("10", "AI Automation Hero", "AI / SaaS", "", False, "website"),
    ("health-portal", "Health Portal", "Landing Page", "hero", True, "website"),
    ("orbis-nft-landing", "Orbis NFT", "Landing Page", "landing-page", True, "website"),
    ("cosmos-interface", "Cosmos Interface", "Landing Page", "hero", False, "website"),
    ("7", "Synapse Dark Hero", "SaaS", "", False, "website"),
    ("3d-collectible-hero", "3D Collectible Hero", "3D Website", "3D Website", True, "website"),
    ("portfolio-cosmic-hero", "Portfolio Cosmic", "Portfolio", "hero", True, "website"),
    ("luxury-hero", "Luxury Hero", "Hero", "hero", False, "website"),
    ("16", "HR SaaS Hero", "SaaS", "", False, "website"),
    ("network-hero", "Network Hero", "Hero", "hero", True, "website"),
    ("securify-hero", "Securify Data Security", "SaaS", "hero", True, "website"),
    ("investment-hero", "Investment Gate", "Landing Page", "hero", False, "website"),
    ("1", "New Era Bold Hero", "Creative", "", False, "website"),
    ("golden-portal", "Golden Portal", "Landing Page", "hero", False, "website"),
    ("portal-hero", "Portal", "Hero Section", "hero", True, "website"),
    ("immersive-ocean", "Immersive Ocean", "Hero", "hero", True, "website"),
    ("21", "Buzzentic Agency", "Agency", "", False, "website"),
    ("wellbeing-os", "Wellbeing OS", "Hero", "hero", True, "website"),
    ("mindloop-landing", "Mindloop Landing", "Landing Page", "landing-page", True, "website"),
    ("innovation-studio", "Innovation Studio", "Hero", "hero", False, "website"),
    ("18", "Loader Animation", "Animation", "", False, "website"),
    ("subscription-agency", "Subscription Agency", "Hero", "hero", True, "website"),
    ("ember-dsgn-hero", "EMBER.dsgn", "Hero Section", "hero", False, "website"),
    ("creative-portfolio", "Creative Portfolio", "Hero", "hero", True, "website"),
    ("3", "ClearInvoice SaaS Hero", "SaaS", "", False, "website"),
    ("obsidian-hero", "Obsidian Hero", "Hero", "hero", False, "website"),
    ("rivr-hero", "RIVR", "Hero Section", "hero", True, "website"),
    ("apex-pulse", "Apex Pulse", "Landing Page", "hero", False, "website"),
    ("wisa-space-hero", "WISA Space", "Hero Section", "hero", False, "website"),
    ("neon-logic", "Neon Logic", "Landing Page", "hero", True, "website"),
    ("vortex-studio-hero", "AI Designer Portfolio", "Landing Page", "hero", True, "website"),
    ("unwind-hero", "Unwind Hero", "Hero", "hero", False, "website"),
    ("12", "Targo Logistics Hero", "Automotive", "", False, "website"),
    ("glitch-pulse", "Glitch Pulse", "Landing Page", "hero", False, "website"),
    ("codenest-hero", "CodeNest Coding Platform", "Landing Page", "", True, "website"),
    ("impact-ventures", "Impact Ventures", "Hero", "hero", True, "website"),
    ("acreage-farming-hero", "Acreage Farming", "Landing Page", "landing-page", False, "website"),
    ("organic-odyssey", "Organic Odyssey", "Hero", "hero", True, "website"),
    ("power-ai-hero", "Power AI", "Hero Section", "hero", True, "website"),
    ("cargo-group", "Cargo Group", "Hero", "hero", False, "website"),
    ("impressive-hero", "Impressive Hero", "Hero Section", "hero", False, "website"),
    ("cyberpunk-reveal", "Cyberpunk Reveal", "Hero", "hero", False, "website"),
    ("bloom-ai-hero", "Bloom AI", "Hero Section", "", True, "website"),
    ("ai-interface", "AI Interface", "Landing Page", "hero", False, "website"),
    ("flowmate-landing", "FlowMate", "Landing Page", "landing-page", False, "website"),
    ("vertex-sci", "Vertex Sci", "Hero", "hero", False, "website"),
    ("luminex-hero", "Luminex", "Hero Section", "hero", True, "website"),
    ("neural-interface", "Neural Interface", "Landing Page", "hero", False, "website"),
    ("nike-premium-landing", "Nike Premium Landing", "Landing Page", "hero", False, "website"),
    ("wellness-hero", "Wellness Hero", "Hero", "hero", True, "website"),
    ("sentinel-ai-hero", "Sentinel AI", "Hero Section", "hero", True, "website"),
    ("cosmic", "Cosmic", "Hero", "hero", False, "website"),
    ("bl", "Bloom", "Landing Page", "landing", False, "website"),
    ("slam-dunk-hero", "Slam Dunk", "Hero Section", "hero", False, "website"),
    ("saas-value", "SaaS Value", "SaaS", "hero", True, "website"),
    ("designpro-hero", "DesignPro Academy", "Hero Section", "hero", True, "website"),
    ("luxury-focus", "Luxury Focus", "E-commerce", "landing", False, "website"),
    ("crypto-wealth-hero", "Crypto Wealth", "Hero Section", "hero", False, "website"),
    ("synthesis", "Synthesis", "Landing Page", "hero", False, "website"),
    ("nexora-hero", "Nexora Automation", "SaaS", "hero", True, "website"),
    ("conversion", "Conversion", "Hero", "hero", False, "website"),
    ("luminara", "Luminara", "Hero", "hero", False, "website"),
    ("transform-data-hero", "Transform Data", "Hero Section", "hero", True, "website"),
    ("nexacore-hero", "NexaCore", "Landing Page", "hero", False, "website"),
    ("digital-experiences", "Digital Experiences", "Landing Page", "hero", True, "website"),
    ("halo-usd-landing", "USD Halo", "Landing Page", "landing-page", True, "website"),
    ("gateway-portal", "Gateway Portal", "Landing page", "hero", False, "website"),
    ("stellar-ai-v2-hero", "Sync AI", "Hero Section", "hero", False, "website"),
    ("audio-showcase", "Audio Showcase", "Hero", "hero", True, "website"),
    ("taskly-hero", "Taskly", "Hero Section", "", True, "website"),
    ("eco-intelligence", "Eco Intelligence", "Hero", "hero", False, "website"),
    ("xportfolio-hero", "xPortfolio Hero", "Hero Section", "hero", False, "website"),
    ("yoga-coach", "Yoga Coach", "Landing Page", "hero", False, "website"),
    ("stellar-ai-hero", "Stellar AI", "Hero Section", "hero", True, "website"),
    ("luxury-real-estate", "Luxury Real Estate", "Landing Page", "hero", False, "website"),
    ("ai-designer-agency", "AI Designer Agency", "Landing Page", "landing-page", False, "website"),
    ("datacore-booking-hero", "Datacore Booking", "SaaS", "", True, "website"),
    ("mythic-naturecore", "Mythic Naturecore", "landing page", "hero", False, "website"),
    ("neovision-landing", "NeoVision", "Landing Page", "landing-page", False, "website"),
    ("cinematic-brand", "Cinematic Brand", "Hero", "hero", False, "website"),
    ("convix-software-hero", "Convix Software", "SaaS", "", True, "website"),
    ("guardnet-landing", "Guardnet", "Landing Page", "landing-page", False, "website"),
    ("neuralyn-hero", "Neuralyn", "SaaS", "", True, "website"),
    ("layered-depth", "Layered Depth", "Landing Page", "hero", False, "website"),
    ("automation-machines-hero", "Automation Machines", "Hero Section", "hero", False, "website"),
    ("intelligentx", "IntelligentX", "Hero", "hero", True, "website"),
    ("digitwist-hero", "Digitwist AI Builder", "SaaS", "", True, "website"),
    ("retro-futurist", "Retro-Futurist", "Hero", "hero", True, "website"),
    ("20", "Space Voyage", "Landing Page", "", False, "website"),
    ("cursor-follow", "Cursor Follow", "Hero", "hero", False, "website"),
    ("dot-hero", "Dot", "Hero Section", "hero", True, "website"),
    ("luxury-botanical", "Luxury Botanical", "Landing Page", "hero", False, "website"),
    ("focus-ai-landing", "Focus AI", "Landing Page", "landing-page", False, "website"),
    ("growth-marketing-saas", "Growth Marketing SaaS", "Hero", "hero", False, "website"),
    ("design-rocket-email-hero", "Email Marketing", "Email Marketing", "hero", True, "website"),
    ("build-with-us", "Build With Us", "Contact us", "hero", True, "website"),
    ("rivr-defi-landing", "RIVR DeFi", "Landing Page", "landing-page", False, "website"),
    ("contact-cybernetic", "Contact Cybernetic", "Hero", "hero", True, "website"),
    ("duolingo-styleguide-hero", "Duolingo Styleguide", "Hero Section", "hero", True, "website"),
    ("aerocore", "AeroCore", "Landing Page", "hero", False, "website"),
    ("yacht-club-hero", "Yacht Club", "Landing Page", "hero", False, "website"),
    ("scroll-landing", "Scroll Landing Page", "Interactive", "hero", False, "website"),
    ("ecommerce-website-landing", "E-commerce Website", "Landing Page", "landing-page", False, "website"),
    ("digital-epoch-hero", "Digital Epoch", "Hero Section", "hero", True, "website"),
    ("finflow", "FinFlow", "Fintech", "hero", False, "website"),
    ("ecovolta-hero", "EcoVolta", "Hero Section", "hero", False, "website"),
    ("bio-digital", "Bio-Digital", "Hero", "hero", False, "website"),
    ("orbit-engineers", "Orbit Engineers", "Agency", "landing-page", False, "website"),
    ("velorix-iic", "Velorix IIC", "Hero", "hero", False, "website"),
    ("pro-ai-deck", "Pro AI Deck", "Presentation", "", False, "website"),
    ("no-code-waitlist", "No-Code Waitlist", "Waitlist", "hero", True, "website"),
    ("terra-hero", "Terra Geo Map", "SaaS", "hero", False, "website"),
    ("portal", "Portal", "Hero", "hero", True, "website"),
    ("veloce-finance-landing", "Veloce Finance", "Landing Page", "landing-page", False, "website"),
    ("clubx-hero", "ClubX Investors", "Hero Section", "hero", False, "website"),
    ("railroad-ai-hero", "Railroad.ai", "Hero Section", "hero", False, "website"),
    ("6", "Bold Portfolio Hero", "Portfolio", "", False, "website"),
    ("vaultshield", "VaultShield", "Hero", "hero", True, "website"),
    ("slate-hero", "Slate", "SaaS", "", False, "website"),
    ("ecovolta-v2-hero", "EcoVolta V2", "Hero Section", "hero", False, "website"),
    ("evr-ventures-hero", "EVR Ventures", "Hero Section", "hero", False, "website"),
    ("cinematic-landing-page", "Cinematic Landing Page", "Landing Page", "", False, "website"),
    ("ai-workflow", "AI Workflow Hero", "Hero", "hero", True, "website"),
    ("ai-automation", "AI Automation", "Landing Page", "hero", False, "website"),
    ("cybersecurity-hero-v2", "Cybersecurity Hero v2", "Hero", "hero", False, "website"),
    ("nimbus-grid", "Nimbus Grid", "Landing Page", "hero", False, "website"),
    ("book-hero", "Book Hero", "Hero", "hero", False, "website"),
    ("neo-museum", "Neo Museum", "Website", "hero", True, "website"),
    ("minimal-workflow-saas", "Minimal Workflow SaaS", "SaaS", "hero", False, "website"),
    ("futuristic-tech", "Futuristic Tech", "Hero", "hero", False, "website"),
    ("evergreen-finance", "Evergreen Finance", "Fintech", "hero", False, "website"),
    ("visual-hero", "Visual Hero", "Hero", "hero", True, "website"),
    ("stellar-launch", "Stellar Launch", "Landing Page", "hero", False, "website"),
    ("financialfocus", "FinancialFocus", "Hero", "hero", False, "website"),
    ("creative-studio", "Creative Studio", "Agency", "hero", True, "website"),
    ("wanderful-hero", "Wanderful Hero", "Travel", "hero", True, "website"),
    ("bookedup", "BookedUp", "SaaS", "hero", False, "website"),
    ("travel-hero", "Scenic Travel", "Landing Page", "hero", False, "website"),
    ("prosthetics-hero", "Prosthetics Hero", "Hero", "hero", True, "website"),
    ("novadesk-signup", "NovaDesk Signup", "Signup", "hero", False, "website"),
    ("learnly", "Learnly", "Hero", "hero", False, "website"),
    ("speakup-venture-hero", "SpeakUp Venture Hero", "Hero", "hero", False, "website"),
    ("futuristic-cinematic", "Futuristic Cinematic", "Hero", "hero", False, "website"),
    ("email-landing-page", "Email Landing Page", "Landing page", "landing", True, "website"),
    ("auramail", "AuraMail", "SaaS", "hero", False, "website"),
    ("waitlist-hero", "Waitlist Hero", "Hero", "hero", False, "website"),
    ("ai-image-generator-ui", "AI Image Generator UI", "AI", "hero", True, "website"),
    ("aurora-onboard", "Aurora Onboard", "Signup", "hero", True, "website"),
    ("naturecore-saas", "Naturecore SaaS", "Hero", "hero", False, "website"),
    ("creative-agency", "Creative Agency", "Landing Page", "hero", False, "website"),
    ("vertex-ai-hero", "VertexAI Hero", "Hero Section", "hero", False, "website"),
    ("cybersecurity-hero", "Cybersecurity Hero", "Hero", "hero", True, "website"),
    ("prioritize-hero", "Prioritize", "Hero Section", "hero", False, "website"),
    ("equilibrium", "Equilibrium", "Hero", "hero", True, "website"),
    ("404", "Nexto 404", "404", "hero", True, "website"),
    ("vitara-hero", "Vitara", "Landing Page", "hero", False, "website"),
    ("orbit-web3-hero", "Orbit Web3", "Web3", "hero", False, "website"),
    ("akor-security-landing", "AKOR Security", "Landing Page", "landing-page", False, "website"),
    ("bionova-hero", "Bionova Biotech", "SaaS", "hero", False, "website"),
    ("mindloop-hero", "Mindloop", "SaaS", "hero", False, "website"),
    ("nexus-hero", "Nexus IT Solutions", "Hero Section", "hero", False, "website"),
    ("nova-space-landing", "NOVA Space Systems", "Landing Page", "landing-page", False, "website"),
    ("nickel-hero", "Nickel Payments", "SaaS", "hero", False, "website"),
    ("13", "Framelix 3D Studios", "Creative / 3D", "", False, "website"),
    ("15", "Dark Portfolio Hero", "Portfolio", "", False, "website"),
    ("19", "Viktor Portfolio", "Portfolio", "", False, "website"),
    ("deck-investor", "Investor Deck", "Presentation", "hero", False, "website"),
    ("11", "Weblex Dark Hero", "Landing Page", "", False, "website"),
    ("8", "New Era Automotive Hero", "Automotive", "", False, "website"),
    ("4", "Datacore SaaS Hero", "SaaS", "", False, "website"),
    ("finlytic-hero", "Finlytic AI Agent", "SaaS", "hero", False, "website"),
    ("2", "Taskora SaaS Hero", "SaaS", "", False, "website"),
    ("0", "Wealth Video Hero", "Fintech", "", False, "website"),
    ("apex-saas-hero", "Apex SaaS", "SaaS", "", False, "website"),
    ("planet-orbit-hero", "Planet Orbit", "SaaS", "", False, "website"),

    # ===== Apps (移动应用类提示词) =====
    ("innovation-summit", "Innovation Summit", "Mobile App", "Mobile", False, "app"),
    ("place-saver", "Place Saver", "Travel", "mobile", True, "app"),
    ("wellness-companion", "Wellness Companion", "Wellness", "mobile", True, "app"),
    ("gear-shop", "Gear Shop", "Ecommerce App", "mobile", False, "app"),
    ("mood-tracker", "Mood Tracker", "Wellness", "mobile", False, "app"),
    ("coffee-rewards", "Coffee Rewards", "Loyalty App", "mobile", True, "app"),
    ("travel-explorer", "Travel Explorer", "Travel", "mobile", False, "app"),
    ("cargox-mobile", "CARGOX Mobile", "Transportation", "mobile", False, "app"),
    ("movie-premiere", "Movie Premiere", "Entertainment", "mobile", False, "app"),
    ("lodge-booking-app", "Lodge Booking App", "Booking", "mobile", False, "app"),
    ("travel-journal", "Travel Journal", "Travel", "mobile", True, "app"),
    ("pet-products", "Pet Products", "Ecommerce App", "mobile", False, "app"),
    ("cross-border", "Cross-Border", "Transportation", "mobile", True, "app"),
    ("supplement-shop", "Supplement Shop", "Health", "mobile", False, "app"),
    ("remit-race", "Remit Race", "Fintech", "mobile", False, "app"),
    ("luxury-escapes", "Luxury Escapes", "Travel App", "mobile", False, "app"),
    ("skills-lea", "LearnHub", "Education", "mobile", False, "app"),
]

# 默认 API Key（从 motionsites.ai JS 中提取，可通过 extract_api_key 自动更新）
DEFAULT_SUPABASE_URL = "https://xgdzyqfalbibzelpdpvr.supabase.co"
DEFAULT_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhnZHp5cWZhbGJpYnplbGRkcHZyIiwi"
    "cm9sZSI6ImFub24iLCJpYXQiOjE3NzE4MzUwMDYsImV4cCI6MjA4NzQxMTAwNn0."
    "u8lH5Y14xx2WxrNEBp8ngkJlijIYHJASq_gOzTaINZY"
)

# 输出目录
OUTPUT_DIR = Path(__file__).parent

# 请求间隔（秒）
REQUEST_DELAY = 0.3

# 最大重试次数
MAX_RETRIES = 3

# 网站基础 URL
SITE_URL = "https://motionsites.ai"


def extract_api_key():
    """
    从 motionsites.ai 的 JS 打包文件中动态提取 Supabase URL 和 API Key。
    如果提取失败，返回默认值。
    """
    try:
        print("正在从网站提取 API Key...")
        resp = requests.get(SITE_URL, timeout=15)
        resp.raise_for_status()

        # 查找 JS 打包文件 URL
        js_match = re.search(r'src="(/assets/index-[^"]+\.js)"', resp.text)
        if not js_match:
            print("  [警告] 未找到 JS 文件，使用默认 API Key")
            return DEFAULT_SUPABASE_URL, DEFAULT_ANON_KEY

        js_url = f"{SITE_URL}{js_match.group(1)}"
        js_resp = requests.get(js_url, timeout=30)
        js_resp.raise_for_status()
        js_text = js_resp.text

        # 提取 Supabase URL
        url_match = re.search(r'(https://[a-z0-9]+\.supabase\.co)', js_text)
        supabase_url = url_match.group(1) if url_match else DEFAULT_SUPABASE_URL

        # 提取 API Key（JWT 格式），取 supabase URL 附近的一个
        idx = js_text.find(supabase_url)
        if idx >= 0:
            context = js_text[idx:idx + 500]
            key_match = re.search(
                r'"(eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)"',
                context,
            )
            if key_match:
                print(f"  API Key 提取成功 (URL: {supabase_url})")
                return supabase_url, key_match.group(1)

        # 回退：在全文中搜索
        all_keys = re.findall(
            r'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
            js_text,
        )
        if all_keys:
            print(f"  API Key 提取成功 (全文搜索)")
            return supabase_url, all_keys[0]

        print("  [警告] API Key 提取失败，使用默认值")
        return DEFAULT_SUPABASE_URL, DEFAULT_ANON_KEY

    except Exception as e:
        print(f"  [警告] 提取 API Key 时出错: {e}，使用默认值")
        return DEFAULT_SUPABASE_URL, DEFAULT_ANON_KEY


def make_headers(api_key):
    """构建请求头"""
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def fetch_prompt_text(supabase_url, api_key, prompt_id):
    """
    调用 Edge Function 获取单个提示词的完整文本。
    返回 (prompt_text, code) 元组。
    """
    headers = make_headers(api_key)
    url = f"{supabase_url}/functions/v1/get-prompt"
    payload = {"prompt_id": prompt_id}

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("prompt_text", "") or ""
                code = data.get("code", "")
                return text, code
            else:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1)
        except requests.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)

    return "", "request_failed"


def generate_description(title, category, platform):
    """根据标题和分类生成简短中文描述"""
    platform_label = "移动应用" if platform == "app" else "网页"
    return f"{title} - {category}类{platform_label}提示词模板。"


def load_existing_results(json_path):
    """加载已有结果（用于断点续爬）"""
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_json(data, filepath):
    """保存为 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  JSON 已保存: {filepath} ({len(data)} 条记录)")


def save_markdown(data, filepath):
    """保存为 Markdown 汇总报告"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# MotionSites 提示词一键提取报告\n\n")
        f.write(
            f"自动从 [motionsites.ai](https://motionsites.ai) 爬取，"
            f"共提取 **{len(data)}** 个提示词。\n\n"
        )

        # 汇总表格
        f.write("## 提示词汇总表\n\n")
        f.write("| 序号 | 标题 | 分类 | 平台 | 权限 | 提示词预览 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")

        for i, item in enumerate(data, 1):
            title = item.get("title", "N/A")
            category = item.get("category", "N/A")
            platform = "App" if item.get("platform") == "app" else "Web"
            is_free = "免费" if item.get("is_free") else "Premium"
            prompt_raw = item.get("prompt_text", "")
            preview = prompt_raw.replace("\n", " ").replace("|", "\\|")
            if len(preview) > 60:
                preview = preview[:57] + "..."
            f.write(f"| {i} | {title} | {category} | {platform} | {is_free} | {preview} |\n")

        # 详细内容
        f.write("\n\n## 详细提示词内容\n\n")
        for item in data:
            title = item.get("title", "N/A")
            category = item.get("category", "N/A")
            platform = "App" if item.get("platform") == "app" else "Web"
            is_free = "免费" if item.get("is_free") else "Premium"
            prompt_text = item.get("prompt_text") or "(Premium 限制，无法获取)"

            f.write(f"### {title}\n")
            f.write(f"- **所属分类**: {category}\n")
            f.write(f"- **平台**: {platform}\n")
            f.write(f"- **访问权限**: {is_free}\n")
            f.write("- **完整提示词**:\n\n")
            f.write(f"```text\n{prompt_text}\n```\n\n")
            f.write("---\n\n")

    print(f"  Markdown 已保存: {filepath}")


def main():
    print("=" * 60)
    print("  MotionSites.ai 提示词爬虫")
    print("=" * 60)
    print()

    # Step 1: 提取 API Key
    supabase_url, api_key = extract_api_key()
    print()

    # Step 2: 准备提示词列表
    total = len(PROMPTS_METADATA)
    print(f"内置提示词列表: {total} 个")
    site_count = sum(1 for p in PROMPTS_METADATA if p[5] == "website")
    app_count = sum(1 for p in PROMPTS_METADATA if p[5] == "app")
    print(f"  - 网站 (Sites): {site_count} 个")
    print(f"  - 应用 (Apps): {app_count} 个")
    print()

    # Step 3: 加载已有结果（断点续爬）
    json_path = OUTPUT_DIR / "motionsites_all_prompts.json"
    existing = load_existing_results(json_path)
    existing_ids = {
        item["id"] + "_" + item.get("platform", "")
        for item in existing
        if item.get("prompt_text")  # 只跳过已成功获取的
    }

    if existing:
        print(f"发现已有结果: {len(existing)} 条 (其中 {len(existing_ids)} 条已获取文本，将跳过)")
        results = list(existing)
    else:
        results = []

    # Step 4: 逐个获取提示词文本
    print(f"\n开始爬取提示词文本...")
    print(f"(每个请求间隔 {REQUEST_DELAY} 秒，预计耗时约 {total * REQUEST_DELAY:.0f} 秒)\n")

    success_count = sum(1 for r in results if r.get("prompt_text"))
    skip_count = 0
    fail_count = 0

    # 构建已有结果的查找表
    result_map = {}
    for r in results:
        key = r["id"] + "_" + r.get("platform", "")
        result_map[key] = r

    for i, (pid, title, category, ptype, is_free, platform) in enumerate(PROMPTS_METADATA, 1):
        key = pid + "_" + platform

        # 断点续爬：跳过已获取的
        if key in existing_ids:
            skip_count += 1
            print(f"  [{i}/{total}] {title} ({pid}) - [跳过，已存在]")
            continue

        print(f"  [{i}/{total}] {title} ({pid})")

        prompt_text, code = fetch_prompt_text(supabase_url, api_key, pid)

        if prompt_text:
            success_count += 1
        else:
            fail_count += 1
            if code == "paid_only":
                print(f"    -> Premium 限制，无法获取文本")
            elif code == "not_found":
                print(f"    -> 提示词文本不存在")
            elif code == "access_denied":
                print(f"    -> 访问被拒绝")
            else:
                print(f"    -> 获取失败 (code: {code})")

        entry = {
            "id": pid,
            "title": title,
            "category": category,
            "type": ptype,
            "is_free": is_free,
            "page_type": ptype,
            "prompt_text": prompt_text,
            "description": generate_description(title, category, platform),
            "platform": platform,
        }

        # 更新或添加到结果列表
        if key in result_map:
            result_map[key] = entry
        else:
            results.append(entry)
            result_map[key] = entry

        # 每 20 条保存一次
        if i % 20 == 0:
            save_json(results, json_path)
            print(f"    [ checkpoint ] 已保存 {i}/{total}")

        time.sleep(REQUEST_DELAY)

    # Step 5: 保存最终结果
    print(f"\n{'=' * 60}")
    print(f"  爬取完成!")
    print(f"  总计: {len(results)} 个提示词")
    print(f"  成功获取文本: {success_count}")
    print(f"  跳过(已存在): {skip_count}")
    print(f"  无法获取(Premium/其他): {fail_count}")
    print(f"{'=' * 60}\n")

    print("正在保存最终结果...")
    save_json(results, json_path)
    save_markdown(results, OUTPUT_DIR / "motionsites_all_prompts.md")

    print(f"\n完成! 输出文件:")
    print(f"  - {json_path}")
    print(f"  - {OUTPUT_DIR / 'motionsites_all_prompts.md'}")


if __name__ == "__main__":
    main()
