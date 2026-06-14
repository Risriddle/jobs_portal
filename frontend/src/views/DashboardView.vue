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

async function fetchJobs() {
  try {
    loading.value = true;

    const response = await api.get("/jobs/");
    jobs.value = response.data;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

async function fetchStatuses() {
  try {
    const response = await api.get("/statuses/");
    statuses.value = response.data;
  } catch (error) {
    console.error(error);
  }
}

async function deleteJob(id) {
  if (!confirm("Delete this job?")) return;

  try {
    await api.delete(`/jobs/${id}/`);
    fetchJobs();
  } catch (error) {
    console.error(error);
  }
}

async function duplicateJob(id) {
  try {
    await api.post(`/jobs/${id}/duplicate/`);
    fetchJobs();
  } catch (error) {
    console.error(error);
  }
}

const filteredJobs = computed(() => {
  let result = jobs.value;

  if (search.value) {
    result = result.filter((job) =>
      job.title.toLowerCase().includes(search.value.toLowerCase())
    );
  }

  if (selectedStatus.value) {
    result = result.filter((job) =>
      job.status_details?.some(
        (status) => status.id === Number(selectedStatus.value)
      )
    );
  }

  return result;
});

onMounted(async () => {
  await Promise.all([
    fetchJobs(),
    fetchStatuses()
  ]);
});
</script>

<template>
  <div class="container">

    <div class="header">
      <h1>Job Dashboard</h1>

      <button @click="showModal = true">
        Post Job
      </button>

      <router-link to="/analytics">
  Analytics
</router-link>
    </div>

    <div class="filters">

      <input
        v-model="search"
        placeholder="Search by title"
      />

      <select v-model="selectedStatus">

        <option value="">
          All Statuses
        </option>

        <option
          v-for="status in statuses"
          :key="status.id"
          :value="status.id"
        >
          {{ status.name }}
        </option>

      </select>

    </div>

    <div v-if="loading">
      Loading jobs...
    </div>

    <div
      v-else-if="filteredJobs.length === 0"
      class="empty-state"
    >
      No Jobs Found
    </div>

    <div
      v-else
      class="grid"
    >
      <JobCard
        v-for="job in filteredJobs"
        :key="job.id"
        :job="job"
        @delete="deleteJob"
        @duplicate="duplicateJob"
      />
    </div>

    <JobForm
      v-if="showModal"
      @close="showModal = false"
      @created="fetchJobs"
    />

  </div>
</template>

<style>
.container {
  max-width: 1400px;
  margin: auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  display: flex;
  gap: 12px;
  margin: 20px 0;
}

.filters input,
.filters select {
  padding: 10px;
}

.grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.empty-state {
  text-align: center;
  font-size: 18px;
  padding: 50px;
}
</style>