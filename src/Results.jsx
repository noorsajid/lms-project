import axios from "axios";
import { useEffect, useState } from "react";
import "./Results.css";

function Results() {

  const [results, setResults] = useState([]);
  const [students, setStudents] = useState([]);
  const [quizzes, setQuizzes] = useState([]);

  const [studentId, setStudentId] = useState("");
  const [quizId, setQuizId] = useState("");
  const [score, setScore] = useState("");
  const [attempts, setAttempts] = useState("");
  const [timeSpent, setTimeSpent] = useState("");

  const [editingId, setEditingId] = useState(null);

  useEffect(() => {

    loadResults();
    loadStudents();
    loadQuizzes();

  }, []);

  // -------------------------
  // Load Students
  // -------------------------

  const loadStudents = async () => {

    try {

      const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/students");

      setStudents(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  // -------------------------
  // Load Quizzes
  // -------------------------

  const loadQuizzes = async () => {

    try {

      const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/quizzes");

      setQuizzes(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  // -------------------------
  // Load Results
  // -------------------------

  const loadResults = async () => {

    try {

      const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/results");

      setResults(res.data);

    } catch (error) {

      console.log(error);

      alert("Unable to Load Results");

    }

  };

  // -------------------------
  // Clear Form
  // -------------------------

  const clearForm = () => {

    setEditingId(null);

    setStudentId("");
    setQuizId("");
    setScore("");
    setAttempts("");
    setTimeSpent("");

  };

  // -------------------------
  // Add Result
  // -------------------------

  const addResult = async () => {

    if (

      studentId === "" ||
      quizId === "" ||
      score === "" ||
      attempts === "" ||
      timeSpent === ""

    ) {

      alert("Please Fill All Fields");

      return;

    }

    try {

      await axios.post("https://lms-backend-api-bnx4.onrender.com/results", {

        student_id: studentId,
        quiz_id: quizId,
        score: score,
        attempts: attempts,
        time_spent: timeSpent

      });

      alert("Result Added Successfully");

      clearForm();

      loadResults();

    } catch (error) {

      console.log(error);

      alert("Error Adding Result");

    }

  };

  // -------------------------
  // Edit Result
  // -------------------------

  const editResult = (result) => {

    setEditingId(result.result_id);

    setStudentId(result.student_id);
    setQuizId(result.quiz_id);
    setScore(result.score);
    setAttempts(result.attempts);
    setTimeSpent(result.time_spent);

  };

  // -------------------------
  // Update Result
  // -------------------------

  const updateResult = async (id) => {

    try {

      await axios.put(`https://lms-backend-api-bnx4.onrender.com/results/${id}`, {

        student_id: studentId,
        quiz_id: quizId,
        score: score,
        attempts: attempts,
        time_spent: timeSpent

      });

      alert("Result Updated Successfully");

      clearForm();

      loadResults();

    } catch (error) {

      console.log(error);

      alert("Update Failed");

    }

  };
    // -------------------------
  // Delete Result
  // -------------------------

  const deleteResult = async (id) => {

    try {

      await axios.delete(`https://lms-backend-api-bnx4.onrender.com/results/${id}`);

      alert("Result Deleted Successfully");

      loadResults();

    } catch (error) {

      console.log(error);

      alert("Delete Failed");

    }

  };

  return (

    <div className="results-container">

      <h1>Result Management</h1>

      <div className="result-form">

        <select
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        >
          <option value="">Select Student</option>

          {
            students.map((student) => (

              <option
                key={student.student_id}
                value={student.student_id}
              >
                {student.name}
              </option>

            ))
          }

        </select>

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

        <input
          type="number"
          placeholder="Score"
          value={score}
          onChange={(e) => setScore(e.target.value)}
        />

        <input
          type="number"
          placeholder="Attempts"
          value={attempts}
          onChange={(e) => setAttempts(e.target.value)}
        />

        <input
          type="number"
          placeholder="Time Spent (Minutes)"
          value={timeSpent}
          onChange={(e) => setTimeSpent(e.target.value)}
        />

        <button
          onClick={
            editingId
              ? () => updateResult(editingId)
              : addResult
          }
        >
          {editingId ? "Update Result" : "Add Result"}
        </button>

      </div>

      <table>

        <thead>

          <tr>

            <th>ID</th>
            <th>Student</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>Attempts</th>
            <th>Time</th>
            <th>Edit</th>
            <th>Delete</th>

          </tr>

        </thead>

        <tbody>

          {

            results.map((result) => (

              <tr key={result.result_id}>

                <td>{result.result_id}</td>
                <td>{result.student_name}</td>
                <td>{result.quiz_title}</td>
                <td>{result.score}</td>
                <td>{result.attempts}</td>
                <td>{result.time_spent} min</td>

                <td>

                  <button
                    className="edit-btn"
                    onClick={() => editResult(result)}
                  >
                    Edit
                  </button>

                </td>

                <td>

                  <button
                    className="delete-btn"
                    onClick={() => deleteResult(result.result_id)}
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

export default Results;
