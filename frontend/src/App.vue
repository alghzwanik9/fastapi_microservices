<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { watchEffect } from 'vue'

const { locale } = useI18n()

// Toggle language
const toggleLanguage = () => {
  locale.value = locale.value === 'en' ? 'ar' : 'en'
}

// Update direction
watchEffect(() => {
  document.documentElement.dir = locale.value === 'ar' ? 'rtl' : 'ltr'
  document.documentElement.lang = locale.value
})
</script>

<template>
  <nav class="sidebar">
    <div class="logo">
      <div class="logo-icon"></div>
      <h2>MicroAdmin</h2>
    </div>
    
    <div class="nav-links">
      <RouterLink to="/" class="nav-item" active-class="active">
        <i class="icon">📊</i> {{ $t('sidebar.dashboard') }}
      </RouterLink>
      <RouterLink to="/products" class="nav-item" active-class="active">
        <i class="icon">📦</i> {{ $t('sidebar.products') }}
      </RouterLink>
      <RouterLink to="/users" class="nav-item" active-class="active">
        <i class="icon">👥</i> {{ $t('sidebar.users') }}
      </RouterLink>
    </div>

    <div class="bottom-actions">
      <button @click="toggleLanguage" class="glass-button small lang-btn">
        🌍 {{ locale === 'ar' ? 'English' : 'عربي' }}
      </button>
    </div>
  </nav>

  <main class="main-content">
    <RouterView />
  </main>
</template>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--accent-gradient);
  box-shadow: var(--shadow-neon);
}

.logo h2 {
  color: var(--text-primary);
  font-size: 1.25rem;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-item.active {
  color: var(--text-primary);
  background: rgba(112, 0, 255, 0.1);
}

[dir="ltr"] .nav-item.active {
  border-right: 3px solid var(--accent-purple);
}

[dir="rtl"] .nav-item.active {
  border-left: 3px solid var(--accent-purple);
}

.icon {
  font-style: normal;
  font-size: 1.2rem;
}

.bottom-actions {
  margin-top: auto;
  padding-top: 24px;
}

.lang-btn {
  width: 100%;
  text-align: center;
}
</style>
