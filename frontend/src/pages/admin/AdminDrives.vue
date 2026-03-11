<template>
  <div class="container mt-4">
    <h2>Manage Placement Drives</h2>
    <p>Review pending drive requests and view approved drives.</p>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>

      <!-- Pending Drive Requests -->
      <div class="d-flex align-items-center gap-3 mb-2 flex-wrap">
        <h5 class="mb-0">Pending Drive Requests</h5>
        <input
          type="text"
          class="form-control form-control-sm"
          style="max-width: 280px"
          v-model="requestSearch"
          placeholder="Search requests..."
        />
      </div>
      <table class="table table-bordered mt-2">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Salary (₹)</th>
            <th>Min CGPA</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredRequests.length === 0">
            <td colspan="8" class="text-center text-muted">No drive requests match your search.</td>
          </tr>
          <tr v-for="(req, i) in filteredRequests" :key="req.id">
            <td>{{ i + 1 }}</td>
            <td>{{ companyName(req.data?.company_id) }}</td>
            <td>{{ req.data?.job_title }}</td>
            <td>{{ req.data?.salary?.toLocaleString() ?? '—' }}</td>
            <td>{{ req.data?.min_cgpa }}</td>
            <td>{{ req.data?.application_deadline }}</td>
            <td><span :class="statusBadgeClass(req.status)">{{ req.status }}</span></td>
            <td>
              <template v-if="req.status === 'pending'">
                <button class="btn btn-success btn-sm me-1" :disabled="req._loading" @click="approve(req)">Approve</button>
                <button class="btn btn-danger btn-sm" :disabled="req._loading" @click="reject(req)">Reject</button>
              </template>
              <span v-else class="text-muted">—</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Approved Drives -->
      <div class="d-flex align-items-center gap-3 mt-5 mb-2 flex-wrap">
        <h5 class="mb-0">Approved Drives</h5>
        <input
          type="text"
          class="form-control form-control-sm"
          style="max-width: 280px"
          v-model="driveSearch"
          placeholder="Search drives..."
        />
      </div>
      <table class="table table-bordered mt-2">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Drive Name</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Salary (₹)</th>
            <th>Min CGPA</th>
            <th>Deadline</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredDrives.length === 0">
            <td colspan="7" class="text-center text-muted">No approved drives match your search.</td>
          </tr>
          <tr v-for="(drive, i) in filteredDrives" :key="drive.id">
            <td>{{ i + 1 }}</td>
            <td>{{ drive.drive_name }}</td>
            <td>{{ companyName(drive.company_id) }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.salary?.toLocaleString() ?? '—' }}</td>
            <td>{{ drive.min_cgpa }}</td>
            <td>{{ drive.application_deadline }}</td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { lifecycleStatusBadgeClass } from "@/utils/ui";

export default {
  name: "AdminDrives",
  data() {
    return {
      requests: [],
      drives: [],
      companyMap: {},
      loading: false,
      error: null,
      requestSearch: '',
      driveSearch: '',
    };
  },
  computed: {
    filteredRequests() {
      const q = this.requestSearch.trim().toLowerCase();
      if (!q) return this.requests;
      return this.requests.filter(r =>
        (this.companyName(r.data?.company_id)).toLowerCase().includes(q) ||
        (r.data?.job_title || '').toLowerCase().includes(q) ||
        (r.status || '').toLowerCase().includes(q)
      );
    },
    filteredDrives() {
      const q = this.driveSearch.trim().toLowerCase();
      if (!q) return this.drives;
      return this.drives.filter(d =>
        (d.drive_name || '').toLowerCase().includes(q) ||
        (this.companyName(d.company_id)).toLowerCase().includes(q) ||
        (d.job_title || '').toLowerCase().includes(q)
      );
    },
  },
  async mounted() {
    this.loading = true;
    try {
      const [requests, drives, companies] = await Promise.all([
        api.get("/admin/requests"),
        api.get("/drives"),
        api.get("/companies"),
      ]);
      companies.forEach((c) => {
        this.companyMap[c.id] = c.company_name;
      });
      this.requests = requests;
      this.drives = drives;
    } catch (err) {
      this.error = err.message || "Failed to load drives.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    companyName(id) {
      return this.companyMap[id] ?? `Company #${id}`;
    },
    statusBadgeClass(status) {
      return lifecycleStatusBadgeClass(status);
    },
    async approve(req) {
      req._loading = true;
      try {
        await api.patch(`/admin/drives/${req.id}/approve`, {});
        req.status = "approved";
        // reload approved drives table
        this.drives = await api.get("/drives");
      } catch (err) {
        alert(err.message || "Failed to approve drive.");
      } finally {
        req._loading = false;
      }
    },
    async reject(req) {
      req._loading = true;
      try {
        await api.patch(`/admin/drives/${req.id}/reject`, {});
        req.status = "rejected";
      } catch (err) {
        alert(err.message || "Failed to reject drive.");
      } finally {
        req._loading = false;
      }
    },
  },
};
</script>
