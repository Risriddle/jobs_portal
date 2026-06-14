<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";
import "../css/Dashboard.css"
import JobCard from "../components/JobCard.vue";
import JobForm from "../components/JobForm.vue";

const jobs = ref([]);
const statuses = ref([]);

const loading = ref(true);
const showModal = ref(false);

const search = ref("");
const selectedStatus = ref("");

const editingJob = ref(null);

function openCreate() {
  editingJob.value = null;
  showModal.value = true;
}

function openEdit(job) {
  editingJob.value = job;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  editingJob.value = null;
}

async function fetchJobs() {
  loading.value = true;
  try {
    const res = await api.get("/jobs/");
    jobs.value = res.data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function fetchStatuses() {
  try {
    const res = await api.get("/statuses/");
    statuses.value = res.data;
  } catch (err) {
    console.error(err);
  }
}

async function deleteJob(id) {
  if (!confirm("Delete this job?")) return;
  await api.delete(`/jobs/${id}/`);
  fetchJobs();
}

async function duplicateJob(id) {
  await api.post(`/jobs/${id}/duplicate/`);
  fetchJobs();
}

const filteredJobs = computed(() => {
  let result = jobs.value;

  if (search.value) {
    result = result.filter(j =>
      j.title.toLowerCase().includes(search.value.toLowerCase())
    );
  }

  if (selectedStatus.value) {
    result = result.filter(job =>
      job.status_details?.some(s => s.id === Number(selectedStatus.value))
    );
  }

  return result;
});

onMounted(async () => {
  await Promise.all([fetchJobs(), fetchStatuses()]);
});
</script>

<template>
  <div class="dashboard">

    <!-- Top nav bar -->
    <header class="topbar">
      <div class="topbar-brand">
        <span class="topbar-logo">&#9670;</span>
        <span class="topbar-title">JobBoard</span>
      </div>
      <nav class="topbar-nav">
        <router-link to="/analytics" class="nav-link">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          Analytics
        </router-link>
        <button class="btn-primary" @click="openCreate">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Post Job
        </button>
      </nav>
    </header>

    <!-- Page content -->
    <main class="page-content">

      <!-- Page heading -->
      <div class="page-heading">
        <div>
          <h1>Jobs Dashboard</h1>
          <p class="page-subtitle" v-if="!loading">
            {{ filteredJobs.length }} {{ filteredJobs.length === 1 ? 'listing' : 'listings' }} found
          </p>
        </div>

        <!-- Filters -->
        <div class="filters">
          <div class="search-wrap">
            <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input v-model="search" placeholder="Search listings…" class="search-input" />
          </div>

          <select v-model="selectedStatus" class="status-select">
            <option value="">Status</option>
            <option v-for="status in statuses" :key="status.id" :value="status.id">
              {{ status.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-wrap">
        <div class="spinner"></div>
        <span>Loading listings…</span>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredJobs.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
        </div>
        <h3>No listings found</h3>
        <p>Try adjusting your filters or post a new job.</p>
        <button class="btn-primary" @click="openCreate">Post a Job</button>
      </div>

      <!-- Grid -->
      <div v-else class="jobs-grid">
        <JobCard
          v-for="job in filteredJobs"
          :key="job.id"
          :job="job"
          @delete="deleteJob"
          @duplicate="duplicateJob"
          @edit="openEdit"
        />
      </div>

    </main>

    <!-- Modal -->
    <JobForm
      v-if="showModal"
      :key="editingJob?.id || 'create'"
      :jobToEdit="editingJob"
      @close="closeModal"
      @created="fetchJobs"
    />

  </div>
</template>
