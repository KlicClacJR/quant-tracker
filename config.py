"""Configuration for the quant opportunity tracker bot."""

MONITORED_SITES = [
    {"firm": "Belvedere Trading", "source": "Careers", "url": "https://www.belvederetrading.com/careers/"},
    {"firm": "Flow Traders", "source": "Careers", "url": "https://www.flowtraders.com/careers/"},
    {"firm": "Five Rings", "source": "Careers", "url": "https://fiverings.com/careers/"},
    {"firm": "Chicago Trading Company", "source": "Careers", "url": "https://www.chicagotrading.com/careers/"},
    {"firm": "Jump Trading", "source": "Careers", "url": "https://www.jumptrading.com/careers/"},
    {"firm": "DRW", "source": "Careers", "url": "https://www.drw.com/work-at-drw/listings/"},
    {"firm": "Old Mission", "source": "Careers", "url": "https://www.oldmissioncapital.com/careers"},
    {"firm": "Lazard Asset Management", "source": "Careers", "url": "https://www.lazard.com/careers/"},
    {"firm": "Squarepoint", "source": "Careers", "url": "https://www.squarepoint-capital.com/careers"},
    {"firm": "Point72", "source": "Students", "url": "https://careers.point72.com/students"},
    {"firm": "Blue Owl Capital", "source": "Careers", "url": "https://blueowl.com/careers"},
    {"firm": "AQR", "source": "Careers", "url": "https://www.aqr.com/About-Us/Careers"},
    {"firm": "Gelber Group", "source": "Careers", "url": "https://gelbergroup.com/careers/"},
    {"firm": "Tiger Global", "source": "Careers", "url": "https://www.tigerglobal.com/careers/"},
    {"firm": "Millennium", "source": "Careers", "url": "https://careers.mlp.com/"},
    {"firm": "Quantbox Research", "source": "Careers", "url": "https://www.quantboxresearch.com/careers"},
    {"firm": "Jefferies", "source": "Students", "url": "https://www.jefferies.com/careers/students-and-graduates/"},
    {"firm": "Aon", "source": "Careers", "url": "https://www.aon.com/careers"},
    {"firm": "Hudson River Trading", "source": "Careers", "url": "https://www.hudsonrivertrading.com/careers/"},
    {"firm": "WorldQuant", "source": "Careers", "url": "https://www.worldquant.com/careers/"},
    {"firm": "Virtu Financial", "source": "Careers", "url": "https://www.virtu.com/careers/"},
    {"firm": "XTX Markets", "source": "Careers", "url": "https://www.xtxmarkets.com/careers/"},
    {"firm": "Bridgewater", "source": "Careers", "url": "https://www.bridgewater.com/careers"},
    {"firm": "Akuna Capital", "source": "Students", "url": "https://akunacapital.com/careers/students/"},
    {"firm": "Radix Trading", "source": "Careers", "url": "https://radixtrading.com/careers/"},
    {"firm": "D. E. Shaw", "source": "Careers", "url": "https://www.deshaw.com/careers"},
    {"firm": "PIMCO", "source": "Early Careers", "url": "https://www.pimco.com/en-us/careers/students"},
    {"firm": "Jump Capital", "source": "Careers", "url": "https://jumpcap.com/careers/"},
    {"firm": "SIG", "source": "Early Careers", "url": "https://careers.sig.com/early-careers"},
    {"firm": "IMC", "source": "Careers", "url": "https://www.imc.com/us/careers/"},
    {"firm": "Two Sigma", "source": "Internships", "url": "https://www.twosigma.com/careers/internships/"},
    {"firm": "Two Sigma", "source": "Students", "url": "https://www.twosigma.com/undergraduate-students/"},
    {"firm": "Jane Street", "source": "Internships", "url": "https://www.janestreet.com/join-jane-street/internships/"},
    {"firm": "Jane Street", "source": "Programs and Events", "url": "https://www.janestreet.com/join-jane-street/programs-and-events/"},
    {"firm": "Citadel", "source": "Students", "url": "https://www.citadel.com/careers/students/"},
    {"firm": "Citadel Securities", "source": "Careers", "url": "https://www.citadelsecurities.com/careers/"},
    {"firm": "Blackstone", "source": "Students", "url": "https://www.blackstone.com/careers/students/"},
    {"firm": "Morgan Stanley", "source": "Students", "url": "https://www.morganstanley.com/people-opportunities/students-graduates"},
    {"firm": "Goldman Sachs", "source": "Students", "url": "https://www.goldmansachs.com/careers/students/"},
    {"firm": "JPMorgan", "source": "Students", "url": "https://careers.jpmorgan.com/us/en/students"},
    {"firm": "EY", "source": "Students", "url": "https://www.ey.com/en_us/careers/students"},
    {"firm": "Tower Research", "source": "Careers", "url": "https://tower-research.com/open-positions/"},
    {"firm": "Headlands Technologies", "source": "Careers", "url": "https://www.headlandstech.com/careers/"},
    {"firm": "Maven Securities", "source": "Careers", "url": "https://www.mavensecurities.com/careers/"},
    {"firm": "TransMarket Group", "source": "Careers", "url": "https://www.transmarketgroup.com/careers/"},
    {"firm": "Wolverine Trading", "source": "Careers", "url": "https://www.wolve.com/careers/"},
    {"firm": "Balyasny", "source": "Careers", "url": "https://www.bamfunds.com/careers"},
    {"firm": "ExodusPoint", "source": "Careers", "url": "https://www.exoduspoint.com/careers"},
    {"firm": "Schonfeld", "source": "Careers", "url": "https://www.schonfeld.com/careers/"},
]

