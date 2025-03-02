"""import random

R_EATING="I don't like eating anything because I'm a bot obviously"
R_FRIEND="yes for sure. I would be happy to be your friend"
R_SUMIT="Sumit is a handsome boy but little bit naughty."
def unknown():
    response=['could you please re-phrase that?',".....","sounds about right","what does that mean"][random.randrange(4)]
    return response"""
# long_responses.py

def unknown():
    return "I'm not sure I understand. Please try asking about plant diseases like Early Blight or Late Blight, or upload a plant image for analysis."

R_EARLY_BLIGHT = """
Early Blight is a fungal disease caused by Alternaria solani. It appears as dark brown to black lesions with concentric rings on lower leaves first. 

Symptoms include:
- Brown/black spots with concentric rings (target-like pattern)
- Yellow areas surrounding spots
- Lower/older leaves affected first
- Leaf drop in severe cases

Control methods include removing infected leaves, proper spacing for air circulation, and fungicide application.
"""

R_LATE_BLIGHT = """
Late Blight is caused by Phytophthora infestans. It's a serious disease that can rapidly destroy plants in cool, wet conditions.

Symptoms include:
- Water-soaked pale/dark green spots on leaves
- White fuzzy growth on leaf undersides in humid conditions
- Brown/black lesions on stems
- Firm, irregular brown spots on tubers/fruits

Management requires fungicides with protective and systemic activity, removing infected plants, and improving air circulation.
"""

R_HEALTHY_PLANT = """
A healthy plant typically has:
- Vibrant green leaves without spots or unusual discoloration
- Sturdy stems
- Consistent growth pattern
- No wilting or drooping

Continue good gardening practices like proper watering, adequate spacing, and regular monitoring for early signs of disease.
"""

R_PLANT_CARE = """
Good plant care practices to prevent diseases:
- Water at the base of plants, not on foliage
- Provide adequate spacing for air circulation
- Remove and destroy diseased plant parts
- Rotate crops yearly
- Use disease-resistant varieties when available
- Apply appropriate fungicides preventatively in high-risk conditions
- Maintain proper soil fertility
"""

R_SYMPTOMS = """
When identifying plant diseases, look for:
- Leaf spots, blotches, or discoloration
- Unusual growth patterns or stunting
- Wilting despite adequate water
- Powdery or fuzzy growth on plant surfaces
- Cankers or lesions on stems
- Fruit/vegetable discoloration or rot

Upload a clear image of the affected plant part for the most accurate diagnosis.
"""

R_TREATMENTS = """
Treatment approaches for plant diseases:
- Cultural: Remove infected plant parts, improve air circulation
- Chemical: Apply appropriate fungicides (copper-based for organic gardens)
- Biological: Use beneficial microorganisms that combat pathogens
- Preventive: Practice crop rotation, use resistant varieties

For specific treatment recommendations, identify the disease first by uploading a plant image.
"""
# Additional healthy plant responses for long_responses.py

R_HEALTHY_SIGNS = """
Signs of a healthy plant include:
- Vibrant, consistent leaf color (usually medium to dark green)
- Firm, sturdy stems
- New growth at appropriate times
- Consistent leaf size and shape
- Absence of spots, discoloration, or unusual markings
- Strong root system (not visible but indicated by plant stability)
- Flowers/fruits developing according to the plant's normal cycle
- Appropriate height and spread for the plant's age and species

A healthy plant will display vigor and resilience to minor stresses like temporary drought or temperature fluctuations.
"""

R_MAINTAINING_HEALTH = """
To maintain plant health:
- Water consistently and appropriately for the plant type
- Ensure proper light exposure (full sun, partial shade, etc.)
- Fertilize according to plant needs, but don't over-fertilize
- Monitor for pests and diseases regularly
- Prune as needed to remove dead growth and promote air circulation
- Use well-draining soil appropriate for your plant type
- Provide support for tall or climbing plants
- Maintain proper spacing between plants
- Mulch to regulate soil temperature and moisture
- Protect from extreme weather conditions

Regular observation is key - check your plants at least weekly for any changes in appearance.
"""

R_HEALTHY_LEAVES = """
Healthy leaves typically show these characteristics:
- Uniform color appropriate to the plant variety
- Smooth, firm texture (for most plants)
- No curling, puckering, or distortion
- No holes or ragged edges (unless caused by harmless insects)
- Appropriate size for the plant's age and type
- No powdery residue or sticky substances
- No yellowing or browning at tips or edges
- No spots or blotches
- Leaves held firmly on stems, not wilting or drooping

Leaf appearance is one of the best indicators of overall plant health!
"""

R_HEALTHY_GROWTH = """
Healthy growth patterns in plants:
- Steady, consistent growth appropriate to the season
- Symmetrical development (generally)
- New shoots and leaves emerging regularly
- Strong, upright stems that don't bend easily
- Balanced branching
- Root growth visible at appropriate times (for potted plants)
- Flowers and fruit developing on schedule
- Recovery from pruning with new growth
- Resilience after transplanting
- Appropriate response to fertilization

Each plant species has unique growth characteristics, but these general patterns apply to most healthy plants.
"""

R_SOIL_HEALTH = """
Healthy soil for plant growth:
- Good texture: crumbly, not compacted
- Proper drainage: water doesn't pool on surface
- Rich in organic matter
- Appropriate pH for your plants (most garden plants prefer 6.0-7.0)
- Contains beneficial microorganisms
- Holds moisture without becoming waterlogged
- Proper nutrient balance (N-P-K and micronutrients)
- Free from contaminants and excessive salts
- Good aeration for root respiration
- Consistent temperature (mulch helps with this)

Healthy soil is the foundation for healthy plants. Consider testing your soil annually and amending as needed.
"""

R_PREVENTION = """
Prevent plant diseases by:
- Using disease-free seeds and transplants
- Maintaining plant vigor through proper nutrition
- Rotating crops annually
- Providing adequate spacing
- Watering at the base, not on foliage
- Applying preventative fungicides before disease appears
- Removing garden debris at the end of the season
- Using disease-resistant varieties
"""

R_UPLOAD_HELP = """
To analyze your plant:
1. Click the "Choose File" button
2. Select a clear image of the affected plant part
3. Make sure the image is well-lit and focused
4. Click "Analyze Image"
5. Wait for the diagnosis results

The system works best with clear, close-up images of affected leaves or stems.
"""

R_POTATO = """
Potatoes are commonly affected by Early Blight and Late Blight:

Early Blight:
- Dark brown concentric rings on leaves
- Older leaves affected first
- Slow progression

Late Blight:
- Water-soaked lesions that quickly turn brown/black
- White fuzzy growth in humid conditions
- Rapid spread in cool, wet weather
- Can destroy entire crop within days

Upload an image of your potato plant for specific diagnosis.
"""

R_TOMATO = """
Tomatoes are susceptible to both Early Blight and Late Blight:

Early Blight:
- Dark brown spots with concentric rings
- Yellow areas around spots
- Affects older leaves first
- Can cause stem lesions and fruit rot

Late Blight:
- Pale green/brown water-soaked patches
- White fuzzy growth in humid conditions
- Fast-spreading
- Affects stems, leaves, and fruits
- Green-brown lesions on fruits

Upload a clear image of your tomato plant for accurate diagnosis.
"""