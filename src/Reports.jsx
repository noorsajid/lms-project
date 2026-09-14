import { useEffect, useState } from "react";
import axios from "axios";
import "./Reports.css";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

function Reports() {

  // ===============================
  // Dashboard Summary
  // ===============================

  const [report, setReport] = useState({
    students: 0,
    courses: 0,
    quizzes: 0,
    attempts: 0,
    average_score: 0,
    average_percentage: 0,
    passed: 0,
    failed: 0
  });

  // ===============================
  // Student Reports
  // ===============================

  const [reports, setReports] = useState([]);

  const [filteredReports, setFilteredReports] = useState([]);

  const [search, setSearch] = useState("");

  // ===============================
  // Load Dashboard Summary
  // ===============================

  const loadReport = async () => {

    try {

      const res = await axios.get(
        "https://lms-backend-api-bnx4.onrender.com/reports-summary"
      );

      setReport(res.data);

    }

    catch (error) {

      console.log(error);

    }

  };

  // ===============================
  // Load Student Reports
  // ===============================

  const loadStudentReports = async () => {

    try {

    const res = await axios.get("https://lms-backend-api-bnx4.onrender.com/student-reports");

    console.log("Student Reports:", res.data);

    setReports(res.data);
    setFilteredReports(res.data);

  } catch (error) {

    console.log(error);

  }

};


  // ===============================
  // Initial Load
  // ===============================

  useEffect(() => {

    loadReport();

    loadStudentReports();

  }, []);

  // ===============================
  // Search Student
  // ===============================

const handleSearch = (e) => {

    const value = e.target.value;

    setSearch(value);

    const filtered = reports.filter((item) => {

        return (
            item.name?.toLowerCase().includes(value.toLowerCase()) ||
            item.email?.toLowerCase().includes(value.toLowerCase()) ||
            item.title?.toLowerCase().includes(value.toLowerCase())
        );

    });

    if (value === "") {
        setFilteredReports(reports);
    } else {
        setFilteredReports(filtered);
    }

};
  // ===============================
  // Export Excel
  // ===============================

  const exportExcel = () => {

    const worksheet = XLSX.utils.json_to_sheet(filteredReports);

    const workbook = XLSX.utils.book_new();

    XLSX.utils.book_append_sheet(
      workbook,
      worksheet,
      "Student Reports"
    );

    const excelBuffer = XLSX.write(workbook, {
      bookType: "xlsx",
      type: "array"
    });

    const file = new Blob(
      [excelBuffer],
      {
        type:
          "application/octet-stream"
      }
    );

    saveAs(file, "Student_Report.xlsx");

  };

  // ===============================
  // Print Report
  // ===============================

  const printReport = () => {

    window.print();

  };

  // ===============================
// Export PDF
// ===============================

const exportPDF = () => {

  const doc = new jsPDF();

  doc.setFontSize(18);

  doc.text("LMS Student Report", 14, 18);

  autoTable(doc, {

    startY: 28,

    head: [[

      "ID",
      "Student",
      "Email",
      "Quiz",
      "Score",
      "%",
      "Status",
      "Attempts",
      "Time"

    ]],

    body: filteredReports.map((item) => [

      item.student_id,

      item.name,

      item.email,

      item.title,

      item.score,

      item.percentage,

      item.status,

      item.attempts,

      item.time_spent + " sec"

    ])

  });

  doc.save("Student_Report.pdf");

};

  return (

    <div className="reports-container">

      <h1>📊 LMS Reports</h1>

      {/* ========================= */}
      {/* Summary Cards */}
      {/* ========================= */}

      <div className="report-grid">

        <div className="report-card">
          <h2>{report.students}</h2>
          <p>Total Students</p>
        </div>

        <div className="report-card">
          <h2>{report.courses}</h2>
          <p>Total Courses</p>
        </div>

        <div className="report-card">
          <h2>{report.quizzes}</h2>
          <p>Total Quizzes</p>
        </div>

        <div className="report-card">
          <h2>{report.attempts}</h2>
          <p>Total Attempts</p>
        </div>

        <div className="report-card">
          <h2>{report.average_score}</h2>
          <p>Average Score</p>
        </div>

        <div className="report-card">
          <h2>{report.average_percentage}%</h2>
          <p>Average Percentage</p>
        </div>

        <div className="report-card pass">
          <h2>{report.passed}</h2>
          <p>Passed Students</p>
        </div>

        <div className="report-card fail">
          <h2>{report.failed}</h2>
          <p>Failed Students</p>
        </div>

      </div>

      {/* ========================= */}
      {/* Search */}
      {/* ========================= */}

      <div className="search-box">

        <input
          type="text"
          placeholder="🔍 Search Student..."
          value={search}
          onChange={handleSearch}
        />

      </div>

      {/* ========================= */}
      {/* Buttons */}
      {/* ========================= */}

      <div className="report-buttons">
      
      <button className="pdf-btn" onClick={exportPDF}>
     📄 Export PDF
       </button>

        <button
          className="excel-btn"
          onClick={exportExcel}
        >
          📊 Export Excel
        </button>

        <button
          className="print-btn"
          onClick={printReport}
        >
          🖨️ Print Report
        </button>

      </div>

      {/* ========================= */}
      {/* Student Report Table */}
      {/* ========================= */}

      <table className="report-table">

        <thead>

          <tr>

            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>%</th>
            <th>Status</th>
            <th>Attempts</th>
            <th>Time</th>

          </tr>

        </thead>

        <tbody>

          {

            filteredReports.length > 0 ?

            filteredReports.map((item) => (

              <tr key={item.student_id}>

                <td>{item.student_id}</td>

                <td>{item.name}</td>

                <td>{item.email}</td>

                <td>{item.title}</td>

                <td>{item.score}</td>

                <td>{item.percentage}%</td>

                <td>

                  <span
                    className={
                      item.status === "Pass"
                        ? "pass"
                        : "fail"
                    }
                  >

                    {item.status}

                  </span>

                </td>

                <td>{item.attempts}</td>

                <td>{item.time_spent} sec</td>

              </tr>

            ))

            :

            <tr>

              <td
                colSpan="9"
                style={{ textAlign: "center" }}
              >

                No Records Found

              </td>

            </tr>

          }

        </tbody>

      </table>

    </div>

  );

}

export default Reports;
