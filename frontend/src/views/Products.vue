<script setup>
import { ref, computed, onMounted } from 'vue'

const products = ref([])
const loading = ref(true)
const error = ref(null)

const searchQuery = ref('')
const showAddModal = ref(false)

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(p => p.name.toLowerCase().includes(query))
})

onMounted(async () => {
  try {
    const response = await fetch('/api/v1/products/?skip=0&limit=100')
    if (!response.ok) throw new Error('Failed to fetch products')
    const data = await response.json()
    products.value = data.products || data || []
  } catch (err) {
    console.warn('Backend not running. Using fallback data for products:', err.message)
    error.value = null
    products.value = [
      { id: 101, name: 'Premium Sidr Honey', category: 'Raw Honey', price: 120.00, stock: 45, is_active: true },
      { id: 102, name: 'Organic Royal Jelly', category: 'Supplements', price: 85.50, stock: 8, is_active: true },
      { id: 103, name: 'Beeswax Candles Set', category: 'Home', price: 25.00, stock: 0, is_active: false },
      { id: 104, name: 'Acacia Honey 500g', category: 'Raw Honey', price: 45.00, stock: 120, is_active: true }
    ]
  } finally {
    loading.value = false
  }
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price)
}
</script>

<template>
  <div class="products animate-fade-in">
    <header class="header">
      <div>
        <h1>{{ $t('products.title') }}</h1>
        <p>{{ $t('products.subtitle') }}</p>
      </div>
      <div class="header-actions">
        <input v-model="searchQuery" type="text" class="glass-input search-input" :placeholder="$t('products.searchPlaceholder')" />
        <button class="glass-button primary" @click="showAddModal = true">{{ $t('products.addBtn') }}</button>
      </div>
    </header>

    <div v-if="loading" class="state-message">{{ $t('products.loading') }}</div>
    <div v-else-if="error" class="state-message error">{{ error }}</div>
    
    <div v-else class="glass-panel table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>{{ $t('products.columns.id') }}</th>
            <th>{{ $t('products.columns.name') }}</th>
            <th>{{ $t('products.columns.category') }}</th>
            <th>{{ $t('products.columns.price') }}</th>
            <th>{{ $t('products.columns.stock') }}</th>
            <th>{{ $t('products.columns.status') }}</th>
            <th>{{ $t('products.columns.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>#{{ product.id }}</td>
            <td class="font-medium">{{ product.name }}</td>
            <td>{{ product.category || 'N/A' }}</td>
            <td class="price" dir="ltr">{{ formatPrice(product.price) }}</td>
            <td>
              <span :class="['stock-indicator', product.stock > 10 ? 'high' : 'low']">
                {{ product.stock }}
              </span>
            </td>
            <td>
              <span :class="['badge', product.is_active ? 'success' : 'danger']">
                {{ product.is_active ? $t('products.status.active') : $t('products.status.inactive') }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button class="glass-button small">{{ $t('products.actions.edit') }}</button>
                <button class="glass-button small danger-text">{{ $t('products.actions.delete') }}</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredProducts.length === 0">
            <td colspan="7" class="empty-state">{{ $t('products.empty') }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Product Modal -->
    <div v-if="showAddModal" class="modal-overlay animate-fade-in">
      <div class="glass-panel modal-content">
        <h2>{{ $t('products.modal.title') }}</h2>
        <form class="modal-form" @submit.prevent="showAddModal = false">
          <div class="form-group">
            <label>{{ $t('products.modal.nameLabel') }}</label>
            <input type="text" class="glass-input" required />
          </div>
          <div class="form-group">
            <label>{{ $t('products.modal.categoryLabel') }}</label>
            <input type="text" class="glass-input" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>{{ $t('products.modal.priceLabel') }}</label>
              <input type="number" step="0.01" class="glass-input" required />
            </div>
            <div class="form-group">
              <label>{{ $t('products.modal.stockLabel') }}</label>
              <input type="number" class="glass-input" required />
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" class="glass-button" @click="showAddModal = false">{{ $t('products.modal.cancel') }}</button>
            <button type="submit" class="glass-button primary">{{ $t('products.modal.save') }}</button>
          </div>
        </form>
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

.action-buttons {
  display: flex;
  gap: 8px;
}

.glass-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.danger-text {
  color: var(--danger);
  border-color: rgba(255, 51, 102, 0.3);
}

.danger-text:hover {
  background: rgba(255, 51, 102, 0.1);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  padding: 32px;
}

.modal-content h2 {
  margin-bottom: 24px;
  color: var(--text-primary);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
}

[dir="ltr"] .data-table {
  text-align: left;
}

.data-table th, .data-table td {
  padding: 16px 24px;
  border-bottom: 1px solid var(--glass-border);
}

.data-table th {
  color: var(--text-secondary);
  font-weight: 500;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  background: rgba(0, 0, 0, 0.2);
}

.data-table tbody tr {
  transition: background-color var(--transition-fast);
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.font-medium {
  font-weight: 500;
  color: var(--text-primary);
}

.price {
  font-family: monospace;
  font-size: 1.1rem;
  display: inline-block;
}

.stock-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.stock-indicator::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.stock-indicator.high::before { background: var(--success); box-shadow: 0 0 10px var(--success); }
.stock-indicator.low::before { background: var(--danger); box-shadow: 0 0 10px var(--danger); }

.state-message {
  padding: 48px;
  text-align: center;
  color: var(--text-secondary);
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px dashed var(--glass-border);
}

.state-message.error {
  color: var(--danger);
  border-color: rgba(255, 51, 102, 0.3);
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: var(--text-secondary);
  font-style: italic;
}
</style>
