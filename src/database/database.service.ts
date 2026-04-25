import { Injectable } from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';

type DatabaseHealthRow = {
  status: number;
};

@Injectable()
export class DatabaseService {
  constructor(@InjectDataSource() private readonly dataSource: DataSource) {}

  async health() {
    const rawResult: unknown =
      await this.dataSource.query('SELECT 1 AS status');
    const result = rawResult as DatabaseHealthRow[];

    return {
      connected: this.dataSource.isInitialized,
      driver: this.dataSource.options.type,
      result: result[0] ?? null,
    };
  }
}
