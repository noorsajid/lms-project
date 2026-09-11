import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./login.css";

function Login({ setIsLoggedIn }) {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {

    // Validation
    if (!email || !password) {
      alert("Please fill all fields ❌");
      return;
    }

    // -------------------------
    // Admin Login
    // -------------------------

    if (email === "admin@gmail.com" && password === "123") {

      alert("Admin Login Success 🎉");

      if (setIsLoggedIn) {
        setIsLoggedIn(true);
      }

      navigate("/admin-dashboard");

      return;
    }

    // -------------------------
    // Student Login (Database)
    // -------------------------

    try {

      const response = await axios.post(
        "https://lms-backend-06457.containers.snapdeploy.app",
        {
          email: email,
          password: password,
        }
      );

      alert(response.data.message);

      localStorage.setItem("student_id", response.data.student_id);
      localStorage.setItem("student_name", response.data.name);

      navigate("/student-dashboard");

    } catch (error) {

      console.log(error);

      alert("Wrong Credentials ❌");

    }

  };

  return (

    <div className="login-page">

      {/* NAVBAR */}

      <nav className="navbar">

        <h2 className="logo">AI Learn</h2>

        <ul>

          <li><Link to="/">Home</Link></li>

          <li><Link to="/about">About</Link></li>

          <li><Link to="/courses">Courses</Link></li>

          <li><Link to="/login">Login</Link></li>

          <li className="signup">
            <Link to="/signup">Sign Up</Link>
          </li>

        </ul>

      </nav>

      {/* Login Form */}

      <div className="container">

        <div className="card">

          <h2>Login Page</h2>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={handleLogin}>
            Login
          </button>

        </div>

      </div>

    </div>

  );
}

export default Login;
