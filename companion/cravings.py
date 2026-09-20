# companion/cravings.py

CRAVING_CATEGORIES = [
    "🍫 Sweet & Indulgent",
    "🍟 Salty & Savory",
    "🍋 Sour, Tangy & Zesty",
    "🥨 Crispy & Crunchy",
    "🥛 Creamy & Rich",
    "🧊 Icy, Cold & Refreshing",
    "🍲 Warm Comfort Food"
]

PANTRY_DATABASE = [
    "Bananas", "Apples", "Dates", "Dark Chocolate", "Yogurt / Curd",
    "Milk", "Oats", "Makhana (Fox Nuts)", "Peanuts / Almonds", "Peanut Butter",
    "Cucumber", "Lemon / Lime", "Chaat Masala", "Paneer", "Toast / Bread"
]

RECIPES = {
    "🍫 Sweet & Indulgent": [
        {"name": "Warm Jaggery Oats Bowl", "prep": "Cook oats in warm milk, stir in jaggery and a pinch of cinnamon.", "vibe": "Warm comfort", "safety": "Sustained iron and fiber."},
        {"name": "Dark Chocolate Date Bites", "prep": "Slit soft dates, add peanut butter, dust with dark cocoa.", "vibe": "Quick luxury", "safety": "Rich in natural magnesium."},
        {"name": "Banana Yogurt Whip", "prep": "Whisk thick curd with mashed ripe banana and a drop of honey.", "vibe": "Silky sweet", "safety": "Gentle potassium boost."}
    ],
    "🍟 Salty & Savory": [
        {"name": "Roasted Ghee Makhana", "prep": "Slow roast fox nuts with 1 tsp ghee and rock salt.", "vibe": "Crispy fix", "safety": "Low glycemic and light on tummy."},
        {"name": "Herbed Paneer Cubes", "prep": "Toss fresh paneer in black pepper and chaat masala, pan sear 2 mins.", "vibe": "Savory bite", "safety": "Bioavailable calcium source."}
    ],
    "🍋 Sour, Tangy & Zesty": [
        {"name": "Chilled Mint Lemon Spritz", "prep": "Crush fresh mint, squeeze lime into ice-cold water with sendha namak.", "vibe": "Nausea-vanisher", "safety": "Natural electrolyte balance."},
        {"name": "Chatpata Cucumber Sticks", "prep": "Thick cucumber batons with lemon juice and roasted cumin.", "vibe": "Crisp crunch", "safety": "Instant hydration."}
    ],
    "🥨 Crispy & Crunchy": [
        {"name": "Toasted Nut Crunch", "prep": "Dry-roast peanuts and almonds with a pinch of pink salt.", "vibe": "Classic bite", "safety": "Plant-based healthy fats."}
    ],
    "🥛 Creamy & Rich": [
        {"name": "Cardamom Hung Curd Shrikhand", "prep": "Whisk strained thick curd with honey and crushed elaichi.", "vibe": "Velvet dessert", "safety": "Gut-soothing probiotics."}
    ],
    "🧊 Icy, Cold & Refreshing": [
        {"name": "Frozen Yogurt Bark", "prep": "Spread curd on a plate with dates, freeze 30 mins, snap into pieces.", "vibe": "Cold ice-cream bite", "safety": "Cooling calcium snack."}
    ],
    "🍲 Warm Comfort Food": [
        {"name": "Golden Haldi Milk & Warm Toast", "prep": "Warm milk with a pinch of turmeric, served with buttered toast.", "vibe": "Nani-style care", "safety": "Anti-inflammatory and relaxing."}
    ]
}

def match_pantry_vast(category: str, user_ingredients: list):
    recipes = RECIPES.get(category, RECIPES["🍫 Sweet & Indulgent"])
    return recipes