import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const getTasks = () => axios.get(`${API_BASE_URL}/tasks/`);
export const addTask = (task) => axios.post(`${API_BASE_URL}/tasks/`, task);
export const analyzeTasks = (tasks, strategy="smart") =>
  axios.post(`${API_BASE_URL}/tasks/analyze/`, { tasks, strategy }).then(res => res.data);
export const suggestTasks = (tasks, strategy="smart") =>
  axios.post(`${API_BASE_URL}/tasks/suggest/`, { tasks, strategy }).then(res => res.data);
