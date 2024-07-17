import { useState } from 'react'

import Game from './pages/Game'
import Signup from './pages/Signup'
import Pagenotfound from './pages/Pagenotfound'
import Login from './pages/Login'
import {BrowserRouter,Routes,Route} from 'react-router-dom'



function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/game" element={<Game/>} />
        <Route path="*" element={<Pagenotfound/>} />

      </Routes>
    
    </BrowserRouter>
    
    </>
  )
}

export default App
