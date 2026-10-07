-- SmartStock schema for MySQL / MariaDB (phpMyAdmin, XAMPP).
-- Import this file in phpMyAdmin. It creates an isolated database and does not
-- drop or overwrite existing tables.
CREATE DATABASE IF NOT EXISTS `smartstock_inventory`
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `smartstock_inventory`;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) NULL DEFAULT 'admin',
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_categories_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `suppliers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `company` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(30) NOT NULL,
  `email` VARCHAR(120) NULL,
  `address` TEXT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `category_id` INT NOT NULL,
  `supplier_id` INT NULL,
  `purchase_price` FLOAT NULL DEFAULT 0,
  `selling_price` FLOAT NULL DEFAULT 0,
  `stock_quantity` INT NULL DEFAULT 0,
  `minimum_stock` INT NULL DEFAULT 10,
  `status` VARCHAR(30) NULL DEFAULT 'In Stock',
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_products_category_id` (`category_id`),
  KEY `ix_products_supplier_id` (`supplier_id`),
  CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`)
    REFERENCES `categories` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT `fk_products_supplier` FOREIGN KEY (`supplier_id`)
    REFERENCES `suppliers` (`id`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(30) NOT NULL,
  `email` VARCHAR(120) NULL,
  `address` TEXT NULL,
  `total_purchases` INT NULL DEFAULT 0,
  `total_spent` FLOAT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `sales` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `invoice_number` VARCHAR(40) NOT NULL,
  `customer_id` INT NOT NULL,
  `subtotal` FLOAT NULL DEFAULT 0,
  `discount` FLOAT NULL DEFAULT 0,
  `tax` FLOAT NULL DEFAULT 0,
  `total_amount` FLOAT NULL DEFAULT 0,
  `payment_method` VARCHAR(30) NULL DEFAULT 'UPI',
  `status` VARCHAR(20) NULL DEFAULT 'Paid',
  `sale_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sales_invoice_number` (`invoice_number`),
  KEY `ix_sales_customer_id` (`customer_id`),
  CONSTRAINT `fk_sales_customer` FOREIGN KEY (`customer_id`)
    REFERENCES `customers` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inventory_records` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_id` INT NOT NULL,
  `movement_type` VARCHAR(20) NOT NULL DEFAULT 'stock_in',
  `quantity` INT NULL DEFAULT 0,
  `unit_price` FLOAT NULL DEFAULT 0,
  `note` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_inventory_records_product_id` (`product_id`),
  KEY `ix_inventory_records_created_at` (`created_at`),
  CONSTRAINT `fk_inventory_records_product` FOREIGN KEY (`product_id`)
    REFERENCES `products` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
