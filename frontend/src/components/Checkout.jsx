import { Minus, Plus, Trash2 } from "lucide-react";


export default function Checkout({ cart, updateQuantity, removeFromCart, placeOrder, latestOrder }) {
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <section className="checkout-layout">
      <div className="checkout-main">
        <div className="section-title">
          <div>
            <p>Cart and checkout</p>
            <h2>Your order</h2>
          </div>
          <strong>Rs. {total}</strong>
        </div>
        {cart.length === 0 ? (
          <div className="empty-state">
            <h3>Your cart is empty</h3>
            <p>Add menu items to prepare a checkout.</p>
          </div>
        ) : (
          <div className="cart-list">
            {cart.map((item) => (
              <article className="cart-row" key={item.id}>
                <div>
                  <h3>{item.name}</h3>
                  <p>Rs. {item.price} each</p>
                </div>
                <div className="quantity-control">
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)} title="Decrease quantity">
                    <Minus size={16} />
                  </button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)} title="Increase quantity">
                    <Plus size={16} />
                  </button>
                </div>
                <button className="icon-button" onClick={() => removeFromCart(item.id)} title="Remove item">
                  <Trash2 size={18} />
                </button>
              </article>
            ))}
          </div>
        )}
      </div>
      <form className="checkout-form" onSubmit={placeOrder}>
        <h2>Delivery details</h2>
        <input name="name" placeholder="Customer name" required />
        <input name="phone" placeholder="Phone number" required />
        <textarea name="address" placeholder="Delivery address" required />
        <select name="payment_method" defaultValue="upi">
          <option value="upi">UPI</option>
          <option value="card">Card</option>
          <option value="wallet">Wallet</option>
          <option value="cash">Cash on delivery</option>
        </select>
        <button className="primary-button" disabled={cart.length === 0}>
          Place order
        </button>
        {latestOrder && (
          <div className="order-status">
            <p>Order #{latestOrder.id}</p>
            <strong>{latestOrder.status.replaceAll("_", " ")}</strong>
          </div>
        )}
      </form>
    </section>
  );
}
