#!/usr/bin/env python3
"""Content for the role pages — one per practice, eight in total.

WHY THIS FILE EXISTS
--------------------
The site used to target a city ("executive search firm Houston"). Going nationwide
removes that modifier, and a page with no modifier corners nothing. So the modifier
moves axis: from *where* to *what role*. "Community association manager recruiters"
is exactly as narrow as "executive search firm Houston" and carries no geography.

These pages are the unit that ranks. The practice pages stay the pillar; each role
page is a spoke that links up to its practice and down into the calculator.

Structure matches industries.py deliberately — same fields, same voice, same
British spelling, &mdash; for em dashes, &#8209; for non-breaking hyphens. Salary
bands are the same figures already published on jobs.html; do not invent new ones.

EVERY LIST IS DERIVED FROM THIS FILE. The nav, the footer, the hub, sitemap.xml,
llms.txt and the test roster all read ROLES. README documents three separate
occasions where a hardcoded practice list drifted and failed silently. Do not type
a fourth copy of anything here.
"""

ROLES = [
{
 "slug": "community-association-manager-recruiters",
 "practice": "hoa-property-management",
 "nav": "Community Association Manager",
 "title": "Community Association Manager Recruiters | Nationwide | Sublime Personnel",
 "desc": "Nationwide recruiters for community association managers &mdash; CMCA, AMS and PCAM holders screened on governance, portfolio complexity and board temperament, not r&eacute;sum&eacute; keywords.",
 "h1_main": "Community Association Manager",
 "h1_fill": "Recruiters",
 "salary": (72, 115),
 "lede": "Boards do not remove managers over spreadsheets. They remove them over meetings, minutes and tone &mdash; which is why a community association manager search that screens on portfolio size alone keeps producing hires who leave in month nine.",
 "does_head": "What the role actually owns.",
 "does": [
   "Running board and annual meetings, holding a quorum together, and documenting decisions in a way that survives a challenge.",
   "Budget preparation, reserve study conversations, and defending an assessment increase to owners who do not want to hear it.",
   "Vendor selection and management, bid walks, and the capital projects the board has been deferring.",
   "Covenant enforcement &mdash; the part of the job that generates every difficult conversation the manager will have this year.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Governance literacy", "Can they read the governing documents, run an annual meeting and hold a quorum? We ask for specifics from actual meetings, not from the job description."),
   ("Portfolio math", "Doors, associations and complexity are three different measures. Twelve small associations and two high&#8209;rises are not the same workload."),
   ("Credentials and trajectory", "CMCA, AMS and PCAM matter to boards. We establish where a candidate sits on that ladder and whether their employer supported the progression."),
   ("Board temperament", "The strongest single predictor of a manager reaching year two. We reference it directly with people who have watched them in a room."),
 ],
 "faq": [
   ("What does a community association manager earn?",
    "The range we are currently seeing nationally runs roughly $72,000 to $115,000 depending on portfolio complexity, credentials and market. A portfolio manager carrying high&#8209;rise or mixed&#8209;use property sits at the top of that band; a single&#8209;association on&#8209;site manager in a smaller market sits below it."),
   ("Do you only place CMCA or PCAM holders?",
    "No. We recruit credentialed managers and strong managers working toward those designations, and we confirm credential status before presenting anyone. Some of the best hires we have made were two courses away from an AMS and were supported through it."),
   ("Can you support a management company entering a new market?",
    "Yes, and it is where we do some of our best work &mdash; market entry needs a portfolio manager and a bench at the same time. Our HOA practice already spans ten states for one client. Give us the timeline and we build the search around it."),
 ],
},
{
 "slug": "restaurant-general-manager-recruiters",
 "practice": "hospitality-restaurant",
 "nav": "Multi&#8209;Unit Restaurant GM",
 "title": "Restaurant General Manager Recruiters | Multi&#8209;Unit | Sublime Personnel",
 "desc": "Restaurant GM and multi-unit recruiters who ran the floor first. We screen on unit economics, span of control and retention &mdash; not on a r&eacute;sum&eacute; that reads like a general manager.",
 "h1_main": "Restaurant General Manager",
 "h1_fill": "Recruiters",
 "salary": (95, 160),
 "lede": "There is a difference between a r&eacute;sum&eacute; that reads like a general manager and a person who can hold a building together on a Saturday night. Thirty years of restaurant operations sit behind every search we run for this role.",
 "does_head": "What the role actually owns.",
 "does": [
   "The P&amp;L &mdash; food cost, labour, COGS, flow&#8209;through &mdash; and the ability to explain in seconds how they moved each one.",
   "Building and holding a management bench, which is the difference between a GM who scales and a GM who is permanently indispensable.",
   "Guest recovery and the culture that decides whether the team stays past ninety days.",
   "For multi&#8209;unit: coaching operators they do not stand next to, and diagnosing a failing store from the numbers before the visit.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Unit economics, not anecdotes", "We ask for the numbers they owned and how they moved them. Operators who genuinely ran the P&amp;L answer immediately."),
   ("Span of control", "A five&#8209;unit district and a twenty&#8209;unit district are different jobs. We map what a candidate actually supervised, and whether they built the bench beneath them."),
   ("Turnover and retention", "Anyone can open a store. We look at whether their teams stayed, and what they did in the first ninety days when they inherited a broken one."),
   ("Hours and expectations", "Hospitality burns people who did not know what they were signing up for. We are direct about schedule and travel before the first interview."),
 ],
 "faq": [
   ("What does a restaurant general manager earn?",
    "Single&#8209;unit GMs in full service currently run roughly $95,000 to $120,000. Multi&#8209;unit and director of operations roles run $130,000 to $160,000 plus bonus, depending on unit count and average unit volume."),
   ("Can you fill hourly or line&#8209;level roles?",
    "Our work is management and above. For hourly volume hiring a staffing agency will serve you better, and we will tell you so rather than take the engagement."),
 ],
},
{
 "slug": "commercial-lines-producer-recruiters",
 "practice": "insurance",
 "nav": "Commercial Lines Producer",
 "title": "Commercial Lines Producer Recruiters | Insurance | Sublime Personnel",
 "desc": "Insurance producer recruiters who separate a portable book from a story about one. Renewal retention, carrier appointments, class concentration and restrictive covenants raised before you spend a quarter.",
 "h1_main": "Commercial Lines Producer",
 "h1_fill": "Recruiters",
 "salary": (90, 140),
 "lede": "Every producer says the book is portable. The question is whether it lawfully is &mdash; and agencies that hire on charm alone spend the following year finding out that it was not.",
 "does_head": "What the role actually owns.",
 "does": [
   "New business production against a written goal, and the pipeline discipline behind it.",
   "A renewal book, its retention rate, and the service relationships that hold it together.",
   "Carrier relationships and appointments &mdash; which markets they can actually access, not which ones they have heard of.",
   "Risk assessment and the technical floor: knowing which classes they can write competently and which they should decline.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("The book, verified", "Renewal retention, class concentration, and premium volume by line. A producer with a genuine book answers in numbers."),
   ("Restrictive covenants", "Non&#8209;solicits, non&#8209;competes and garden leave, raised in the first conversation so nobody spends a quarter on a hire who cannot bring anything with them."),
   ("Carrier appointments", "Which markets travel with them and which belong to the agency they are leaving. These are rarely the same."),
   ("New business versus inherited", "Whether they built the book or were handed it. Both can be the right hire &mdash; but not for the same seat."),
 ],
 "faq": [
   ("What does a commercial lines producer earn?",
    "Base currently runs roughly $90,000 to $140,000 with uncapped commission on top; total compensation depends almost entirely on the book. Account manager roles supporting them run $68,000 to $85,000."),
   ("Do you recruit personal lines as well?",
    "Yes. The technical screen differs &mdash; in personal lines the equivalent of production discipline is retention behaviour, how somebody handles a rate increase call and whether they re&#8209;market before the policyholder asks."),
 ],
},
{
 "slug": "nurse-practitioner-recruiters",
 "practice": "healthcare",
 "nav": "Nurse Practitioner",
 "title": "Nurse Practitioner Recruiters | NP &amp; PA Search | Sublime Personnel",
 "desc": "Nurse practitioner and physician assistant recruiters screening on prescribing authority state by state, supervision arrangements and licensure &mdash; not on the r&eacute;sum&eacute;.",
 "h1_main": "Nurse Practitioner",
 "h1_fill": "Recruiters",
 "salary": (110, 145),
 "lede": "In healthcare the wrong hire is not an inconvenience, it is a licensing problem. Which is why the screen for an NP or PA turns on scope of practice in that specific state, and only then on everything else.",
 "does_head": "What the role actually owns.",
 "does": [
   "Patient assessment, diagnosis and &mdash; where the state permits it &mdash; prescribing, which is frequently the whole reason the seat exists.",
   "Working within whatever supervision or collaborative practice arrangement that state requires, which varies enormously across the country.",
   "Documentation and coding accuracy, because it drives both compliance and the revenue cycle.",
   "Patient volume and throughput in a clinic model where the schedule is the business.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Licensure and prescribing authority", "Which licences permit which services, in which state, under which supervision arrangement. This is the screen, and it is state&#8209;by&#8209;state work."),
   ("Setting and scale", "A high&#8209;volume retail clinic model and a specialty practice are different jobs. We establish which one a candidate has actually run."),
   ("Credentialing timeline", "How long they take to credential with your payers, because it determines when the seat starts producing."),
   ("Standing with clinical staff", "Whether the nursing and front&#8209;office teams around them will stay. Clinical turnover follows leadership more closely than it follows pay."),
 ],
 "faq": [
   ("What does a nurse practitioner earn?",
    "The range we are currently seeing runs roughly $110,000 to $145,000 depending on specialty, state and setting. Director of nursing and multi&#8209;site clinical leadership runs $115,000 to $140,000."),
   ("Do you recruit across state lines?",
    "Yes &mdash; we recruit nationwide, and for multi&#8209;site clinical groups that is the point. Prescribing authority and supervision rules differ by state, so we run the licensure screen per location rather than once."),
 ],
},
{
 "slug": "controller-recruiters",
 "practice": "accounting-finance",
 "nav": "Controller",
 "title": "Controller Recruiters | Accounting &amp; Finance | Sublime Personnel",
 "desc": "Controller and assistant controller recruiters who screen on close ownership, industry accounting and systems &mdash; because a technically sound accountant in the wrong industry leaves in month nine.",
 "h1_main": "Controller",
 "h1_fill": "Recruiters",
 "salary": (110, 150),
 "lede": "Association accounting is not restaurant accounting. Percentage&#8209;of&#8209;completion for a commercial contractor is not agency trust accounting. Hiring a controller on credentials alone is how you discover that in month nine.",
 "does_head": "What the role actually owns.",
 "does": [
   "The month&#8209;end close &mdash; how many days, how many entities, and what they inherited when they arrived.",
   "Audit liaison, and the working papers that decide whether the audit is a week or a quarter.",
   "Cash forecasting and the covenant compliance that comes with a lender.",
   "A team &mdash; usually small, frequently inherited, and often the reason the previous controller left.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Close ownership", "Do they own the close or support it? Days to close, entity count, and what state the books were in when they arrived."),
   ("Industry accounting", "Percentage&#8209;of&#8209;completion, association reserves, trust accounting, multi&#8209;unit consolidations &mdash; whichever applies to you."),
   ("Systems", "QuickBooks, Sage Intacct, NetSuite, Yardi, Vantaca, restaurant back&#8209;office platforms. Ramp time is largely a systems question."),
   ("Business partnership", "Whether they can sit in front of an owner or a board and explain the number, or whether they can only produce it."),
 ],
 "faq": [
   ("What does a controller earn?",
    "Currently roughly $110,000 to $150,000 depending on revenue size, entity complexity and whether the role carries a team. Assistant controller sits below that; a CFO or fractional CFO engagement sits above it."),
   ("Do candidates need to be CPAs?",
    "Not always, and we will say so plainly when a strong candidate is not one and it does not matter for the role. Where CPA status is claimed we verify licence standing before presentation."),
 ],
},
{
 "slug": "construction-superintendent-recruiters",
 "practice": "commercial-construction",
 "nav": "Superintendent",
 "title": "Construction Superintendent Recruiters | Commercial | Sublime Personnel",
 "desc": "Commercial construction superintendent recruiters screening on project profile, delivery method and dollar value &mdash; because a $12M tilt-wall super and a $90M healthcare super are not interchangeable.",
 "h1_main": "Construction Superintendent",
 "h1_fill": "Recruiters",
 "salary": (110, 145),
 "lede": "Construction hiring is judged in the field, not in the interview. A superintendent can tell within a minute whether the recruiter on the other end has ever stood on a jobsite &mdash; which is most of why these searches fail before they start.",
 "does_head": "What the role actually owns.",
 "does": [
   "The schedule, and the daily decisions that either protect it or quietly lose a week at a time.",
   "Subcontractor coordination and the quality of the work that goes in behind them.",
   "Site safety, which is the one area where a bad hire is not a cost problem but a liability problem.",
   "Owner and architect relationships in the field, where most of the change orders are really negotiated.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Project profile", "Sector, square footage, dollar value and delivery method &mdash; CM at risk, design&#8209;build, hard bid. The r&eacute;sum&eacute; rarely says. We always ask."),
   ("Self&#8209;perform or subcontract", "Whether they managed their own crews or coordinated subs changes what they can do on day one."),
   ("Software", "Procore, Bluebeam, Sage 300 CRE, On&#8209;Screen Takeoff. A field leader who cannot use your stack costs you a quarter."),
   ("Travel and geography", "Construction candidates will move for the right project. We settle relocation and per&#8209;diem expectations before the first interview, not after the offer."),
 ],
 "faq": [
   ("What does a construction superintendent earn?",
    "Currently roughly $110,000 to $145,000 for commercial work, usually with a truck and fuel allowance. Project executives carrying two to three concurrent projects run $160,000 to $200,000."),
   ("Do you recruit for specialty trades and industrial work?",
    "Yes &mdash; mechanical, electrical, roofing and industrial contractors, plus energy&#8209;adjacent technical roles through our Gulf Coast network."),
 ],
},
{
 "slug": "franchise-business-consultant-recruiters",
 "practice": "qsr-franchise",
 "nav": "Franchise Business Consultant",
 "title": "Franchise Business Consultant Recruiters | FBC &amp; Area Coach | Sublime Personnel",
 "desc": "Franchise business consultant and area coach recruiters for both sides of the relationship &mdash; franchisors staffing field support and multi-unit franchisees building an operations bench.",
 "h1_main": "Franchise Business Consultant",
 "h1_fill": "Recruiters",
 "salary": (78, 110),
 "lede": "Running units you own and coaching units somebody else owns require two different personalities. Hiring the wrong one produces a year of quiet friction and a field team nobody listens to.",
 "does_head": "What the role actually owns.",
 "does": [
   "Influence without authority &mdash; moving an owner who does not employ them. This is the rare skill and the whole job.",
   "Brand standards, audits, and the conversation with a franchisee who does not want to hear the result.",
   "P&amp;L coaching across a portfolio of owners with wildly different capability and appetite.",
   "New store openings and remodel cycles, worked backwards from the build schedule.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Franchisee or franchisor", "Which side they have operated on, and whether they can influence an owner they do not employ."),
   ("Units and AUV", "Units supervised, average unit volume, and whether growth came from new builds or from repairing existing stores."),
   ("Speed and scale", "New&#8209;store opening experience, remodel cycles, and how many openings they have personally led."),
   ("Brand standards", "How they handle an audit, a failing store, and an owner who does not want to hear it."),
 ],
 "faq": [
   ("What does a franchise business consultant earn?",
    "Currently roughly $78,000 to $110,000 with a vehicle allowance and bonus, depending on brand, unit count and territory size. Area coach roles at a franchisee sit at the lower end; franchisor field consultant roles at the upper end."),
   ("Do you work with franchisees or franchisors?",
    "Both. A multi&#8209;unit franchisee building a district manager bench and a franchisor staffing field consultants are different searches, and we run them differently."),
 ],
},
{
 "slug": "drilling-engineer-recruiters",
 "practice": "oil-gas",
 "nav": "Drilling &amp; Completions Engineer",
 "title": "Drilling Engineer Recruiters | Completions &amp; Upstream | Sublime Personnel",
 "desc": "Drilling and completions engineer recruiters who screen on the cycle &mdash; what a candidate did in 2015 and 2020 tells you more about the next five years than anything on the r&eacute;sum&eacute;.",
 "h1_main": "Drilling &amp; Completions Engineer",
 "h1_fill": "Recruiters",
 "salary": (145, 185),
 "lede": "An engineer whose whole career ran through one boom has never had to cut, re&#8209;bid or hold a programme together on a flat year. In energy, that is the screen &mdash; not the basin on the r&eacute;sum&eacute;.",
 "does_head": "What the role actually owns.",
 "does": [
   "Well planning through execution, and the AFE discipline that decides whether the programme lands on budget.",
   "Vendor and service company management, where most of the recoverable cost sits.",
   "Field presence &mdash; how much, and whether the candidate genuinely wants it.",
   "Completions design and the offset analysis behind it, in an unconventional programme.",
 ],
 "screen_head": "How we screen for it.",
 "screen": [
   ("Segment and asset", "Upstream, midstream or downstream &mdash; and which basin, which formation, which plant. Permian unconventional and deepwater Gulf are different jobs with the same job title."),
   ("Cycle behaviour", "What they did in 2015 and in 2020. How a candidate behaved in a downturn predicts the next five years better than the r&eacute;sum&eacute; does."),
   ("Operator or service side", "Whether they have sat on the operator's side of the table or the vendor's. It changes how they manage cost."),
   ("Budget dependence", "Whether somebody who thrived at a supermajor can operate without that budget behind them."),
 ],
 "faq": [
   ("What does a drilling engineer earn?",
    "Currently roughly $145,000 to $185,000 depending on basin, operator size and rotation. Production superintendents, turnaround managers and project controls leads sit in adjacent bands."),
   ("Do you recruit outside the Gulf Coast?",
    "Yes, nationwide. Our deepest technical network is on the Gulf Coast &mdash; including the hard&#8209;to&#8209;fill subsea and ROV roles where the candidate pool is a set of relationships rather than a job board &mdash; but the drilling and completions work follows the basins."),
 ],
},
]

SLUGS = [r["slug"] for r in ROLES]
ROLE_BY_PRACTICE = {r["practice"]: r for r in ROLES}
