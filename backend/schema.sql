-- 数据库设计 (MySQL / PostgreSQL)
-- 创建数据库 (如果不存在)
-- CREATE DATABASE nova_payment_db;

-- =========================
-- MySQL 版本
-- =========================

-- 1. Teams 团队报名表
CREATE TABLE teams (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(150) NOT NULL,
    advisor_name VARCHAR(50) NOT NULL,
    advisor_phone VARCHAR(20) NOT NULL,
    leader_name VARCHAR(50) NOT NULL,
    leader_phone VARCHAR(20) NOT NULL,
    leader_qq VARCHAR(20) NOT NULL,
    team_email VARCHAR(120) NOT NULL,
    remark TEXT,
    team_size INT NOT NULL,
    registration_form_url TEXT NOT NULL,
    payment_mode ENUM('immediate', 'deferred') NOT NULL,
    payment_status ENUM('unpaid', 'paid', 'pending') NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Payments 支付订单表
CREATE TABLE payments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    team_id BIGINT NOT NULL,
    order_no VARCHAR(64) NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'CNY',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(50) DEFAULT 'mock',
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

-- 3. Captcha 图片验证码表
CREATE TABLE captcha (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(64) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL,
    request_ip VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引建议
CREATE INDEX idx_teams_email ON teams(team_email);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_captcha_expires ON captcha(expires_at);

-- =========================
-- PostgreSQL 版本
-- =========================

-- 1. Teams 团队报名表
CREATE TABLE teams (
    id BIGSERIAL PRIMARY KEY,
    school VARCHAR(150) NOT NULL,
    advisor_name VARCHAR(50) NOT NULL,
    advisor_phone VARCHAR(20) NOT NULL,
    leader_name VARCHAR(50) NOT NULL,
    leader_phone VARCHAR(20) NOT NULL,
    leader_qq VARCHAR(20) NOT NULL,
    team_email VARCHAR(120) NOT NULL,
    remark TEXT,
    team_size INT NOT NULL,
    registration_form_url TEXT NOT NULL,
    payment_mode VARCHAR(20) NOT NULL CHECK (payment_mode IN ('immediate', 'deferred')),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'unpaid' CHECK (payment_status IN ('unpaid', 'paid', 'pending')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Payments 支付订单表
CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    order_no VARCHAR(64) NOT NULL UNIQUE,
    amount NUMERIC(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'CNY',
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    payment_method VARCHAR(50) DEFAULT 'mock',
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Captcha 图片验证码表
CREATE TABLE captcha (
    id BIGSERIAL PRIMARY KEY,
    token VARCHAR(64) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL,
    request_ip VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引建议
CREATE INDEX idx_teams_email ON teams(team_email);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_captcha_expires ON captcha(expires_at);
