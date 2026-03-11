<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-primary bg-gradient text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-4 fw-bold mb-3">
              Campus Placement Portal
            </h1>
            <p class="lead mb-4">
              Connect students with top companies. Apply for placement drives,
              track applications, and launch your career.
            </p>

            <router-link :to="placementDrivesLink" class="btn btn-light btn-lg me-2">
              View Placement Drives
            </router-link>

            <router-link to="/register" class="btn btn-outline-light btn-lg">
              Get Started
            </router-link>
          </div>

          <div class="col-lg-6 d-none d-lg-block text-center">
            <i class="bi bi-briefcase-fill display-1" style="font-size:200px"></i>
          </div>
        </div>
      </div>
    </div>


    <!-- Features Section -->
    <div class="container py-5">
      <div class="row g-4">

        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-building"></i>
              </div>
              <h5 class="card-title">Top Companies</h5>
              <p class="card-text text-muted">
                Leading companies register and conduct placement drives.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-person-check"></i>
              </div>
              <h5 class="card-title">Student Applications</h5>
              <p class="card-text text-muted">
                Students can apply for drives and track application status.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-bar-chart"></i>
              </div>
              <h5 class="card-title">Placement Statistics</h5>
              <p class="card-text text-muted">
                Admin can monitor placement activity 
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>


    <!-- Portal Roles Section -->
    <div class="bg-light py-5">
      <div class="container">

        <h2 class="text-center mb-4">Portal Roles</h2>

        <div class="row g-4">

          <div
            v-for="role in roles"
            :key="role.name"
            class="col-md-4"
          >
            <div class="card h-100 border-0 shadow-sm hover-lift">
              <div class="card-body text-center p-4">

                <i :class="role.icon + ' display-6 mb-3 text-primary'"></i>

                <h5 class="card-title">
                  {{ role.name }}
                </h5>

                <p class="text-muted">
                  {{ role.description }}
                </p>

              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useUserStore } from "@/stores/user";

export default {
  name: "HomePage",

  data() {
    return {
      roles: [
        {
          name: "Students",
          icon: "bi bi-mortarboard",
          description:
            "Register, view placement drives, apply for jobs, and track application status."
        },
        {
          name: "Companies",
          icon: "bi bi-building",
          description:
            "Create placement drives, review student applications, and shortlist candidates."
        },
        {
          name: "Admin",
          icon: "bi bi-shield-check",
          description:
            "Approve companies, manage placement drives, and monitor platform activity."
        }
      ]
    }
  },

  computed: {
    placementDrivesLink() {
      const userStore = useUserStore();
      if (userStore?.isStudent) return "/student/drives";
      if (userStore?.isCompany) return "/company/dashboard";
      if (userStore?.isAdmin) return "/admin/dashboard";
      return "/login";
    }
  }
}
</script>


<style scoped>

.hover-lift{
  transition: transform 0.2s ease;
}

.hover-lift:hover{
  transform: translateY(-5px);
}

.bg-primary{
  background: linear-gradient(45deg,#0d6efd,#0dcaf0) !important;
}

</style>