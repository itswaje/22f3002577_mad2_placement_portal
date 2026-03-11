<template>
  <div class="container py-5" style="max-width: 640px">
    <div class="mb-4">
      <router-link to="/student/dashboard" class="btn btn-outline-secondary btn-sm">
        <i class="bi bi-arrow-left me-1"></i> Back to Dashboard
      </router-link>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white border-bottom py-3">
        <h5 class="fw-bold mb-0"><i class="bi bi-person-gear me-2"></i>Edit Profile</h5>
      </div>
      <div class="card-body p-4">

        <!-- Loading -->
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-muted mt-2 mb-0">Loading your profile...</p>
        </div>

        <!-- Error -->
        <div v-else-if="fetchError" class="alert alert-danger">{{ fetchError }}</div>

        <!-- Form -->
        <form v-else @submit.prevent="handleSubmit">
          <!-- Name (read-only, managed at account level) -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Name</label>
            <input type="text" class="form-control" :value="form.name" disabled />
            <div class="form-text">Name is managed at the account level.</div>
          </div>

          <!-- Branch -->
          <div class="mb-3">
            <label for="branch" class="form-label fw-semibold">Branch <span class="text-danger">*</span></label>
            <input
              id="branch"
              type="text"
              class="form-control"
              v-model="form.branch"
              placeholder="e.g. Computer Science"
              required
            />
          </div>

          <!-- Year -->
          <div class="mb-3">
            <label for="year" class="form-label fw-semibold">Year <span class="text-danger">*</span></label>
            <select id="year" class="form-select" v-model.number="form.year" required>
              <option value="" disabled>Select year</option>
              <option :value="1">1st Year</option>
              <option :value="2">2nd Year</option>
              <option :value="3">3rd Year</option>
              <option :value="4">4th Year</option>
            </select>
          </div>

          <!-- CGPA -->
          <div class="mb-3">
            <label for="cgpa" class="form-label fw-semibold">CGPA <span class="text-danger">*</span></label>
            <input
              id="cgpa"
              type="number"
              class="form-control"
              v-model.number="form.cgpa"
              min="0"
              max="10"
              step="0.01"
              placeholder="e.g. 8.5"
              required
            />
            <div class="form-text">Enter a value between 0 and 10.</div>
          </div>

          <!-- Skills -->
          <div class="mb-4">
            <label for="skills" class="form-label fw-semibold">Skills</label>
            <textarea
              id="skills"
              class="form-control"
              v-model="form.skills"
              rows="3"
              placeholder="e.g. Python, React, Machine Learning"
            ></textarea>
            <div class="form-text">Comma-separated list of your key skills.</div>
          </div>

          <!-- Success / Error messages -->
          <div v-if="successMsg" class="alert alert-success py-2">
            <i class="bi bi-check-circle me-1"></i> {{ successMsg }}
          </div>
          <div v-if="submitError" class="alert alert-danger py-2">{{ submitError }}</div>

          <!-- Actions -->
          <div class="d-flex gap-2 justify-content-end">
            <router-link to="/student/dashboard" class="btn btn-outline-secondary">Cancel</router-link>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              Save Changes
            </button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { useUserStore } from "@/stores/user";

export default {
  name: "StudentEditProfile",
  data() {
    return {
      form: {
        name: "",
        branch: "",
        year: "",
        cgpa: "",
        skills: "",
      },
      profileId: null,
      loading: true,
      fetchError: null,
      submitting: false,
      successMsg: null,
      submitError: null,
    };
  },
  async mounted() {
    try {
      const profile = await api.get("/students/me");
      this.profileId = profile.id;
      this.form.name = profile.name || useUserStore().user?.name || "";
      this.form.branch = profile.branch || "";
      this.form.year = profile.year || "";
      this.form.cgpa = profile.cgpa || "";
      this.form.skills = profile.skills || "";
    } catch (err) {
      this.fetchError = err.message || "Failed to load profile.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async handleSubmit() {
      this.successMsg = null;
      this.submitError = null;
      this.submitting = true;
      try {
        await api.put(`/students/${this.profileId}`, {
          branch: this.form.branch,
          year: this.form.year,
          cgpa: this.form.cgpa,
          skills: this.form.skills,
        });
        this.successMsg = "Profile updated successfully!";
        // Clear message after 3 seconds
        setTimeout(() => { this.successMsg = null; }, 3000);
      } catch (err) {
        this.submitError = err.message || "Failed to update profile.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>
