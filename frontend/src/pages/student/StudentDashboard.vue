<template>
  <div class="container-fluid py-4 px-4">
    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-3">
      <div>
        <h2 class="fw-bold mb-1 text-dark">
          Welcome back, <span class="text-primary">{{ studentName }}</span>
        </h2>
        <p class="text-muted mb-0">
          <span class="me-3"><i class="bi bi-mortarboard me-1"></i>{{ profile.branch || '—' }}</span>
          <span class="me-3"><i class="bi bi-calendar3 me-1"></i>Year {{ profile.year || '—' }}</span>
          <span><i class="bi bi-star-fill text-warning me-1"></i>CGPA {{ profile.cgpa || '—' }}</span>
        </p>
      </div>
      <div class="d-flex gap-2">
        <router-link to="/student/drives" class="btn btn-primary">
          <i class="bi bi-search me-1"></i> Browse Drives
        </router-link>
        <router-link to="/student/applications" class="btn btn-outline-secondary">
          <i class="bi bi-clock-history me-1"></i> My Applications
        </router-link>
        <router-link to="/student/edit-profile" class="btn btn-outline-primary">
          <i class="bi bi-pencil-square me-1"></i> Edit Profile
        </router-link>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="text-muted mt-2">Loading your dashboard...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <!-- Stats Row -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
          <div class="stat-card card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="stat-icon bg-primary-subtle text-primary mb-2">
                <i class="bi bi-send-fill"></i>
              </div>
              <div class="display-6 fw-bold text-dark">{{ stats.total }}</div>
              <small class="text-muted">Total Applied</small>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="stat-card card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="stat-icon bg-warning-subtle text-warning mb-2">
                <i class="bi bi-hourglass-split"></i>
              </div>
              <div class="display-6 fw-bold text-dark">{{ stats.pending }}</div>
              <small class="text-muted">Under Review</small>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="stat-card card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="stat-icon bg-info-subtle text-info mb-2">
                <i class="bi bi-person-check-fill"></i>
              </div>
              <div class="display-6 fw-bold text-dark">{{ stats.shortlisted }}</div>
              <small class="text-muted">Shortlisted</small>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="stat-card card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="stat-icon bg-success-subtle text-success mb-2">
                <i class="bi bi-trophy-fill"></i>
              </div>
              <div class="display-6 fw-bold text-dark">{{ stats.selected }}</div>
              <small class="text-muted">Selected / Offer</small>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="stat-card card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="stat-icon bg-dark text-white mb-2">
                <i class="bi bi-slash-circle-fill"></i>
              </div>
              <div class="display-6 fw-bold text-dark">{{ stats.cancelled }}</div>
              <small class="text-muted">Cancelled</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Companies Section -->
      <div class="mb-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center py-3">
            <h6 class="fw-semibold mb-0">
              <i class="bi bi-building me-2"></i>Available Companies with Drives
            </h6>
          </div>
          <div class="card-body">
            <div v-if="companiesWithDrives.length === 0" class="text-center py-5 text-muted">
              <i class="bi bi-briefcase fs-2 d-block mb-2"></i>
              <p>No companies with active drives at the moment.</p>
            </div>
            <div v-else>
              <!-- Company Selection -->
              <div class="mb-3 d-flex flex-wrap gap-2">
                <button
                  @click="selectedCompanyId = null"
                  :class="{ 'btn-primary': selectedCompanyId === null, 'btn-outline-primary': selectedCompanyId !== null }"
                  class="btn btn-sm"
                >
                  All Companies
                </button>
                <button
                  v-for="company in companiesWithDrives"
                  :key="company.id"
                  @click="selectedCompanyId = company.id"
                  :class="{ 'btn-primary': selectedCompanyId === company.id, 'btn-outline-primary': selectedCompanyId !== company.id }"
                  class="btn btn-sm"
                >
                  {{ company.company_name }}
                  <span class="badge bg-light text-dark ms-1">{{ company.drives?.length || 0 }}</span>
                </button>
              </div>

              <!-- Company Drives Grid -->
              <div v-if="filteredCompanyDrives.length" class="row g-3">
                <div
                  v-for="drive in filteredCompanyDrives"
                  :key="drive.id"
                  class="col-12 col-sm-6 col-lg-4"
                >
                  <div class="drive-card card border-0 shadow-sm h-100 d-flex flex-column hover-shadow-lg">
                    <div class="card-body d-flex flex-column">
                      <h6 class="card-title fw-semibold text-primary mb-1 text-truncate">{{ drive.job_title }}</h6>
                      <p class="text-muted small mb-1">{{ drive.company_name }}</p>
                      <div class="small text-muted mb-2">
                        <i class="bi bi-briefcase me-1"></i>{{ drive.drive_name }}
                      </div>
                      <div v-if="drive.job_description" class="small text-secondary mb-3 flex-grow-1">
                        {{ truncateText(drive.job_description, 60) }}
                      </div>
                      <div class="d-flex gap-2 flex-wrap small mb-3">
                        <span v-if="drive.salary" class="badge bg-success-subtle text-success">
                          <i class="bi bi-cash-coin me-1"></i>₹{{ formatSalary(drive.salary) }}
                        </span>
                        <span v-if="drive.min_cgpa" class="badge bg-info-subtle text-info">
                          CGPA {{ drive.min_cgpa }}+
                        </span>
                      </div>
                      <router-link
                        :to="`/student/drives/${drive.id}`"
                        class="btn btn-sm btn-primary mt-auto align-self-start"
                      >
                        <i class="bi bi-arrow-right me-1"></i>View Details
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4 text-muted small">
                <i class="bi bi-inbox fs-2 d-block mb-2"></i>
                No drives available for the selected company.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Recent Applications -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom d-flex justify-content-between align-items-center py-3">
              <h6 class="fw-semibold mb-0">Recent Applications</h6>
              <router-link to="/student/applications" class="btn btn-link btn-sm text-decoration-none p-0">
                View All <i class="bi bi-arrow-right"></i>
              </router-link>
            </div>
            <div class="card-body p-0">
              <div v-if="!recentApplications.length" class="text-center py-5 text-muted">
                <i class="bi bi-inbox fs-2 d-block mb-2"></i>
                No applications yet. <router-link to="/student/drives">Browse drives</router-link> to get started.
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th class="ps-3">Job Title</th>
                      <th>Company</th>
                      <th>Status</th>
                      <th class="pe-3">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="app in recentApplications" :key="app.id">
                      <td class="ps-3">
                        <div class="fw-semibold small">{{ app.drive?.job_title || '—' }}</div>
                        <div class="text-muted" style="font-size:0.75rem">{{ app.drive?.drive_name }}</div>
                      </td>
                      <td class="small">{{ app.drive?.company_name || '—' }}</td>
                      <td>
                        <span :class="statusBadgeClass(resolveStatus(app))" class="badge rounded-pill px-2 py-1 text-capitalize">
                          {{ resolveStatus(app) }}
                        </span>
                      </td>
                      <td class="pe-3">
                        <router-link
                          :to="`/student/drives/${app.drive_id}`"
                          class="btn btn-outline-primary btn-sm"
                        >
                          View
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Links + Profile Summary -->
        <div class="col-lg-4 d-flex flex-column gap-3">
          <!-- Profile Summary -->
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
              <h6 class="fw-semibold mb-0">My Profile</h6>
              <router-link to="/student/edit-profile" class="btn btn-link btn-sm text-decoration-none p-0">
                <i class="bi bi-pencil me-1"></i>Edit
              </router-link>
            </div>
            <div class="card-body">
              <div class="d-flex flex-column gap-2">
                <div class="d-flex justify-content-between small">
                  <span class="text-muted">Name</span>
                  <span class="fw-semibold">{{ profile.name || studentName }}</span>
                </div>
                <div class="d-flex justify-content-between small">
                  <span class="text-muted">Branch</span>
                  <span class="fw-semibold">{{ profile.branch || '—' }}</span>
                </div>
                <div class="d-flex justify-content-between small">
                  <span class="text-muted">Year</span>
                  <span class="fw-semibold">{{ profile.year || '—' }}</span>
                </div>
                <div class="d-flex justify-content-between small">
                  <span class="text-muted">CGPA</span>
                  <span class="fw-semibold">{{ profile.cgpa || '—' }}</span>
                </div>
                <div v-if="profile.skills" class="d-flex justify-content-between small">
                  <span class="text-muted">Skills</span>
                  <span class="fw-semibold text-end" style="max-width: 60%">{{ profile.skills }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3">
              <h6 class="fw-semibold mb-0">Quick Actions</h6>
            </div>
            <div class="card-body d-flex flex-column gap-2">
              <router-link to="/student/drives" class="btn btn-outline-primary btn-sm text-start">
                <i class="bi bi-briefcase me-2"></i>Browse Placement Drives
              </router-link>
              <router-link to="/student/applications" class="btn btn-outline-secondary btn-sm text-start">
                <i class="bi bi-list-check me-2"></i>View Application History
              </router-link>
              <button @click="exportCSV" :disabled="exporting" class="btn btn-outline-success btn-sm text-start">
                <span v-if="exporting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                <i v-else class="bi bi-download me-2"></i>
                {{ exporting ? 'Exporting...' : 'Export Applications CSV' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { useUserStore } from "@/stores/user";
import { applicationStatusBadgeClass } from "@/utils/ui";

export default {
  name: "StudentDashboard",
  data() {
    return {
      profile: {},
      applications: [],
      companies: [],
      allDrives: [],
      selectedCompanyId: null,
      loading: false,
      exporting: false,
      error: null,
    };
  },
  computed: {
    studentName() {
      return useUserStore().user?.name ?? "Student";
    },
    stats() {
      const all = this.applications;
      return {
        total: all.length,
        pending: all.filter((a) => ["applied", "pending"].includes(this.resolveStatus(a)?.toLowerCase())).length,
        shortlisted: all.filter((a) => this.resolveStatus(a)?.toLowerCase() === "shortlisted").length,
        selected: all.filter((a) => this.resolveStatus(a)?.toLowerCase() === "selected").length,
        cancelled: all.filter((a) => this.resolveStatus(a)?.toLowerCase() === "cancelled").length,
      };
    },
    recentApplications() {
      return this.applications.slice(0, 5);
    },
    companiesWithDrives() {
      // Return companies that have at least one approved drive
      return this.companies.filter(company => {
        const companyDrives = this.allDrives.filter(drive => drive.company_id === company.id && drive.status === "approved");
        return companyDrives.length > 0;
      }).map(company => ({
        ...company,
        drives: this.allDrives.filter(drive => drive.company_id === company.id && drive.status === "approved")
      }));
    },
    filteredCompanyDrives() {
      // If a company is selected, show only its drives
      if (this.selectedCompanyId) {
        return this.allDrives.filter(drive => 
          drive.company_id === this.selectedCompanyId && drive.status === "approved"
        );
      }
      // Otherwise, show all approved drives from all companies
      return this.allDrives.filter(drive => drive.status === "approved");
    }
  },
  async mounted() {
    // Show loading only if request takes longer than 300ms
    const loadingTimer = setTimeout(() => {
      this.loading = true;
    }, 300);

    try {
      const profile = await api.get("/students/me");
      this.profile = profile;

      this.applications = await api.get(`/students/${profile.id}/applications/details`);
    } catch (err) {
      this.error = err.message || "Failed to load dashboard.";
    } finally {
      clearTimeout(loadingTimer);
      this.loading = false;
    }

    // Load companies and drives in the background (don't block dashboard)
    try {
      this.companies = await api.get("/companies");
      this.allDrives = await api.get("/drives");
    } catch (err) {
      console.error("Failed to load companies or drives:", err);
    }
  },
  methods: {
    resolveStatus(app) {
      if (app?.drive?.status === "cancelled") {
        return "cancelled";
      }
      return app?.status || "applied";
    },
    statusBadgeClass(status) {
      return applicationStatusBadgeClass(status);
    },
    truncateText(text, length) {
      if (!text) return '';
      return text.length > length ? text.substring(0, length) + '...' : text;
    },
    formatSalary(salary) {
      if (!salary) return '0';
      if (salary >= 1000000) {
        return (salary / 100000).toFixed(1) + 'L';
      }
      return salary.toLocaleString('en-IN');
    },
    async exportCSV() {
      this.exporting = true;
      try {
        const res = await api.post('/students/me/export-csv');
        alert(res.message || 'Export started! You will receive an email with the CSV shortly.');
      } catch (err) {
        alert('Export failed: ' + (err.message || 'Unknown error'));
      } finally {
        this.exporting = false;
      }
    }
  },
};
</script>

<style scoped>
.stat-card {
  border-radius: 12px;
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.drive-card {
  transition: all 0.3s ease;
  border-radius: 10px;
}

.drive-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12) !important;
}

.hover-shadow-lg {
  border-radius: 10px;
}

.bg-success-subtle {
  background-color: #d1e7dd;
}

.text-success {
  color: #198754;
}

.bg-info-subtle {
  background-color: #cfe2ff;
}

.text-info {
  color: #0d6efd;
}
</style>
