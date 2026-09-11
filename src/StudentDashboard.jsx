import axios from "axios";
import { useEffect, useState } from "react";
import "./StudentDashboard.css";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
function StudentDashboard() {

  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [myCourses, setMyCourses] = useState([]);

  const studentId = localStorage.getItem("student_id");
  const studentName = localStorage.getItem("student_name");

  // eslint-disable-next-line react-hooks/exhaustive-deps
useEffect(() => {

    loadCourses();
    loadMyCourses();

}, []);

  // Load all available courses
  const loadCourses = async () => {

    try {

      const res = await axios.get("http://localhost:5000/courses");

      setCourses(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  // Load enrolled courses
  const loadMyCourses = async () => {

    try {

      const res = await axios.get(
        `http://localhost:5000/enrollments/${studentId}`
      );

      setMyCourses(res.data);

    } catch (error) {

      console.log(error);

    }

  };

  // Enroll Course
  const enrollCourse = async (courseId) => {

    try {

      const res = await axios.post(
        "http://localhost:5000/enrollments",
        {

          student_id: studentId,
          course_id: courseId,

        }
      );

      alert(res.data.message);

      loadMyCourses();

    } catch (error) {

      if (error.response) {
        alert(error.response.data.message);
      } else {
        alert("Enrollment Failed");
      }

    }

  };

  return (

    <div className="student-dashboard">

        <div className="dashboard-header">

            <div className="dashboard-buttons">

                <button onClick={() => navigate("/student-results")}>
                    📊 Results
                </button>

                <button onClick={() => navigate("/announcements")}>
                    📢 Announcements
                </button>
              
              <button onClick={() => navigate("/prediction")}>
                🤖 AI Prediction
                </button>
            </div>

            <h2>
                Welcome, {studentName}
            </h2>

        </div>


      <h2>Available Courses</h2>

      <div className="course-grid">

        {
          courses.map((course) => (

            <div className="course-card" key={course.course_id}>

              <h3>{course.course_name}</h3>

              <p>{course.description}</p>

              <p>
                <b>Difficulty:</b> {course.difficulty_level}
              </p>

              <p>
                <b>Duration:</b> {course.duration}
              </p>

              <button
                onClick={() => enrollCourse(course.course_id)}
              >
                Enroll
              </button>

            </div>

          ))
        }

      </div>

      <h2 style={{ marginTop: "40px" }}>
        My Courses
      </h2>

      <table>

        <thead>

          <tr>

            <th>ID</th>
            <th>Course Name</th>
            <th>Description</th>
            <th>Difficulty</th>
            <th>Duration</th>
            <th>Watch Material</th>

          </tr>

        </thead>

        <tbody>

          {
            myCourses.map((course) => (

              <tr key={course.enrollment_id}>

                <td>{course.course_id}</td>

                <td>{course.course_name}</td>

                <td>{course.description}</td>

                <td>{course.difficulty_level}</td>

                <td>{course.duration}</td>

                  <td>
  <Link to={`/course-material/${course.course_id}`}>
    <button className="watch-btn">
      Watch Material
    </button>
  </Link>
</td>

              </tr>

            ))
          }

        </tbody>

      </table>

    </div>
    

  );

}

export default StudentDashboard;