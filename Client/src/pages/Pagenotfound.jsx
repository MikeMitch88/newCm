import React from 'react'
import backgroundImageee from "../assets/404.png";

function Pagenotfound() {
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
    ></div>
  )
}

export default Pagenotfound