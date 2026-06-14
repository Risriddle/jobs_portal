<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from "chart.js";

import {
  Pie,
  Bar
} from "vue-chartjs";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

const statusChart = ref(null);
const cityChart = ref(null);
const stateChart = ref(null);

const loading = ref(true);

async function fetchAnalytics() {
  try {
    const response = await api.get("/analytics/");

    const data = response.data;

    statusChart.value = {
      labels: data.status_distribution.map(
        item => item.name
      ),
      datasets: [
        {
          data: data.status_distribution.map(
            item => item.total
          )
        }
      ]
    };

    cityChart.value = {
      labels: data.city_distribution.map(
        item => item.city
      ),
      datasets: [
        {
          label: "Jobs",
          data: data.city_distribution.map(
            item => item.total
          )
        }
      ]
    };

    stateChart.value = {
      labels: data.state_distribution.map(
        item => item.state
      ),
      datasets: [
        {
          label: "Jobs",
          data: data.state_distribution.map(
            item => item.total
          )
        }
      ]
    };

  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAnalytics);
</script>

<template>
  <div class="analytics-page">

    <h1>Analytics Dashboard</h1>

<router-link to="/">
  Back To Dashboard
</router-link>

    <div v-if="loading">
      Loading analytics...
    </div>

    <div
      v-else
      class="charts"
    >

      <div class="chart-card">
        <h2>Status Distribution</h2>

        <Pie
          :data="statusChart"
        />
      </div>

      <div class="chart-card">
        <h2>Jobs by City</h2>

        <Bar
          :data="cityChart"
        />
      </div>

      <div class="chart-card">
        <h2>Jobs by State</h2>

        <Bar
          :data="stateChart"
        />
      </div>

    </div>

  </div>
</template>

<style scoped>
.analytics-page {
  padding: 20px;
}

.charts {
  display: grid;
  gap: 30px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}
</style>