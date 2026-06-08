<template>
  <div class="customer-layout">
    <header class="header">
      <div class="header-inner">
        <router-link to="/" class="logo" @click="menuOpen = false">
          <el-icon><House /></el-icon>
          <span>家私展览</span>
        </router-link>

        <nav class="nav nav-desktop">
          <router-link to="/">首页</router-link>
          <router-link to="/products">全部产品</router-link>
          <router-link v-if="auth.isCustomer" to="/favorites">我的收藏</router-link>
          <router-link v-if="auth.isMerchant" to="/merchant">商家后台</router-link>
        </nav>

        <div class="actions actions-desktop">
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

        <el-button class="menu-btn" :icon="Menu" circle @click="menuOpen = true" />
      </div>
    </header>

    <el-drawer v-model="menuOpen" direction="rtl" size="78%" title="菜单">
      <nav class="drawer-nav">
        <router-link to="/" @click="menuOpen = false">首页</router-link>
        <router-link to="/products" @click="menuOpen = false">全部产品</router-link>
        <router-link v-if="auth.isCustomer" to="/favorites" @click="menuOpen = false">
          我的收藏
        </router-link>
        <router-link v-if="auth.isMerchant" to="/merchant" @click="menuOpen = false">
          商家后台
        </router-link>
      </nav>
      <div class="drawer-actions">
        <template v-if="auth.isLoggedIn">
          <p class="drawer-user">你好，{{ auth.user?.name }}</p>
          <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
        </template>
        <template v-else>
          <router-link to="/login" @click="menuOpen = false">
            <el-button size="large" style="width: 100%">登录</el-button>
          </router-link>
          <router-link to="/register" @click="menuOpen = false">
            <el-button size="large" type="primary" style="width: 100%; margin-top: 12px">
              注册
            </el-button>
          </router-link>
        </template>
      </div>
    </el-drawer>

    <main class="main-content">
      <router-view />
    </main>

    <nav v-if="showTabBar" class="tab-bar">
      <router-link to="/" class="tab-item">
        <el-icon><House /></el-icon>
        <span>首页</span>
      </router-link>
      <router-link to="/products" class="tab-item">
        <el-icon><Grid /></el-icon>
        <span>分类</span>
      </router-link>
      <router-link
        :to="auth.isCustomer ? '/favorites' : '/login'"
        class="tab-item"
      >
        <el-icon><Star /></el-icon>
        <span>收藏</span>
      </router-link>
      <router-link
        :to="auth.isLoggedIn ? (auth.isMerchant ? '/merchant' : '/products') : '/login'"
        class="tab-item"
      >
        <el-icon><User /></el-icon>
        <span>{{ auth.isLoggedIn ? '我的' : '登录' }}</span>
      </router-link>
    </nav>

    <footer class="footer footer-desktop">
      <p>家私家具展览系统 · 发现理想家居</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Grid, House, Menu, Star, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const menuOpen = ref(false)

const hideTabBarRoutes = ['/login', '/register']
const showTabBar = computed(
  () =>
    !hideTabBarRoutes.includes(route.path) && !/^\/products\/\d+/.test(route.path),
)

function handleLogout() {
  auth.logout()
  menuOpen.value = false
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
  padding: 0 16px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
  flex-shrink: 0;
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

.menu-btn {
  margin-left: auto;
  display: none;
}

.main-content {
  flex: 1;
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.footer {
  text-align: center;
  padding: 24px;
  color: var(--color-muted);
  font-size: 0.875rem;
  border-top: 1px solid #e8dfd3;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.drawer-nav a {
  padding: 14px 12px;
  border-radius: 8px;
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--color-text);
}

.drawer-nav a.router-link-active {
  background: #f5ebe0;
  color: var(--color-primary);
}

.drawer-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e8dfd3;
}

.drawer-user {
  margin-bottom: 12px;
  color: var(--color-muted);
}

.tab-bar {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  border-top: 1px solid #e8dfd3;
  padding-bottom: env(safe-area-inset-bottom, 0);
  z-index: 100;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 8px 0 6px;
  font-size: 0.7rem;
  color: var(--color-muted);
}

.tab-item .el-icon {
  font-size: 1.35rem;
}

.tab-item.router-link-active {
  color: var(--color-primary);
}

@media (max-width: 768px) {
  .nav-desktop,
  .actions-desktop,
  .footer-desktop {
    display: none;
  }

  .menu-btn {
    display: inline-flex;
  }

  .tab-bar {
    display: flex;
  }

  .main-content {
    padding-bottom: calc(56px + env(safe-area-inset-bottom, 0));
  }
}

@media (min-width: 769px) {
  .header-inner {
    height: 64px;
    padding: 0 20px;
    gap: 32px;
  }

  .logo {
    font-size: 1.25rem;
  }
}
</style>
