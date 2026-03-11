<template>
  <div>
    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="!applications.length" class="text-center py-5 text-muted">
      <i class="bi bi-inbox fs-1 d-block mb-2"></i>
      No applications found.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Drive / Job Title</th>
            <th>Company</th>
            <th>Salary (₹)</th>
            <th>Applied On</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(app, i) in applications" :key="app.id">
            <td class="text-muted small">{{ i + 1 }}</td>
            <td>
              <div class="fw-semibold">{{ app.drive?.job_title || '—' }}</div>
              <small class="text-muted">{{ app.drive?.drive_name }}</small>
            </td>
            <td>{{ app.drive?.company_name || '—' }}</td>
            <td>
              {{ app.drive?.salary ? '₹' + Number(app.drive.salary).toLocaleString('en-IN') : '—' }}
            </td>
            <td class="small text-muted">{{ formatDate(app.applied_date) }}</td>
            <td>
              <span :class="statusBadgeClass(resolveStatus(app))" class="badge rounded-pill px-3 py-1 text-capitalize">
                {{ resolveStatus(app) }}
              </span>
              <div v-if="resolveStatus(app) === 'cancelled'" class="small text-muted mt-1">
                Company was blacklisted by admin.
              </div>
            </td>
            <td>
              <button
                v-if="canWithdraw(app)"
                class="btn btn-outline-danger btn-sm"
                @click="$emit('withdraw', app.id)"
              >
                Withdraw
              </button>
              <router-link
                v-else
                :to="`/student/drives/${app.drive_id}`"
                class="btn btn-outline-secondary btn-sm"
              >
                View Drive
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { applicationStatusBadgeClass, formatDate } from "@/utils/ui";

export default {
  name: "ApplicationTable",
  props: {
    applications: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
  },
  emits: ["withdraw"],
  methods: {
    statusBadgeClass(status) {
      return applicationStatusBadgeClass(status);
    },
    resolveStatus(app) {
      if (app?.drive?.status === "cancelled") {
        return "cancelled";
      }
      return app?.status || "applied";
    },
    canWithdraw(app) {
      const status = this.resolveStatus(app);
      return ["applied", "pending"].includes(status?.toLowerCase());
    },
    formatDate(dateStr) {
      return formatDate(dateStr);
    },
  },
};
</script>
