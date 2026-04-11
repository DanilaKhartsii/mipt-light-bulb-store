CREATE TABLE "goods" (
  "good_id" int,
  "socle_id" int,
  "shape_id" int,
  "type_id" int,
  "suppliers_id" int,
  "title" varchar,
  "price" float,
  "quantity" int,
  "description" text,
  "size" float,
  "illumination" int,
  "power" int,
  "awaited_delivery_time" datetime,
  "is_visible" bool
);

CREATE TABLE "socle" (
  "socle_id" int,
  "title" varchar
);

CREATE TABLE "shape" (
  "shape_id" int,
  "title" varchar
);

CREATE TABLE "type" (
  "type_id" int,
  "title" varchar
);

CREATE TABLE "suppliers" (
  "supplier_id" int,
  "name" varchar
);

CREATE TABLE "suppliers_to_goods" (
  "suppliers_id" int,
  "good_id" int
);

ALTER TABLE "socle" ADD FOREIGN KEY ("socle_id") REFERENCES "goods" ("socle_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "goods" ADD FOREIGN KEY ("shape_id") REFERENCES "shape" ("shape_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "goods" ADD FOREIGN KEY ("type_id") REFERENCES "type" ("type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "suppliers" ADD FOREIGN KEY ("supplier_id") REFERENCES "suppliers_to_goods" ("suppliers_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "goods" ADD FOREIGN KEY ("good_id") REFERENCES "suppliers_to_goods" ("good_id") DEFERRABLE INITIALLY IMMEDIATE;
