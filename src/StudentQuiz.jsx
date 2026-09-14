import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./StudentQuiz.css";

function StudentQuiz() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});

  // Timer
  const [startTime] = useState(Date.now());
  const [seconds, setSeconds] = useState(0);

  // --------------------------------
  // Parse Options
  // --------------------------------
  const parseOptions = (options) => {
    if (!options) return [];

    const optionString = String(options).trim();

    // If database contains JSON array
    if (optionString.startsWith("[")) {
      try {
        const parsed = JSON.parse(optionString);

        if (Array.isArray(parsed)) {
          return parsed;
        }
      } catch (error) {
        console.log("JSON option parsing error:", error);
      }
    }

    // If database contains old pipe-separated format
    return optionString
      .split("|")
      .map((option) => option.trim())
      .filter((option) => option.length > 0);
  };

  // --------------------------------
  // Clean A) B) C) D) from options
  // --------------------------------
  const cleanOption = (option) => {
    if (!option) return "";

    return String(option)
      .replace(/^[A-D]\)\s*/i, "")
      .trim();
  };

  // --------------------------------
  // Live Timer
  // --------------------------------
  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(
        Math.floor((Date.now() - startTime) / 1000)
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  // --------------------------------
  // Load Questions
  // --------------------------------
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        console.log("Loading Quiz ID:", id);

        const res = await axios.get(
          `https://lms-backend-api-bnx4.onrender.com/student-quiz/${id}`
        );

        console.log("Questions:", res.data);

        setQuestions(res.data);
      } catch (error) {
        console.log("Quiz Loading Error:", error);

        alert("Unable to load quiz questions.");
      }
    };

    loadQuestions();
  }, [id]);

  // --------------------------------
  // Select Answer
  // --------------------------------
  const handleOptionChange = (questionId, option) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: option,
    }));
  };

  // --------------------------------
  // Submit Quiz
  // --------------------------------
  const submitQuiz = async () => {
    try {
      if (questions.length === 0) {
        alert("No questions available.");
        return;
      }

      // Check unanswered questions
      const unansweredQuestions = questions.filter(
        (question) =>
          !answers[question.question_id]
      );

      if (unansweredQuestions.length > 0) {
        const confirmSubmit = window.confirm(
          `You have ${unansweredQuestions.length} unanswered question(s).\n\nDo you want to submit anyway?`
        );

        if (!confirmSubmit) {
          return;
        }
      }

      const timeSpent = Math.floor(
        (Date.now() - startTime) / 1000
      );

      const studentId =
        localStorage.getItem("student_id");

      if (!studentId) {
        alert("Student ID not found. Please login again.");
        return;
      }

      console.log("Submitting Quiz...");
      console.log("Student ID:", studentId);
      console.log("Quiz ID:", id);
      console.log("Answers:", answers);
      console.log("Time Spent:", timeSpent);

      const res = await axios.post(
        "https://lms-backend-api-bnx4.onrender.com/submit-quiz",
        {
          student_id: studentId,
          quiz_id: id,
          answers: answers,
          time_spent: timeSpent,
        }
      );

      console.log("Submission Response:", res.data);

      alert(
        `Quiz Submitted Successfully\n\n` +
        `Score: ${res.data.score}/${res.data.total_questions}\n\n` +
        `Percentage: ${res.data.percentage}%\n\n` +
        `Status: ${res.data.status}`
      );

      navigate("/student-results");
    } catch (error) {
      console.log("Submission Error:", error);

      if (error.response) {
        console.log(
          "Backend Error:",
          error.response.data
        );
      }

      alert("Submission Failed.");
    }
  };

  // --------------------------------
  // Get Quiz Name
  // --------------------------------
  const getQuizName = () => {
    switch (Number(id)) {
      case 2:
        return "Web / HTML";

      case 3:
        return "Java Fundamentals";

      case 4:
        return "Data Structures & Algorithms";

      case 5:
        return "Database";

      case 6:
        return "Operating Systems";

      case 7:
        return "Software Design & Architecture";

      case 8:
        return "Web Development";

      default:
        return "Student Quiz";
    }
  };

  return (
    <div className="student-quiz-container">

      <h1>{getQuizName()}</h1>

      <h3>
        Time: {seconds} sec
      </h3>

      <p>
        Total Questions: {questions.length}
      </p>

      {/* Questions */}
      {questions.length === 0 ? (
        <p>Loading questions...</p>
      ) : (
        questions.map((question, index) => {
          const options = parseOptions(
            question.options
          );

          return (
            <div
              className="question-card"
              key={question.question_id}
            >

              <h3>
                Q{index + 1}.{" "}
                {question.question_text}
              </h3>

              {/* Options */}
              {options.map((option, optionIndex) => {
                const cleanedOption =
                  cleanOption(option);

                return (
                  <div
                    className="option"
                    key={optionIndex}
                  >

                    <label>
                      <input
                        type="radio"
                        name={`question-${question.question_id}`}
                        value={cleanedOption}
                        checked={
                          answers[
                            question.question_id
                          ] === cleanedOption
                        }
                        onChange={() =>
                          handleOptionChange(
                            question.question_id,
                            cleanedOption
                          )
                        }
                      />

                      {" "}

                      {cleanedOption}
                    </label>

                  </div>
                );
              })}

            </div>
          );
        })
      )}

      {/* Submit Button */}
      {questions.length > 0 && (
        <button
          className="submit-btn"
          onClick={submitQuiz}
        >
          Submit Quiz
        </button>
      )}

    </div>
  );
}

export default StudentQuiz;
