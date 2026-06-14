<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const emit = defineEmits([
  "close",
  "created"
]);

const statuses = ref([]);
const categories = ref([]);

const title = ref("");
const description = ref("");

const address = ref("");
const city = ref("");
const state = ref("");

const startDate = ref("");
const endDate = ref("");

const selectedStatuses = ref([]);
const selectedCategories = ref([]);

const loading = ref(false);

onMounted(async () => {
  try {
    const statusRes = await api.get("/statuses/");
    const categoryRes = await api.get("/categories/");

    statuses.value = statusRes.data;
    categories.value = categoryRes.data;
  } catch (error) {
    console.error(error);
  }
});

async function createJob() {
  try {
    loading.value = true;

    await api.post("/jobs/", {
      title: title.value,
      description: description.value,

      statuses: selectedStatuses.value,
      categories: selectedCategories.value,

      address: address.value,
      city: city.value,
      state: state.value,

      start_date: startDate.value,
      end_date: endDate.value
    });

    emit("created");
    emit("close");

  } catch (error) {
    console.error(error);

    alert("Failed to create job");
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="modal-overlay">

    <div class="modal">

      <h2>Create Job</h2>

      <div class="form-group">
        <label>Job Title</label>

        <input
          v-model="title"
          type="text"
          placeholder="Enter job title"
        />
      </div>

      <div class="form-group">
        <label>Description</label>

        <textarea
          v-model="description"
          rows="5"
          placeholder="Enter job description"
        />
      </div>

      <div class="form-group">
        <label>Status</label>

        <select
          multiple
          v-model="selectedStatuses"
        >
          <option
            v-for="status in statuses"
            :key="status.id"
            :value="status.id"
          >
            {{ status.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Category</label>

        <select
          multiple
          v-model="selectedCategories"
        >
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Address</label>

        <input
          v-model="address"
          type="text"
          placeholder="Address"
        />
      </div>

      <div class="form-group">
        <label>City</label>

        <input
          v-model="city"
          type="text"
          placeholder="City"
        />
      </div>

      <div class="form-group">
        <label>State</label>

        <input
          v-model="state"
          type="text"
          placeholder="State"
        />
      </div>

      <div class="form-group">
        <label>Start Date</label>

        <input
          v-model="startDate"
          type="date"
        />
      </div>

      <div class="form-group">
        <label>End Date</label>

        <input
          v-model="endDate"
          type="date"
        />
      </div>

      <div class="button-group">

        <button
          @click="createJob"
          :disabled="loading"
        >
          {{ loading ? "Creating..." : "Create Job" }}
        </button>

        <button @click="emit('close')">
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);

  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;

  width: 600px;
  max-width: 90%;

  padding: 24px;

  border-radius: 12px;
}

.form-group {
  margin-bottom: 16px;

  display: flex;
  flex-direction: column;
}

input,
textarea,
select {
  padding: 10px;
  margin-top: 6px;
}

select {
  min-height: 120px;
}

.button-group {
  display: flex;
  gap: 12px;
}

button {
  padding: 10px 16px;
  cursor: pointer;
}
</style>