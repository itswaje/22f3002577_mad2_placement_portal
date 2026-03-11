<template>
  <div class="container-fluid py-4 px-4">
    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-3">
      <div>
        <h2 class="fw-bold text-dark mb-1">My Applications</h2>
        <p class="text-muted mb-0">Track the status of all your placement applications.</p>
      </div>
      <router-link to="/student/drives" class="btn btn-primary">
        <i class="bi bi-search me-1"></i> Browse More Drives
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="text-muted mt-2">Loading your applications...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <!-- Stats Row -->
      <div class="row g-3 mb-4">
        <div v-for="stat in statusStats" :key="stat.label" class="col-6 col-md-3 col-lg-2">
          <div
            class="stat-pill card border-0 shadow-sm text-center py-3 px-2 h-100"
            :class="{ 'active-stat': activeFilter === stat.status }"
            style="cursor: pointer"
            @click="activeFilter = activeFilter === stat.status ? '' : stat.status"
          >
            <div :class="stat.iconClass" class="fs-5 mb-1">
              <i :class="stat.icon"></i>
            </div>
            <div class="fw-bold fs-5">{{ stat.count }}</div>
            <small class="text-muted">{{ stat.label }}</small>
          </div>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom d-flex align-items-center justify-content-between flex-wrap gap-2 py-3">
          <div class="d-flex gap-2 flex-wrap">
            <button
              v-for="tab in filterTabs"
              :key="tab.value"
              class="btn btn-sm"
              :class="activeFilter === tab.value ? 'btn-primary' : 'btn-outline-secondary'"
              @click="activeFilter = tab.value"
            >
              {{ tab.label }}
              <span class="badge ms-1" :class="activeFilter === tab.value ? 'bg-white text-primary' : 'bg-secondary'">
                {{ tab.count }}
              </span>
            </button>
          </div>
          <small class="text-muted">
            {{ filteredApplications.length }} result{{ filteredApplications.length !== 1 ? 's' : '' }}
          </small>
        </div>

        <div class="card-body p-0">
          <!-- Withdraw confirmation banner -->
          <div v-if="withdrawSuccess" class="alert alert-success m-3 py-2 small">
            <i class="bi bi-check-circle-fill me-1"></i> Application withdrawn successfully.
          </div>
          <div v-if="withdrawError" class="alert alert-danger m-3 py-2 small">{{ withdrawError }}</div>

          <div v-if="!filteredApplications.length" class="text-center py-5 text-muted">
            <i class="bi bi-inbox fs-1 d-block mb-2"></i>
            <span v-if="activeFilter">No <strong>{{ activeFilter }}</strong> applications found.</span>
            <span v-else>You haven't applied to any drives yet. <router-link to="/student/drives">Browse drives</router-link>.</span>
          </div>

          <ApplicationTable
            v-else
            :applications="filteredApplications"
            :loading="false"
            @withdraw="confirmWithdraw"
          />
        </div>
      </div>
    </div>

    <!-- Withdraw Confirm Modal -->
    <div
      class="modal fade"
      id="withdrawModal"
      tabindex="-1"
      ref="withdrawModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header border-0">
            <h6 class="modal-title fw-semibold">Withdraw Application</h6>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-muted">
            Are you sure you want to withdraw this application? This action cannot be undone.
          </div>
          <div class="modal-footer border-0">
            <button class="btn btn-outline-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
            <button
              class="btn btn-danger btn-sm"
              :disabled="withdrawing"
              @click="doWithdraw"
            >
              <span v-if="withdrawing"><span class="spinner-border spinner-border-sm me-1"></span></span>
              Withdraw
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import ApplicationTable from "@/components/ApplicationTable.vue";
import { Modal } from "bootstrap";

