<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">商品管理</h1>
      <router-link to="/merchant/products/new">
        <el-button type="primary" :icon="Plus">新增商品</el-button>
      </router-link>
    </div>

    <el-table v-loading="loading" :data="products" stripe>
      <el-table-column prop="name" label="名称" min-width="160" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column prop="material" label="材质" width="100" />
      <el-table-column label="价格" width="120">
        <template #default="{ row }">
          {{ row.price ? `¥${row.price.toLocaleString()}` : '面议' }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '上架中' : '已下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <router-link :to="`/merchant/products/${row.id}/edit`">
            <el-button size="small" text type="primary">编辑</el-button>
          </router-link>
          <el-button size="small" text type="danger" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { merchantApi } from '@/api'
import type { Product } from '@/types'

const products = ref<Product[]>([])
const loading = ref(false)

async function loadProducts() {
  loading.value = true
  try {
    const res = await merchantApi.products()
    products.value = res.data
  } finally {
    loading.value = false
  }
}

async function handleDelete(row: Product) {
  await ElMessageBox.confirm(`确定删除「${row.name}」？`, '确认删除', { type: 'warning' })
  await merchantApi.deleteProduct(row.id)
  ElMessage.success('已删除')
  loadProducts()
}

onMounted(loadProducts)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header .page-title {
  margin-bottom: 0;
}
</style>
