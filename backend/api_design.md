# 后端 API 接口设计规范 (RESTful) - 团队报名与支付

本文档描述了团队报名、验证码校验、支付订单的后端接口。
所有接口均返回 JSON 格式数据。

**基础 URL**: `/api/v1`

---

## 0. 跨域 (CORS) 约定
前端是静态 HTML，必须开启 CORS，否则浏览器会阻止请求。

建议后端配置允许以下内容：
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type`
- `Access-Control-Allow-Methods: GET, POST, PATCH, OPTIONS`

---

## 1. 验证码接口 (Public)

### 1.1 获取图片验证码
生成验证码并返回 `captcha_token` 与 Base64 图片。

- **URL**: `/captcha`
- **Method**: `GET`

**响应:**
```json
{
  "captcha_token": "b9a3f8c0e31a4f5a",
  "image_base64": "data:image/png;base64,iVBORw0KGgoAAA..."
}
```

---

## 2. 团队报名接口 (Public)

### 2.1 提交报名（含立即支付 / 延期支付）
前端表单填写完毕并上传文件（获取到文件 URL）后，调用此接口提交报名信息。

- **URL**: `/teams`
- **Method**: `POST`
- **Content-Type**: `application/json`

**请求体 (Request Body):**
```json
{
  "school": "XX大学",
  "advisor_name": "李老师",
  "advisor_phone": "13800000000",
  "leader_name": "张三",
  "leader_phone": "13900000000",
  "leader_qq": "12345678",
  "team_email": "team@example.com",
  "remark": "需要无障碍通道",
  "team_size": 6,
  "registration_form_url": "https://oss.example.com/uploads/team_form.pdf",
  "payment_mode": "immediate", 
  "captcha_token": "b9a3f8c0e31a4f5a",
  "captcha_code": "A7C9"
}
```

**响应 (立即支付):**
```json
{
  "message": "Team created",
  "data": {
    "team_id": 101,
    "payment_mode": "immediate",
    "payment_status": "pending",
    "order": {
      "order_id": 5002,
      "order_no": "MOCK202602040001",
      "qr_image_base64": "data:image/png;base64,iVBORw0KGgoAAA...",
      "qr_image_url": "/static/qr.png"
    }
  }
}
```

**响应 (延期支付):**
```json
{
  "message": "Team created",
  "data": {
    "team_id": 102,
    "payment_mode": "deferred",
    "payment_status": "unpaid"
  }
}
```

**常见错误:**
- `400 Bad Request`: 验证码错误或字段缺失
- `409 Conflict`: 重复提交（例如团队邮箱已存在）

---

## 3. 支付相关接口 (Public)

### 3.1 创建订单（可选）
当报名接口未生成订单时，可单独创建。

- **URL**: `/teams/{team_id}/payments`
- **Method**: `POST`

**响应:**
```json
{
  "message": "Payment created",
  "data": {
    "order_id": 5002,
    "order_no": "MOCK202602040001",
    "payment_status": "pending",
    "qr_image_base64": "data:image/png;base64,iVBORw0KGgoAAA...",
    "qr_image_url": "/static/qr.png"
  }
}
```

### 3.2 查询订单支付状态
前端可以使用轮询方式查询支付结果。

- **URL**: `/payments/{order_id}/status`
- **Method**: `GET`

**响应:**
```json
{
  "order_id": 5002,
  "order_no": "MOCK202602040001",
  "payment_status": "paid",
  "updated_at": "2026-02-04T10:00:00Z"
}
```

---

## 4. 管理后台接口 (Admin Only)
*注意：实际开发中需要添加鉴权（如 Token）。支付完成后由管理员手动更新状态。*

### 4.1 获取团队列表
- **URL**: `/admin/teams`
- **Method**: `GET`
- **Query Params**: `?payment_status=unpaid&page=1`

### 4.2 获取订单列表
- **URL**: `/admin/payments`
- **Method**: `GET`
- **Query Params**: `?payment_status=pending&page=1`

### 4.3 手动更新订单状态
- **URL**: `/admin/payments/{payment_id}/status`
- **Method**: `PATCH`

**请求体:**
```json
{
  "payment_status": "paid"
}
```

---

## 4. 管理后台接口 (Admin Only)
*注意：实际开发中需要添加鉴权（如 Token）。*

### 4.1 获取团队列表
- **URL**: `/admin/teams`
- **Method**: `GET`
- **Query Params**: `?payment_status=unpaid&page=1`

**响应:**
```json
{
  "total": 50,
  "page": 1,
  "data": [
    {
      "team_id": 101,
      "school": "XX大学",
      "leader_name": "张三",
      "team_email": "team@example.com",
      "payment_status": "paid"
    }
  ]
}
```

---

## 前端调用示例 (Native Fetch)

```javascript
// 1) 获取验证码
async function loadCaptcha() {
  const res = await fetch('http://your-backend-api.com/api/v1/captcha');
  const data = await res.json();
  document.getElementById('captchaImg').src = data.image_base64;
  document.getElementById('captchaToken').value = data.captcha_token;
}

// 2) 提交报名
async function submitTeam() {
  const body = {
    school: document.getElementById('school').value,
    advisor_name: document.getElementById('advisorName').value,
    advisor_phone: document.getElementById('advisorPhone').value,
    leader_name: document.getElementById('leaderName').value,
    leader_phone: document.getElementById('leaderPhone').value,
    leader_qq: document.getElementById('leaderQQ').value,
    team_email: document.getElementById('teamEmail').value,
    remark: document.getElementById('remark').value,
    team_size: Number(document.getElementById('teamSize').value),
    registration_form_url: document.getElementById('formUrl').value,
    payment_mode: document.querySelector('input[name="payMode"]:checked').value,
    captcha_token: document.getElementById('captchaToken').value,
    captcha_code: document.getElementById('captchaCode').value
  };

  const res = await fetch('http://your-backend-api.com/api/v1/teams', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  const data = await res.json();
  if (res.ok) {
    if (data.data.payment_mode === 'immediate') {
      window.location.href = data.data.order.payment_url;
    } else {
      alert('报名成功，等待缴费');
    }
  } else {
    alert(data.message || '提交失败');
  }
}
```
