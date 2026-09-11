import axios from "axios";
import { useEffect, useState } from "react";
import "./StudentPrediction.css";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function StudentPrediction() {

  const [prediction, setPrediction] = useState(null);

  const studentId = localStorage.getItem("student_id");

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {

    loadPrediction();

  }, []);

  const loadPrediction = async () => {

    try {

      const res = await axios.get(
        `http://localhost:5000/predict-performance/${studentId}`
      );

      setPrediction(res.data);

    }
    catch (error) {

      console.log(error);

      alert("Unable to load prediction.");

    }

  };

  if (!prediction) {

    return <h2 style={{ padding: "30px" }}>Loading...</h2>;

  }

  // ----------------------------
  // Chart Data
  // ----------------------------

  const chartData = [

    {
      name: "Resources",
      value: prediction.visited_resources
    },

    {
      name: "Announcements",
      value: prediction.announcements_view
    },

    {
      name: "Learning",
      value: prediction.visited_resources
    },

    {
      name: "Participation",
      value: prediction.raised_hands
    },

    {
      name: "Login",
      value: prediction.login_count
    }

  ];

  return (

    <div className="prediction-container">

      <h1>🤖 AI Performance Prediction</h1>

      {/* Prediction */}

      <div className="prediction-card">

        <h2>

          Prediction :

          <span className="prediction-result">

            {prediction.performance}

          </span>

        </h2>

        <p>
          <br></br>
          <strong>Recommendation:</strong>

          <br />

          {prediction.recommendation}

        </p>

      </div>

      {/* Activity Table */}

      <div className="activity-card">

        <h2>📊 Activity Statistics</h2>

        <table>

          <tbody>

            <tr>

              <td>Visited Resources</td>

              <td>{prediction.visited_resources}</td>

            </tr>

            <tr>

              <td>Announcements Viewed</td>

              <td>{prediction.announcements_view}</td>

            </tr>

            <tr>

              <td>Discussion Activity</td>

              <td>{prediction.visited_resources}</td>

            </tr>

            <tr>

              <td>Quiz Participation</td>

              <td>{prediction.raised_hands}</td>

            </tr>

            <tr>

              <td>Login Count</td>

              <td>{prediction.login_count}</td>

            </tr>

          </tbody>

        </table>

      </div>

      {/* Chart */}

      <div className="chart-card">

        <h2>📈 Performance Analytics</h2>

        <ResponsiveContainer width="100%" height={350}>

          <BarChart data={chartData}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="value"
              fill="#4f46e5"
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

      {/* Recommended Courses */}

      <div className="course-card-ai">

        <h2>📚 Recommended Courses</h2>

        <ul>

          {prediction.recommended_courses.map((course, index) => (

            <li key={index}>

              {course}

            </li>

          ))}

        </ul>

      </div>

    </div>

  );

}

export default StudentPrediction;