import streamlit as st
import json
import random
import os
from datetime import datetime
from typing import List, Dict, Any

# Load questions from JSON file
@st.cache_data
def load_questions() -> List[Dict[str, Any]]:
    try:
        with open('questions.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("questions.json file not found!")
        return []
    except json.JSONDecodeError:
        st.error("Error reading questions.json file!")
        return []

def normalize_answer(answer: str) -> str:
    """Remove ** formatting and normalize answer"""
    return answer.replace('**', '').strip()

def shuffle_options(options: List[str]) -> List[str]:
    """Shuffle the order of answer options"""
    shuffled = options.copy()
    random.shuffle(shuffled)
    return shuffled

def get_correct_answers(question: Dict[str, Any]) -> List[str]:
    """Extract correct answers, handling both single answers and lists"""
    correct = question.get('correct_answer', '')
    if isinstance(correct, list):
        return [normalize_answer(ans) for ans in correct]
    else:
        return [normalize_answer(correct)]

def check_answer(selected_options: List[str], correct_answers: List[str]) -> bool:
    """Check if selected answers match correct answers"""
    if not selected_options:
        return False
    
    normalized_selected = [normalize_answer(opt) for opt in selected_options]
    return set(normalized_selected) == set(correct_answers)

def load_user_statistics():
    """Load user statistics from file"""
    try:
        filename = "user_statistics.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {
                "created": datetime.now().isoformat(),
                "total_quizzes": 0,
                "questions": {}
            }
    except Exception as e:
        st.error(f"Błąd przy wczytywaniu statystyk: {e}")
        return {"created": datetime.now().isoformat(), "total_quizzes": 0, "questions": {}}

def save_user_statistics(stats: Dict[str, Any]):
    """Save user statistics to file"""
    try:
        filename = "user_statistics.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(stats, file, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Błąd przy zapisywaniu statystyk: {e}")

def update_question_statistics(question: Dict[str, Any], user_answer: List[str], is_correct: bool, stats: Dict[str, Any]):
    """Update statistics for a specific question"""
    question_text = question["question"]
    correct_answers = get_correct_answers(question)
    
    if question_text not in stats["questions"]:
        stats["questions"][question_text] = {
            "attempts": 0,
            "correct_attempts": 0,
            "incorrect_attempts": 0,
            "correct_answers": correct_answers,
            "wrong_answers_given": [],
            "last_attempted": None,
            "first_attempted": None
        }
    
    question_stats = stats["questions"][question_text]
    question_stats["attempts"] += 1
    question_stats["last_attempted"] = datetime.now().isoformat()
    
    if question_stats["first_attempted"] is None:
        question_stats["first_attempted"] = datetime.now().isoformat()
    
    if is_correct:
        question_stats["correct_attempts"] += 1
    else:
        question_stats["incorrect_attempts"] += 1
        # Record the wrong answer given
        wrong_answer = {
            "answer": user_answer,
            "timestamp": datetime.now().isoformat()
        }
        question_stats["wrong_answers_given"].append(wrong_answer)

def save_incorrect_question(question: Dict[str, Any], reason: str = ""):
    """Save question marked as having incorrect answer to a file"""
    try:
        # Create filename
        filename = "pytania_z_blędnymi_odpowiedziami.json"
        
        # Load existing data if file exists
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {
                "created": datetime.now().isoformat(),
                "questions": []
            }
        
        # Add timestamp when this question was marked
        question_with_timestamp = question.copy()
        question_with_timestamp["marked_as_incorrect"] = datetime.now().isoformat()
        question_with_timestamp["reason"] = reason.strip() if reason else "Brak podanego powodu"
        
        # Check if question already exists (avoid duplicates)
        question_text = question["question"]
        if not any(q["question"] == question_text for q in data["questions"]):
            data["questions"].append(question_with_timestamp)
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            return True
        else:
            return False  # Already exists
    except Exception as e:
        st.error(f"Błąd przy zapisywaniu pytania: {e}")
        return False

