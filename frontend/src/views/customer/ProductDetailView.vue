<template>
  <div v-loading="loading" class="page-container">
    <template v-if="product">
      <div class="detail-layout">
        <div class="gallery">
          <el-carousel v-if="product.images.length" height="400px" indicator-position="outside">
            <el-carousel-item v-for="(img, i) in product.images" :key="i">
              <img :src="resolveAssetUrl(img)" :alt="product.name" class="carousel-img" />
            </el-carousel-item>
          </el-carousel>
          <div v-else class="placeholder-img">
            <img src="https://placehold.co/600x400/F5E6D3/8B5A2B?text=家具" :alt="product.name" />
          </div>
        </div>

        <div class="info-panel">
          <h1>{{ product.name }}</h1>
          <div class="tags">
            <el-tag>{{ product.category }}</el-tag>
            <el-tag v-if="product.material" type="info">{{ product.material }}</el-tag>
          </div>
          <p v-if="product.price" class="price">¥{{ product.price.toLocaleString() }}</p>
          <p v-else class="price muted">价格面议</p>
          <p v-if="product.shop_name" class="shop">商家：{{ product.shop_name }}</p>
          <p class="description">{{ product.description }}</p>

          <div class="actions">
            <el-button
              v-if="auth.isCustomer"
              :type="product.is_favorited ? 'warning' : 'default'"
              :icon="product.is_favorited ? StarFilled : Star"
              @click="toggleFavorite"
            >
              {{ product.is_favorited ? '已收藏' : '收藏' }}
            </el-button>
            <el-button
              v-if="auth.isCustomer"
              type="primary"
              :icon="ChatDotRound"
              @click="openInquiry"
            >
              立即咨询
            </el-button>
            <el-button v-else-if="!auth.isLoggedIn" type="primary" @click="router.push('/login')">
              登录后咨询
            </el-button>
          </div>
        </div>
      </div>
    </template>

    <InquiryDialog ref="inquiryRef" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled, ChatDotRound } from '@element-plus/icons-vue'
import { productApi, favoriteApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { Product } from '@/types'
import InquiryDialog from '@/components/InquiryDialog.vue'
import { resolveAssetUrl } from '@/utils/asset'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const product = ref<Product | null>(null)
const loading = ref(false)
const inquiryRef = ref<InstanceType<typeof InquiryDialog>>()

async function loadProduct() {
  loading.value = true
  try {
    const res = await productApi.get(Number(route.params.id))
    product.value = res.data
  } catch {
    router.push('/products')
  } finally {
    loading.value = false
  }
}

async function toggleFavorite() {
  if (!product.value) return
  try {
    if (product.value.is_favorited) {
      await favoriteApi.remove(product.value.id)
      product.value.is_favorited = false
      ElMessage.success('已取消收藏')
    } else {
      await favoriteApi.add(product.value.id)
      product.value.is_favorited = true
      ElMessage.success('已加入收藏')
    }
  } catch {
    /* handled by interceptor */
  }
}

function openInquiry() {
  if (!product.value) return
  inquiryRef.value?.open(product.value.id, product.value.name)
}

onMounted(loadProduct)
</script>

<style scoped>
.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

@media (max-width: 768px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }
}

.carousel-img,
.placeholder-img img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
}

.placeholder-img {
  background: #f0e8dc;
  border-radius: 12px;
  overflow: hidden;
}

.info-panel h1 {
  font-size: 1.75rem;
  margin-bottom: 12px;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.price {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 8px;
}

.price.muted {
  font-size: 1.2rem;
}

.shop {
  color: var(--color-muted);
  margin-bottom: 16px;
}

.description {
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: 24px;
}

.actions {
  display: flex;
  gap: 12px;
}
</style>
