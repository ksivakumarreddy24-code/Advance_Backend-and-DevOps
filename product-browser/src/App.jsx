import ProductsPage from "./pages/ProductsPage"
import { Link, Route, Routes } from "react-router-dom"
import BrowsePage from "./pages/BrowsePage.jsx"
import ProductDetailPage from "./pages/ProductdetailPage.jsx"
function App() {
  return (
    <>
      <nav>
        <Link to="/">All Products</Link> | <Link to="/browser">Browse</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/browser" element={<BrowsePage />} />
        <Route path ="/products/:id" element ={<ProductDetailPage/>}/>
        <Route path="*" element={<h1>404 - Page not found</h1>} />
      </Routes>
    </>
  )
}

export default App;