def show_full_statistics_modal(stats: Dict[str, Any]):
    """Display full statistics in a modal-like interface"""
    st.header("📈 Pełne statystyki użytkownika")
    
    # Close button
    if st.button("❌ Zamknij statystyki"):
        st.session_state.show_full_stats = False
        st.rerun()
    
    # Overall statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ukończone quizy", stats["total_quizzes"])
    with col2:
        total_attempts = sum(q["attempts"] for q in stats["questions"].values())
        st.metric("Łączne próby", total_attempts)
    with col3:
        total_correct = sum(q["correct_attempts"] for q in stats["questions"].values())
        if total_attempts > 0:
            overall_success = (total_correct / total_attempts) * 100
            st.metric("Ogólna skuteczność", f"{overall_success:.1f}%")
        else:
            st.metric("Ogólna skuteczność", "0%")
    
    st.divider()
    
    # Questions statistics
    st.subheader("📋 Statystyki pytań")
    
    if not stats["questions"]:
        st.info("Brak danych o pytaniach. Rozwiąż kilka pytań, aby zobaczyć statystyki.")
        return
    
    # Filter options
    filter_option = st.selectbox(
        "Filtruj pytania:",
        ["Wszystkie", "Najczęściej błędne", "Najczęściej poprawne", "Ostatnio rozwiązywane"]
    )
    
    # Sort questions based on filter
    questions_list = list(stats["questions"].items())
    
    if filter_option == "Najczęściej błędne":
        questions_list.sort(key=lambda x: x[1]["incorrect_attempts"] / max(x[1]["attempts"], 1), reverse=True)
    elif filter_option == "Najczęściej poprawne":
        questions_list.sort(key=lambda x: x[1]["correct_attempts"] / max(x[1]["attempts"], 1), reverse=True)
    elif filter_option == "Ostatnio rozwiązywane":
        questions_list.sort(key=lambda x: x[1]["last_attempted"] or "", reverse=True)
    
    # Display questions in pages
    questions_per_page = 5
    total_pages = (len(questions_list) + questions_per_page - 1) // questions_per_page
    
    if total_pages > 1:
        page = st.selectbox("Strona", range(1, total_pages + 1)) - 1
    else:
        page = 0
    
    start_idx = page * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions_list))
    
    for i, (question_text, q_stats) in enumerate(questions_list[start_idx:end_idx], start_idx + 1):
        with st.expander(f"Pytanie {i}: {question_text[:100]}..."):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Próby", q_stats["attempts"])
            with col2:
                st.metric("Poprawne", q_stats["correct_attempts"])
            with col3:
                st.metric("Błędne", q_stats["incorrect_attempts"])
            with col4:
                if q_stats["attempts"] > 0:
                    success_rate = (q_stats["correct_attempts"] / q_stats["attempts"]) * 100
                    st.metric("Skuteczność", f"{success_rate:.1f}%")
                else:
                    st.metric("Skuteczność", "0%")
            
            # Show correct answers
            st.write(f"**Poprawne odpowiedzi:** {', '.join(q_stats['correct_answers'])}")
            
            # Show wrong answers given
            if q_stats["wrong_answers_given"]:
                st.write("**Błędne odpowiedzi, które dawałeś:**")
                for wrong in q_stats["wrong_answers_given"][-5:]:  # Show last 5
                    timestamp = datetime.fromisoformat(wrong["timestamp"]).strftime("%d.%m.%Y %H:%M")
                    answer_text = ', '.join(wrong["answer"]) if wrong["answer"] else "Brak odpowiedzi"
                    st.write(f"• {answer_text} _(dn. {timestamp})_")
            
            # Show timing info
            if q_stats["first_attempted"]:
                first_time = datetime.fromisoformat(q_stats["first_attempted"]).strftime("%d.%m.%Y %H:%M")
                st.write(f"**Pierwszy raz:** {first_time}")
            if q_stats["last_attempted"]:
                last_time = datetime.fromisoformat(q_stats["last_attempted"]).strftime("%d.%m.%Y %H:%M")
                st.write(f"**Ostatnio:** {last_time}")

