import React, { createContext, useContext, useState } from 'react';
import { toast } from 'sonner';
import axios from 'axios';
import { API } from '@/App';

const CartNotificationContext = createContext();

export const useCartNotification = () => {
  const context = useContext(CartNotificationContext);
  if (!context) {
    throw new Error('useCartNotification must be used within CartNotificationProvider');
  }
  return context;
};

export const CartNotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);

  const sendCartNotification = async (productData, userInfo) => {
    try {
      // Send notification to backend
      await axios.post(`${API}/cart-notification`, {
        product: productData,
        user: userInfo,
        timestamp: new Date().toISOString(),
        action: 'added_to_cart'
      });

      // Add to local notifications
      const notification = {
        id: Date.now(),
        product: productData,
        user: userInfo,
        timestamp: new Date(),
        read: false
      };

      setNotifications(prev => [notification, ...prev]);

      // Show toast for admin (in real app this would be sent via websocket or email)
      toast.info(`🛒 ${userInfo?.name || 'Guest'} προσθέσε "${productData.name}" στο καλάθι!`, {
        duration: 5000,
        action: {
          label: 'Προβολή',
          onClick: () => {
            console.log('Notification details:', notification);
          }
        }
      });

    } catch (error) {
      console.error('Failed to send cart notification:', error);
    }
  };

  const markAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const getUnreadCount = () => {
    return notifications.filter(n => !n.read).length;
  };

  return (
    <CartNotificationContext.Provider 
      value={{
        notifications,
        sendCartNotification,
        markAsRead,
        getUnreadCount
      }}
    >
      {children}
    </CartNotificationContext.Provider>
  );
};