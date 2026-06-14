<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";

const emit = defineEmits(["close", "created"]);

const props = defineProps({
  jobToEdit: {
    type: Object,
    default: null
  }
});

const isEditMode = computed(() => !!props.jobToEdit);

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
  const [statusRes, categoryRes] = await Promise.all([
    api.get("/statuses/"),
    api.get("/categories/")
  ]);

  statuses.value = statusRes.data;
  categories.value = categoryRes.data;

  if (props.jobToEdit) {
    const job = props.jobToEdit;

    title.value = job.title;
    description.value = job.description;

    address.value = job.address;
    city.value = job.city;
    state.value = job.state;

    startDate.value = job.start_date;
    endDate.value = job.end_date;

    selectedStatuses.value = job.status_details.map(s => s.id);
    selectedCategories.value = job.category_details.map(c => c.id);

    imagePreview.value = job.profile_picture;
  }
});

function handleImage(e) {
  const file = e.target.files[0];
  if (!file) return;

  image.value = file;
  imagePreview.value = URL.createObjectURL(file);
}

async function submitJob() {
  if (!title.value.trim()) {
    alert("Title required");
    return;
  }

  if (endDate.value < startDate.value) {
    alert("Invalid dates");
    return;
  }

  loading.value = true;

  try {
    const formData = new FormData();

    formData.append("title", title.value);
    formData.append("description", description.value);
    formData.append("address", address.value);
    formData.append("city", city.value);
    formData.append("state", state.value);
    formData.append("start_date", startDate.value);
    formData.append("end_date", endDate.value);

    selectedStatuses.value.forEach(s =>
      formData.append("statuses", s)
    );

    selectedCategories.value.forEach(c =>
      formData.append("categories", c)
    );

    if (image.value) {
      formData.append("profile_picture", image.value);
    }

    if (isEditMode.value) {
      await api.patch(`/jobs/${props.jobToEdit.id}/`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
    } else {
      await api.post("/jobs/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
    }

    emit("created");
    emit("close");

  } catch (err) {
    console.error(err);
    alert("Failed to save job");
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="overlay">
    <div class="modal">

      <div class="header">
        <h2>
          {{ isEditMode ? "Edit Job" : "Create Job" }}
        </h2>

        <button @click="emit('close')">✕</button>
      </div>

      <input type="file" @change="handleImage" />

      <img v-if="imagePreview" :src="imagePreview" class="preview" />

      <input v-model="title" placeholder="Title" />
      <textarea v-model="description" placeholder="Description" />

      <select multiple v-model="selectedStatuses">
        <option
          v-for="s in statuses"
          :key="s.id"
          :value="s.id"
        >
          {{ s.name }}
        </option>
      </select>

      <select multiple v-model="selectedCategories">
        <option
          v-for="c in categories"
          :key="c.id"
          :value="c.id"
        >
          {{ c.name }}
        </option>
      </select>

      <input v-model="city" placeholder="City" />
      <input v-model="state" placeholder="State" />

      <input type="date" v-model="startDate" />
      <input type="date" v-model="endDate" />

      <button @click="submitJob" :disabled="loading">
        {{ loading ? "Saving..." : isEditMode ? "Update" : "Create" }}
      </button>

      <button @click="emit('close')">Cancel</button>

    </div>
  </div>
</template>