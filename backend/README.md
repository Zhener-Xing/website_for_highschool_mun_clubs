# NOVA 团队报名后端 (FastAPI)

这是一个面向静态前端的报名与支付（模拟二维码）后端服务，支持：
- 图片验证码
- 团队报名
- 立即支付（返回二维码）与延期支付
- 管理员手动更新订单状态
- CORS 跨域

## 1. 目录结构
```
backend/
├── app/
│   ├── assets/           # 静态资源（qr.png）
│   ├── routers/          # 路由
│   ├── crud.py           # 数据库操作
│   ├── database.py       # 数据库连接
│   ├── main.py           # 应用入口
│   ├── models.py         # ORM 模型
│   ├── schemas.py        # 数据校验
│   └── utils.py          # 工具函数
├── requirements.txt
├── schema.sql
└── api_design.md
```

## 2. 运行前准备
- Python 3.10+
- 建议使用虚拟环境（venv）

## 3. 环境安装
1) 安装依赖：
- `pip install -r requirements.txt`

2) 可选：放置二维码图片
- 将二维码图片保存为 `backend/app/assets/qr.png`
- 如果未提供，系统会自动生成模拟二维码

## 4. 启动服务
- `uvicorn app.main:app --reload`

启动后：
- API 地址：`http://127.0.0.1:8000`
- 文档：`http://127.0.0.1:8000/docs`

## 5. 主要接口
- `GET /api/v1/captcha` 获取验证码
- `POST /api/v1/teams` 提交报名
- `GET /api/v1/payments/{payment_id}/status` 查询支付状态
- `PATCH /api/v1/admin/payments/{payment_id}/status` 管理员手动更新支付状态

详细接口说明见 [api_design.md](api_design.md)
