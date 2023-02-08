from flask import Flask, request, render_template
import openai
import pymongo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymongo_sqlalchemy
from bson import json_util
import json
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
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
    # text = "get the total number of '_id' from the insurance table"
    text = request.form["text"]
    sql = text_to_sql(text)
    generated_sql = sql.replace('\n', '')

    # Extract the generated SQL from the API response
    print("Generated SQL:", generated_sql)

    # Connect to MongoDB using SQLAlchemy
    engine = create_engine('mongodb://localhost:27017/test')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define the SQL query
    sql_query = generated_sql

    # Convert the SQL query to a MongoDB equivalent
    mongo_query = str(pymongo_sqlalchemy.SQLAlchemyCompiler(
        session.get_bind(), sql_query).compile())

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Mongo']
    collection = db['insurance']

    # Convert the mongo_query string to a dictionary
    mongo_query_dict = json.loads(json_util.dumps(mongo_query))

    # Execute the MongoDB query using the dictionary
    results = collection.find(mongo_query_dict)
    for result in results:
        print(result)

    # Execute the generated SQL
    # cursor = collection.find()
    # cursor = execute_sql(generated_sql, collection)

    # Pass the query result to the result page
    return render_template("result.html", result=results)

    # # Insert the generated SQL into MongoDB
    # insert = collection.insert_one({"generated_sql": generated_sql})

    # # Print the generated SQL result
    # result = collection.find({})

    # for document in result:
    #     print(document)

    # return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run()
