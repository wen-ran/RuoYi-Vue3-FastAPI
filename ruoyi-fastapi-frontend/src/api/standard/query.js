import request from "@/utils/request";

// 查询可打开的标准列表
export function listStandard(query) {
  return request({
    url: "/standard/query/list",
    method: "get",
    params: query,
  });
}

// 查询标准正文内容列表
export function listStandardContent(query) {
  return request({
    url: "/standard/query/content/list",
    method: "get",
    params: query,
  });
}
