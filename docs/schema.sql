PRAGMA foreign_keys = ON;

CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    seed INTEGER,
    config_json TEXT,
    notes TEXT
);

CREATE TABLE wounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER,
    created_at TEXT NOT NULL,
    error_type TEXT NOT NULL,
    severity REAL NOT NULL CHECK (severity >= 0 AND severity <= 1),
    impact REAL NOT NULL CHECK (impact >= 0 AND impact <= 1),
    description TEXT,
    context_json TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id)
);

CREATE TABLE scars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    scar_pressure REAL NOT NULL,
    threshold REAL NOT NULL,
    formula_version TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('FORMING','ACTIVE','CONSOLIDATED','OBSOLETE','RETIRED')),
    description TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id),
    UNIQUE (experiment_id, name)
);

CREATE TABLE scar_wounds (
    scar_id INTEGER NOT NULL,
    wound_id INTEGER NOT NULL,
    contribution REAL,
    PRIMARY KEY (scar_id, wound_id),
    FOREIGN KEY (scar_id) REFERENCES scars(id) ON DELETE CASCADE,
    FOREIGN KEY (wound_id) REFERENCES wounds(id) ON DELETE CASCADE
);

CREATE TABLE capabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER,
    name TEXT NOT NULL,
    origin_scar_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('NACIENTE','ACTIVA','CONSOLIDADA','OBSOLETA','RETIRADA')),
    utility_score REAL DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    description TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id),
    FOREIGN KEY (origin_scar_id) REFERENCES scars(id),
    UNIQUE (experiment_id, name)
);

CREATE TABLE capability_usages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    capability_id INTEGER NOT NULL,
    used_at TEXT NOT NULL,
    success INTEGER NOT NULL CHECK (success IN (0,1)),
    error_avoided INTEGER CHECK (error_avoided IN (0,1)),
    context_json TEXT,
    notes TEXT,
    FOREIGN KEY (capability_id) REFERENCES capabilities(id) ON DELETE CASCADE
);

CREATE TABLE capability_state_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    capability_id INTEGER NOT NULL,
    previous_state TEXT,
    new_state TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY (capability_id) REFERENCES capabilities(id) ON DELETE CASCADE
);
