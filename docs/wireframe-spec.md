# Website wireframes v2 — extracted spec

Source: `~/Downloads/WEBSITE WIREFRAMES-2/` (29 annotated pages, extracted 14 Sep 2026).
Numbers below are the wireframe page numbers. "Delta" = what differs from the site today.

> **Warning on facts:** the wireframes' specific claims (member counts, head engineer
> names, project numbers, debut years, crew lists) are placeholder bluff, not confirmed
> facts. The site deliberately keeps this copy vague: it describes what each division
> does without unverified numbers or names. Do not copy wireframe specifics onto the
> site without the committee confirming them.

## Public site

**1. Home** — matches the built page (video hero, opacity-on-scroll statements, domain
cards, recent events scroller, "Interested in joining?" CTA). Copy in the wireframe:
"unites 80 interdisciplinary students" and "Founded in 2019". NOTE: "2019" contradicts
the history page (society created Dec 2023) and the current site (est. 2023) — needs a
decision before changing copy.

**2. Site navigation overlay** — as built, except the Divisions section gains a fourth
entry: OPERATIONS. Join Us cards: Joining the Team / Create Account / Log In
(+ My Application exists today).

**3. Land division** — new copy: "60 active students… hydrogen powered endurance
vehicle", focus line "sustainable mobility and energy efficiency". "Our Entry" card
HFR SEM 2027: hover floods the page with the gradient; click goes to the HEV project
page (7). Shell Eco Marathon section: location Poland, learn-more links to the official
site.

**4. Sea division** — copy: "XX active students… zero emission race crafts" (member
count TBD), focus "sustainable solutions and performance racing". Entry card FLAGSHIP
links to the boat project page (8). Competitions: Monaco Energy Boat Challenge (Monaco)
and Lake Como Energy Boat Challenge (Italy), with Yacht Club de Monaco branding.

**5. Air division** — copy: "21 active students that collaborate with UGA", focus
"innovation and collaboration". "Our 2026 Concept" card links to the aero concept page
(9, already built). New UGA section: University of Glasgow Aeronautics society
cross-collaboration + link out.

**6. Operations division (NEW page)** — hero like other divisions. Copy: "backbone of
HFR… essential maintenance, organisation and creative direction". Three sections with
jump buttons: Business (events, lectures, worksite trips, university/SRC and sponsor
comms), Finance & Contracts (books and balances, strategic funding), Creative Direction
(promo videos, posters, identity; "Check out our socials!" → Instagram).
NOTE: the application form wireframe (21) instead lists the third ops subteam as
"Social Media" — naming needs one decision.

**7. HEV project page (NEW)** — 2026 HYDROGEN ENDURANCE VEHICLE. Facts row: Project
No. 1, Head Engineer Chloe Steel, Powertrain "Gaseous Hydrogen electric", Year 2024/27.
Copy: core project since Dec 2023, single-tank distance goal, debuts at 2027 Shell Eco
Marathon in Poland. Five team tabs, each with a blurb: Chassis, Aerodynamics,
Electrical, Vehicle Dynamics, Data & Telemetry, plus Hydrogen Fuel Cell (six boxes are
drawn; copy exists for all six). Includes car render image (in wireframe).

**8. Energy Class Boat project page (NEW)** — 2026 ENERGY CLASS BOAT, orange→teal
gradient page. Deliberately vague copy ("cannot reveal too much"): future of maritime
is electric propulsion; pushing market limits. Scroll-expanding hero image.

**9. Aero concept page** — already built. Facts per wireframe: Project 3, Head
Engineer Arman, Powertrain "???", Year 2026 (current "TBD" is consistent).

**10. Partners page** — partner grid (8 slots, 5 named): Schwer Fittings, Hydrogen
Scotland, Shaffimed, Glasgow Centre for Sustainability & Energy, Dassault Systems.
The sponsor ranking table (platinum/gold/silver/bronze) is crossed out — do NOT build.

**11. Support Us page (NEW)** — "Drive the Change / SUPPORT US" + donation pitch
(100+ students). A "Support Us <3" button reveals a form: full name, email, donation
amount, message to the team, "Continue to payment". Side cards with donation blurbs.
Payment processing method is not specified — needs a decision (external link vs real
processor).

**12. Our Mission page** — mission statement + HFR CONSTITUTION (6 numbered points,
key phrases highlighted) signed "Muhemmed Bin Naseeb, Founder" + closing belief line.

**13. History page** — alternating timeline: UGEV ESTABLISHED (Dec 2023) → VERSION 1
(SEM vehicle dev) → H.F.R FORMED (Sep 2024) → H.S.N (assisting Hydrogen Scotland
Network at 12th MEBC 2025) → EXPANSION (Air and Sea divisions) → COMPETITION (first
official entry, 13th Monaco EBC 2026) → CONSTRUCTION (SEM build begins).

**14. Events page** — grid of 6 image cards; each links to an event article page.

