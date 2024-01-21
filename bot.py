# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer


# bot = ChatBot('Norman')
# trainer = ListTrainer(bot)

# trainer.train([
#     'How are you?',
#     'I am good.',
#     'That is good to hear.',
#     'Thank you',
#     'You are welcome.',
# ])

# import nltk
from nltk.chat import Chat
from nltk.chat.util import reflections

# Define patterns and responses
patterns = [
    (r'Hello|Hi|Hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'How can you help me?', ['I can assist you with interior design ideas, color schemes, furniture selection, and more. Just ask!']),
    (r'(.*) interior design (.*)', ['I can provide advice on interior design trends, color schemes, furniture, lighting, and more. Just let me know what specific area you are interested in.']),
    (r'(.*) color scheme (.*)', ['Choosing the right color scheme is crucial for a great design. Consider the purpose of the space, desired atmosphere, and personal preferences. Warm colors like red and orange create coziness, while cool colors like blue and green promote tranquility.']),
    (r'(.*) furniture (.*)', ['The right furniture can transform a space. Are you looking for advice on a specific room or type of furniture?']),
    (r'(.*) lighting (.*)', ['Proper lighting enhances the atmosphere. Consider natural light, task lighting, and ambient lighting for different areas. What specific area or room do you need lighting ideas for?']),
    (r'(.*) small space (.*)', ['For small spaces, consider multi-functional furniture, light colors, and strategic lighting to create an illusion of space. Do you have a specific small space in mind?']),
    (r'(.*) budget-friendly (.*)', ["Creating a stylish design on a budget is possible! Look for affordable furniture, DIY projects, and consider second-hand items. What's your budget, and do you have any specific preferences?"]),
    (r'(.*) thank you (.*)', ['You\'re welcome!', 'Anytime! If you have more questions or need further assistance, feel free to ask.']),
    (r'quit', ['Goodbye!', 'It was nice chatting with you.']),
]


interior_design_chatbot = Chat(patterns, reflections)

def start_chat():
    print("Hello! I'm your interior design chatbot. How can I assist you today?")
    print("Type 'quit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye!")
            break
        else:
            response = interior_design_chatbot.respond(user_input)
            print("Chatbot:", response)


start_chat()
