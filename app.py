from flask import Flask, render_template, request, redirect, url_for, session
import openai
import random
import os


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'KADOKUBIERDEM-test'

print("Setting API Key")
test = os.environ["TEST_KEY"]
openai.api_key = os.environ["OPENAI_API"]

# Article content
article = """
Business Applications of Machine Learning

In today's digital age, machine learning (ML) has swiftly infiltrated various business sectors, transforming traditional methodologies and offering unprecedented opportunities. This technological revolution, characterized by algorithms that improve through experience, has empowered organizations to streamline operations, enhance user experience, and generate insights from vast data silos. Here, we delve into how some of the world's most recognized businesses integrate machine learning and the diverse applications driving their success.


1. Core Business Models: A Glimpse into Netflix and Google

Netflix: At the heart of Netflix's success is its ability to understand user preferences. The streaming giant leverages advanced machine learning algorithms to analyze viewing patterns and subsequently offer tailored recommendations. By grouping movies and series into clusters based on similarity, Netflix ensures that users always find content aligned with their tastes. Moreover, ML aids in optimizing streaming quality based on a user's internet connection, providing a seamless viewing experience.

Google: Google's prowess in search and advertising can be attributed significantly to its robust machine learning models. The search algorithms continually refine themselves by analyzing billions of search queries, ensuring that users get the most relevant results. Beyond search, Google Photos employs ML for image recognition, enabling users to search their photo library using natural language queries. Moreover, Google's ad system utilizes machine learning to predict click-through rates, ensuring ads are targeted more effectively.


2. Different ways companies are integrating machine learning.

Machine learning's adaptability means that it can be molded to fit a plethora of business needs. Here are some ways companies are integrating it:

Recommendation Systems: Beyond Netflix, e-commerce giants like Amazon and Alibaba use ML-driven recommendation systems. By analyzing user behavior, purchase histories, and browsing patterns, these systems curate product suggestions, significantly enhancing the shopping experience and boosting sales.

Image Analysis: Retailers are employing image analysis to optimize inventory management and checkout processes. Machine learning models can identify products, assess their condition, and even predict trends based on historical sales data.

Fraud Detection: Financial institutions are at the forefront of integrating ML for security. Algorithms can detect unusual transaction patterns, flagging potentially fraudulent activities in real-time. This not only protects consumers but also saves institutions from substantial financial losses.

Chatbots and Virtual Assistants: From customer support to sales, chatbots powered by machine learning offer 24/7 service, efficiently handling queries and complaints. These virtual assistants are continuously evolving, learning from each interaction to improve future engagements.

Self-driving Cars: Automotive giants like Tesla and Waymo use machine learning for their autonomous vehicles. Advanced algorithms process data from vehicle sensors in real-time, making split-second decisions that can prevent accidents and navigate the car safely.

Medical Diagnostics: The healthcare sector is undergoing a machine learning revolution. From predicting patient deterioration to analyzing medical images for early disease detection, ML models are supporting clinicians in delivering more accurate and timely care.
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        curriculum_choice = request.form.get('curriculum')
        if curriculum_choice == "Machine Learning by TUM":
            return redirect(url_for('medium'))
    return render_template('index.html')




@app.route('/medium', methods=['GET', 'POST'])
def medium():
    if request.method == 'POST':
        module = request.form.get('module')


        variations = [
            "What is an intriguing question about",
            "Can you come up with a challenging question concerning",
            "I'd like to ask a thought-provoking question regarding",
        ]


        prompt_variation = random.choice(variations)

        # Form the complete prompt using the chosen variation
        prompt = f"{prompt_variation} the module: '{module}' and article: '{article}'?"


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,  # Use a higher temperature for more varied output
            max_tokens=200
        )


        question = response['choices'][0]['message']['content'].strip()


        session['question'] = question


        return render_template('result.html', question=question)


    return render_template('medium.html', message=test)


@app.route('/result', methods=['POST', 'GET'])
def result():
    answer = request.form.get('answer')
    question = session.get('question', 'No question available')

    # Further Revised Rating Prompt with Specific Instruction
    rating_prompt = (f"Assuming the role of a strict and detail-oriented examiner, evaluate the answer '{answer}' "
                     f"to the question '{question}'. Assess if the answer specifically and accurately addresses the "
                     f"question, considering the information in the article '{article}'. Assign a rating from 1 to 5 stars, "
                     f"where 1 star means the answer is brief, vague, or incomplete, and 5 stars means it is highly "
                     f"relevant, accurate, and complete. Give the star rating in the beginning of your response")
    rating_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": rating_prompt}],
        temperature=0.7,
        max_tokens=150
    )
    rating = rating_response['choices'][0]['message']['content'].strip()

    # Suggestion Prompt remains the same
    suggestion_prompt = f"Suggest a better answer than '{answer}' for the question '{question}' based on the article '{article}'."
    suggestion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": suggestion_prompt}],
        temperature=0.1,
        max_tokens=150
    )
    suggestion = suggestion_response['choices'][0]['message']['content'].strip()

    return render_template("ranking.html", answer=answer, rating=rating, suggestions=suggestion)


if __name__ == "__main__":
    app.run(debug=True)





