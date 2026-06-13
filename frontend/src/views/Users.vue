<script setup>
import { ref, computed, onMounted } from 'vue'

const users = ref([])
const loading = ref(true)
const error = ref(null)

const searchQuery = ref('')

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(u => 
    u.full_name?.toLowerCase().includes(query) || 
    u.username.toLowerCase().includes(query) ||
    u.email.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  try {
    const response = await fetch('/api/v1/users/')
    if (!response.ok) {
      throw new Error('API route /api/v1/users/ not found or unauthorized')
    }
    const data = await response.json()
    users.value = data
  } catch (err) {
    console.warn('Using fallback data:', err.message)
    users.value = [
      { id: 1, username: 'admin', email: 'admin@micro.io', full_name: 'Super Admin', is_active: true, created_at: '2023-01-15T10:00:00Z', role: 'admin', total_orders: 14 },
      { id: 2, username: 'johndoe', email: 'john@example.com', full_name: 'John Doe', is_active: true, created_at: '2023-05-20T14:30:00Z', role: 'customer', total_orders: 5 },
      { id: 3, username: 'janedoe', email: 'jane@example.com', full_name: 'Jane Doe', is_active: false, created_at: '2023-06-10T09:15:00Z', role: 'customer', total_orders: 0 }
    ]
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

const getAvatarColor = (name) => {
  const colors = ['#7000ff', '#00f0ff', '#ff3366', '#00ff88', '#ffb800']
  const index = name.length % colors.length
  return colors[index]
}
</script>

<template>
  <div class="users animate-fade-in">
    <header class="header">
      <div>
        <h1>{{ $t('users.title') }}</h1>
        <p>{{ $t('users.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <input v-model="searchQuery" type="text" class="glass-input search-input" :placeholder="$t('users.searchPlaceholder')" />
        <button class="glass-button primary">{{ $t('users.inviteBtn') }}</button>
      </div>
    </header>

    <div v-if="loading" class="state-message">{{ $t('users.loading') }}</div>
    
    <div v-else class="users-grid">
      <div v-for="user in filteredUsers" :key="user.id" class="glass-panel user-card">
        <div class="user-header">
          <div class="avatar" :style="{ background: getAvatarColor(user.username) }">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>
          <div class="status-indicator">
            <span :class="['badge', user.is_active ? 'success' : 'danger']">
              {{ user.is_active ? $t('users.status.active') : $t('users.status.inactive') }}
            </span>
          </div>
        </div>
        
        <div class="user-info">
          <div class="name-row">
            <h3>{{ user.full_name || user.username }}</h3>
            <span v-if="user.role" :class="['role-badge', user.role === 'admin' ? 'role-admin' : 'role-customer']">
              {{ user.role === 'admin' ? $t('users.roles.admin') : $t('users.roles.customer') }}
            </span>
          </div>
          <p class="email" dir="ltr" style="text-align: start;">{{ user.email }}</p>
          <div class="username-badge" dir="ltr">@{{ user.username }}</div>
          <div class="user-stats" v-if="user.total_orders !== undefined">
            <span class="stat-item">{{ $t('users.stats.totalOrders') }} <strong>{{ user.total_orders }}</strong></span>
          </div>
        </div>

        <div class="user-footer">
          <div class="joined">{{ $t('users.joined') }} <span dir="ltr">{{ formatDate(user.created_at) }}</span></div>
          <button class="glass-button small">{{ $t('users.edit') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-input {
  width: 250px;
}

.name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.role-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  font-weight: 600;
  text-transform: uppercase;
}

.role-admin {
  background: rgba(112, 0, 255, 0.2);
  color: #b070ff;
  border: 1px solid rgba(112, 0, 255, 0.3);
}

.role-customer {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
  border: 1px solid var(--glass-border);
}

.user-stats {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.user-stats strong {
  color: var(--text-primary);
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.user-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.2);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-info h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.email {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.username-badge {
  display: inline-block;
  margin-top: 8px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-pill);
  font-size: 0.8rem;
  font-family: monospace;
  color: var(--accent-blue);
  align-self: flex-start;
}

[dir="rtl"] .username-badge {
  align-self: flex-end;
}

.user-footer {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px dashed var(--glass-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.joined {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.glass-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.state-message {
  padding: 48px;
  text-align: center;
  color: var(--text-secondary);
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px dashed var(--glass-border);
}
</style>
