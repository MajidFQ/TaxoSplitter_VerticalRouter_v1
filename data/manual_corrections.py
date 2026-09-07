MANUAL_CORRECTIONS = [

    # ════════════════════════════════════════════════════════════════
    # RULES:
    #   - correct_domain must be DIFFERENT from wrong_domain
    #   - never add (cat, X, X) — it creates contradictory training signal
    #   - keep total count under 70 to avoid drowning the anchor signal
    # ════════════════════════════════════════════════════════════════

    # ── Suffix trap: "station" pulls into Education ──────────────────
    ("power station",                    "V5_Industrial",    "V10_Education"),
    ("smog inspection station",          "V2_Automotive",    "V10_Education"),
    ("weigh station",                    "V2_Automotive",    "V10_Education"),

    # ── Suffix trap: "company" / "supplier" pulls into Industrial ────
    ("software company",                 "V9_Professional",  "V5_Industrial"),
    ("media company",                    "V9_Professional",  "V5_Industrial"),
    ("beauty product supplier",          "V8_Retail",        "V5_Industrial"),
    ("audio visual equipment supplier",  "V9_Professional",  "V5_Industrial"),
    ("hair extensions supplier",         "V8_Retail",        "V5_Industrial"),

    # ── V6_Facilities intruders ──────────────────────────────────────
    ("thermal power plant",              "V5_Industrial",    "V6_Facilities"),
    ("dog trainer",                      "V9_Professional",  "V6_Facilities"),
    ("organic farm",                     "V5_Industrial",    "V6_Facilities"),
    ("grain elevator",                   "V5_Industrial",    "V6_Facilities"),
    ("fortress",                         "ARCHIVE",          "V6_Facilities"),
    ("environmental consultant",         "V9_Professional",  "V6_Facilities"),
    ("wallpaper installer",              "V3_Construction",  "V6_Facilities"),
    ("cemetery",                         "ARCHIVE",          "V6_Facilities"),
    ("satellite communication service",  "V9_Professional",  "V6_Facilities"),
    ("greenhouse",                       "V5_Industrial",    "V6_Facilities"),
    ("commercial photographer",          "V9_Professional",  "V6_Facilities"),
    ("parking garage",                   "V4_RealEstate",    "V6_Facilities"),
    ("painting",                         "ARCHIVE",          "V6_Facilities"),

    # ── V5_Industrial intruders ──────────────────────────────────────
    ("electronics engineer",             "V9_Professional",  "V5_Industrial"),
    ("music producer",                   "V9_Professional",  "V5_Industrial"),
    ("technology museum",                "V10_Education",    "V5_Industrial"),

    # ── V4_RealEstate intruders ──────────────────────────────────────
    ("mine",                             "V5_Industrial",    "V4_RealEstate"),
    ("baseball club",                    "V7_Hospitality",   "V4_RealEstate"),
    ("diamond buyer",                    "V8_Retail",        "V4_RealEstate"),
    ("private investigator",             "V9_Professional",  "V4_RealEstate"),
    ("insurance attorney",               "V9_Professional",  "V4_RealEstate"),
    ("agricultural cooperative",         "V5_Industrial",    "V4_RealEstate"),
    ("film production company",          "V9_Professional",  "V4_RealEstate"),
    ("sports complex",                   "V7_Hospitality",   "V4_RealEstate"),

    # ── V8_Retail intruders ──────────────────────────────────────────
    ("paintball center",                 "V7_Hospitality",   "V8_Retail"),
    ("display stand manufacturer",       "V5_Industrial",    "V8_Retail"),

    # ── V7_Hospitality intruders ─────────────────────────────────────
    ("honey farm",                       "V5_Industrial",    "V7_Hospitality"),
    ("seafood farm",                     "V5_Industrial",    "V7_Hospitality"),
    ("dairy farm",                       "V5_Industrial",    "V7_Hospitality"),
    ("orchard",                          "V5_Industrial",    "V7_Hospitality"),
    ("wedding photographer",             "V9_Professional",  "V7_Hospitality"),
    ("student dormitory",                "V10_Education",    "V7_Hospitality"),
    ("theater production",               "V9_Professional",  "V7_Hospitality"),

    # ── V3_Construction intruders ────────────────────────────────────
    ("graphic designer",                 "V9_Professional",  "V3_Construction"),
    ("website designer",                 "V9_Professional",  "V3_Construction"),
    ("interior designer",                "V9_Professional",  "V3_Construction"),
    ("electrical engineer",              "V9_Professional",  "V3_Construction"),
    ("power plant consultant",           "V9_Professional",  "V3_Construction"),
    ("engineering consultant",           "V9_Professional",  "V3_Construction"),
    ("interior architect office",        "V9_Professional",  "V3_Construction"),
    ("saw mill",                         "V5_Industrial",    "V3_Construction"),
    ("quarry",                           "V5_Industrial",    "V3_Construction"),

    # ── V2_Automotive intruders ──────────────────────────────────────
    ("rail museum",                      "V10_Education",    "V2_Automotive"),
    ("golf driving range",               "V7_Hospitality",   "V2_Automotive"),
    ("customs broker",                   "V9_Professional",  "V2_Automotive"),
    ("off-road racing venue",            "V7_Hospitality",   "V2_Automotive"),
    ("rv park",                          "V7_Hospitality",   "V2_Automotive"),
    ("plastic injection molding service","V5_Industrial",    "V2_Automotive"),
    ("horseback riding service",         "V7_Hospitality",   "V2_Automotive"),

    # ── V1_Healthcare intruders ──────────────────────────────────────
    ("make-up artist",                   "V7_Hospitality",   "V1_Healthcare"),
    ("yoga instructor",                  "V7_Hospitality",   "V1_Healthcare"),
    ("photo lab",                        "V8_Retail",        "V1_Healthcare"),
    ("life coach",                       "V9_Professional",  "V1_Healthcare"),
    ("dog day care center",              "V6_Facilities",    "V1_Healthcare"),
]