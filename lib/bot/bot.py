
from lib.bot.data import QASystem
# from data import QA_data


def chatbot(input):
    # First try to get a response from the QASystem
    # Initialize the QASystem
  
   # qa = QASystem('https://docs.google.com/spreadsheets/d/e/2PACX-1vTnLjDvKnVVqQfVA7QGhXXdV8Eo7fOFc_dYp4HMfqSzcTdYuSJI4GccuxeaBgzGtH7m1M9GfLZkzFST/pub?gid=2008373479&single=true&output=csv')
    # print(qa)
    qa = QASystem("lib/bot/docberg_qa.csv")
    
    try:

        qa_response = qa.get_response(input)
        print("Try")
    except:
        qa_response = "I can't answer this question."
        print("Except")
        # Save the question and the AI's response to the CSV file
       #df = pd.DataFrame([['"' + input + '"', '"' + reply + '"']], columns=['Questions'])
       #df.to_csv('bank.csv', mode='a', header=False, index=False)

    return qa_response