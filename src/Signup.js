import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./login.css";

function Signup() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {

    if (!name || !email || !password) {
      alert("Please Fill All Fields ❌");
      return;
    }

    try {

      await axios.post("http://localhost:5000/student-signup", {

        name: name,
        email: email,
        password: password

      });

      alert("Account Created Successfully 🎉");

      setName("");
      setEmail("");
      setPassword("");

      navigate("/login");

    } catch (error) {

      console.log(error);

      alert("Registration Failed");

    }

  };

  return (

    <div className="login-page">

      {/* NAVBAR */}

      <nav className="navbar">

        <h2 className="logo">AI Learn</h2>

        <ul>

          <li>
            <Link to="/">Home</Link>
          </li>

          <li>
            <Link to="/about">About</Link>
          </li>

          <li>
            <Link to="/courses">Courses</Link>
          </li>

          <li>
            <Link to="/login">Login</Link>
          </li>

          <li className="signup">
            <Link to="/signup">Sign Up</Link>
          </li>

        </ul>

      </nav>

      {/* SIGNUP FORM */}

      <div className="container">

        <div className="card">

          <h2>Student Sign Up</h2>

          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

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

          <button onClick={handleSignup}>
            Create Account
          </button>

          <p style={{ marginTop: "15px", textAlign: "center" }}>
            Already have an account?{" "}
            <Link to="/login">Login</Link>
          </p>

        </div>

      </div>

    </div>

  );

}

export default Signup;