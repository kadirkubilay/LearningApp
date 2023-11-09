from flask import Flask, render_template, request, redirect, url_for, session
import openai



# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'KADOKUBIERDEM'

# Configuration for OpenAI GPT-3 API
openai.api_key = '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'

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
        prompt = f"Given the module: '{module}' and article: '{article}', generate a question."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200
        )
        question = response['choices'][0]['message']['content'].strip()
        session['question'] = question
        return render_template('result.html', question=question)
    return render_template('medium.html')

@app.route('/result', methods=['POST','GET'])
def result():
    answer = request.form.get('answer')
    question = session.get('question', 'No question available')
    evaluation_prompt = (f"\n\n--RatingStart--\nRate the answer: '{answer}' for question '{question}' based on the article: '{article}' from  1 to 5 stars "
                     f"\n--RatingEnd--\n"
                     f"--SuggestionStart--\nSuggest a better answer than '{answer}' for question: '{question}' based on the article :{article}. "
                     f"\n--SuggestionEnd--")
    response = openai.Completion.create(
        model="davinci",
        prompt=evaluation_prompt,
        temperature=0.2,
        max_tokens=400
    )
    response_text = response['choices'][0]['text'].strip()


    # Extract rating
    rating_start = response_text.find("--RatingStart--") + len("--RatingStart--")
    rating_end = response_text.find("--RatingEnd--")
    rating = response_text[rating_start:rating_end].replace("Rating (1 to 5 stars):", "").strip()
    print(rating)

    # Extract suggestion
    suggestion_start = response_text.find("--SuggestionStart--") + len("--SuggestionStart--")
    suggestion_end = response_text.find("--SuggestionEnd--")
    suggestions = response_text[suggestion_start:suggestion_end].strip()

    return redirect(url_for('result'))

@app.route('/ranking1', methods=['GET', 'POST'])
def ranking1():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "Ask me another question from this module":
            return redirect(url_for('medium'))
        elif action == "Go back to the curriculum":
            return redirect(url_for('index'))
    return render_template('ranking1.html')



if __name__ == "__main__":
    app.run(debug=True)





