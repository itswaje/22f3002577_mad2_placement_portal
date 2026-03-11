<template>
  <div class="container py-4">
    <!-- Back -->
    <button class="btn btn-link text-decoration-none ps-0 mb-3 text-muted" @click="$router.back()">
      <i class="bi bi-arrow-left me-1"></i> Back to Drives
    </button>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="text-muted mt-2">Loading drive details...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="drive">
      <!-- Drive Hero Card -->
      <div class="drive-hero card border-0 shadow mb-4">
        <div class="card-body p-4">
          <div class="d-flex align-items-start gap-4 flex-wrap">
            <div class="company-logo-lg d-flex align-items-center justify-content-center flex-shrink-0">
              {{ companyInitial }}
            </div>
            <div class="flex-grow-1">
              <h3 class="fw-bold mb-1 text-dark">{{ drive.job_title }}</h3>
              <div class="text-muted mb-2">
                <span class="fw-semibold text-primary">{{ drive.company_name || drive.drive_name }}</span>
                &nbsp;&bull;&nbsp;
                {{ drive.drive_name }}
              </div>
              <div class="d-flex flex-wrap gap-3 text-muted small">
                <span><i class="bi bi-mortarboard-fill text-primary me-1"></i>{{ drive.eligibility_branch || 'All Branches' }}</span>
                <span><i class="bi bi-graph-up-arrow text-success me-1"></i>CGPA ≥ {{ drive.min_cgpa ?? '—' }}</span>
                <span><i class="bi bi-cash-stack text-warning me-1"></i>₹{{ drive.salary ? Number(drive.salary).toLocaleString('en-IN') : '—' }} / yr</span>
                <span><i class="bi bi-calendar-event text-danger me-1"></i>Deadline: {{ formatDate(drive.application_deadline) }}</span>
              </div>
            </div>
            <div class="text-end flex-shrink-0">
              <div v-if="alreadyApplied && drive.status === 'cancelled'" class="alert alert-dark mb-2 py-2 px-3 small">
                <i class="bi bi-slash-circle-fill me-1"></i> Application cancelled because the company was blacklisted by admin.
              </div>
              <div v-else-if="alreadyApplied" class="alert alert-success mb-0 py-2 px-3 small">
                <i class="bi bi-check-circle-fill me-1"></i> Already Applied
              </div>
              <div v-else-if="isDeadlinePassed" class="alert alert-secondary mb-0 py-2 px-3 small">
                <i class="bi bi-x-circle me-1"></i> Deadline Passed
              </div>
              <div v-else-if="!studentEligible && eligibilityReasons.length > 0" class="alert alert-warning mb-0 py-2 px-3 small">
                <i class="bi bi-exclamation-triangle-fill me-1"></i> Not Eligible
              </div>
              <button
                v-else-if="!(isDeadlinePassed || alreadyApplied)"
                class="btn btn-primary px-4"
                :disabled="applying"
                @click="applyNow"
              >
                <span v-if="applying"><span class="spinner-border spinner-border-sm me-1"></span> Applying...</span>
                <span v-else><i class="bi bi-send-fill me-1"></i> Apply Now</span>
              </button>

              <div v-if="applySuccess" class="text-success small mt-2">
                <i class="bi bi-check-circle-fill me-1"></i> Application submitted!
              </div>
              <div v-if="applyError" class="text-danger small mt-2">{{ applyError }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Details Grid -->
      <div class="row g-4">
        <!-- Left: Description + Skills -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white border-bottom py-3">
              <h6 class="fw-semibold mb-0"><i class="bi bi-file-text me-2 text-primary"></i>Job Description</h6>
            </div>
            <div class="card-body">
              <p class="text-muted mb-0" style="white-space: pre-line; line-height: 1.7">
                {{ drive.job_description || 'No description provided.' }}
              </p>
            </div>
          </div>

          <div v-if="drive.skills_required" class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3">
              <h6 class="fw-semibold mb-0"><i class="bi bi-tools me-2 text-info"></i>Skills Required</h6>
            </div>
            <div class="card-body">
              <div class="d-flex flex-wrap gap-2">
                <span
                  v-for="skill in skillsList"
                  :key="skill"
                  class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-3 py-2"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Key Info -->
        <div class="col-lg-4">
          <!-- Eligibility Card -->
          <div v-if="eligibilityChecked" class="card border-0 shadow-sm mb-4" :class="studentEligible ? 'border-success' : 'border-warning'">
            <div class="card-header" :class="studentEligible ? 'bg-light-success' : 'bg-light-warning'">
              <h6 class="fw-semibold mb-0" :class="studentEligible ? 'text-success' : 'text-warning'">
                <i :class="studentEligible ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-triangle-fill'" class="me-2"></i>
                <span>{{ studentEligible ? 'You Are Eligible' : 'Not Eligible' }}</span>
              </h6>
            </div>
            <div class="card-body">
              <div v-if="studentEligible" class="text-success small">
                <i class="bi bi-check-lg me-2"></i> You meet all eligibility criteria for this drive.
              </div>
              <div v-else class="d-flex flex-column gap-2">
                <div v-for="(reason, idx) in eligibilityReasons" :key="idx" class="alert alert-warning py-2 px-3 mb-0 small">
                  <i class="bi bi-exclamation-circle me-2"></i>{{ reason }}
                </div>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3">
              <h6 class="fw-semibold mb-0"><i class="bi bi-info-circle me-2 text-secondary"></i>Drive Details</h6>
            </div>
            <div class="card-body">
              <div class="d-flex flex-column gap-3">
                <div class="detail-row">
                  <div class="detail-label text-muted small">Drive Name</div>
                  <div class="fw-semibold small">{{ drive.drive_name }}</div>
                </div>
                <div class="detail-row">
                  <div class="detail-label text-muted small">Eligible Branches</div>
                  <div class="fw-semibold small">{{ drive.eligibility_branch || 'All Branches' }}</div>
                </div>
                <div class="detail-row">
                  <div class="detail-label text-muted small">Minimum CGPA</div>
                  <div class="fw-semibold small">{{ drive.min_cgpa ?? '—' }}</div>
                </div>
                <div class="detail-row">
                  <div class="detail-label text-muted small">Annual Salary</div>
                  <div class="fw-semibold small text-success">
                    ₹{{ drive.salary ? Number(drive.salary).toLocaleString('en-IN') : '—' }}
                  </div>
                </div>
                <div class="detail-row">
                  <div class="detail-label text-muted small">Application Deadline</div>
                  <div class="fw-semibold small" :class="isDeadlinePassed ? 'text-danger' : 'text-dark'">
                    {{ formatDate(drive.application_deadline) }}
                    <span v-if="isDeadlinePassed" class="badge bg-danger ms-1">Closed</span>
                  </div>
                </div>
                <div class="detail-row">
                  <div class="detail-label text-muted small">Status</div>
                  <div>
                    <span :class="statusBadgeClass(drive.status)" class="badge rounded-pill px-2 py-1">
                      {{ drive.status }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="!alreadyApplied && !isDeadlinePassed" class="card-footer bg-white border-top p-3">
              <button 
                class="btn btn-primary w-100" 
                :disabled="applying || !studentEligible || !eligibilityChecked" 
                @click="applyNow"
              >
                <span v-if="applying"><span class="spinner-border spinner-border-sm me-1"></span> Applying...</span>
                <span v-else-if="!studentEligible"><i class="bi bi-lock me-1"></i> Not Eligible</span>
                <span v-else><i class="bi bi-send-fill me-1"></i> Apply Now</span>
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

export default {
  name: "DriveDetails",
  data() {
    return {
      drive: null,
      myApplications: [],
      loading: false,
      error: null,
      applying: false,
      applySuccess: false,
      applyError: null,
      studentEligible: false,
      eligibilityReasons: [],
      eligibilityChecked: false,
    };
  },
  computed: {
    driveId() {
      return this.$route.params.id;
    },
    companyInitial() {
      const name = this.drive?.company_name || this.drive?.drive_name || "?";
      return name.charAt(0).toUpperCase();
    },
    skillsList() {
      if (!this.drive?.skills_required) return [];
      return this.drive.skills_required
        .split(/[,;]+/)
        .map((s) => s.trim())
        .filter(Boolean);
    },
    alreadyApplied() {
      return this.myApplications.some((a) => a.drive_id === Number(this.driveId));
    },
    isDeadlinePassed() {
      if (!this.drive?.application_deadline) return false;
      return new Date(this.drive.application_deadline) < new Date();
    },
  },
  async mounted() {
    this.loading = true;
    const store = useUserStore();
    const profileId = store.user?.profile_id;
    try {
      const [drive, apps] = await Promise.all([
        api.get(`/drives/${this.driveId}`),
        profileId ? api.get(`/students/${profileId}/applications`) : Promise.resolve([]),
      ]);
      this.drive = drive;
      this.myApplications = apps;

      // Check eligibility if student logged in and not already applied and deadline not passed
      if (profileId && !this.alreadyApplied && !this.isDeadlinePassed) {
        try {
          const eligibility = await api.get(`/eligibility/${this.driveId}`);
          this.studentEligible = eligibility.eligible;
          this.eligibilityReasons = eligibility.reasons || [];
          this.eligibilityChecked = true;
        } catch (err) {
          // If eligibility check fails, show the error
          console.error("Eligibility check failed:", err);
          this.eligibilityChecked = true;
          this.studentEligible = false;
          this.eligibilityReasons = ["Unable to check eligibility. Please try again later."];
        }
      } else if (this.alreadyApplied || this.isDeadlinePassed) {
        this.eligibilityChecked = true;
      }
    } catch (err) {
      this.error = err.message || "Failed to load drive details.";
      this.eligibilityChecked = true;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async applyNow() {
      this.applyError = null;
      this.applying = true;
      try {
        await api.post("/applications", { drive_id: Number(this.driveId) });
        this.applySuccess = true;
        // Add a placeholder so the applied state is reflected immediately
        this.myApplications.push({ drive_id: Number(this.driveId) });
      } catch (err) {
        // Extract meaningful error from response
        let errorMessage = err.message || "Application failed. Please try again.";
        if (err.response?.data?.message) {
          errorMessage = err.response.data.message;
        }
        this.applyError = errorMessage;
      } finally {
        this.applying = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "—";
      const d = new Date(dateStr);
      if (isNaN(d)) return dateStr;
      return d.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    },
    statusBadgeClass(status) {
      const map = {
        approved: "bg-success",
        pending: "bg-warning text-dark",
        rejected: "bg-danger",
      };
      return map[status?.toLowerCase()] ?? "bg-secondary";
    },
  },
};
</script>

<style scoped>
.drive-hero {
  border-radius: 14px;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
  border-left: 4px solid #2563eb !important;
}
.company-logo-lg {
  width: 72px;
  height: 72px;
  border-radius: 14px;
  background: linear-gradient(135deg, #1e3a5f, #2563eb);
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  flex-shrink: 0;
}
.detail-row {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}
.detail-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.bg-light-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
}
.bg-light-warning {
  background-color: #fff3cd;
  border-color: #ffeaa7;
}
</style>
