import React from 'react'
import { useState } from 'react'
import backgroundimm from "../assets/cave.jpg"
import { useNavigate } from 'react-router-dom'


function Signup() {
  const [Username,setUsername]=useState()
  const [Password,setPassword]=useState()
  const [Email,setEmail]=useState()
  const navigate = useNavigate()
  
  function handlesubmit(e){
    e.preventDefault()
    console.log(Password)
    const formData={
      username:Username,
      email:Email,
      password:Password,
    }
    console.log(JSON.stringify(formData))

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(formData),
      redirect: "follow"
    };

    fetch("http://localhost:5000/register", requestOptions)
      .then((response) => response.text())
      .then((result)=> console.log(result),navigate('/'))
      .catch((error) => console.error(error));

      // onChange={(e)=>setUsername(e.target.value)
  }

  return (
    <div 
    style={{
      backgroundImage: `url(${backgroundimm})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      height: '100vh', // Add a height to the div to make it visible
      width: '100vw', // Add a width to the div to make it visible
    }}
    
    className="flex items-center justify-center h-screen">
      <div className="bg-white rounded-lg shadow-lg w-80 flex flex-col items-center">
        <div className="relative w-full">
          <div className="triangle absolute top-0 right-0 transform rotate-180"></div>
          <div className="triangle absolute top-0 left-0 transform rotate-0 border-x-50 resize-20"></div>
          <h2 className="text-center underline decorator-slate-50 font-black underline py-8">Register</h2>
        </div>
        <form onSubmit={handlesubmit} className="px-8 pb-8 w-full flex flex-col">
          <label htmlFor="email" className="block text-sm mb-2">email</label>
          <input type="email" onChange={(e)=>setEmail(e.target.value)} id="email" name="email" className="w-full mb-4 p-2 border rounded-md" />
          
          <label htmlFor="username" className="block text-sm mb-2">username</label>
          <input type="text" id="username" onChange={(e)=>setUsername(e.target.value)} name="username" className="w-full mb-4 p-2 border rounded-md" />
          
          <label htmlFor="password" className="block text-sm mb-2">password</label>
          <input type="password" id="password" onChange={(e)=>setPassword(e.target.value)} name="password" className="w-full mb-4 p-2 border rounded-md" />
          
          <button type="submit" className="buttonsubmit">Register</button>
        </form>
      </div>
    </div>
  );
}


export default Signup