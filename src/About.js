import { Link } from "react-router-dom";
import "./about.css";

function About() {
  return (
    <div className="about">

      {/* NAVBAR */}
      <nav className="navbar">

        <h2 className="logo">AI Learn</h2>

        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li className="signup"><Link to="/signup">Sign Up</Link></li>
        </ul>

      </nav>

      {/* HERO */}
      <section className="about-hero">
        <h1>About AI Learn</h1>
        <p>
          AI Learn is a smart learning platform designed to help students
          improve skills through personalized AI-based recommendations.
        </p>
      </section>

      {/* MISSION */}
      <section className="about-section">
        <h2>🎯 Our Mission</h2>
        <p>
          Our mission is to transform education by making it personalized,
          accessible, and intelligent.
        </p>
      </section>

      {/* CARDS */}
      <section className="about-cards">

        <div className="info-card">
          <h3>🧠 AI Recommendation</h3>
          <p>Suggests courses based on student performance</p>
        </div>

        <div className="info-card">
          <h3>📊 Progress Tracking</h3>
          <p>Tracks learning progress</p>
        </div>

        <div className="info-card">
          <h3>📚 Smart Courses</h3>
          <p>Adaptive learning system</p>
        </div>

      </section>
 {/* TEAM / INFO */}
<section className="about-section">
  <h2>🌍 Why This Platform?</h2>
  <p>
    Traditional learning systems follow a fixed structure, but every
    student learns differently. Our platform uses AI to customize
    learning for each student, improving engagement and success rate.
  </p>

  {/* CARDS */}
  <div className="about-cards">
    <div className="info-card">
      <img
        src="https://img.freepik.com/free-vector/online-certification-illustration_23-2148575636.jpg"
        alt="education"
      />
      <h3>📚 Smart Education</h3>
      <p>
        Our AI-powered system helps students learn according
        to their own pace with interactive lessons and quizzes.
      </p>
    </div>
    <div className="info-card">
      <img
        src="https://img.freepik.com/free-vector/artificial-intelligence-concept-illustration_114360-7000.jpg"
        alt="ai"
      />
      <h3>🤖 AI Recommendations</h3>
      <p>
        The platform analyzes student performance and recommend spersonalized courses and study material automatically.
      </p>
    </div>
    <div className="info-card">
      <img
        src="https://img.freepik.com/free-vector/students-learning-online-course_74855-5513.jpg"
        alt="students"
      />
      <h3>🎯 Student Success</h3>
      <p>
        Students improve their skills, time management,
        confidence and career opportunities through digital learning.
      </p>
    </div></div>
</section>

{/* FOOTER */}
<footer className="footer">

  <div className="footer-container">

    <div className="footer-col">
      <h2>AI Learn</h2>
      <p>
        Smart AI-based learning platform that helps students improve
        skills and achieve success through personalized education.
      </p>
    </div>

    <div className="footer-col">
      <h3>Quick Links</h3>
      <ul>
        <li>Home</li>
        <li>About</li>
        <li>Courses</li>
        <li>Login</li>
      </ul>
    </div>

    <div className="footer-col">
      <h3>Top Courses</h3>
      <ul>
        <li>Web Development</li>
        <li>Python</li>
        <li>AI / ML</li>
        <li>UI/UX Design</li>
      </ul>
    </div>

    <div className="footer-col">
      <h3>Contact</h3>
      <p>Email: info@ailearn.com</p>
      <p>Phone: +92 300 1234567</p>
    </div>

  </div>

  <div className="footer-bottom">
    <p>© 2026 AI Learn | All Rights Reserved</p>
  </div>

</footer>
    </div>
  );
}

export default About;