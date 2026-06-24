import { useEffect, useMemo, useState } from "react";
import AdminDashboard from "./components/AdminDashboard.jsx";
import Checkout from "./components/Checkout.jsx";
import Header from "./components/Header.jsx";
import MenuPanel from "./components/MenuPanel.jsx";
import RestaurantList from "./components/RestaurantList.jsx";
import { createOrder, getAdminSummary, getRestaurants } from "./services/api.js";


export default function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [cart, setCart] = useState([]);
  const [activeView, setActiveView] = useState("restaurants");
  const [search, setSearch] = useState("");
  const [summary, setSummary] = useState({ restaurants: 0, orders: 0, revenue: 0, latest_orders: [] });
  const [latestOrder, setLatestOrder] = useState(null);

  useEffect(() => {
    getRestaurants().then((items) => {
      setRestaurants(items);
      setSelectedRestaurant(items[0]);
    });
    getAdminSummary().then(setSummary);
  }, []);

  const filteredRestaurants = useMemo(() => {
    return restaurants.filter((restaurant) => {
      const searchText = `${restaurant.name} ${restaurant.cuisine}`.toLowerCase();
      return searchText.includes(search.toLowerCase());
    });
  }, [restaurants, search]);

  function addToCart(item) {
    setCart((current) => {
      const existing = current.find((cartItem) => cartItem.id === item.id);
      if (existing) {
        return current.map((cartItem) => (
          cartItem.id === item.id ? { ...cartItem, quantity: cartItem.quantity + 1 } : cartItem
        ));
      }
      return [...current, { ...item, quantity: 1 }];
    });
  }

  function updateQuantity(id, quantity) {
    if (quantity <= 0) {
      removeFromCart(id);
      return;
    }
    setCart((current) => current.map((item) => (item.id === id ? { ...item, quantity } : item)));
  }

  function removeFromCart(id) {
    setCart((current) => current.filter((item) => item.id !== id));
  }

  async function placeOrder(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const order = await createOrder({
      customer: {
        name: data.get("name"),
        phone: data.get("phone"),
        address: data.get("address"),
      },
      restaurant_id: selectedRestaurant?.id || "unknown",
      items: cart,
      payment_method: data.get("payment_method"),
    });
    setLatestOrder(order);
    setCart([]);
    setSummary((current) => ({
      ...current,
      orders: current.orders + 1,
      revenue: current.revenue + order.total,
      latest_orders: [order, ...(current.latest_orders || [])].slice(0, 5),
    }));
  }

  return (
    <div className="app-shell">
      <Header cartCount={cart.reduce((sum, item) => sum + item.quantity, 0)} activeView={activeView} setActiveView={setActiveView} />
      <main>
        {activeView === "restaurants" && (
          <>
            <section className="browse-toolbar">
              <div>
                <p>Online food ordering</p>
                <h1>Find meals and track every order</h1>
              </div>
              <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search restaurants or cuisines" />
            </section>
            <div className="content-grid">
              <RestaurantList restaurants={filteredRestaurants} selectedRestaurant={selectedRestaurant} setSelectedRestaurant={setSelectedRestaurant} />
              <MenuPanel restaurant={selectedRestaurant} addToCart={addToCart} />
            </div>
          </>
        )}
        {activeView === "checkout" && (
          <Checkout
            cart={cart}
            updateQuantity={updateQuantity}
            removeFromCart={removeFromCart}
            placeOrder={placeOrder}
            latestOrder={latestOrder}
          />
        )}
        {activeView === "admin" && <AdminDashboard summary={summary} />}
      </main>
    </div>
  );
}
