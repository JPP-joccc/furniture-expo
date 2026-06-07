<template>
  <div>
    <section class="hero">
      <div class="hero-content">
        <h1>发现理想家居</h1>
        <p>精选优质家具，打造温馨生活空间</p>
        <el-input
          v-model="searchQuery"
          placeholder="搜索家具名称..."
          size="large"
          class="search-input"
          @keyup.enter="goSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="goSearch">搜索</el-button>
          </template>
        </el-input>
      </div>
    </section>

    <section class="page-container">
      <h2 class="section-title">浏览分类</h2>
      <div class="categories">
        <router-link
          v-for="cat in CATEGORIES"
          :key="cat"
          :to="`/products?category=${cat}`"
          class="category-card"
        >
          <span>{{ cat }}</span>
        </router-link>
      </div>
    </section>

    <section class="page-container">
      <div class="section-header">
        <h2 class="section-title">精选商品</h2>
        <router-link to="/products" class="more-link">查看全部 →</router-link>
      </div>
      <div v-loading="loading" class="product-grid">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { productApi } from '@/api'
import { CATEGORIES } from '@/types'
import type { Product } from '@/types'
import ProductCard from '@/components/ProductCard.vue'

const router = useRouter()
const searchQuery = ref('')
const products = ref<Product[]>([])
const loading = ref(false)

function goSearch() {
  router.push({ path: '/products', query: searchQuery.value ? { q: searchQuery.value } : {} })
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await productApi.list()
    products.value = res.data.slice(0, 8)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #8b5a2b 0%, #d4a574 100%);
  color: #fff;
  padding: 80px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.hero-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 32px;
}

.search-input {
  max-width: 520px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.more-link {
  color: var(--color-primary);
  font-weight: 500;
}

.categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 48px;
}

.category-card {
  background: #fff;
  border: 1px solid #e8dfd3;
  border-radius: 12px;
  padding: 28px 16px;
  text-align: center;
  font-weight: 600;
  color: var(--color-primary);
  transition: all 0.2s;
}

.category-card:hover {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  min-height: 200px;
}
</style>
