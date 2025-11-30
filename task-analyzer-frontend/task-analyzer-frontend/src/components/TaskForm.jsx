import React, { useState } from "react";

export default function TaskForm({ onTaskAdded }) {
  const [title, setTitle] = useState("");
  const [estimated_hours, setEstimatedHours] = useState(2);
  const [due_date, setDueDate] = useState("");
  const [importance, setImportance] = useState(5);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title || !due_date) {
      alert("Please fill all required fields");
      return;
    }
    onTaskAdded({ title, estimated_hours, due_date, importance, dependencies: [] });
    setTitle(""); setEstimatedHours(2); setDueDate(""); setImportance(5);
  };

  return (
    <form onSubmit={handleSubmit} style={{border:"1px solid #ccc", padding:"10px", marginBottom:"10px"}}>
      <div>
        <label>Task Title:</label>
        <input value={title} onChange={e=>setTitle(e.target.value)} />
      </div>
      <div>
        <label>Estimated Hours:</label>
        <input type="number" value={estimated_hours} onChange={e=>setEstimatedHours(parseInt(e.target.value))} />
      </div>
      <div>
        <label>Importance (1-10):</label>
        <input type="number" value={importance} min={1} max={10} onChange={e=>setImportance(parseInt(e.target.value))} />
      </div>
      <div>
        <label>Due Date:</label>
        <input type="date" value={due_date} onChange={e=>setDueDate(e.target.value)} />
      </div>
      <button type="submit">Add Task</button>
    </form>
  );
}
