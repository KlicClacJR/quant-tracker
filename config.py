"""Configuration for the quant opportunity tracker bot."""

MAX_ALERTS_PER_RUN = 10
FILTER_SCORE_THRESHOLD = 3
MONITORED_SITES = [
    {"firm": "Belvedere Trading", "source": "Careers", "url": "https://jobs.lever.co/belvederetrading?commitment=Intern"},
    {"firm": "Flow Traders", "source": "Careers", "url": "https://www.flowtraders.com/careers/job-search"},
    {"firm": "Five Rings", "source": "Careers", "url": "https://fiverings.com/careers/"},
    {"firm": "Chicago Trading Company", "source": "Careers", "url": "https://www.chicagotrading.com/search"},
    {"firm": "Jump Trading", "source": "Careers", "url": "https://www.jumptrading.com/hr/students-new-grads"},
    {"firm": "DRW", "source": "Careers", "url": "https://www.drw.com/work-at-drw/listings?filterType=category&value=Trading"},
    {"firm": "DRW", "source": "Careers", "url": "https://www.drw.com/work-at-drw/listings?filterType=category&value=Technology"},
    {"firm": "Old Mission", "source": "Careers", "url": "https://www.oldmissioncapital.com/careers"},
    {"firm": "Lazard Asset Management", "source": "Careers", "url": "https://lazard-careers.tal.net/vx/lang-en-GB/appcentre-ext/brand-4/candidate/jobboard/vacancy/2/adv/?"},
    {"firm": "Squarepoint", "source": "Careers", "url": "https://www.squarepoint-capital.com/open-opportunities?lvl=Early+Careers+Opportunity%2CInternship&dep=86658%2C86659"},
    {"firm": "Point72", "source": "Students", "url": "https://careers.point72.com/?experience=internships"},
    {"firm": "Blue Owl Capital", "source": "Careers", "url": "https://blueowl.wd1.myworkdayjobs.com/blueowl"},
    {"firm": "AQR", "source": "Careers", "url": "https://careers.aqr.com/jobs/city/greenwich?size=n_20_n"},
    {"firm": "Gelber Group", "source": "Careers", "url": "https://www.gelbergroup.com/careers/"},
    {"firm": "Tiger Global", "source": "Careers", "url": "https://www.tigerglobal.com/careers/"},
    {"firm": "Millennium", "source": "Careers", "url": "https://campusjobs.mlp.com/careers?pid=755953958409&domain=mlp.com&sort_by=relevance&triggerGoButton=true"},
    {"firm": "Quantbox Research", "source": "Careers", "url": "https://www.quantboxresearch.com"},
    {"firm": "Jefferies", "source": "Students", "url": "https://jefferies.tal.net/vx/lang-en-GB/mobile-0/appcentre-ext/brand-4/xf-152c05cf8968/candidate/jobboard/vacancy/2/adv/"},
    {"firm": "Aon", "source": "Careers", "url": "https://jobs.aon.com/jobs?keywords=%22%23AonInternUS%22&sortBy=relevance&page=1&_gl=1*hhg050*_gcl_au*MTI0NDc0MDMyMy4xNzc0OTI2MTk5*FPAU*MTI0NDc0MDMyMy4xNzc0OTI2MTk5*_ga*MTE4MzA5ODg4MC4xNzc0OTI2MTk5*_ga_S2CXP61BY4*czE3NzQ5MjYxOTkkbzEkZzEkdDE3NzQ5MjYyNTMkajYkbDAkaDMyMzc4NDA3OA..*_fplc*UVNCeXFtbUF2dGpuRm1YYTViTkE4V3FQTXl1YklpdmZFNktTc3RuU3pFOHpEJTJCSndkdnFCeUF3aGZFR2RLYUhFSjJzQndxOUpCU2tPZ1htQkRVVzl1WVNNJTJCNmdYV1QyZ0RxTFdLbyUyRmRoRURTYTRQM2NGMGlPWDglMkZaM3k1aGclM0QlM0Q."},
    {"firm": "Hudson River Trading", "source": "Careers", "url": "https://www.hudsonrivertrading.com/careers/"},
    {"firm": "Hudson River Trading", "source": "Careers", "url": "https://www.hudsonrivertrading.com/student-opportunities/"},
    {"firm": "WorldQuant", "source": "Careers", "url": "https://www.worldquant.com/career-listing/"},
    {"firm": "Virtu Financial", "source": "Careers", "url": "https://www.virtu.com/careers/"},
    {"firm": "XTX Markets", "source": "Careers", "url": "https://www.xtxmarkets.com/careers/"},
    {"firm": "Bridgewater", "source": "Careers", "url": "https://www.bridgewater.com/careers"},
    {"firm": "Bridgewater", "source": "Careers", "url": "https://job-boards.greenhouse.io/bridgewater89"},
    {"firm": "Akuna Capital", "source": "Students", "url": "https://akunacapital.com/careers/?experience=Internships"},
    {"firm": "Radix Trading", "source": "Careers", "url": "https://job-boards.greenhouse.io/radixuniversity"},
    {"firm": "D. E. Shaw", "source": "Careers", "url": "https://www.deshaw.com/careers/internships"},
    {"firm": "PIMCO", "source": "Early Careers", "url": "https://pimco.wd1.myworkdayjobs.com/pimco-careers?jobFamilies=b27adc21fb8410010c147bdeecc60000"},
    {"firm": "Jump Capital", "source": "Careers", "url": "https://jumpcap.com/careers/"},
    {"firm": "SIG", "source": "Early Careers", "url": "https://careers.sig.com/intern-co-op-jobs/"},
    {"firm": "IMC", "source": "Careers", "url": "https://www.imc.com/us/search-careers?jobQuery=intern&jobOffices=Chicago%2CNew+York&jobTypes=Intern&page=1"},
    {"firm": "Two Sigma", "source": "Internships", "url": "https://careers.twosigma.com/careers/OpenRoles/?5081=%5B16718737%5D&5081_format=3146&listFilterMode=1&jobRecordsPerPage=10&"},
    {"firm": "Two Sigma", "source": "Student Events", "url": "https://careers.twosigma.com/events/SearchEvents"},
    {"firm": "Jane Street", "source": "Internships", "url": "https://www.janestreet.com/join-jane-street/open-roles/?type=internship&location=all-locations"},
    {"firm": "Jane Street", "source": "Programs and Events", "url": "https://www.janestreet.com/join-jane-street/programs-and-events/?location=north-america&program-type=university&event-type=all-events&show-programs=true&show-events=true"},
    {"firm": "Citadel", "source": "Students", "url": "https://www.citadel.com/careers/open-opportunities?experience-filter=internships&location-filter=americas,chicago,greenwich,houston,miami,new-york,europe,dublin,london,paris,zurich&selected-job-sections=388,389,387,390&current_page=1&sort_order=DESC&per_page=10&action=careers_listing_filter"},
    {"firm": "Citadel Securities", "source": "Student Events", "url": "https://www.citadelsecurities.com/careers/programs-and-events/"},
    {"firm": "Blackstone", "source": "Students", "url": "https://blackstone.wd1.myworkdayjobs.com/en-US/Blackstone_Campus_Careers"},
    {"firm": "Morgan Stanley", "source": "Students", "url": "https://www.morganstanley.com/careers/career-opportunities-search?opportunity=sg#"},
    {"firm": "Goldman Sachs", "source": "Students", "url": "https://www.goldmansachs.com/careers/students/programs-and-internships?0=gscom%253Aprogram-type%252Finternship"},
    {"firm": "JPMorgan", "source": "Students", "url": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?keyword=intern&mode=location"},
    {"firm": "EY", "source": "Students", "url": "https://usearlycareers.ey.com/search-jobs"},
    {"firm": "Tower Research", "source": "Careers", "url": "https://tower-research.com/internships/#internship-opportunities"},
    {"firm": "Headlands Technologies", "source": "Careers", "url": "https://www.headlandstech.com/careers/"},
    {"firm": "Maven Securities", "source": "Careers", "url": "https://job-boards.greenhouse.io/mavensecuritiesholdingltd"},
    {"firm": "TransMarket Group", "source": "Careers", "url": "https://www.transmarketgroup.com/careers"},
    {"firm": "Wolverine Trading", "source": "Careers", "url": "https://www.wolve.com/open-positions"},
    {"firm": "Balyasny", "source": "Careers", "url": "https://bambusdev.my.site.com/s/"},
    {"firm": "ExodusPoint", "source": "Careers", "url": "https://www.exoduspoint.com/careers"},
    {"firm": "Schonfeld", "source": "Careers", "url": "https://www.schonfeld.com/careers/students-and-early-career/"},
]

INCLUDE_GROUP_A = [
    "quant",
    "quantitative",
    "trading",
    "trader",
    "research",
    "researcher",
    "strats",
    "systematic",
    "markets",
    "alpha",
    "portfolio",
    "machine learning",
    "data science",
]

INCLUDE_GROUP_B = [
    "intern",
    "internship",
    "summer analyst",
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
    "new grad",
]

EXCLUDE_TERMS = [
    "full-time",
    "experienced hire",
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

STUDENT_OVERRIDE_TERMS = [
    "first-year",
    "first year",
    "sophomore",
    "insight",
    "immersion",
    "discovery",
    "summit",
    "competition",
    "hackathon",
]

REQUEST_TIMEOUT_SECONDS = 20
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 QuantTrackerBot/1.0"
)

SEEN_FILE_PATH = "seen.json"
