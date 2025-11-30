import React from "react";

export default function TaskSummary({ analyzedTasks, suggestedTasks }) {
  if (analyzedTasks.length === 0 && suggestedTasks.length === 0) return null;

  return (
    <div>
      {analyzedTasks.length > 0 && (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px", borderRadius: "5px" }}>
          <h3>Analyzed Tasks</h3>
          <ul>
            {analyzedTasks.map((task, index) => (
              <li key={index}>{task.title} - Score: {task.score}</li>
            ))}
          </ul>
        </div>
      )}

      {suggestedTasks.length > 0 && (
        <div style={{ border: "1px solid #0a0", padding: "10px", borderRadius: "5px", backgroundColor: "#e6ffe6" }}>
          <h3>Top 3 Suggested Tasks</h3>
          <ul>
            {suggestedTasks.map((task, index) => (
              <li key={index}>{index + 1}. {task.title} - Score: {task.score}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
