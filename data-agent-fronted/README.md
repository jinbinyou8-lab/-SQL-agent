# SQL-Agent 前端

基于 Vue 3 + Vite 的问答界面,对接后端 `POST /api/query` 的 SSE 流。

## 功能

- 输入自然语言问题,回车或点击发送
- 实时展示 Agent 每个节点的执行进度(召回字段 → 合并信息 → 生成 SQL …)
- 结果以表格渲染,自动滚动到底部
- 执行期间按钮禁用,避免重复提交

## 开发

```bash
npm install
npm run dev
```

开发服务器默认 `http://localhost:5173`。`vite.config.js` 已把 `/api` 代理到 `http://localhost:8000`,所以需要先把后端跑起来:

```bash
# 在仓库根目录
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

如果后端换了端口,改 `vite.config.js` 里 `server.proxy["/api"].target`。

## 构建

```bash
npm run build      # 产物在 dist/
npm run preview    # 本地预览构建结果
```

## 与后端的约定

请求体:

```json
{ "query": "统计各分类销售商品数量" }
```

后端按 SSE 逐条推送,前端按 `type` 分流渲染:

| `type` | 处理方式 |
| --- | --- |
| `progress` | 追加/更新进度步骤,`status` 为 `running` / `success` / `error` |
| `result` | 把 `data`(行字典列表)渲染成表格,列名取首行对象的 keys |
