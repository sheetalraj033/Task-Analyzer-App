import React from "react";

export default function TaskList({ tasks }) {
  if (!tasks || tasks.length === 0) {
    return <p>No tasks added yet.</p>;
  }

  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "20px" }}>
      <h3>Task List</h3>

      {tasks.map((task, index) => (
        <div
          key={index}
          style={{
            padding: "8px",
            borderBottom: "1px solid #ddd",
            marginBottom: "10px"
          }}
        >
          <p><strong>{task.title}</strong></p>
          <p>Estimated Hours: {task.estimated_hours}</p>
          <p>Importance: {task.importance}</p>
          <p>Due Date: {task.due_date}</p>

          {task.dependencies?.length > 0 && (
            <p>Dependencies: {task.dependencies.join(", ")}</p>
          )}
        </div>
      ))}
    </div>
  );
}
