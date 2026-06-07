<template>
  <div class="page-container">
    <h1 class="page-title">全部产品</h1>

    <div class="filters">
      <el-input
        v-model="filters.q"
        placeholder="搜索关键词"
        clearable
        style="width: 220px"
        @change="loadProducts"
      />
      <el-select
        v-model="filters.category"
        placeholder="分类"
        clearable
        style="width: 140px"
        @change="loadProducts"
      >
        <el-option v-for="cat in CATEGORIES" :key="cat" :label="cat" :value="cat" />
      </el-select>
      <el-input-number
        v-model="filters.min_price"
        :min="0"
        placeholder="最低价"
        controls-position="right"
        @change="loadProducts"
      />
      <el-input-number
        v-model="filters.max_price"
        :min="0"
        placeholder="最高价"
        controls-position="right"
        @change="loadProducts"
      />
      <el-button type="primary" @click="loadProducts">筛选</el-button>
    </div>

    <div v-loading="loading" class="product-grid">
      <ProductCard v-for="p in products" :key="p.id" :product="p" />
      <el-empty v-if="!loading && products.length === 0" description="暂无商品" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { productApi } from '@/api'
import { CATEGORIES } from '@/types'
import type { Product } from '@/types'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const products = ref<Product[]>([])
const loading = ref(false)

const filters = reactive({
  q: (route.query.q as string) || '',
  category: (route.query.category as string) || '',
  min_price: undefined as number | undefined,
  max_price: undefined as number | undefined,
})

async function loadProducts() {
  loading.value = true
  try {
    const params: Record<string, string | number> = {}
    if (filters.q) params.q = filters.q
    if (filters.category) params.category = filters.category
    if (filters.min_price != null) params.min_price = filters.min_price
    if (filters.max_price != null) params.max_price = filters.max_price
    const res = await productApi.list(params)
    products.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  align-items: center;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  min-height: 300px;
}
</style>
