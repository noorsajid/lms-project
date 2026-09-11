import { useEffect, useState } from "react";
import axios from "axios";
import "./students.css";

function Students() {

  const [reports, setReports] = useState([]);
  const [filteredReports, setFilteredReports] = useState([]);

  useEffect(() => {

    loadStudentReports();

  }, []);

  const loadStudentReports = async () => {

    try {

      const res = await axios.get(
        "http://localhost:5000/student-reports"
      );

      setReports(res.data);
      setFilteredReports(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  return (

    <div className="students-container">

      <h1>Students</h1>

      <table className="report-table">

        <thead>

          <tr>

            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>%</th>
            <th>Status</th>
            <th>Attempts</th>
            <th>Time</th>

          </tr>

        </thead>

        <tbody>

          {

            filteredReports.length > 0 ?

              filteredReports.map((item, index) => (

                <tr key={index}>

                  <td>{item.student_id}</td>

                  <td>{item.name}</td>

                  <td>{item.email}</td>

                  <td>{item.title}</td>

                  <td>{item.score}</td>

                  <td>{item.percentage}%</td>

                  <td>

                    <span
                      className={
                        item.status === "Pass"
                          ? "pass"
                          : "fail"
                      }
                    >

                      {item.status}

                    </span>

                  </td>

                  <td>{item.attempts}</td>

                  <td>{item.time_spent} sec</td>

                </tr>

              ))

              :

              <tr>

                <td
                  colSpan="9"
                  style={{ textAlign: "center" }}
                >

                  No Records Found

                </td>

              </tr>

          }

        </tbody>

      </table>

    </div>

  );

}

export default Students;