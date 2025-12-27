import { sqliteTable, integer, text } from 'drizzle-orm/sqlite-core';

export const partners = sqliteTable('partners', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  type: text('type').notNull(),
  arr: integer('arr'),
  region: text('region'),
  status: text('status').default('Active'),
});
