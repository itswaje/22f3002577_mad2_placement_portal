<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <div>
        <h2>Welcome, {{ userName }}</h2>
        <p class="text-muted mb-0">Overview of your placement drives.</p>
      </div>
      <router-link to="/company/create-drive" class="btn btn-primary">
        + Create Drive
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger mt-4">{{ error }}</div>

    <div v-else class="mt-4">
      <h5>Your Drives</h5>
      <table class="table table-bordered table-hover mt-2">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Drive Name</th>
            <th>Job Title</th>
            <th>Salary (₹)</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="drives.length === 0">
            <td colspan="7" class="text-center text-muted">
              No drives yet. Click "+ Create Drive" to submit one for admin approval.
            </td>
          </tr>
          <tr v-for="(drive, i) in drives" :key="drive.id">
            <td>{{ i + 1 }}</td>
            <td>{{ drive.drive_name }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.salary?.toLocaleString() ?? '—' }}</td>
            <td>{{ drive.application_deadline }}</td>
            <td>
              <span :class="statusBadge(drive.status)">{{ drive.status }}</span>
            </td>
            <td>
              <router-link
                :to="`/company/applications?drive_id=${drive.id}`"
                class="btn btn-outline-primary btn-sm"
              >
                View Applications
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { useUserStore } from "@/stores/user";

export default {
  name: "CompanyDashboard",
  data() {
    return {
      drives: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    userName() {
      return useUserStore().user?.name ?? "Company";
    },
  },
  async mounted() {
    const profileId = useUserStore().user?.profile_id;
    if (!profileId) {
      this.error = "Company profile not found. Please log in again.";
      return;
    }
    this.loading = true;
    try {
      this.drives = await api.get(`/companies/${profileId}/drives`);
    } catch (err) {
      this.error = err.message || "Failed to load drives.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    statusBadge(status) {
      return {
        badge: true,
        "bg-warning text-dark": status === "pending",
        "bg-success": status === "approved",
        "bg-danger": status === "rejected",
      };
    },
  },
};
</script>
