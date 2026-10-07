function EmployeeTable({ employees, onEdit, onDelete }) {
  if (employees.length === 0) {
    return (
      <div className="empty-state">
        <h3>No employees found</h3>
        <p>Add your first employee to get started.</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Salary</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {employees.map((employee,index) => (
            <tr key={employee.id}>
            <td>{index + 1}</td>
              <td>{employee.name}</td>
              <td>{employee.email}</td>
              <td>{employee.role}</td>
              <td>₹{employee.salary}</td>

              <td>
                <button
                  className="edit-btn"
                  onClick={() => onEdit(employee)}
                >
                  Edit
                </button>

                <button
                  className="delete-btn"
                  onClick={() => onDelete(employee.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EmployeeTable;