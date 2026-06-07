import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/CustomerLayout.vue'),
      children: [
        { path: '', name: 'home', component: () => import('@/views/customer/HomeView.vue') },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/views/customer/ProductListView.vue'),
        },
        {
          path: 'products/:id',
          name: 'product-detail',
          component: () => import('@/views/customer/ProductDetailView.vue'),
        },
        {
          path: 'favorites',
          name: 'favorites',
          meta: { requiresCustomer: true },
          component: () => import('@/views/customer/FavoritesView.vue'),
        },
        { path: 'login', name: 'login', component: () => import('@/views/customer/LoginView.vue') },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/customer/RegisterView.vue'),
        },
      ],
    },
    {
      path: '/merchant',
      component: () => import('@/layouts/MerchantLayout.vue'),
      meta: { requiresMerchant: true },
      children: [
        {
          path: '',
          name: 'merchant-dashboard',
          component: () => import('@/views/merchant/DashboardView.vue'),
        },
        {
          path: 'products',
          name: 'merchant-products',
          component: () => import('@/views/merchant/MerchantProductList.vue'),
        },
        {
          path: 'products/new',
          name: 'merchant-product-new',
          component: () => import('@/views/merchant/ProductFormView.vue'),
        },
        {
          path: 'products/:id/edit',
          name: 'merchant-product-edit',
          component: () => import('@/views/merchant/ProductFormView.vue'),
        },
        {
          path: 'inquiries',
          name: 'merchant-inquiries',
          component: () => import('@/views/merchant/InquiryListView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (auth.token && !auth.user) {
    await auth.fetchMe()
  }

  if (to.meta.requiresMerchant) {
    if (!auth.isLoggedIn) return { name: 'login', query: { redirect: to.fullPath } }
    if (!auth.isMerchant) return { name: 'home' }
  }

  if (to.meta.requiresCustomer) {
    if (!auth.isLoggedIn) return { name: 'login', query: { redirect: to.fullPath } }
    if (!auth.isCustomer) return { name: 'home' }
  }

  return true
})

export default router
