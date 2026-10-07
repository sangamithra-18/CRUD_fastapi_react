import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getEmployees = () => {
  return api.get("/employees");
};

export const getEmployee = (id) => {
  return api.get(`/employees/${id}`);
};

export const createEmployee = (employee) => {
  return api.post("/employees", employee);
};

export const updateEmployee = (id, employee) => {
  return api.put(`/employees/${id}`, employee);
};

export const deleteEmployee = (id) => {
  return api.delete(`/employees/${id}`);
};