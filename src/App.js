import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import Login from "./Login";
import Signup from "./Signup";
import AdminDashboard from "./AdminDashboard";
import Courses from "./Courses";
import Quiz from "./Quiz";
import Questions from "./Questions";
import Results from "./Results";
import StudentDashboard from "./StudentDashboard";
import CourseMaterial from "./CourseMaterial";
import StudentQuiz from "./StudentQuiz";
import StudentResults from "./StudentResults";
import AdminResults from "./AdminResults";
import Announcements from "./Announcements";
import AdminAnnouncements from "./AdminAnnouncements";
import StudentPrediction from "./StudentPrediction";
import Reports from "./Reports";
import Students from "./students";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Home />} />

        <Route path="/about" element={<About />} />

        <Route path="/login" element={<Login />} />

        <Route path="/signup" element={<Signup />} />

        {/* Admin Dashboard */}
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
       
        <Route path="/courses" element={<Courses />} />
        
        <Route path="/quizzes"  element={<Quiz />} />
        
        <Route path="/questions" element={<Questions />} />

        <Route path="/results" element={<Results />} />
       
       <Route path="/student-dashboard" element={<StudentDashboard />}/>

       <Route path="/course-material/:id" element={<CourseMaterial />} />

       <Route path="/student-quiz/:id" element={<StudentQuiz />}/>

       <Route path="/student-results"element={<StudentResults />}/>

       <Route path="/admin-results" element={<AdminResults />} />

       <Route path="/announcements"element={<Announcements />}/>

       <Route path="/adminannouncements"element={<AdminAnnouncements />}/>
        
      <Route path="/prediction" element={<StudentPrediction />}/>

      <Route path="/reports" element={<Reports />} />

      <Route path="/students" element={<Students />} />

      </Routes>

    </BrowserRouter>
  );
}

export default App;