# Strong quant/trading/research signal terms.
QUANT_SIGNAL_TERMS = [
    "quant",
    "quantitative",
    "trading",
    "trader",
    "research",
    "researcher",
    "strats",
    "systematic",
    "market making",
    "market-maker",
    "alpha",
    "portfolio",
    "machine learning",
    "data science",
    "statistical arbitrage",
]

# Student/early-career signal terms.
STUDENT_SIGNAL_TERMS = [
    "intern",
    "internship",
    "summer analyst",
    "summer internship",
    "program",
    "summit",
    "insight",
    "immersion",
    "discovery",
    "event",
    "undergraduate",
    "student",
    "campus",
    "early careers",
    "early career",
    "first-year",
    "first year",
    "sophomore",
    "new grad",
]

INTERNSHIP_SIGNAL_TERMS = [
    "intern",
    "internship",
    "summer analyst",
    "summer internship",
]

PROGRAM_EVENT_SIGNAL_TERMS = [
    "program",
    "summit",
    "insight",
    "immersion",
    "discovery",
    "event",
    "competition",
    "hackathon",
    "undergraduate",
    "campus",
]

# High-confidence target phrases for quant/trading student opportunities.
TARGET_ROLE_PHRASES = [
    "quantitative researcher intern",
    "quantitative trading intern",
    "quantitative trader intern",
    "quant trader intern",
    "trader intern",
    "trading intern",
    "quant analyst intern",
    "quant developer intern",
    "strats intern",
    "systematic trading intern",
    "research intern",
    "quant internship",
    "trading internship",
    "quantitative researcher internship",
    "quantitative trader internship",
]

TARGET_PROGRAM_EVENT_PHRASES = [
    "quant program",
    "trading program",
    "quantitative program",
    "trading summit",
    "quant summit",
    "trading insight",
    "quant insight",
    "trading immersion",
    "quant immersion",
    "trading discovery",
    "quant discovery",
    "undergraduate trading",
    "undergraduate quant",
]

EXCLUDE_TERMS = [
    "full-time",
    "experienced hire",
    "experienced professional",
    "senior",
    "manager",
    "director",
    "vice president",
    "tax",
    "audit",
    "hr",
    "human resources",
    "compliance",
    "legal",
    "marketing",
    "sales",
    "operations",
    "accounting",
]

# Exclude generic internship categories that are usually not quant/trading/research.
GENERIC_UNRELATED_TERMS = [
    "investment banking internship",
    "wealth management internship",
    "private wealth internship",
    "corporate finance internship",
    "corporate strategy internship",
    "risk internship",
    "internal audit internship",
    "human resources internship",
    "marketing internship",
    "operations internship",
    "compliance internship",
    "legal internship",
    "tax internship",
    "accounting internship",
]

GENERIC_TECH_TERMS = [
    "software engineer intern",
    "software engineering intern",
    "software developer intern",
    "frontend intern",
    "backend intern",
    "mobile intern",
    "web developer intern",
]

PROGRAM_TERMS = [
    "program",
    "summit",
    "insight",
    "immersion",
    "discovery",
    "undergraduate",
    "student",
    "campus",
    "event",
]

EVENT_TERMS = [
    "event",
    "summit",
    "hackathon",
    "competition",
    "insight",
    "immersion",
    "discovery",
]

KNOWN_STUDENT_PAGE_TERMS = [
    "students",
    "student",
    "undergraduate",
    "internship",
    "internships",
    "early careers",
    "early-careers",
    "programs-and-events",
    "programs",
]

REQUEST_TIMEOUT_SECONDS = 20
SEEN_FILE_PATH = "seen.json"
MAX_ALERTS_PER_RUN = 15
FILTER_SCORE_THRESHOLD = 6
SNIPPET_MAX_CHARS = 160

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 QuantTrackerBot/1.0"
)
