DOMAINS = {

    "D01_Healthcare": """
        RULE: The business's primary purpose is diagnosing, treating, or caring
        for human physical or mental health. The customer is a human patient.

        INCLUDES: Medical doctors (GPs, specialists), surgeons, dentists,
        orthodontists, chiropractors, optometrists, ophthalmologists, physical
        therapists, occupational therapists, speech therapists, psychologists,
        psychiatrists, counselors, nutritionists, audiologists, midwives,
        acupuncturists, massage therapists (clinical/medical), holistic and
        alternative medicine practitioners. Hospitals, urgent care centers,
        emergency rooms, surgical centers, medical groups, medical clinics,
        medical laboratories, diagnostic imaging, MRI centers, pregnancy care,
        fertility clinics, IV therapy, dialysis centers, addiction treatment,
        rehabilitation centers, home health care, nursing homes, hospices,
        assisted living facilities, adult day care.

        DOES NOT INCLUDE: Animal health or veterinary (D02_PetCare). Gyms,
        yoga studios, spas, salons, tanning (D09_BeautyWellness or
        D10_FitnessSports). Pharmacies and medical supply retail (D11_Retail).
        Life coaches or personal trainers (D10_FitnessSports).
    """,

    "D02_PetCare": """
        RULE: The business provides health, grooming, boarding, or care
        services where the primary patient or client is an animal.

        INCLUDES: Veterinarians, animal hospitals, veterinary specialists,
        emergency animal clinics, pet dental care. Dog groomers, cat groomers,
        mobile pet groomers. Dog training, pet obedience schools. Boarding
        kennels, doggy day care, cat boarding, pet sitting services, dog
        walking services. Aquarium maintenance, exotic animal care,
        livestock veterinarians. Pet cremation, animal shelters and rescues.

        DOES NOT INCLUDE: Pet supply stores and pet food retail (D11_Retail).
        Animal farms raising livestock for food production (D13_Manufacturing).
        Human healthcare (D01_Healthcare).
    """,

    "D03_Automotive": """
        RULE: The business sells, repairs, services, rents, or cleans motor
        vehicles or vehicle-specific parts and accessories.

        INCLUDES: Car dealerships (new and used), motorcycle dealers, ATV
        dealers, truck dealers, trailer dealers, RV dealers, golf cart
        dealers, electric vehicle dealers, boat dealers, snowmobile dealers.
        Auto repair shops, auto body shops, collision repair, brake shops,
        muffler shops, transmission shops, oil change services, wheel
        alignment, auto glass repair, dent removal, car detailing, car wash,
        tire shops, roadside assistance, towing services. Auto parts stores,
        car battery stores, motorcycle parts stores. Smog inspection, vehicle
        inspection, auto auctions, fleet management services.

        DOES NOT INCLUDE: Gas stations as standalone fuel retailers (D11_Retail).
        Driving schools (D14_PublicNonProfit or D12_B2BCorporate). Parking
        lots and garages as real estate (D06_RealEstate). Boat tours
        (D08_Lodging). Manufacturers of vehicles (D13_Manufacturing).
    """,

    "D04_Construction": """
        RULE: The business physically builds, installs, renovates, or
        structurally repairs buildings and infrastructure on-site at the
        property. Workers go to the site and physically change the structure.

        INCLUDES: General contractors, home builders, custom home builders,
        remodeling contractors, roofing contractors, HVAC installers,
        electrical contractors (installation), plumbing contractors, concrete
        contractors, demolition contractors, masonry contractors, insulation
        contractors, flooring contractors (installation), drywall contractors,
        siding contractors, tile contractors, paving contractors, fence
        contractors, swimming pool contractors, deck builders, garage
        builders, shed builders, dock builders, modular home builders,
        foundation contractors, excavation contractors, scaffolding services.
        Carpenters, plumbers, electricians, glaziers, plasterers, welders
        doing on-site structural work. Road construction, bridge construction,
        civil engineering contractors.

        DOES NOT INCLUDE: Routine maintenance and cleaning (D05_Cleaning).
        Interior designers and architects who do not build (D12_B2BCorporate).
        Manufacturers of building materials (D13_Manufacturing). Landscaping
        and lawn care (D05_Cleaning).
    """,

    "D05_Cleaning": """
        RULE: The business provides routine or project-based physical
        maintenance, cleaning, security, or restoration of properties.
        They maintain the property — they do not build or renovate it.

        INCLUDES: Commercial office cleaning, janitorial services, maid
        services, house cleaning, carpet cleaning, window cleaning, pressure
        washing, air duct cleaning, dryer vent cleaning. Landscaping, lawn
        care, lawn mowing, arborist services, tree trimming, tree removal,
        stump grinding, hedge trimming, leaf blowing, irrigation maintenance.
        Pest control, rodent control, termite treatment. Waste management,
        junk removal, debris removal, garbage collection, septic system
        service, sanitation, portable toilet rental. Fire and water damage
        restoration, mold remediation, chimney sweeps, gutter cleaning and
        repair, drain cleaning, property maintenance services. Snow removal,
        pool cleaning and maintenance. Security guard services, security
        patrol services, alarm monitoring.

        DOES NOT INCLUDE: Construction and renovation (D04_Construction).
        Landscaping supply stores (D11_Retail). Manufacturing (D13_Manufacturing).
    """,

    "D06_RealEstate": """
        RULE: The business's revenue comes from property transactions,
        property management, or financial instruments tied to real property.

        INCLUDES: Real estate agencies, real estate agents and brokers,
        commercial real estate firms, industrial real estate, property
        management companies, property investment firms, real estate
        appraisers, home inspectors, mortgage lenders, mortgage brokers,
        loan agencies, real estate attorneys, foreclosure services, escrow
        services, title companies, land surveyors, housing authorities,
        homeowners associations. Apartment complexes, housing developments,
        condominiums, student housing, housing cooperatives, furnished
        apartments. Self-storage facilities, cold storage operators, records
        storage facilities, parking garages and parking lots.

        DOES NOT INCLUDE: Construction companies that build properties
        (D04_Construction). Moving and logistics services (D13_Manufacturing).
        Short-term vacation rentals operating as hospitality (D08_Lodging).
        Banks and general financial institutions (D12_B2BCorporate).
    """,

    "D07_FoodDining": """
        RULE: The business is a place where customers come in person to
        purchase and consume food or beverages on-site or as takeout.

        INCLUDES: Restaurants of all cuisines and formats (dine-in, fast
        food, fast casual, fine dining), diners, cafes, coffee shops,
        espresso bars, tea houses, juice bars, smoothie shops, food trucks,
        food halls, food courts, delis, sandwich shops, pizza places, burger
        joints, taco stands. Bars, pubs, taverns, brewpubs, cocktail bars,
        wine bars, sports bars. Bakeries, donut shops, pastry shops, dessert
        shops, ice cream parlors, frozen yogurt shops, candy stores.
        Catering companies primarily serving individuals and events.

        DOES NOT INCLUDE: Hotels that serve food secondarily (D08_Lodging).
        Grocery stores and food retail (D11_Retail). Food manufacturers and
        distributors (D13_Manufacturing). Corporate catering (D12_B2BCorporate).
    """,

    "D08_Lodging": """
        RULE: The business provides overnight accommodation or organized
        travel and tourism experiences.

        INCLUDES: Hotels, motels, boutique hotels, luxury resorts, beach
        resorts, mountain resorts, casino resorts, extended-stay hotels,
        bed and breakfasts, hostels, guest houses, inns, lodges, serviced
        apartments, vacation rental operators, RV parks, campgrounds,
        glamping sites, cabin rentals. Tour operators, travel agencies,
        cruise agencies, sightseeing tour companies, boat tour operators,
        helicopter tour operators, hot air balloon rides, guided hiking
        tours, adventure tourism operators. Airport shuttles and travel
        transport services.

        DOES NOT INCLUDE: Restaurants and bars (D07_FoodDining). Real estate
        managing long-term rentals (D06_RealEstate). Amusement and recreation
        venues (D10_FitnessSports).
    """,

    "D09_BeautyWellness": """
        RULE: The business provides personal appearance, grooming, or
        relaxation services directly to individual human clients.

        INCLUDES: Hair salons, barbershops, hair colorists, blowout bars,
        braiding salons. Nail salons, manicure and pedicure services, nail
        art studios. Waxing studios, threading studios, laser hair removal,
        electrolysis. Skincare clinics, facials, estheticians, med spas
        (non-medical cosmetic). Massage spas, day spas, body treatment
        studios, float therapy. Tattoo studios, piercing studios. Eyelash
        extensions, brow studios, permanent makeup. Tanning salons, spray
        tanning. Makeup artists, bridal hair and makeup. Holistic wellness:
        aromatherapy, reiki, reflexology studios.

        DOES NOT INCLUDE: Medical procedures by licensed physicians
        (D01_Healthcare). Clinical massage therapy billed to insurance
        (D01_Healthcare). Gyms and fitness centers (D10_FitnessSports).
        Beauty product retail (D11_Retail). Cosmetology schools
        (D14_PublicNonProfit).
    """,

    "D10_FitnessSports": """
        RULE: The business provides in-person active recreation, exercise,
        sports training, or entertainment as a live venue experience.

        INCLUDES: Gyms, fitness centers, CrossFit boxes, weightlifting gyms.
        Yoga studios, pilates studios, barre studios, cycling studios.
        Martial arts schools, boxing gyms, wrestling clubs, jiu-jitsu academies.
        Rock climbing gyms, parkour gyms. Dance studios, ballet schools.
        Swimming pools (private), tennis clubs, golf courses, golf driving
        ranges, mini golf. Sports complexes, athletic facilities, batting
        cages, go-kart tracks, paintball centers, archery ranges, shooting
        ranges. Bowling alleys, billiards halls, axe throwing venues.
        Amusement parks, theme parks, water parks, escape rooms, arcades,
        laser tag, trampoline parks. Event venues, concert halls, theaters,
        stadiums, amphitheaters, comedy clubs, live music venues, casinos,
        nightclubs, banquet halls for events.

        DOES NOT INCLUDE: Dance schools teaching academic programs
        (D14_PublicNonProfit). Medical rehabilitation (D01_Healthcare).
        Sporting goods stores (D11_Retail). Tour operators (D08_Lodging).
    """,

    "D11_Retail": """
        RULE: The business operates a physical storefront that sells tangible
        goods directly to individual end consumers who walk in and purchase.

        INCLUDES: Clothing stores, footwear stores, department stores,
        general merchandise stores, dollar stores, discount stores, specialty
        retail, home goods stores, furniture stores, flooring stores, mattress
        stores, hardware stores, electronics stores, appliance stores, toy
        stores, book stores, music stores, game stores, sporting goods stores,
        hobby stores, jewelry stores, gift shops, pharmacies, drug stores.
        Grocery stores, supermarkets, health food stores, organic food stores,
        ethnic grocery stores, liquor stores, wine stores. Pet supply stores,
        pet food stores. Camping stores, bicycle shops, outdoor recreation
        stores. Thrift stores, antique stores, pawn shops, consignment shops.
        Gas stations, convenience stores, vape shops, smoke shops.

        DOES NOT INCLUDE: B2B wholesalers (D13_Manufacturing). Online-only
        retailers. Restaurants where food is consumed on-site (D07_FoodDining).
        Service businesses that incidentally sell products.
    """,

    "D12_B2BCorporate": """
        RULE: The business sells specialized professional knowledge, legal,
        financial, technology, or administrative services — primarily to
        other businesses or sophisticated clients. The deliverable is advice,
        a document, software, or a managed service, not a physical product
        or in-person experience.

        INCLUDES: Law firms, attorneys, legal services, notary publics,
        paralegals. Accounting firms, accountants, auditors, tax preparation,
        payroll services, bookkeepers. Financial planners, financial advisors,
        investment services, insurance agencies, banks, credit unions, debt
        collectors. Management consultants, business consultants, HR
        consultants. Marketing agencies, advertising agencies, branding
        agencies, PR firms, SEO agencies, digital agencies. Software
        companies, IT service companies, managed IT providers, cybersecurity
        firms, web hosting, ISPs, data centers, cloud services, tech support.
        Staffing agencies, employment agencies, executive recruiters.
        Architects, engineering consultants (office-based), design firms.
        Private investigators, process servers, court reporters, notaries.
        Commercial printing, sign companies (design and print).

        DOES NOT INCLUDE: On-site trade contractors (D04_Construction).
        Government agencies (D14_PublicNonProfit). Hospitals and medical
        practices (D01_Healthcare). Software retail stores (D11_Retail).
    """,

    "D13_Manufacturing": """
        RULE: The business manufactures physical goods at scale, distributes
        raw materials or products B2B, or operates energy and logistics
        infrastructure. The primary customer is another business.

        INCLUDES: Manufacturers of all types — auto parts, electronics,
        furniture, food, industrial machinery, chemicals, glass, metals,
        tools, batteries, plastics, textiles, clothing, shoes, paper, wood
        products. Industrial suppliers and B2B wholesalers: metal suppliers,
        pipe suppliers, electrical equipment suppliers, hydraulic equipment,
        building material suppliers, energy suppliers, industrial gases,
        chemical wholesalers. Energy infrastructure: oil and gas companies,
        petroleum companies, power plants, electric utilities, solar energy
        farms, wind farms, refineries, nuclear power plants. Logistics:
        freight forwarders, shipping companies, trucking companies, import
        and export firms, warehouses, distribution centers, courier services.
        Food processing plants, commercial breweries, distilleries, packaging
        companies, commercial print shops. Farms producing agricultural goods
        as a commodity business (not agritourism). Mines, quarries,
        sawmills, steel mills.

        DOES NOT INCLUDE: Retail stores selling manufactured goods to
        consumers (D11_Retail). On-site construction contractors
        (D04_Construction). Software and tech service companies (D12_B2BCorporate).
        Restaurants and food service (D07_FoodDining).
    """,

    "D14_PublicNonProfit": """
        RULE: The organization's primary mission is education, public
        administration, civic service, public safety, or a non-commercial
        social mission. Revenue model is tuition, taxes, grants, or
        donations — not market-rate sales.

        INCLUDES: K-12 schools, universities, colleges, community colleges,
        technical and trade schools, vocational schools, language schools,
        driving schools, cosmetology schools, culinary schools, music
        schools, martial arts schools (if non-profit or community-based),
        dance schools, tutoring centers, test prep centers. Non-profit
        organizations, charities, foundations, volunteer organizations,
        veterans organizations, social services organizations, food banks,
        homeless shelters, halfway houses, community centers, animal shelters.
        Government offices: city halls, county offices, federal offices,
        post offices, public health departments, DMV, public libraries,
        police departments, fire departments, courts, probation offices, tax
        offices. Places of worship: churches, mosques, synagogues, temples,
        shrines as non-commercial community organizations. Military bases,
        armed forces, government agencies, labor unions, professional
        associations, civic organizations.

        DOES NOT INCLUDE: For-profit private training companies (D12_B2BCorporate).
        Commercial gyms and dance studios (D10_FitnessSports). Cosmetology
        schools operated as for-profit businesses (D12_B2BCorporate).
    """,

    "ARCHIVE": """
        RULE: The entry is not a business — it is a geographic location,
        natural feature, public landmark, or abstract term with no
        identifiable commercial entity that a B2B sales team could contact.

        INCLUDES: Natural features — beaches, rivers, lakes, mountains,
        waterfalls, caves, forests, bays, islands, peninsulas, cliffs,
        springs, inlets, ridges. Public parks — national parks, state parks,
        city parks, nature preserves, wildlife refuges, botanical gardens.
        Public infrastructure as places — bridges, dams, canals, highways,
        train stations (the physical location, not a transit company).
        Purely geographic or civic landmarks — plazas, monuments, scenic
        overlooks, historical sites as places (not as museum businesses).
        Abstract or overly generic terms with no specific commercial
        entity: "services", "industry", "company", "store", "center" alone.

        DOES NOT INCLUDE: Businesses operating at natural locations (e.g.
        a tour operator at a national park belongs in D08_Lodging). Transit
        companies that sell tickets and operate routes (D13_Manufacturing
        or D12_B2BCorporate).
    """
}
