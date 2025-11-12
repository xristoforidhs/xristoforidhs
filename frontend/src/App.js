import { useEffect, useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import axios from "axios";
import HomePage from "@/pages/HomePage";
import ProductDetailPage from "@/pages/ProductDetailPage";
import CartPage from "@/pages/CartPage";
import CheckoutPage from "@/pages/CheckoutPage";
import PaymentSuccessPage from "@/pages/PaymentSuccessPage";
import AdminDashboard from "@/pages/AdminDashboard";
import OrdersPage from "@/pages/OrdersPage";
import AuthPage from "@/pages/AuthPage";
import StoreSettingsPage from "@/pages/StoreSettingsPage";
import CategoryPage from "@/pages/CategoryPage";
import DailyOffersPage from "@/pages/DailyOffersPage";
import SocialPage from "@/pages/SocialPage";
import CustomersPage from "@/pages/CustomersPage";
import { Toaster } from "@/components/ui/sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const AuthContext = React.createContext();

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`);
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user", error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (newToken, userData) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(userData);
    axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common["Authorization"];
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Φόρτωση...</div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, token }}>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/product/:id" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/payment-success" element={<PaymentSuccessPage />} />
            <Route path="/auth" element={<AuthPage />} />
            <Route path="/orders" element={user ? <OrdersPage /> : <Navigate to="/auth" />} />
            <Route path="/admin" element={user?.role === "admin" ? <AdminDashboard /> : <Navigate to="/" />} />
            <Route path="/admin/settings" element={user?.role === "admin" ? <StoreSettingsPage /> : <Navigate to="/" />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-center" richColors />
      </div>
    </AuthContext.Provider>
  );
}

import React from "react";
export default App;