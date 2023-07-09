import React, { useEffect, useState } from "react";
import "../task.css";
// Conection to backend flask
const API_URL = import.meta.env.VITE_REACT_APP_API;

function Carro() {
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

  const [carro, setCarro] = useState([]);
  const [total, setTotal] = useState(0);
  const getCarro = async () => {
    const response = await fetch(`${API_URL}/tableuser/${id}`);
    const data = await response.json();
    setCarro(data);
    let sum = 0;
    data.forEach((parameter) => {
      sum += parameter.amount * parameter.price;
    });
    setTotal(sum);
  };

  useEffect(() => {
    getCarro();
  });

  const deleteProduct = async (id, id_row) => {
    const response = await fetch(`${API_URL}/tableuser/${id}/${id_row}`, {
      method: "DELETE",
    });
    const data = await response.json();
    console.log(data);
    await getCarro();
  };


  const home = () => {
    window.location.href = "/home";
  };

  return (
    <div className="darkTheme">
      <h1>Shoppings</h1>
      <button onClick={home}>Home</button>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Price</th>
              <th>Amount</th>
              <th>Total</th>
              <th>Operations</th>
            </tr>
          </thead>
          <tbody>
            {carro.map((parameter) => (
              <tr key={parameter.id}>
                <td className="justified">{parameter.title}</td>
                <td className="justified">{parameter.price}</td>
                <td className="justified">{parameter.amount}</td>
                <td className="justified">{parameter.amount * parameter.price}</td>
                <td>
                  <button
                    className="update"
                    onClick={() =>
                      deleteProduct(
                        id,parameter.id
                      )
                    }
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <h1>Total: ${total}</h1>
      </div>
    </div>
  );
}

export default Carro;
