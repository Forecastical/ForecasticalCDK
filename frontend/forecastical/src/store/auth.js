// src/store/auth.js
import { defineStore } from 'pinia';
import { authService } from '@/services/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    username: (state) => state.user?.username,
  },

  actions: {
    async login(username, password) {
      this.loading = true;
      try {
        const user = await authService.login(username, password);
        this.user = user;
        return user;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async register(userData) {
      this.loading = true;
      try {
        const user = await authService.register(userData);
        return user;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(userData) {
      this.loading = true;
      try {
        const updatedUser = await authService.updateUser(userData);
        this.user = { ...this.user, ...updatedUser };
        return updatedUser;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    logout() {
      authService.logout();
      this.user = null;
    },

    initializeFromStorage() {
      const user = authService.getCurrentUser();
      if (user) {
        this.user = user;
      }
    }
  }
});