import { Link } from "react-router-dom";
import "./home.css";
import myImage from "./assets/Online Image.png";

import {
  FaBrain,
  FaClock,
  FaGraduationCap,
  FaGlobe,
} from "react-icons/fa";

const features = [
  {
    icon: <FaBrain />,
    title: "Smart Learning System",
    text: "AI powered learning helps students improve understanding and self study.",
  },

  {
    icon: <FaClock />,
    title: "Time Management",
    text: "Students learn discipline and better time control through online learning.",
  },

  {
    icon: <FaGraduationCap />,
    title: "Education Impact",
    text: "Better education leads to higher income, skills and opportunities.",
  },

  {
    icon: <FaGlobe />,
    title: "E-Learning Growth",
    text: "Pakistan is growing in digital education through mobile learning.",
  },
];

const courses = [
  {
    title: "Web Development",
    desc: "HTML, CSS, JavaScript, React complete course",
    img: "https://img.freepik.com/free-vector/programming-concept-illustration_114360-1351.jpg",
    rating: "4.8",
    duration: "6 Weeks",
  },

  {
    title: "Python Programming",
    desc: "Beginner to advanced Python training",
    img: "https://img.freepik.com/free-vector/coding-concept-illustration_114360-939.jpg",
    rating: "4.7",
    duration: "5 Weeks",
  },

  {
    title: "AI & Machine Learning",
    desc: "Learn ML algorithms and AI basics",
    img: "https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-8023.jpg",
    rating: "4.9",
    duration: "8 Weeks",
  },

  {
    title: "UI/UX Design",
    desc: "Design modern user interfaces",
    img: "https://img.freepik.com/free-vector/ui-ux-concept-illustration_114360-810.jpg",
    rating: "4.6",
    duration: "4 Weeks",
  },
];

function Home() {
  return (
    <div className="home">

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
            <Link to="/login">Login</Link>
          </li>

          <li className="signup">
            <Link to="/signup">Sign Up</Link>
          </li>

        </ul>

      </nav>

      {/* HERO SECTION */}
      <section className="hero">

        <div className="left">

          <h1>Smart Learning with AI</h1>

          <p>
            Personalized learning with quizzes, AI recommendations,
            and performance tracking.
          </p>

          <div className="buttons">

            <button className="primary">
              Get Started
            </button>

            <button className="outline">
              Explore
            </button>

          </div>

        </div>

        <div className="right">
          <img src={myImage} alt="learning" />
        </div>

      </section>

      {/* FEATURES */}
      <section className="features">

        <h2>Why Choose Us</h2>

        <div className="features-grid">

          {features.map((f, i) => (

            <div className="feature-card" key={i}>

              <div className="icon">{f.icon}</div>

              <h3>{f.title}</h3>

              <p>{f.text}</p>

            </div>

          ))}

        </div>

      </section>

      {/* COURSES */}
      <section className="courses">

        <h2>Popular Courses</h2>

        <div className="course-cards">

          {courses.map((course, index) => (

            <div className="course-card" key={index}>

              <img src={course.img} alt="course" />

              <h3>{course.title}</h3>

              <p>{course.desc}</p>

              <div className="info">

                <span>⭐ {course.rating}</span>

                <span>⏱ {course.duration}</span>

              </div>

              <button>Start Learning</button>

            </div>

          ))}

        </div>

      </section>

      {/* STATS */}
      <section className="stats">

        <div>
          <h1>10K+</h1>
          <p>Students</p>
        </div>

        <div>
          <h1>500+</h1>
          <p>Courses</p>
        </div>

        <div>
          <h1>95%</h1>
          <p>Success Rate</p>
        </div>

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

export default Home;