import axios from "axios";
import { useEffect, useState } from "react";
import "./Announcements.css";

function Announcements() {

  const [announcements, setAnnouncements] = useState([]);

  useEffect(() => {

    loadAnnouncements();

    updateAnnouncementView();

  }, []);

  const loadAnnouncements = async () => {

    try {

      const res = await axios.get(
        "http://localhost:5000/announcements"
      );

      setAnnouncements(res.data);

    } catch (error) {

      console.log(error);

      alert("Unable to load announcements.");

    }

  };

  const updateAnnouncementView = async () => {

    try {

      await axios.post(
        "http://localhost:5000/announcement-view",
        {

          student_id: localStorage.getItem("student_id")

        }
      );

    } catch (error) {

      console.log(error);

    }

  };

  return (

    <div className="announcement-container">

      <h1>Latest Announcements</h1>

      {

        announcements.map((announcement) => (

          <div
            className="announcement-card"
            key={announcement.announcement_id}
          >

            <h2>{announcement.title}</h2>

            <p>{announcement.description}</p>

            <small>

              {announcement.created_at}

            </small>

          </div>

        ))

      }

    </div>

  );

}

export default Announcements;