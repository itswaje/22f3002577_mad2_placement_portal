<template>
  <div class="container mt-4">
    <h2>Manage Companies</h2>
    <p>Approve or reject registered companies.</p>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div class="mb-3 mt-3">
        <input
          type="text"
          class="form-control"
          v-model="searchQuery"
          placeholder="Search by company name, industry, location or HR contact..."
        />
      </div>
      <table class="table mt-2">
      <thead>
        <tr>
          <th>Company</th>
          <th>Industry</th>
          <th>Location</th>
          <th>HR Contact</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="filteredCompanies.length === 0">
          <td colspan="6" class="text-center text-muted">No companies match your search.</td>
        </tr>
        <tr v-for="company in filteredCompanies" :key="company.id">
          <td>{{ company.company_name }}</td>
          <td>{{ company.industry }}</td>
          <td>{{ company.location }}</td>
          <td>{{ company.hr_contact }}</td>
          <td>
            <span :class="statusBadgeClass(company.status)">
              {{ company.status }}
            </span>
          </td>
          <td>
            <template v-if="company.status === 'pending'">
              <button
                class="btn btn-success btn-sm me-2"
                :disabled="company._loading"
                @click="approve(company)"
              >
                Approve
              </button>
              <button
                class="btn btn-danger btn-sm"
                :disabled="company._loading"
                @click="reject(company)"
              >
                Reject
              </button>
            </template>
            <button
              v-else-if="company.status !== 'blacklisted'"
              class="btn btn-dark btn-sm"
              :disabled="company._loading"
              @click="blacklist(company)"
            >
              Blacklist
            </button>
            <span v-else class="text-muted">—</span>
          </td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";

export default {
  name: "AdminCompanies",
  data() {
    return {
      companies: [],
      loading: false,
      error: null,
      searchQuery: '',
    };
  },
  computed: {
    filteredCompanies() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) return this.companies;
      return this.companies.filter(c =>
        (c.company_name || '').toLowerCase().includes(q) ||
        (c.industry || '').toLowerCase().includes(q) ||
        (c.location || '').toLowerCase().includes(q) ||
        (c.hr_contact || '').toLowerCase().includes(q)
      );
    },
  },
  async mounted() {
    this.loading = true;
    try {
      this.companies = await api.get("/companies");
    } catch (err) {
      this.error = err.message || "Failed to load companies.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    statusBadgeClass(status) {
      return {
        badge: true,
        "bg-warning text-dark": status === "pending",
        "bg-success": status === "approved",
        "bg-danger": status === "rejected",
        "bg-dark": status === "blacklisted",
      };
    },
    async approve(company) {
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/approve`, {});
        company.status = "approved";
      } catch (err) {
        alert(err.message || "Failed to approve company.");
      } finally {
        company._loading = false;
      }
    },
    async reject(company) {
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/reject`, {});
        company.status = "rejected";
      } catch (err) {
        alert(err.message || "Failed to reject company.");
      } finally {
        company._loading = false;
      }
    },
    async blacklist(company) {
      if (!confirm(`Blacklist company "${company.company_name}"? This will cancel all active drives.`)) return;
      company._loading = true;
      try {
        await api.patch(`/admin/companies/${company.id}/blacklist`, {});
        company.status = "blacklisted";
      } catch (err) {
        alert(err.message || "Failed to blacklist company.");
      } finally {
        company._loading = false;
      }
    },
  },
};
</script>
