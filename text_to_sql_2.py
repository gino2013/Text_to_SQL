import openai
import pymongo

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


text = "get the total number of '_id' from the insurance table"
sql = text_to_sql(text)
generated_sql = sql.replace('\n', '')

# Extract the generated SQL from the API response
print("Generated SQL:", generated_sql)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Mongo"]
collection = db["insurance"]

# Insert the generated SQL into MongoDB
result = collection.insert_one({"generated_sql": generated_sql})

# Print the generated SQL result
result = collection.find({})

for document in result:
    print(document)
