<template>
  <el-dialog v-model="visible" title="咨询商品" width="480px" @closed="resetForm">
    <p v-if="productName" class="product-hint">咨询商品：{{ productName }}</p>
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="留言" prop="message">
        <el-input
          v-model="form.message"
          type="textarea"
          :rows="4"
          placeholder="请描述您的需求，如尺寸、颜色偏好等"
        />
      </el-form-item>
      <el-form-item label="联系方式" prop="contact">
        <el-input v-model="form.contact" placeholder="手机号或微信号" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="submit">提交咨询</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { inquiryApi } from '@/api'

const visible = ref(false)
const loading = ref(false)
const productId = ref(0)
const productName = ref('')
const formRef = ref<FormInstance>()

const form = reactive({
  message: '',
  contact: '',
})

const rules: FormRules = {
  message: [{ required: true, message: '请填写留言', trigger: 'blur' }],
  contact: [{ required: true, message: '请填写联系方式', trigger: 'blur' }],
}

function open(id: number, name: string) {
  productId.value = id
  productName.value = name
  visible.value = true
}

function resetForm() {
  form.message = ''
  form.contact = ''
  formRef.value?.resetFields()
}

async function submit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await inquiryApi.create({
      product_id: productId.value,
      message: form.message,
      contact: form.contact,
    })
    ElMessage.success('咨询已提交，商家将尽快联系您')
    visible.value = false
  } finally {
    loading.value = false
  }
}

defineExpose({ open })
</script>

<style scoped>
.product-hint {
  margin-bottom: 16px;
  color: var(--color-muted);
  font-size: 0.9rem;
}
</style>