**15. Sea Team 2026 page (NEW)** — full-bleed team photo "TEAM 2026", Monaco debut
copy, 11 engineers (3 first years, 6 second years, 2 third years), crew list:
Muntazin Ahammad (Team Principal), Ethan Thomson (Head Engineer), Firm Kongso (Thermal
Management Lead), Sethikha Kodithuwakku (Powertrain Lead), Martha Hennessy and Iona
Patrick (Aerodynamics Leads), Diego Flores (CAD & Design Lead), Krystian Pelchner
(Chief Mechanic), Matthew Bishop (Testing & Documentation), Tytus Dmytryszyn (Creative
Lead), Kareem Bannaga (Videography).

**16. Event article template (NEW)** — hero image with title band, then title, body
text (author-supplied), side image.

**17. Joining the Team page** — full redesign with real photos (now extracted, see
below). Q&A flow: opportunities (three divisions + sub teams), what the team is like
(100+ engineers, socials/competitions/trips), volunteering (STEM ambassadors),
career benefits, why join, how to join (create applicant account → application + CV)
→ CREATE ACCOUNT button.

## Auth + recruitment

**18. Account creation / 19. Log in** — as built (GUID email requirement, gradient
hover, invalid-data messages, success message).

**20. Applicant dashboard** — as built (empty state → APPLY NOW; stacked status bars:
submitted date / first choice interview / decision pending / accepted+rejected; JOIN
HFR reveals code entry; congratulations + enter code → logged out promotion flow).

**21. Application form** — deltas from the built form:
- Year picker is 5 gradient-fill buttons (1–5); current form likely equivalent.
- Team choice: pick 3 to a "Draft Board" (First Pick / Alternative / WildCard) by
  selecting a division then a sub team. Sub teams shown:
  LAND: Aerodynamics, Electrical, Dynamics, Data & Telemetry, Chassis, HFC.
  SEA: Aerodynamics, Electrical, Dynamics, Chassis (page 26 version: Hull & Body,
  Dynamics, Propulsion, Powertrain, Embedded — CONTRADICTION, needs decision).
  AIR: Aerodynamics, Electrical, Dynamics, Chassis (page 26: Aerodynamics, Chassis,
  Embedded, HFC — CONTRADICTION).
  OPERATIONS: Business, Finance & Contracts, Social Media (page 6: Creative
  Direction — CONTRADICTION).
- Questions are now THREE: "What is your reason for your first pick?", "What is your
  reason for your alternative pick?", "Describe the time you completed a difficult
  task" (current form has four different questions; DB migration needed).
- Closing blurb + SUBMIT APPLICATION.

## Member area (all NEW features)

**23/24. Member dashboard + Events** — "Welcome NOOR" (random tagline, e.g. "Goated
member of the LAND division"). Upcoming events list: colored capacity bars
(e.g. "Boat Testing Event 4/12"), click for details, first-come-first-serve
self-registration. Create Event form (leads/high clearance only): title, date, short
description, capacity, optional division lock, display color (4 choices), Create.

**26. Team structure + Objectives** — division/sub-team browser, then a team
objectives table (Objective # / Description / Status, e.g. "Waiting on electrical
team", "On Going", "Not Begun", "Completed" in green). REVIEW CHECKLIST enters a
review mode (green frame): Delete Objective / Add Objective / Finish Review.
Lead-only editing.

**27. Tasks** — each member sees "MY TASKS": colored task bars with title, MARK AS
COMPLETED, expandable step list and due date. Leads see a set-task form: title, due
date, assign to (multiple people), steps (numbered/bullets), color, SET TASK.
Note: tracked as a performance metric but must feel friendly, not surveillance.

**28. Resource Vault** — placeholder page: title + "Learn" button (content TBD).

**29. Member store** — members-only store: product grid, basket with count badge,
checkout so people "can complete orders on the site"; implementation freedom
explicitly given, correct colors required. Payment method unspecified — decision
needed (real payments vs order-request without payment).

**22/25. Account overlay + Edit profile** — as built. Edit profile wireframe shows
7 preset circles + upload; current has 4 presets + upload.

## Photos extracted from the wireframes

Saved to `core/static/core/photos/` at wireframe resolution (1366px wide max):
- `monaco-podium.jpg` — team with Saltire at 13° Monaco Energy Boat Challenge wall
- `night-workshop.jpg` — two members testing at night
- `rules-briefing.jpg` — classroom rules-requirements talk
- `boat-crane.jpg` — boat craned into Monaco harbour
- `vital-spark-pit.jpg` — Vital Spark pit work at Monaco
- `monaco-flags.jpg` — crew with Saltire + Union Jack on deck
- `team-pizza.jpg` — team social, pizza restaurant
- `lecture-hall.jpg` — full society photo in lecture theatre
- `team-2026-main.jpg` — Team 2026 in front of the university (cropped from page 15;
  has design overlays trimmed, original photo would be better if available)

## Decisions needed before building

1. Founding year: 2019 (home wireframe) vs Dec 2023 (history + current site).
2. Ops third subteam: "Creative Direction" (page 6) vs "Social Media" (pages 21/26).
3. Sea/Air sub team lists: application form (21) vs team structure page (26).
4. Application questions: switching to the three new questions drops the current four
   (existing applications keep old answers; form + review UI need migrating).
5. Sea division member count ("XX" in wireframe).
6. Payments for Support Us donations and the member store.
