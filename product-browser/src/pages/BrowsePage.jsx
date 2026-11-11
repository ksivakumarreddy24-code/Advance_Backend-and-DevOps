import {useState, useEffect} from "react";
import { Link } from "react-router-dom";

function BrowserPage() {
    const[products, setProducts] = useState([]);
    const[page,setPages]=useState(1);

    useEffect(() => {
        async function loadProducts() {
            const skip =(page -1)*10;
            const res = await fetch(`https://dummyjson.com/products?limit=10&skip=${skip}`);
            const data = await res.json();
            setProducts(data.products);
        }
        loadProducts();
    }, [page]);

    return (
        <>
        <button disabled ={page ==1}onClick={() => setPages(page - 1)}>Previous</button>
        <span>page {page}</span>
        <button onClick={() => setPages(page + 1)}>Next</button>
        <p>Loaded {products.length} products</p>
        <ol>
            {products.map((product) => (
                <li key={product.id}>
                    <img src={product.thumbnail}></img>
                    <h3>Title - {product.title}</h3>
                    <p>Price - ${product.price}</p>
                    <p>Ratings - {product.rating}</p>
                    <p>Category - {product.category}</p>
                    <Link to={`/products/${product.id}`}>View details</Link>
        
                </li>

            ))}
        </ol>
        </>
    );
}

export default BrowserPage;
  