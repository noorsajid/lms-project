import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./CourseMaterial.css";

function CourseMaterial() {

  const { id } = useParams();
  const navigate = useNavigate();

  const [course, setCourse] = useState({});

  // Start Quiz
  const startQuiz = async () => {
    try {

      const res = await axios.get(
        `https://lms-backend-api-bnx4.onrender.com/quiz-by-course/${course.course_id}`
      );

      console.log("Quiz Response:", res.data);

      navigate(`/student-quiz/${res.data.quiz_id}`);

    } catch (error) {

      console.log(error);

      alert("Quiz not found.");

    }
  };


  // Load Course
  useEffect(() => {

    const loadCourse = async () => {

      try {

        const res = await axios.get(
          `https://lms-backend-api-bnx4.onrender.com/courses/${id}`
        );

        console.log("Course Response:", res.data);

        setCourse(res.data);

        // Update AI activity
        await axios.post(
          "https://lms-backend-api-bnx4.onrender.com/update-resource",
          {
            student_id: localStorage.getItem("student_id"),
            course_id: res.data.course_id
          }
        );

      } catch (error) {

        console.log(error);

        alert("Unable to load course material.");

      }

    };

    loadCourse();

  }, [id]);


  // Convert YouTube URL into Embed URL
  const getYoutubeEmbedUrl = (url) => {

    if (!url) {
      return null;
    }

    // YouTube short URL
    // https://youtu.be/Znmz_WxMxp4?si=xxxxx

    if (url.includes("youtu.be/")) {

      const videoId = url
        .split("youtu.be/")[1]
        .split("?")[0];

      return `https://www.youtube.com/embed/${videoId}`;

    }

    // YouTube watch URL
    // https://www.youtube.com/watch?v=Znmz_WxMxp4

    if (url.includes("watch?v=")) {

      const videoId = url
        .split("watch?v=")[1]
        .split("&")[0];

      return `https://www.youtube.com/embed/${videoId}`;

    }

    // Already an embed URL
    if (url.includes("youtube.com/embed/")) {

      return url.split("?")[0];

    }

    return null;
  };


  const videoUrl = getYoutubeEmbedUrl(course.youtube_link);


  return (

    <div className="material-container">

      <h1>{course.course_name}</h1>


      <div className="course-info">

        <p>
          <strong>Difficulty:</strong>{" "}
          {course.difficulty_level}
        </p>

        <p>
          <strong>Duration:</strong>{" "}
          {course.duration}
        </p>

      </div>


      {/* Course Video */}

      <div className="video-container">

        {videoUrl ? (

          <iframe
            src={videoUrl}
            title={`${course.course_name} Course Video`}
            width="100%"
            height="500"
            frameBorder="0"
            style={{
              border: "2px solid #ddd",
              borderRadius: "12px",
              display: "block"
            }}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          ></iframe>

        ) : (

          <div className="no-video">
            <p>No course video available.</p>
          </div>

        )}

      </div>


      {/* Course Description */}

      <div className="description">

        <h2>Course Description</h2>

        <p>{course.description}</p>

      </div>


      {/* Start Quiz */}

      <button
        className="quiz-btn"
        onClick={startQuiz}
      >
        Start Quiz
      </button>

    </div>

  );

}

export default CourseMaterial;
