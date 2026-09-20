# core/craving_engine.py
import random

PANTRY_STAPLES = [
    "Banana", "Apple", "Mango", "Strawberries", "Milk", "Curd / Yogurt",
    "Oats", "Makhana", "Peanut Butter", "Honey / Jaggery", "Dark Chocolate",
    "Bread", "Eggs", "Besan", "Poha", "Paneer", "Lemon", "Cucumber", 
    "Chaat Masala", "Ghee", "Nuts (Almonds/Walnuts)", "Coconut Water"
]

# Base components for generative expansion (1000+ permutations)
FLAVOR_MATRIX = {
    "🍫 Sweet": {
        "easy": [
            "Ghee-roasted banana slices dusted with cinnamon & jaggery",
            "Chilled dahi with crushed Marie biscuits & a swirl of honey",
            "Warm milk with crushed almonds, cardamom, and saffron strands",
            "Dates stuffed with crunchy peanut butter & a touch of dark chocolate",
            "Quick Apple & honey chaat with a pinch of sweet cinnamon"
        ],
        "time": [
            "Slow-cooked Besan & Jaggery Sheera made with aromatic desi ghee",
            "Creamy Roasted Makhana Kheer sweetened with dates",
            "Warm Atta Halwa infused with crushed green cardamom",
            "Pan-toasted whole wheat french toast topped with caramelized bananas",
            "Oats & Jaggery Kheer garnished with toasted cashews"
        ],
        "exotic": [
            "Cardamom-spiced dark chocolate fondue with chilled seasonal fruit skewers",
            "Coconut milk Chia Pudding topped with ripe Alphonso puree",
            "Rose petal (Gulkand) & saffron stuffed dates topped with roasted pistachios",
            "Warm baked pear with sweet jaggery-butter glaze & crushed walnuts",
            "Avocado chocolate mousse sweetened lightly with jaggery syrup"
        ]
    },
    "🍟 Salty": {
        "easy": [
            "Crispy ghee-roasted Makhana tossed in pink salt and roasted cumin",
            "Chilled cucumber & tender tomato slices sprinkled with homemade chaat masala",
            "Toasted brown bread slice with creamy mashed paneer and black salt",
            "Light roasted puffed rice (Kurmura) with roasted peanuts & curry leaves",
            "Boiled egg slices sprinkled with fresh cracked pepper and sea salt"
        ],
        "time": [
            "Light steamed Poha loaded with crunchy peanuts, mustard seeds & lemon",
            "Tawa-toasted Paneer Bhurji tucked into a warm multigrain roti",
            "Crispy Besan Chilla made with shredded carrots, coriander & cumin",
            "Steamed corn chaat tossed in warm salted butter and green chilies",
            "Warm Moong Dal Cheela stuffed with mild grated paneer"
        ],
        "exotic": [
            "Za'atar-spiced roasted lotus seeds (Makhana) with toasted sesame",
            "Air-crisped sweet potato fries tossed in smoked paprika & pink Himalayan salt",
            "Avocado & crumbled fresh paneer tartine on sourdough with flaky salt",
            "Whipped salted feta & labneh dip with warm wholewheat pita wedges",
            "Herb-infused salted cottage cheese bites grilled with sweet bell peppers"
        ]
    },
    "🍋 Sour": {
        "easy": [
            "Chilled raw mango slices dusted with mild Kashmiri chilli & rock salt",
            "Fresh sweet-lime (Mosambi) segments sprinkled with black salt",
            "Crisp green apple rounds dipped in tangy spiced lemon-honey dressing",
            "Tangy hung-curd dip with fresh lemon zest and crunchy cucumber ribbons",
            "Starfruit (Kamrakh) slices tossed in black salt and roasted jeera"
        ],
        "time": [
            "Sweet and tangy Tamarind-date bhel with plenty of crisp coriander",
            "Warm lemon-coriander vegetable broth with soft steamed dumplings",
            "Spiced curd rice tempered with mustard seeds, ginger & pickled amla",
            "Tangy Matar Chaat cooked with dry mango powder (Amchur) & lemon juice",
            "Roasted sweet potato chaat tossed with fresh lemon and pomegranate seeds"
        ],
        "exotic": [
            "Sumac-spiced citrus carpaccio with mint leaves and pomegranate glaze",
            "Pickled baby radishes and cucumbers in apple cider vinegar & crushed pepper",
            "Chilled passionfruit and tender coconut spritzer with fresh lime",
            "Tangy Mediterranean green olive & preserved lemon tapenade on toast",
            "Kaffir lime & lemongrass infused clear vegetable broth"
        ]
    },
    "🌶️ Spicy": {
        "easy": [
            "Spiced masala papad topped with chopped onions, tomatoes & coriander",
            "Crispy roasted peanuts tossed in red chilli flakes, chaat masala & lemon",
            "Toasted bread with a thin spread of mint-coriander chutney & cheese",
            "Spicy boiled chana chaat with chopped ginger and green chillies",
            "Cucumber disks with hot peri-peri sprinkle and sea salt"
        ],
        "time": [
            "Mumbai-style Masala Pav lightly toasted with spicy tomato garlic gravy",
            "Stuffed spicy paneer paratha served with a bowl of cooling mint curd",
            "Spicy crushed corn and pea cutlets cooked crisp on an iron tawa",
            "Warm South Indian Rasam served with a handful of crushed appalam",
            "Spicy vegetable Kathi roll with pickled onions and zesty mustard sauce"
        ],
        "exotic": [
            "Korean gochujang-glazed mild pan-seared paneer cubes with sesame",
            "Jalapeño and sweet corn poppers baked with Monterey Jack cheese",
            "Spicy chipotle black bean dip with baked cumin tortilla crisps",
            "Harissa-roasted carrot skewers paired with cooling hung curd sauce",
            "Thai red curry infused roasted peanuts and cashews"
        ]
    },
    "🥭 Fruity": {
        "easy": [
            "Chilled bowl of diced sweet mangoes, strawberries & mint sprigs",
            "Fresh papaya cubes sprinkled with a squeeze of fresh lime juice",
            "Watermelon triangles topped with chopped fresh mint & rock salt",
            "Sliced sweet pears paired with mild cheddar cheese cubes",
            "Juicy pomegranate pearls mixed with sweet seedless grapes"
        ],
        "time": [
            "Warm slow-simmered spiced apple compote with toasted cinnamon oats",
            "Fresh mixed berry coulis layered with thick hung curd parfait",
            "Classic Shikandji-poached pear served with sweet vanilla cream",
            "Creamy coconut milk fruit salad tossed with tender coconut slices",
            "Baked seasonal stone fruits drizzled with wild blossom honey"
        ],
        "exotic": [
            "Acai bowl infused with dragonfruit puree and coconut flakes",
            "Chilled lychee and rose compote over creamy coconut cream",
            "Passion fruit & tender coconut jelly cups with mint blossom",
            "Macerated figs with citrus zest and whipped mascarpone",
            "Grilled pineapple wedges dusted with mild star-anise powder"
        ]
    },
    "🥛 Creamy": {
        "easy": [
            "Chilled set curd blended smoothly with cardamom & a spoon of honey",
            "Ripe banana mashed with warm whole milk and crushed cashews",
            "Creamy paneer cubes tossed gently in thick homemade curd and herbs",
            "Ripe avocado mashed smoothly on toasted multigrain bread",
            "Full-cream chilled milk blended with soft dates and soaked almonds"
        ],
        "time": [
            "Traditional velvety Mango Shrikhand whipped with green cardamom",
            "Rich Paneer Butter Gravy with mild aromatic spices and warm paratha",
            "Cream of roasted butternut squash soup made with fresh coconut milk",
            "Slow-stirred Rabdi sweetened with dates and loaded with pistachios",
            "Baked macaroni with creamy white béchamel sauce and cheddar"
        ],
        "exotic": [
            "Chilled saffron & pistachio infused Italian Panna Cotta",
            "Silken tofu berry pudding with a touch of vanilla bean",
            "Truffle-infused creamy polenta topped with sautéed wild mushrooms",
            "Turkish hung-labneh drizzled with honeyed fig syrup",
            "Matcha green tea and white chocolate whipped cream pots"
        ]
    },
    "🥨 Crunchy": {
        "easy": [
            "Oven-crisped spiced chickpeas (Kabuli Chana) with rock salt",
            "Toasted almond and walnut mix with sunflower & pumpkin seeds",
            "Crispy khakhra drizzled with two drops of ghee and dry methi masala",
            "Crunchy carrot and celery sticks dipped in thick peanut butter",
            "Homemade lightly salted popcorn tossed with dry nutritional yeast"
        ],
        "time": [
            "Crispy baked vegetable cutlets crusted with roasted poha crumbs",
            "Tawa-crisped multi-seed Lavash crackers with fresh garlic hummus",
            "Stir-fried crunchy lotus stems (Nadru) tossed in mild sweet-tangy glaze",
            "Crispy baked palak (spinach) leaves dusted with dry amchur masala",
            "Golden toasted granola clusters baked with rolled oats, jaggery & seeds"
        ],
        "exotic": [
            "Japanese nori sesame crisps paired with creamy wasabi mayo",
            "Taro root & parsnip chips lightly seasoned with Himalayan pink salt",
            "Rosemary & sea salt sourdough crostini with whipped goat cheese",
            "Baked crunchy plantain crisps with Caribbean herb salsa",
            "Crispy tempura-style green beans with toasted sesame dipping sauce"
        ]
    },
    "🧊 Something Cold": {
        "easy": [
            "Fresh tender coconut water served over crushed ice and tender malai",
            "Frozen seedless grapes dusted with sweet chaat masala",
            "Chilled sweet lassi topped with a spoon of homemade fresh cream",
            "Blended frozen banana 'nice-cream' with a drop of vanilla extract",
            "Iced fresh watermelon cooler with fresh crushed mint leaves"
        ],
        "time": [
            "Authentic Matka Malai Kulfi infused with cardamom & saffron",
            "Homemade fresh strawberry & curd popsicles frozen overnight",
            "Chilled Badam Milk infused with rose petals and crushed pistachios",
            "Slow-churned Alphonso mango sorbet with fresh lime zest",
            "Frozen mixed berry and greek yogurt bark with jaggery caramel drizzle"
        ],
        "exotic": [
            "Espresso-free chilled iced matcha latte with creamy oat milk",
            "Chilled coconut water granita with a squeeze of fresh Key lime",
            "Cold strawberry & elderflower infusion over crystalline ice",
            "Affogato made with caffeine-free chicory brew over rich vanilla ice cream",
            "Chilled yuzu and peach slushie topped with edible flowers"
        ]
    },
    "🍲 Comfort Food": {
        "easy": [
            "Warm Moong Dal Khichdi served with a dollop of pure desi ghee",
            "Soft buttered toast dipped in sweet, warm cardamom milk",
            "Steaming cup of mild turmeric milk (Golden Haldi Doodh) with honey",
            "Plain steamed rice mixed with fresh homemade curd and mild salt",
            "A warm bowl of simple tomato soup with crispy bread croutons"
        ],
        "time": [
            "Soft, fluffy Idlis served with mild coconut chutney and comforting sambar",
            "Slow-cooked Dal Makhani paired with soft whole-wheat phulkas",
            "Rich vegetable Tehri (spiced yellow rice) loaded with potatoes and peas",
            "Warm Rajma stew simmered with whole spices served over steamed basmati",
            "Sweet and comforting sweet potato & cardamom halwa in desi ghee"
        ],
        "exotic": [
            "Silky Japanese vegetable Miso soup with soft tofu & tender greens",
            "Creamy Italian saffron risotto finished with aged parmesan & butter",
            "Classic French rustic potato and leek soup (Potage Parmentier)",
            "Warm baked Shepard’s Pie with spiced lentils and creamy mashed potato crust",
            "Tibetan comforting vegetable Thukpa with warm ginger-infused broth"
        ]
    },
    "🤷 I Don't Even Know": {
        "easy": [
            "A crisp cold Honeycrisp apple sliced into thin crunchy wedges",
            "A handful of dry roasted cashews and sweet golden raisins",
            "A slice of warm toast with salted butter and a light drizzle of honey",
            "A bowl of fresh sweet pomegranate arils",
            "A warm cup of mild cinnamon-infused water with honey"
        ],
        "time": [
            "Warm semolina (Sooji) toast crisp-grilled with mild herbs and capsicum",
            "A comforting bowl of mild sweet corn vegetable soup",
            "Warm Besan Puda cooked golden with chopped fresh coriander",
            "Classic scrambled eggs or soft paneer tossed in mild butter and toast",
            "Slow-steamed sweet corn cobs brushed with salted butter and lime"
        ],
        "exotic": [
            "Warm Belgian waffle quarter topped with organic maple syrup and berries",
            "Toasted brioche with creamy mascarpone cheese and fig preserve",
            "Warm cinnamon churro bites with non-caffeinated spiced dipping sauce",
            "Coconut sticky rice served with sweet ripe mango slices",
            "Baked camembert bite with a small spoon of cranberry chutney"
        ]
    }
}

