<template>
  <div class="container-fluid py-4 px-4">
    <!-- Header -->
    <div class="mb-4">
      <h2 class="fw-bold text-dark mb-1">Placement Drives</h2>
      <p class="text-muted mb-0">Explore all open placement opportunities. Apply before the deadline!</p>
    </div>

    <!-- Search + Filter Bar -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body py-3">
        <div class="row g-2 align-items-center">
          <div class="col-12 col-md-4">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0">
                <i class="bi bi-search text-muted"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control border-start-0"
                placeholder="Search by drive name, job title..."
              />
            </div>
          </div>
          <div class="col-6 col-md-2">
            <select v-model="filterBranch" class="form-select">
              <option value="">All Branches</option>
              <option v-for="b in branchOptions" :key="b" :value="b">{{ b }}</option>
            </select>
          </div>
          <div class="col-6 col-md-2">
            <select v-model="filterSalary" class="form-select">
              <option value="">Any Salary</option>
              <option value="300000">₹3L+</option>
              <option value="600000">₹6L+</option>
              <option value="1000000">₹10L+</option>
              <option value="1500000">₹15L+</option>
            </select>
          </div>
          <div class="col-6 col-md-2">
            <select v-model="sortBy" class="form-select">
              <option value="deadline">Sort: Deadline</option>
              <option value="salary">Sort: Salary (High)</option>
              <option value="name">Sort: Name A–Z</option>
            </select>
          </div>
          <div class="col-6 col-md-2 d-flex gap-2">
            <button class="btn btn-outline-secondary flex-fill" @click="resetFilters">
              <i class="bi bi-x-circle me-1"></i>Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="text-muted mt-2">Loading drives...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <!-- Results count -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <p class="text-muted small mb-0">
          Showing <strong>{{ filteredDrives.length }}</strong> of {{ drives.length }} drives
        </p>
      </div>

      <!-- No results -->
      <div v-if="!filteredDrives.length" class="text-center py-5 text-muted">
        <i class="bi bi-search fs-1 d-block mb-3"></i>
        <h5>No drives match your search</h5>
        <p>Try adjusting your filters or check back later.</p>
        <button class="btn btn-outline-primary" @click="resetFilters">Clear Filters</button>
      </div>

      <!-- Drive Cards Grid -->
      <div v-else class="row g-4">
        <div
          v-for="drive in filteredDrives"
          :key="drive.id"
          class="col-12 col-sm-6 col-lg-4 col-xl-3"
        >
          <DriveCard :drive="drive" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import DriveCard from "@/components/DriveCard.vue";

export default {
  name: "DriveList",
  components: { DriveCard },
  data() {
    return {
      drives: [],
      loading: false,
      error: null,
      search: "",
      filterBranch: "",
      filterSalary: "",
      sortBy: "deadline",
    };
  },
  computed: {
    branchOptions() {
      const branches = this.drives
        .map((d) => d.eligibility_branch)
        .filter(Boolean);
      return [...new Set(branches)].sort();
    },
    filteredDrives() {
      let result = [...this.drives];

      if (this.search.trim()) {
        const q = this.search.toLowerCase();
        result = result.filter(
          (d) =>
            d.drive_name?.toLowerCase().includes(q) ||
            d.job_title?.toLowerCase().includes(q) ||
            d.company_name?.toLowerCase().includes(q) ||
            d.skills_required?.toLowerCase().includes(q)
        );
      }

      if (this.filterBranch) {
        result = result.filter(
          (d) =>
            !d.eligibility_branch ||
            d.eligibility_branch.toLowerCase().includes(this.filterBranch.toLowerCase())
        );
      }

      if (this.filterSalary) {
        const minSal = Number(this.filterSalary);
        result = result.filter((d) => d.salary && Number(d.salary) >= minSal);
      }

      if (this.sortBy === "salary") {
        result.sort((a, b) => (Number(b.salary) || 0) - (Number(a.salary) || 0));
      } else if (this.sortBy === "name") {
        result.sort((a, b) => (a.drive_name || "").localeCompare(b.drive_name || ""));
      } else {
        result.sort((a, b) => {
          const da = a.application_deadline ? new Date(a.application_deadline) : Infinity;
          const db = b.application_deadline ? new Date(b.application_deadline) : Infinity;
          return da - db;
        });
      }

      return result;
    },
  },
  async mounted() {
    this.loading = true;
    try {
      this.drives = await api.get("/drives");
    } catch (err) {
      this.error = err.message || "Failed to load drives.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    resetFilters() {
      this.search = "";
      this.filterBranch = "";
      this.filterSalary = "";
      this.sortBy = "deadline";
    },
  },
};
</script>
