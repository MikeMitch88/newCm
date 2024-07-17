import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import backgroundImageee from "../assets/antonio-alcantara-DWIbVgYzu6U-unsplash.jpg";
import Pagenotfound from './Pagenotfound'; // Import your NotFound component

function Login() {
  const [Username, setUsername] = useState('');
  const [Password, setPassword] = useState('');
  const [error, setError] = useState(false); // State to track error
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();

    const formData = {
      username: Username,
      password: Password,
    };

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(formData),
      redirect: "follow"
    };

    fetch("http://localhost:5000/login", requestOptions)
      .then(response => {
        if (!response.ok) {
          throw new Error('User not found'); // Throw error if response is not ok
        }
        return response.text();
      })
      .then(result => {
        console.log(result);
        navigate('/game');
      })
      .catch(error => {
        console.error(error);
        setError(true); // Set error state to true
      });
  }

  // Render NotFound component if error state is true
  if (error) {
    return <Pagenotfound />;
  }

  return (
    <div 
      style={{
        backgroundImage: `url(${backgroundImageee})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        height: '100vh',
        width: '100vw',
      }}
      className="flex items-center justify-center h-screen"
    >
      <div className="bg-white rounded-lg shadow-lg w-80 flex flex-col items-center">
        <div className="relative w-full">
          <div className="triangle absolute top-0 left-0"></div>
          <h2 className="text-center text-xl font-bold py-8">Login</h2>
        </div>
        <form onSubmit={handleSubmit} className="px-8 pb-8 w-full flex flex-col">
          <label htmlFor="username" className="block text-sm mb-2">Username</label>
          <input 
            type="text" 
            onChange={(e) => setUsername(e.target.value)} 
            id="username" 
            name="username" 
            className="w-full mb-4 p-2 border rounded-md" 
          />
          
          <label htmlFor="password" className="block text-sm mb-2">Password</label>
          <input 
            type="password"  
            onChange={(e) => setPassword(e.target.value)} 
            id="password" 
            name="password" 
            className="w-full mb-4 p-2 border rounded-md" 
          />
          
          <button type="submit" className="buttonsubmit">Login</button>

          <div className="flex justify-between text-sm mb-1 mt-6">
            <a href="#" className="text-gray-600">Forgot password?</a>
            <Link to="/signup" className="text-gray-600">Sign up</Link>
          </div>

        </form>
      </div>
    </div>
  );
}

export default Login;
