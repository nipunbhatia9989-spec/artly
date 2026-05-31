# 50-level art curriculum.
# difficulty: 1=beginner → 5=advanced
# wikipedia_article: title used by the Wikipedia REST API

LEVELS = [
    # ── FOUNDATIONS (1–10) ──────────────────────────────────────────────
    (1,  "What Is Art?",               "Explore the definition, purpose, and forms of art.", 1, "Art"),
    (2,  "Elements of Art",            "The seven building blocks every artwork is made of.", 1, "Elements of art"),
    (3,  "Color Theory",               "Primary colors, the color wheel, and how colors interact.", 1, "Color theory"),
    (4,  "Principles of Design",       "Balance, contrast, emphasis, and other design rules.", 1, "Design elements and principles"),
    (5,  "Art Mediums",                "Oils, watercolor, charcoal, clay, and more.", 1, "Art media"),
    (6,  "Drawing",                    "Line, form, and the basics of mark-making.", 1, "Drawing"),
    (7,  "Painting",                   "Techniques, supports, and the history of painting.", 1, "Painting"),
    (8,  "Sculpture",                  "Three-dimensional art across cultures and centuries.", 1, "Sculpture"),
    (9,  "Visual Composition",         "How artists arrange elements to guide the viewer's eye.", 1, "Composition (visual arts)"),
    (10, "Art and Society",            "Why art matters — its cultural, political, and social roles.", 1, "Art and society"),

    # ── ANCIENT ART (11–15) ─────────────────────────────────────────────
    (11, "Prehistoric Cave Art",       "The earliest known human images — ochre, charcoal, and mystery.", 2, "Cave painting"),
    (12, "Ancient Egyptian Art",       "Hieroglyphs, tombs, and the art of the afterlife.", 2, "Ancient Egyptian art"),
    (13, "Ancient Greek Art",          "Idealized human form, pottery, and classical sculpture.", 2, "Ancient Greek art"),
    (14, "Ancient Roman Art",          "Mosaics, frescoes, and the art of an empire.", 2, "Roman art"),
    (15, "Byzantine Art",              "Sacred icons, gold mosaics, and the art of faith.", 2, "Byzantine art"),

    # ── MEDIEVAL TO RENAISSANCE (16–22) ─────────────────────────────────
    (16, "Medieval Art",               "Illuminated manuscripts, Gothic cathedrals, and devotion.", 2, "Medieval art"),
    (17, "The Italian Renaissance",    "Humanism, perspective, and art reborn in Italy.", 2, "Italian Renaissance"),
    (18, "Leonardo da Vinci",          "The ultimate Renaissance man — artist, scientist, inventor.", 2, "Leonardo da Vinci"),
    (19, "Michelangelo",               "The Sistine Chapel, David, and the power of the human body.", 2, "Michelangelo"),
    (20, "Raphael",                    "Grace, harmony, and the School of Athens.", 3, "Raphael (painter)"),
    (21, "The Northern Renaissance",   "Van Eyck, Dürer, and the art of Northern Europe.", 3, "Northern Renaissance"),
    (22, "Perspective in Art",         "How artists create depth and space on a flat surface.", 3, "Perspective (graphical)"),

    # ── 17TH–18TH CENTURY (23–27) ───────────────────────────────────────
    (23, "Baroque Art",                "Drama, darkness, and light — Caravaggio and Rembrandt.", 3, "Baroque"),
    (24, "Dutch Golden Age Painting",  "Vermeer, still life, and art for the merchant class.", 3, "Dutch Golden Age painting"),
    (25, "Rococo",                     "Playfulness, elegance, and the art of French aristocracy.", 3, "Rococo"),
    (26, "Neoclassicism",              "A return to ancient ideals — order, reason, and restraint.", 3, "Neoclassicism"),
    (27, "Romanticism",                "Emotion, the sublime, and the power of nature.", 3, "Romanticism"),

    # ── 19TH CENTURY (28–33) ────────────────────────────────────────────
    (28, "Realism",                    "Ordinary life as worthy of art — Courbet and the everyday.", 3, "Realism (arts)"),
    (29, "Impressionism",              "Capturing fleeting light — Monet, Renoir, and the open air.", 3, "Impressionism"),
    (30, "Claude Monet",               "Water lilies, haystacks, and the birth of modern painting.", 3, "Claude Monet"),
    (31, "Post-Impressionism",         "Beyond light — Van Gogh, Cézanne, and Gauguin.", 4, "Post-Impressionism"),
    (32, "Vincent van Gogh",           "Swirling skies, vivid color, and a tortured genius.", 4, "Vincent van Gogh"),
    (33, "Art Nouveau",                "Organic forms, flowing lines, and the art of everyday beauty.", 4, "Art Nouveau"),

    # ── EARLY MODERN (34–40) ────────────────────────────────────────────
    (34, "Fauvism",                    "Wild color unchained — Matisse and the beasts of paint.", 4, "Fauvism"),
    (35, "Expressionism",              "Emotion distorted into image — Munch and the inner scream.", 4, "Expressionism"),
    (36, "Cubism",                     "Multiple perspectives at once — Picasso and Braque.", 4, "Cubism"),
    (37, "Pablo Picasso",              "Guernica, Cubism, and a century of reinvention.", 4, "Pablo Picasso"),
    (38, "Surrealism",                 "Dreams made visible — Dalí, Magritte, and the unconscious.", 4, "Surrealism"),
    (39, "Salvador Dalí",              "Melting clocks, the paranoiac-critical method, and spectacle.", 4, "Salvador Dalí"),
    (40, "Abstract Expressionism",     "Action painting and pure emotion — Pollock and Rothko.", 4, "Abstract expressionism"),

    # ── CONTEMPORARY (41–50) ────────────────────────────────────────────
    (41, "Pop Art",                    "Warhol, Lichtenstein, and consumer culture as canvas.", 5, "Pop art"),
    (42, "Andy Warhol",                "Soup cans, silkscreen, and the Factory.", 5, "Andy Warhol"),
    (43, "Minimalism",                 "Less is more — Donald Judd, Frank Stella, and pure form.", 5, "Minimalism"),
    (44, "Conceptual Art",             "The idea as the artwork — art that challenges what art is.", 5, "Conceptual art"),
    (45, "Photography as Art",         "From Daguerreotype to Cindy Sherman — photography's art journey.", 5, "Photography"),
    (46, "Street Art",                 "Banksy, murals, and the city as gallery.", 5, "Street art"),
    (47, "Digital Art",                "Pixels, screens, generative art, and NFTs.", 5, "Digital art"),
    (48, "Installation Art",           "Environments you enter — immersive art beyond the frame.", 5, "Installation art"),
    (49, "Performance Art",            "The body as medium — Marina Abramović and live art.", 5, "Performance art"),
    (50, "Contemporary Art Today",     "Where art stands now — pluralism, globalism, and the market.", 5, "Contemporary art"),
]
