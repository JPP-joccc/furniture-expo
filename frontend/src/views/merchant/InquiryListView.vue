<template>
  <div>
    <h1 class="page-title">咨询管理</h1>
    <el-table v-loading="loading" :data="inquiries" stripe>
      <el-table-column prop="product_name" label="商品" min-width="140" />
      <el-table-column prop="user_name" label="客户" width="100" />
      <el-table-column prop="contact" label="联系方式" width="140" />
      <el-table-column prop="message" label="留言" min-width="200" show-overflow-tooltip />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'pending' ? 'warning' : 'success'">
            {{ row.status === 'pending' ? '待处理' : '已回复' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending'"
            size="small"
            type="primary"
            text
            @click="markReplied(row)"
          >
            标记已回复
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && inquiries.length === 0" description="暂无咨询" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { merchantApi } from '@/api'
import type { Inquiry } from '@/types'

const inquiries = ref<Inquiry[]>([])
const loading = ref(false)

async function loadInquiries() {
  loading.value = true
  try {
    const res = await merchantApi.inquiries()
    inquiries.value = res.data
  } finally {
    loading.value = false
  }
}

async function markReplied(row: Inquiry) {
  await merchantApi.updateInquiry(row.id, 'replied')
  ElMessage.success('已标记为已回复')
  loadInquiries()
}

onMounted(loadInquiries)
</script>
