from flask import Flask, render_template, request, jsonify
import re
import long_responses as long

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    return int(percentage * 100) if has_required_words or single_response else 0


def check_all_messages(message):
    highest_prob_list = {}

    """def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Yes, I can be your friend!', ['can', 'you', 'be', 'my', 'friend'], required_words=['friend', 'my'])

    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(long.R_FRIEND, ['will', 'you', 'be', 'my', 'friend'], required_words=['you', 'friend', 'my'])
    response(long.R_SUMIT, ['who','is','Sumit'],required_words=['Sumit','who','is'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match"""

    """def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Basic greeting responses
    response('Hello! I am your Plant Health Assistant. Upload a plant image or ask me about plant diseases.',
             ['hello', 'hi', 'hey', 'greetings'], single_response=True)
    response('Goodbye! Feel free to return if you need help with plant disease diagnosis.',
             ['bye', 'goodbye', 'see', 'you'], single_response=True)
    response('I\'m ready to help with your plant health questions!',
             ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome! Happy gardening!',
             ['thank', 'thanks'], single_response=True)

    # Plant disease specific responses
    response(long.R_EARLY_BLIGHT,
             ['early', 'blight', 'disease', 'spot', 'leaves'], required_words=['early', 'blight'])
    response(long.R_LATE_BLIGHT,
             ['late', 'blight', 'disease', 'spot', 'leaves'], required_words=['late', 'blight'])
    response(long.R_HEALTHY_PLANT,
             ['healthy', 'good', 'plant', 'normal'], required_words=['healthy'])
    response(long.R_PLANT_CARE,
             ['care', 'water', 'fertilize', 'sunlight', 'how', 'grow'], required_words=['care'])
    response(long.R_SYMPTOMS,
             ['symptoms', 'signs', 'look', 'like', 'identify'], required_words=['symptoms'])
    response(long.R_TREATMENTS,
             ['treatment', 'treat', 'cure', 'spray', 'fix', 'solution'], required_words=['treat'])
    response(long.R_PREVENTION,
             ['prevent', 'avoid', 'stop', 'protect'], required_words=['prevent','how','plants','we'])
    response(long.R_UPLOAD_HELP,
             ['upload', 'image', 'picture', 'photo', 'scan'], required_words=['upload'])
    response(long.R_POTATO,
             ['potato', 'potatoes', 'crop'], required_words=['potato'])
    response(long.R_TOMATO,
             ['tomato', 'tomatoes', 'crop'], required_words=['tomato'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match"""

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Basic greeting responses
    response('Hello! I am your Plant Health Assistant. Upload a plant image or ask me about plant diseases.',
             ['hello', 'hi', 'hey', 'greetings'], single_response=True)
    response('Goodbye! Feel free to return if you need help with plant disease diagnosis.',
             ['bye', 'goodbye', 'see', 'you'], single_response=True)
    response('I\'m ready to help with your plant health questions!',
             ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome! Happy gardening!',
             ['thank', 'thanks'], single_response=True)

    # Plant disease specific responses
    response(long.R_EARLY_BLIGHT,
             ['early', 'blight', 'disease', 'spot', 'leaves'], required_words=['early', 'blight'])
    response(long.R_LATE_BLIGHT,
             ['late', 'blight', 'disease', 'spot', 'leaves'], required_words=['late', 'blight'])

    # Healthy plant responses
    response(long.R_HEALTHY_PLANT,
             ['healthy', 'good', 'plant', 'normal'], required_words=['healthy'])
    response(long.R_HEALTHY_SIGNS,
             ['signs', 'indicators', 'healthy', 'plant', 'look'], required_words=['signs', 'healthy'])
    response(long.R_MAINTAINING_HEALTH,
             ['maintain', 'keep', 'healthy', 'plant'], required_words=['maintain', 'healthy'])
    response(long.R_HEALTHY_LEAVES,
             ['healthy', 'leaves', 'look', 'like'], required_words=['healthy', 'leaves'])
    response(long.R_HEALTHY_GROWTH,
             ['healthy', 'growth', 'pattern', 'normal'], required_words=['healthy', 'growth'])
    response(long.R_SOIL_HEALTH,
             ['soil', 'healthy', 'good', 'plant'], required_words=['soil', 'healthy'])

    # General plant care responses
    response(long.R_PLANT_CARE,
             ['care', 'water', 'fertilize', 'sunlight', 'how', 'grow'], required_words=['care'])
    response(long.R_SYMPTOMS,
             ['symptoms', 'signs', 'look', 'like', 'identify'], required_words=['symptoms'])
    response(long.R_TREATMENTS,
             ['treatment', 'treat', 'cure', 'spray', 'fix', 'solution'], required_words=['treat'])
    response(long.R_PREVENTION,
             ['prevent', 'avoid', 'stop', 'protect'], required_words=['prevent'])
    response(long.R_UPLOAD_HELP,
             ['upload', 'image', 'picture', 'photo', 'scan'], required_words=['upload'])
    response(long.R_POTATO,
             ['potato', 'potatoes', 'crop'], required_words=['potato'])
    response(long.R_TOMATO,
             ['tomato', 'tomatoes', 'crop'], required_words=['tomato'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    return check_all_messages(split_message)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["GET", "POST"])
def chatbot_response():
    user_text = request.form["msg"]
    response_text = get_response(user_text)
    return jsonify({"response": response_text})

#
# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
