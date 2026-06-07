<template>
  <router-link :to="`/products/${product.id}`" class="product-card">
    <div class="image-wrap">
      <img :src="coverImage" :alt="product.name" />
      <el-tag v-if="product.material" class="material-tag" size="small" effect="plain">
        {{ product.material }}
      </el-tag>
    </div>
    <div class="info">
      <h3>{{ product.name }}</h3>
      <p class="category">{{ product.category }}</p>
      <p v-if="product.price" class="price">¥{{ product.price.toLocaleString() }}</p>
      <p v-else class="price muted">价格面议</p>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Product } from '@/types'
import { resolveAssetUrl } from '@/utils/asset'

const props = defineProps<{ product: Product }>()

const coverImage = computed(() => {
  if (props.product.images?.length) return resolveAssetUrl(props.product.images[0])
  return 'https://placehold.co/400x300/F5E6D3/8B5A2B?text=家具'
})
</script>

<style scoped>
.product-card {
  display: block;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e8dfd3;
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(139, 90, 43, 0.12);
}

.image-wrap {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
  background: #f0e8dc;
}

.image-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.material-tag {
  position: absolute;
  top: 10px;
  left: 10px;
}

.info {
  padding: 16px;
}

.info h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category {
  font-size: 0.85rem;
  color: var(--color-muted);
  margin-bottom: 8px;
}

.price {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
}

.price.muted {
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