def main():
    st.set_page_config(
        page_title="Quiz App",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Quiz App - Interactive Learning")
    
    # Load questions and statistics
    questions = load_questions()
    if not questions:
        st.error("No questions available. Please ensure questions.json file is present and properly formatted.")
        return
    
    # Load user statistics
    user_stats = load_user_statistics()
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.quiz_completed = False
        st.session_state.shuffled_questions = random.sample(questions, len(questions))
        st.session_state.show_answer_feedback = False
        st.session_state.current_is_correct = False
        st.session_state.user_stats = user_stats
        # Pre-shuffle options for each question
        st.session_state.shuffled_options = {}
        for i, question in enumerate(st.session_state.shuffled_questions):
            if 'options' in question:
                st.session_state.shuffled_options[i] = shuffle_options(question['options'])
    
    # Quiz completed
    if st.session_state.quiz_completed:
        st.success("🎉 Quiz zakończony!")
        
        # Update total quizzes count
        st.session_state.user_stats["total_quizzes"] += 1
        save_user_statistics(st.session_state.user_stats)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Wynik", f"{st.session_state.score}/{len(questions)}")
        with col2:
            percentage = (st.session_state.score / len(questions)) * 100
            st.metric("Procent", f"{percentage:.1f}%")
        with col3:
            if percentage >= 80:
                st.metric("Ocena", "Bardzo dobra! 🌟")
            elif percentage >= 60:
                st.metric("Ocena", "Dobra! 👍")
            else:
                st.metric("Ocena", "Do poprawy 📚")
        
        # Show detailed results
        with st.expander("Zobacz szczegółowe wyniki"):
            for i, (question, user_answer, correct) in enumerate(st.session_state.answers):
                st.write(f"**Pytanie {i+1}:** {question['question']}")
                st.write(f"Twoja odpowiedź: {', '.join(user_answer) if user_answer else 'Brak odpowiedzi'}")
                correct_answers = get_correct_answers(question)
                st.write(f"Poprawna odpowiedź: {', '.join(correct_answers)}")
                if correct:
                    st.success("✅ Poprawnie")
                else:
                    st.error("❌ Niepoprawnie")
                st.divider()
        
        if st.button("🔄 Rozpocznij quiz ponownie"):
            for key in ['current_question', 'score', 'answers', 'quiz_completed', 'shuffled_questions', 'show_answer_feedback', 'current_is_correct', 'shuffled_options']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        return
    
    # Current question
    current_q = st.session_state.current_question
    question = st.session_state.shuffled_questions[current_q]
    
    # Progress bar
    progress = (current_q + 1) / len(questions)
    st.progress(progress)
    st.write(f"Pytanie {current_q + 1} z {len(questions)}")
    
    # Display question
    st.subheader(f"Pytanie {current_q + 1}")
    st.write(question['question'])
    
    # Get correct answers for this question
    correct_answers = get_correct_answers(question)
    
    # Display options - always as multiple choice
    st.write("**Opcje odpowiedzi:**")
    
    # Use shuffled options for this question
    options = st.session_state.shuffled_options.get(current_q, question.get('options', []))
    selected_options = []
    
    # All questions are treated as multiple choice
    for option in options:
        clean_option = normalize_answer(option)
        if st.checkbox(clean_option, key=f"option_{current_q}_{option}", disabled=st.session_state.show_answer_feedback):
            selected_options.append(clean_option)
    
    # Show current selection
    if selected_options:
        st.write(f"**Wybrane odpowiedzi:** {', '.join(selected_options)}")
    
    # Show answer feedback if we just answered
    if st.session_state.show_answer_feedback:
        if st.session_state.current_is_correct:
            st.success("✅ Poprawna odpowiedź!")
        else:
            st.error("❌ Niepoprawna odpowiedź!")
            st.write(f"**Poprawna odpowiedź:** {', '.join(correct_answers)}")
        
        # Next/Finish button after showing feedback
        st.divider()
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        with col_nav2:
            if current_q < len(questions) - 1:
                if st.button("Następne ➡️", use_container_width=True):
                    st.session_state.current_question += 1
                    st.session_state.show_answer_feedback = False
                    st.rerun()
            else:
                if st.button("🏁 Zakończ quiz", use_container_width=True):
                    st.session_state.quiz_completed = True
                    st.rerun()
        
        # Add button to mark question as having incorrect answer
        st.divider()
        st.write("**Zgłoś problem z pytaniem:**")
        
        col_text, col_button = st.columns([3, 1])
        with col_text:
            reason = st.text_input(
                "Dlaczego uważasz, że to pytanie jest błędne?",
                placeholder="np. Błędna odpowiedź, niejednoznaczne sformułowanie, błąd merytoryczny...",
                key=f"reason_{current_q}",
                help="Opisz dlaczego uważasz, że pytanie lub odpowiedź są niepoprawne"
            )
        
        with col_button:
            st.write("")  # Add some spacing
            if st.button("🚩 Oznacz jako błędne", help="Oznacz to pytanie jako mające niepoprawną odpowiedź w bazie"):
                success = save_incorrect_question(question, reason)
                if success:
                    st.success("✅ Pytanie zostało zapisane jako błędne!")
                else:
                    st.warning("⚠️ To pytanie już zostało wcześniej oznaczone jako błędne.")
                st.rerun()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_q > 0 and not st.session_state.show_answer_feedback:
            if st.button("⬅️ Poprzednie"):
                st.session_state.current_question -= 1
                st.session_state.show_answer_feedback = False
                st.rerun()
    
    with col3:
        if not st.session_state.show_answer_feedback:
            # Submit answer button
            if st.button("✅ Sprawdź odpowiedź"):
                # Check answer and save
                is_correct = check_answer(selected_options, correct_answers)
                if is_correct:
                    st.session_state.score += 1
                
                # Update question statistics
                update_question_statistics(question, selected_options, is_correct, st.session_state.user_stats)
                save_user_statistics(st.session_state.user_stats)
                
                st.session_state.answers.append((question, selected_options, is_correct))
                st.session_state.show_answer_feedback = True
                st.session_state.current_is_correct = is_correct
                st.rerun()
    
    # Sidebar with quiz info
    with st.sidebar:
        st.header("📊 Informacje o quizie")
        st.write(f"**Łączna liczba pytań:** {len(questions)}")
        st.write(f"**Aktualny postęp:** {current_q + 1}/{len(questions)}")
        
        if st.session_state.answers:
            correct_so_far = sum(1 for _, _, correct in st.session_state.answers if correct)
            st.write(f"**Poprawne odpowiedzi:** {correct_so_far}/{len(st.session_state.answers)}")
        
        st.divider()
        
        # User Statistics Section
        st.header("📈 Twoje statystyki")
        st.write(f"**Ukończone quizy:** {st.session_state.user_stats['total_quizzes']}")
        
        # Statistics for current question
        current_question = st.session_state.shuffled_questions[current_q]
        question_text = current_question["question"]
        if question_text in st.session_state.user_stats["questions"]:
            q_stats = st.session_state.user_stats["questions"][question_text]
            with st.expander(f"📊 Statystyki tego pytania"):
                st.write(f"**Łącznie prób:** {q_stats['attempts']}")
                st.write(f"**Poprawnych:** {q_stats['correct_attempts']}")
                st.write(f"**Błędnych:** {q_stats['incorrect_attempts']}")
                if q_stats['attempts'] > 0:
                    success_rate = (q_stats['correct_attempts'] / q_stats['attempts']) * 100
                    st.write(f"**Skuteczność:** {success_rate:.1f}%")
                
                # Show wrong answers given
                if q_stats['wrong_answers_given']:
                    st.write("**Błędne odpowiedzi, które dawałeś:**")
                    for i, wrong in enumerate(q_stats['wrong_answers_given'][-3:]):  # Show last 3
                        st.write(f"• {', '.join(wrong['answer']) if wrong['answer'] else 'Brak odpowiedzi'}")
        
        # Global statistics button
        if st.button("📈 Zobacz pełne statystyki"):
            st.session_state.show_full_stats = True
        
        st.divider()
        st.write("**Instrukcje:**")
        st.write("• Przeczytaj pytanie uważnie")
        st.write("• Zaznacz odpowiedź(i)")
        st.write("• Kliknij 'Sprawdź odpowiedź'")
        st.write("• Po zobaczeniu wyniku kliknij 'Następne'")
    
    # Full statistics modal
    if hasattr(st.session_state, 'show_full_stats') and st.session_state.show_full_stats:
        show_full_statistics_modal(st.session_state.user_stats)

if __name__ == "__main__":
    main()
