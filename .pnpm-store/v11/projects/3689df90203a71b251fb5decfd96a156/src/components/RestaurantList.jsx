import { Clock, Star } from "lucide-react";


export default function RestaurantList({ restaurants, selectedRestaurant, setSelectedRestaurant }) {
  return (
    <section className="restaurant-grid">
      {restaurants.map((restaurant) => (
        <button
          className={`restaurant-card ${selectedRestaurant?.id === restaurant.id ? "selected" : ""}`}
          key={restaurant.id}
          onClick={() => setSelectedRestaurant(restaurant)}
        >
          <img src={restaurant.image} alt={restaurant.name} />
          <div className="restaurant-card-body">
            <h3>{restaurant.name}</h3>
            <p>{restaurant.cuisine}</p>
            <div className="meta-row">
              <span><Star size={16} /> {restaurant.rating}</span>
              <span><Clock size={16} /> {restaurant.delivery_time}</span>
            </div>
          </div>
        </button>
      ))}
    </section>
  );
}
