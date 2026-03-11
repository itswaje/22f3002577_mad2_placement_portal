
//gloabal way to interact with the backend
//We need to get the nav bar dynamically like it shouln't show sign in to the people already signed for that we use stores in pages

import { defineStore } from "pinia";
import api from "@/utils/api";
//stores the token so that user need not login each time
export const useUserStore = defineStore("user", {

  state: () => ({
    token: localStorage.getItem("access_token") || null,
    user: JSON.parse(localStorage.getItem("user")) || null
  }),

  getters: {

    isAuthenticated: (state) => !!state.token,

    role: (state) => {
      return state.user ? state.user.role : null
    },

    isAdmin: (state) => !!state.token && state.user && state.user.role === "admin",

    isStudent: (state) => !!state.token && state.user && state.user.role === "student",

    isCompany: (state) => !!state.token && state.user && state.user.role === "company"
  },

  actions: {

    setToken(token){
      this.token = token

      if(token){
        localStorage.setItem("access_token", token)
      }else{
        localStorage.removeItem("access_token")
      }
    },

    setUser(user){
      this.user = user

      if(user){
        localStorage.setItem("user", JSON.stringify(user))
      }else{
        localStorage.removeItem("user")
      }
    },
//kind of blacklisting by forgetting the toke
    logout(){
      this.setToken(null)
      this.setUser(null)
    },

    async login(credentials){

      const res = await api.post("/auth/login", credentials)

      const token = res.token
      const user = {
        id: res.id,
        email: res.email,
        name: res.name,
        role: res.role,
        profile_id: res.profile_id ?? null
      }

      this.setToken(token)
      this.setUser(user)

      return user
    }

  }

})


export default useUserStore;
