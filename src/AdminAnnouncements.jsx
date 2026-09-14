import axios from "axios";
import { useEffect, useState } from "react";
import "./AdminAnnouncements.css";
function Announcements() {

  const [announcements, setAnnouncements] = useState([]);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [editId, setEditId] = useState(null);

  useEffect(() => {
    loadAnnouncements();
  }, []);

  const loadAnnouncements = async () => {

    const res = await axios.get(
      "https://lms-backend-api-bnx4.onrender.com/announcements"
    );

    setAnnouncements(res.data);

  };

  const saveAnnouncement = async () => {

    if (editId === null) {

      await axios.post(
        "https://lms-backend-api-bnx4.onrender.com/announcements",
        {
          title,
          description
        }
      );

      alert("Announcement Added Successfully");

    } else {

      await axios.put(
        `https://lms-backend-api-bnx4.onrender.com/announcements/${editId}`,
        {
          title,
          description
        }
      );

      alert("Announcement Updated Successfully");

      setEditId(null);

    }

    setTitle("");
    setDescription("");

    loadAnnouncements();

  };

  const editAnnouncement = (announcement) => {

    setEditId(announcement.announcement_id);

    setTitle(announcement.title);

    setDescription(announcement.description);

  };

  const deleteAnnouncement = async (id) => {

    if (window.confirm("Delete this announcement?")) {

      await axios.delete(
        `https://lms-backend-api-bnx4.onrender.com/announcements/${id}`
      );

      loadAnnouncements();

    }

  };
     return (

  <div className="announcement-admin">

    <h1>Manage Announcements</h1>

    <div className="announcement-form">

      <input
        type="text"
        placeholder="Announcement Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <textarea
        placeholder="Announcement Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      ></textarea>

      <button onClick={saveAnnouncement}>
        {editId === null ? "Add Announcement" : "Update Announcement"}
      </button>

    </div>

    <table>

      <thead>

        <tr>

          <th>Title</th>
          <th>Description</th>
          <th>Date</th>
          <th>Action</th>
          <th>Delete</th>

        </tr>

      </thead>

      <tbody>

        {announcements.map((announcement) => (

          <tr key={announcement.announcement_id}>

            <td>{announcement.title}</td>

            <td>{announcement.description}</td>

            <td>{announcement.created_at}</td>

            <td>

              <button
                className="edit-btn"
                onClick={() => editAnnouncement(announcement)}
              >
                Edit
              </button>

            </td>
            <td>
              <button
                className="delete-btn"
                onClick={() =>
                  deleteAnnouncement(announcement.announcement_id)
                }
              >
                Delete
              </button>
            </td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>

);


}

export default Announcements;
