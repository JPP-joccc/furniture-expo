const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

/** 将 /uploads/... 转为可访问的完整地址（部署到 Vercel 时需要） */
export function resolveAssetUrl(path: string): string {
  if (!path) return path
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return `${API_BASE}${path}`
}
