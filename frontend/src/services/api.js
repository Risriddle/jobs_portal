import axios from "axios";

const api = axios.create({
  baseURL: "https://jobs-portal-murex.vercel.app/_/backend/api",
});

export default api;