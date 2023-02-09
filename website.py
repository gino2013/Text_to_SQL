from flask import Flask, request, render_template
import openai
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    try:
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

        text = request.form["text"]
        sql = text_to_sql(text)
        generated_sql = sql.replace('\n', '')

        # Connect to SQLite database
        conn = sqlite3.connect("medical_insurance.db")
        cursor = conn.cursor()

        # Execute the generated SQL
        cursor.execute(generated_sql)
        result = cursor.fetchall()

        # Pass the query result to the result page
        return render_template("index.html", result=result, sql=sql)

    except Exception as e:
        # When error happened, deal with it here
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
