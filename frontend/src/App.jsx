import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Login from './page/Login/Login'
import CategorySelection from './page/CategorySelection/CategorySelection';
import LinkAdd from './page/LinkAdd/LinkAdd';
import Home from './page/Home/Home';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path='/category_selection' element={<CategorySelection/>}/>
        <Route path='/link_add' element={<LinkAdd/>}/>
        <Route path='/home' element={<Home/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
