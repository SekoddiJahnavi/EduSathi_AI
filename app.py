from datetime import date, timedelta
import random
import ollama
import PyPDF2
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG & SESSION STATE
# ---------------------------------------------------------
st.set_page_config(page_title="EduSathi AI", page_icon="🎓", layout="wide")

defaults = {
    "page": "🔐 Login",
    "logged_in": False,
    "user_name": "",
    "study_text": "",
    "questions_answered": 0,
    "correct_answers": 0,
    "quizzes_completed": 0,
    "quiz_questions": [],
    "quiz_submitted": False,
    "last_score": 0,
    "last_total": 0,
    "study_plan": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ---------------------------------------------------------
# AI FUNCTION
# ---------------------------------------------------------
def ask_ollama(prompt):
    try:
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"


# ---------------------------------------------------------
# QUIZ QUESTION BANK
# ---------------------------------------------------------
QUIZ_BANK = {
    "python": [
        {
            "question": (
                "Which keyword is used to define a function in Python?"
            ),
            "options": ["A) function", "B) define", "C) def", "D) func"],
            "answer": "C",
        },
        {
            "question": (
                "Which data type is used to store whole numbers in Python?"
            ),
            "options": ["A) float", "B) int", "C) string", "D) bool"],
            "answer": "B",
        },
        {
            "question": "Which symbol is used to write a comment in Python?",
            "options": ["A) //", "B) <!--", "C) #", "D) **"],
            "answer": "C",
        },
        {
            "question": "Which collection stores data using key-value pairs?",
            "options": ["A) List", "B) Tuple", "C) Set", "D) Dictionary"],
            "answer": "D",
        },
        {
            "question": "Which function is used to display output in Python?",
            "options": ["A) display()", "B) output()", "C) print()", "D) show()"],
            "answer": "C",
        },
        {
            "question": "Which symbol is used to create a list in Python?",
            "options": ["A) {}", "B) []", "C) ()", "D) <>"],
            "answer": "B",
        },
        {
            "question": "Which keyword is used for a conditional statement?",
            "options": ["A) if", "B) when", "C) check", "D) condition"],
            "answer": "A",
        },
        {
            "question": (
                "Which loop is commonly used to iterate over a sequence?"
            ),
            "options": ["A) repeat", "B) foreach", "C) for", "D) iterate"],
            "answer": "C",
        },
    ],
    "statistics": [
        {
            "question": "What is the average of 10, 20 and 30?",
            "options": ["A) 10", "B) 15", "C) 20", "D) 30"],
            "answer": "C",
        },
        {
            "question": (
                "What is the middle value of an ordered dataset called?"
            ),
            "options": ["A) Mean", "B) Median", "C) Mode", "D) Range"],
            "answer": "B",
        },
        {
            "question": "Which measure describes the spread of data?",
            "options": ["A) Variance", "B) Mean", "C) Median", "D) Mode"],
            "answer": "A",
        },
        {
            "question": "What is the most frequently occurring value called?",
            "options": ["A) Mean", "B) Median", "C) Mode", "D) Variance"],
            "answer": "C",
        },
        {
            "question": "The probability of an event always lies between:",
            "options": ["A) -1 and 1", "B) 0 and 1", "C) 1 and 10", "D) 0 and 100"],
            "answer": "B",
        },
        {
            "question": (
                "If a coin is tossed once, what is the probability of getting"
                " heads?"
            ),
            "options": ["A) 0", "B) 1/4", "C) 1/2", "D) 1"],
            "answer": "C",
        },
        {
            "question": (
                "Which graph is commonly used to display the distribution of"
                " numerical data?"
            ),
            "options": [
                "A) Histogram",
                "B) Pie chart",
                "C) Flowchart",
                "D) Tree diagram",
            ],
            "answer": "A",
        },
    ],
    "machine learning": [
        {
            "question": "Learning from labeled training data is called:",
            "options": [
                "A) Unsupervised learning",
                "B) Supervised learning",
                "C) Reinforcement learning",
                "D) Random learning",
            ],
            "answer": "B",
        },
        {
            "question": "Which is an example of classification?",
            "options": [
                "A) Predicting house price",
                "B) Predicting temperature",
                "C) Spam email detection",
                "D) Calculating average",
            ],
            "answer": "C",
        },
        {
            "question": "K-Means is mainly used for:",
            "options": [
                "A) Classification",
                "B) Clustering",
                "C) Regression",
                "D) Encryption",
            ],
            "answer": "B",
        },
        {
            "question": (
                "Which algorithm is commonly used for classification?"
            ),
            "options": [
                "A) Linear Regression",
                "B) K-Means",
                "C) K-Nearest Neighbors",
                "D) PCA",
            ],
            "answer": "C",
        },
        {
            "question": "What is overfitting?",
            "options": [
                "A) Model performs poorly on training data",
                "B) Model learns training data too closely",
                "C) Model has no data",
                "D) Model does not train",
            ],
            "answer": "B",
        },
        {
            "question": "Which technique is used to reduce overfitting?",
            "options": [
                "A) Regularization",
                "B) Increasing noise",
                "C) Removing validation",
                "D) Ignoring data",
            ],
            "answer": "A",
        },
    ],
    "java": [
        {
            "question": "Java is primarily a:",
            "options": [
                "A) Procedural language",
                "B) Object-oriented programming language",
                "C) Markup language",
                "D) Database",
            ],
            "answer": "B",
        },
        {
            "question": "Which keyword is used to create an object in Java?",
            "options": ["A) object", "B) create", "C) new", "D) class"],
            "answer": "C",
        },
        {
            "question": "Which method is the entry point of a Java program?",
            "options": ["A) start()", "B) main()", "C) run()", "D) execute()"],
            "answer": "B",
        },
        {
            "question": "Which keyword is used to inherit a class?",
            "options": [
                "A) implements",
                "B) extends",
                "C) inherits",
                "D) super",
            ],
            "answer": "B",
        },
        {
            "question": (
                "Which concept allows one interface to have multiple"
                " implementations?"
            ),
            "options": [
                "A) Encapsulation",
                "B) Inheritance",
                "C) Polymorphism",
                "D) Compilation",
            ],
            "answer": "C",
        },
    ],
    "data science": [
        {
            "question": "Data Science mainly combines:",
            "options": [
                "A) Statistics, programming and domain knowledge",
                "B) Only programming",
                "C) Only mathematics",
                "D) Only databases",
            ],
            "answer": "A",
        },
        {
            "question": "Which language is widely used in Data Science?",
            "options": ["A) Python", "B) HTML", "C) CSS", "D) XML"],
            "answer": "A",
        },
        {
            "question": (
                "Which library is commonly used for numerical computing in"
                " Python?"
            ),
            "options": ["A) NumPy", "B) Flask", "C) Django", "D) Tkinter"],
            "answer": "A",
        },
        {
            "question": (
                "Which library is commonly used for data manipulation?"
            ),
            "options": ["A) Pandas", "B) Turtle", "C) Pygame", "D) Requests"],
            "answer": "A",
        },
        {
            "question": "What is data visualization?",
            "options": [
                "A) Encrypting data",
                "B) Representing data graphically",
                "C) Deleting data",
                "D) Compressing data",
            ],
            "answer": "B",
        },
    ],
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🎓 EduSathi AI")
st.sidebar.caption("Learn smarter. Learn your way.")
st.sidebar.markdown("---")

if st.session_state.logged_in:
    st.sidebar.write(f"👤 Welcome, **{st.session_state.user_name}**!")
    pages = [
        "🏠 Home",
        "🤖 AI Tutor",
        "📚 Study Materials",
        "📝 AI Quiz",
        "📅 Study Planner",
        "📊 My Progress",
        "♿ Accessibility",
    ]
    for p in pages:
        if st.sidebar.button(p, use_container_width=True):
            st.session_state.page = p
            st.session_state.quiz_submitted = False
            st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.page = "🔐 Login"
        st.rerun()
else:
    st.sidebar.info("Please log in to access EduSathi AI features.")

# ---------------------------------------------------------
# 🔐 LOGIN / SIGN UP PAGE
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🎓 Welcome to EduSathi AI")
    st.subheader("Your AI-Powered Learning Assistant")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        st.markdown("### Log In")
        login_user = st.text_input("Username / Email", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", use_container_width=True):
            if login_user.strip() and login_pass.strip():
                st.session_state.logged_in = True
                st.session_state.user_name = login_user
                st.session_state.page = "🏠 Home"
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.warning("Please enter both username and password.")

    with tab2:
        st.markdown("### Create an Account")
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email Address", key="signup_email")
        signup_pass = st.text_input(
            "Create Password", type="password", key="signup_pass"
        )
        if st.button("Sign Up", use_container_width=True):
            if (
                signup_name.strip()
                and signup_email.strip()
                and signup_pass.strip()
            ):
                st.session_state.logged_in = True
                st.session_state.user_name = signup_name
                st.session_state.page = "🏠 Home"
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.warning("Please fill out all details to sign up.")

# ---------------------------------------------------------
# 🏠 HOME
# ---------------------------------------------------------
elif st.session_state.page == "🏠 Home":
    st.title("🎓 EduSathi AI")
    st.subheader(f"Welcome back, {st.session_state.user_name}!")
    st.write(
        "EduSathi AI helps students learn concepts, study materials, practice"
        " quizzes, organize schedules, and track academic progress."
    )
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.markdown("### 🤖 AI Tutor")
            st.write("Ask questions and get simple AI explanations.")
    with col2:
        with st.container(border=True):
            st.markdown("### 📚 Study Materials")
            st.write("Upload PDF materials and extract quick insights.")
    with col3:
        with st.container(border=True):
            st.markdown("### 📝 AI Quiz")
            st.write("Test knowledge and track test metrics.")
    with col4:
        with st.container(border=True):
            st.markdown("### 📅 Study Planner")
            st.write("Generate custom day-by-day study schedules.")

    st.markdown("---")
    st.success("💡 Start with AI Tutor or build a personalized Study Schedule!")

# ---------------------------------------------------------
# 🤖 AI TUTOR
# ---------------------------------------------------------
elif st.session_state.page == "🤖 AI Tutor":
    st.title("🤖 AI Tutor")
    st.write("Ask EduSathi AI any academic question.")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input(
            "📚 Topic",
            placeholder="Example: Python, Statistics, Machine Learning",
        )
    with col2:
        difficulty = st.selectbox(
            "🎯 Difficulty", ["Beginner", "Intermediate", "Advanced"]
        )

    language = st.selectbox("🌐 Language", ["English", "Telugu", "Hindi"])
    question = st.text_area(
        "❓ Ask your question",
        placeholder="Example: Explain supervised learning in simple words.",
    )

    if st.button("🤖 Ask AI Tutor", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("EduSathi AI is thinking..."):
                prompt = (
                    f"You are EduSathi AI, an educational tutor.\nTopic:"
                    f" {topic}\nDifficulty: {difficulty}\nLanguage:"
                    f" {language}\nStudent question: {question}\nGive a clear"
                    " student-friendly answer structured as: 1. Simple"
                    " Definition 2. Explanation 3. Example 4. Real-world"
                    " Application 5. Important Exam Points"
                )
                answer = ask_ollama(prompt)

            if answer.startswith("ERROR:"):
                st.error(answer)
            else:
                st.markdown("### 💡 EduSathi AI Answer")
                st.write(answer)

# ---------------------------------------------------------
# 📚 STUDY MATERIALS
# ---------------------------------------------------------
elif st.session_state.page == "📚 Study Materials":
    st.title("📚 Study Materials")
    st.write("Upload a PDF and ask questions based on your study material.")

    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([
                page.extract_text() + "\n"
                for page in reader.pages
                if page.extract_text()
            ])
            st.session_state.study_text = text
            st.success(
                f"PDF loaded successfully! {len(reader.pages)} pages found."
            )

            # Generate and display a summary of the PDF in place of character count
            with st.spinner("Summarizing PDF..."):
                summary_prompt = (
                    "You are EduSathi AI. Provide a concise summary of the key "
                    f"points in the following study material:\n\n{text[:20000]}"
                )
                summary = ask_ollama(summary_prompt)
                st.info(f"**📌 PDF Summary:**\n\n{summary}")

        except Exception as e:
            st.error(f"Could not read PDF: {e}")

    if st.session_state.study_text:
        st.markdown("---")
        st.subheader("📖 Ask From Your PDF")
        pdf_question = st.text_area(
            "Your question",
            placeholder=(
                "Example: What is the definition given in this chapter?"
            ),
        )

        if st.button("🔎 Ask From PDF", use_container_width=True):
            if not pdf_question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching your study material..."):
                    context = st.session_state.study_text[:20000]
                    prompt = (
                        "You are EduSathi AI. Answer the question using ONLY"
                        " the study material below:\nSTUDY"
                        f" MATERIAL:\n{context}\nQUESTION:\n{pdf_question}\nIf"
                        " answer isn't in material, say 'The answer was not"
                        " found in the uploaded material.'"
                    )
                    answer = ask_ollama(prompt)
                st.markdown("### 💡 Answer")
                st.write(answer)
# ---------------------------------------------------------
# 📝 AI QUIZ
# ---------------------------------------------------------
elif st.session_state.page == "📝 AI Quiz":
    st.title("📝 AI Quiz")
    st.write("Choose a topic and test your knowledge.")

    col1, col2, col3 = st.columns(3)
    with col1:
        topic = st.selectbox(
            "📚 Select Topic",
            [
                "Python",
                "Statistics",
                "Machine Learning",
                "Java",
                "Data Science",
            ],
        )
    with col2:
        difficulty = st.selectbox("🎯 Difficulty", ["Easy", "Medium", "Hard"])
    with col3:
        number_of_questions = st.selectbox("🔢 Questions", [3, 5, 7, 10])

    st.markdown("---")

    if st.button("✨ Generate Quiz", use_container_width=True):
        questions = QUIZ_BANK.get(topic.lower(), QUIZ_BANK["python"]).copy()
        random.shuffle(questions)
        st.session_state.quiz_questions = questions[:number_of_questions]
        st.session_state.quiz_submitted = False
        st.session_state.last_score = 0
        st.session_state.last_total = len(st.session_state.quiz_questions)
        st.rerun()

    if st.session_state.quiz_questions:
        questions = st.session_state.quiz_questions
        st.markdown(f"## 🎯 {topic} Quiz")
        st.info(f"{len(questions)} questions • Difficulty: {difficulty}")

        if not st.session_state.quiz_submitted:
            for i, q in enumerate(questions):
                st.markdown(f"### Question {i + 1}")
                st.write(q["question"])
                st.radio(
                    "Choose your answer:",
                    q["options"],
                    key=f"quiz_answer_{i}",
                    index=None,
                )
                st.markdown("---")

            if st.button("✅ Submit Quiz", use_container_width=True):
                score = sum([
                    1
                    for i, q in enumerate(questions)
                    if st.session_state.get(f"quiz_answer_{i}")
                    and st.session_state.get(f"quiz_answer_{i}")[0]
                    == q["answer"]
                ])
                st.session_state.last_score = score
                st.session_state.questions_answered += len(questions)
                st.session_state.correct_answers += score
                st.session_state.quizzes_completed += 1
                st.session_state.quiz_submitted = True
                st.rerun()
        else:
            score = st.session_state.last_score
            total = st.session_state.last_total
            percentage = (score / total) * 100

            st.markdown("---")
            st.subheader("🏆 Quiz Result")
            col1, col2, col3 = st.columns(3)
            col1.metric("Score", f"{score}/{total}")
            col2.metric("Percentage", f"{percentage:.0f}%")
            result_text = (
                "Excellent"
                if percentage >= 80
                else "Good" if percentage >= 60 else "Needs Practice"
            )
            col3.metric("Performance", result_text)

            if percentage >= 80:
                st.success(
                    "🎉 Excellent! You have a strong understanding of this"
                    " topic."
                )
            elif percentage >= 60:
                st.info(
                    "👍 Good work! Review the incorrect answers and practice"
                    " again."
                )
            else:
                st.warning(
                    "📚 Keep practicing. Use AI Tutor to strengthen this"
                    " topic."
                )

            st.markdown("---")
            st.subheader("📋 Answer Review")
            for i, q in enumerate(questions):
                selected = st.session_state.get(f"quiz_answer_{i}")
                correct_answer = q["answer"]
                correct_option = next(
                    opt
                    for opt in q["options"]
                    if opt.startswith(correct_answer)
                )

                st.markdown(f"### Question {i + 1}")
                st.write(q["question"])
                if selected:
                    if selected[0] == correct_answer:
                        st.success(f"✅ Your answer: {selected}")
                    else:
                        st.error(f"❌ Your answer: {selected}")
                        st.info(f"✅ Correct answer: {correct_option}")
                else:
                    st.warning("⚠️ You did not answer this question.")
                    st.info(f"✅ Correct answer: {correct_option}")
                st.markdown("---")

            if st.button("🔄 Take Another Quiz", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_submitted = False
                st.rerun()

# ---------------------------------------------------------
# 📅 STUDY PLANNER
# ---------------------------------------------------------
# ---------------------------------------------------------
# 📅 STUDY PLANNER
# ---------------------------------------------------------
elif st.session_state.page == "📅 Study Planner":
    st.title("📅 AI Study Planner")
    st.caption("Generate a structured schedule to organize your study plan effectively.")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input(
                "📖 Subject / Target Exam",
                placeholder="e.g. Python Programming, Machine Learning",
            )
            daily_hours = st.slider("⏱ Daily Study Hours", 1, 8, 3)
        with col2:
            tomorrow = date.today() + timedelta(days=1)
            target_date = st.date_input(
                "🎯 Target Exam Date", value=tomorrow, min_value=tomorrow
            )
            days_remaining = (target_date - date.today()).days
            st.info(f"🗓️ **{days_remaining} days** remaining until target date.")

        generate_btn = st.button("✨ Generate Study Plan", use_container_width=True)

    if generate_btn:
        if not subject.strip():
            st.warning("Please enter a subject or target exam.")
        else:
            with st.spinner("Creating your personalized study schedule..."):
                prompt = f"""You are EduSathi AI Study Planner. Create a beautifully formatted, structured daily and weekly study plan for subject: '{subject}'. 
Target Date: {target_date} ({days_remaining} days available), Daily Study Budget: {daily_hours} hours.

Format your response using clear Markdown features:
1. Use bold headings (##, ###).
2. Use bullet points and numbered lists for steps.
3. Use Markdown Tables for the Daily Breakdown/Timetable where applicable.
4. Include callout sections for '💡 Key Tips' and '🎯 Daily Milestones'.

Sections required:
- ## 📌 Plan Overview
- ## 🎯 Milestones
- ## 🗓️ Daily Breakdown
- ## 💡 Revision & Practice Strategy"""
                st.session_state.study_plan = ask_ollama(prompt)

    if st.session_state.study_plan:
        st.markdown("---")
        st.subheader("📋 Your Personalized Study Schedule")
        
        # Display as rich Markdown inside a styled container block
        with st.container(border=True):
            st.markdown(st.session_state.study_plan)
# ---------------------------------------------------------
# 📊 MY PROGRESS
# ---------------------------------------------------------
elif st.session_state.page == "📊 My Progress":
    st.title("📊 My Progress")
    q_ans = st.session_state.questions_answered
    c_ans = st.session_state.correct_answers
    quizzes = st.session_state.quizzes_completed
    accuracy = (c_ans / q_ans * 100) if q_ans > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Questions Answered", q_ans)
    col2.metric("Correct Answers", c_ans)
    col3.metric("Quizzes Completed", quizzes)
    col4.metric("Overall Accuracy", f"{accuracy:.0f}%")

    st.markdown("---")
    st.subheader("📈 Overall Performance")
    st.progress(int(accuracy))
    st.write(f"Your current accuracy is **{accuracy:.1f}%**.")

    st.markdown("---")
    st.subheader("🎯 Adaptive Recommendation")
    if q_ans == 0:
        st.info("Take your first quiz to start building your learning profile.")
    elif accuracy < 50:
        st.warning(
            "📚 Your accuracy is below 50%. Start with beginner-level questions"
            " and use AI Tutor to review basic concepts."
        )
    elif accuracy < 70:
        st.info(
            "📖 You are making progress. Practice more questions and review"
            " concepts you answered incorrectly."
        )
    elif accuracy < 85:
        st.success(
            "👍 Good progress! Try medium and advanced questions to improve"
            " further."
        )
    else:
        st.success(
            "🏆 Excellent performance! You are ready for advanced-level"
            " practice."
        )

    st.markdown("---")
    st.subheader("💡 Learning Strategy")
    st.write(
        "1. Build a study schedule using Study Planner.\n2. Review material and"
        " ask AI Tutor.\n3. Take regular topic quizzes.\n4. Analyze incorrect"
        " options.\n5. Track your overall accuracy."
    )

# ---------------------------------------------------------
# ♿ ACCESSIBILITY
# ---------------------------------------------------------
elif st.session_state.page == "♿ Accessibility":
    st.title("♿ Accessibility")
    st.write("Customize EduSathi AI for easier learning.")
    st.markdown("---")

    text_size = st.selectbox(
        "🔤 Preferred Text Size", ["Normal", "Large", "Extra Large"]
    )
    language = st.selectbox(
        "🌐 Preferred Language", ["English", "Telugu", "Hindi"]
    )
    high_contrast = st.checkbox("🌗 High Contrast Mode")

    if high_contrast:
        st.markdown(
            "<style>.stApp { background-color: #111111; color: white; }"
            " .stMarkdown, .stText, p, label { color: white !important;"
            " }</style>",
            unsafe_allow_html=True,
        )

    if text_size == "Large":
        st.markdown(
            "<style>.stApp { font-size: 20px; }</style>",
            unsafe_allow_html=True,
        )
    elif text_size == "Extra Large":
        st.markdown(
            "<style>.stApp { font-size: 24px; }</style>",
            unsafe_allow_html=True,
        )

    st.success(
        f"Accessibility settings applied. Preferred language: {language}"
    )