<template>
  <el-container class="merchant-layout">
    <el-aside width="220px" class="aside">
      <div class="brand">
        <el-icon><Shop /></el-icon>
        <span>商家后台</span>
      </div>
      <el-menu :default-active="activeMenu" router>
        <el-menu-item index="/merchant">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/merchant/products">
          <el-icon><Goods /></el-icon>
          <span>商品管理</span>
        </el-menu-item>
        <el-menu-item index="/merchant/inquiries">
          <el-icon><ChatDotRound /></el-icon>
          <span>咨询管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <span class="shop-name">{{ auth.user?.shop_name || auth.user?.name }}</span>
        </div>
        <div class="header-right">
          <router-link to="/">
            <el-button text>返回前台</el-button>
          </router-link>
          <el-button text type="danger" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => {
  if (route.path.startsWith('/merchant/products')) return '/merchant/products'
  if (route.path.startsWith('/merchant/inquiries')) return '/merchant/inquiries'
  return '/merchant'
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.merchant-layout {
  min-height: 100vh;
}

.aside {
  background: #fff;
  border-right: 1px solid #e8dfd3;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
  border-bottom: 1px solid #e8dfd3;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e8dfd3;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.shop-name {
  font-weight: 600;
  color: var(--color-text);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.main {
  background: var(--color-bg);
  padding: 24px;
}
</style>
