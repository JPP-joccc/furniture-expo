<template>
  <div class="page-container">
    <h1 class="page-title">全部产品</h1>

    <div class="search-row">
      <el-input
        v-model="filters.q"
        placeholder="搜索家具..."
        clearable
        size="large"
        class="search-input"
        @change="loadProducts"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-button class="filter-btn-mobile" :icon="Filter" @click="filterOpen = true">
        筛选
      </el-button>
    </div>

    <div class="filters filters-desktop">
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

    <el-drawer v-model="filterOpen" direction="btt" size="auto" title="筛选条件">
      <el-form label-position="top">
        <el-form-item label="分类">
          <el-select v-model="filters.category" placeholder="全部分类" clearable style="width: 100%">
            <el-option v-for="cat in CATEGORIES" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格区间">
          <div class="price-range">
            <el-input-number v-model="filters.min_price" :min="0" placeholder="最低" controls-position="right" />
            <span>—</span>
            <el-input-number v-model="filters.max_price" :min="0" placeholder="最高" controls-position="right" />
          </div>
        </el-form-item>
        <el-button type="primary" size="large" style="width: 100%" @click="applyFilter">
          应用筛选
        </el-button>
      </el-form>
    </el-drawer>

    <div v-loading="loading" class="product-grid">
      <ProductCard v-for="p in products" :key="p.id" :product="p" />
      <el-empty v-if="!loading && products.length === 0" description="暂无商品" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Filter, Search } from '@element-plus/icons-vue'
import { productApi } from '@/api'
import { CATEGORIES } from '@/types'
import type { Product } from '@/types'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const products = ref<Product[]>([])
const loading = ref(false)
const filterOpen = ref(false)

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

function applyFilter() {
  filterOpen.value = false
  loadProducts()
}

onMounted(loadProducts)
</script>

<style scoped>
.search-row {
  display: none;
  gap: 10px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
}

.filter-btn-mobile {
  flex-shrink: 0;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  align-items: center;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  min-height: 300px;
}

@media (max-width: 768px) {
  .search-row {
    display: flex;
  }

  .filters-desktop {
    display: none;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .page-title {
    font-size: 1.35rem;
    margin-bottom: 12px;
  }
}
</style>
