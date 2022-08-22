// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Main from './Main/Main'
import './index.css'


const rootElement = document.getElementById('root')
const root = createRoot(rootElement)

root.render(
  // <StrictMode>
    <Main />
  /* </StrictMode> */
)