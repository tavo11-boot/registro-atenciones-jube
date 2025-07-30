
-- Script SQL completo para MySQL
CREATE DATABASE IF NOT EXISTS jube_centro;
USE jube_centro;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'profesional') NOT NULL
);

CREATE TABLE profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    dni VARCHAR(8) UNIQUE,
    colegiatura VARCHAR(20),
    area ENUM('odontología', 'psicología', 'enfermería')
);

CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    dni VARCHAR(8) UNIQUE,
    edad INT,
    programa_estudios VARCHAR(100),
    semestre VARCHAR(10),
    turno VARCHAR(10)
);

CREATE TABLE atenciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    dni VARCHAR(8),
    edad INT,
    programa_estudios VARCHAR(100),
    semestre VARCHAR(10),
    turno VARCHAR(10),
    motivo TEXT,
    tratamiento TEXT,
    fecha_atencion DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_profesional INT,
    FOREIGN KEY (id_profesional) REFERENCES profesionales(id) ON DELETE CASCADE
);
