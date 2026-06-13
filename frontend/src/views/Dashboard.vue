<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const stats = computed(() => [
  { title: t('dashboard.stats.totalProducts'), value: '1,234', trend: '+12%', color: 'var(--accent-purple)' },
  { title: t('dashboard.stats.activeUsers'), value: '892', trend: '+5%', color: 'var(--accent-blue)' },
  { title: t('dashboard.stats.newOrders'), value: '156', trend: '+24%', color: 'var(--success)' },
  { title: t('dashboard.stats.revenue'), value: '$12.4k', trend: '+18%', color: 'var(--warning)' }
])

const recentActivities = computed(() => [
  { id: 1, text: 'New order #1024 placed', time: '5 mins ago', type: 'order' },
  { id: 2, text: 'User Sarah registered', time: '1 hour ago', type: 'user' },
  { id: 3, text: 'Product "Honey Jar" stock updated', time: '2 hours ago', type: 'product' },
  { id: 4, text: 'New order #1023 placed', time: '5 hours ago', type: 'order' }
])

const topProducts = computed(() => [
  { id: 1, name: 'Premium Sidr Honey', sales: 145, revenue: '$4,350' },
  { id: 2, name: 'Organic Royal Jelly', sales: 98, revenue: '$2,450' },
  { id: 3, name: 'Beeswax Candles Set', sales: 74, revenue: '$1,110' }
])
</script>

<template>
  <div class="dashboard animate-fade-in">
    <header class="header">
      <div>
        <h1>{{ $t('dashboard.title') }}</h1>
        <p>{{ $t('dashboard.subtitle') }}</p>
      </div>
    </header>

    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.title" class="glass-panel stat-card">
        <h3>{{ stat.title }}</h3>
        <div class="stat-value" :style="{ color: stat.color }">{{ stat.value }}</div>
        <div class="stat-trend"><span dir="ltr">{{ stat.trend }}</span> {{ $t('dashboard.stats.thisMonth') }}</div>
      </div>
    </div>

    <div class="dashboard-widgets">
      <div class="glass-panel widget">
        <h3>{{ $t('dashboard.recentActivities') }}</h3>
        <ul class="activity-list">
          <li v-for="activity in recentActivities" :key="activity.id" class="activity-item">
            <span class="activity-icon" :class="activity.type"></span>
            <div class="activity-details">
              <p class="activity-text" dir="ltr">{{ activity.text }}</p>
              <span class="activity-time" dir="ltr">{{ activity.time }}</span>
            </div>
          </li>
        </ul>
      </div>

      <div class="glass-panel widget">
        <h3>{{ $t('dashboard.topProducts') }}</h3>
        <ul class="top-products-list">
          <li v-for="product in topProducts" :key="product.id" class="top-product-item">
            <div class="product-info">
              <span class="product-name" dir="ltr">{{ product.name }}</span>
              <span class="product-sales" dir="ltr">{{ product.sales }} sales</span>
            </div>
            <span class="product-revenue" dir="ltr">{{ product.revenue }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.stat-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-card h3 {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.stat-trend {
  font-size: 0.85rem;
  color: var(--success);
}

.dashboard-widgets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-top: 32px;
}

.widget {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.widget h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  border-bottom: 1px solid var(--glass-border);
  padding-bottom: 12px;
}

.activity-list, .top-products-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.activity-icon {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 6px;
}

.activity-icon.order { background: var(--success); box-shadow: 0 0 8px var(--success); }
.activity-icon.user { background: var(--accent-blue); box-shadow: 0 0 8px var(--accent-blue); }
.activity-icon.product { background: var(--warning); box-shadow: 0 0 8px var(--warning); }

.activity-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.activity-text {
  color: var(--text-primary);
  font-size: 0.95rem;
  margin: 0;
}

.activity-time {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.top-product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast);
}

.top-product-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.95rem;
}

.product-sales {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.product-revenue {
  font-family: monospace;
  font-size: 1.1rem;
  color: var(--accent-purple);
  font-weight: 600;
}
</style>
