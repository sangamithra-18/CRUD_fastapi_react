import { useEffect, useState } from "react";

function EmployeeForm({
  employee,
  onSubmit,
  onClose,
  submitting,
}) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    role: "",
    salary: "",
  });

  const [errors, setErrors] = useState({});

  const isEditMode = Boolean(employee);

  useEffect(() => {
    if (employee) {
      setFormData({
        name: employee.name,
        email: employee.email,
        role: employee.role,
        salary: employee.salary,
      });
    } else {
      setFormData({
        name: "",
        email: "",
        role: "",
        salary: "",
      });
    }

    setErrors({});
  }, [employee]);

  const validate = () => {
    const newErrors = {};

    // Name
    if (!formData.name.trim()) {
      newErrors.name = "Name is required";
    } else if (
      !/^[A-Za-z]+(?:\s+[A-Za-z]+)*$/.test(formData.name.trim())
    ) {
      newErrors.name =
        "Name must contain only letters and spaces";
    }

    // Email
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)
    ) {
      newErrors.email = "Enter a valid email";
    }

    // Role
    if (!formData.role.trim()) {
      newErrors.role = "Role is required";
    }

    // Salary
    if (!formData.salary) {
      newErrors.salary = "Salary is required";
    } else if (Number(formData.salary) <= 0) {
      newErrors.salary = "Salary must be greater than 0";
    }

    setErrors(newErrors);

    return newErrors;
  };
const handleChange = (event) => {
  const { name, value } = event.target;

  let updatedValue = value;

  if (name === "name") {
    updatedValue = value
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  setFormData((previous) => ({
    ...previous,
    [name]: updatedValue,
  }));

  setErrors((previous) => ({
    ...previous,
    [name]: "",
  }));
};

  const handleSubmit = async (event) => {
    event.preventDefault();

    const validationErrors = validate();

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    await onSubmit({
      ...formData,
      salary: Number(formData.salary),
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal">

        <div className="modal-header">
          <div>
            <h2>
              {isEditMode ? "Edit Employee" : "Add Employee"}
            </h2>

            <p>
              {isEditMode
                ? "Update employee information."
                : "Enter employee details below."}
            </p>
          </div>

          <button
            type="button"
            className="close-btn"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} noValidate>

          <div className="form-group">
            <label>Name</label>

            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter employee name"
            />

            {errors.name && (
              <span className="field-error">
                {errors.name}
              </span>
            )}
          </div>

          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter email address"
            />

            {errors.email && (
              <span className="field-error">
                {errors.email}
              </span>
            )}
          </div>

          <div className="form-group">
            <label>Role</label>

            <input
              type="text"
              name="role"
              value={formData.role}
              onChange={handleChange}
              placeholder="e.g. Frontend Developer"
            />

            {errors.role && (
              <span className="field-error">
                {errors.role}
              </span>
            )}
          </div>

          <div className="form-group">
            <label>Salary</label>

            <input
              type="number"
              name="salary"
              value={formData.salary}
              onChange={handleChange}
              placeholder="Enter salary"
              min="1"
            />

            {errors.salary && (
              <span className="field-error">
                {errors.salary}
              </span>
            )}
          </div>

          <div className="form-actions">

            <button
              type="button"
              className="cancel-btn"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="save-btn"
              disabled={submitting}
            >
              {submitting
                ? "Saving..."
                : isEditMode
                  ? "Update Employee"
                  : "Save Employee"}
            </button>

          </div>

        </form>
      </div>
    </div>
  );
}

export default EmployeeForm;