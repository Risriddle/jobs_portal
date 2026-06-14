<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";

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
  console.log("EDIT CLICKED:", job);
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
      job.status_details?.some(
        s => s.id === Number(selectedStatus.value)
      )
    );
  }

  return result;
});

onMounted(async () => {
  await Promise.all([fetchJobs(), fetchStatuses()]);
});
</script>

<template>
  <div class="container">

    <div class="header">
      <h1>Job Dashboard</h1>

      <button @click="openCreate">
        Post Job
      </button>

      <router-link to="/analytics">
        Analytics
      </router-link>
    </div>

    <div class="filters">
      <input v-model="search" placeholder="Search by title" />

      <select v-model="selectedStatus">
        <option value="">All Statuses</option>

        <option
          v-for="status in statuses"
          :key="status.id"
          :value="status.id"
        >
          {{ status.name }}
        </option>
      </select>
    </div>

    <div v-if="loading">Loading jobs...</div>

    <div v-else-if="filteredJobs.length === 0" class="empty-state">
      No Jobs Found
    </div>

    <div v-else class="grid">
      <JobCard
        v-for="job in filteredJobs"
        :key="job.id"
        :job="job"
        @delete="deleteJob"
        @duplicate="duplicateJob"
        @edit="openEdit"
      />
    </div>

    <JobForm
      v-if="showModal"
      :key="editingJob?.id || 'create'"
      :jobToEdit="editingJob"
      @close="closeModal"
      @created="fetchJobs"
    />

  </div>
</template>