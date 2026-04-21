<template>
  <div class="app-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="标准查询" name="standard">
        <el-form
          :model="standardQueryParams"
          ref="standardQueryRef"
          :inline="true"
          v-show="showSearch"
          label-width="68px"
        >
          <el-form-item label="标准号" prop="standardNo">
            <el-input
              v-model="standardQueryParams.standardNo"
              placeholder="请输入标准号"
              clearable
              style="width: 240px"
              @keyup.enter="handleStandardQuery"
            />
          </el-form-item>
          <el-form-item label="标准名" prop="nameZh">
            <el-input
              v-model="standardQueryParams.nameZh"
              placeholder="请输入标准名"
              clearable
              style="width: 260px"
              @keyup.enter="handleStandardQuery"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="Search" @click="handleStandardQuery">搜索</el-button>
            <el-button icon="Refresh" @click="resetStandardQuery">重置</el-button>
          </el-form-item>
        </el-form>

        <el-row :gutter="10" class="mb8">
          <el-col :span="18">
            <el-alert
              title="双击标准可打开文件。"
              type="info"
              show-icon
              :closable="false"
            />
          </el-col>
          <right-toolbar v-model:showSearch="showSearch" @queryTable="getStandardList"></right-toolbar>
        </el-row>

        <el-table
          v-loading="standardLoading"
          :data="standardList"
          :row-key="getStandardRowKey"
          :row-class-name="getOpenableRowClass"
          @row-dblclick="openStandard"
        >
          <el-table-column type="index" label="序号" width="70" align="center" />
          <el-table-column label="标准号" align="center" prop="standardNo" min-width="180" />
          <el-table-column
            label="标准名"
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
        </el-table>

        <pagination
          v-show="standardTotal > 0"
          :total="standardTotal"
          v-model:page="standardQueryParams.pageNum"
          v-model:limit="standardQueryParams.pageSize"
          @pagination="getStandardList"
        />
      </el-tab-pane>

      <el-tab-pane label="正文查询" name="content">
        <el-form
          :model="contentQueryParams"
          ref="contentQueryRef"
          :inline="true"
          v-show="showSearch"
          label-width="68px"
        >
          <el-form-item label="标准号" prop="standardNo">
            <el-input
              v-model="contentQueryParams.standardNo"
              placeholder="请输入标准号"
              clearable
              style="width: 220px"
              @keyup.enter="handleContentQuery"
            />
          </el-form-item>
          <el-form-item label="标准名" prop="nameZh">
            <el-input
              v-model="contentQueryParams.nameZh"
              placeholder="请输入标准名"
              clearable
              style="width: 240px"
              @keyup.enter="handleContentQuery"
            />
          </el-form-item>
          <el-form-item label="正文" prop="contentTextWithNo">
            <el-input
              v-model="contentQueryParams.contentTextWithNo"
              placeholder="请输入正文内容"
              clearable
              style="width: 300px"
              @keyup.enter="handleContentQuery"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="Search" @click="handleContentQuery">搜索</el-button>
            <el-button icon="Refresh" @click="resetContentQuery">重置</el-button>
          </el-form-item>
        </el-form>

        <el-row :gutter="10" class="mb8">
          <el-col :span="18">
            <el-alert
              title="双击正文可打开来源页。"
              type="info"
              show-icon
              :closable="false"
            />
          </el-col>
          <right-toolbar v-model:showSearch="showSearch" @queryTable="getContentList"></right-toolbar>
        </el-row>

        <el-table
          v-loading="contentLoading"
          :data="contentList"
          :row-key="getContentRowKey"
          :row-class-name="getOpenableRowClass"
          @row-dblclick="openContent"
        >
          <el-table-column type="index" label="序号" width="70" align="center" />
          <el-table-column label="标准号" align="center" prop="standardNo" min-width="170" />
          <el-table-column
            label="标准名"
            align="left"
            prop="nameZh"
            min-width="260"
            show-overflow-tooltip
          />
          <el-table-column label="来源页" align="center" prop="sourcePageNo" width="100" />
          <el-table-column label="条款号" align="center" prop="clauseNo" width="120" />
          <el-table-column
            label="正文内容"
            align="left"
            prop="contentTextWithNo"
            min-width="420"
            show-overflow-tooltip
          />
        </el-table>

        <pagination
          v-show="contentTotal > 0"
          :total="contentTotal"
          v-model:page="contentQueryParams.pageNum"
          v-model:limit="contentQueryParams.pageSize"
          @pagination="getContentList"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup name="StandardQuery">
