<template>
  <div class="container py-5" style="max-width: 420px">
    <div class="card shadow-sm">
      <div class="card-body">

        <h3 class="card-title mb-3 text-center">
          Placement Portal Login
        </h3>

        <form @submit.prevent="submitLogin" novalidate><!--we want to validate with own func of js and not default html validation -->

          <!-- Email -->
          <div class="mb-3">
            <label class="form-label" for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-control"
              placeholder="you@example.com"
              required
            />
          </div>

          <!-- Password -->
          <div class="mb-3">
            <label class="form-label" for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-control"
              placeholder="••••••••"
              required
            />
          </div>

          <!-- Error -->
          <div v-if="error" class="text-danger mb-2 small">
            {{ error }}
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
              role="status"
            ></span>

            {{ loading ? "Signing in..." : "Login" }}
          </button>

          <!-- Register link -->
          <div class="text-center mt-3 small">
            Don't have an account?
            <router-link to="/register">Register</router-link>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user"

export default {
  name: "LoginPage",

  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: "",
      userStore: null,
    }
  },

  created() {
    this.userStore = useUserStore()
  },

  methods: {

    async submitLogin() {
      this.error = ""
      this.loading = true

      try {

        const user = await this.userStore.login({    //await tells wait for the function to complete
          email: this.email,
          password: this.password
        })

        /* role based redirect */

        if (user.role === "admin") {
          this.$router.push("/admin/dashboard")
        }

        else if (user.role === "company") {
          this.$router.push("/company/dashboard")
        }

        else {
          this.$router.push("/student/dashboard")
        }

      }

      catch (e) {
        this.error = e.message || "Login failed"
      }

      finally {
        this.loading = false
      }
    }

  }
}
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>