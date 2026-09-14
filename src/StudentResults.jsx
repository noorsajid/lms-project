import axios from "axios";
import { useEffect, useState } from "react";
import "./StudentResults.css";

function StudentResults() {

  const [results, setResults] = useState([]);

  const studentId = localStorage.getItem("student_id");

  useEffect(() => {

    const loadResults = async () => {

      try {

        const res = await axios.get(
          `https://lms-backend-api-bnx4.onrender.com/student-results/${studentId}`
        );

        setResults(res.data);

      } catch (error) {

        console.log(error);
        alert("Unable to load results.");

      }

    };

    loadResults();

  }, [studentId]);

  return (

    <div className="results-container">

      <h1>My Quiz Results</h1>

      <table>

        <thead>

          <tr>

            <th>Quiz</th>
            <th>Score</th>
            <th>Attempts</th>
            <th>Time</th>
            <th>Percentage</th>
            <th>Status</th>
            <th>Recommendation</th>

          </tr>

        </thead>

        <tbody>

          {

            results.map((result) => (

              <tr key={result.result_id}>

                <td>{result.quiz_name}</td>

                <td>{result.score}</td>

                <td>{result.attempts}</td>

                <td>{result.time_spent} sec</td>

                <td>{result.percentage}%</td>

                <td>

                  <span
                    className={
                      result.status === "Pass"
                        ? "pass"
                        : "fail"
                    }
                  >
                    {result.status}
                  </span>

                </td>
                <td>{result.recommendation}</td>
              </tr>

            ))

          }

        </tbody>

      </table>

    </div>

  );

}

export default StudentResults;
