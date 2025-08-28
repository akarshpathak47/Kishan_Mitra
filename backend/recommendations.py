import json

# --- IMPORTANT: Populate this dictionary with actual agricultural advice ---
# The keys here must EXACTLY match the disease names found in your class_names.json.
DISEASE_RECOMMENDATIONS = {
    "Apple___Apple_scab": {
        "symptoms": "Olive-green to brown spots on leaves and fruit, causing distortion. Lesions darken with age.",
        "prevention": [
            "Prune trees to ensure good air circulation and sunlight penetration.",
            "Sanitize pruning tools after each cut.",
            "Remove and destroy fallen leaves and infected fruit in autumn.",
            "Plant apple varieties known for scab resistance (e.g., Prima, Liberty).",
            "Avoid overhead irrigation to reduce leaf wetness."
        ],
        "treatment_organic": [
            "Apply dormant oil spray in late winter to smother overwintering spores.",
            "Use copper-based fungicides (e.g., Bordeaux mixture) before bud break and during early spring.",
            "Apply sulfur-based fungicides as a preventative measure, especially during wet periods. (Note: Sulfur can burn some varieties/temperatures).",
            "Consider bio-fungicides containing Bacillus subtilis."
        ],
        "treatment_chemical": [
            "Apply fungicides containing captan, mancozeb, or myclobutanil.",
            "Follow spray schedule as per local agricultural guidelines.",
            "Always read and follow product label instructions carefully for application rates, safety, and re-entry intervals."
        ],
        "soil_health_tips": [
            "Ensure well-drained soil; scab thrives in moist conditions.",
            "Maintain balanced soil nutrients to promote tree vigor, making it less susceptible.",
            "Incorporate organic matter to improve soil structure and microbial activity."
        ]
    },
    "Apple___Black_rot": {
        "symptoms": "Dark brown circular lesions on leaves ('frogeye leaf spot'), black mummified fruit, and sunken cankers on branches.",
        "prevention": [
            "Remove and destroy all mummified fruit from the tree and ground.",
            "Prune out dead, diseased, or weakened branches and cankers during dormancy.",
            "Promote good air circulation within the tree canopy.",
            "Avoid wounds to bark and fruit, which can be entry points for the fungus."
        ],
        "treatment_organic": [
            "Apply copper fungicides (organic certified) as a preventative measure.",
            "Use bio-fungicides like Bacillus subtilis containing products."
        ],
        "treatment_chemical": [
            "Apply fungicides like captan, ziram, or myclobutanil.",
            "Timely application is crucial after petal fall."
        ],
        "soil_health_tips": [
            "Maintain overall tree health through proper fertilization and watering to increase disease resistance.",
            "Avoid excessive nitrogen fertilization, which can promote lush growth susceptible to disease."
        ]
    },
    "Apple___Cedar_apple_rust": {
        "symptoms": "Bright orange-yellow spots with small black dots on upper leaf surfaces, developing tube-like structures (aecia) on the underside. Lesions on fruit and twigs.",
        "prevention": [
            "Crucially, remove or control nearby Juniper (cedar) trees, which are alternate hosts for the rust fungus.",
            "Plant rust-resistant apple varieties (e.g., Liberty, Prima, Goldrush).",
            "Ensure proper tree spacing for good air circulation."
        ],
        "treatment_organic": [
            "Apply sulfur-based fungicides in early spring.",
            "Organic copper sprays might offer some protection."
        ],
        "treatment_chemical": [
            "Fungicides containing myclobutanil or propiconazole are effective. Begin applications when orange gelatinous galls appear on junipers and continue until 2-3 weeks after apple petal fall.",
            "Consult local advisories for precise timing based on weather conditions."
        ],
        "soil_health_tips": [
            "Healthy, well-nourished trees are better equipped to resist disease. Ensure balanced soil nutrients."
        ]
    },
    "Apple___healthy": {
        "symptoms": "Vibrant green leaves, uniform color, no visible spots, lesions, deformities, or discolorations. Fruit is firm and healthy.",
        "prevention": [
            "Continue good horticultural practices: regular pruning, proper watering, balanced fertilization.",
            "Regularly inspect trees for any early signs of pests or diseases.",
            "Maintain orchard hygiene by removing plant debris."
        ],
        "treatment_organic": [
            "Focus on soil health with organic compost and mulching.",
            "Promote beneficial insects that can control potential pests naturally."
        ],
        "treatment_chemical": [
            "No treatment needed, focus on preventive care."
        ],
        "soil_health_tips": [
            "Conduct regular soil tests to monitor nutrient levels and pH.",
            "Implement crop rotation (if in an orchard setting with annual intercropping).",
            "Ensure good drainage and aeration to prevent root issues."
        ]
    },
    "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot": {
        "symptoms": "Long, narrow, rectangular gray-brown lesions that develop between leaf veins, often surrounded by a yellow halo.",
        "prevention": [
            "Plant resistant corn varieties.",
            "Implement crop rotation (at least 2 years) with non-host crops (e.g., soybean, wheat).",
            "Manage corn residue through tillage or by promoting rapid decomposition to reduce fungal inoculum.",
            "Ensure proper plant spacing for air circulation."
        ],
        "treatment_organic": [
            "No highly effective organic fungicide specific to this disease. Focus heavily on cultural practices."
        ],
        "treatment_chemical": [
            "Apply strobilurin or triazole fungicides when symptoms first appear, or as a preventive measure in high-risk areas."
        ],
        "soil_health_tips": [
            "Improve soil organic matter to enhance plant vigor and resilience.",
            "Balanced nutrient management, especially avoiding excessive nitrogen, can help."
        ]
    },
    "Corn_(maize)___Common_rust": {
        "symptoms": "Small, circular to oval, reddish-brown pustules on both upper and lower leaf surfaces, rupturing to release powdery spores.",
        "prevention": [
            "Plant rust-resistant corn hybrids.",
            "No specific cultural practices effectively control rust once it develops, focus on genetics."
        ],
        "treatment_organic": [
            "Some copper-based fungicides can offer limited protection, but generally not very effective for rust on corn."
        ],
        "treatment_chemical": [
            "Foliar fungicides (e.g., strobilurins, triazoles, or mixtures) can provide control if applied early at the onset of symptoms or as a preventive measure during susceptible growth stages (e.g., tasseling).",
            "Economic thresholds for spraying are often used."
        ],
        "soil_health_tips": [
            "Healthy soil leads to strong plants, which can better withstand minor disease pressure."
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "symptoms": "Long, elliptical, gray-green to tan lesions on leaves, resembling cigar-shaped spots.",
        "prevention": [
            "Plant resistant corn hybrids.",
            "Rotate crops with non-host plants.",
            "Manage corn residue to reduce inoculum."
        ],
        "treatment_organic": [
            "Cultural practices are key, as organic fungicides are not very effective."
        ],
        "treatment_chemical": [
            "Apply fungicides (e.g., strobilurins, triazoles) at the onset of symptoms or when disease pressure is high."
        ],
        "soil_health_tips": [
            "Maintain good soil drainage and structure."
        ]
    },
    "Corn_(maize)___healthy": {
        "symptoms": "Vibrant green leaves, strong stalks, healthy ear development. No visible lesions, discoloration, or deformities.",
        "prevention": [
            "Continue optimal growing practices: proper planting density, irrigation, and nutrient management.",
            "Regular scouting for pests or disease."
        ],
        "treatment_organic": [
            "Focus on building healthy soil with organic amendments and cover cropping."
        ],
        "treatment_chemical": [
            "No treatment needed."
        ],
        "soil_health_tips": [
            "Perform regular soil tests and adjust nutrient applications.",
            "Practice minimum tillage to preserve soil structure."
        ]
    },
    "Potato___Early_blight": {
        "symptoms": "Dark brown to black concentric spots (target-like rings) on older leaves, leading to defoliation.",
        "prevention": [
            "Plant resistant potato varieties.",
            "Ensure balanced fertilization, avoiding excessive nitrogen.",
            "Rotate crops with non-solanaceous crops.",
            "Avoid overhead irrigation, or irrigate early in the day so foliage can dry."
        ],
        "treatment_organic": [
            "Apply copper-based fungicides.",
            "Bio-fungicides like Bacillus amyloliquefaciens."
        ],
        "treatment_chemical": [
            "Apply chlorothalonil, mancozeb, or strobilurin fungicides.",
            "Begin sprays at early disease onset or preventatively under favorable conditions."
        ],
        "soil_health_tips": [
            "Ensure good soil drainage.",
            "Maintain adequate potassium levels in the soil, as potassium deficiency can increase susceptibility."
        ]
    },
    "Potato___Late_blight": {
        "symptoms": "Water-soaked lesions on leaves and stems that rapidly enlarge, turning brown/black, often with a white fuzzy growth on the underside. Causes potato rot.",
        "prevention": [
            "Plant certified disease-free seed potatoes.",
            "Eliminate volunteer potato plants.",
            "Ensure proper hilling to cover tubers and prevent spore contact.",
            "Avoid overhead irrigation, or irrigate during dry periods so foliage dries quickly.",
            "Choose resistant potato varieties."
        ],
        "treatment_organic": [
            "Apply copper-based fungicides as a preventative and early curative measure.",
            "Bio-fungicides like those based on Bacillus subtilis."
        ],
        "treatment_chemical": [
            "Highly effective systemic fungicides (e.g., propamocarb, dimethomorph, fluazinam) are often necessary. Rotate chemistries to manage resistance.",
            "Start preventive sprays when weather conditions favor disease development."
        ],
        "soil_health_tips": [
            "Good soil drainage is essential to prevent waterlogged conditions that favor the pathogen."
        ]
    },
    "Potato___healthy": {
        "symptoms": "Vigorous green foliage, healthy stems, no visible spots, lesions, or wilting. Tubers are firm and free from blemishes.",
        "prevention": [
            "Continue good cultural practices: proper spacing, timely watering, and balanced fertilization.",
            "Regular scouting for early signs of issues."
        ],
        "treatment_organic": [
            "Focus on enriching soil with organic matter and promoting beneficial soil microbes."
        ],
        "treatment_chemical": [
            "No treatment needed."
        ],
        "soil_health_tips": [
            "Maintain optimal soil pH (5.0-6.0) for potato growth.",
            "Ensure adequate calcium in the soil for tuber quality and disease resistance."
        ]
    },
    "Tomato___Bacterial_spot": {
        "symptoms": "Small, dark, water-soaked spots on leaves that become angular with yellow halos. Spots on fruit are dark, slightly raised, and scabby.",
        "prevention": [
            "Use certified disease-free seeds or transplants.",
            "Avoid overhead irrigation; use drip irrigation.",
            "Prune lower leaves to improve air circulation and reduce splash dispersal.",
            "Sanitize tools and stakes.",
            "Rotate crops with non-solanaceous plants for at least two years."
        ],
        "treatment_organic": [
            "Apply copper-based sprays (organic certified). Repeated applications may be necessary.",
            "Consider bio-pesticides containing Bacillus amyloliquefaciens."
        ],
        "treatment_chemical": [
            "Sprays containing copper and mancozeb (or streptoMycin in specific cases, check regulations) can help. Note: Bacterial spot can develop resistance to copper.",
            "Apply when conditions favor disease development."
        ],
        "soil_health_tips": [
            "Healthy soil promotes stronger plants more resilient to bacterial infections.",
            "Good drainage prevents waterlogging that can spread bacteria."
        ]
    },
    "Tomato___Early_blight": {
        "symptoms": "Dark brown to black spots with concentric rings (target-like) on older leaves. Can also affect stems and fruit.",
        "prevention": [
            "Practice good sanitation: remove infected plant debris.",
            "Ensure proper plant spacing and staking for air circulation.",
            "Rotate crops with non-host plants.",
            "Avoid prolonged leaf wetness by watering at the base of plants."
        ],
        "treatment_organic": [
            "Apply copper-based fungicides or bio-fungicides (e.g., Bacillus subtilis) preventatively."
        ],
        "treatment_chemical": [
            "Fungicides like chlorothalonil or mancozeb can be used. Apply at first sign of disease or preventatively."
        ],
        "soil_health_tips": [
            "Maintain balanced soil fertility, especially adequate phosphorus and potassium.",
            "Good soil drainage is important."
        ]
    },
    "Tomato___Late_blight": {
        "symptoms": "Large, irregular, water-soaked lesions on leaves and stems that turn brown/black. Often has a fuzzy white mold growth on the underside in humid conditions. Rapidly causes fruit rot.",
        "prevention": [
            "Use certified disease-free seeds/transplants.",
            "Eliminate volunteer potato and tomato plants (alternate hosts).",
            "Ensure good air circulation, prune lower leaves.",
            "Avoid overhead irrigation, especially in humid conditions.",
            "Plant resistant varieties if available."
        ],
        "treatment_organic": [
            "Apply copper-based fungicides preventatively and regularly during favorable conditions (cool, wet weather)."
        ],
        "treatment_chemical": [
            "Fast-acting systemic fungicides (e.g., those containing propamocarb, dimethomorph, fluazinam) are highly effective and often critical for control. Rotate chemistries to manage resistance."
        ],
        "soil_health_tips": [
            "Ensure well-drained soil; wet conditions exacerbate late blight."
        ]
    },
    "Tomato___Leaf_Mold": {
        "symptoms": "Yellowish spots on upper leaf surface, followed by olive-green to brown velvety fungal growth on the underside.",
        "prevention": [
            "Improve air circulation through proper spacing and pruning.",
            "Ventilate greenhouses well.",
            "Avoid overhead watering."
        ],
        "treatment_organic": [
            "Copper-based sprays or bio-fungicides can provide some control."
        ],
        "treatment_chemical": [
            "Fungicides like chlorothalonil or mancozeb can be used preventatively."
        ],
        "soil_health_tips": [
            "Good soil structure and drainage."
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "symptoms": "Numerous small, circular spots with dark brown margins and gray or tan centers, often with tiny black specks (pycnidia) in the center. Primarily affects older leaves.",
        "prevention": [
            "Remove and destroy infected lower leaves and plant debris.",
            "Rotate crops with non-solanaceous plants.",
            "Avoid overhead watering and splashing soil onto leaves.",
            "Use stakes or cages to keep plants off the ground."
        ],
        "treatment_organic": [
            "Apply copper-based fungicides."
        ],
        "treatment_chemical": [
            "Fungicides like chlorothalonil or mancozeb can be used. Start applications at the first sign of disease."
        ],
        "soil_health_tips": [
            "Maintain good soil hygiene."
        ]
    },
    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "symptoms": "Stippling (tiny white or yellow dots) on leaves, bronze discoloration, fine webbing on the underside of leaves and stems. Leaves may turn yellow and drop.",
        "prevention": [
            "Regularly scout for mites, especially in hot, dry conditions.",
            "Maintain plant vigor with proper watering and nutrition.",
            "Use strong sprays of water to dislodge mites (especially on leaf undersides)."
        ],
        "treatment_organic": [
            "Apply neem oil or insecticidal soaps. Repeat applications are often necessary.",
            "Introduce beneficial predatory mites (e.g., Phytoseiulus persimilis) if feasible.",
            "Garlic spray."
        ],
        "treatment_chemical": [
            "Apply miticides (acaricides) specifically designed for mites. Rotate chemistries to prevent resistance.",
            "Examples: abamectin, bifenthrin. Always follow label directions.",
            "Target the underside of leaves."
        ],
        "soil_health_tips": [
            "Healthy soil promotes robust plants that are less susceptible to mite infestations."
        ]
    },
    "Tomato___Target_Spot": {
        "symptoms": "Small, circular, dark brown spots on leaves, stems, and fruit. On leaves, they often have a yellow halo and may develop concentric rings.",
        "prevention": [
            "Rotate crops.",
            "Manage plant debris.",
            "Improve air circulation by proper spacing and pruning.",
            "Avoid overhead irrigation."
        ],
        "treatment_organic": [
            "Copper-based fungicides can offer some protection."
        ],
        "treatment_chemical": [
            "Fungicides containing chlorothalonil or strobilurins."
        ],
        "soil_health_tips": [
            "Ensure good soil drainage."
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "symptoms": "Mosaic patterns (alternating light and dark green areas) on leaves, leaf distortion (e.g., 'fern leaf'), stunting, and reduced fruit set/quality.",
        "prevention": [
            "Use certified virus-free seeds/transplants.",
            "Practice good hygiene: wash hands, sanitize tools.",
            "Remove and destroy infected plants immediately.",
            "Control insect vectors (like aphids) if they are known to transmit the virus (less common for ToMV).",
            "Avoid handling tobacco products before handling plants."
        ],
        "treatment_organic": [
            "No direct organic cure. Focus entirely on prevention and removal of infected plants."
        ],
        "treatment_chemical": [
            "No chemical cure. Focus on prevention and vector control if applicable."
        ],
        "soil_health_tips": [
            "Soil health does not directly prevent viral infections, but healthy plants may be more resilient to secondary stresses."
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "symptoms": "Leaves become small, thick, and leathery, curl upwards and inwards, and turn yellow between the veins. Plants are severely stunted, and flowers may not produce fruit.",
        "prevention": [
            "Use certified virus-free transplants.",
            "Crucially, control whiteflies, which are the primary vector. Use sticky traps, reflective mulches, or insecticides targeting whiteflies.",
            "Use netting or row covers to exclude whiteflies.",
            "Remove and destroy infected plants promptly."
        ],
        "treatment_organic": [
            "No direct organic cure. Focus on whitefly control with neem oil, insecticidal soaps, or releasing beneficial insects (e.g., predatory wasps).",
            "Use reflective mulches."
        ],
        "treatment_chemical": [
            "No direct chemical cure for the virus. Use insecticides to manage whitefly populations effectively. Rotate insecticide classes to prevent resistance.",
            "Systemic insecticides can be used for persistent whitefly control."
        ],
        "soil_health_tips": [
            "Good soil health indirectly supports plant vigor, which might help plants tolerate minor stress from early infections, but primary focus must be on vector control."
        ]
    },
    "Tomato___healthy": {
        "symptoms": "Leaves are uniformly green, firm, and free from spots, discoloration, or deformities. Stems are sturdy, and fruit development is normal.",
        "prevention": [
            "Maintain optimal watering and fertilization schedules.",
            "Ensure good air circulation around plants.",
            "Regularly scout for any signs of pests or diseases to allow for early intervention."
        ],
        "treatment_organic": [
            "Continue enriching soil with compost and other organic matter.",
            "Promote biodiversity to support natural pest control."
        ],
        "treatment_chemical": [
            "No treatment needed. Focus on proactive care."
        ],
        "soil_health_tips": [
            "Conduct soil tests periodically to ensure nutrient balance and appropriate pH.",
            "Practice crop rotation to prevent soil-borne disease buildup and improve nutrient cycling."
        ]
    },
    "Unknown Disease/Class Index Not Found": {
        "symptoms": "The AI could not confidently identify the specific disease or pest. Symptoms may include general wilting, discoloration, spots, or abnormal growth.",
        "prevention": [
            "Isolate the affected plant if possible to prevent spread.",
            "Ensure proper plant care (watering, light, nutrients).",
            "Regularly inspect other plants for similar symptoms.",
            "Clean gardening tools after use."
        ],
        "treatment_organic": [
            "Apply general organic pest and disease control measures like neem oil or insecticidal soap, but test on a small area first.",
            "Improve air circulation around plants."
        ],
        "treatment_chemical": [
            "Do NOT apply broad-spectrum chemicals without proper identification. This can harm beneficial insects and the environment.",
            "Consult with a local agricultural expert or extension officer for professional diagnosis and targeted treatment recommendations."
        ],
        "soil_health_tips": [
            "Check soil for drainage issues and nutrient deficiencies.",
            "Consider a soil test to understand its composition and pH.",
            "Ensure balanced fertilization according to crop needs."
        ]
    }
}

def get_recommendations(disease_name):
    """
    Retrieves recommendations for a given disease name.
    Provides a generic fallback if the disease name is not found.
    """
    return DISEASE_RECOMMENDATIONS.get(disease_name, DISEASE_RECOMMENDATIONS["Unknown Disease/Class Index Not Found"])

if __name__ == '__main__':
    print("--- Testing Recommendation Logic ---")
    disease_example = "Apple___Black_rot"
    recs_example = get_recommendations(disease_example)
    print(f"\nRecommendations for '{disease_example}':")
    print(json.dumps(recs_example, indent=4, ensure_ascii=False))

    disease_unknown_example = "Some_New_Disease_Not_In_Our_List"
    recs_unknown_example = get_recommendations(disease_unknown_example)
    print(f"\nRecommendations for '{disease_unknown_example}' (Fallback):")
    print(json.dumps(recs_unknown_example, indent=4, ensure_ascii=False))
    print("--- Recommendation Logic Test Complete ---")