CREATE TABLE "admin_users" (
  "admin_user_id" int,
  "login" varchar,
  "password_hash" varchar,
  "full_name" varchar,
  "role" varchar,
  "is_active" bool,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "admin_sessions" (
  "session_id" int,
  "admin_user_id" int,
  "token" varchar,
  "ip_address" varchar,
  "user_agent" varchar,
  "expires_at" datetime,
  "created_at" datetime
);

CREATE TABLE "audit_log" (
  "log_id" int,
  "admin_user_id" int,
  "action" varchar,
  "entity_type" varchar,
  "entity_id" int,
  "old_value" text,
  "new_value" text,
  "created_at" datetime
);

ALTER TABLE "admin_sessions" ADD FOREIGN KEY ("admin_user_id") REFERENCES "admin_users" ("admin_user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "audit_log" ADD FOREIGN KEY ("admin_user_id") REFERENCES "admin_users" ("admin_user_id") DEFERRABLE INITIALLY IMMEDIATE;