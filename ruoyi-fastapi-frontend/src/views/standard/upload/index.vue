<template>
  <div class="app-container">
    <el-form
      :model="queryParams"
      ref="queryRef"
      :inline="true"
      v-show="showSearch"
    >
      <el-form-item label="标准号" prop="standardNo">
        <el-input
          v-model="queryParams.standardNo"
          placeholder="请输入标准号"
          clearable
          style="width: 220px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="中文名" prop="nameZh">
        <el-input
          v-model="queryParams.nameZh"
          placeholder="请输入中文名"
          clearable
          style="width: 260px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="18">
        <el-alert
          title="仅显示已填写标准号、中文名且文件地址为空的标准。上传成功后会保存到本地，并回填文件地址。"
          type="info"
          show-icon
          :closable="false"
        />
      </el-col>
      <right-toolbar
        v-model:showSearch="showSearch"
        @queryTable="getList"
      ></right-toolbar>
    </el-row>

    <el-table
      v-loading="loading"
      :data="standardList"
      :row-key="getRowKey"
    >
      <el-table-column type="index" label="序号" width="70" align="center" />
      <el-table-column label="标准号" align="center" prop="standardNo" min-width="180" />
      <el-table-column
        label="中文名"
        align="left"
        prop="nameZh"
        min-width="320"
        show-overflow-tooltip
      />
      <el-table-column label="发布日期" align="center" prop="releaseDate" width="130">
        <template #default="scope">
          <span>{{ formatDate(scope.row.releaseDate) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="实施日期" align="center" prop="effectiveDate" width="130">
        <template #default="scope">
          <span>{{ formatDate(scope.row.effectiveDate) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center" prop="status" width="110" />
      <el-table-column
        label="操作"
        align="center"
        width="160"
        class-name="small-padding fixed-width"
        fixed="right"
      >
        <template #default="scope">
          <el-upload
            :show-file-list="false"
            :auto-upload="true"
            :http-request="(options) => handleUpload(options, scope.row)"
            :before-upload="handleBeforeUpload"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.zip,.rar"
            :disabled="uploadingKey === getRowKey(scope.row)"
          >
            <el-button
              link
              type="primary"
              icon="Upload"
              :loading="uploadingKey === getRowKey(scope.row)"
              v-hasPermi="['standard:upload:file']"
            >
              上传文件
            </el-button>
          </el-upload>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />
  </div>
</template>

<script setup name="StandardUpload">
import { listPendingStandard, uploadStandardFile } from "@/api/standard/upload";

const { proxy } = getCurrentInstance();

const standardList = ref([]);
const loading = ref(true);
const showSearch = ref(true);
const total = ref(0);
const uploadingKey = ref("");

const data = reactive({
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    standardNo: undefined,
    nameZh: undefined,
  },
});

const { queryParams } = toRefs(data);
// 允许上传的标准文件类型
const allowTypes = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "zip", "rar"];

/** 获取表格行唯一标识 */
function getRowKey(row) {
  return String(row.id ?? row.standardNo);
}

/** 格式化日期 */
function formatDate(value) {
  return value ? parseTime(value, "{y}-{m}-{d}") : "-";
}

/** 查询待上传标准列表 */
function getList() {
  loading.value = true;
  listPendingStandard(queryParams.value)
    .then((response) => {
      standardList.value = response.rows;
      total.value = response.total;
    })
    .finally(() => {
      loading.value = false;
    });
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 上传前校验文件格式和大小 */
function handleBeforeUpload(file) {
  const fileName = file.name || "";
  const fileExt = fileName.includes(".") ? fileName.split(".").pop().toLowerCase() : "";
  if (!allowTypes.includes(fileExt)) {
    proxy.$modal.msgError(`文件格式不正确，请上传 ${allowTypes.join("/")} 格式文件`);
    return false;
  }

  const isLt100M = file.size / 1024 / 1024 <= 100;
  if (!isLt100M) {
    proxy.$modal.msgError("上传文件大小不能超过 100 MB");
    return false;
  }

  return true;
}

/** 上传标准文件 */
function handleUpload(options, row) {
  const rowKey = getRowKey(row);
  const formData = new FormData();
  if (row.id !== undefined && row.id !== null) {
    formData.append("id", row.id);
  }
  formData.append("standardNo", row.standardNo);
  formData.append("file", options.file);
  uploadingKey.value = rowKey;

  return uploadStandardFile(formData)
    .then((response) => {
      options.onSuccess(response);
      proxy.$modal.msgSuccess("上传成功");
      getList();
    })
    .catch((error) => {
      options.onError(error);
    })
    .finally(() => {
      uploadingKey.value = "";
    });
}

getList();
</script>
