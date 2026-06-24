import { Plus } from "lucide-react";


export default function MenuPanel({ restaurant, addToCart }) {
  if (!restaurant) {
    return (
      <section className="menu-panel empty-state">
        <h2>Select a restaurant</h2>
        <p>Choose a restaurant to view its menu and start an order.</p>
      </section>
    );
  }

  return (
    <section className="menu-panel">
      <div className="section-title">
        <div>
          <p>{restaurant.cuisine}</p>
          <h2>{restaurant.name}</h2>
        </div>
        <span>{restaurant.delivery_time}</span>
      </div>
      <div className="menu-list">
        {restaurant.menu.map((item) => (
          <article className="menu-item" key={item.id}>
            <div>
              <span className={item.veg ? "food-tag veg" : "food-tag nonveg"}>{item.veg ? "Veg" : "Non-veg"}</span>
              <h3>{item.name}</h3>
              <p>{item.category}</p>
            </div>
            <div className="price-action">
              <strong>Rs. {item.price}</strong>
              <button onClick={() => addToCart(item)} title={`Add ${item.name}`}>
                <Plus size={18} />
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
