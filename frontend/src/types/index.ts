export type Role = 'customer' | 'merchant'

export interface User {
  id: number
  email: string
  name: string
  role: Role
  shop_name?: string | null
}

export interface Product {
  id: number
  name: string
  description: string
  category: string
  material: string | null
  price: number | null
  images: string[]
  status: string
  merchant_id: number
  merchant_name?: string | null
  shop_name?: string | null
  is_favorited?: boolean
}

export interface Favorite {
  id: number
  product: Product
}

export interface Inquiry {
  id: number
  message: string
  contact: string
  status: string
  user_id: number
  product_id: number
  merchant_id: number
  user_name?: string | null
  product_name?: string | null
}

export interface MerchantStats {
  product_count: number
  pending_inquiries: number
}

export const CATEGORIES = ['沙发', '床', '餐桌', '柜子', '桌椅'] as const
