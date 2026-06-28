// frontend/src/api/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "/ParaVirPred"
});

export default api;