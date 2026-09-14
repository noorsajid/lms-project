import axios from "axios";
import { useEffect, useState } from "react";
import "./Quiz.css";

function Quiz() {

const [quizzes,setQuizzes]=useState([]);
const [courses,setCourses]=useState([]);

const [courseId,setCourseId]=useState("");
const [title,setTitle]=useState("");
const [totalMarks,setTotalMarks]=useState("");
const [timeLimit,setTimeLimit]=useState("");
const [passingMarks,setPassingMarks]=useState("");

const [editingId,setEditingId]=useState(null);

useEffect(()=>{

loadQuizzes();
loadCourses();

},[]);

const loadCourses = async () => {

try{

const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/courses");

setCourses(res.data);

}catch(error){

console.log(error);

}

}

const loadQuizzes = async () => {

try{

const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/quizzes");

setQuizzes(res.data);

}catch(error){

console.log(error);

}

}

const addQuiz=async()=>{

await axios.post("https://lms-backend-api-bnx4.onrender.com/quizzes",{

course_id:courseId,
title:title,
total_marks:totalMarks,
time_limit:timeLimit,
passing_marks:passingMarks

});

alert("Quiz Added");

clearForm();

loadQuizzes();

}

const editQuiz=(quiz)=>{

setEditingId(quiz.quiz_id);

setCourseId(quiz.course_id);
setTitle(quiz.title);
setTotalMarks(quiz.total_marks);
setTimeLimit(quiz.time_limit);
setPassingMarks(quiz.passing_marks);

}

const updateQuiz=async(id)=>{

await axios.put(`https://lms-backend-api-bnx4.onrender.com/quizzes/${id}`,{

course_id:courseId,
title:title,
total_marks:totalMarks,
time_limit:timeLimit,
passing_marks:passingMarks

});

alert("Quiz Updated");

clearForm();

loadQuizzes();

}

const deleteQuiz=async(id)=>{

await axios.delete(`https://lms-backend-api-bnx4.onrender.com/quizzes/${id}`);

alert("Quiz Deleted");

loadQuizzes();

}

const clearForm=()=>{

setEditingId(null);

setCourseId("");
setTitle("");
setTotalMarks("");
setTimeLimit("");
setPassingMarks("");

}

return(

<div className="quiz-container">

<h1>Quiz Management</h1>

<div className="quiz-form">

<select
value={courseId}
onChange={(e)=>setCourseId(e.target.value)}
>

<option value="">Select Course</option>

{
courses.map(course=>(

<option
key={course.course_id}
value={course.course_id}
>

{course.course_name}

</option>

))
}

</select>

<input
type="text"
placeholder="Quiz Title"
value={title}
onChange={(e)=>setTitle(e.target.value)}
/>

<input
type="number"
placeholder="Total Marks"
value={totalMarks}
onChange={(e)=>setTotalMarks(e.target.value)}
/>

<input
type="number"
placeholder="Time Limit (Minutes)"
value={timeLimit}
onChange={(e)=>setTimeLimit(e.target.value)}
/>

<input
type="number"
placeholder="Passing Marks"
value={passingMarks}
onChange={(e)=>setPassingMarks(e.target.value)}
/>

<button
onClick={editingId ? ()=>updateQuiz(editingId):addQuiz}
>

{editingId ? "Update Quiz":"Add Quiz"}

</button>

</div>

<table>

<thead>

<tr>

<th>ID</th>
<th>Course</th>
<th>Title</th>
<th>Total</th>
<th>Time</th>
<th>Passing</th>
<th>Edit</th>
<th>Delete</th>

</tr>

</thead>

<tbody>

{

quizzes.map((quiz)=>(

<tr key={quiz.quiz_id}>

<td>{quiz.quiz_id}</td>
<td>{quiz.course_name}</td>
<td>{quiz.title}</td>
<td>{quiz.total_marks}</td>
<td>{quiz.time_limit}</td>
<td>{quiz.passing_marks}</td>

<td>

<button
className="edit-btn"
onClick={()=>editQuiz(quiz)}
>

Edit

</button>

</td>

<td>

<button
className="delete-btn"
onClick={()=>deleteQuiz(quiz.quiz_id)}
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

export default Quiz;