export default {
  name: "ApplicationHistory",
  components: { ApplicationTable },
  data() {
    return {
      applications: [],
      loading: false,
      error: null,
      activeFilter: "",
      pendingWithdrawId: null,
      withdrawing: false,
      withdrawSuccess: false,
      withdrawError: null,
      withdrawModal: null,
    };
  },
  computed: {
    filterTabs() {
      const total = this.applications.length;
      const counts = this.statusCounts;
      return [
        { label: "All", value: "", count: total },
        { label: "Applied", value: "applied", count: counts.applied },
        { label: "Shortlisted", value: "shortlisted", count: counts.shortlisted },
        { label: "Selected", value: "selected", count: counts.selected },
        { label: "Rejected", value: "rejected", count: counts.rejected },
        { label: "Cancelled", value: "cancelled", count: counts.cancelled },
      ];
    },
    statusCounts() {
      const c = { applied: 0, shortlisted: 0, selected: 0, rejected: 0, cancelled: 0 };
      this.applications.forEach((a) => {
        const s = this.resolveStatus(a).toLowerCase();
        if (s in c) c[s]++;
        else c.applied++;
      });
      return c;
    },
    statusStats() {
      const c = this.statusCounts;
      return [
        { label: "Total", status: "", count: this.applications.length, icon: "bi bi-send-fill", iconClass: "text-primary" },
        { label: "Applied", status: "applied", count: c.applied, icon: "bi bi-clock-fill", iconClass: "text-secondary" },
        { label: "Shortlisted", status: "shortlisted", count: c.shortlisted, icon: "bi bi-person-check-fill", iconClass: "text-info" },
        { label: "Selected", status: "selected", count: c.selected, icon: "bi bi-trophy-fill", iconClass: "text-success" },
        { label: "Rejected", status: "rejected", count: c.rejected, icon: "bi bi-x-circle-fill", iconClass: "text-danger" },
        { label: "Cancelled", status: "cancelled", count: c.cancelled, icon: "bi bi-slash-circle-fill", iconClass: "text-dark" },
      ];
    },
    filteredApplications() {
      if (!this.activeFilter) return this.applications;
      return this.applications.filter(
        (a) => this.resolveStatus(a).toLowerCase() === this.activeFilter
      );
    },
  },
  async mounted() {
    this.withdrawModal = new Modal(this.$refs.withdrawModal);
    this.loading = true;
    try {
      const profile = await api.get("/students/me");
      const apps = await api.get(`/students/${profile.id}/applications`);
      // Enrich with drive details in parallel
      const driveIds = [...new Set(apps.map((a) => a.drive_id))];
      const driveMap = {};
      await Promise.all(
        driveIds.map(async (id) => {
          try {
            driveMap[id] = await api.get(`/drives/${id}`);
          } catch {
            driveMap[id] = null;
          }
        })
      );
      this.applications = apps.map((a) => ({
        ...a,
        drive: driveMap[a.drive_id] ?? null,
      }));
    } catch (err) {
      this.error = err.message || "Failed to load applications.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    resolveStatus(app) {
      if (app?.drive?.status === "cancelled") {
        return "cancelled";
      }
      return app?.status || "applied";
    },
    confirmWithdraw(appId) {
      this.pendingWithdrawId = appId;
      this.withdrawSuccess = false;
      this.withdrawError = null;
      this.withdrawModal.show();
    },
    async doWithdraw() {
      if (!this.pendingWithdrawId) return;
      this.withdrawing = true;
      try {
        await api.delete(`/applications/${this.pendingWithdrawId}`);
        this.applications = this.applications.filter(
          (a) => a.id !== this.pendingWithdrawId
        );
        this.withdrawSuccess = true;
        this.withdrawModal.hide();
      } catch (err) {
        this.withdrawError = err.message || "Failed to withdraw application.";
      } finally {
        this.withdrawing = false;
        this.pendingWithdrawId = null;
      }
    },
  },
};
</script>

<style scoped>
.stat-pill {
  border-radius: 12px;
  transition: all 0.15s ease;
  border: 2px solid transparent !important;
}
.stat-pill:hover {
  border-color: #2563eb !important;
}
.active-stat {
  border-color: #2563eb !important;
  background: #eff6ff;
}
</style>
