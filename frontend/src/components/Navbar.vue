<script>
import { useUserStore } from "@/stores/user";

export default {

  name: "Navbar",

  data() {
    return {
      userStore: null,
      dropdownOpen: false,
    };
  },

  created() {
    this.userStore = useUserStore();
  },

  mounted() {
    this._onDocClick = (e) => {
      if (!this.$el.contains(e.target)) {
        this.dropdownOpen = false;
      }
    };
    document.addEventListener("click", this._onDocClick);
  },

  beforeUnmount() {
    document.removeEventListener("click", this._onDocClick);
  },

  computed: {

    isAuthenticated() {
      return this.userStore && this.userStore.isAuthenticated;
    },

    isAdmin() {
      return this.userStore && this.userStore.isAdmin;
    },

    isStudent() {
      return this.userStore?.user?.role === "student";
    },

    isCompany() {
      return this.userStore?.user?.role === "company";
    },

    displayName() {
      if (!this.userStore || !this.userStore.user) return "Account";
      return this.userStore.user.name || this.userStore.user.email || "Account";
    },

    userInitial() {
      const name =
        this.userStore &&
        this.userStore.user &&
        (this.userStore.user.name || this.userStore.user.email);

      return name ? String(name).charAt(0).toUpperCase() : "U";
    },

    profileRoute() {
      if (this.isAdmin) return "/admin/dashboard";
      if (this.isCompany) return "/company/dashboard";
      if (this.isStudent) return "/student/dashboard";
      return "/homepage";
    }

  },

  methods: {

    handleLogout() {
      this.dropdownOpen = false;
      if (this.userStore) {
        this.userStore.logout();
      }
      this.$router.push("/login");
    }

  }

};
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">

      <router-link class="navbar-brand fw-bold" to="/">
        Placement Portal
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNav">

        <!-- LEFT SIDE -->
        <ul class="navbar-nav me-auto">

          <!-- STUDENT -->
          <li class="nav-item" v-if="isStudent">
            <router-link class="nav-link" to="/student/dashboard">
              Dashboard
            </router-link>
          </li>

          <li class="nav-item" v-if="isStudent">
            <router-link class="nav-link" to="/student/drives">
              Placement Drives
            </router-link>
          </li>

          <li class="nav-item" v-if="isStudent">
            <router-link class="nav-link" to="/student/applications">
              My Applications
            </router-link>
          </li>

          <!-- COMPANY -->
          <li class="nav-item" v-if="isCompany">
            <router-link class="nav-link" to="/company/dashboard">
              Dashboard
            </router-link>
          </li>

          <!-- ADMIN -->
          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link text-warning" to="/admin/dashboard">
              Admin Dashboard
            </router-link>
          </li>

          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link" to="/admin/companies">
              Companies
            </router-link>
          </li>

          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link" to="/admin/students">
              Students
            </router-link>
          </li>

        </ul>


        <!-- RIGHT SIDE -->
        <ul class="navbar-nav ms-auto align-items-center">

          <!-- NOT LOGGED IN -->
          <template v-if="!isAuthenticated">

            <li class="nav-item me-2">
              <router-link class="btn btn-outline-primary btn-sm" to="/login">
                Login
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="btn btn-primary btn-sm" to="/register">
                Register
              </router-link>
            </li>

          </template>


          <!-- LOGGED IN -->
          <template v-else>

            <li class="nav-item dropdown" :class="{ show: dropdownOpen }">

              <a
                class="nav-link dropdown-toggle d-flex align-items-center"
                href="#"
                @click.prevent="dropdownOpen = !dropdownOpen"
              >

                <span
                  class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center me-2"
                  style="width:36px;height:36px;font-size:0.9rem"
                >
                  {{ userInitial }}
                </span>

                <span class="small">{{ displayName }}</span>

              </a>

              <ul class="dropdown-menu dropdown-menu-end" :class="{ show: dropdownOpen }">

                <li>
                  <router-link class="dropdown-item" :to="profileRoute">
                    Profile
                  </router-link>
                </li>

                <li><hr class="dropdown-divider"></li>

                <li>
                  <button
                    class="dropdown-item text-danger"
                    @click.prevent="handleLogout"
                  >
                    Logout
                  </button>
                </li>

              </ul>

            </li>

          </template>

        </ul>

      </div>
    </div>
  </nav>
</template>


<style scoped>

.navbar-brand {
  letter-spacing: 0.4px;
  font-size: 1.1rem;
}

.rounded-circle {
  flex: 0 0 auto;
}

.dropdown-toggle::after {
  margin-left: 0.4rem;
}

.dropdown-menu {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.nav-link {
  font-weight: 500;
}

.nav-link:hover {
  color: #0d6efd;
}

</style>
