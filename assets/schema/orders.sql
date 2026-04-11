CREATE TABLE "orders" (
  "order_id" int,
  "customer_name" varchar,
  "customer_phone" varchar,
  "customer_email" varchar,
  "comment" text,
  "status" varchar,
  "total_amount" float,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "order_items" (
  "item_id" int,
  "order_id" int,
  "good_id" int,
  "good_title" varchar,
  "good_sku" varchar,
  "price" float,
  "quantity" int,
  "subtotal" float
);

CREATE TABLE "order_status_history" (
  "history_id" int,
  "order_id" int,
  "old_status" varchar,
  "new_status" varchar,
  "changed_by" varchar,
  "change_reason" varchar,
  "changed_at" datetime
);

ALTER TABLE "order_items" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("order_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_status_history" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("order_id") DEFERRABLE INITIALLY IMMEDIATE;