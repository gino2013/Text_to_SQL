import openai
import sqlite3

# Apply for an OpenAI API key and replace the value below with your own key
openai.api_key = "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"


def text_to_sql(text):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"text-to-sql: {text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.8,
    )

    message = completions.choices[0].text
    return message


# text = 'get the total number of ''sex'' from the Insurance table'
text = 'get the average number of ''age'' from the Insurance table'
sql = text_to_sql(text)
generated_sql = sql.replace('\n', '')

# Connect to SQLite database
conn = sqlite3.connect("medical_insurance.db")

cursor = conn.cursor()

# Execute the generated SQL
cursor.execute(generated_sql)
result = cursor.fetchall()

for document in result:
    print(document)
