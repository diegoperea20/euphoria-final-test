import React, { useEffect, useState } from 'react';
import "../home.css";
// Conection to backend flask
const API_URL = import.meta.env.VITE_REACT_APP_API;


function Home() {
  const [user, setUser] = useState('');
  const [id, setId] = useState('');
  const [token, setToken] = useState('');
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedId = localStorage.getItem('id');
    const storedToken = localStorage.getItem('token');

    if (!storedUser && !storedId) {
      // Si no se encuentra el nombre de usuario en el almacenamiento local, redirigir al inicio de sesión
      window.location.replace('/');
    } else {
      // Si se encuentra el nombre de usuario, establecer el estado del usuario
      setUser(storedUser);
      setId(storedId);
      setToken(storedToken);
    }

    
  }, []);

  const handleLogout = () => {
    // Eliminar el token y el nombre de usuario del almacenamiento local al cerrar sesión
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    // Redireccionar al inicio de sesión después de cerrar sesión
    window.location.replace('/');
  };



  const changePassword = () => {
    // Almacenar el user y el id en el almacenamiento local antes de redirigir
    localStorage.setItem('userForChangePassword', user);
    localStorage.setItem('idForChangePassword', id);
    localStorage.setItem('tokenForChangePassword', token);
    

    // Redireccionar a la página de cambio de contraseña
    window.location.href = '/changepassword';
  };
   
  const deleteAccount = async (id, user) => {
    if (window.confirm('¿Desea eliminar la cuenta?')) {
      const response = await fetch(`${API_URL}/loginup/${id}`, {
        method: "DELETE",
      });
      const response_all = await fetch(`${API_URL}/tableuser/account/${id}`, {
        method: "DELETE",
      });
  
      if (response.status === 200 && response_all.status === 200) {
        // La cuenta se ha eliminado correctamente
        window.alert('Cuenta eliminada correctamente');
        window.location.href = `/`;
      } else {
        // Ocurrió un error al eliminar la cuenta
        console.log('Error al eliminar la cuenta');
        window.alert('Error al eliminar la cuenta');
      }
    }
  };
  

  const comprar= async () => {
    const response = await fetch(`${API_URL}/tableuser`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id
      }),
    });
    
  
    window.location.href = '/home/task';
  };
  

  return (
    <div className="darkTheme">
      <h1>Welcome: {user} ! ,  ID:{id}</h1>
      <button onClick={handleLogout}>Logout</button>
      <br/>
      <br/>
      <button onClick={changePassword}>Change Password</button>
      <br/>
      <br/>
      <button onClick={() => deleteAccount(id, user)}>Delete Account</button>
      <br/>
      <br/>
      <button onClick={comprar}>Buy</button>

    </div>
  );
}

export default Home;
