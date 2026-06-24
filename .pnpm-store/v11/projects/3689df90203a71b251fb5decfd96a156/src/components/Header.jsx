import { ShoppingCart, Store, UserRound } from "lucide-react";


export default function Header({ cartCount, activeView, setActiveView }) {
  return (
    <header className="app-header">
      <button className="brand" onClick={() => setActiveView("restaurants")}>
        <Store size={24} />
        <span>FoodFlow</span>
      </button>
      <nav>
        <button className={activeView === "restaurants" ? "active" : ""} onClick={() => setActiveView("restaurants")}>
          Restaurants
        </button>
        <button className={activeView === "admin" ? "active" : ""} onClick={() => setActiveView("admin")}>
          Admin
        </button>
      </nav>
      <div className="header-actions">
        <button className="icon-button" title="Customer profile">
          <UserRound size={20} />
        </button>
        <button className="cart-pill" onClick={() => setActiveView("checkout")}>
          <ShoppingCart size={19} />
          <span>{cartCount}</span>
        </button>
      </div>
    </header>
  );
}
