import "./AdminDashboard.css";
import { useEffect, useState } from "react";
import axios from "axios";
import { FaSignOutAlt } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";

import {
  FaUserGraduate,
  FaBook,
  FaClipboardList,
  FaQuestionCircle,
  FaChartLine,
  FaRobot,
  FaUsers,
  FaCog,
  FaHome,
  FaClipboardCheck
} from "react-icons/fa";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

function AdminDashboard() {

  const [analytics, setAnalytics] = useState({
    average_score:0,
    average_percentage:0,
    attempts:0,
    passed:0,
    failed:0
});

  // Dashboard Cards
  const [dashboard, setDashboard] = useState({
    students: 0,
    courses: 0,
    quizzes: 0,
    questions: 0,
    attempts: 0,
    predictions: 0
  });

  // AI Pie Chart
  const [predictionChart, setPredictionChart] = useState([]);

  const loadAnalytics = async () => {

    try{

        const res = await axios.get(
            "https://lms-backend-api-bnx4.onrender.com/quiz-analytics"
        );

        setAnalytics(res.data);

    }

    catch(error){

        console.log(error);

    }

};
  // -----------------------------
  // Load Dashboard Statistics
  // -----------------------------
  const loadDashboard = async () => {

    try {

      const res = await axios.get(
        "https://lms-backend-api-bnx4.onrender.com/admin-dashboard"
      );

      setDashboard(res.data);

    } catch (error) {

      console.log(error);

    }

  };
  //---------------------------------------------------------LOGOUT-----------------------------------------
  const navigate = useNavigate();

const handleLogout = () => {

    localStorage.removeItem("user");
    localStorage.removeItem("token");

    navigate("/login");

};
  // ----------------------------------------------------------------------
  // Load Prediction Pie Chart
  // -----------------------------
  const loadPredictionChart = async () => {

    try {

      const res = await axios.get(
        "https://lms-backend-api-bnx4.onrender.com/prediction-chart"
      );

      setPredictionChart(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  useEffect(() => {

    loadDashboard();
    loadPredictionChart();
    loadAnalytics();

  }, []);

  // -----------------------------
  // Bar Chart Data
  // -----------------------------
  const chartData = [

    {
      name: "Students",
      value: dashboard.students
    },

    {
      name: "Courses",
      value: dashboard.courses
    },

    {
      name: "Quizzes",
      value: dashboard.quizzes
    },

    {
      name: "Questions",
      value: dashboard.questions
    },

    {
      name: "Attempts",
      value: dashboard.attempts
    },

    {
      name: "Predictions",
      value: dashboard.predictions
    }

  ];

  // -----------------------------
  // Pie Chart Colors
  // -----------------------------
  const COLORS = [

    "#22c55e", // Excellent
    "#3b82f6", // Good
    "#f59e0b", // Average
    "#ef4444"  // At Risk

  ];
  return (

<div className="dashboard">

  {/* Sidebar */}

  <div className="sidebar">

    <h2>AI Learn</h2>

    <ul>

      <li>
        <Link to="/admin-dashboard" className="sidebar-link">
          <FaHome /> Dashboard
        </Link>
      </li>

      <li>
        <Link to="/students" className="sidebar-link">
          <FaUsers /> Students
        </Link>
      </li>

      <li>
        <Link to="/courses" className="sidebar-link">
          <FaBook /> Courses
        </Link>
      </li>

      <li>
        <Link to="/quizzes" className="sidebar-link">
          <FaClipboardList /> Quizzes
        </Link>
      </li>

      <li>
        <Link to="/questions" className="sidebar-link">
          <FaQuestionCircle /> Questions
        </Link>
      </li>

      <li>
        <Link to="/results" className="sidebar-link">
          <FaClipboardCheck /> Results
        </Link>
      </li>

      <li>
        <Link to="/adminAnnouncements" className="sidebar-link">
          <FaRobot /> Announcements
        </Link>
      </li>

      <li>
        <Link to="/reports" className="sidebar-link">
          <FaChartLine /> Reports
        </Link>
      </li>
      <li>

<Link
    to="/login"
    className="sidebar-link"
    onClick={() => {

        localStorage.removeItem("user");
        localStorage.removeItem("token");

    }}
>

<FaSignOutAlt /> Logout

</Link>

</li>

    </ul>

  </div>

  {/* Main */}

  <div className="main">

    <div className="header">

      <h1>Admin Dashboard</h1>

    </div>

    {/* Dashboard Cards */}

    <div className="cards">

      <div className="card">
        <FaUserGraduate className="icon" />
        <h2>{dashboard.students}</h2>
        <p>Total Students</p>
      </div>

      <div className="card">
        <FaBook className="icon" />
        <h2>{dashboard.courses}</h2>
        <p>Total Courses</p>
      </div>

      <div className="card">
        <FaClipboardList className="icon" />
        <h2>{dashboard.quizzes}</h2>
        <p>Total Quizzes</p>
      </div>

      <div className="card">
        <FaQuestionCircle className="icon" />
        <h2>{dashboard.questions}</h2>
        <p>Total Questions</p>
      </div>

      <div className="card">
        <FaClipboardCheck className="icon" />
        <h2>{dashboard.attempts}</h2>
        <p>Quiz Attempts</p>
      </div>

      <div className="card">
        <FaRobot className="icon" />
        <h2>{dashboard.predictions}</h2>
        <p>AI Predictions</p>
      </div>

    </div>

  

    {/* Bar Chart */}

    <div className="chart-container">

      <h2>📊 LMS Analytics</h2>

      <ResponsiveContainer width="100%" height={350}>

        <BarChart data={chartData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="name" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="value"
            fill="#6366F1"
          />

        </BarChart>

      </ResponsiveContainer>

    </div>

    {/* Pie Chart */}

    <div className="chart-container">

      <h2>🤖 AI Prediction Analytics</h2>

      <ResponsiveContainer width="100%" height={350}>

        <PieChart>

          <Pie
            data={predictionChart}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label
          >

            {

              predictionChart.map((entry, index) => (

                <Cell
                  key={index}
                  fill={COLORS[index % COLORS.length]}
                />

              ))

            }

          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </ResponsiveContainer>

      <div className="chart-container">

<h2>📈 Quiz Analytics</h2>

<ResponsiveContainer width="100%" height={350}>

<BarChart

data={[

{
name:"Average Score",
value:analytics.average_score
},

{
name:"Average %",
value:analytics.average_percentage
},

{
name:"Attempts",
value:analytics.attempts
},

{
name:"Passed",
value:analytics.passed
},

{
name:"Failed",
value:analytics.failed
}

]}

>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Bar
dataKey="value"
fill="#10b981"
/>

</BarChart>

</ResponsiveContainer>

</div>

    </div>

    
</div>

</div>

  );

}

export default AdminDashboard;