VIBE_INFLUENCES = {
    "🍫 “I deserve a treat.”": "Treat mode: indulgence, sweetness, and comfort.",
    "🥺 “I need comfort.”": "Comfort mode: warm, gentle, grounding foods.",
    "😋 “I just WANT IT.”": "Intense craving mode: punchy flavors and instant satisfaction.",
    "😴 “I'm hungry and tired.”": "Effortless mode: 2-minute prep, zero cleanup.",
    "🤷 “Random pregnancy craving.”": "Whimsical mode: unexpected and delightful combinations."
}

def get_craving_recipes(category: str, vibe: str, user_pantry: list):
    """Generates 3 categorized ideas (Quick, Time, Exotic) with desi touches and pantry matching."""
    cat_data = FLAVOR_MATRIX.get(category, FLAVOR_MATRIX["🍫 Sweet"])
    
    # Randomly select one base from each tier for endless variety
    quick_pick = random.choice(cat_data["easy"])
    time_pick = random.choice(cat_data["time"])
    exotic_pick = random.choice(cat_data["exotic"])
    
    # Evaluate pantry matching
    matched_pantry = []
    for item in user_pantry:
        for pick in [quick_pick, time_pick, exotic_pick]:
            if item.lower() in pick.lower() and item not in matched_pantry:
                matched_pantry.append(item)
                
    return {
        "quick": quick_pick,
        "time": time_pick,
        "exotic": exotic_pick,
        "matched_pantry": matched_pantry,
        "vibe_note": VIBE_INFLUENCES.get(vibe, "Custom companion selection.")
    }

def get_surprise_recipe(user_pantry: list):
    """Picks a random category, tier, and food combo based on pantry."""
    cat = random.choice(list(FLAVOR_MATRIX.keys()))
    tier = random.choice(["easy", "time", "exotic"])
    recipe = random.choice(FLAVOR_MATRIX[cat][tier])
    tier_label = "⚡ Quick & Simple" if tier == "easy" else ("⏳ Takes a Little Love" if tier == "time" else "✨ Exotic Twist")
    return {
        "category": cat,
        "tier_label": tier_label,
        "recipe": recipe,
        "summary": "Sweet, simple, and hits the spot perfectly."
    }