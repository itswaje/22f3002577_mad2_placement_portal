<template>
  <div class="container mt-4">

    <!-- Back link -->
    <router-link to="/company/dashboard" class="btn btn-outline-secondary btn-sm mb-3">
      &larr; Back to Dashboard
    </router-link>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <!-- Drive Info -->
      <h4>{{ drive.drive_name }}</h4>
      <p class="text-muted mb-1">Job Title: <strong>{{ drive.job_title }}</strong></p>
      <p class="text-muted mb-4">Deadline: {{ drive.application_deadline }}</p>

      <h5>Applicants <span class="badge bg-secondary ms-1">{{ applications.length }}</span></h5>

      <div v-if="applications.length === 0" class="text-muted mt-3">
        No applications received for this drive yet.
      </div>

      <table v-else class="table table-bordered table-hover mt-2">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Student</th>
            <th>Branch</th>
            <th>CGPA</th>
            <th>Status</th>
            <th>Update Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(app, i) in applications" :key="app.id">
            <td>{{ i + 1 }}</td>
            <td>{{ app.student?.name || `Student #${app.student_id}` }}</td>
            <td>{{ app.student?.branch || "—" }}</td>
            <td>{{ app.student?.cgpa || "—" }}</td>
            <td>
              <span :class="statusBadge(app.status)">{{ app.status }}</span>
            </td>
            <td class="d-flex gap-2 align-items-center">
              <select
                v-model="app._newStatus"
                class="form-select form-select-sm"
                style="width: 140px"
              >
                <option value="applied">Applied</option>
                <option value="shortlisted">Shortlisted</option>
                <option value="waiting">Waiting</option>
                <option value="selected">Selected</option>
                <option value="rejected">Rejected</option>
              </select>
              <button
                class="btn btn-primary btn-sm"
                :disabled="app._loading"
                @click="updateStatus(app)"
              >
                Update
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import api from "@/utils/api";
import { applicationStatusBadgeClass } from "@/utils/ui";

export default {
  name: "CompanyApplications",
  data() {
    return {
      drive: {},
      applications: [],
      loading: false,
      error: null,
    };
  },
  async mounted() {
    const driveId = this.$route.query.drive_id;
    if (!driveId) {
      this.error = "No drive selected. Go back and click 'View Applications' on a drive.";
      return;
    }
    this.loading = true;
    try {
      const [drive, applications] = await Promise.all([
        api.get(`/drives/${driveId}`),
        api.get(`/drives/${driveId}/applications/details`),
      ]);
      this.drive = drive;

      // attach editable status field to each application
      this.applications = applications.map((a) => ({ ...a, _newStatus: a.status, _loading: false }));
    } catch (err) {
      this.error = err.message || "Failed to load applications.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    statusBadge(status) {
      return ["badge", applicationStatusBadgeClass(status)];
    },
    async updateStatus(app) {
      if (app._newStatus === app.status) return;
      app._loading = true;
      try {
        const updated = await api.patch(`/applications/${app.id}`, { status: app._newStatus });
        app.status = updated.status;
        app._newStatus = updated.status;
      } catch (err) {
        alert(err.message || "Failed to update status.");
      } finally {
        app._loading = false;
      }
    },
  },
};
</script>
