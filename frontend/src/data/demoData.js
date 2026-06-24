export const demoRestaurants = [
  {
    id: "spice-hub",
    name: "Spice Hub",
    cuisine: "Indian",
    rating: 4.7,
    delivery_time: "25-35 min",
    image: "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=900&q=80",
    menu: [
      { id: "paneer-butter-masala", name: "Paneer Butter Masala", price: 220, category: "Main Course", veg: true },
      { id: "chicken-biryani", name: "Chicken Biryani", price: 260, category: "Rice", veg: false },
      { id: "garlic-naan", name: "Garlic Naan", price: 55, category: "Bread", veg: true },
    ],
  },
  {
    id: "urban-bites",
    name: "Urban Bites",
    cuisine: "Fast Food",
    rating: 4.4,
    delivery_time: "20-30 min",
    image: "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=900&q=80",
    menu: [
      { id: "classic-burger", name: "Classic Burger", price: 180, category: "Burger", veg: false },
      { id: "loaded-fries", name: "Loaded Fries", price: 140, category: "Snacks", veg: true },
      { id: "cold-coffee", name: "Cold Coffee", price: 120, category: "Beverage", veg: true },
    ],
  },
  {
    id: "green-bowl",
    name: "Green Bowl",
    cuisine: "Healthy",
    rating: 4.6,
    delivery_time: "30-40 min",
    image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
    menu: [
      { id: "protein-salad", name: "Protein Salad", price: 210, category: "Salad", veg: true },
      { id: "smoothie-bowl", name: "Smoothie Bowl", price: 190, category: "Breakfast", veg: true },
      { id: "detox-juice", name: "Detox Juice", price: 110, category: "Beverage", veg: true },
    ],
  },
];
