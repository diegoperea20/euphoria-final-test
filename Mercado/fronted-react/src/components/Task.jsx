import React, { useEffect, useState } from "react";
import "../task.css";
// Conection to backend flask
const API_URL = import.meta.env.VITE_REACT_APP_API;

function Task() {
  const [user, setUser] = useState("");
  const [id, setId] = useState("");
  const [token, setToken] = useState("");

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const storedId = localStorage.getItem("id");
    const storedToken = localStorage.getItem("token");

    if (!storedUser && !storedId) {
      // Si no se encuentra el nombre de usuario en el almacenamiento local, redirigir al inicio de sesión
      window.location.replace("/");
    } else {
      // Si se encuentra el nombre de usuario, establecer el estado del usuario
      setUser(storedUser);
      setId(storedId);
      setToken(storedToken);
    }
  }, []);

  const home = () => {
    window.location.href = "/home";
  };

  const carro = () => {
    window.location.href = "/home/task/carro";
  }

  const [tasks, setTasks] = useState([]);
  const [taskAmounts, setTaskAmounts] = useState({});
  const handleAmountChange = (taskId, value) => {
    setTaskAmounts((prevState) => ({
      ...prevState,
      [taskId]: value,
    }));
  };

  const getTasks = async () => {
    const response = await fetch(`${API_URL}/products`);
    const data = await response.json();
    setTasks(data);
  };

  useEffect(() => {
    getTasks();
  });


  const agregarProducto = async (title, price, amount) => {

    
    const response = await fetch(`${API_URL}/tableuser/${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        price,
        amount,
      }),
    });
    const data = await response.json();
    console.log(data);
    window.alert("Product added to cart");
    await getTasks();
  };

  return (
    <div className="darkTheme">
      <h1>Buy Zone</h1>

      <button onClick={home}>Home</button>
      <button onClick={carro}>Show 🛒</button>
      <br />
      <br />
      <div></div>
      <br />
      <br />

      <div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Price</th>
                <th>Amount</th>
                <th>Operations</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr key={task.id}>
                  <td className="justified">{task.title}</td>
                  <td className="justified">{task.price}</td>
                  <td className="justified">
                  <input
                        type="number"
                        onChange={(e) => handleAmountChange(task.id, e.target.value)}
                        value={taskAmounts[task.id] || ""}
                        required min="1"
                        
                      />
                  </td>
                  <td>
                    <button
                      className="update"
                      onClick={() =>
                        agregarProducto(task.title, task.price, taskAmounts[task.id])
                      }
                    >
                      Add
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Task;
