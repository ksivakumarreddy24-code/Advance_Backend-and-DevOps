import { useState } from "react";
import { useEffect } from "react";
import { Link } from "react-router-dom";

function ProductsPage() {
    const[products, setProducts] = useState([]);
 
    useEffect(() => {
        async function loadProducts() {
            const res = await fetch("https://dummyjson.com/products");
            const data = await res.json();
            
            setProducts(data.products);
        }
        loadProducts();
    }, []);

    return(
        <>
        <button>Previous</button>
        <button>Next</button>
        <p>Loaded {products.length} products</p>
        <ul>
            {products.map((product) => (
                <li key={product.id}>
                    <img src={product.thumbnail} alt={product.title} />
                    <h3>{product.title}</h3>
                    <p>Price: ${product.price}</p>
                    <p>Rating: {product.rating}</p>
                    <p>Category: {product.category}</p>
                    <Link to={`/products/${product.id}`}>View details</Link>
                </li>
            ))}
        </ul>
        </>
    )

}

export default ProductsPage;