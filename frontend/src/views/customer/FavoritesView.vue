<template>
  <div class="page-container">
    <h1 class="page-title">我的收藏</h1>
    <div v-loading="loading" class="product-grid">
      <ProductCard v-for="fav in favorites" :key="fav.id" :product="fav.product" />
      <el-empty v-if="!loading && favorites.length === 0" description="暂无收藏" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { favoriteApi } from '@/api'
import type { Favorite } from '@/types'
import ProductCard from '@/components/ProductCard.vue'

const favorites = ref<Favorite[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await favoriteApi.list()
    favorites.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  min-height: 200px;
}
</style>
