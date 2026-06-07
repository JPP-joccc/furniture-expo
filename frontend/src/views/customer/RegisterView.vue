<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <h2>注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="form.role">
            <el-radio value="customer">客户</el-radio>
            <el-radio value="merchant">商家</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item v-if="form.role === 'merchant'" label="店铺名" prop="shop_name">
          <el-input v-model="form.shop_name" />
        </el-form-item>
        <el-form-item v-if="form.role === 'merchant'" label="邀请码" prop="merchant_invite_code">
          <el-input v-model="form.merchant_invite_code" placeholder="向平台索取商家邀请码" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-button type="primary" class="submit-btn" :loading="loading" @click="submit">
          注册
        </el-button>
      </el-form>
      <p class="hint">
        已有账号？
        <router-link to="/login">去登录</router-link>
      </p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import type { Role } from '@/types'

const auth = useAuthStore()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  role: 'customer' as Role,
  name: '',
  shop_name: '',
  merchant_invite_code: '',
  email: '',
  password: '',
})

const rules: FormRules = {
  role: [{ required: true }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  shop_name: [
    {
      validator: (_r, v, cb) => {
        if (form.role === 'merchant' && !v) cb(new Error('商家需填写店铺名称'))
        else cb()
      },
      trigger: 'blur',
    },
  ],
  merchant_invite_code: [
    {
      validator: (_r, v, cb) => {
        if (form.role === 'merchant' && !v) cb(new Error('请输入商家邀请码'))
        else cb()
      },
      trigger: 'blur',
    },
  ],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少 8 位', trigger: 'blur' },
  ],
}

async function submit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const user = await auth.register({
      email: form.email,
      password: form.password,
      name: form.name,
      role: form.role,
      shop_name: form.role === 'merchant' ? form.shop_name : undefined,
      merchant_invite_code:
        form.role === 'merchant' ? form.merchant_invite_code : undefined,
    })
    ElMessage.success('注册成功')
    router.push(user.role === 'merchant' ? '/merchant' : '/')
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
  max-width: 480px;
  padding: 8px;
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: var(--color-primary);
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
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
</style>
