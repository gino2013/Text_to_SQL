import openai
from sqlalchemy import create_engine, text

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


def query_database(sql):
    # Connect to your database
    engine = create_engine("sqlite:///dummy.db")

    with engine.connect() as con:
        result = con.execute(text(sql)).fetchall()
    con.close()
    return result


input_text = "get the total number of customers from the customers table"
sql = text_to_sql(input_text)
print(sql)
print("---------------------------")
sql = sql.replace('\n', '')
print("result: ", query_database(sql))
