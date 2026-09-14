import axios from "axios";
import { useEffect, useState } from "react";
import "./Questions.css";

function Questions() {

  const [questions, setQuestions] = useState([]);
  const [quizzes, setQuizzes] = useState([]);

  const [quizId, setQuizId] = useState("");
  const [questionText, setQuestionText] = useState("");

  const [optionA, setOptionA] = useState("");
  const [optionB, setOptionB] = useState("");
  const [optionC, setOptionC] = useState("");
  const [optionD, setOptionD] = useState("");

  const [correctOption, setCorrectOption] = useState("");

  const [editingId, setEditingId] = useState(null);

  useEffect(() => {

    loadQuestions();
    loadQuizzes();

  }, []);

  // Load Quizzes
  const loadQuizzes = async () => {

    try {

      const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/quizzes");

      setQuizzes(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  // Load Questions
  const loadQuestions = async () => {

    try {

      const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/questions");

      setQuestions(res.data);

    } catch (error) {

      console.log(error);

      alert("Unable to Load Questions");

    }

  };

  // Clear Form
  const clearForm = () => {

    setEditingId(null);

    setQuizId("");
    setQuestionText("");

    setOptionA("");
    setOptionB("");
    setOptionC("");
    setOptionD("");

    setCorrectOption("");

  };

  // Add Question
  const addQuestion = async () => {

    if (
      quizId === "" ||
      questionText === "" ||
      optionA === "" ||
      optionB === "" ||
      optionC === "" ||
      optionD === "" ||
      correctOption === ""
    ) {

      alert("Please Fill All Fields");

      return;

    }

    const options = JSON.stringify([
      optionA,
      optionB,
      optionC,
      optionD
    ]);

    try {

      await axios.post("https://lms-backend-api-bnx4.onrender.com/questions", {

        quiz_id: quizId,
        question_text: questionText,
        options: options,
        correct_option: correctOption

      });

      alert("Question Added Successfully");

      clearForm();

      loadQuestions();

    } catch (error) {

      console.log(error);

      alert("Error Adding Question");

    }

  };

  // Edit Question
  const editQuestion = (question) => {

    setEditingId(question.question_id);

    setQuizId(question.quiz_id);

    setQuestionText(question.question_text);

    const opts = JSON.parse(question.options);

    setOptionA(opts[0]);
    setOptionB(opts[1]);
    setOptionC(opts[2]);
    setOptionD(opts[3]);

    setCorrectOption(question.correct_option);

  };

  // Update Question
  const updateQuestion = async (id) => {

    const options = JSON.stringify([
      optionA,
      optionB,
      optionC,
      optionD
    ]);

    try {

      await axios.put(`https://lms-backend-api-bnx4.onrender.com/questions/${id}`, {

        quiz_id: quizId,
        question_text: questionText,
        options: options,
        correct_option: correctOption

      });

      alert("Question Updated Successfully");

      clearForm();

      loadQuestions();

    } catch (error) {

      console.log(error);

      alert("Update Failed");

    }

  };

  // Delete Question
  const deleteQuestion = async (id) => {

    try {

      await axios.delete(`https://lms-backend-api-bnx4.onrender.com/questions/${id}`);

      alert("Question Deleted");

      loadQuestions();

    } catch (error) {

      console.log(error);

      alert("Delete Failed");

    }

  };

  return (

    <div className="questions-container">

      <h1>Question Management</h1>

      <div className="question-form">

        <select
          value={quizId}
          onChange={(e) => setQuizId(e.target.value)}
        >

          <option value="">Select Quiz</option>

          {
            quizzes.map((quiz) => (

              <option
                key={quiz.quiz_id}
                value={quiz.quiz_id}
              >

                {quiz.title}

              </option>

            ))
          }

        </select>

        <textarea

          placeholder="Question"

          value={questionText}

          onChange={(e) => setQuestionText(e.target.value)}

        />

        <input

          type="text"

          placeholder="Option A"

          value={optionA}

          onChange={(e) => setOptionA(e.target.value)}

        />

        <input

          type="text"

          placeholder="Option B"

          value={optionB}

          onChange={(e) => setOptionB(e.target.value)}

        />

        <input

          type="text"

          placeholder="Option C"

          value={optionC}

          onChange={(e) => setOptionC(e.target.value)}

        />

        <input

          type="text"

          placeholder="Option D"

          value={optionD}

          onChange={(e) => setOptionD(e.target.value)}

        />

        <select

          value={correctOption}

          onChange={(e) => setCorrectOption(e.target.value)}

        >

          <option value="">Correct Option</option>

          <option>{optionA}</option>

          <option>{optionB}</option>

          <option>{optionC}</option>

          <option>{optionD}</option>

        </select>

        <button

          onClick={editingId ? () => updateQuestion(editingId) : addQuestion}

        >

          {editingId ? "Update Question" : "Add Question"}

        </button>

      </div>

      <table>

        <thead>

          <tr>

            <th>ID</th>

            <th>Quiz</th>

            <th>Question</th>

            <th>Correct Answer</th>

            <th>Edit</th>

            <th>Delete</th>

          </tr>

        </thead>

        <tbody>

          {

            questions.map((question) => (

              <tr key={question.question_id}>

                <td>{question.question_id}</td>

                <td>{question.quiz_title}</td>

                <td>{question.question_text}</td>

                <td>{question.correct_option}</td>

                <td>

                  <button

                    className="edit-btn"

                    onClick={() => editQuestion(question)}

                  >

                    Edit

                  </button>

                </td>

                <td>

                  <button

                    className="delete-btn"

                    onClick={() => deleteQuestion(question.question_id)}

                  >

                    Delete

                  </button>

                </td>

              </tr>

            ))

          }

        </tbody>

      </table>

    </div>

  );

}

export default Questions;
