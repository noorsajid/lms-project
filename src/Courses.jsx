import axios from "axios";
import { useEffect, useState } from "react";
import "./Courses.css";

function Courses() {

  const [courses, setCourses] = useState([]);

  const [courseName, setCourseName] = useState("");
  const [description, setDescription] = useState("");
  const [difficultyLevel, setDifficultyLevel] = useState("");
  const [duration, setDuration] = useState("");
  const [youtubeLink, setYoutubeLink] = useState("");

  const [editingId, setEditingId] = useState(null);
  // Load courses when page opens
  useEffect(() => {
    loadCourses();
  }, []);

  // Get all courses from database
  const loadCourses = async () => {
    try {

      const response = await axios.get("https://lms-backend-api-bnx4.onrender.com/courses");

      setCourses(response.data);

    } catch (error) {
      console.log(error);
      alert("Unable to load courses");
    }
  };

  // Add Course
  const addCourse = async () => {

    if (
      courseName === "" ||
      description === "" ||
      difficultyLevel === "" ||
      duration === ""
      
    ) {
      alert("Please fill all fields");
      return;
    }

    try {

      await axios.post("https://lms-backend-api-bnx4.onrender.com/courses", {

        course_name: courseName,
        description: description,
        difficulty_level: difficultyLevel,
        duration: duration,
        youtube_link: youtubeLink,
      });

      alert("Course Added Successfully");

      setCourseName("");
      setDescription("");
      setDifficultyLevel("");
      setDuration("");

      loadCourses();

    } catch (error) {

      console.log(error);
      alert("Error Adding Course");

    }

  };

  // Update Course 

  // Edit Course
const editCourse = (course) => {

  setEditingId(course.course_id);

  setCourseName(course.course_name);
  setDescription(course.description);
  setDifficultyLevel(course.difficulty_level);
  setDuration(course.duration);
  setYoutubeLink(course.youtube_link);
};

// Update Course
const updateCourse = async (id) => {

  try {

    await axios.put(`https://lms-backend-api-bnx4.onrender.com/courses/${id}`, {

      course_name: courseName,
      description: description,
      difficulty_level: difficultyLevel,
      duration: duration,
      youtube_link: youtubeLink,

    });

    alert("Course Updated Successfully");

    setEditingId(null);

    setCourseName("");
    setDescription("");
    setDifficultyLevel("");
    setDuration("");

    loadCourses();

  } catch (error) {

    console.log(error);
    alert("Update Failed");

  }

};
  // Delete Course
  const deleteCourse = async (id) => {

    try {

      await axios.delete(`https://lms-backend-api-bnx4.onrender.com/courses/${id}`);

      alert("Course Deleted");

      loadCourses();

    } catch (error) {

      console.log(error);
      alert("Delete Failed");

    }

  };
  return (

    <div className="courses-container">

      <h1>Course Management</h1>

      <div className="course-form">

        <input
          type="text"
          placeholder="Course Name"
          value={courseName}
          onChange={(e) => setCourseName(e.target.value)}
        />

        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>

        <select
          value={difficultyLevel}
          onChange={(e) => setDifficultyLevel(e.target.value)}
        >

          <option value="">Select Difficulty</option>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>

        </select>

        <input
          type="text"
          placeholder="Duration (Example: 6 Weeks)"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
        />

        <input
        type="text"
        placeholder="YouTube Embed Link"
        value={youtubeLink}
        onChange={(e) => setYoutubeLink(e.target.value)}
        />

       <button
  onClick={editingId ? () => updateCourse(editingId) : addCourse}
>
  {editingId ? "Update Course" : "Add Course"}
</button>

      </div>

      <table>

        <thead>

          <tr>

            <th>ID</th>

            <th>Course Name</th>

            <th>Description</th>

            <th>Difficulty</th>

            <th>Duration</th>

            <th>Update</th>

             <th>Delete</th>

          </tr>

        </thead>

        <tbody>

          {
            courses.map((course) => (

              <tr key={course.course_id}>

                <td>{course.course_id}</td>

                <td>{course.course_name}</td>

                <td>{course.description}</td>

                <td>{course.difficulty_level}</td>

                <td>{course.duration}</td>

                  <td>

                  <button
                     className="edit-btn"
                     onClick={() => editCourse(course)}
                     >
                        Edit
                    </button>
                    </td>
                    <td>
  <button
    className="delete-btn"
    onClick={() => deleteCourse(course.course_id)}
  >
    Delete
  </button>

</td>

                

              </tr>

            ))
          }

        </tbody>

      </table>

    </div>

  );

}

export default Courses;
