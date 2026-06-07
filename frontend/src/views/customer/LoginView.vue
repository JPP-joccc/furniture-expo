<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <h2>登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0">
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
            @keyup.enter="submit"
          />
        </el-form-item>
        <el-button type="primary" size="large" class="submit-btn" :loading="loading" @click="submit">
          登录
        </el-button>
      </el-form>
      <p class="hint">
        还没有账号？
        <router-link to="/register">立即注册</router-link>
      </p>
      <el-divider>演示账号</el-divider>
      <p class="demo">客户：customer@demo.com / Demo12345</p>
      <p class="demo">商家：merchant@demo.com / Demo12345</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({ email: '', password: '' })

const rules: FormRules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function submit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const user = await auth.login(form)
    ElMessage.success('登录成功')
    const redirect = (route.query.redirect as string) || (user.role === 'merchant' ? '/merchant' : '/')
    router.push(redirect)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 8px;
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: var(--color-primary);
}

.submit-btn {
  width: 100%;
}

.hint {
  text-align: center;
  margin-top: 16px;
  color: var(--color-muted);
  font-size: 0.9rem;
}

.hint a {
  color: var(--color-primary);
}

.demo {
  font-size: 0.85rem;
  color: var(--color-muted);
  text-align: center;
}
</style>
