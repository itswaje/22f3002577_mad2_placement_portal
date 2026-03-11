<template>
  <div class="drive-card card h-100 shadow-sm border-0">
    <div class="card-header drive-card-header d-flex align-items-center gap-2">
      <div class="company-logo-placeholder">{{ companyInitial }}</div>
      <div class="overflow-hidden">
        <div class="fw-semibold text-white text-truncate">{{ drive.company_name || 'Company' }}</div>
        <small class="text-white-50">{{ drive.drive_name }}</small>
      </div>
    </div>

    <div class="card-body d-flex flex-column gap-2">
      <h6 class="card-title mb-1 text-dark fw-bold">{{ drive.job_title }}</h6>

      <div class="drive-meta d-flex flex-column gap-1">
        <div class="d-flex align-items-center gap-2 text-muted small">
          <i class="bi bi-mortarboard-fill text-primary"></i>
          <span>{{ drive.eligibility_branch || 'All Branches' }}</span>
        </div>
        <div class="d-flex align-items-center gap-2 text-muted small">
          <i class="bi bi-graph-up-arrow text-success"></i>
          <span>CGPA ≥ {{ drive.min_cgpa ?? '—' }}</span>
        </div>
        <div class="d-flex align-items-center gap-2 text-muted small">
          <i class="bi bi-cash-stack text-warning"></i>
          <span>₹{{ drive.salary ? Number(drive.salary).toLocaleString('en-IN') : '—' }} / yr</span>
        </div>
        <div class="d-flex align-items-center gap-2 text-muted small">
          <i class="bi bi-calendar-event text-danger"></i>
          <span>Deadline: {{ formatDate(drive.application_deadline) }}</span>
        </div>
      </div>

      <div v-if="skillsList.length" class="mt-1 d-flex flex-wrap gap-1">
        <span v-for="skill in skillsList" :key="skill" class="badge bg-light text-secondary border">
          {{ skill }}
        </span>
      </div>
    </div>

    <div class="card-footer bg-white border-0 pt-0 pb-3 px-3">
      <router-link :to="`/student/drives/${drive.id}`" class="btn btn-primary btn-sm w-100">
        View Details
      </router-link>
    </div>
  </div>
</template>

<script>
import { formatDate } from "@/utils/ui";

export default {
  name: "DriveCard",
  props: {
    drive: { type: Object, required: true },
  },
  computed: {
    companyInitial() {
      const name = this.drive.company_name || this.drive.drive_name || "?";
      return name.charAt(0).toUpperCase();
    },
    skillsList() {
      if (!this.drive.skills_required) return [];
      return this.drive.skills_required
        .split(/[,;]+/)
        .map((s) => s.trim())
        .filter(Boolean)
        .slice(0, 4);
    },
  },
  methods: {
    formatDate(dateStr) {
      return formatDate(dateStr);
    },
  },
};
</script>

<style scoped>
.drive-card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.drive-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}
.drive-card-header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
  padding: 12px 16px;
}
.company-logo-placeholder {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
