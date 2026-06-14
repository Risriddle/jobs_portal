<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const emit = defineEmits([
  "close",
  "created"
]);

const statuses = ref([]);
const categories = ref([]);

const loading = ref(false);

const title = ref("");
const description = ref("");

const address = ref("");
const city = ref("");
const state = ref("");

const startDate = ref("");
const endDate = ref("");

const selectedStatuses = ref([]);
const selectedCategories = ref([]);

const image = ref(null);
const imagePreview = ref(null);

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

function handleImage(event) {
  const file = event.target.files[0];

  if (!file) return;

  image.value = file;
  imagePreview.value = URL.createObjectURL(file);
}

async function createJob() {
  if (!title.value.trim()) {
    alert("Title is required");
    return;
  }

  if (endDate.value < startDate.value) {
    alert("End date cannot be before start date");
    return;
  }

  try {
    loading.value = true;

    const formData = new FormData();

    formData.append("title", title.value);
    formData.append("description", description.value);

    formData.append("address", address.value);
    formData.append("city", city.value);
    formData.append("state", state.value);

    formData.append("start_date", startDate.value);
    formData.append("end_date", endDate.value);

    selectedStatuses.value.forEach((status) => {
      formData.append("statuses", status);
    });

    selectedCategories.value.forEach((category) => {
      formData.append("categories", category);
    });

    if (image.value) {
      formData.append(
        "profile_picture",
        image.value
      );
    }

    await api.post(
      "/jobs/",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data"
        }
      }
    );

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
  <div class="overlay">

    <div class="modal">

      <div class="header">
        <h2>Create Job</h2>

        <button
          class="close-btn"
          @click="emit('close')"
        >
          ✕
        </button>
      </div>

      <div class="form-group">

        <label>
          Job Profile Picture
        </label>

        <input
          type="file"
          accept="image/*"
          @change="handleImage"
        />

      </div>

      <div
        v-if="imagePreview"
        class="preview"
      >
        <img
          :src="imagePreview"
          alt="Preview"
        />
      </div>

      <div class="form-group">

        <label>
          Job Title
        </label>

        <input
          v-model="title"
          placeholder="Enter job title"
        />

      </div>

      <div class="form-group">

        <label>
          Description
        </label>

        <textarea
          v-model="description"
          rows="4"
          placeholder="Enter description"
        />

      </div>

      <div class="form-group">

        <label>
          Status
        </label>

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

        <label>
          Category
        </label>

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

        <label>
          Address
        </label>

        <input
          v-model="address"
          placeholder="Address"
        />

      </div>

      <div class="location-grid">

        <div>

          <label>
            City
          </label>

          <input
            v-model="city"
            placeholder="City"
          />

        </div>

        <div>

          <label>
            State
          </label>

          <input
            v-model="state"
            placeholder="State"
          />

        </div>

      </div>

      <div class="date-grid">

        <div>

          <label>
            Start Date
          </label>

          <input
            type="date"
            v-model="startDate"
          />

        </div>

        <div>

          <label>
            End Date
          </label>

          <input
            type="date"
            v-model="endDate"
          />

        </div>

      </div>

      <div class="actions">

        <button
          class="primary"
          @click="createJob"
          :disabled="loading"
        >
          {{
            loading
              ? "Creating..."
              : "Create Job"
          }}
        </button>

        <button
          class="secondary"
          @click="emit('close')"
        >
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;

  background: rgba(0, 0, 0, 0.5);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 999;
}

.modal {
  background: white;

  width: 700px;
  max-width: 95%;

  max-height: 90vh;
  overflow-y: auto;

  padding: 24px;

  border-radius: 12px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 20px;
}

.close-btn {
  border: none;
  background: none;

  cursor: pointer;

  font-size: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;

  margin-bottom: 16px;
}

input,
textarea,
select {
  margin-top: 6px;
  padding: 10px;
}

select {
  min-height: 100px;
}

.preview {
  margin-bottom: 20px;
}

.preview img {
  width: 180px;
  height: 180px;

  object-fit: cover;

  border-radius: 10px;
}

.location-grid,
.date-grid {
  display: grid;

  grid-template-columns: 1fr 1fr;

  gap: 12px;

  margin-bottom: 16px;
}

.actions {
  display: flex;
  gap: 12px;

  margin-top: 20px;
}

.primary {
  padding: 10px 18px;
}

.secondary {
  padding: 10px 18px;
}
</style>