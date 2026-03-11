<template>
  <div class="container mt-4" style="max-width: 640px">
    <h2>Create Placement Drive</h2>
    <p class="text-muted">Your request will be sent to the admin for approval.</p>

    <div v-if="success" class="alert alert-success">
      Drive request submitted successfully! Awaiting admin approval.
      <router-link to="/company/dashboard" class="ms-2">Back to Dashboard</router-link>
    </div>

    <form v-else @submit.prevent="submitDrive" class="mt-3">

      <div class="mb-3">
        <label class="form-label">Drive Name <span class="text-danger">*</span></label>
        <input v-model="form.drive_name" type="text" class="form-control" placeholder="e.g. Campus Hiring 2026" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Job Title <span class="text-danger">*</span></label>
        <input v-model="form.job_title" type="text" class="form-control" placeholder="e.g. Software Engineer" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Job Description <span class="text-danger">*</span></label>
        <textarea v-model="form.job_description" class="form-control" rows="3" placeholder="Describe the role and responsibilities" required></textarea>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Eligibility Branch <span class="text-danger">*</span></label>
          <input v-model="form.eligibility_branch" type="text" class="form-control" placeholder="e.g. CSE, ECE, ALL" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Minimum CGPA <span class="text-danger">*</span></label>
          <input v-model.number="form.min_cgpa" type="number" class="form-control" step="0.1" min="0" max="10" placeholder="e.g. 7.5" required />
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Salary (₹ per annum) <span class="text-danger">*</span></label>
          <input v-model.number="form.salary" type="number" class="form-control" min="0" placeholder="e.g. 600000" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Application Deadline <span class="text-danger">*</span></label>
          <input v-model="form.application_deadline" type="date" class="form-control" required />
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Skills Required</label>
        <input v-model="form.skills_required" type="text" class="form-control" placeholder="e.g. Python, React, SQL (optional)" />
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        {{ loading ? "Submitting..." : "Submit for Approval" }}
      </button>

    </form>
  </div>
</template>

<script>
import api from "@/utils/api";

export default {
  name: "CreateDrive",
  data() {
    return {
      form: {
        drive_name: "",
        job_title: "",
        job_description: "",
        eligibility_branch: "",
        min_cgpa: null,
        salary: null,
        skills_required: "",
        application_deadline: "",
      },
      loading: false,
      error: null,
      success: false,
    };
  },
  methods: {
    async submitDrive() {
      this.error = null;
      this.loading = true;
      try {
        await api.post("/drives", this.form);
        this.success = true;
      } catch (err) {
        this.error = err.message || "Failed to submit drive.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
