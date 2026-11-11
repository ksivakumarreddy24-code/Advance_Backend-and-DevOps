import {useState, useEffect} from "react";
import {useParams} from "react-router";
import { Link } from "react-router-dom";

function ProductDetailPage() {
    const {id} = useParams();
    const[products, setProducts] = useState([]);

    useEffect(() => {
        async function loadProducts() {
            const res = await fetch(`https://dummyjson.com/products/${id}`);
            const data = await res.json();
            
            setProducts(data);
        }
        loadProducts();
    }, []);

    if (!products) {
        return <p>Loading...</p>
    }

    return(
        <>
        <Link to="/">Back to products</Link>
        <ul>
            {products.map((product) => (
                <li key={product.id}>
                    <h2>Title - {product.title}</h2>
                    <img src={product.thumbnail}></img>
                    <p>Description - {product.description}</p>
                    <p>Price - ${product.price}</p>
                    <p>Stock - {product.stock}</p>
                    <p>Ratings - {product.rating}</p>
                    <p>Category - {product.category}</p>
                    <p>Reviews - {product.reviews}</p>
                
                </li>

            ))}
        </ul>
        </>
    )

}

export default ProductDetailPage