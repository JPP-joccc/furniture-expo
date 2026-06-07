import client from './client'
import type { Favorite, Inquiry, MerchantStats, Product, Role, User } from '@/types'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  name: string
  role: Role
  shop_name?: string
  merchant_invite_code?: string
}

export interface ProductFilters {
  category?: string
  q?: string
  min_price?: number
  max_price?: number
}

export interface ProductPayload {
  name: string
  description: string
  category: string
  material?: string
  price?: number
  images: string[]
  status?: string
}

export const authApi = {
  login: (data: LoginPayload) =>
    client.post<{ access_token: string; user: User }>('/api/auth/login', data),
  register: (data: RegisterPayload) =>
    client.post<{ access_token: string; user: User }>('/api/auth/register', data),
  me: () => client.get<User>('/api/auth/me'),
}

export const productApi = {
  list: (params?: ProductFilters) =>
    client.get<Product[]>('/api/products', { params }),
  get: (id: number) => client.get<Product>(`/api/products/${id}`),
}

export const favoriteApi = {
  list: () => client.get<Favorite[]>('/api/favorites'),
  add: (product_id: number) =>
    client.post<Favorite>('/api/favorites', { product_id }),
  remove: (product_id: number) =>
    client.delete(`/api/favorites/${product_id}`),
}

export const inquiryApi = {
  create: (data: { product_id: number; message: string; contact: string }) =>
    client.post<Inquiry>('/api/inquiries', data),
}

export const merchantApi = {
  stats: () => client.get<MerchantStats>('/api/merchant/stats'),
  products: () => client.get<Product[]>('/api/merchant/products'),
  createProduct: (data: ProductPayload) =>
    client.post<Product>('/api/merchant/products', data),
  updateProduct: (id: number, data: Partial<ProductPayload>) =>
    client.put<Product>(`/api/merchant/products/${id}`, data),
  deleteProduct: (id: number) => client.delete(`/api/merchant/products/${id}`),
  inquiries: () => client.get<Inquiry[]>('/api/merchant/inquiries'),
  updateInquiry: (id: number, status: string) =>
    client.patch<Inquiry>(`/api/merchant/inquiries/${id}`, { status }),
  upload: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return client.post<{ url: string }>('/api/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
