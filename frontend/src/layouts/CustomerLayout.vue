<template>
  <div class="customer-layout">
    <header class="header">
      <div class="header-inner">
        <router-link to="/" class="logo">
          <el-icon><House /></el-icon>
          <span>家私展览</span>
        </router-link>
        <nav class="nav">
          <router-link to="/">首页</router-link>
          <router-link to="/products">全部产品</router-link>
          <router-link v-if="auth.isCustomer" to="/favorites">我的收藏</router-link>
          <router-link v-if="auth.isMerchant" to="/merchant">商家后台</router-link>
        </nav>
        <div class="actions">
          <template v-if="auth.isLoggedIn">
            <span class="user-name">{{ auth.user?.name }}</span>
            <el-button size="small" @click="handleLogout">退出</el-button>
          </template>
          <template v-else>
            <router-link to="/login">
              <el-button size="small">登录</el-button>
            </router-link>
            <router-link to="/register">
              <el-button size="small" type="primary">注册</el-button>
            </router-link>
          </template>
        </div>
      </div>
    </header>
    <main>
      <router-view />
    </main>
    <footer class="footer">
      <p>家私家具展览系统 · 发现理想家居</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.customer-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e8dfd3;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary);
}

.nav {
  display: flex;
  gap: 24px;
  flex: 1;
}

.nav a {
  color: var(--color-muted);
  font-weight: 500;
  transition: color 0.2s;
}

.nav a:hover,
.nav a.router-link-active {
  color: var(--color-primary);
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  color: var(--color-muted);
  font-size: 0.9rem;
}

main {
  flex: 1;
}

.footer {
  text-align: center;
  padding: 24px;
  color: var(--color-muted);
  font-size: 0.875rem;
  border-top: 1px solid #e8dfd3;
}
</style>
