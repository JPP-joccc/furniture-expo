<template>
  <div>
    <h1 class="page-title">{{ isEdit ? '编辑商品' : '新增商品' }}</h1>
    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" style="max-width: 640px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" style="width: 100%">
            <el-option v-for="cat in CATEGORIES" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="材质" prop="material">
          <el-input v-model="form.material" />
        </el-form-item>
        <el-form-item label="参考价" prop="price">
          <el-input-number v-model="form.price" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">上架</el-radio>
            <el-radio value="inactive">下架</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="图片">
          <div class="upload-area">
            <el-upload
              :show-file-list="false"
              :http-request="handleUpload"
              accept="image/*"
            >
              <el-button :icon="Upload">上传图片</el-button>
            </el-upload>
            <div v-if="form.images.length" class="image-list">
              <div v-for="(img, i) in form.images" :key="i" class="image-item">
                <img :src="resolveAssetUrl(img)" alt="product" />
                <el-button
                  class="remove-btn"
                  type="danger"
                  :icon="Delete"
                  circle
                  size="small"
                  @click="form.images.splice(i, 1)"
                />
              </div>
            </div>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="submit">保存</el-button>
          <router-link to="/merchant/products">
            <el-button>取消</el-button>
          </router-link>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules, type UploadRequestOptions } from 'element-plus'
import { Upload, Delete } from '@element-plus/icons-vue'
import { merchantApi } from '@/api'
import { CATEGORIES } from '@/types'
import { resolveAssetUrl } from '@/utils/asset'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const saving = ref(false)

const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const productId = computed(() => Number(route.params.id))

const form = reactive({
  name: '',
  description: '',
  category: '',
  material: '',
  price: undefined as number | undefined,
  images: [] as string[],
  status: 'active',
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
}

async function handleUpload(options: UploadRequestOptions) {
  const res = await merchantApi.upload(options.file as File)
  form.images.push(res.data.url)
  ElMessage.success('上传成功')
}

async function loadProduct() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const res = await merchantApi.products()
    const product = res.data.find((p) => p.id === productId.value)
    if (!product) {
      router.push('/merchant/products')
      return
    }
    form.name = product.name
    form.description = product.description
    form.category = product.category
    form.material = product.material || ''
    form.price = product.price ?? undefined
    form.images = [...product.images]
    form.status = product.status
  } finally {
    loading.value = false
  }
}

async function submit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    const payload = {
      name: form.name,
      description: form.description,
      category: form.category,
      material: form.material || undefined,
      price: form.price,
      images: form.images,
      status: form.status,
    }
    if (isEdit.value) {
      await merchantApi.updateProduct(productId.value, payload)
      ElMessage.success('更新成功')
    } else {
      await merchantApi.createProduct(payload)
      ElMessage.success('创建成功')
    }
    router.push('/merchant/products')
  } finally {
    saving.value = false
  }
}

onMounted(loadProduct)
</script>

<style scoped>
.upload-area {
  width: 100%;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}

.image-item {
  position: relative;
  width: 100px;
  height: 100px;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e8dfd3;
}

.remove-btn {
  position: absolute;
  top: -8px;
  right: -8px;
}
</style>
