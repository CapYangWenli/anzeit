import newspaper
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


ARTICLE_URL = "https://www.zeit.de/politik/2025-01/angela-merkel-friedrich-merz-usa"


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)



article = newspaper.article(ARTICLE_URL)

# print(article.text)
# New England Patriots head coach Bill Belichick, right, embraces Buffalo Bills head coach Sean McDermott ...

print(article.top_image)
# https://media.cnn.com/api/v1/images/stellar/prod/231015223702-06-nfl-season-gallery-1015.jpg?c=16x9&q=w_800,c_fill

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "developer",
            "content": [
                {
                "type": "text",
                "text": """
                    You are a diligent assistant that helps us to simplify german news articles to a level of A2. 
                    We are building a website where people learning german can read current news while learning the language at the same time.
                    We will be sending you news articles.  
                    Your job is to rewrite the article so a person with vocabulary and grammar corresponding to a level of A2 CEFR will be able to read it.
                    Include glossary for words that are not A2 level but are necessary for understanding the article.
                    The glossary should contain the word, english translation, and a simple definition in german.
                    The response must be formatted in markdown.
                    Respond ONLY with the rewritten article and glossary.
                """ 
                }
            ]
        },

        {
            "role": "user",
            "content": article.text,
        }
    ],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message)

# Create markdown file with the article and glossary
with open("article.md", "w") as file:
    file.write(chat_completion.choices[0].message.content)