import { listStandard, listStandardContent } from "@/api/standard/query";

const { proxy } = getCurrentInstance();

const activeTab = ref("standard");
const showSearch = ref(true);
const standardLoading = ref(false);
const contentLoading = ref(false);
const standardList = ref([]);
const contentList = ref([]);
const standardTotal = ref(0);
const contentTotal = ref(0);

const standardQueryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  standardNo: undefined,
  nameZh: undefined,
});

const contentQueryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  standardNo: undefined,
  nameZh: undefined,
  contentTextWithNo: undefined,
});

/** 获取标准行唯一标识 */
function getStandardRowKey(row) {
  return String(row.id ?? row.standardNo);
}

/** 获取正文行唯一标识 */
function getContentRowKey(row) {
  return String(row.id ?? `${row.standardNo}-${row.sourcePageNo}-${row.clauseNo}`);
}

/** 为可打开的行添加鼠标样式 */
function getOpenableRowClass({ row }) {
  return row.filePath ? "standard-openable-row" : "";
}

/** 格式化日期 */
function formatDate(value) {
  return value ? parseTime(value, "{y}-{m}-{d}") : "-";
}

/** 拼接标准文件访问地址 */
function buildFileUrl(filePath, pageNo) {
  if (!filePath) {
    return "";
  }

  const isAbsoluteUrl = /^https?:\/\//i.test(filePath);
  const baseApi = import.meta.env.VITE_APP_BASE_API || "";
  const normalizedPath = filePath.startsWith("/") ? filePath : `/${filePath}`;
  const rawUrl = isAbsoluteUrl ? filePath : `${baseApi}${normalizedPath}`;
  const urlWithoutHash = rawUrl.split("#")[0];
  const querySeparator = urlWithoutHash.includes("?") ? "&" : "?";
  let url = `${urlWithoutHash}${querySeparator}_openTime=${Date.now()}`;
  const normalizedPageNo = Number(pageNo);

  if (Number.isInteger(normalizedPageNo) && normalizedPageNo > 0) {
    url = `${url}#page=${normalizedPageNo}`;
  }

  return encodeURI(url);
}

/** 打开标准文件 */
function openFile(row, pageNo) {
  if (!row.filePath) {
    proxy.$modal.msgWarning("该标准暂无文件地址");
    return;
  }

  window.open(buildFileUrl(row.filePath, pageNo), "_blank");
}

/** 查询标准列表 */
function getStandardList() {
  standardLoading.value = true;
  listStandard(standardQueryParams)
    .then((response) => {
      standardList.value = response.rows || [];
      standardTotal.value = response.total || 0;
    })
    .finally(() => {
      standardLoading.value = false;
    });
}

/** 查询标准正文列表 */
function getContentList() {
  contentLoading.value = true;
  listStandardContent(contentQueryParams)
    .then((response) => {
      contentList.value = response.rows || [];
      contentTotal.value = response.total || 0;
    })
    .finally(() => {
      contentLoading.value = false;
    });
}

/** 标准搜索按钮操作 */
function handleStandardQuery() {
  standardQueryParams.pageNum = 1;
  getStandardList();
}

/** 正文搜索按钮操作 */
function handleContentQuery() {
  contentQueryParams.pageNum = 1;
  getContentList();
}

/** 标准重置按钮操作 */
function resetStandardQuery() {
  proxy.resetForm("standardQueryRef");
  handleStandardQuery();
}

/** 正文重置按钮操作 */
function resetContentQuery() {
  proxy.resetForm("contentQueryRef");
  handleContentQuery();
}

/** 标准行双击操作 */
function openStandard(row) {
  openFile(row, 1);
}

/** 正文行双击操作 */
function openContent(row) {
  openFile(row, row.sourcePageNo);
}
</script>

<style scoped>
:deep(.standard-openable-row) {
  cursor: pointer;
}
</style>
