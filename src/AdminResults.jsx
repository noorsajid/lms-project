import axios from "axios";
import { useEffect, useState } from "react";
import "./AdminResults.css";

function AdminResults() {

  const [results, setResults] = useState([]);

  const loadStudentReports = async () => {

    try {

      const res = await axios.get(
        "https://lms-backend-api-bnx4.onrender.com/student-reports"
      );

      setResults(res.data);

    } catch (error) {

      console.log(error);
      alert("Unable to load student reports.");

    }

  };

  useEffect(() => {

    loadStudentReports();

  }, []);

  return (

    <div className="admin-results-container">

      <h1>Admin Result Report</h1>

      <table>

        <thead>

          <tr>

            <th>Student</th>
            <th>Email</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Status</th>
            <th>Attempts</th>
            <th>Time</th>

          </tr>

        </thead>

        <tbody>

          {

            results.map((result, index) => (

              <tr key={index}>

                <td>{result.name}</td>

                <td>{result.email}</td>

                <td>{result.title}</td>

                <td>{result.score}</td>

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

                <td>{result.attempts}</td>

                <td>{result.time_spent} sec</td>

              </tr>

            ))

          }

        </tbody>

      </table>

    </div>

  );

}

export default AdminResults;
