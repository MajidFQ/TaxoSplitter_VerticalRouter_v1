DOMAINS = {

    "V1_Healthcare": """
        RULE: The business's PRIMARY purpose is diagnosing, treating, or caring for
        human physical or mental health. The customer is a patient.

        INCLUDES: Medical doctors, specialists, dentists, orthodontists, chiropractors,
        optometrists, ophthalmologists, physical therapists, occupational therapists,
        speech therapists, psychotherapists, counselors, psychiatrists, nutritionists,
        audiologists, midwives, doulas, acupuncturists, massage therapists (clinical),
        holistic and alternative medicine practitioners. Hospitals, urgent care centers,
        emergency rooms, surgical centers, medical groups, medical offices, clinics,
        medical laboratories, diagnostic imaging centers, MRI centers, pregnancy care
        centers, fertility clinics, IV therapy, dialysis centers, addiction treatment
        centers, rehabilitation centers, home health care services, nursing homes,
        hospices, assisted living facilities, adult day care centers.

        DOES NOT INCLUDE: Gyms, yoga studios, spas, tanning salons (those are
        V7_Hospitality). Pharmacies and medical supply stores (those are V8_Retail).
        Life coaches, personal trainers unless medically supervised (V9_Professional
        or V7_Hospitality). Veterinarians (use V6_Facilities or V9_Professional).
    """,

    "V2_Automotive": """
        RULE: The business sells, services, repairs, or rents motor vehicles or
        directly vehicle-specific parts and accessories. The product or service
        is a vehicle or a component designed for a vehicle.

        INCLUDES: Car dealerships (new and used), motorcycle dealers, ATV dealers,
        RV dealers, truck dealers, trailer dealers, golf cart dealers, electric
        vehicle dealers, boat dealers, personal watercraft dealers, snowmobile dealers.
        Auto repair shops, auto body shops, brake shops, muffler shops, transmission
        shops, oil change services, wheel alignment, auto glass, dent removal, car
        detailing, car wash, tire shops. Auto parts stores, car battery stores,
        car accessories stores, motorcycle parts stores. Vehicle inspection, smog
        inspection, auto auctions, towing services.

        DOES NOT INCLUDE: Gas stations (V8_Retail). Driving schools (V10_Education).
        Parking lots and garages (V4_RealEstate). Boat tours or RV parks (V7_Hospitality).
        Ship manufacturers or aircraft manufacturers (V5_Industrial).
    """,

    "V3_Construction": """
        RULE: The business physically builds, installs, renovates, or repairs
        structures and built environments on-site. The worker goes to the site
        and changes something physical about a building or property.

        INCLUDES: General contractors, home builders, remodelers, roofing contractors,
        HVAC contractors, electrical contractors (installation), plumbing contractors,
        concrete contractors, demolition contractors, masonry contractors, insulation
        contractors, flooring contractors, drywall contractors, siding contractors,
        tile contractors, paving contractors, fence contractors, swimming pool
        contractors, deck builders, garage builders, shed builders, dock builders,
        modular home builders, foundation contractors, excavation contractors,
        scaffolding services. Electricians, plumbers, carpenters, welders (on-site),
        glaziers, plasterers, handypersons. Civil engineering, road construction.

        DOES NOT INCLUDE: Architects and interior designers who do not build
        (V9_Professional). Manufacturers of building materials (V5_Industrial).
        Landscapers and lawn care (V6_Facilities). Property maintenance cleaning
        (V6_Facilities). Metal fabrication shops not doing on-site work (V5_Industrial).
    """,

    "V4_RealEstate": """
        RULE: The business's revenue comes from property transactions, property
        management, or financial instruments backed by real property.

        INCLUDES: Real estate agencies, real estate agents and brokers, real estate
        developers, commercial real estate firms, industrial real estate firms,
        property management companies, property investment firms, real estate
        appraisers, home inspectors, mortgage lenders, mortgage brokers, loan
        agencies, real estate attorneys, foreclosure services, escrow services,
        title companies, land surveyors. Apartment complexes, housing developments,
        condominiums, student housing communities, housing cooperatives, furnished
        apartments, homeowners associations, housing authorities. Self-storage
        facilities, cold storage operators, records storage facilities, parking
        garages and lots (as commercial real estate assets).

        DOES NOT INCLUDE: Construction companies that build properties (V3_Construction).
        Moving and storage services (V5_Industrial for logistics). Short-term vacation
        rentals operated as hospitality (V7_Hospitality). Banks and financial
        institutions not focused on mortgages (V9_Professional).
    """,

    "V5_Industrial": """
        RULE: The business manufactures physical goods at scale, distributes raw
        materials or finished goods B2B, or operates energy/logistics infrastructure.
        The primary customer is another business, not an end consumer.

        INCLUDES: Manufacturers of all types — automotive parts, electronics,
        furniture, food, industrial machinery, chemicals, glass, metals, tools,
        batteries, plastics, textiles, clothing, shoes, paper. Industrial suppliers
        and B2B wholesalers: metal suppliers, pipe suppliers, electrical equipment
        suppliers, hydraulic suppliers, building material suppliers, energy suppliers,
        industrial gas suppliers, chemical wholesalers. Energy infrastructure: oil
        and gas companies, petroleum companies, power plants, electric utilities,
        solar energy companies, wind farms, refineries, nuclear power plants.
        Logistics: freight forwarders, shipping companies, trucking companies,
        import/export firms, warehouses, distribution centers. Food processing,
        breweries, distilleries, packaging companies, print shops (commercial).
        Farms producing agricultural goods as a business (not agritourism).

        DOES NOT INCLUDE: Retail stores selling manufactured goods to consumers
        (V8_Retail). Contractors who install or build on-site (V3_Construction).
        Software companies (V9_Professional). Restaurants and food service (V7_Hospitality).
    """,

    "V6_Facilities": """
        RULE: The business provides ongoing or project-based physical maintenance,
        cleaning, security, or restoration services to properties. They come to
        the property and maintain it — they do not build or renovate it.

        INCLUDES: Commercial cleaning, janitorial services, carpet cleaning, window
        cleaning, pressure washing, air duct cleaning, dryer vent cleaning, house
        cleaning. Landscaping, lawn care, lawn mowing, arborist services, tree
        services, tree trimming, pest control, irrigation maintenance. Waste
        management, junk removal, debris removal, garbage collection, septic system
        service, sanitation services, portable toilet rental. Fire damage restoration,
        water damage restoration, mold remediation, chimney sweeps, gutter cleaning,
        drain cleaning, property maintenance. Security guard services, alarm system
        monitoring, physical security providers. Snow removal, pool cleaning and
        maintenance, parking lot maintenance.

        DOES NOT INCLUDE: Construction and renovation (V3_Construction). Landscaping
        supply stores (V8_Retail). Manufacturing (V5_Industrial). Veterinarians or
        animal care (V1_Healthcare). Facility security equipment sales (V8_Retail).
    """,

    "V7_Hospitality": """
        RULE: The business's product is an in-person experience — the customer
        comes to the location to eat, drink, sleep, be entertained, or recreate.

        INCLUDES: Restaurants of all cuisines and formats (dine-in, fast food,
        cafes, food trucks), bars, pubs, brewpubs, cocktail bars, coffee shops,
        bakeries, dessert shops, ice cream shops. Hotels, motels, resorts, bed and
        breakfasts, hostels, guest houses, inns, lodges, serviced apartments,
        vacation rentals operated as lodging, RV parks, campgrounds. Event venues,
        banquet halls, concert halls, amphitheaters, stadiums, wedding venues, live
        music venues. Amusement parks, theme parks, water parks, escape rooms,
        bowling alleys, casinos, golf courses, go-kart tracks, ski resorts,
        recreational clubs, paintball centers. Gyms, fitness centers, yoga studios,
        pilates studios, rock climbing gyms. Spas, day spas, massage spas, tanning
        salons, nail salons, hair salons, barbershops. Tour operators, travel
        agencies, cruise agencies, boat tours, helicopter tours.

        DOES NOT INCLUDE: Hotels that only manage properties (V4_RealEstate).
        Catering companies primarily serving corporate clients (V9_Professional).
        Food manufacturers and distributors (V5_Industrial). Sporting goods stores (V8_Retail).
    """,

    "V8_Retail": """
        RULE: The business operates a physical storefront that sells tangible goods
        directly to individual end consumers who walk in and purchase items.

        INCLUDES: Clothing stores, footwear stores, department stores, general
        merchandise stores, dollar stores, discount stores, specialty retail,
        home goods stores, furniture stores, flooring stores, mattress stores,
        hardware stores, electronics stores, appliance stores, pet stores, toy
        stores, book stores, music stores, game stores, sporting goods stores,
        hobby stores, jewelry stores, gift shops, pharmacies, drug stores.
        Grocery stores, supermarkets, health food stores, organic food stores,
        ethnic grocery stores, liquor stores, wine stores, beer stores.
        Camping stores, bicycle shops, fishing stores, outdoor recreation stores.
        Thrift stores, consignment shops, antique stores, pawn shops, outlet stores.
        Auto parts stores open to the public, tire shops (retail), gas stations.

        DOES NOT INCLUDE: B2B wholesalers and distributors (V5_Industrial).
        Online-only retailers with no physical storefront. Restaurants and food
        service where food is consumed on-premises (V7_Hospitality). Repair shops
        that sell parts incidentally (classify by primary service).
    """,

    "V9_Professional": """
        RULE: The business sells specialized knowledge, expertise, or technology
        services. The primary deliverable is advice, a document, software, or
        a managed service — not a physical product or in-person experience.

        INCLUDES: Law firms, attorneys, legal services, notary publics, paralegals.
        Accounting firms, accountants, auditors, tax preparation services, payroll
        services, bookkeepers, financial planners, financial advisors. Management
        consultants, business consultants, HR consultants, marketing consultants.
        Marketing agencies, advertising agencies, branding agencies, PR firms,
        SEO agencies, digital agencies. Software companies, IT service companies,
        computer networking, cybersecurity firms, web hosting providers, ISPs,
        telecommunications companies, data centers, cloud services. Insurance
        agencies, banks, credit unions, investment services, debt collection.
        Staffing agencies, employment agencies, executive recruiters. Architects,
        engineering consultants (non-construction), design firms, industrial designers.
        Private investigators, process servers, notaries, court reporters.

        DOES NOT INCLUDE: Software stores that sell boxed products (V8_Retail).
        On-site trade contractors who install things (V3_Construction). Government
        agencies (V10_Education). Hospitals and medical practices (V1_Healthcare).
    """,

    "V10_Education": """
        RULE: The organization's primary mission is education, workforce training,
        civic administration, public safety, or non-commercial social services.
        Revenue model is tuition, taxes, grants, or donations — not market sales.

        INCLUDES: K-12 schools, universities, colleges, community colleges, technical
        schools, trade schools, vocational schools, language schools, driving schools,
        beauty schools, martial arts schools, dance schools, music schools, tutoring
        centers, test prep centers. Non-profit organizations, charities, foundations,
        volunteer organizations, veterans organizations, social services, food banks,
        homeless shelters, halfway houses, community centers. Government offices:
        city halls, county offices, federal offices, post offices, public health
        departments, DMV, public libraries, police departments, fire departments,
        sheriff departments, courts, probation offices, tax offices. Places of
        worship: churches, mosques, synagogues, temples, shrines as community
        non-commercial organizations. Military bases, armed forces, government agencies.
        Labor unions, professional associations, civic organizations.

        DOES NOT INCLUDE: For-profit private training companies selling courses as
        a product (V9_Professional). Commercial gyms or dance studios that operate
        as entertainment businesses (V7_Hospitality).
    """,

    "ARCHIVE": """
        RULE: The entry is not a business — it is a geographic location, natural
        feature, public infrastructure, or abstract concept with no commercial entity
        that a B2B sales team would target.

        INCLUDES: Natural features — beaches, rivers, lakes, mountains, waterfalls,
        caves, forests, bays, peninsulas, islands, ridges, springs, cliffs, inlets.
        Public parks — national parks, state parks, city parks, nature preserves,
        wildlife refuges, arboretums, botanical gardens. Public infrastructure —
        bridges, canals, highways, dams, train stations (the infrastructure, not the
        business), bus stops. Purely geographic or civic landmarks — plazas, monuments,
        scenic spots, vista points, historical landmarks as places (not businesses).
        Abstract or generic terms with no specific commercial entity: "cars", "services",
        "industry", "health", "entertainment", "company", "store".

        DOES NOT INCLUDE: Businesses that happen to be located at a natural attraction
        (e.g., a tour operator at a national park → V7_Hospitality). Public transit
        companies that sell services (→ V5_Industrial or V9_Professional).
    """
}
