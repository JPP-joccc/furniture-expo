<template>
  <div>
    <h1 class="page-title">仪表盘</h1>
    <el-row :gutter="24" v-loading="loading">
      <el-col :span="12">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value">{{ stats?.product_count ?? 0 }}</div>
          <div class="stat-label">商品总数</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" class="stat-card pending">
          <div class="stat-value">{{ stats?.pending_inquiries ?? 0 }}</div>
          <div class="stat-label">待处理咨询</div>
        </el-card>
      </el-col>
    </el-row>
    <div class="quick-actions">
      <router-link to="/merchant/products/new">
        <el-button type="primary" :icon="Plus">新增商品</el-button>
      </router-link>
      <router-link to="/merchant/inquiries">
        <el-button :icon="ChatDotRound">查看咨询</el-button>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, ChatDotRound } from '@element-plus/icons-vue'
import { merchantApi } from '@/api'
import type { MerchantStats } from '@/types'

const stats = ref<MerchantStats | null>(null)
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await merchantApi.stats()
    stats.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stat-card {
  text-align: center;
  padding: 20px 0;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

.stat-card.pending .stat-value {
  color: #e6a23c;
}

.stat-label {
  color: var(--color-muted);
  margin-top: 8px;
}

.quick-actions {
  margin-top: 32px;
  display: flex;
  gap: 12px;
}
</style>
