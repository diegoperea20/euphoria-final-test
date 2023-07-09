import React, { useState ,useEffect} from "react";
import "../loginup.css";


// Conection to backend flask
const API_URL = import.meta.env.VITE_REACT_APP_API;

function Loginup() {
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const[same_password, setSame_password] = useState("");

  const [error, setError] = useState(""); // Nueva variable de estado para el mensaje de error

  const validatePassword = (value) => {
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;
    const requirements = [
      /\d/,
      /[a-z]/,
      /[A-Z]/,
      /[!@#$%^&*]/,
      /.{8,}/,
      /\S/,
    ];
    const errorMessages = [
      "Debe incluir al menos un número.",
      "Debe incluir al menos una letra minúscula.",
      "Debe incluir al menos una letra mayúscula.",
      "Debe incluir al menos un carácter especial.",
      "La longitud de la contraseña debe ser igual o mayor a 8 caracteres.",
      "No debe contener espacios en blanco.",
    ];

    const errors = [];
    for (let i = 0; i < requirements.length; i++) {
      if (!requirements[i].test(value)) {
        errors.push(errorMessages[i]);
      }
    }

    if (errors.length > 0) {
      setError(errors.join(" "));
    } else {
      setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (user === "" || email === "" || password === "" || same_password === "") {
      window.alert("Todos los campos son obligatorios");
      return;

    }

    if (password !== same_password) {
      window.alert("Las contraseñas no coinciden");
      return;
    }
    const response = await fetch(`${API_URL}/loginup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user,
        password,
        email,
      }),
    });
    const data = await response.json();

    if (response.status === 200) {
      // Registro exitoso, restablecer los campos y borrar el mensaje de error
      setUser("");
      setEmail("");
      setPassword("");
      setError("");
      window.location.href = `/`;
    } else {
      // Mostrar el mensaje de error en caso de que ocurra un error en el registro
      setError(data.error);
    }
  };

  




//------------------------------
  

  return (
    <div className="darkTheme">
      <h1>Login UP</h1>
      <form onSubmit={handleSubmit}>
        <h3>Username</h3>
        <input
          type="text"
          onChange={(e) => setUser(e.target.value)}
          value={user}
          placeholder="Username"
          autoFocus
        />
        <br />
        
        <h3>Password</h3>
        <input
          type="password"
          onChange={(e) => {
            setPassword(e.target.value);
            validatePassword(e.target.value);
          }}
          value={password}
          placeholder="Password"
          autoFocus
        />
        
        {/* Mostrar la condición de validación de la contraseña */}
        {error && <p className="errorMessage">{error}</p>}
        
        
        <h3>Confirm Password</h3>
        <input
          type="password"
          onChange={(e) => {
            setSame_password(e.target.value);
            
          }}
          value={same_password}
          placeholder="Validation Password"
          autoFocus
        />
        
        <h3>Email</h3>
        <input
          type="email"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          placeholder="Email"
          autoFocus
        />
        <br />
        <br />
        <button disabled={error.length > 0 && error !== "User already exists"}>Register</button>

      </form>
      <br/>
      <a href="/">Login In</a>
      <br/>
      <br/>
       
    </div>
  );
}

export default Loginup;
