<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";
import "../css/JobForm.css"
const emit = defineEmits(["close", "created"]);

const props = defineProps({
  jobToEdit: {
    type: Object,
    default: null
  }
});

const isEditMode = computed(() => !!props.jobToEdit);

const statuses    = ref([]);
const categories  = ref([]);
const loading     = ref(false);

const title             = ref("");
const description       = ref("");
const address           = ref("");
const city              = ref("");
const state             = ref("");
const startDate         = ref("");
const endDate           = ref("");
const selectedStatuses  = ref([]);
const selectedCategories = ref([]);
const image             = ref(null);
const imagePreview      = ref(null);

onMounted(async () => {
  const [statusRes, categoryRes] = await Promise.all([
    api.get("/statuses/"),
    api.get("/categories/")
  ]);

  statuses.value   = statusRes.data;
  categories.value = categoryRes.data;

  if (props.jobToEdit) {
    const job = props.jobToEdit;
    title.value       = job.title;
    description.value = job.description;
    address.value     = job.address;
    city.value        = job.city;
    state.value       = job.state;
    startDate.value   = job.start_date;
    endDate.value     = job.end_date;
    selectedStatuses.value   = job.status_details.map(s => s.id);
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

function toggleStatus(id) {
  const idx = selectedStatuses.value.indexOf(id);
  if (idx === -1) selectedStatuses.value.push(id);
  else selectedStatuses.value.splice(idx, 1);
}

function toggleCategory(id) {
  const idx = selectedCategories.value.indexOf(id);
  if (idx === -1) selectedCategories.value.push(id);
  else selectedCategories.value.splice(idx, 1);
}

async function submitJob() {
  if (!title.value.trim()) { alert("Title is required"); return; }
  if (endDate.value && startDate.value && endDate.value < startDate.value) {
    alert("End date must be after start date"); return;
  }

  loading.value = true;
  try {
    const formData = new FormData();
    formData.append("title",       title.value);
    formData.append("description", description.value);
    formData.append("address",     address.value);
    formData.append("city",        city.value);
    formData.append("state",       state.value);
    formData.append("start_date",  startDate.value);
    formData.append("end_date",    endDate.value);
    selectedStatuses.value.forEach(s => formData.append("statuses", s));
    selectedCategories.value.forEach(c => formData.append("categories", c));
    if (image.value) formData.append("profile_picture", image.value);

    const headers = { "Content-Type": "multipart/form-data" };
    if (isEditMode.value) {
      await api.patch(`/jobs/${props.jobToEdit.id}/`, formData, { headers });
    } else {
      await api.post("/jobs/", formData, { headers });
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
  <!-- Backdrop -->
  <div class="overlay" @click.self="emit('close')">
    <div class="modal" role="dialog" :aria-label="isEditMode ? 'Edit Job' : 'Create Job'">

      <!-- Modal header -->
      <div class="modal-header">
        <h2>{{ isEditMode ? "Edit Job" : "Post a Job" }}</h2>
        <button class="btn-icon close-btn" @click="emit('close')" aria-label="Close">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Scrollable body -->
      <div class="modal-body">

        <!-- Image upload -->
        <div class="field">
          <label class="field-label">Cover Image</label>
          <div class="image-upload-row">
            <div class="image-preview-box">
              <img v-if="imagePreview" :src="imagePreview" class="preview-img" alt="Preview" />
              <div v-else class="preview-placeholder">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              </div>
            </div>
            <label class="upload-btn btn-ghost">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Upload
              <input type="file" accept="image/*" @change="handleImage" class="hidden-file-input" />
            </label>
          </div>
        </div>

        <!-- Title -->
        <div class="field">
          <label class="field-label" for="job-title">Job Title <span class="required">*</span></label>
          <input id="job-title" v-model="title" placeholder="e.g. Senior Frontend Developer" />
        </div>

        <!-- Description -->
        <div class="field">
          <label class="field-label" for="job-desc">Description</label>
          <textarea id="job-desc" v-model="description" placeholder="Describe the role, responsibilities, and requirements…" rows="4" />
        </div>

        <!-- Statuses -->
        <div class="field">
          <label class="field-label">Status</label>
          <div class="chip-group">
            <button
              v-for="s in statuses"
              :key="s.id"
              type="button"
              class="chip"
              :class="{ 'chip-active': selectedStatuses.includes(s.id) }"
              @click="toggleStatus(s.id)"
            >{{ s.name }}</button>
          </div>
        </div>

        <!-- Categories -->
        <div class="field">
          <label class="field-label">Categories</label>
          <div class="chip-group">
            <button
              v-for="c in categories"
              :key="c.id"
              type="button"
              class="chip"
              :class="{ 'chip-active': selectedCategories.includes(c.id) }"
              @click="toggleCategory(c.id)"
            >{{ c.name }}</button>
          </div>
        </div>

        <!-- Location -->
        <div class="field">
          <label class="field-label">Location</label>
          <div class="field-row">
            <input v-model="city"  placeholder="City" />
            <input v-model="state" placeholder="State" style="max-width: 120px;" />
          </div>
          <input v-model="address" placeholder="Street address (optional)" style="margin-top: 8px;" />
        </div>

        <!-- Dates -->
        <div class="field">
          <label class="field-label">Date Range</label>
          <div class="field-row">
            <div class="date-group">
              <span class="date-label">From</span>
              <input type="date" v-model="startDate" />
            </div>
            <div class="date-group">
              <span class="date-label">To</span>
              <input type="date" v-model="endDate" />
            </div>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button class="btn-ghost" @click="emit('close')">Cancel</button>
        <button class="btn-primary" @click="submitJob" :disabled="loading">
          <span v-if="loading" class="btn-spinner"></span>
          {{ loading ? "Saving…" : isEditMode ? "Save Changes" : "Post Job" }}
        </button>
      </div>

    </div>
  </div>
</template>
