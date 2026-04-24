-- Run this once in cPanel phpMyAdmin or MySQL terminal
-- to create all required tables for the portfolio

CREATE TABLE IF NOT EXISTS bio (
    id          INT PRIMARY KEY DEFAULT 1,
    name        VARCHAR(255)    NOT NULL DEFAULT '',
    role        VARCHAR(255)    NOT NULL DEFAULT '',
    bio         TEXT,
    tagline     TEXT,
    github      VARCHAR(500)    DEFAULT '',
    linkedin    VARCHAR(500)    DEFAULT '',
    email       VARCHAR(255)    DEFAULT '',
    photo       LONGTEXT,
    updated_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Seed default bio
INSERT IGNORE INTO bio (id, name, role, bio, tagline)
VALUES (
    1,
    'Samuel Ojayhagbega',
    'AI Engineer · Embedded Systems',
    'I''m an engineer at the intersection of hardware and artificial intelligence. I build embedded systems that monitor critical infrastructure and develop AI-powered software that transforms raw telemetry into actionable insight.',
    'I design hardware that reads the physical world and build software that turns raw data into decisions.'
);

CREATE TABLE IF NOT EXISTS projects (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255)    NOT NULL,
    type        ENUM('hw','sw') NOT NULL DEFAULT 'sw',
    description TEXT,
    tags        TEXT,
    url         VARCHAR(500)    DEFAULT '',
    features    TEXT,
    sort_order  INT             DEFAULT 0,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- Seed default projects
INSERT IGNORE INTO projects (id, name, type, description, tags, features, sort_order) VALUES
(1, 'Power Monitoring System',   'hw', 'Real-time voltage, current, and power factor sensing with anomaly alerts and consumption logging for energy management.', 'Embedded C,ADC,RTOS,IoT', '', 1),
(2, 'Water Monitoring System',   'hw', 'Distributed sensors tracking flow rate, pressure, and water quality. Wireless telemetry with real-time leak detection.', 'Sensors,MQTT,Wireless', '', 2),
(3, 'Elevator Monitoring & Predictive Maintenance', 'hw', 'End-to-end condition monitoring capturing vibration, motor load, and door cycle data. Detects wear before failures occur.', 'Vibration,Edge ML,CAN Bus,Time Series', 'Motor current anomaly detection\nDoor cycle wear prediction\nRemote diagnostics dashboard\nMaintenance scheduling engine\nAlert & escalation pipeline', 3),
(4, 'RAG System from YouTube Videos', 'sw', 'Speech-to-text transcription pipeline feeding a retrieval-augmented Q&A interface. Query any video corpus with natural language.', 'RAG,Whisper,Vector DB,LLM', '', 4),
(5, 'LLM-Powered Chatbot',       'sw', 'Conversational AI assistant with context-aware memory and customisable personas. Designed for extensibility across deployment targets.', 'LLM,Prompt Eng.,API,NLP', '', 5),
(6, 'PowerLog — Generator Analytics Platform', 'sw', 'BI platform ingesting generator telemetry to track fuel consumption, runtime hours, and load profiles for fleet operators.', 'Data Pipeline,BI Dashboard,REST API,Analytics', 'Fuel efficiency benchmarking\nLoad profile visualisation\nPredictive refuelling alerts\nMulti-site fleet management\nCompliance report exports', 6);

CREATE TABLE IF NOT EXISTS posts (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(500)    NOT NULL,
    category    VARCHAR(255)    DEFAULT '',
    excerpt     TEXT,
    content     LONGTEXT,
    url         VARCHAR(500)    DEFAULT '',
    date        DATE,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- Migration: Add project detail columns
ALTER TABLE projects
  ADD COLUMN IF NOT EXISTS full_description TEXT,
  ADD COLUMN IF NOT EXISTS overview         TEXT,
  ADD COLUMN IF NOT EXISTS challenges       TEXT,
  ADD COLUMN IF NOT EXISTS outcome          TEXT,
  ADD COLUMN IF NOT EXISTS tech_stack       TEXT,
  ADD COLUMN IF NOT EXISTS code_snippets    JSON,
  ADD COLUMN IF NOT EXISTS images           JSON;
