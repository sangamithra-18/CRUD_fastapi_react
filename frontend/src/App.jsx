import { useEffect, useState } from "react";

import {
  getEmployees,
  createEmployee,
  updateEmployee,
  deleteEmployee,
} from "./services/employeeService";

import EmployeeTable from "./components/EmployeeTable";
import EmployeeForm from "./components/EmployeeForm";

function App() {
  const [employees, setEmployees] = useState([]);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
   
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [deleteEmployeeId, setDeleteEmployeeId] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [showForm, setShowForm] = useState(false);

  // null = Add mode
  // employee object = Edit mode
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  
  const fetchEmployees = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getEmployees();

      setEmployees(response.data);
    } catch (error) {
      console.error(error);
      setError("Failed to load employees.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  // -----------------------------
  // ADD / UPDATE
  // -----------------------------

  const handleFormSubmit = async (employeeData) => {
    try {
      setSubmitting(true);
      setError("");
      setSuccess("");

      if (selectedEmployee) {
        // UPDATE
        await updateEmployee(
          selectedEmployee.id,
          employeeData
        );

        setSuccess("Employee updated successfully.");
      } else {
        // CREATE
        await createEmployee(employeeData);

        setSuccess("Employee added successfully.");
      }

      setShowForm(false);
      setSelectedEmployee(null);

      await fetchEmployees();

      setTimeout(() => {
        setSuccess("");
      }, 3000);

    } catch (error) {
      console.error(error);

      if (error.response?.status === 409) {
        setError(
          "An employee with this email already exists."
        );
      } else if (error.response?.status === 404) {
        setError("Employee not found.");
      } else {
        setError(
          selectedEmployee
            ? "Failed to update employee."
            : "Failed to create employee."
        );
      }

    } finally {
      setSubmitting(false);
    }
  };

  // -----------------------------
  // OPEN ADD FORM
  // -----------------------------

  const handleAdd = () => {
    setSelectedEmployee(null);
    setShowForm(true);
    setError("");
  };

  // -----------------------------
  // OPEN EDIT FORM
  // -----------------------------

  const handleEdit = (employee) => {
    setSelectedEmployee(employee);
    setShowForm(true);
    setError("");
  };

  // -----------------------------
  // CLOSE FORM
  // -----------------------------

  const handleCloseForm = () => {
    if (submitting) {
      return;
    }

    setShowForm(false);
    setSelectedEmployee(null);
  };

  // -----------------------------
  // DELETE
  // -----------------------------

 const handleDelete = (id) => {
  setDeleteEmployeeId(id);
};
const confirmDelete = async () => {
  try {
    setDeleting(true);
    setError("");
    setSuccess("");

    await deleteEmployee(deleteEmployeeId);

    setSuccess("Employee deleted successfully.");

    setDeleteEmployeeId(null);

    await fetchEmployees();

    setTimeout(() => {
      setSuccess("");
    }, 3000);

  } catch (error) {
    console.error(error);

    if (error.response?.status === 404) {
      setError("Employee not found.");
    } else {
      setError("Failed to delete employee.");
    }
  } finally {
    setDeleting(false);
  }
};
  return (
    <div className="app">

      <header className="header">

        <div>
          <h1>Employee Management</h1>
          <p>Manage your employees</p>
        </div>

        <button
          className="add-btn"
          onClick={handleAdd}
        >
          + Add Employee
        </button>

      </header>

      <main className="container">

        {success && (
          <div className="success">
            {success}
          </div>
        )}

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            Loading employees...
          </div>
        )}

        {!loading && !error && (
          <EmployeeTable
            employees={employees}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        )}

      </main>

      {showForm && (
        <EmployeeForm
          employee={selectedEmployee}
          onSubmit={handleFormSubmit}
          onClose={handleCloseForm}
          submitting={submitting}
        />
      )}

      {deleteEmployeeId && (
  <div className="modal-overlay">
    <div className="confirm-modal">

      <div className="confirm-icon">
        !
      </div>

      <h2>Delete Employee?</h2>

      <p>
        Are you sure you want to delete this employee?
        This action cannot be undone.
      </p>

      <div className="confirm-actions">

        <button
          className="cancel-btn"
          onClick={() => setDeleteEmployeeId(null)}
          disabled={deleting}
        >
          Cancel
        </button>

        <button
          className="delete-confirm-btn"
          onClick={confirmDelete}
          disabled={deleting}
        >
          {deleting ? "Deleting..." : "Delete"}
        </button>

      </div>

    </div>
  </div>
)}

    </div>
  );
}

export default App;