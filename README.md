EDUSATHI AI
An Adaptive Multimodal AI Learning Companion for Accessible Education

PROJECT OVERVIEW
EduSathi AI is an AI-powered educational learning companion designed to help students learn, practice, and improve their academic performance. It uses Ollama and the Llama 3.2 local AI model to provide an interactive and personalized learning experience.

MAIN FEATURES

1. AI Tutor

* ChatGPT-style academic conversation
* Answers student questions
* Provides simple explanations
* Gives step-by-step solutions
* Supports follow-up questions
* Provides exam-oriented answers

2. PDF Study Assistant

* Upload study notes and PDF documents
* Extract text from PDF files
* Ask questions about uploaded study material
* Generate summaries
* Generate important exam points

3. AI Quiz Generator

* Generate topic-based multiple-choice questions
* Select difficulty level
* Automatically evaluate answers
* Display score and correct answers
* Provide explanations for answers

4. Aptitude Test

* Quantitative Aptitude
* Logical Reasoning
* Verbal Ability
* AI-generated practice questions
* Automatic scoring and explanations

5. Student Dashboard

* View learning activity
* View quiz scores
* View aptitude scores
* Monitor learning progress

6. Adaptive Study Recommendations

* Analyzes recent performance
* Identifies areas that need improvement
* Provides personalized study suggestions

TECHNOLOGIES USED

* Python
* Streamlit
* Ollama
* Llama 3.2
* PyPDF2
* Pandas
* NumPy
* Matplotlib

PROJECT STRUCTURE

EduSathi_AI/
│
├── app.py
├── requirements.txt
└── README.txt

INSTALLATION

1. Install Python 3.10 or newer.

2. Install Ollama.

3. Open Command Prompt inside the EduSathi_AI folder.

4. Create a virtual environment:

python -m venv venv

5. Activate the virtual environment:

venv\Scripts\activate

6. Install the required packages:

pip install -r requirements.txt

7. Download the Llama 3.2 model:

ollama pull llama3.2:latest

RUN THE PROJECT

1. Activate the virtual environment:

venv\Scripts\activate

2. Start the Streamlit application:

streamlit run app.py

3. Open the URL displayed in the terminal, usually:

http://localhost:8501

REQUIREMENTS

* Windows computer
* Python 3.10 or newer
* Ollama
* Llama 3.2 model
* Internet connection for initial package/model installation

NOTE

EduSathi AI uses a local Llama 3.2 model through Ollama for AI features. The application does not require an OpenAI or Gemini API key.

PROJECT PURPOSE

The main purpose of EduSathi AI is to provide students with an accessible and personalized AI learning companion that supports academic question answering, document-based learning, quiz practice, aptitude preparation, and performance-based study recommendations.
