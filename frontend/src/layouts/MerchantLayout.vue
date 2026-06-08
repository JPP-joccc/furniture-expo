<template>
  <el-container class="merchant-layout">
    <el-aside width="220px" class="aside aside-desktop">
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

    <el-container class="content-wrap">
      <el-header class="header">
        <div class="header-left">
          <el-button class="menu-btn-mobile" :icon="Menu" circle @click="drawerOpen = true" />
          <span class="shop-name">{{ auth.user?.shop_name || auth.user?.name }}</span>
        </div>
        <div class="header-right">
          <router-link to="/">
            <el-button text>返回前台</el-button>
          </router-link>
          <el-button text type="danger" @click="handleLogout">退出</el-button>
        </div>
      </el-header>

      <el-drawer v-model="drawerOpen" direction="ltr" size="78%" title="商家菜单">
        <el-menu :default-active="activeMenu" router @select="drawerOpen = false">
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
      </el-drawer>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const drawerOpen = ref(false)

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
  height: 56px;
  padding: 0 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.shop-name {
  font-weight: 600;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.main {
  background: var(--color-bg);
  padding: 16px;
}

.menu-btn-mobile {
  display: none;
}

@media (max-width: 768px) {
  .aside-desktop {
    display: none;
  }

  .menu-btn-mobile {
    display: inline-flex;
  }

  .header-right :deep(.el-button) {
    padding: 8px;
    font-size: 0.85rem;
  }
}

@media (min-width: 769px) {
  .main {
    padding: 24px;
  }

  .header {
    height: 60px;
    padding: 0 20px;
  }
}
</style>
