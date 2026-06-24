import { IndianRupee, ReceiptText, Store } from "lucide-react";


export default function AdminDashboard({ summary }) {
  return (
    <section className="admin-dashboard">
      <div className="section-title">
        <div>
          <p>Restaurant management</p>
          <h2>Admin dashboard</h2>
        </div>
      </div>
      <div className="stat-grid">
        <article className="stat-card">
          <Store size={24} />
          <span>Restaurants</span>
          <strong>{summary.restaurants}</strong>
        </article>
        <article className="stat-card">
          <ReceiptText size={24} />
          <span>Orders</span>
          <strong>{summary.orders}</strong>
        </article>
        <article className="stat-card">
          <IndianRupee size={24} />
          <span>Revenue</span>
          <strong>{summary.revenue}</strong>
        </article>
      </div>
      <div className="management-table">
        <div className="table-header">
          <span>Order</span>
          <span>Status</span>
          <span>Total</span>
        </div>
        {(summary.latest_orders || []).map((order) => (
          <div className="table-row" key={order.id}>
            <span>{order.id}</span>
            <span>{order.status}</span>
            <span>Rs. {order.total}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
