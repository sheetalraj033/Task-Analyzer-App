import React, { useState, useEffect } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import TaskSummary from "./components/TaskSummary";
import { getTasks, addTask, analyzeTasks, suggestTasks } from "./services/api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [analyzedTasks, setAnalyzedTasks] = useState([]);
  const [suggestedTasks, setSuggestedTasks] = useState([]);
  const [strategy, setStrategy] = useState("smart");

  const fetchTasks = async () => {
    const res = await getTasks();
    setTasks(res.data);
  };

  useEffect(()=>{ fetchTasks(); }, []);

  const handleTaskAdded = async (task) => {
    await addTask(task);
    fetchTasks();
  };

  const handleAnalyze = async () => {
    const analyzed = await analyzeTasks(tasks, strategy);
    const suggested = await suggestTasks(tasks, strategy);
    setAnalyzedTasks(analyzed);
    setSuggestedTasks(suggested);
  };

  return (
    <div style={{maxWidth:"600px", margin:"20px auto"}}>
      <h1>Task Analyzer</h1>
      <TaskForm onTaskAdded={handleTaskAdded} />
      <div>
        <label>Strategy: </label>
        <select value={strategy} onChange={e=>setStrategy(e.target.value)}>
          <option value="fastest">Fastest Wins</option>
          <option value="highimpact">High Impact</option>
          <option value="deadline">Deadline Driven</option>
          <option value="smart">Smart Balance</option>
        </select>
      </div>
      <TaskList tasks={tasks} />
      <button onClick={handleAnalyze}>Analyze & Suggest Top 3 Tasks</button>
      <TaskSummary analyzedTasks={analyzedTasks} suggestedTasks={suggestedTasks} />
    </div>
  );
}

export default App;
