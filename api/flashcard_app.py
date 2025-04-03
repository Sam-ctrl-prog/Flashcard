from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)

# Load flashcards from the JSON file
def load_flashcards():
    try:
        with open('flashcards.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"flashcards": [], "results": {"correct": 0, "total": 0}}

# Save flashcards to the JSON file
def save_flashcards(data):
    with open('flashcards.json', 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    data = load_flashcards()
    return render_template('Homepage.html', flashcards=data['flashcards'])

@app.route('/add_flashcard', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        topic = request.form['topic']
        question = request.form['question']
        answer = request.form['answer']
        
        data = load_flashcards()
        data['flashcards'].append({'topic': topic, 'question': question, 'answer': answer})
        save_flashcards(data)
        
        return redirect(url_for('Homepage'))
    
    return render_template('add_flashcard.html')

@app.route('/test_flashcards', methods=['GET', 'POST'])
def test_flashcards():
    data = load_flashcards()
    flashcards = data['flashcard']
    
    if len(flashcards) == 0:
        return redirect(url_for('add_flashcard'))
    
    random_flashcard = random.choice(flashcards)
    
    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = random_flashcard['answer']
        
        if user_answer.strip().lower() == correct_answer.strip().lower():
            data['results']['correct'] += 1
        data['results']['total'] += 1
        save_flashcards(data)
        
        return redirect(url_for('test_flashcards'))
    
    return render_template('test_flashcards.html', flashcard=random_flashcard)

@app.route('/result_flashcard')
def flashcard_results():
    data = load_flashcards()
    correct = data['results']['correct']
    total = data['results']['total']
    accuracy = (correct / total * 100) if total > 0 else 0
    return render_template('result_flashcard.html', correct=correct, total=total, accuracy=accuracy)

if __name__ == '__main__':
    app.run(debug=True)
