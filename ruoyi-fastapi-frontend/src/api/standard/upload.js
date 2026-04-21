import request from "@/utils/request";

// 查询待上传标准列表
export function listPendingStandard(query) {
  return request({
    url: "/standard/upload/list",
    method: "get",
    params: query,
  });
}

// 上传标准文件
export function uploadStandardFile(data) {
  return request({
    url: "/standard/upload",
    method: "post",
    data,
    timeout: 120000,
    headers: {
      "Content-Type": "multipart/form-data",
      repeatSubmit: false,
    },
  });
}
