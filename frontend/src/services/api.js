import { demoRestaurants } from "../data/demoData";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function getRestaurants() {
  try {
    return await request("/restaurants/");
  } catch {
    return demoRestaurants;
  }
}

export async function createOrder(order) {
  try {
    return await request("/orders/", {
      method: "POST",
      body: JSON.stringify(order),
    });
  } catch {
    return {
      id: `local-${Date.now()}`,
      ...order,
      total: order.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
      status: "received",
      payment_status: order.payment_method === "cash" ? "pending" : "paid",
    };
  }
}

export async function getAdminSummary() {
  try {
    return await request("/admin/summary/");
  } catch {
    return {
      restaurants: demoRestaurants.length,
      orders: 1,
      revenue: 220,
      latest_orders: [],
    };
  }
}
